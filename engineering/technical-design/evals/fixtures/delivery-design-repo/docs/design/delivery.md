# Message Delivery Design

Status: accepted for the behavior under Proposed behavior and Decisions. Open questions remain.

## Purpose

This design explains how the delivery service moves an accepted message from the message table to its subscriber
endpoint, and which guarantees subscribers and operators can rely on. It realizes the accepted
[delivery requirements](../requirements.md).

## Current behavior

Messages live in the `messages` table with a status of `pending`, `in_flight`, `delivered`, or `failed`, an attempt
count, and the last error. A worker claims the oldest pending message by setting it to `in_flight` and recording its
own worker identifier and the claim time. It then posts the message to the subscriber endpoint with the message
identifier in an `Idempotency-Key` header. A 2xx response marks the message `delivered`. Any other outcome marks it
`pending` again, or `failed` once the attempt count reaches five.

The worker records the attempt before it posts. No code today changes an `in_flight` message except the worker that
claimed it.

## Proposed behavior

Delivery stays at least once. The worker claims one message at a time, increments the attempt count when it claims, and
sends. Retries use the same message identifier so that the subscriber's repeat detection keeps working. A failed message
keeps its last error for operators. One endpoint's failures never block a message for another endpoint, because the
worker claims by age and not by endpoint.

## Decisions

1. Delivery is at least once, and duplicates are allowed (accepted requirement 2).
2. Every attempt sends the message identifier as the `Idempotency-Key` header.
3. The attempt count increases when a message is claimed, before the post. A worker that stops mid-post still used an
   attempt.
4. A message becomes `failed` at five attempts, and the last error is kept.
5. The service gives no ordering guarantee between messages.

## Open questions

1. How is a message reclaimed when its worker stops while the message is `in_flight`? The options are an expiry time on
   the claim, releasing a worker's claims when a worker with the same identifier starts, or a separate sweep.
2. Which signal tells operators that a message has been in flight for too long?
