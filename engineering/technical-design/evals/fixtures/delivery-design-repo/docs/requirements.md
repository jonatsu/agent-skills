# Delivery Requirements

Status: accepted. Revision 1, accepted 2026-09-18 by the product owner.

## Requirements

1. Every message the service accepts is delivered to its subscriber endpoint at least once, unless five delivery
   attempts have failed.
2. A subscriber can receive the same message more than once. Each attempt carries the message identifier so that the
   subscriber can recognize a repeat.
3. A message whose five attempts have failed is marked failed and stays visible to operators with its last error.
4. Delivery to one slow or failing endpoint does not stop delivery to other endpoints.

## Non-goals

- Ordering of messages, within or across endpoints.
- Delivery to endpoints other than HTTPS URLs.
