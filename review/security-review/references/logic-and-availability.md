# Business Logic, Concurrency, and Availability

Scanners do not find these. Every construct is individually correct, and the defect is that the sequence
permits an outcome the business did not intend. Finding them requires knowing what the code is for, so start
by writing down the rule the code is supposed to enforce.

## Business Logic

For each workflow, state the invariant in one sentence. A discount applies once. A refund never exceeds the
payment. An order ships only after payment settles. Then look for a path that reaches the end state without
passing the check that establishes the invariant.

The recurring shapes:

- a multi-step flow whose steps can be requested out of order, or whose final step can be requested directly;
- a value validated on the client and trusted on the server, most often a price, a quantity, or a discount;
- a quantity or an amount that accepts a negative value, a zero, or a number large enough to overflow or to
  lose precision, so a refund credits the attacker;
- a limit enforced per request while the operation is available in bulk;
- an identifier that the flow trusts because an earlier step produced it, though the client can substitute
  another;
- a currency, a unit, or a rounding direction that differs between two steps of the same calculation; and
- a cancel, reverse, or retry path that undoes the record without undoing the effect, or that can be replayed.

Ask what happens when a step fails halfway. A workflow that grants access before the payment confirms, and
that has no compensating action, is exploitable by making the later step fail.

## Race Conditions

Any check followed by a separate action on shared state is a candidate. The attacker's tool is concurrency, so
the question is what two simultaneous requests do.

Look for a read-check-write sequence over a balance, a quota, a stock count, a coupon redemption, a
one-time token, or a uniqueness constraint. The correct forms are a conditional update the database performs
atomically, a row lock held across the check and the write, a unique constraint that makes the second write
fail, or an idempotency key the caller supplies.

An application-level lock is correct only within one process. In any deployment with more than one instance,
it is not a control. Say so when you see it.

Also look at file operations that check a path and then open it, since the path can change between the two.
Open first and inspect the handle.

## Rate Limiting and Resource Exhaustion

Ask which operations are expensive and which are reachable without authentication. Login, password reset,
registration, search, export, report generation, file conversion, and anything that calls a paid third-party
service all belong on the list.

Check that limits are keyed on something the attacker cannot rotate freely. A limit keyed on a client-supplied
header or on an unvalidated forwarded address is not a limit. Check that a limit exists per account as well as
per source, because otherwise a distributed attempt passes.

Separately, check the bounds on individual requests: maximum body size, maximum upload size, maximum items in
a batch, maximum page size, maximum nesting depth in parsed input, maximum expansion for anything decompressed,
and a timeout on every outbound call. An unbounded page size turns a normal endpoint into a data-export
endpoint.

Check that a failure in a dependency does not consume the caller's resources indefinitely. Connection pools
exhausted by a slow dependency take down endpoints that do not use it.

## Error Handling

The question is what the code does on the failure path, and whether that path was designed at all.

Fail-closed is the requirement for anything that authorizes, validates, or verifies. Look for a caught
exception around an authorization or signature check whose handler continues, a default return value that is
permissive, a timeout on an authorization service treated as an allow, and a cache miss treated as a pass.

Look also for a defect that succeeds partially and reports success, so the caller believes a security-relevant
step ran.

Then check what the failure discloses. A stack trace, a query fragment, an internal path, a version banner, or
a differently-worded message for a different failure cause all give an attacker information. Return one generic
message with a correlation identifier and keep the detail in the server log.

## Audit Logging

Logging is a security control when it makes an incident reconstructable. Check that authentication successes
and failures, authorization denials, privilege and role changes, credential and configuration changes, and
significant data access are recorded with who, what, when, and from where.

Then check the parts that make the log trustworthy: that the application cannot silently drop records, that a
user cannot forge entries by injecting newlines or control characters into a logged field, that the retention
period is long enough for an incident to be noticed, and that log storage is not writable by the systems the
log is meant to hold accountable.

Confirm that something reads the log. A security event nobody alerts on is a record, not a control, and saying
so is more useful than reporting the log as adequate.
