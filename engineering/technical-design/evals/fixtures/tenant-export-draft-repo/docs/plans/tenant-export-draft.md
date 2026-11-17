# Tenant-Safe Dashboard Export Draft

Status: accepted by the user as the basis for technical design on 2026-10-20. Still explicitly incomplete: it fixes
intent, scope, and constraints, and leaves technical questions open. Next phase: technical design.

## Original idea

"Our administrators keep asking for a way to get the filtered records out of the dashboard as a file. The one thing we
cannot get wrong is showing somebody else's customers' data."

## Purpose and outcome

Administrators can download the records they see on a filtered dashboard view, so they can work with them in
spreadsheets. The outcome is a file that holds exactly the filtered records of the administrator's own tenant.

## Direction

An administrator applies the dashboard's existing filters, requests an export, and receives a CSV file of the matching
records. This is a user decision. The first release has one format and no scheduled or recurring exports.

## Scope

- Administrators of a tenant export filtered records of that tenant.
- The export uses the filters already available on the dashboard: date range and status.
- The administrator sees whether the export succeeded or failed.

## Exclusions

- Viewers cannot export.
- Cross-tenant reporting for the vendor's own staff.
- Formats other than CSV, and scheduled or emailed exports.

## Prohibited outcome

An export must never disclose another tenant's data. This holds for the file's content and also for its name, its
record counts, any message shown to the user, and any failure. This is a user decision and it defines success.

## Constraints and assumptions

1. The prohibited outcome above has priority over every other goal, including convenience and speed. User decision.
2. Tenant membership is already established at sign-in; the export adds no new way to choose a tenant. Assumption,
   confirmed in the existing code.
3. Exports of up to a few thousand records are typical. Larger exports are possible. Provisional.

## Success signal

No export produced in the first quarter contains a record of another tenant, judged by the security reviewer's sample
audit of exports and by an empty result from the audit query that compares an export's records with its tenant.

## Open questions for technical design

1. Where is tenant scoping enforced so that the export path cannot bypass it?
2. How are filters validated so that a crafted filter cannot widen the tenant boundary?
3. How are large exports produced, and does the file outlive the request?
4. What does the administrator see on failure, without disclosing anything beyond their own tenant?
5. What is recorded for audit when an export is requested, produced, or denied?
