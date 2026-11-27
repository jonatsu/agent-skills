# Tactics and Their Costs

Each tactic answers a problem and costs something. Name both when you choose one.

## Load and Scale

- **Reads exceed one store:** a cache, filled on a miss or ahead of reads. It costs staleness, an invalidation
  rule, and a surge on the store behind it when the cache is cold.
- **Reads exceed one store, and must stay fresh:** read replicas. Readers can see replication lag, and failover
  gets more complex.
- **Writes or data exceed one unit:** sharding by a key. Queries and transactions across shards get hard, a hot
  key overloads one shard, and resharding is a migration.
- **Bursts exceed steady capacity:** a queue between the burst and the worker. It adds latency, and the queue
  must be bounded and monitored.
- **The same work repeats:** precompute or batch it. Results are as old as the last run.

## Overload

- **Callers send more than the system serves:** rate limiting per client. A token bucket allows bursts up to its
  size; a fixed window allows a double burst at the window's edge; a sliding window is more exact and keeps more
  state. Replicas need a shared counter, and the design must say whether requests pass or fail when the limiter
  itself fails.
- **A consumer is slower than its producer:** backpressure through bounded queues or flow control. The producer
  slows down, or drops work by a stated rule.
- **Load exceeds capacity anyway:** load shedding by priority. Some requests fail fast, so that the rest succeed.
- **A part is degraded:** switch off optional features. Users lose them, and the degraded mode needs its own
  test.

## Failure of a Dependency

- **Calls hang:** a timeout on every call, shorter than the caller's own deadline, set from measured latency.
  Legitimately slow calls fail.
- **Failures are transient:** retry with exponential backoff, jitter, and a retry budget, only for idempotent
  operations. Retries multiply load during an outage, which the budget caps.
- **Failures repeat:** a circuit breaker that fails fast while open and probes before closing. It needs a
  fallback for the calls it refuses.
- **One dependency exhausts shared resources:** a bulkhead, a separate pool for each dependency. Utilisation
  drops.
- **One instance, zone, or region fails:** redundancy with failover, active-active or standby. It costs money,
  failover needs regular tests, and two sides that both think they lead need fencing or consensus.
- **A write is retried or duplicated:** an idempotency key stored with the result, or a consumer that removes
  duplicates. Keys must outlive the longest retry.

## Consistency Across Parts

- **A database write and its event must both happen:** a transactional outbox, relayed after commit. It adds a
  relay process and delivers at least once.
- **An operation spans services:** a saga, each step with a compensating action. Intermediate states are visible,
  and each compensation needs its own design.
- **State must agree across zones:** replicated consensus. Each write waits for a majority round trip, which caps
  the rate of writes that must run in sequence.
- **Reads need another shape than writes:** separate read and write models. They are kept in step, with lag.

## Lists

- **Offset pagination** is simple and allows jumping to a page. It slows at large offsets, and skips or repeats
  items when data changes.
- **Cursor or keyset pagination** stays stable and uses an index. It allows no jumping, and it needs a unique sort
  key.
