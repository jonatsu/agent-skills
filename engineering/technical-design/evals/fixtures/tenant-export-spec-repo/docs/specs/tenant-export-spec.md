# Tenant Dashboard Export Specification

Status: accepted. Revision 3, accepted 2026-11-02 by the product owner. Supersedes revision 2.

Requirement identifiers (`EXP-n`) are stable. A change to a requirement's meaning gets a new identifier; the old one is
retired, not reused.

## Purpose

Tenant administrators can download the records of a filtered dashboard view as a file. An export never discloses another
tenant's data.

## Actors

- Tenant administrator: a signed-in user with the administrator role in one tenant.
- Tenant viewer: a signed-in user with the viewer role in one tenant.

## Requirements

### EXP-1 Export own filtered records

When a tenant administrator requests an export with a date range, a status, both, or neither, the system produces a CSV
file that contains every record of the administrator's own tenant that matches those filters.

Acceptance: for a tenant with 40 records, 12 of which match a chosen status, the file has a header row and 12 data rows.

### EXP-2 Columns and order

The file has the columns `id`, `name`, `status`, and `created_on`, in that order, and its rows are ordered by `id`.

Acceptance: opening the file in a spreadsheet shows those four columns, with ids ascending.

### EXP-3 Administrators only

When a tenant viewer requests an export, the system refuses the request, creates no file, and tells the viewer that
exporting requires an administrator.

Acceptance: a viewer's request returns the refusal message and the dashboard shows no new export.

### EXP-4 Export status

After a request, the administrator sees the export as in progress, ready, or failed. A ready export offers a download
that stays available for 24 hours.

Acceptance: a ready export downloads within 24 hours of becoming ready and is no longer offered after that.

### EXP-5 Failure without partial files

When an export fails, the administrator sees it as failed with the message "The export could not be completed." The
system offers no partial file.

Acceptance: after a forced failure, the status is failed, the message is shown, and no download is offered.

### EXP-6 No cross-tenant disclosure

No export, in any state, discloses data of a tenant other than the requesting administrator's. This covers the file's
content, its name, any count or total shown, and every message the administrator sees, including failure messages.

Acceptance: with records in two tenants, an administrator of one tenant who requests exports with every combination of
filters, including values naming the other tenant's records, never receives a file, name, count, or message that
reveals the other tenant's data.

### EXP-7 Own downloads only

An export can be downloaded only by the administrator who requested it, or by another administrator of the same tenant.

Acceptance: an administrator of a different tenant who is given the download address of a ready export receives a
not-found response and no file.

## Non-goals

- Formats other than CSV.
- Scheduled or emailed exports.
- Exports by the vendor's own staff across tenants.

## Revision history

| Revision | Date       | Change                                            |
| -------- | ---------- | ------------------------------------------------- |
| 3        | 2026-11-02 | Added EXP-7; EXP-5 now fixes the failure message. |
| 2        | 2026-10-14 | Added EXP-6, the cross-tenant prohibition.        |
| 1        | 2026-09-30 | First accepted revision.                          |
