---
name: system-design
description: "Design a system's qualities and structure: latency, throughput, and availability as SLOs and scenarios, capacity estimates, components and deployment units, data and communication, and failure handling. Use when sizing a system or asking whether it will handle a load, setting SLOs, RTO, or RPO, or finding bottlenecks and single points of failure. Writing the design document goes to technical-design, reviewing a settled design to architecture-review, and a live performance failure to systematic-debugging."
license: MIT
metadata:
  author: Joonas Onatsu
---

# System Design

Decide how a system meets its quality targets: how fast, how available, how large, and how it fails. Turn each
target into a number, estimate the resources it needs, and shape components, data, and deployment around the
targets that matter most. `technical-design` runs this skill as its "Settle System Qualities" step and records the
result in the design document. A standalone question, such as whether a system will handle ten times its load,
uses the same method and gets its answer in the reply.

A quality target is a business decision: a service level, a retention period, or how much data may be lost.
Propose a number with its cost, and let the user or the spec settle it.

## Fit the Depth to the Stakes

Run every step, at a depth that fits the work. A change that moves no target, adds no load, and changes no
deployment clears the skill in one sentence saying so. Go deep when a target is tight, load is large or growing,
data is hard to recover, or a failure costs money, safety, or trust. Estimate only where a number could change a
decision, because a design built for load nobody expects is a defect too.

## 1. State the Quality Targets

Write each target the design must meet as a scenario that a test or a measurement could check. Read
[references/quality-scenarios.md](references/quality-scenarios.md) before writing them. Each scenario names:

- what triggers it, such as a request, a load peak, or a failed zone;
- the conditions it holds under, including the load;
- the response the system gives, and its measure, such as a percentile latency or an SLO over a window; and
- what the system does when the measure is breached.

Give durability as the data that may be lost (RPO), and recovery as the time to restore service (RTO). Name the
consistency each operation needs, rather than one setting for the whole system. Rank the targets by importance to
users and by difficulty to meet; the highly ranked ones drive the steps that follow.

The step is done when every target has a measure, the load it holds at, and a failure response, or is listed as
an open question with its owner.

## 2. Estimate the Load and Capacity

Derive the numbers the design depends on, as [references/capacity.md](references/capacity.md) describes: average
and peak rates, item sizes, growth and retention, replicas, the working set, and bandwidth. Mark each input as
measured, with its source, or assumed. Round up, and carry units through the arithmetic.

Compare each result with the ceiling of one unit, such as one disk's IO rate, one machine's memory, one network
link, or one database primary. Take each ceiling from a measurement or the vendor's documentation, never from
memory. The quantity that exceeds a single unit's ceiling first is the binding constraint, and it shapes the
design.

The step is done when every number that drives a decision traces to marked inputs, and the binding constraint is
named.

## 3. Decompose Around the Drivers

Split the system into parts, starting from the whole and working down. For each part:

1. Name its drivers: the highly ranked targets and the constraints it must meet.
2. Choose an approach that meets them, from [references/tactics.md](references/tactics.md), and state what it
   costs.
3. Assign each child part its responsibility, and define the interfaces between the children.
4. Check that the children together still meet the drivers, then take the next part.

Stop when each part is small enough for `technical-design` to define as a component. Separate parts that scale,
fail, or change at different rates, so each can grow or fail alone. Name the levels as the C4 model does: the
system, its containers, which are separately deployed units such as a service or a database, and the
components inside them. Name too the deployment nodes each container runs on.

The step is done when every highly ranked target is assigned to the parts that meet it, and every part has its
responsibility and interfaces.

## 4. Choose Data and Communication from Access Patterns

List each operation with its rate, item size, latency target, and consistency. Choose each store from how it is
read and written: lookup by key, range scans, relations and joins, full-text search, time series, or an append
log. Choose the data model first and the product second. Add replicas for availability or read load, and state
what replication lag shows the reader. Choose a sharding key from the access pattern, and check it for hot keys.
Use a transaction where an invariant spans several items.

Call synchronously when the caller needs the result to continue, and asynchronously, through a queue or stream,
when the work may finish later. A queue that delivers at least once needs an idempotent consumer. For each cache,
state what it holds, where it sits, how it is invalidated, what a stale read costs, and what happens to the
store behind it when the cache is empty.

The step is done when every operation has its store, its consistency, and its path, and every cache states its
invalidation and what a stale read costs.

## 5. Iterate Until It Fits and Survives

Ask four questions of each candidate design, and change it until all four pass:

1. **Possible:** does it meet the targets if limits are ignored?
2. **Simpler:** can a smaller design reach the same targets?
3. **Feasible:** does it fit the ceilings from step 2 and the budget?
4. **Resilient:** what happens when each part fails, up to a whole zone or region?

On every pass, look for:

- single points of failure, including one machine, zone, region, dependency, or a manual step;
- the next ceiling, such as IO, network, CPU, memory, a lock, or a step that must run in sequence;
- the latency budget across hops, built from per-hop budgets, because percentiles do not add, and a request
  that waits on many calls waits on the slowest; and
- hot spots, where one key, tenant, or item takes a disproportionate share of the load.

Then run the failure pass. For each dependency, decide its timeout, its retry with backoff, jitter, and a budget,
and whether it needs a circuit breaker, a bulkhead, backpressure, or load shedding. Decide what the user sees in
degraded operation, and how quickly monitoring detects the failure. Take each fix from
[references/tactics.md](references/tactics.md) with its cost.

The step is done when every highly ranked target holds at its stated load, and every single point of failure is
removed or accepted by its owner with what it costs in error budget.

## 6. Record the Result

Within a design, `technical-design` records each result in arc42:

- the targets and scenarios in section 10;
- the deployment units and nodes in section 7;
- the tactics that cut across parts in section 8;
- each choice with its rejected alternatives in section 9; and
- the risks left open in section 11.

For a standalone question, answer it in the first sentence. Then give the targets assumed, the estimate with its
marked inputs, the binding constraint, the design, and the open questions. Keep every input visible, so that a
reader can rerun the estimate with their own numbers.

## Attributions

See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for the sources this skill is based on.
