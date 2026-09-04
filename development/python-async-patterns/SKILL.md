---
name: python-async-patterns
description: Write and fix concurrent Python with asyncio. Use when deciding whether async helps at all, running work concurrently, adding timeouts or cancellation, offloading blocking or CPU-bound calls, building async context managers and iterators, or diagnosing a hung or blocked event loop.
license: MIT
compatibility: Examples target Python 3.11+, where TaskGroup and asyncio.timeout exist. Fallbacks for older versions are noted where they differ.
metadata:
  author: Joonas Onatsu
---

# Python Async Patterns

Concurrency with asyncio: structuring it, bounding it, cancelling it, and finding out why it stalled. Testing
async code is `python-testing`.

## First, Decide Whether Async Helps

Async buys concurrency for **waiting**, not for computing. A single event loop runs one thing at a time; it
wins only when that thing is usually blocked on I/O.

| Workload                                          | Use                                                         |
| ------------------------------------------------- | ----------------------------------------------------------- |
| Many concurrent network or database calls         | asyncio                                                     |
| CPU-bound computation                             | `ProcessPoolExecutor`, or a library that releases the GIL   |
| Mixed I/O and CPU                                 | asyncio, with the CPU work offloaded to a thread or process |
| A handful of sequential calls, a short script     | Plain synchronous code                                      |
| One request at a time, blocking library available | Plain synchronous code                                      |

**Async is not free.** It splits every library choice into two ecosystems, makes stack traces harder to read,
and turns any accidental blocking call into a stall that affects every other task. Adopt it when the
concurrency is the point, not because it sounds faster.

**Stay fully sync or fully async along a call path.** A sync function that needs an async result has no good
options: `asyncio.run` inside a running loop raises, and blocking on a future deadlocks. Push the boundary out
to the program's entry point instead.

## Run Concurrent Work with TaskGroup

`asyncio.TaskGroup` (Python 3.11+) is the default for running tasks together. It waits for all of them, and
if one fails it cancels the rest and raises an `ExceptionGroup`.

```python
async def fetch_all(urls: list[str]) -> list[Response]:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch(url)) for url in urls]
    return [t.result() for t in tasks]
```

Handle the failures with `except*`:

```python
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(fetch(url))
            tg.create_task(refresh_cache())
    except* TimeoutError as eg:
        log.warning("timed out: %s", eg.exceptions)
    except* ValueError as eg:
        log.error("bad response: %s", eg.exceptions)
```

### Why Not gather

`asyncio.gather` is still correct for simple cases, but its failure behavior surprises people. Measured on
CPython 3.13.15: when one coroutine raises, `gather` propagates that exception immediately **and leaves the
other tasks running**. A sibling scheduled to finish later still finished after the exception had already
propagated.

That is a leak: work continues after the caller has moved on, holding connections and possibly writing
somewhere, with nothing awaiting its result. `TaskGroup` cancels siblings instead, which is almost always what
was meant.

```python
results = await asyncio.gather(*coros, return_exceptions=True)
```

`return_exceptions=True` returns exceptions inline as results rather than raising, so the call always
completes. Use it when you genuinely want every result including the failures, and remember that you must then
inspect the list — `isinstance(r, Exception)` — because nothing raises on your behalf.

Reach for `gather` when you want a list of results from a fixed set of coroutines and no cancellation
semantics. Reach for `TaskGroup` the rest of the time.

## Bound Everything That Waits

An `await` on the network with no timeout can hang forever.

```python
async with asyncio.timeout(5):
    data = await fetch(url)
```

`asyncio.timeout` is 3.11+. Before that, `asyncio.wait_for(fetch(url), timeout=5)`. From 3.11
`asyncio.TimeoutError` is an alias of the built-in `TimeoutError`, so catching the built-in is correct on both.

Bound concurrency too. Ten thousand tasks against one API is a denial-of-service attack on your own
dependency:

```python
semaphore = asyncio.Semaphore(20)

async def fetch_bounded(url: str) -> Response:
    async with semaphore:
        return await fetch(url)
```

The client's own connection pool is the other half of this, and it is per-client: creating a fresh
`ClientSession` or `AsyncClient` per request throws the pool away. Create one, reuse it, close it.

## Cancellation Is Not an Error

`CancelledError` inherits from `BaseException`, so `except Exception` does not catch it — deliberately. If you
catch it explicitly, re-raise:

```python
async def worker():
    try:
        while True:
            await do_a_unit()
    except asyncio.CancelledError:
        await release_resources()
        raise                      # without this, cancellation silently fails
```

Swallowing `CancelledError` produces a task that ignores shutdown, a `TaskGroup` that will not exit, and a
process that hangs on Ctrl-C. Use `finally` for cleanup that must run either way, and keep it short: an
`await` in a cleanup path can itself be cancelled.

## Never Block the Loop

One blocking call stalls every task in the process. `time.sleep`, `requests.get`, a synchronous database
driver, `open().read()` on a slow disk, and any CPU-heavy loop all do it.

```python
result = await asyncio.to_thread(blocking_call, arg)          # I/O-bound blocking library

loop = asyncio.get_running_loop()
result = await loop.run_in_executor(process_pool, cpu_heavy, arg)   # CPU-bound
```

`asyncio.to_thread` (3.9+) suits a blocking I/O library with no async equivalent. CPU work needs a process
pool; a thread still holds the GIL for the duration.

Run with `PYTHONASYNCIODEBUG=1` during development. The loop then logs any callback that takes too long, which
finds accidental blocking that reading the code does not.

## Structure

Async context managers and iterators, background task lifetime, queues, and producer-consumer shapes are in
[structure.md](references/structure.md). Read it when the work is a pipeline or a long-lived service rather
than a batch of calls.

## Diagnosing

| Symptom                               | Look at                                                      |
| ------------------------------------- | ------------------------------------------------------------ |
| Nothing runs concurrently             | Awaiting each call in a loop instead of scheduling first     |
| Whole process stalls                  | A blocking call on the loop; run with `PYTHONASYNCIODEBUG=1` |
| Hangs on shutdown or Ctrl-C           | `CancelledError` caught without re-raising                   |
| `coroutine ... was never awaited`     | A coroutine created and dropped; nothing ran                 |
| Work continues after an error         | `gather` without `TaskGroup`; siblings are not cancelled     |
| `attached to a different loop`        | An object created under one loop used under another          |
| Unbounded memory or connection errors | No semaphore, or a client created per request                |

Deeper diagnosis, including `asyncio.all_tasks` snapshots and reading a stalled loop, is in
[diagnosing.md](references/diagnosing.md).

## The Ecosystem

Prefer the standard library. Reach for these when they solve a problem you actually have.

| Tool                                                                                     | What it gives you                                                                 |
| ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| [uvloop](https://github.com/MagicStack/uvloop)                                           | A faster event loop implementation, drop-in on Linux and macOS                    |
| [anyio](https://github.com/agronholm/anyio)                                              | One API over asyncio and Trio, plus structured concurrency on both                |
| [Trio](https://github.com/python-trio/trio)                                              | A separate async runtime built around structured concurrency and cancel scopes    |
| [aiomisc](https://github.com/aiokitchen/aiomisc)                                         | Service scaffolding: entrypoints, worker pools, periodic tasks, graceful shutdown |
| [aiofiles](https://github.com/Tinche/aiofiles)                                           | File I/O offloaded to a thread pool behind an async API                           |
| [httpx](https://github.com/encode/httpx), [aiohttp](https://github.com/aio-libs/aiohttp) | Async HTTP clients                                                                |

Check the upstream documentation for the current API rather than trusting a summary. Note that Trio is a
different runtime, not a library you add to an asyncio program; anyio is the way to write code that runs on
both.

## Before Calling Async Code Done

1. Does every network or subprocess `await` have a timeout?
2. Is concurrency bounded by a semaphore or a pool, rather than by the size of the input?
3. Does every task that catches `CancelledError` re-raise it?
4. Is there any blocking call on the loop? Check with `PYTHONASYNCIODEBUG=1`.
5. Are long-lived clients created once and closed, rather than per call?
6. If a task fails, do its siblings stop?
