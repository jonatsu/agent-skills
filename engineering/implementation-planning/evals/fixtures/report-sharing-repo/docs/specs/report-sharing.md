# Specification: Report Sharing

Revision: 2 (accepted 2026-10-14)

## Revision History

| Revision | Accepted   | Change                                                                                  |
| -------- | ---------- | --------------------------------------------------------------------------------------- |
| 1        | 2026-08-20 | Initial requirements: sharing with named users and by public link.                      |
| 2        | 2026-10-14 | Public links prohibited after the data-handling review; requirement R3 replaced by R3a. |

## Requirements

<a id="r1"></a>

### R1. Share with named users

A report owner can share a report with named users in the same organization, as viewer or editor.

<a id="r2"></a>

### R2. Revoke access

The owner can revoke any share. Revocation takes effect on the next request.

<a id="r3a"></a>

### R3a. No public access

A report must never be viewable without signing in. No link, token, or embed may grant access to a user who is not
signed in, and no sharing option may offer one.

<a id="r4"></a>

### R4. Audit

Every share, change of role, and revocation is recorded with actor, target, and time.

## Acceptance

- A named viewer can open the report; a user without a share cannot.
- After revocation, the former viewer cannot open the report.
- A request without a signed-in session never returns report content.
- Every sharing change appears in the audit log.
