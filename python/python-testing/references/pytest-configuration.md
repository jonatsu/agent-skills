# pytest and Coverage Configuration

Read this when setting up pytest in a project, adding coverage, or working out why a setting has no effect.

## Where Configuration Lives

pytest reads the first of these it finds: `pytest.ini`, `pyproject.toml`, `tox.ini`, `setup.cfg`. A project
with more than one can be reading a file you are not editing. The run header prints the resolved `rootdir`
and `inifile`, and `pytest --collect-only -q` shows them without running anything.

In `pyproject.toml` the table is `[tool.pytest.ini_options]`.

## The Table Name Is a Silent Failure

**`[tool.pytest]` is ignored by pytest 8 and earlier.** Measured 2026-09-04 with identical settings containing
a deliberately invalid flag in `addopts`:

| pytest | Behavior with a bare `[tool.pytest]` table  |
| ------ | ------------------------------------------- |
| 8.3.5  | Ignored the table entirely; the run passed  |
| 9.1.1  | Read the table; errored on the invalid flag |

The consequence is worse than a missing setting: `--cov-fail-under=80` written under `[tool.pytest]` on
pytest 8 produces a green run with no coverage gate at all. Use `[tool.pytest.ini_options]`, which is correct
on every version.

To check that a project's settings are actually in force, put a nonsense flag in `addopts` temporarily. If the
run does not fail, the table is not being read.

## A Working Baseline

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--import-mode=importlib",
]
markers = [
    "slow: takes more than a second",
    "integration: needs a real external dependency",
]
filterwarnings = ["error"]
```

| Setting                      | Why                                                                       |
| ---------------------------- | ------------------------------------------------------------------------- |
| `testpaths`                  | A bare `pytest` collects only there, so the run is fast and predictable   |
| `pythonpath`                 | Makes a `src/` layout importable without installing                       |
| `--strict-markers`           | An unregistered marker becomes an error instead of a silent no-op         |
| `--strict-config`            | An unknown config key becomes an error                                    |
| `--import-mode=importlib`    | Avoids the `sys.path` manipulation of the legacy prepend mode             |
| `filterwarnings = ["error"]` | Turns a deprecation warning into a failure while it is still cheap to fix |

`filterwarnings = ["error"]` is the one to adopt deliberately. It is the difference between finding out about
a removal now and finding out when the dependency drops it, but on a legacy codebase it fails everything on
day one. Add per-warning ignores rather than abandoning it:

```toml
filterwarnings = [
    "error",
    "ignore:datetime.datetime.utcnow:DeprecationWarning",
]
```

## Markers

Register every marker. With `--strict-markers`, a typo like `@pytest.mark.itegration` fails the run instead of
silently marking nothing, which is the failure that makes people believe their exclusions work when they do
not.

```bash
pytest -m "not slow"          # skip the slow ones
pytest -m integration         # only integration tests
```

Gate anything needing a real dependency behind a marker and exclude it by default, so the ordinary run stays
fast:

```toml
addopts = ["-m", "not integration"]
```

Then run the excluded set explicitly in CI. Note that `addopts` and a command-line `-m` do not merge: the
command line replaces it.

## Coverage

Coverage comes from `pytest-cov`, configured under `[tool.coverage.*]`.

```toml
[tool.coverage.run]
branch = true
source = ["src/myproject"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
    "raise NotImplementedError",
]
```

```bash
pytest --cov --cov-report=term-missing
pytest --cov --cov-fail-under=80
```

`branch = true` matters: line coverage counts an `if` as covered when only one side ever runs.

Two cautions. `source` naming the package rather than the test directory is what makes an untested module
count as uncovered instead of being invisible. And a coverage percentage measures which lines executed, not
whether anything was asserted — `test-engineer` owns whether the number means anything.

## Test Layout

Both layouts work; match what the project has.

```text
tests/                        # separate tree, most common
    conftest.py
    unit/
    integration/

src/myproject/
    orders.py
    orders_test.py            # beside the code
```

With a `src/` layout, either install the package (`pip install -e .` or the project's equivalent) or set
`pythonpath = ["src"]`. Without one of those, imports fail in a way that looks like a broken test.

## Useful Invocations

| Command                           | Use                                  |
| --------------------------------- | ------------------------------------ |
| `pytest --collect-only`           | What was actually collected          |
| `pytest -rs`                      | Why tests were skipped               |
| `pytest -x`                       | Stop at the first failure            |
| `pytest --lf`                     | Rerun only last-failed               |
| `pytest --ff`                     | Run last-failed first, then the rest |
| `pytest -k "expiry and not slow"` | Select by name expression            |
| `pytest --durations=10`           | The ten slowest tests                |
| `pytest -p no:randomly`           | Disable a plugin for one run         |

`--collect-only` and `-rs` are the two that answer "did my test actually run", which is a different question
from "did it pass".

## Plugins Worth Knowing

Check what the project already has with `pytest --version` before adding any of these.

| Plugin          | Purpose                                                         |
| --------------- | --------------------------------------------------------------- |
| pytest-cov      | Coverage measurement and thresholds                             |
| pytest-xdist    | Parallel execution across processes                             |
| pytest-randomly | Randomizes order, exposing inter-test dependencies              |
| pytest-timeout  | Fails a hanging test instead of blocking the run                |
| pytest-mock     | A `mocker` fixture wrapping `unittest.mock` with automatic undo |
| pytest-subtests | Multiple independently-reported assertions in one test          |

pytest-xdist and pytest-randomly are the pair that surface order dependence: parallel execution breaks
implicit sequencing, and randomization stops a suite from relying on alphabetical luck.
