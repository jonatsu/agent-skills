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

## Verified Behavior

Measured on CPython 3.13.15 on 2026-09-04 rather than taken from documentation:

- `asyncio.gather` propagates the first exception immediately **and leaves sibling tasks running**. A sibling
  scheduled to finish later still ran to completion after the exception had propagated.
- `asyncio.TaskGroup` cancels sibling tasks when one fails, delivering `CancelledError` into the sibling, and
  raises the failure as an `ExceptionGroup` catchable with `except*`.
- `asyncio.gather(..., return_exceptions=True)` returns exception instances inline among the results rather
  than raising.

These three measurements are the basis for recommending `TaskGroup` over `gather` as the default.

## External Tools Referenced

Named with a link and a one-line purpose, with no vendored API surface: uvloop, anyio, Trio, aiomisc,
aiofiles, httpx, aiohttp, tenacity, py-spy. Third-party interfaces move, so the upstream link is the authority
rather than any summary here.
