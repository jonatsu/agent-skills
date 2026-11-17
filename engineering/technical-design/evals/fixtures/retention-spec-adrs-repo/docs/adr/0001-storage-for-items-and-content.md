# ADR 0001: Store item metadata in PostgreSQL and content in object storage

Status: accepted, 2026-08-18.

## Context

The service stores item records (name, folder, owner, versions) and the files themselves, which range from a few
kilobytes to several gigabytes. Workspaces are small, and the team runs one database already.

## Decision

Item metadata, folders, versions, holds, and the activity log live in PostgreSQL. File content lives in an
S3-compatible object store, addressed by an opaque content key held in the item version's record. Deleting an item
sets a `deleted_at` timestamp on its record; content is never removed by the delete itself.

## Consequences

- The database is the source of truth for what exists. Content without a record is unreachable.
- Content removal is a separate step from record removal, and a failure between them can leave orphaned content.
- Listings and search read metadata only, so they filter on `deleted_at` without touching the object store.
