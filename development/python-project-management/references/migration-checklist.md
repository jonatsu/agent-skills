# Migration Checklist

Read this when the user has asked to move an existing project onto uv and ruff. Do not start a migration that
was not requested.

## Before Touching Anything

- [ ] Commit or branch first, so the migration is one reviewable diff and is trivially abandonable.
- [ ] Decide the layout: `src/` or flat. A flat layout needs `[tool.uv.build-backend] module-root = ""`.
- [ ] Decide the lock policy: an application commits `uv.lock`, a library usually ignores it. A library that
  ignores it cannot use `uv sync --locked` or `uv lock --check` in CI, so choose the pair together.
- [ ] Record the current interpreter floor. `requires-python` has to match what the code already assumes.

## Bring Dependencies Across

```bash
uv init --bare                      # pyproject.toml only, no layout changes
uv add httpx rich                   # runtime dependencies, one reviewed batch
uv add --group dev ruff mypy
uv add --group test pytest pytest-cov
uv sync --all-groups
```

**Review each line of `requirements.txt` rather than piping it into `uv add`.** A requirements file can carry
an editable install, a VCS URL, a hash pin, an environment marker, or a constraint that no longer resolves.
Each of those needs a decision, and a loop makes all of them silently.

For a `setup.py` or `setup.cfg` project, `install_requires` becomes `dependencies`, the extras become
`[project.optional-dependencies]`, the development extras become `[dependency-groups]`, and the remaining
metadata moves into `[project]` unchanged.

## Replace the Linters

```bash
uv remove --group dev flake8 black isort   # name the group they live in; a bare remove fails
uv add --group dev ruff
uv run ruff check --fix .
uv run ruff format .
```

Then delete the configuration they left behind: `.flake8`, `setup.cfg` lint sections, and the `[tool.black]`,
`[tool.isort]`, `[tool.pylint]` and `[tool.flake8]` tables.

Expect the first `ruff format` to touch nearly every file. Land it as its own commit so the behavioral diff
that follows stays readable, and add that commit to `.git-blame-ignore-revs`.

## Files to Delete

- [ ] `requirements.txt`, `requirements-dev.txt`, `constraints.txt`
- [ ] `setup.py`, `setup.cfg`, `MANIFEST.in`
- [ ] `Pipfile`, `Pipfile.lock`, `poetry.lock`
- [ ] `.flake8`, and `mypy.ini` or `pyrightconfig.json` only if that checker is actually being replaced
- [ ] `tox.ini`, unless it still drives a matrix that CI does not
- [ ] Old environments: `venv/`, `.venv/`, `env/`

## `.gitignore`

```gitignore
__pycache__/
*.py[cod]
.venv/
.ruff_cache/
.mypy_cache/
.pytest_cache/

# Libraries ignore the lock; applications commit it
# uv.lock
```

## Automatic Modernization

Each of these is mechanical and reviewable on its own:

```bash
uv run ruff check --select=UP --fix .       # modern syntax and typing forms
uv run ruff check --select=SIM --fix .      # simplifiable conditionals and comprehensions
uv run ruff check --select=RET504 --fix .   # pointless assignment before return
uv run ruff check --select=ERA .            # commented-out code, review before deleting
```

Run `ERA` without `--fix` first. Commented-out code is sometimes a note rather than dead weight.

Find what the old linters left behind:

```bash
rg "# pylint:|# noqa:|# type: ignore" --files-with-matches
uv run ruff check --select=INP001 .          # packages missing __init__.py
```

A `# noqa:` with no code after it suppresses everything on that line and should be narrowed or removed.

## Adopting a Type Checker Gradually

A legacy codebase will not pass `--strict` on day one, and blocking the migration on that guarantees the
migration stalls. Start where it passes and tighten per module.

```toml
[tool.mypy]
python_version = "3.11"   # set to the project's own floor
warn_unused_ignores = true

[[tool.mypy.overrides]]
module = "myproject.legacy.*"
ignore_errors = true
```

Remove overrides as modules are cleaned. `python-typing` owns the strictness ladder and the per-module
progression; this is only the migration entry point.

## CI

- [ ] Replace `pip install` steps with `uv sync --locked --all-groups`.
- [ ] Run tools through `uv run` so local and CI invoke the same thing.
- [ ] Pin actions to commit SHAs, if the project uses GitHub Actions. Adapt these to whatever CI it runs.
- [ ] Add `uv lock --check`.
- [ ] Drop scheduled triggers that no one reads.

## Verify

```bash
uv sync --all-groups
uv run ruff format --check .
uv run ruff check .
uv run mypy src/          # use the project's own package path
uv run pytest
uv run pip-audit
uv build          # only if the project is distributed
```

The migration is done when this sequence passes from a clean checkout, not when the files are deleted.
