# Design: Account Activity Export

Status: Accepted

Implements: [account export specification](../specs/account-export.md), revision 3.

## Overview

Exports are generated synchronously in pages and streamed; there is no background job. Resumption uses the id of the
last record the client received, so the service needs no per-download state.

The repository has no web layer, authentication, or database setup. This change adds two new modules:
`src/accounts/export.py` for export records and serializers, and `src/accounts/http.py` for two framework-free handler
functions. The host service that mounts the handlers supplies the database connection, the clock, and the
authenticated caller.

## Decisions

<a id="d1-export-records"></a>

### D1. Export records

Satisfies [format selection](../specs/account-export.md#req-format),
[resumability](../specs/account-export.md#req-resume), and [retention](../specs/account-export.md#req-retention).

Table `exports(id TEXT PRIMARY KEY, tenant_id TEXT, format TEXT, created_at TEXT, last_id INTEGER)`, created by
`accounts.export.create_schema(db)` with `CREATE TABLE IF NOT EXISTS`; the host calls it at start-up. `id` is a random
128-bit token, and `created_at` is ISO 8601 UTC. `format` is fixed at request time. `last_id` is the highest activity id
of the tenant at request time (0 when there is none), so an export is a snapshot: later activity is never included, and
a resumed download sees the same record set as the original.

Export content is generated from `activity` on each download and never stored, so an export is deleted, in the
specification's sense, when it expires: a row whose `created_at` is 72 hours or more before `now` is expired on read.
The row stays as a tombstone, so a later request can still answer that the export expired. There is no cleanup job.

<a id="d2-streaming"></a>

### D2. Streaming and serializers

Satisfies [format selection](../specs/account-export.md#req-format).

`accounts.export.stream(db, export, after_id)` pages through `accounts.activity.list_activity`, stops after
`export.last_id`, and passes each page to a serializer chosen by `export.format`. `export` is an
`accounts.export.Export` dataclass with the table's columns. Both serializers write the fields `id`, `occurred_at`, and
`summary`. JSON Lines writes one object per line. CSV writes the header row `id,occurred_at,summary` only when
`after_id` is 0, so the partial download followed by the resumed download forms one valid file.

<a id="d3-resume"></a>

### D3. Resume cursor

Satisfies [resumability](../specs/account-export.md#req-resume).

The response carries no separate cursor. Every record includes its `id`, so a client that was interrupted resumes with
`after_id` set to the `id` of the last complete record it received. Because activity ids only grow and `list_activity`
orders by id, a resume neither repeats nor skips records.

<a id="d4-scoping"></a>

### D4. Tenant scoping

Satisfies [cross-tenant nondisclosure](../specs/account-export.md#req-nondisclosure).

Every lookup of an export uses `(id, caller.tenant_id)`. A missing row, another tenant's row, and an expired row for
another tenant all return `404 export_not_found`. An expired row for the caller's tenant returns `410 export_expired`.
`stream` reads activity only through the export's own `tenant_id`.

Handlers receive the caller as `accounts.http.Caller(tenant_id: str)`, built by the host from its authentication.

## Interfaces

- `POST /exports {"format": "jsonl" | "csv"}` returns `201 {"id": ...}`. Any other format returns
  `400 invalid_request`.
- `GET /exports/{id}?after_id=N` streams records with ids above `N`; `after_id` defaults to 0, and a value that is not
  a non-negative integer returns `400 invalid_request`.

The handlers are `accounts.http.create_export(db, caller, body, now)` and
`accounts.http.get_export(db, caller, export_id, after_id, now)`. Each returns the status code and either a JSON body or
the record stream. The host maps them to the routes above.

## Out of Scope

Filtering exports by date, and formats other than JSON Lines and CSV.
