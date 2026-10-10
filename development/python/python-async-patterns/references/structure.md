# Structuring Async Code

## Async Context Managers

`async with` is how an async resource gets released even when the body raises.

```python
class Connection:
    async def __aenter__(self) -> "Connection":
        self._transport = await open_transport(self.dsn)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self._transport.close()
```

`contextlib.asynccontextmanager` is shorter when there is no class to hang it on:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def connection(dsn: str):
    transport = await open_transport(dsn)
    try:
        yield transport
    finally:
        await transport.close()
```

The `try`/`finally` is the point. Without it, an exception in the caller's body skips the close.

`contextlib.AsyncExitStack` handles a variable number of resources, or resources acquired conditionally:

```python
async with AsyncExitStack() as stack:
    clients = [await stack.enter_async_context(make_client(u)) for u in upstreams]
```

## Async Iterators

Implement `__aiter__` and `__anext__` for a source that produces items over time, or use an async generator:

```python
async def paginate(client, url: str) -> AsyncIterator[dict]:
    while url:
        page = await client.get(url)
        for item in page["items"]:
            yield item
        url = page.get("next")
```

An async generator that owns a resource needs cleanup on early exit. When a consumer breaks out of the loop,
the generator is finalized by the loop at an unpredictable time; `aclosing` makes it deterministic:

```python
from contextlib import aclosing

async with aclosing(paginate(client, url)) as pages:
    async for item in pages:
        if item["id"] == target:
            break
```

## Producer and Consumer with a Queue

`asyncio.Queue` decouples the rate of production from consumption, and its `maxsize` is the backpressure.

```python
async def producer(queue: asyncio.Queue[Job]) -> None:
    async for job in source():
        await queue.put(job)          # blocks when full: this is the backpressure

async def consumer(queue: asyncio.Queue[Job]) -> None:
    while True:
        job = await queue.get()
        try:
            await handle(job)
        finally:
            queue.task_done()

async def main() -> None:
    queue: asyncio.Queue[Job] = asyncio.Queue(maxsize=100)
    async with asyncio.TaskGroup() as tg:
        producing = tg.create_task(producer(queue))
        workers = [tg.create_task(consumer(queue)) for _ in range(10)]
        await producing               # every job is now on the queue
        await queue.join()            # every queued job is now done
        for worker in workers:
            worker.cancel()
```

**An unbounded queue is a memory leak waiting for a slow consumer.** Always set `maxsize` when the producer
can outrun the consumer.

**Await the producer before `queue.join()`.** `join()` returns as soon as the queue's unfinished count is
zero, and immediately after `create_task` the producer has not run, so the count is still zero. Verified on
CPython 3.13.15: without the `await producing` line the workers are cancelled before handling anything and the
program silently processes no jobs at all.

`queue.join()` then returns when `task_done()` has been called for every item. Consumers loop forever, so
cancel them once the queue has drained; the `TaskGroup` exits cleanly afterwards.

## Background Tasks Need an Owner

```python
asyncio.create_task(background_work())     # wrong: nothing holds this
```

A bare `create_task` returns a task nobody references. The loop keeps only a weak reference, so it can be
garbage collected mid-flight, and any exception it raises surfaces late as "Task exception was never
retrieved", or not at all.

Give every task an owner:

```python
class Service:
    def __init__(self) -> None:
        self._tasks: set[asyncio.Task] = set()

    def spawn(self, coro) -> None:
        task = asyncio.create_task(coro)
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)

    async def aclose(self) -> None:
        for task in list(self._tasks):
            task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
```

A `TaskGroup` is better whenever the tasks' lifetime fits a lexical scope. This pattern is for tasks that
outlive any single scope, such as a server's background workers.

## Graceful Shutdown

A service should finish in-flight work and stop accepting new work, rather than dying mid-request.

```python
async def main() -> None:
    stop = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop.set)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(serve(stop))
        await stop.wait()
```

`loop.add_signal_handler` is Unix-only. On Windows, handle `KeyboardInterrupt` around `asyncio.run` instead.

Give shutdown a deadline. Waiting forever for a task that will not finish turns a graceful shutdown into a
hang:

```python
    try:
        async with asyncio.timeout(30):
            await drain_in_flight()
    except TimeoutError:
        log.warning("shutdown deadline exceeded, cancelling remaining work")
```

## Synchronizing Between Tasks

| Primitive           | Use for                                           |
| ------------------- | ------------------------------------------------- |
| `asyncio.Event`     | One-shot signal: shutdown, readiness              |
| `asyncio.Semaphore` | Bounding how many tasks do a thing at once        |
| `asyncio.Lock`      | Guarding a critical section that spans an `await` |
| `asyncio.Condition` | Waiting for a state change with a predicate       |
| `asyncio.Queue`     | Handing work between tasks with backpressure      |

Use `asyncio.Lock`, never `threading.Lock`, inside async code: the threading lock blocks the whole loop.

You need a lock only when state must stay consistent **across** an `await`. Code between two awaits cannot be
interrupted by another task on the same loop, so a purely synchronous update needs no lock.

## Request Context Across Tasks

`contextvars` carries per-request state — a request ID, a tenant, a trace span — through a call chain without
threading it through every signature. It is the async-safe replacement for a thread-local, because the event
loop interleaves requests on one thread and a thread-local would mix them up.

```python
from contextvars import ContextVar

request_id: ContextVar[str] = ContextVar("request_id", default="-")

async def handle(raw_id: str) -> None:
    token = request_id.set(raw_id)
    try:
        await do_work()          # anything downstream can read request_id.get()
    finally:
        request_id.reset(token)
```

Use the token and `reset` rather than setting the variable and walking away, so a reused worker coroutine does
not leak one request's identity into the next.

**A task gets a copy of the context, not a reference to it.** Measured on CPython 3.12.14 and 3.13.15: a child
task sees the value the parent had when `create_task` was called, and a `set()` inside the child is invisible
to the parent afterwards. Two consequences:

- Set the variable **before** spawning the tasks that should see it. A value set after `create_task` does not
  reach an already-running task.
- A task cannot return a value by setting a `ContextVar`. Return it, or write it somewhere both can reach.

The same copy-on-spawn rule applies to `TaskGroup.create_task`.

**Offloading to a thread splits on which call you use.** Measured on both versions: `asyncio.to_thread` copies
the calling context into the worker thread, so a logging filter reading these variables still works there.
`loop.run_in_executor` does **not** — the function runs with an empty context and every variable falls back to
its default, silently. Prefer `to_thread`; where you need a specific executor, carry the context yourself:

```python
context = contextvars.copy_context()
await loop.run_in_executor(pool, lambda: context.run(blocking_call, arg))
```

For logging, read the variables in a `logging.Filter` rather than passing them into every call site. The rest
of the logging setup is `python-style`'s subject, not this skill's.

## Retries

Retry a transient failure with a bounded count, exponential backoff, and jitter:

```python
async def with_retries(operation, attempts: int = 3, base: float = 0.5):
    for attempt in range(attempts):
        try:
            return await operation()
        except TransientError:
            if attempt == attempts - 1:
                raise
            await asyncio.sleep(base * 2**attempt + random.uniform(0, 0.1))
```

Jitter matters at scale: without it, every client that failed at the same moment retries at the same moment.

Retry only what is safe to repeat: a read is usually idempotent; a payment is not. Catch the transient
exception types by name, so that a `CancelledError`, which is a shutdown signal, propagates.

[tenacity](https://github.com/jd/tenacity) implements this and more if the project already has it.
