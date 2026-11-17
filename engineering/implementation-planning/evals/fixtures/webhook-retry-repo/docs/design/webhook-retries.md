# Design: Webhook Delivery Retries

Status: Accepted (approved by the platform maintainers for 0.5.0)

## Context

`hooksvc.sender.deliver` makes one attempt and records `delivered` or `failed`. A brief endpoint outage loses the
event. Tenants have asked for automatic retries with a way to replay events that never got through.

## Decisions

### D1. Endpoint validation on every attempt

`validate_endpoint` runs when a subscription is stored, which is new: `Store.add_subscription` calls it and lets
`InvalidEndpointError` propagate. It runs again before each attempt, because a stored endpoint may have been registered
before the current rules. An attempt whose endpoint fails validation is not sent. A retried delivery moves to `dead`
with reason `invalid_endpoint` and is not retried. With retries off, the delivery is recorded `failed` and `deliver`
raises `InvalidEndpointError`.

### D2. Durable retry state

Retry state lives in the existing `deliveries` table, added by migration `0002`:

| Column            | Type    | Meaning                                                                         |
| ----------------- | ------- | ------------------------------------------------------------------------------- |
| `attempts`        | INTEGER | Attempts claimed so far, default 0                                              |
| `next_attempt_at` | TEXT    | UTC time the delivery becomes due; NULL once terminal                           |
| `last_error`      | TEXT    | Short reason for the latest failure or the `dead` reason, never a response body |
| `lease_until`     | TEXT    | UTC time until which a worker owns the row; NULL when unclaimed                 |

Times are UTC text in the `YYYY-MM-DD HH:MM:SS` form that `created_at` already uses. `status` gains the values
`pending` and `dead`. Existing rows keep `delivered` or `failed` and are never retried.

A worker claims due rows by setting `lease_until` to now plus 60 seconds and incrementing `attempts` in one
`UPDATE ... WHERE` statement, so two workers cannot claim the same row. A row whose lease expired without an outcome is
due again; this is how a crashed worker's work is recovered. A due row that already has 8 attempts moves to `dead`
with reason `exhausted` without a send. Delivery is therefore at least once, and receivers deduplicate with the
`X-Delivery-Id` header, which carries the delivery row id and is sent only on worker attempts.

Migration `0002` is applied to a deployed database with `sqlite3 <db> < src/hooksvc/migrations/0002_retry_state.sql`
as part of the release. `Store.SCHEMA` gains the same columns for new databases; `CREATE TABLE IF NOT EXISTS` does not
alter an existing table.

### D3. Backoff

The delay before attempt `n` (n starting at 2) is `30 s * 2^(n-2)` with uniform jitter of plus or minus 20 percent. A
delivery makes at most 8 attempts, spanning roughly one hour.

### D4. Failure classification

| Outcome                                   | Action                                  |
| ----------------------------------------- | --------------------------------------- |
| 2xx                                       | `delivered`                             |
| 408, 429, any 5xx, timeout, network error | retry with backoff                      |
| 429 with a numeric `Retry-After`          | retry after the larger of header and D3 |
| 1xx, 3xx, any other 4xx                   | `dead`, reason `rejected`               |
| eighth retryable failure                  | `dead`, reason `exhausted`              |

A `Retry-After` value above one hour counts as one hour. A missing or non-numeric value is ignored. Redirects are not
followed.

### D5. Replay and authorization

`hooksvc.api.replay_delivery(store, tenant_id, delivery_id)`, in a new module `src/hooksvc/api.py`, moves a `dead`
delivery back to `pending` with `attempts` reset to 0 and `next_attempt_at` set to now. The row, and so its
`X-Delivery-Id`, stays the same. It succeeds only when the delivery's subscription belongs to `tenant_id`; otherwise it
raises `NotFoundError`, so a caller cannot learn that another tenant's delivery exists. A delivery that is not `dead` is
left unchanged and `InvalidStateError` is raised. Both exceptions are new in `hooksvc.errors`. Replay does not bypass
D1.

### D6. Compatibility

`deliver(store, client, subscription_id, payload)` keeps its signature. With retries enabled for the subscription's
tenant it records a `pending` delivery due now and returns. With retries disabled it behaves as in 0.4.0, with the
validation of D1 as the only addition. Signatures, headers other than the new `X-Delivery-Id`, and the request timeout
do not change.

### D7. Rollout and rollback

Rollout order:

1. Release migration `0002` and the worker with `HOOKSVC_RETRIES=off`; confirm the existing suite and a 0.4.0
   database upgraded by the migration both behave as before.
2. Set `HOOKSVC_RETRIES` to the id of one internal tenant for 48 hours. Watch `hooksvc_deliveries_total{status}`,
   `hooksvc_retry_attempts_total`, and `hooksvc_dead_total{reason}`.
3. Set `HOOKSVC_RETRIES=all` if the dead rate stays under 1 percent of deliveries and no row is stuck (D8).

Rollback sets `HOOKSVC_RETRIES=off` and restarts. Rows left `pending` stay in the table and are neither sent nor
deleted; enabling again resumes them. Migration `0002` only adds columns, so it stays in place on rollback.

### D8. Worker, setting, and metrics

The worker is a new module, `src/hooksvc/worker.py`, run as a separate process with `python -m hooksvc.worker`. It
opens the SQLite file named by `HOOKSVC_DB`, polls for due rows every 5 seconds, and makes the attempts with the same
`httpx` client settings as `deliver`. Any number of worker processes may run against one database.

`HOOKSVC_RETRIES` is `off` (the default), `all`, or a comma-separated list of tenant ids. The service and the worker
read it at start-up, so a change takes effect on restart. The worker sends only rows of tenants the setting enables.

The worker emits the metrics with `prometheus-client`, a new dependency, and serves them on port 9100. `deliver` on
the retries-off path emits none. `hooksvc_deliveries_total{status}` counts each recorded outcome,
`hooksvc_retry_attempts_total` counts attempts after the first, and `hooksvc_dead_total{reason}` counts moves to
`dead`. A leased row is stuck when it is `pending` and its `lease_until` is more than 5 minutes in the past.

## Out of Scope

Per-tenant retry policies, a dashboard for dead deliveries, and payload size limits.
