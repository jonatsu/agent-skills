# Diagnosing Async Failures

Read this when async code hangs, stalls, leaks, or runs slower than the synchronous version it replaced.

## Debug Mode First

```bash
PYTHONASYNCIODEBUG=1 python -m myapp
```

Or `asyncio.run(main(), debug=True)`. Debug mode logs callbacks that take too long, warns about coroutines
that were never awaited, and reports tasks destroyed while pending. It is the cheapest way to find accidental
blocking, because the log names the callback rather than leaving you to read every dependency.

Adjust the threshold when the default is too noisy or too quiet:

```python
loop = asyncio.get_running_loop()
loop.slow_callback_duration = 0.05     # seconds
```

## Nothing Runs Concurrently

The most common async bug is sequential code wearing async syntax:

```python
for url in urls:
    results.append(await fetch(url))       # each await completes before the next starts
```

`await` means "wait for this now". Concurrency requires scheduling the work first:

```python
async with asyncio.TaskGroup() as tg:
    tasks = [tg.create_task(fetch(url)) for url in urls]
results = [t.result() for t in tasks]
```

Symptom: total time equals the sum of the parts rather than the slowest part.

## The Whole Process Stalls

One blocking call freezes every task. Candidates, in rough order of likelihood:

- `time.sleep` instead of `asyncio.sleep`
- A synchronous HTTP client (`requests`, `urllib`) in an async function
- A synchronous database driver
- Large file reads, `json.loads` on a very large payload, compression, hashing
- A tight CPU loop

Debug mode names it. Failing that, `py-spy dump --pid <pid>` shows what every thread is doing without
modifying or restarting the process, which is usually the fastest answer in production.

The fix is `asyncio.to_thread` for blocking I/O, a `ProcessPoolExecutor` for CPU work, or an async-native
library.

## It Hangs on Shutdown

Usually one of three things:

1. **A task caught `CancelledError` without re-raising.** It ignores cancellation, so the `TaskGroup` or
   `gather` waiting on it never returns.
2. **An `await` with no timeout.** Something upstream never answers and nothing bounds the wait.
3. **A consumer loop with no exit.** `while True: await queue.get()` never finishes on its own; it must be
   cancelled.

Snapshot what is still pending:

```python
for task in asyncio.all_tasks():
    print(task.get_name(), task.get_coro())
    task.print_stack()
```

Naming tasks at creation, `tg.create_task(work(), name="refresh-cache")`, turns that dump from a list of
anonymous coroutines into something readable. Do it as a matter of course for long-lived tasks.

## Errors That Vanish

```text
Task exception was never retrieved
```

A task raised and nobody awaited its result. The exception surfaces whenever the task is garbage collected,
which may be much later or never. The cause is almost always a fire-and-forget `create_task` with no owner;
see the background-task section in [structure.md](structure.md).

```text
coroutine 'fetch' was never awaited
```

A coroutine was created and dropped, so its body never ran. Usually a forgotten `await`, or passing
`fetch(url)` where a callable was expected.

Under a `TaskGroup`, failures arrive as an `ExceptionGroup`. A plain `except ValueError` does not match one —
use `except*`, or `except ExceptionGroup` if you need the whole group.

## Loop Mismatch

```text
RuntimeError: ... is attached to a different loop
```

An object bound to one event loop is being used from another. Common causes: a client or lock created at
import time, before any loop exists; `asyncio.run` called more than once, each call creating and destroying a
loop; a test fixture whose loop scope is narrower than the tests using it.

Create loop-bound objects inside the coroutine that uses them, or in a lifespan or fixture whose scope matches.

## Leaks

**Connections.** Creating an `aiohttp.ClientSession` or `httpx.AsyncClient` per request discards the pool and
eventually exhausts file descriptors. Create one, reuse it, close it on shutdown.

**Tasks.** `len(asyncio.all_tasks())` growing over time means tasks are being created faster than they finish.

**Queues.** An `asyncio.Queue` with no `maxsize` grows without limit when the producer outruns the consumer.
The process dies of memory exhaustion far from the cause.

## Async Is Slower Than the Sync Version

Real, and usually one of:

- **The workload is CPU-bound.** Async adds scheduling overhead and no parallelism.
- **The concurrency is one.** Sequential awaits, as above.
- **Blocking calls dominate.** The loop spends its time stalled.
- **Per-call client construction.** TLS handshakes repeated for every request.
- **The dependency is the bottleneck.** More concurrency against a saturated server makes it worse, not
  better. Bound it with a semaphore and measure.

Measure before changing anything. `asyncio.run(main(), debug=True)` plus a timer around the phases usually
localizes it in one run.
