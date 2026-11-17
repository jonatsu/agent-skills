# Design: Request Deduplication with Idempotency Keys

Status: Accepted

## Goal

Clients retry `POST /orders` after timeouts and create duplicate orders. A client may send an `Idempotency-Key` header
so that a retry returns the original result instead of creating a second order.

## Behavior

1. **Same key, same payload.** A request whose key matches a completed request from the same account, with the same
   payload hash, returns the stored status and body. No new order is created.
2. **Same key, different payload.** The request is rejected with `409 Conflict` and body
   `{"error": "idempotency_key_reused"}`. The stored result is unchanged.
3. **Concurrent duplicates.** When two requests with the same key and payload arrive before either completes, exactly
   one order is created and both receive the same result. The second request waits up to 5 seconds for the first;
   after that it returns `409` with `{"error": "request_in_progress"}`.
4. **Expiry.** Keys are kept for 24 hours from first use. After expiry the key is treated as new.
5. **Persisted results.** The stored status and body survive a process restart, so a retry after a restart still
   returns the original result.
6. Requests without the header behave as today.

Keys are scoped per account: two accounts may use the same key independently.

## Design

A new table `idempotency_keys(account_id, key, request_hash, status, response_status, response_body, created_at)`
with primary key `(account_id, key)`. The handler inserts a row with `status = 'in_progress'` inside the same
transaction that creates the order; the primary key makes the second concurrent insert fail, and that request then
polls the row until it is `completed` or the wait limit passes. The request hash is SHA-256 over the canonical JSON
body (sorted keys, no whitespace). Expired rows are ignored on read and deleted by an hourly cleanup.

## Verification Obligations

Each numbered behavior above needs a test that sends real requests through `create_order` against a SQLite file
database, so that behavior 5 can reopen the database between requests.
