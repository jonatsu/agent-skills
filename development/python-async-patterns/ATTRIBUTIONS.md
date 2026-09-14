# Attributions

## Current Skill

- Skill: `python-async-patterns`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: independently written, replacing a third-party package whose concurrency guidance was a version behind

## Predecessor

Replaces `async-python-patterns` from
[wshobson/agents](https://github.com/wshobson/agents) `plugins/python-development/skills`, MIT, which was
deployed unreviewed until 2026-09-04. No text or code was carried across.

One idea is retained because it was the package's best asset: the **sync-versus-async decision table** that
puts the "should this be async at all" question before any technique, together with its rule about not mixing
the two along a call path. The pitfalls it listed — forgetting `await`, blocking the loop, catching
`CancelledError` without re-raising — are genuine and appear here, restated and with the reasons attached.

Three things were deliberately not carried:

- **`gather` as the default for concurrent work.** The predecessor taught `gather` exclusively; a search of
  the whole package found no mention of `TaskGroup`, `asyncio.timeout`, or anyio, despite its siblings
  targeting Python 3.12.
- **Its error-handling example**, which was incoherent: a wrapper swallowed the exception and returned `None`,
  so the accompanying `return_exceptions=True` collected nothing and the "failed" count it printed was always
  zero.
- **`typing.List` and `typing.Optional`**, which contradicted the built-in generic and `X | None` forms taught
  by its own sibling skills.

## Influencing Sources

Read on 2026-09-15. Neither supplied wording or code; each surfaced a subject the skill had omitted, and every
claim below was written from the measurements in the next section rather than from the source.

- ["Python Async Best Practices"](https://github.com/sempervent/sempervent.github.io/blob/main/docs/best-practices/python/python-async-best-practices.md),
  sempervent. Prompted three additions: `asyncio.shield` for cleanup that must finish, `contextvars` for
  request context across tasks, and timeout **placement** — one outer budget plus a per-attempt deadline —
  rather than only the existence of timeouts. Its concurrency-limit formulas, resource-manager class, and
  structured-logging class were reviewed and not adopted; so were two defects in it, a per-task `try`/`except`
  inside a `TaskGroup` body and a test that swallows `CancelledError` against its own stated rule.
- ["Asynchronous Programming in Python"](https://kitchingroup.cheme.cmu.edu/pycse/book/25-async-programming.html),
  John Kitchin, *pycse*. Prompted two additions: `asyncio.as_completed` for handling results in completion
  order, and the already-running-loop case that Jupyter users hit. Its `wait_for`-first timeout framing,
  `get_event_loop()` usage, "fire and forget" description of `create_task`, and an `aiohttp` example that
  reads responses after closing the session were all reviewed and not adopted.

## Verified Behavior

Measured on CPython 3.13.15 on 2026-09-04 rather than taken from documentation:

- `asyncio.gather` propagates the first exception immediately **and leaves sibling tasks running**. A sibling
  scheduled to finish later still ran to completion after the exception had propagated.
- `asyncio.TaskGroup` cancels sibling tasks when one fails, delivering `CancelledError` into the sibling, and
  raises the failure as an `ExceptionGroup` catchable with `except*`.
- `asyncio.gather(..., return_exceptions=True)` returns exception instances inline among the results rather
  than raising.

These three measurements are the basis for recommending `TaskGroup` over `gather` as the default.

Measured on both CPython 3.12.14 and 3.13.15 on 2026-09-15, for the additions above:

- **`as_completed` differs across the 3.13 boundary.** On 3.12 it is a plain generator yielding opaque
  coroutine wrappers, and `async for` over it raises `TypeError`. On 3.13 it is additionally an async iterator,
  and *that* iteration yields the original task objects; its synchronous iteration still yields wrappers.
- **`as_completed` leaves siblings running** when one task raises, on both versions — the same leak `gather`
  has.
- **`asyncio.shield` survives its awaiter's cancellation.** The shielded coroutine ran to completion after the
  task awaiting it had been cancelled.
- **Nested `asyncio.timeout` blocks compose.** The inner deadline raises `TimeoutError` inside the outer block,
  leaving the surrounding loop in control; an outer budget shorter than the attempts need cuts the operation
  off mid-attempt at its own deadline.
- **A task receives a copy of the context.** A child sees the parent's value at `create_task` time, and a
  `set()` inside the child does not reach the parent afterwards.
- **`asyncio.to_thread` propagates contextvars; `loop.run_in_executor` does not.** The executor call ran with
  an empty context and every variable silently fell back to its default. `contextvars.copy_context()` plus
  `context.run(...)` restores it.
- **Starting a loop inside a running loop fails with two distinct messages.** `asyncio.run` raises
  `asyncio.run() cannot be called from a running event loop`; `loop.run_until_complete` raises
  `This event loop is already running`.

## External Tools Referenced

Named with a link and a one-line purpose, with no vendored API surface: uvloop, anyio, Trio, aiomisc,
aiofiles, httpx, aiohttp, tenacity, py-spy. Third-party interfaces move, so the upstream link is the authority
rather than any summary here.
