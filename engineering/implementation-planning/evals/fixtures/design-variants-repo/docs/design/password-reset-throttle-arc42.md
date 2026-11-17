# Password Reset Throttling (arc42)

Status: Accepted

## 1. Introduction and Goals

Stop reset-email flooding. Quality goals: no account enumeration, bounded mail volume per account, and no new
infrastructure.

## 2. Constraints

Standard library and the existing SQLite database only. `request_reset` keeps its signature and return value.

## 3. Context and Scope

Actors: anonymous caller requesting a reset; the mail sender (`send_email`). Out of scope: CAPTCHA, IP-based limits.

## 4. Solution Strategy

Count sent reset emails per account in the database and refuse sends above the limit, returning the unchanged generic
response.

## 5. Building Block View

- `identity.reset.request_reset`: unchanged interface; consults the throttle before sending.
- `identity.throttle.allow_reset(db, account_id, now) -> bool`: new; returns whether a send is allowed and records it
  when it is.
- Table `reset_requests(account_id, sent_at)`: new, created by migration `0007_reset_requests.sql`.

## 6. Runtime View

1. Caller submits an email address.
2. `find_account` resolves it. Unknown address: return `GENERIC_RESPONSE`.
3. `allow_reset` counts rows for the account with `sent_at` in the last 60 minutes. If the count is below
   `RESET_EMAILS_PER_HOUR` (default 3), it inserts a row in the same transaction and returns True.
4. On True, `send_email` runs. Either way, `GENERIC_RESPONSE` is returned.

## 7. Deployment View

One release containing migration `0007_reset_requests.sql`. Rollback is the previous release; older code ignores the
table.

## 8. Crosscutting Concepts

Fail closed: if the throttle table cannot be read or written, no email is sent and the generic response is returned.
Log the account id on failure, never the email address. The nightly maintenance job deletes rows older than 24 hours.

## 9. Architecture Decisions

- ADR-1: Rolling 60-minute window per account, limit 3, configurable by `RESET_EMAILS_PER_HOUR`.
- ADR-2: Store sends in the existing database rather than an in-memory counter, so limits hold across processes.
- ADR-3: Throttled and unknown addresses get the identical response.

## 10. Quality Requirements

A throttled request must be indistinguishable from an unknown address by response text.

## 11. Risks and Technical Debt

Clock skew between processes could admit one extra email at a window edge; accepted.

## 12. Glossary

- **Window**: the 60 minutes before the current request.
