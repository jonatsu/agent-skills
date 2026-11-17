# Design: Account Activity Export

Status: Accepted

Implements: [account export specification](../specs/account-export.md), revision 3.

## Overview

Exports are generated synchronously in pages and streamed; there is no background job. Resumption uses a cursor that
encodes the last activity id written, so the service needs no per-download state.

## Decisions

<a id="d1-export-records"></a>

### D1. Export records

Satisfies [format selection](../specs/account-export.md#req-format) and
[retention](../specs/account-export.md#req-retention).

Table `exports(id TEXT PRIMARY KEY, tenant_id TEXT, format TEXT, created_at TEXT)`. `id` is a random 128-bit token.
`format` is fixed at request time. A row older than 72 hours is treated as expired on read; the existing nightly
cleanup deletes such rows.

<a id="d2-streaming"></a>

### D2. Streaming and serializers

Satisfies [format selection](../specs/account-export.md#req-format).

`accounts.export.stream(db, export, after_id)` pages through `accounts.activity.list_activity` and passes each page to
a serializer chosen by `export.format`. Both serializers write the fields `id`, `occurred_at`, and `summary`.

<a id="d3-resume"></a>

### D3. Resume cursor

Satisfies [resumability](../specs/account-export.md#req-resume).

Each streamed chunk ends with the last activity id written. A resume request passes that id as `after_id`. Because
activity ids only grow and `list_activity` orders by id, a resume neither repeats nor skips records.

<a id="d4-scoping"></a>

### D4. Tenant scoping

Satisfies [cross-tenant nondisclosure](../specs/account-export.md#req-nondisclosure).

Every lookup of an export uses `(id, caller.tenant_id)`. A missing row, another tenant's row, and an expired row for
another tenant all return `404 export_not_found`. An expired row for the caller's tenant returns `410 export_expired`.
`stream` reads activity only through the export's own `tenant_id`.

## Interfaces

- `POST /exports {"format": "jsonl" | "csv"}` returns `201 {"id": ...}`.
- `GET /exports/{id}?after_id=N` streams records with ids above `N`.

## Out of Scope

Filtering exports by date, and formats other than JSON Lines and CSV.
