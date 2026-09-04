---
name: python-project-management
description: Set up and maintain a Python project with uv, ruff, and mypy. Use when creating a project or standalone script, configuring pyproject.toml, wiring pre-commit and CI security checks, updating or auditing dependencies, cutting a release, or migrating off pip, Poetry, setup.py, black, flake8, or isort.
license: CC-BY-SA-4.0
compatibility: Requires uv. Python 3.11+ for the recommended configuration. Optional tools named in references are installed on demand and reported when absent.
metadata:
  author: Joonas Onatsu
---

# Python Project Management

Set up a Python project once, then keep it current. This skill owns the project's tooling and its lifecycle:
`pyproject.toml`, dependency management with uv, lint and format configuration, pre-commit and CI wiring,
dependency updates and audits, version bumps, and migration off legacy tooling.

It does not own test authoring or test configuration, which is `python-testing`, nor type-checker usage, which
is `python-typing`. Both are named where the boundary matters below.

**Respect an existing project's choices.** When a repository already declares its tooling, its configuration
wins over every default here. Recommend a change, explain what it buys, and let the user decide. Migrate only
when asked.

## Decide What You Are Setting Up

| Situation                                | Do this                                                                               |
| ---------------------------------------- | ------------------------------------------------------------------------------------- |
| Single file with dependencies            | PEP 723 inline metadata, [pep723-scripts.md](references/pep723-scripts.md)            |
| Multi-file project, not distributed      | `uv init`, then the minimal setup below                                               |
| Reusable package or library              | `uv init --package`, then [pyproject-reference.md](references/pyproject-reference.md) |
| Existing project on legacy tooling       | [migration-checklist.md](references/migration-checklist.md)                           |
| Project that already works, needs upkeep | [dependency-maintenance.md](references/dependency-maintenance.md)                     |

## The Tools and What They Replace

| Tool       | Purpose                                                       | Replaces                                        |
| ---------- | ------------------------------------------------------------- | ----------------------------------------------- |
| uv         | Packages, dependencies, virtual environments, Python versions | pip, virtualenv, pip-tools, pipx, pyenv, Poetry |
| ruff       | Linting and formatting                                        | flake8, black, isort, pyupgrade, pydocstyle     |
| mypy       | Type checking                                                 | —                                               |
| pytest     | Testing                                                       | unittest                                        |
| pre-commit | Git hook runner                                               | —                                               |

**Two of these have faster rivals worth knowing but not defaulting to.** `ty` is Astral's type checker and is
much faster than mypy; as of 2026-09-04 it is version 0.0.78 and classified Beta on PyPI, so choose it only
when a project accepts a pre-1.0 dependency in its gate. `prek` is a Rust reimplementation of pre-commit that
needs no Python runtime; choose it when hook startup time actually hurts. Both are drop-in enough to swap
later. Default to mypy and pre-commit, and say why when you propose either alternative.

## Always Use uv to Change Dependencies

`uv add` and `uv remove` edit `pyproject.toml` and update `uv.lock` together. Editing the `dependencies` or
`dependency-groups` tables by hand leaves the lock stale, and the next `uv sync` either overwrites the edit or
installs something the file does not describe.

Never activate a virtual environment. `uv run <cmd>` resolves and runs in the project environment, which is
also what makes a command reproducible in CI and in a hook.

```bash
uv add httpx                      # runtime dependency
uv add --group dev ruff mypy      # development dependency group
uv remove httpx
uv sync --all-groups              # install everything the lock describes
uv run pytest                     # run inside the project environment
```

Full command reference: [uv-commands.md](references/uv-commands.md).

## Minimal Project

For a multi-file project that will not be distributed:

```bash
uv init myproject
cd myproject
uv add --group dev ruff mypy pytest
uv sync --all-groups
uv run ruff check .
```

## Full Project

For a package or library, add the configuration that makes the project checkable and buildable.

```bash
uv init --package myproject
cd myproject
uv add --group dev ruff mypy
uv add --group test pytest pytest-cov
uv sync --all-groups
```

Then write the configuration. The essential shape:

```toml
[project]
name = "myproject"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []

[build-system]
requires = ["uv_build>=0.9,<1"]
build-backend = "uv_build"

[dependency-groups]
dev = [{ include-group = "lint" }, { include-group = "test" }, { include-group = "audit" }]
lint = ["ruff", "mypy"]
test = ["pytest", "pytest-cov"]
audit = ["pip-audit"]

[tool.uv]
default-groups = ["dev"]

[tool.ruff]
line-length = 100          # a choice, not a standard; ruff's own default is 88
target-version = "py311"   # match requires-python above
src = ["src"]

[tool.ruff.lint]
select = ["ALL"]
ignore = ["D", "COM812", "ISC001"]
```

`[dependency-groups]` is PEP 735 and is not installed by consumers of the package.
`[project.optional-dependencies]` is for optional *runtime* features a user opts into, and is the wrong place
for development tools.

Complete configuration reference, including per-file ignores, coverage, and the flat-layout build root:
[pyproject-reference.md](references/pyproject-reference.md).

**Test configuration belongs to `python-testing`.** Put `[tool.pytest.ini_options]` and `[tool.coverage.*]`
there rather than deciding them here; this skill only names the `test` dependency group. **Type-checker
configuration belongs to `python-typing`** for the same reason.

## Ruff Owns the Style Rules

`select = ["ALL"]` with a short, explained ignore list is the recommended starting point: it opts into every
rule ruff ships and forces each exclusion to be deliberate. Three exclusions are near-universal.

| Ignored  | Why                                                                           |
| -------- | ----------------------------------------------------------------------------- |
| `D`      | pydocstyle. Enable selectively once the project agrees a docstring convention |
| `COM812` | Trailing comma rule that fights the formatter                                 |
| `ISC001` | Implicit string concatenation rule that fights the formatter                  |

Tests need their own relaxations, `S101` for `assert` and `PLR2004` for magic values among them. The
per-file-ignores block is in [pyproject-reference.md](references/pyproject-reference.md).

Configuring ruff is how this project's style preferences get enforced at the moment code is written. Anything
ruff can decide belongs in this configuration rather than in prose an agent has to remember.

## Wire the Gates

These are the project's checks, and each is an ordinary command a developer can run at any time:

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy src/          # use the project's own package path
uv run pytest
uv run pip-audit
```

**Check how the project already runs each one before invoking or configuring it.** Look at
`.pre-commit-config.yaml`, the CI workflows, and any `justfile`, `Makefile` or `tox.ini`. A tool may be a
hook, a CI step, a task-runner recipe, an on-demand command, or several of those. Match what is there.

Hook configuration, secret scanning, workflow auditing, and the CI shape are in
[security-setup.md](references/security-setup.md).

## Keep It Current

Setup is the smaller half. Dependency updates, lock refreshes, vulnerability audits, version bumps, and
publishing are in [dependency-maintenance.md](references/dependency-maintenance.md). Read it when the project
already exists and the request is about keeping it healthy rather than starting it.

## Migrating Off Legacy Tooling

Only when the user asks. The order that avoids a broken intermediate state:

1. `uv init --bare` in the existing project to create `pyproject.toml` without touching the source layout.
2. Add each dependency with `uv add`, reviewing rather than bulk-importing. A `requirements.txt` line can
   carry a constraint or an editable install that does not translate.
3. Move development tools to `uv add --group dev`.
4. Copy non-dependency metadata into `[project]`.
5. Replace flake8, black and isort with ruff, then run `uv run ruff check --fix .` and `uv run ruff format .`.
6. Delete the superseded files and configuration tables.
7. Verify: sync, lint, type-check, test, audit, and build.

Step-by-step cleanup, the artifacts to delete, the `.gitignore` additions, and the automatic modernization
passes are in [migration-checklist.md](references/migration-checklist.md).

## Before Calling Setup Done

1. Does `uv sync --all-groups` succeed from a clean checkout?
2. Do lint, format-check, type-check and tests all run through `uv run`?
3. Is `uv.lock` committed for an application, and ignored for a library?
4. Does `requires-python` match what ruff and the type checker target?
5. Does the project build, if it is meant to be distributed?
