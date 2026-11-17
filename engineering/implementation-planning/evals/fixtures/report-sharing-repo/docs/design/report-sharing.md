# Design: Report Sharing

Status: Accepted (approved 2026-09-02)

Implements: [report sharing specification](../specs/report-sharing.md), revision 1.

## Overview

Sharing adds a `shares` table for named users and a `public_links` table for anonymous links. `can_view` consults
both. Every change writes an audit event.

## Decisions

### D1. Named-user shares

Table `shares(report_id, user_id, role, created_by, created_at)` with primary key `(report_id, user_id)`. `role` is
`viewer` or `editor`. `can_view` returns True for the owner or any user with a share row. Shares are limited to users
in the owner's organization; the API rejects others with `422`.

### D2. Revocation

Revoking deletes the share row. Because `can_view` reads the table on every request and nothing is cached, revocation
applies on the next request.

### D3. Public links

Table `public_links(token, report_id, created_by, expires_at)`. `token` is a random 32-byte URL-safe string.
`GET /r/{token}` renders the report read-only without a session until `expires_at` (default 30 days). The share dialog
offers "Create public link"; the owner can delete a link at any time.

### D4. Audit events

Each create, role change, and delete in D1 to D3 writes an `audit_events` row with `actor_id`, `action`, `report_id`,
`target` (user id or link token prefix), and `occurred_at`.

## Interfaces

- `POST /reports/{id}/shares {"user_id", "role"}`
- `DELETE /reports/{id}/shares/{user_id}`
- `POST /reports/{id}/public-links` returns `{"url"}`
- `DELETE /reports/{id}/public-links/{token}`
- `GET /r/{token}` (no session required)

## Rollout

One release. Rollback is the previous release; the new tables are unused by older code.
