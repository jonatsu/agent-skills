# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## Third-party Sources

### Seth Hobson: `async-python-patterns` skill

- Source: <https://github.com/wshobson/agents>, `plugins/python-development/skills/async-python-patterns`
- License: `MIT`
- Version: read 2026-09-04

The skill supplied the sync-versus-async decision table that puts "should this be async at all" before any
technique, with its rule against mixing the two along a call path, and a list of common pitfalls. The idea and the
pitfalls are restated in new words and code; nothing was copied.

### sempervent: Python Async Best Practices

- Source: <https://github.com/sempervent/sempervent.github.io>,
  `docs/best-practices/python/python-async-best-practices.md`
- License: `GPL-3.0-only`
- Version: read 2026-09-15

The article prompted three additions: `asyncio.shield` for cleanup that must finish, `contextvars` for request
context across tasks, and the placement of timeouts. Nothing was copied.

### John Kitchin: pycse, "Asynchronous Programming in Python"

- Source: <https://kitchingroup.cheme.cmu.edu/pycse/book/25-async-programming.html>,
  in the repository <https://github.com/jkitchin/pycse>
- License: `GPL-2.0-or-later`
- Version: read 2026-09-15

The chapter prompted two additions: `asyncio.as_completed` for handling results in completion order, and the
already-running-loop case that notebook users hit. Nothing was copied. The repository's `LICENSE` is the GPL-2.0
text with no version notice; its `pyproject.toml` declares `GPL-3.0-or-later` for the Python package.
