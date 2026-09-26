# pyproject.toml Reference

Complete configuration reference, for when the shape in `SKILL.md` is not enough.

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
dependencies = []

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
line-length = 120          # a choice, not a standard; ruff's own default is 88
target-version = "py311"   # match requires-python above
src = ["src"]

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "I", "B", "UP"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
docstring-code-format = true

```

`[tool.pytest.ini_options]`, `[tool.coverage.*]` and `[tool.mypy]` are deliberately absent; `SKILL.md` names
the skills that own them.

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

`uv_build` is the simplest backend that covers most projects. Keep `version` static unless the release process
actually needs a VCS-derived version: dynamic versioning makes the built artifact depend on checkout state.

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

### Optional Ruff Rules

Enable additional families deliberately. If adopting `D` for docstrings, set the Google convention and exempt test
docstrings where they add no information. If adopting `S`, allow `S101` in tests; fixture-secret exceptions need
case-specific justification. Add ignores only for enabled rules whose findings have been reviewed.

If adopting `TC`, preserve imports needed by runtime annotation consumers. Pydantic resolves model annotations at runtime;
moving their dependencies under `TYPE_CHECKING` can break model construction. Configure
`runtime-evaluated-base-classes = ["pydantic.BaseModel"]` under `[tool.ruff.lint.flake8-type-checking]` when applicable.
Check other consumers, such as `attrs.resolve_types` and SQLAlchemy models, against the actual API before moving imports.

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

Commit `uv.lock` for reproducible development and CI, including for libraries.
Library consumers resolve the constraints in published package metadata; a repository lock does not constrain them.
Test supported dependency ranges separately from the locked development environment.
See [uv's lockfile guidance](https://docs.astral.sh/uv/concepts/projects/layout/#the-lockfile).

## Shapes by Project Type

**Library.** Minimal runtime dependencies, optional extras for genuinely optional features:

```toml
[project]
dependencies = []

[project.optional-dependencies]
async = ["httpx2"]

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
