# Design: Tenant Record Export

Status: Accepted

## Purpose

Tenant administrators need a CSV export of their records, filtered the same way as search.

## Behavior

- `POST /exports` with an optional `status` filter starts an export for the caller's tenant and returns an export id.
- `GET /exports/{id}` returns the CSV once ready.
- Only callers with the `admin` role may start or download exports. A non-admin receives `403`.
- An export contains only records of the tenant that requested it. A caller who requests or downloads an export of
  another tenant receives `404`, the same response as for an id that does not exist, so export ids of other tenants
  cannot be discovered.
- A tenant with no matching records receives a CSV with only the header row.

## Design

`records.export.start_export(db, caller, status)` checks `is_admin`, then stores an `exports` row holding `tenant_id`
taken from the caller, never from the request. The CSV is built by reusing `records.search.search`, so the tenant
filter and status filter have one implementation.

`records.export.get_export(db, caller, export_id)` loads the row by `(export_id, caller.tenant_id)`. A row that exists
for another tenant is indistinguishable from a missing row.

Exports are kept for 7 days and deleted by the existing nightly cleanup job.

## Security Obligations

- S1: No export, by content, status code, timing class, or error text, reveals records or export ids of another tenant.
- S2: Tenant scope comes only from the authenticated caller.
- S3: Non-admin callers cannot start or download exports.

## Out of Scope

Export formats other than CSV, and cross-tenant exports for platform operators.
