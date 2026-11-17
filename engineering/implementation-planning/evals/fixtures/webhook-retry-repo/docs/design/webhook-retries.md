# Design: Webhook Delivery Retries

Status: Accepted (approved by the platform maintainers for 0.5.0)

## Context

`hooksvc.sender.deliver` makes one attempt and records `delivered` or `failed`. A brief endpoint outage loses the
event. Tenants have asked for automatic retries with a way to replay events that never got through.

## Decisions

### D1. Endpoint validation on every attempt

`validate_endpoint` runs when a subscription is stored and again before each attempt, because a stored endpoint may
have been registered before the current rules. An attempt whose endpoint fails validation is not sent; the delivery
moves to `dead` with reason `invalid_endpoint` and is not retried.

### D2. Durable retry state

Retry state lives in the existing `deliveries` table, added by migration `0002`:

| Column            | Type    | Meaning                                                         |
| ----------------- | ------- | --------------------------------------------------------------- |
| `attempts`        | INTEGER | Attempts made so far, default 0                                 |
| `next_attempt_at` | TEXT    | UTC time the delivery becomes due; NULL once terminal           |
| `last_error`      | TEXT    | Short reason for the latest failure, never the response body    |
| `lease_until`     | TEXT    | UTC time until which a worker owns the row; NULL when unclaimed |

`status` gains the values `pending` and `dead`. Existing rows keep `delivered` or `failed` and are never retried.

A worker claims due rows by setting `lease_until` to now plus 60 seconds in one `UPDATE ... WHERE` statement, so two
workers cannot claim the same row. A row whose lease expired without an outcome is due again; this is how a crashed
worker's work is recovered. Delivery is therefore at least once, and receivers deduplicate with the `X-Delivery-Id`
header, which carries the delivery row id.

### D3. Backoff

The delay before attempt `n` (n starting at 2) is `30 s * 2^(n-2)`, capped at one hour, with uniform jitter of plus or
minus 20 percent. A delivery makes at most 8 attempts, spanning roughly two hours.

### D4. Failure classification

| Outcome                                   | Action                                  |
| ----------------------------------------- | --------------------------------------- |
| 2xx                                       | `delivered`                             |
| 408, 429, any 5xx, timeout, network error | retry with backoff                      |
| 429 with `Retry-After` up to one hour     | retry after the larger of header and D3 |
| any other 4xx                             | `dead`, reason `rejected`               |
| eighth retryable failure                  | `dead`, reason `exhausted`              |

### D5. Replay and authorization

`hooksvc.api.replay_delivery(tenant_id, delivery_id)` moves a `dead` delivery back to `pending` with `attempts` reset.
It succeeds only when the delivery's subscription belongs to `tenant_id`; otherwise it raises `NotFoundError`, so a
caller cannot learn that another tenant's delivery exists. Replay does not bypass D1.

### D6. Compatibility

`deliver(store, client, subscription_id, payload)` keeps its signature. With retries enabled it records a `pending`
delivery and returns; with retries disabled it behaves exactly as in 0.4.0. Signatures, headers other than the new
`X-Delivery-Id`, and the request timeout do not change.

### D7. Rollout and rollback

Retries are behind the setting `HOOKSVC_RETRIES` (`off` by default). Rollout order:

1. Release migration `0002` and the worker with the setting `off`; confirm the existing suite and a 0.4.0 database
   upgraded by the migration both behave as before.
2. Enable for one internal tenant for 48 hours. Watch `hooksvc_deliveries_total{status}`,
   `hooksvc_retry_attempts_total`, and `hooksvc_dead_total{reason}`.
3. Enable for all tenants if the dead rate stays under 1 percent of deliveries and no row stays leased past 5 minutes.

Rollback sets `HOOKSVC_RETRIES=off`. Rows left `pending` stay in the table and are neither sent nor deleted; enabling
again resumes them. Migration `0002` only adds columns, so it stays in place on rollback.

## Out of Scope

Per-tenant retry policies, a dashboard for dead deliveries, and payload size limits.
