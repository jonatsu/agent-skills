---
name: python-project-management
description: Set up and maintain a Python project's tooling with uv and ruff, wiring mypy and pytest into CI. Use when creating a project or standalone script, configuring pyproject.toml, wiring pre-commit and CI security checks, updating or auditing dependencies, cutting a release, or migrating off pip, Poetry, setup.py, black, flake8, or isort.
license: CC-BY-SA-4.0
compatibility: Requires uv. Python 3.11+ for the recommended configuration. Optional tools named in references are installed on demand and reported when absent.
metadata:
  author: Joonas Onatsu
---

# Python Project Management

Set up a Python project once, then keep it current. This skill owns the project's tooling and its lifecycle:
`pyproject.toml`, dependency management with uv, lint and format configuration, pre-commit and CI wiring,
dependency updates and audits, version bumps, and migration off legacy tooling.

Test authoring and test configuration, including `[tool.pytest.ini_options]` and `[tool.coverage.*]`, belong
to `python-testing`. Type-checker usage and `[tool.mypy]` belong to `python-typing`. This skill names only the
dependency groups and the commands that run them.

## Respect Project Conventions

Use these defaults for new projects. In established projects, follow declared conventions and consistent local practice,
including for new files and modules. Check both before filling an undecided choice.

Recommend a correction only when it is supported by incorrect behavior, a security vulnerability, or concrete
reliability or maintenance harm; a different tool, layout, style, or supported syntax is a preference, not a
defect. Explain the evidence, consequence, and smallest remedy.

Apply fixes within the authorized task; otherwise report the recommendation without changing the project.
An explicit modernization or conventions review permits broader recommendations.

## Decide What You Are Setting Up

| Situation                                | Do this                                                                               |
| ---------------------------------------- | ------------------------------------------------------------------------------------- |
| Single file with dependencies            | PEP 723 inline metadata, [pep723-scripts.md](references/pep723-scripts.md)            |
| Multi-file project, not distributed      | `uv init`, then the minimal setup below                                               |
| Reusable package or library              | `uv init --package`, then [pyproject-reference.md](references/pyproject-reference.md) |
| Authorized tooling migration             | [migration-checklist.md](references/migration-checklist.md)                           |
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

## Choose Defaults for a New Project

Use the latest stable CPython supported by the target environment and required dependencies.
Choose the supported Python floor deliberately; the examples' version numbers are placeholders for that decision.
Use the tools in the table above, with pytest for new test suites and pip-audit before deployment.
Prefer `uv_build` for distributable pure-Python packages; use a compatible backend for specialized builds.

Add runtime libraries only for capabilities the project needs. For new HTTP-client use, prefer Pydantic's `httpx2`
as both dependency and import. Verify its current API and required integrations before adopting it.
For a CLI that benefits from a framework, prefer Typer; small dependency-free CLIs can use `argparse`.
Logging and value-type defaults belong to `python-style`; validation library choices belong to
`python-error-handling`; entry-point structure belongs to `python-architecture`.

## Change Dependencies in a uv Project

Prefer `uv add` and `uv remove`: they update project metadata and the lock together.
Deliberate metadata edits are valid; follow them with `uv lock` and verify the resulting resolution.
`uv sync` normally updates an outdated lock from project metadata. Use `--locked` in CI to reject drift.
Change `uv.lock` only through uv commands; never edit it by hand. Choose version constraints for compatibility
rather than requiring exact pins universally.

Run commands the way the project already does: its task runner, an activated environment, or `uv run`.
Dependency-free scripts can use an interpreter directly. These commands apply to uv projects; a project on
another manager moves to uv only through an authorized migration.

```bash
uv add httpx2                     # when an HTTP client is needed
uv add --group dev ruff mypy      # development dependency group
uv remove httpx2
uv sync --all-groups              # install everything the lock describes
uv run pytest                     # run inside the project environment
```

Read [uv-commands.md](references/uv-commands.md) for a uv command not shown here, the `--locked` versus
`--frozen` difference, interpreter selection, or uv's environment variables.

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
uv add --group lint ruff mypy
uv add --group test pytest pytest-cov
uv add --group audit pip-audit
```

Then write the rest of the configuration, including the `dev` group that includes the other three, and run
`uv sync --all-groups`. The essential shape:

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
line-length = 120          # a choice, not a standard; ruff's own default is 88
target-version = "py311"   # match requires-python above
src = ["src"]

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "I", "B", "UP"]
```

`[dependency-groups]` is PEP 735 and is not installed by consumers of the package.
`[project.optional-dependencies]` is for optional *runtime* features a user opts into, and is the wrong place
for development tools.

Read [pyproject-reference.md](references/pyproject-reference.md) when the project needs more than this shape:
optional runtime extras, entry points, project URLs, a flat layout, optional Ruff families, or the shape for a
library, application, or CLI.

## Ruff Owns the Style Rules

Start with `E4`, `E7`, `E9`, `F`, `I`, `B`, and `UP` for basic errors, import sorting, bug risks, and supported syntax.
Use four-space indentation and a 120-character line limit when the project has no formatting convention.
Add other rule families only when their findings justify the cost. `ALL` also adopts new rules on upgrades;
[Ruff recommends a small starting set](https://docs.astral.sh/ruff/linter/#rule-selection). Before enabling
`D`, `S`, or `TC`, read the optional-rules section of the configuration reference: each needs an exception.

Fix causes before suppressing findings. When a suppression is justified, name the rule with `# noqa: RULE_CODE`
and explain the non-obvious reason. Keep file-level exceptions narrow and remove obsolete suppressions.

Put anything ruff can decide into its configuration rather than into prose an agent has to remember.

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

Read [security-setup.md](references/security-setup.md) when adding pre-commit hooks, a mypy hook, secret
scanning, workflow auditing, or a CI job.

## Keep It Current

Read [dependency-maintenance.md](references/dependency-maintenance.md) when the project already exists and the
request is about keeping it healthy: lock refreshes, dependency updates, vulnerability audits, version bumps,
or publishing.

## Migrating Off Legacy Tooling

Migrate only when the user asks. Follow [migration-checklist.md](references/migration-checklist.md) in order:
it brings dependencies across before replacing linters and deletes superseded files last, so no intermediate
state is broken. Review each `requirements.txt` line rather than bulk-importing it, because a line can carry a
constraint or an editable install that does not translate.

## Before Calling Setup Done

1. Does `uv sync --all-groups` succeed from a clean checkout?
2. Does every command under Wire the Gates pass, run the way the project runs it?
3. Is `uv.lock` committed for reproducible development and CI, including for a library?
4. Does `requires-python` match what ruff and the type checker target?
5. Does the project build, if it is meant to be distributed?
