# Estimating Capacity

An estimate turns targets into resources and finds the binding constraint. Aim for the right order of magnitude;
the reasoning matters more than the final figures.

## Method

1. List the inputs: clients, operations per client per day, item size, read-to-write ratio, retention, replicas,
   and the ratio of peak to average load. Mark each as measured, with its source, or assumed.
2. Derive rates. A day has 86,400 seconds, about 10^5, so one million a day is about 12 a second. Multiply by the
   peak ratio, measured from real traffic where it exists.
3. Derive storage: items a day times size, retention, and replicas, plus index overhead.
4. Derive bandwidth: rate times size, in each direction. Multiply bytes by 8 for bits.
5. Name the working set: the data read often enough to belong in memory.
6. Divide each demand by the ceiling of one unit, taken from a measurement or the vendor's documentation. Add
   headroom for peaks, for losing one unit, and for growth over the planning horizon.
7. Name the binding constraint: the first resource whose demand exceeds one unit. It decides whether to shard,
   cache, batch, or change approach.

Write numbers in scientific notation so units stay straight, round each input up, and say that you did.

## Example

A notification service, with every input assumed: two million users, 20 notifications each a day, 1 KB per
stored record, kept 30 days, three replicas, and a peak five times the average.

- Writes: 2 × 10^6 × 20 / 8.64 × 10^4 ≈ 460 a second on average, about 2,300 at peak.
- Storage: 4 × 10^7 records a day × 1 KB × 30 days × 3 replicas ≈ 3.6 TB.
- Peak bandwidth in: 2,300 × 1 KB ≈ 2.3 MB/s, about 18 Mbit/s.

Storage and bandwidth fit one machine easily. Whether 2,300 writes a second, each copied to two replicas, fits one
database primary depends on that database's measured ceiling. That figure decides whether writes are the binding
constraint.

## Latency Budget

Start from the end-to-end target, subtract the measured fixed costs such as network round trips, and divide the
rest among the hops. A sum of per-hop percentiles is not the end-to-end percentile: with n hops, up to n percent
of requests can have some hop beyond its own p99. Budget each hop at a stricter percentile, and measure the whole
request. When one request
fans out to many calls, the chance that all are fast is the product of each one's chance. With 100 calls each fast
99% of the time, only about 37% of requests avoid a slow call.
