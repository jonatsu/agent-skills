# Writing Quality Targets

A quality target is useful only when a test, a load run, or a monitor can say whether it holds.

## The Scenario

Write each target in this form:

```text
Trigger:     who or what starts it, such as 2,000 searches a second or a lost zone
Conditions:  the state and load it holds under
Response:    what the system does
Measure:     the number that decides pass or fail, with its unit and window
On breach:   what the system does when the measure is not met
```

A simple target folds into one sentence when its trigger and conditions are obvious: "p95 search latency stays
under 250 ms at 2,000 searches a second." Use the full form when context changes the meaning, such as a
compliance duty or a failure condition. Every measure needs a number, a unit, the load it holds at, and a window.

## Latency and Throughput

State latency as percentiles, such as p50 and p99, at a stated load. An average hides the slow tail that users
feel. Name what the latency covers: the whole request, or one component. State throughput as an average and a
peak rate, with the window the peak is measured over.

## Availability and Error Budget

An SLO is the share of good events over a window, measured at a named point: "99.9% of requests in any 28 days
succeed within one second, measured at the load balancer". The error budget is the rest, the failures the window
allows. Its owner decides what may spend it, such as releases or risky changes. Set targets from what users need,
not from what the system does today, and keep them few. Set an internal SLO tighter than any SLA, the contract
that carries consequences.

| SLO    | Downtime per 30 days | Downtime per year |
| ------ | -------------------- | ----------------- |
| 99%    | 7.2 hours            | 3.65 days         |
| 99.9%  | 43.2 minutes         | 8.76 hours        |
| 99.95% | 21.6 minutes         | 4.38 hours        |
| 99.99% | 4.32 minutes         | 52.6 minutes      |

Dependencies in series multiply: two at 99.9% give about 99.8%. Redundant copies that fail independently give
`1 − (1 − a)^n`. Use that formula only for truly independent failures. A shared zone, deployment, or
configuration makes copies fail together, and the real figure is worse.

## Durability, Recovery, and Consistency

The RPO is the most data, measured in time, that may be lost. An RPO of five minutes needs replication or backup
at least that often, and a restore tested against it. The RTO is the time to restore service, and it includes
detecting the failure and deciding to fail over. Name the consistency each operation needs: strong, read-your-own
writes, monotonic reads, or eventual with a bound on staleness. A payment and a view counter rarely need the same.

## Rank the Targets

Rate each target high, medium, or low on two scales: its importance to users and the business, and how hard the
design makes it to meet. Targets high on both drive the decomposition first. A target low on both needs only a
check.
