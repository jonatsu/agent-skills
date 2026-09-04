# Structuring Async Code

Read this when the work is a pipeline, a long-lived service, or a resource that has to be acquired and
released, rather than a batch of independent calls.

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
        tg.create_task(producer(queue))
        workers = [tg.create_task(consumer(queue)) for _ in range(10)]
        await queue.join()            # wait until every queued job is done
        for worker in workers:
            worker.cancel()
```

**An unbounded queue is a memory leak waiting for a slow consumer.** Always set `maxsize` when the producer
can outrun the consumer.

`queue.join()` returns when `task_done()` has been called for every item. Consumers loop forever, so cancel
them once the queue has drained; the `TaskGroup` then exits cleanly.

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

Retry only what is safe to repeat. A read is usually idempotent; a payment is not. Do not retry a
`CancelledError` — that is a shutdown signal, not a transient failure.

[tenacity](https://github.com/jd/tenacity) implements this and more if the project already has it.
