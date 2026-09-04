# Attributions

## Current Skill

- Skill: `python-testing`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: independently written, replacing a third-party package that mixed mechanics with strategy

## Predecessor

Replaces `python-testing-patterns` from
[wshobson/agents](https://github.com/wshobson/agents) `plugins/python-development/skills`, MIT, which was
deployed unreviewed until 2026-09-04. No text or code was carried across.

The predecessor's useful subjects informed this skill's coverage: pytest fixtures and scopes, parametrize,
monkeypatch, temporary directories, conftest layout, markers, coverage invocation, controlling time, database
fixtures, and property-based testing. Its retry-behavior examples, which use `side_effect` with a list to test
a retry loop, were the clearest thing in the package and the idea is retained in
`references/fixtures-and-doubles.md`.

Two things were deliberately not carried:

- **Test strategy.** The predecessor's description claimed test-driven development and its trigger list
  included implementing TDD, which collided with the locally maintained `test-driven-development` and
  `test-engineer` skills. This skill owns mechanics only and says so.
- **Its test-naming section**, which stated a convention and then gave "good" examples that did not follow it.

## Verified Behavior

Measured on 2026-09-04 on this machine rather than taken from documentation:

- A `[tool.pytest]` table in `pyproject.toml` is ignored by pytest 8.3.5 and honoured by 9.1.1. Identical
  settings with an invalid flag in `addopts` passed silently on 8.3.5 and errored on 9.1.1.
- An `async def` test with no async plugin installed is skipped with a warning and exit status 0 on pytest
  7.4.4 and 8.3.5, and fails naming the candidate plugins on 9.1.1. The file's only test asserted `False`.
- `unittest.mock.MagicMock` raises `TypeError: object MagicMock can't be used in 'await' expression` when
  awaited.
- `unittest.mock.patch(..., autospec=True)` produces `AsyncMock` for a class's coroutine methods and
  `MagicMock` for its ordinary methods.
- `pytest.mark.asyncio` under pytest-asyncio's default strict mode collects a marked test with no additional
  configuration.

## External Tools Referenced

Named with a link and a one-line purpose, with no vendored API surface: aioresponses, RESPX,
pytest-httpserver, freezegun, time-machine, pytest-docker, testcontainers-python, Hypothesis, pytest-cov,
pytest-xdist, pytest-randomly, pytest-timeout, pytest-mock, pytest-subtests. Third-party interfaces move, so
the upstream link is the authority rather than any summary here.
