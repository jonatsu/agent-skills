# Specification: Account Activity Export

Revision: 3 (accepted)

Revision history: revision 2 added the retention period; revision 3 clarified that a resumed export keeps its
original format.

## Purpose

Tenant administrators need a copy of their account activity for audits.

## Requirements

<a id="req-format"></a>

### Format selection

An administrator chooses JSON Lines or CSV when requesting an export. Both formats contain the same records and fields.
A resumed export keeps the format chosen when it was requested.

<a id="req-resume"></a>

### Resumability

An interrupted download can resume from where it stopped without repeating or skipping records. An export can be
resumed until it expires.

<a id="req-retention"></a>

### Retention

A completed export is available for 72 hours, then deleted. After deletion, download and resume attempts report that
the export has expired.

<a id="req-nondisclosure"></a>

### Cross-tenant nondisclosure

An export contains only the requesting tenant's activity. No request, response, or error reveals whether another
tenant's export exists or what it contains.

## Acceptance

- Each format can be requested, downloaded, and parsed, and both contain the same records.
- An interrupted download resumed at any point yields exactly the full record set.
- A download or resume after 72 hours reports expiry.
- Requests for another tenant's export are indistinguishable from requests for an export that does not exist.
