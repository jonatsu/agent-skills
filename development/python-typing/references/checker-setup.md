# Configuring a Type Checker

Read this before turning on strict mode anywhere that already has code, or when setting up a checker in a
project that has none.

## Which Checker

| Checker | Notes                                                                                                                           |
| ------- | ------------------------------------------------------------------------------------------------------------------------------- |
| mypy    | The reference implementation, the most configurable, the widest plugin support                                                  |
| pyright | Fast, the checker behind Pylance, stricter about some inference by default                                                      |
| ty      | Astral's checker, very fast, pre-1.0 at the time of writing — check its current version and status before adopting it in a gate |

Use whichever the project already uses. Two checkers in one project means two sets of suppressions and two
sets of disagreements, so adopt a second one only deliberately.

## mypy

```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_unreachable = true
warn_unused_ignores = true
```

`strict = true` is a bundle. Turning it on for a codebase that has never been checked produces thousands of
errors, which is why projects abandon it on day one.

Two settings are worth naming even inside `strict`:

- **`warn_unused_ignores`** reports a `# type: ignore` that no longer suppresses anything, so suppressions get
  removed when the underlying problem is fixed rather than accumulating forever.
- **`warn_unreachable`** flags code the checker proves cannot run, which is usually a narrowing bug or a
  condition that is always false.

### Adopting Strict Gradually

Start strict globally and exempt what does not pass yet, rather than starting lenient and never tightening:

```toml
[tool.mypy]
python_version = "3.12"
strict = true

[[tool.mypy.overrides]]
module = "myproject.legacy.*"
ignore_errors = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

The exemption list is then a visible, shrinking backlog. The alternative — global leniency — has no such list,
and nothing ever tightens.

Relaxing annotations in tests is a common and reasonable choice: test functions take fixtures and return
`None`, so requiring annotations adds noise without catching anything.

### Third-Party Libraries Without Types

```toml
[[tool.mypy.overrides]]
module = ["untyped_dependency.*"]
ignore_missing_imports = true
```

Before reaching for that, check for a stub package: many libraries have `types-<name>` on PyPI, and installing
it gives real checking instead of silence. `mypy --install-types` offers to install the ones it detects.

Keep `ignore_missing_imports` scoped to named modules. Setting it globally silences a genuine typo in an import
as readily as a missing stub.

### Useful Invocations

```bash
mypy src/                       # check a path
mypy --strict path/to/file.py   # one file, maximum strictness
mypy --warn-unused-ignores src/ # find stale suppressions
```

## pyright

```toml
[tool.pyright]
pythonVersion = "3.12"
typeCheckingMode = "strict"
include = ["src"]
```

Modes are `off`, `basic`, `standard` and `strict`. Per-directory overrides use `executionEnvironments`, and
`reportMissingTypeStubs` is the setting that most often needs relaxing early.

pyright understands some inference that mypy does not, and vice versa. Code that passes one is not guaranteed
to pass the other.

## Suppressions

```python
result = legacy_call()  # type: ignore[no-any-return]
```

Always name the error code. A bare `# type: ignore` hides every present and future error on that line,
including ones introduced later by an unrelated change.

pyright's equivalent is `# pyright: ignore[reportGeneralTypeIssues]`, and it ignores mypy's comments. A project
running both needs both forms, which is another reason to run one.

For a whole file, `# mypy: ignore-errors` at the top is preferable to a per-line sweep — it is one visible
marker rather than fifty invisible ones, and it greps.

## What to Check, and When

Check `src/`, not the whole tree. Checking generated code, vendored code and build output produces errors
nobody will act on.

Where the checker runs is a per-project decision. Look at what the project already does before adding it
anywhere; `python-project-management` covers wiring it into gates, including why a file-scoped invocation
sees a different program than a full run.

## Debugging a Disagreement

```python
reveal_type(value)          # checker prints the inferred type; no import needed
reveal_locals()             # mypy: every local in scope
```

`reveal_type` is the single most useful tool here. When a call is rejected and the code looks right, print
what the checker actually thinks each side is; the mismatch is usually one level down from where the error
appears.

Then, in order:

1. Is the annotation on the **declaration** or only inferred? Annotate the declaration.
2. Is a narrowing check invisible to the checker? See the narrowing section in `SKILL.md`.
3. Is an untyped dependency returning `Any` that spreads? Convert at the boundary.
4. Is it a variance problem? See [generics.md](generics.md).
5. Is it a genuine checker limitation? Then a coded `# type: ignore` with a comment is the right answer.

Reach for step 5 last. Most disagreements are the checker being right about something subtle.
