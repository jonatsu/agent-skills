---
name: python-async-patterns
description: Write and fix concurrent Python with asyncio. Use when deciding whether async helps at all, running tasks concurrently, adding timeouts or cancellation, offloading a blocking call from the event loop, building async context managers and iterators, or diagnosing a hung or blocked event loop.
license: MIT
compatibility: Examples target Python 3.11+, where TaskGroup and asyncio.timeout exist. Fallbacks for older versions are noted where they differ.
metadata:
  author: Joonas Onatsu
---

# Python Async Patterns

Concurrency with asyncio: structuring it, bounding it, cancelling it, and finding out why it stalled. Testing
async code is `python-testing`. This skill hands work off the event loop; choosing threads or processes for
that work, and running the pool, is `python-parallelism`.

## Respect Project Conventions

Use these defaults for new projects. In established projects, follow declared conventions and consistent local practice,
including for new files and modules. Check both before filling an undecided choice.

Do not recommend changes merely because these defaults differ. Recommend corrections supported by incorrect behavior,
security vulnerabilities, or concrete reliability or maintenance harm. Explain the evidence, consequence, and smallest
remedy. A different tool, layout, style, or supported syntax is not itself a defect.

Apply fixes within the authorized task; otherwise report the recommendation without changing the project.
An explicit modernization or conventions review permits broader recommendations.

## First, Decide Whether Async Helps

Async buys concurrency for **waiting**, not for computing. A single event loop runs one thing at a time; it
wins only when that thing is usually blocked on I/O.

| Workload                                          | Use                                                         |
| ------------------------------------------------- | ----------------------------------------------------------- |
| Many concurrent network or database calls         | asyncio                                                     |
| CPU-bound computation                             | Not asyncio: `python-parallelism`                           |
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

This shows the grouping only: a real `fetch` also needs a timeout and a concurrency bound, both in the next
section.

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

When one coroutine raises, `asyncio.gather` propagates that exception immediately **and leaves the other tasks
running**. That is a leak: work continues after the caller has moved on, holding connections and possibly
writing somewhere, with nothing awaiting its result. `TaskGroup` cancels siblings instead, which is almost
always what was meant.

```python
results = await asyncio.gather(*coros, return_exceptions=True)
```

`return_exceptions=True` returns exceptions inline as results rather than raising, so the call always
completes. Use it when you want every result including the failures, then inspect the list with
`isinstance(r, Exception)`, because nothing raises on your behalf.

Reach for `gather` when you want a list of results from a fixed set of coroutines and no cancellation
semantics. Reach for `TaskGroup` the rest of the time.

### Handling Results as They Arrive

Neither `TaskGroup` nor `gather` gives you a result before the whole batch is ready. `asyncio.as_completed`
yields each awaitable in completion order, which is what you want to stream results, show progress, or stop
early on the first good answer. **Its interface changed in 3.13, and the two versions call for different
code.**

**On 3.12 and earlier** it is a plain generator that yields opaque coroutine wrappers, not the tasks you passed
in. `async for` over it raises `TypeError`, and the wrapper does not say which input it came from, so carry the
identity in the result:

```python
for wrapper in asyncio.as_completed(coros):
    name, value = await wrapper        # the coroutine returns its own identity
    record(name, value)
```

**On 3.13 and later** it is also an async iterator, and `async for` yields the **original** task objects:

```python
async for task in asyncio.as_completed(tasks):
    record(await task)
```

The synchronous iterator still yields wrappers on 3.13, so the 3.12 form runs on both. Write it when the code
must support 3.12; use `async for` where 3.13 is the floor.

Either way, `as_completed` inherits `gather`'s leak: on both versions, when one task raises, the exception
propagates and **the siblings keep running**. Wrap the loop in a `TaskGroup`, or cancel the rest yourself once
you have what you came for.

## Bound Everything That Waits

An `await` on the network with no timeout can hang forever.

```python
async with asyncio.timeout(5):
    data = await fetch(url)
```

`asyncio.timeout` is 3.11+. Before that, `asyncio.wait_for(fetch(url), timeout=5)`. From 3.11
`asyncio.TimeoutError` is an alias of the built-in `TimeoutError`, so catching the built-in is correct on both.

**Put timeouts at the boundaries, not on every step.** A timeout belongs where the program hands control to
something it does not run: a socket, a subprocess, a lock it might not win. Wrapping each internal step in its
own deadline produces numbers nobody can reason about, and their sum is not the deadline the caller cares
about. The shape that works is one outer deadline for the whole operation plus one inner deadline per attempt:

```python
async with asyncio.timeout(30):              # the caller's budget for the whole thing
    for attempt in range(ATTEMPTS):
        try:
            async with asyncio.timeout(5):   # this attempt's share
                return await fetch(url)
        except TimeoutError:
            if attempt == ATTEMPTS - 1:
                raise
```

Nested `asyncio.timeout` blocks compose: the inner one firing raises `TimeoutError` inside the block, leaving
the loop in control, and the outer one firing cuts the whole thing off mid-attempt at its own deadline. The
outer budget therefore bounds the retries, which without one multiply the worst case by the attempt count.
Backoff, jitter, and which failures are safe to retry are in [structure.md](references/structure.md).

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

### Shield the Cleanup That Must Finish

When a cleanup `await` must complete even though its task is being cancelled — committing a transaction,
releasing a lease, flushing a final record — `asyncio.shield` detaches it from the cancellation:

```python
try:
    await do_work()
except asyncio.CancelledError:
    await asyncio.shield(commit())     # commit() runs to completion
    raise
```

`shield` protects the **inner** coroutine, not the `await` on it: the awaiting task still receives
`CancelledError` at that line, so the `await` can raise while `commit()` keeps running detached. Shield only
the cleanup step that genuinely cannot be abandoned, and give it a timeout; a shielded task body is something
shutdown cannot stop.

## Keep Blocking Calls Off the Loop

One blocking call stalls every task in the process. `time.sleep`, `requests.get`, a synchronous database
driver, `open().read()` on a slow disk, and any CPU-heavy loop all do it.

```python
result = await asyncio.to_thread(blocking_call, arg)          # blocking I/O library, default thread pool

loop = asyncio.get_running_loop()
result = await loop.run_in_executor(pool, cpu_heavy, arg)     # CPU-bound: a long-lived process pool
```

`asyncio.to_thread` (3.9+) suits a blocking I/O library with no async equivalent. Create a process pool once
and reuse it rather than per call; whether the work wants threads or processes is `python-parallelism`'s
question. `run_in_executor` drops `contextvars`, which [structure.md](references/structure.md) covers.

Run with `PYTHONASYNCIODEBUG=1` during development. The loop then logs any callback that takes too long, which
finds accidental blocking that reading the code does not.

## Structure

Read [structure.md](references/structure.md) when the work is a pipeline, a long-lived service, or a resource
to acquire and release, rather than a batch of calls. It covers async context managers and iterators,
background task ownership, queues and backpressure, graceful shutdown, synchronization primitives, request
context with `contextvars`, and retries.

## Diagnosing

| Symptom                                      | Look at                                                    |
| -------------------------------------------- | ---------------------------------------------------------- |
| Nothing runs concurrently                    | Awaiting each call in a loop instead of scheduling first   |
| Whole process stalls                         | A blocking call on the loop; run in debug mode             |
| Hangs on shutdown or Ctrl-C                  | `CancelledError` caught without re-raising                 |
| `coroutine ... was never awaited`            | A coroutine created and dropped; nothing ran               |
| Work continues after an error                | `gather` without `TaskGroup`; siblings are not cancelled   |
| `attached to a different loop`               | An object created under one loop used under another        |
| `cannot be called from a running event loop` | `asyncio.run` in a notebook, test or handler; just `await` |
| Unbounded memory or connection errors        | No semaphore, or a client created per request              |

Read [diagnosing.md](references/diagnosing.md) when the row's fix does not resolve the symptom, when the
symptom is not listed, or when async code runs slower than the synchronous version. It covers `asyncio.all_tasks`
snapshots, `py-spy`, and each row in depth.

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

Check the upstream documentation for the current API rather than trusting a summary. Trio replaces asyncio
rather than adding to it, so an asyncio program adopts anyio to support both.

## Before Calling Async Code Done

1. Does every network or subprocess `await` have a timeout?
2. Is concurrency bounded by a semaphore or a pool, rather than by the size of the input?
3. Does every task that catches `CancelledError` re-raise it?
4. Is there any blocking call on the loop? Check with `PYTHONASYNCIODEBUG=1`.
5. Are long-lived clients created once and closed, rather than per call?
6. If a task fails, do its siblings stop?
