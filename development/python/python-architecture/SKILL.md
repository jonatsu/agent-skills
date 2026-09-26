---
name: python-architecture
description: Decide where Python code lives and what may depend on what. Use when starting a project, adding or splitting a module or package, moving code between modules, resolving a circular import, choosing between src and flat layout, deciding what an __init__.py should do, placing tests, adding a console entry point, or reviewing project structure.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Python Architecture

Where code lives, and what may depend on what. How the code inside a module is written belongs to the other
Python skills: `python-style` for everyday code, `python-typing` for annotations, `python-error-handling` for
validation and failure, `python-testing` for the tests themselves. Project tooling and `pyproject.toml`
belong to `python-project-management`; this skill owns only the layout decisions that tooling then has to
match.

## Respect Project Conventions

Use these defaults for new projects. In established projects, follow declared conventions and consistent local practice,
including for new files and modules. Check both before filling an undecided choice.

Do not recommend changes merely because these defaults differ. Recommend corrections supported by incorrect behavior,
security vulnerabilities, or concrete reliability or maintenance harm. Explain the evidence, consequence, and smallest
remedy. A different tool, layout, style, or supported syntax is not itself a defect.

Apply fixes within the authorized task; otherwise report the recommendation without changing the project.
An explicit modernization or conventions review permits broader recommendations.

## Prefer a src Layout for New Installed Packages

```text
project/
├── src/
│   └── mypkg/
│       ├── __init__.py
│       └── ...
├── tests/
├── pyproject.toml
└── README.md
```

In this layout, `src/` is the import root and `mypkg/` is the package. Configure the build backend to match it.

The reason is not tidiness. Under a flat layout the package directory sits in the working directory, so
`import mypkg` resolves to the working copy rather than the installed one — and a test suite can pass against
code that was never installed, hiding a missing module in the packaged artifact until someone else installs it.
A src layout avoids that accidental root import under normal path settings. Test an installed artifact to verify
packaging; editable-install tests alone cannot establish that the wheel contains the required files.

A flat layout is also valid for installed projects. Preserve it when established, and check the built artifact in an
isolated environment outside the checkout. Missing packaged files or unintended import resolution are defects;
the layout itself is a convention.

Keep the repository root to files that describe or configure the project. Group code into directories rather
than letting modules accumulate at the top level.

## Name Packages for What They Own

Name a package for the capability it owns — `billing`, `recognition` — not for the kind of thing inside it.
`helpers`, `utils`, `models`, and `common` describe a filing decision rather than a responsibility, so they
attract anything that does not obviously belong elsewhere and stop being searchable once they do.

Split a package into subpackages when its modules form groups that do not reference each other, and give each
subpackage more than one module.

## Keep Dependencies Acyclic

Point dependencies one direction, so a new design has no direct or transitive import cycle.

When an import cycle causes a failure or its repair is authorized, work through these in order:

1. **Is it only an annotation cycle?** Add `from __future__ import annotations` and move the import under
   `if TYPE_CHECKING:` when runtime consumers do not need the annotation's name. Check model validation and reflection
   before moving imports; postponed annotations alone do not make runtime dependencies optional.
2. **Is there a shared piece?** Hoist it up the tree into a module both may depend on.
3. **Is one side substitutable?** Declare the seam as a `Protocol` and inject the implementation, so the caller
   never imports the default one.

A function-local import runs at call time, so it hides a cycle only while nothing calls the function during
either module's initialization; a call at import time still fails with
`cannot import name ... from partially initialized module`. Use it deliberately for optional dependencies,
startup cost, or a documented import-order constraint. When a cycle causes failures or concrete maintenance
harm, recommend the smallest repair and test the relevant import and call order.

## Give `__init__.py` a Job or Leave It Empty

The legitimate jobs are re-exporting the package's public names, package initialization, and selecting a
platform-specific implementation.

- A re-exporting `__init__.py` defines the package's public surface. List it in `__all__` and keep it stable,
  because callers will import from it rather than from the module behind it.
- Re-export downward only. A subpackage that imports its parent is a cycle waiting for an import-order change.
- Keep work that can fail in a function the caller invokes. `__init__.py` runs on every import, including the
  one a test does to check something unrelated, so a failure there takes out things that never used it.

## Place Tests Outside the Package

Put tests in a top-level `tests/` directory that loosely mirrors the package. This keeps them out of the
distribution and lets them run against the installed package rather than a path that happens to resolve.

Mirror module names — `tests/test_recognition.py` for `mypkg/recognition.py` — so a reader finds a module's
tests without searching.

Tests inside the package, run with `pytest --pyargs mypkg`, are the alternative when the tests ship
deliberately. Choose one and apply it consistently; a project with both has two answers to where a new test
goes.

`python-testing` owns the pytest side of this layout: `--import-mode=importlib`, `pythonpath` for a `src/`
layout, and where shared fixtures go in `conftest.py`.

## Keep Entry Points Thin

Declare console scripts in `[project.scripts]`, pointing at a function rather than a module-level side effect.
Add `__main__.py` when the package should also run as `python -m mypkg`, and have it call the same function the
console script does.

The command-line layer parses and validates arguments, then calls into the package. Keep reusable logic separate from
command parsing and process exit behavior so callers and tests can invoke it directly.

For complex internal algorithms, expose a focused internal module interface when that improves cohesion and testing.
Keep public API for real callers; whether to test an underscore-prefixed helper directly is `python-testing`'s choice.

## Layer an Application, and Point Dependencies One Way

For an application rather than a library, name the layers and let dependencies point inward:

- **Boundary** code talks to the outside world — the CLI, HTTP handlers, database and service clients. It
  depends on the core.
- **Core** code holds the domain model and the decisions. It depends on nothing outside itself and on no
  framework.

A layer may not import from a layer above it, and no layer may reach around the layer below it to touch an
external system directly. Where a boundary needs a type that describes the contract, the type belongs in the
core, not in the layer that happens to use it first.

Record the intended layering in the repository's own documentation, and treat an import that violates it as a
defect rather than a shortcut. The interpreter and the type checker both accept such an import, so only a
review or an import-contract tool such as `import-linter`'s `layers` contract will catch it.

## Before Calling Structural Work Done

1. Does the built package import and work in an isolated environment outside the checkout?
2. Do new or moved modules respect intended dependencies, with deferred imports verified where relevant?
3. Does each `__init__.py` have one of the three jobs, or nothing at all?
4. Can a reader find a module's tests from the module's name?

## Reference

- [src layout vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) —
  Python Packaging User Guide
- [Good integration practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html) — pytest
