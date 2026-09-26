---
name: python-testing
description: "Write Python tests with pytest and its ecosystem. Use when writing or fixing tests, choosing fixtures, parametrizing cases, faking a boundary, testing async code, configuring pytest or coverage, working out why a test does not run, mutation-testing a Python suite, or fuzzing a Python parser. Triggers on: pytest, conftest.py, test_*.py, fixture, parametrize, monkeypatch, tmp_path, pytest.ini_options, mutmut, atheris."
license: MIT
compatibility: Assumes pytest. Plugins named here are installed per project; check what the project already has before adding one.
metadata:
  author: Joonas Onatsu
---

# Python Testing

Mechanics of testing Python: pytest, its fixtures, its plugins, and the tools that fake a boundary. This skill
answers "how do I express this test", not "what should we test".

**Strategy belongs elsewhere.** What to test, at which level, and whether coverage is adequate is
`test-engineer`. Writing a failing test before the code is `test-driven-development`. Project and dependency
setup is `python-project-management`. This skill assumes the decision to write a test has been made.

## Respect Project Conventions

Use these defaults for new projects. In established projects, follow declared conventions and consistent local practice,
including for new files and modules. Check both before filling an undecided choice.

Do not recommend changes merely because these defaults differ. Recommend corrections supported by incorrect behavior,
security vulnerabilities, or concrete reliability or maintenance harm. Explain the evidence, consequence, and smallest
remedy. A different tool, layout, style, or supported syntax is not itself a defect.

Apply fixes within the authorized task; otherwise report the recommendation without changing the project.
An explicit modernization or conventions review permits broader recommendations.

## Read the Project First

Before writing or running anything, find out what this project already does:

- **How tests run.** A bare `pytest`, a runner prefix, or a task recipe. Check `justfile`, `Makefile`,
  `tox.ini`, `noxfile.py`, CI workflows, and the project's contributing docs.
- **What is configured.** `[tool.pytest.ini_options]` in `pyproject.toml`, or `pytest.ini`, `tox.ini`,
  `setup.cfg`. Registered markers, `testpaths`, and default `addopts` change what a bare invocation does.
- **Which plugins are installed.** `pytest --version` lists them. An async test needs one; a fixture you were
  about to write may already exist in a plugin the project has.
- **Where tests live and how they are named.** Match the existing layout rather than introducing a second one.
- **What the existing tests look like.** Their fixture style, naming, and level of mocking are the house
  conventions.

Commands in this skill are written as bare `pytest`. If the project wraps it, use the wrapper. A project on
unittest or another framework keeps it; apply the pytest-specific guidance only where pytest runs.

## The Shape of a Test

```python
def test_rejects_a_negative_quantity():
    with pytest.raises(ValueError, match="quantity"):
        Order(quantity=-1)
```

Name the test after the behavior it pins, not the function it calls. `test_create_user` tells a reader
nothing when it fails at 03:00; `test_create_user_with_duplicate_email_raises_conflict` tells them what broke.

Assert with plain `assert`. pytest rewrites it and reports both sides, so `assertEqual`-style helpers buy
nothing.

One behavior per test. A test that asserts four unrelated things reports only the first failure and hides the
rest.

## Test Interfaces

Prefer tests through public behavior. Direct tests of complex internal logic are appropriate when they isolate meaningful
edge cases without excessive setup. Do not delete a branch merely because current public-interface tests do not reach it.
If extraction improves cohesion, use `python-architecture` to define a focused internal interface.

## Fixtures

A fixture supplies state or a dependency, and its scope decides how often that setup runs.

```python
@pytest.fixture
def order():
    return Order(quantity=1)

@pytest.fixture(scope="session")
def database_url(tmp_path_factory):
    return f"sqlite:///{tmp_path_factory.mktemp('db') / 'test.db'}"
```

| Scope                        | Created once per | Use for                                 |
| ---------------------------- | ---------------- | --------------------------------------- |
| `function` (default)         | Test             | Anything mutable                        |
| `class`, `module`, `package` | That grouping    | Expensive setup shared by related tests |
| `session`                    | Run              | Containers, servers, compiled artifacts |

**A wider scope shares mutable state between tests.** That is how a suite becomes order-dependent and starts
passing alone but failing in a full run. Widen scope only for setup that is genuinely expensive, and keep what
tests mutate at function scope.

Put fixtures used by more than one file in `conftest.py`, at the directory level where they apply. Fixtures do
not need importing; pytest resolves them by name from the nearest `conftest.py` upward.

Built-in fixtures worth knowing before writing your own: `tmp_path`, `tmp_path_factory`, `monkeypatch`,
`capsys`, `caplog`, `recwarn`.

Details, cleanup with `yield`, factory fixtures, parametrized fixtures, and faking boundaries:
[fixtures-and-doubles.md](references/fixtures-and-doubles.md).

## Parametrize Instead of Repeating

```python
@pytest.mark.parametrize(
    ("value", "expected"),
    [("1", 1), ("-1", -1), ("0", 0)],
)
def test_parses_an_integer(value, expected):
    assert parse_int(value) == expected
```

Each case is a separate test with its own result, so one failure does not hide the others. Cases, `ids`,
stacking, and property-based testing with Hypothesis: [parametrize-and-property.md](references/parametrize-and-property.md).
When a parser or decoder needs a longer, coverage-guided search than Hypothesis gives, fuzz it with atheris:
[fuzzing.md](references/fuzzing.md).

## Async Tests Need a Plugin, and Silence Is the Failure Mode

**On pytest 8 and earlier, an async test with no async plugin is skipped with a warning and the run exits 0.**
A whole async suite can look green without ever running; pytest 9 fails instead. Check for skips before
trusting an async run:

```bash
pytest -q -rs        # report skipped tests and the reason
```

Read [async-testing.md](references/async-testing.md) before writing the first async test in a project. It
covers the measurements, choosing between pytest-asyncio and anyio, `AsyncMock`, faking HTTP, and testing
cancellation and timeouts.

## Configuration

**Write pytest settings under `[tool.pytest.ini_options]` in `pyproject.toml`.** pytest 8 and earlier
silently ignore a bare `[tool.pytest]` table, so a coverage threshold written there reports success while never
running.

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = ["--strict-markers", "--strict-config"]
markers = ["slow: takes more than a second", "integration: needs a real dependency"]
```

`--strict-markers` turns a typo'd marker into an error instead of a silent no-op. Coverage settings, marker
registration, the measurements behind the table-name rule, and the rest:
[pytest-configuration.md](references/pytest-configuration.md).

## Faking a Boundary, and Not Faking Anything Else

Fake I/O, network, clocks, randomness and subprocesses. Do not fake the logic under test: a test that mocks
the thing it is testing asserts that the mock was configured, which is always true.

Prefer the narrowest fake that works, in this order:

1. **A real value.** Most functions need an argument, not a double.
2. **A built-in fixture.** `tmp_path` for the filesystem, `monkeypatch` for environment and attributes.
3. **A fake implementation** the project already has, or a small one you write.
4. **`unittest.mock`**, when you must assert on the interaction itself.

## When a Test Does Not Run

Symptoms and where to look:

| Symptom                          | Likely cause                                                          |
| -------------------------------- | --------------------------------------------------------------------- |
| Async test reported as skipped   | No async plugin, or a missing mode setting                            |
| Test not collected at all        | File or function name outside the discovery patterns                  |
| Marker appears to do nothing     | Unregistered marker, no `--strict-markers`                            |
| Coverage threshold never fails   | Settings under `[tool.pytest]` instead of `[tool.pytest.ini_options]` |
| Passes alone, fails in the suite | Shared state from a wider-scoped fixture                              |
| Passes locally, fails in CI      | Environment, time zone, locale, or ordering assumption                |

`pytest --collect-only` shows what pytest actually found, and `-rs` shows what it skipped. Both answer
"did my test run" faster than reading the code again.

## Before Calling a Test Done

1. Does it fail when the behavior it pins is broken? Break the code once and confirm. To ask that of a whole
   module or suite, run mutmut rather than mutating by hand: [mutation-testing.md](references/mutation-testing.md).
2. Does the failure message identify the cause without opening the test?
3. Does it pass in a full run and in isolation, in either order?
4. Does it avoid asserting on incidental detail: dict ordering, log wording, wall-clock time?
5. Was anything faked that is actually the thing under test?
