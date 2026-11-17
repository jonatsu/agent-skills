# Password Reset Throttling

Status: Accepted

## Context

`identity.reset.request_reset` sends a reset email on every request for a registered address. Repeated requests flood
the user's inbox and let anyone use the service to send mail to a known address.

## Decision

Allow at most 3 reset emails per account in any rolling 60-minute window. A request over the limit sends no email and
returns the same `GENERIC_RESPONSE` as every other request, so a caller cannot tell a throttled address from an
unknown one.

Sent requests are recorded in a new table `reset_requests(account_id, sent_at)`, written in the same transaction as
the decision to send. The count for the window is
`SELECT COUNT(*) ... WHERE account_id = ? AND sent_at > now - 60 minutes`. Rows older than 24 hours are deleted by the
existing nightly maintenance job.

The limit lives in the setting `RESET_EMAILS_PER_HOUR` (default 3) so support can raise it during an incident.

## Interfaces

`request_reset(email, find_account, send_email)` keeps its signature and return value. A new module `identity.throttle`
exposes `allow_reset(db, account_id, now) -> bool`, which records a send when it returns True.

## Failure Handling

If the throttle table cannot be read or written, the request fails closed: no email is sent and the generic response
is returned. The failure is logged with the account id, never the email address.

## Rollout

Ships in one release with migration `0007_reset_requests.sql`. Rollback is the previous release; the table is unused by
older code and can stay.
