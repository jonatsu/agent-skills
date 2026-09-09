---
name: python-architecture
description: Decide where Python code lives and what may depend on what. Use when starting a project, adding or splitting a module or package, moving code between modules, resolving a circular import, choosing between src and flat layout, deciding what an __init__.py should do, placing tests, adding a console entry point, or reviewing project structure.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Python Architecture

Where code lives, and what may depend on what. How the code inside a module is written belongs to the other
Python skills: `python-typing` for annotations, `python-error-handling` for boundaries, `python-testing` for
the tests themselves. Project tooling and `pyproject.toml` belong to `python-project-management`; this skill
owns only the layout decisions that tooling then has to match.

Apply these defaults where the project leaves the choice open. An established layout wins: propose a change and
say what it buys, but do not restructure a working project as a side effect of another task.

## Use a src Layout for Anything Installed

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

The distribution package sits one level below `src/`. `src/` is not itself a package: no `__init__.py`, no
loose modules beside the package.

The reason is not tidiness. Under a flat layout the package directory sits in the working directory, so
`import mypkg` resolves to the working copy rather than the installed one — and a test suite can pass against
code that was never installed, hiding a missing module in the packaged artifact until someone else installs it.
A src layout cannot be imported without installing the project, normally as an editable install, and that
requirement is what makes the suite honest.

A flat layout is fine for a single-file script or a throwaway. It is not fine for anything that will be
installed or imported.

Keep the repository root to files that describe or configure the project. Group code into directories rather
than letting modules accumulate at the top level.

## Name Packages for What They Own

Name a package for the capability it owns — `billing`, `recognition` — not for the kind of thing inside it.
`helpers`, `utils`, `models`, and `common` describe a filing decision rather than a responsibility, so they
attract anything that does not obviously belong elsewhere and stop being searchable once they do.

Split a package into subpackages when its modules form groups that do not reference each other. Do not create a
subpackage for a single module.

## Keep the Dependency Graph a Tree

Dependencies point one direction. No module imports a module that imports it back, directly or transitively.

When a cycle appears, work through these in order:

1. **Is it only an annotation cycle?** Add `from __future__ import annotations` and move the import under
   `if TYPE_CHECKING:`. Check this first — it resolves most cycles a type hint introduces, and hoisting a
   module to fix one is over-treatment.
2. **Is there a shared piece?** Hoist it up the tree into a module both may depend on.
3. **Is one side substitutable?** Declare the seam as a `Protocol` and inject the implementation, so the caller
   never imports the default one.

An import placed inside a function to break a cycle is not a fix. It moves the failure to first call and hides
the coupling from every tool that reads imports statically — record it as a defect rather than closing the
task. A function-local import is legitimate only for a genuinely optional or expensive dependency, and then it
needs a comment saying which of the two it is.

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

`python-testing` owns what follows from this layout: `--import-mode=importlib`, test-file basename uniqueness,
and the `conftest.py` rules.

## Keep Entry Points Thin

Declare console scripts in `[project.scripts]`, pointing at a function rather than a module-level side effect.
Add `__main__.py` when the package should also run as `python -m mypkg`, and have it call the same function the
console script does.

The command-line layer parses and validates arguments, then calls into the package. Logic that lives in the CLI
module cannot be tested without invoking the CLI, and cannot be reused by anything that is not the CLI.

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
defect rather than a shortcut — nothing else will catch it.

## Before Calling Structural Work Done

1. Does the package import only after an install, rather than because of the working directory?
2. Does every new or moved module leave the dependency graph acyclic, without a function-local import standing
   in for a design decision?
3. Does each `__init__.py` have one of the three jobs, or nothing at all?
4. Can a reader find a module's tests from the module's name?

## Reference

- [src layout vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) —
  Python Packaging User Guide
- [Good integration practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html) — pytest
