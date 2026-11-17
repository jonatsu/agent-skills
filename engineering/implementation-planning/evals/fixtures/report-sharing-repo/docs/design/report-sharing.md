# Design: Report Sharing

Status: Accepted (approved 2026-09-02)

Implements: [report sharing specification](../specs/report-sharing.md), revision 1.

## Overview

Sharing adds a `shares` table for named users and a `public_links` table for anonymous links. `can_view` consults
both. Every change writes an audit event.

## Decisions

### D1. Named-user shares

Table `shares(report_id, user_id, role, created_by, created_at)` with primary key `(report_id, user_id)`. `role` is
`viewer` or `editor`. `can_view` returns True for the owner or any user with a share row; `editor` grants no more
than `viewer` here, because editing is out of scope. Shares are limited to users in the owner's organization, which the
host reports through `Directory.organization_of(user_id) -> str | None`, a protocol in the new module
`src/reports/sharing.py`; the API rejects others with `422`. Posting a share for a user who already has one changes the
role.

### D2. Revocation

Revoking deletes the share row. Because `can_view` reads the table on every request and nothing is cached, revocation
applies on the next request.

### D3. Public links

Table `public_links(token, report_id, created_by, expires_at)`. `token` is a random 32-byte URL-safe string.
`GET /r/{token}` renders the report read-only without a session until `expires_at` (default 30 days). The share dialog
offers "Create public link"; the owner can delete a link at any time.

### D4. Audit events

Each create, role change, and delete in D1 to D3 writes an `audit_events` row with `actor_id`, `action`, `report_id`,
`target` (user id or link token prefix), and `occurred_at`. For shares, `action` is `share.create`, `share.update`, or
`share.delete`. Rows are written by `record_audit(db, actor_id, action, report_id, target, now)` in the new module
`src/reports/audit.py`, in the same transaction as the change.

### D5. Integration

The repository has no web layer, database setup, or user model. The tables of D1 to D3 are created by
`migrations/0001_report_sharing.sql`, in a new top-level `migrations/` directory that the release applies with
`sqlite3 <db> < migrations/0001_report_sharing.sql`; tests apply it with `executescript`. `can_view` becomes
`can_view(db, report, user_id)` and reads `shares` on each call. Each share route in Interfaces is a plain function in
`src/reports/sharing.py` that takes `db`, the acting user's id, a `Directory`, the `Report` the host has already loaded,
and `now`, and returns a status code and a JSON body. Only the report's owner may create or delete shares, otherwise
the function returns `403`; deleting a share that does not exist returns `404`. The host application mounts the
functions on its routes, loads the report, and supplies the acting user.

## Interfaces

- `POST /reports/{id}/shares {"user_id", "role"}`
- `DELETE /reports/{id}/shares/{user_id}`
- `POST /reports/{id}/public-links` returns `{"url"}`
- `DELETE /reports/{id}/public-links/{token}`
- `GET /r/{token}` (no session required)

## Out of Scope

Editing reports; the `editor` role is stored but grants no extra access in this change.

## Rollout

One release. Rollback is the previous release; the new tables are unused by older code.
