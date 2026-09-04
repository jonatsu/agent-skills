# uv Command Reference

Read this for the command that does what you need. uv manages packages, dependencies, virtual environments and
Python versions in one tool, replacing pip, virtualenv, pip-tools, pipx and pyenv.

**Never activate a virtual environment.** `uv run <cmd>` resolves and executes in the project environment,
which is what makes the same command work for a developer, a hook and CI.

## Projects

| Command                    | Effect                                                     |
| -------------------------- | ---------------------------------------------------------- |
| `uv init <name>`           | New application project                                    |
| `uv init --package <name>` | New distributable package with a `src/` layout             |
| `uv init --lib <name>`     | New library package                                        |
| `uv init --bare`           | `pyproject.toml` only, for adopting uv in an existing tree |
| `uv init --script file.py` | New single file with PEP 723 metadata                      |

## Dependencies

| Command                            | Effect                                       |
| ---------------------------------- | -------------------------------------------- |
| `uv add <pkg>`                     | Add a runtime dependency and update the lock |
| `uv add --group dev <pkg>`         | Add to a dependency group                    |
| `uv add --optional postgres <pkg>` | Add to an optional runtime extra             |
| `uv remove <pkg>`                  | Remove a dependency and update the lock      |
| `uv lock`                          | Re-resolve the lock without installing       |
| `uv lock --check`                  | Fail if the lock is stale, for CI            |

## Environments

uv creates and manages the environment. Do not create one by hand.

| Command                | Effect                                                 |
| ---------------------- | ------------------------------------------------------ |
| `uv sync`              | Install what the lock describes, plus `default-groups` |
| `uv sync --all-groups` | Install every dependency group                         |
| `uv sync --group test` | Install one named group                                |
| `uv sync --frozen`     | Install from the lock without re-resolving             |

`--frozen` is the CI form: it fails rather than silently resolving something new.

## Running

| Command                      | Effect                                       |
| ---------------------------- | -------------------------------------------- |
| `uv run <cmd>`               | Run in the project environment               |
| `uv run --with <pkg> <cmd>`  | Run with an extra package not in the project |
| `uv run --python 3.11 <cmd>` | Run under a specific interpreter             |

`--with` is for one-off use: trying a library, a throwaway script, a tool that is not a project dependency.
`uv add` is for anything the project actually needs.

```bash
uv run --with httpx python -c "import httpx; print(httpx.get('https://example.com').status_code)"
uv run --with pytest-randomly pytest      # try a plugin without adopting it
```

## Tools

Run or install a tool without adding it to the project:

```bash
uvx ruff check .              # shorthand for `uv tool run`
uv tool install ruff
uv tool list
uv tool upgrade ruff
```

## Python Versions

```bash
uv python install 3.12
uv python list
uv python pin 3.12            # writes .python-version
```

## Scripts

```bash
uv init --script myscript.py
uv add --script myscript.py httpx
uv remove --script myscript.py httpx
uv lock --script myscript.py   # writes myscript.py.lock
uv run myscript.py
```

See [pep723-scripts.md](pep723-scripts.md) for the inline metadata format.

## Building and Publishing

| Command                     | Effect                             |
| --------------------------- | ---------------------------------- |
| `uv build`                  | Build wheel and sdist into `dist/` |
| `uv build --wheel`          | Wheel only                         |
| `uv publish`                | Upload to PyPI                     |
| `uv publish --token $TOKEN` | Upload with an API token           |

Release sequencing is in [dependency-maintenance.md](dependency-maintenance.md).

## Environment Variables

| Variable                 | Effect                                  |
| ------------------------ | --------------------------------------- |
| `UV_CACHE_DIR`           | Cache location                          |
| `UV_NO_CACHE`            | Disable caching                         |
| `UV_PYTHON`              | Default interpreter                     |
| `UV_PROJECT_ENVIRONMENT` | Use a non-default environment directory |
| `UV_SYSTEM_PYTHON`       | Use the system interpreter              |

`UV_PROJECT_ENVIRONMENT` solves one specific problem: developing on a host while also building in a
container. Point the host at `.venv-dev` and the container keeps `.venv`, so switching context does not
rebuild an environment for a different OS or interpreter. Ignore both paths in git.

## Common Workflows

```bash
# New application
uv init myapp && cd myapp
uv add fastapi uvicorn
uv add --group dev ruff mypy pytest
uv sync --all-groups

# Adopt uv in an existing project
uv init --bare
uv add httpx rich
uv add --group dev ruff mypy

# Reproducible CI install
uv sync --frozen --all-groups
```

## Notes

- uv caches aggressively; the first resolve of a dependency set is the slow one.
- `uv cache clean` when the cache grows past what you want to keep.
- A nonzero exit from `uv sync --frozen` in CI usually means someone edited `pyproject.toml` without running
  `uv add`, so the lock no longer matches.
