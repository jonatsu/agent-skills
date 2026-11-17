# Sign-in Lockout Plan

## Goal

Lock an account for 15 minutes after five failed sign-ins in a row, as decided in the sign-in lockout design. The
design has since been folded into the security handbook.

## Work packages

1. **Failure counter.** Add `failed_sign_ins` to the account table and increment it on each failed attempt; reset it
   on success. Checked by unit tests for increment and reset.
2. **Lockout check.** Refuse sign-in while `locked_until` is in the future and set it on the fifth failure. Checked by
   a test that the sixth attempt is refused even with the right password, and that sign-in works after 15 minutes.

## Acceptance

`just test` covers the lockout sequence end to end, and a manual check on the staging site shows the lockout message.
