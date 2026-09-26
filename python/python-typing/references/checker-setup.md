# Configuring a Type Checker

## Which Checker

| Checker      | Notes                                                                                                   |
| ------------ | ------------------------------------------------------------------------------------------------------- |
| mypy         | The reference implementation, the most configurable, the widest plugin support                          |
| pyright      | Fast, the checker behind Pylance, stricter about some inference by default                              |
| basedpyright | A pyright fork with stricter defaults, configured in `[tool.basedpyright]`; common as a language server |
| ty           | Astral's checker, very fast, pre-1.0; check its current version and status before adopting it in a gate |

Use whichever the project already uses. Two checkers in one project means two sets of suppressions and two
sets of disagreements, so adopt a second one only deliberately.

## mypy

```toml
[tool.mypy]
python_version = "3.12"   # set to the project's own floor
strict = true
warn_unreachable = true
warn_unused_ignores = true
```

`strict = true` is a bundle. Turning it on for a codebase that has never been checked produces thousands of
errors, which is why projects abandon it on day one.

Two settings are worth naming explicitly:

- **`warn_unused_ignores`** reports a `# type: ignore` that no longer suppresses anything, so suppressions get
  removed when the underlying problem is fixed rather than accumulating forever. `strict` already enables it;
  list it anyway so it stays on if `strict` is later dropped.
- **`warn_unreachable`** flags code the checker proves cannot run, which is usually a narrowing bug or a
  condition that is always false. `strict` does not enable it.

### Adopting Strict Gradually

Start strict globally and exempt what does not pass yet, rather than starting lenient and never tightening:

```toml
[tool.mypy]
python_version = "3.12"   # set to the project's own floor
strict = true

[[tool.mypy.overrides]]
module = "myproject.legacy.*"
ignore_errors = true
```

The exemption list is then a visible, shrinking backlog. Global leniency has no such list, so nothing ever
tightens.

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
pythonVersion = "3.12"    # set to the project's own floor
typeCheckingMode = "strict"
include = ["src"]
```

Modes are `off`, `basic`, `standard` and `strict`. For gradual adoption, set a lenient mode globally and list
the paths that already pass in the `strict` array. Per-directory rule overrides use `executionEnvironments`,
and `reportMissingTypeStubs`, an error only in strict mode, is the setting that most often needs relaxing early.

pyright understands some inference that mypy does not, and vice versa. Code that passes one is not guaranteed
to pass the other.

### Import Roots

pyright and basedpyright resolve imports from the project root and the installed environment, and fail quietly
on anything else. Three layouts import from elsewhere: script-style tools that import siblings by bare name,
`src/` packages installed in editable mode, and tests that import `conftest` or a helper from a directory
without `__init__.py`. The CLI reports them as `reportImplicitRelativeImport` and `reportMissingTypeStubs`.
The language server does worse: finding references returns only the defining file and misses every
cross-file use. A project that gates on mypy still runs pyright or basedpyright as its language server, so
configure the roots there too.

Declare each import root the tests and mypy already use, one execution environment per tool:

```toml
[tool.basedpyright]
executionEnvironments = [
    { root = "tools/renderer" },                                   # script-style: siblings by bare name
    { root = "tools/merger", extraPaths = ["tools/merger/tests"] }, # tests dir without __init__.py
    { root = "packages/vault", extraPaths = ["packages/vault/src"] },  # src layout
]
```

Use one environment per tool rather than a global `extraPaths`: two tools that each own a `model.py` would
otherwise resolve `import model` to whichever root comes first. Take the roots from pytest's `pythonpath` and
the mypy invocations rather than guessing them. The configuration is done when both warning rules count zero
across the tree and no other rule's count rose; a rule that rises means an import now resolves to the wrong
module. A language server that has only just started still returns partial references until it finishes
indexing, so retry before blaming the configuration.

## Suppressions

```python
result = legacy_call()  # type: ignore[no-any-return]
```

A bare `# type: ignore` hides every present and future error on that line, including ones introduced later by
an unrelated change.

pyright honours `# type: ignore` by default (`enableTypeIgnoreComments`), but as a blanket suppression that
disregards the bracketed code, so a mypy-coded comment silences every pyright error on its line. pyright's own
form, `# pyright: ignore[reportGeneralTypeIssues]`, names its rule. basedpyright ignores `# type: ignore` in its
default and `recommended` modes but honours it under `typeCheckingMode = "strict"`. A project running two
checkers pays for both conventions, which is another reason to run one.

For a whole file, `# mypy: ignore-errors` at the top is preferable to a per-line sweep — it is one visible
marker rather than fifty invisible ones, and it greps.

## What to Check, and When

Check the source and its tests, with test function signatures annotated too, and exclude the rest of the tree.
Generated code, vendored code, and build output produce errors nobody will act on.

Before adding the checker to a hook or CI step, load `python-project-management`: a file-scoped invocation
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
