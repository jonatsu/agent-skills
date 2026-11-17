# Design: Opaque String Account IDs

Status: Accepted

## Problem

Account IDs are sequential integers. They leak account counts and creation order to anyone who sees two IDs, and
consumers have started relying on their numeric form (billing pads them into partition keys). New accounts must get
opaque string IDs, and existing accounts must move to them without breaking consumers.

## Target State

Every account has an `id` of the form `acc_` followed by 22 base62 characters from a random 128-bit value. The integer
column is gone, and every consumer treats the ID as an opaque string.

## Decisions

### Storage

Migration `0002` adds a nullable, unique `public_id TEXT` column to `accounts`. New accounts get a `public_id` at
creation. A backfill job assigns one to each existing account in batches of 1,000 and is safe to rerun: it touches only
rows where `public_id IS NULL`. Migration `0002` is reversible (drop the column). The later removal of the integer
column (migration `0003`) is not reversible and is the last step.

### Event compatibility window

For one release, `account.created` carries both `account_id` (integer, unchanged) and `account_ref` (the string ID).
`decode` accepts messages with either or both fields; consumers read `account_ref` when present and fall back to
`account_id`. After the window, producers send only `account_ref`, and `account_id` is removed from the schema.

Old and new readers must coexist for that release: a consumer on the previous `decode` must keep working against new
messages, and an updated consumer must keep working against old messages still on the bus.

### Lookups

`AccountStore.get` accepts either form during the window. After cutover it accepts only the string form; an integer
lookup returns `None`.

### Billing partition keys

Billing derives its key from `account_ref` after cutover. Existing invoices keep their integer keys; billing maps old
to new through a lookup table it owns. That table is billing's work and outside this design, but cutover waits for
billing to confirm it is in place.

## Verification Obligations

- An incumbent regression gate: the current test suite and a recorded set of current `account.created` messages must
  pass unchanged against the compatibility release before any rollout step.
- Mixed-version checks: old `decode` against new messages, new `decode` against old messages.
- Backfill evidence: zero rows with `public_id IS NULL`, and a uniqueness check, before producers stop sending
  `account_id`.

## Rollout

The compatibility release goes through the normal staged train (canary, 25 percent, all). Rollout watches consumer
decode errors on `ledger-overview` and the backfill's remaining-row count.

## Rollback

Until migration `0003` runs, rollback is the previous release plus, if needed, migration `0002`'s down step. Rollback
is triggered by any consumer decode error rate above 0.1 percent of `account.created` messages during a stage, or a
backfill failure. Success of a rollback is measured by decode errors returning to the pre-release baseline within one
hour.

## Removal

Removing `account_id` from events and the integer column happens only after:

- the backfill evidence above holds,
- every consumer in `docs/consumers.md` has confirmed it reads `account_ref`, and
- one full release has shipped with both fields.

## Out of Scope

Changing IDs of other entities, and rewriting historical invoice keys.
