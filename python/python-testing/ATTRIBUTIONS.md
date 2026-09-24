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
pytest-xdist, pytest-randomly, pytest-timeout, pytest-mock, pytest-subtests, mutmut, atheris. Third-party
interfaces move, so the upstream link is the authority rather than any summary here.

## Mutation Testing and Fuzzing, 2026-09-24

`references/mutation-testing.md` and `references/fuzzing.md` are independently written from runs on this
machine against a copy of this repository's `skill_source/descriptions.py` and its tests: mutmut 3.8.0 and
atheris 3.1.0 on Python 3.12, installed ephemerally with `uv run --with`. The counts, survivors, throughput
figures, and the configuration-shadowing failure are observed results. mutmut's configuration keys and file
lookup order were read from its installed `configuration.py`.

Candidates considered and not adopted: GitLab's `pythonfuzz`, whose hosting feature GitLab deprecated in 18.0
as unmaintained, and the PyPI `fuzzing` package, last released in 2015 for Python 3.3 to 3.5. cosmic-ray and
poodle are maintained mutation tools that were not trialled. The OSS-Fuzz Python integration guide is linked
as further reading; no text from it is carried.

## Python Defaults Review, 2026-09-11

Reviewed Integralist's `.claude/rules/python.md` in `Integralist/agent-skills` at commit
`07155927c4a44cf97b050ea4f728fce840822ce9`:

<https://github.com/Integralist/agent-skills/blob/07155927c4a44cf97b050ea4f728fce840822ce9/.claude/rules/python.md>

The comparison informed the preference for public-behavior tests, with deliberate exceptions for internal logic.
The expression is independent; no upstream text or code is copied or adapted.
No license covering these rules was found in the pinned tree; the MCP component has separate licensing.
