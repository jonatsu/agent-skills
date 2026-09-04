# pyproject.toml Reference

Complete configuration reference. Read this when the shape in `SKILL.md` is not enough: optional runtime
extras, entry points, per-file lint ignores, coverage, or a flat layout.

**Change dependencies with `uv add` and `uv remove`, never by editing the tables directly.** A hand-edited
`dependencies` or `dependency-groups` list leaves `uv.lock` stale.

## Complete Example

```toml
[project]
name = "myproject"
version = "0.1.0"
description = "A modern Python project"
readme = "README.md"
license = "MIT"
requires-python = ">=3.11"
authors = [{ name = "Your Name", email = "you@example.com" }]
classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]
dependencies = ["httpx", "rich"]

[project.optional-dependencies]
postgres = ["psycopg[binary]"]

[project.scripts]
myproject = "myproject.cli:main"

[project.urls]
Homepage = "https://github.com/org/myproject"
Repository = "https://github.com/org/myproject"

[build-system]
requires = ["uv_build>=0.9,<1"]
build-backend = "uv_build"

[dependency-groups]
dev = [{ include-group = "lint" }, { include-group = "test" }, { include-group = "audit" }]
lint = ["ruff", "mypy"]
test = ["pytest", "pytest-cov"]
audit = ["pip-audit"]
docs = ["sphinx", "myst-parser"]

[tool.uv]
default-groups = ["dev"]

[tool.ruff]
line-length = 100
target-version = "py311"
src = ["src"]

[tool.ruff.lint]
select = ["ALL"]
ignore = [
    "D",       # pydocstyle; enable selectively
    "COM812",  # trailing comma, conflicts with the formatter
    "ISC001",  # implicit string concat, conflicts with the formatter
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = [
    "S101",     # assert is the point of a test
    "PLR2004",  # magic values are readable in a test
    "ANN",      # annotations optional in tests
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
docstring-code-format = true

[tool.coverage.run]
branch = true
source = ["src/myproject"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
]
```

`[tool.pytest.ini_options]` is deliberately absent: `python-testing` owns it, along with the rest of the
coverage decisions. `[tool.mypy]` is absent for the same reason and belongs to `python-typing`.

## Section Notes

### `[project]`

PEP 621 metadata. `name` and `version` are required. `requires-python` is not required but should always be
set, because it is what ruff, the type checker and uv all read to decide which syntax and which resolution
apply.

### `[project.optional-dependencies]` versus `[dependency-groups]`

|                                   | Installed by a consumer               | Use for                                      |
| --------------------------------- | ------------------------------------- | -------------------------------------------- |
| `[project.optional-dependencies]` | Yes, via `uv add myproject[postgres]` | Optional runtime features                    |
| `[dependency-groups]`             | No                                    | Development, test, lint, audit, docs tooling |

Putting development tools in optional-dependencies publishes them in the package metadata, where consumers
see them and resolvers may consider them.

### `[build-system]`

`uv_build` is the simplest backend that covers most projects. Prefer a static `version` over VCS-derived
dynamic versioning unless the release process actually needs it.

```toml
[build-system]
requires = ["uv_build>=0.9,<1"]
build-backend = "uv_build"
```

For a flat layout with no `src/` directory, name the module root:

```toml
[tool.uv.build-backend]
module-root = ""
```

These backends move quickly. Prefer a `>=X.Y,<X+1` constraint so patch and minor releases arrive without an
edit.

### `[tool.uv]`

```toml
[tool.uv]
default-groups = ["dev"]   # what a bare `uv sync` installs
python-preference = "managed"
```

## Version Specifiers

| Specifier    | Meaning                          |
| ------------ | -------------------------------- |
| `>=1.0`      | At least 1.0                     |
| `>=1.0,<2.0` | 1.x only                         |
| `~=1.4`      | Compatible release: `>=1.4,<2.0` |
| `==1.4.*`    | Any 1.4 patch                    |

## Committing `uv.lock`

| Project type           | `uv.lock` in git | Why                                                |
| ---------------------- | ---------------- | -------------------------------------------------- |
| Application or service | Commit           | Reproducible deploys and CI                        |
| Library                | Ignore           | Consumers resolve against their own constraint set |

## Shapes by Project Type

**Library.** Minimal runtime dependencies, optional extras for genuinely optional features:

```toml
[project]
dependencies = []

[project.optional-dependencies]
async = ["httpx"]

[dependency-groups]
dev = ["ruff", "mypy"]
test = ["pytest", "pytest-cov"]
```

**Application.** Pinned through the committed lock, with an entry point:

```toml
[project]
dependencies = ["fastapi", "uvicorn", "sqlalchemy"]

[project.scripts]
myapp = "myapp.main:run"
```

**CLI tool.** The entry point is the product:

```toml
[project]
dependencies = ["typer", "rich"]

[project.scripts]
mytool = "mytool.cli:app"
```
