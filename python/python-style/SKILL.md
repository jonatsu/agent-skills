---
name: python-style
description: Write and review readable, idiomatic Python. Use for new Python code, style or conventions reviews, naming, docstrings, value types, datetime semantics, resource handling, or logging. Tool configuration belongs to python-project-management; detailed typing, validation, architecture, async, and testing have specialist skills.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Python Style

Everyday Python defaults for code whose conventions are not already settled. This skill owns the coding choices
that need judgment, including value types, logging, and docstrings, and hands each detailed subject to its
specialist. Load the specialist when the task reaches its subject:

| Subject                                                           | Skill                       |
| ----------------------------------------------------------------- | --------------------------- |
| Tool configuration, dependencies, and HTTP or CLI library choices | `python-project-management` |
| Annotation interfaces and type-checker problems                   | `python-typing`             |
| Boundary validation, exception design, and translation            | `python-error-handling`     |
| Module layout, package boundaries, and import direction           | `python-architecture`       |
| Asynchronous code and asynchronous resource lifetimes             | `python-async-patterns`     |
| Parallel CPU work with threads, processes, or joblib              | `python-parallelism`        |
| Tests and test configuration                                      | `python-testing`            |

## Respect Project Conventions

Use these defaults for new projects. In established projects, follow declared conventions and consistent local practice,
including for new files and modules. Check both before filling an undecided choice.

Do not recommend changes merely because these defaults differ. Recommend corrections supported by incorrect behavior,
security vulnerabilities, or concrete reliability or maintenance harm. Explain the evidence, consequence, and smallest
remedy. A different tool, layout, style, or supported syntax is not itself a defect.

Apply fixes within the authorized task; otherwise report the recommendation without changing the project.
An explicit modernization or conventions review permits broader recommendations.

## Readable Code

Use descriptive names and consistent domain vocabulary. Qualify generic symbols and filenames when context is ambiguous;
keep a working interface's name, since better isolated search results alone do not justify a rename. Keep
identifying literals intact where practical. Explain non-obvious behavior in searchable language.

Prefer straightforward control flow and guard clauses when they reduce nesting. Split functions when responsibilities
or control flow warrant it. Build abstractions and configuration options for present needs only.

Annotate function parameters and returns. Use built-in generics and union syntax supported by the project's Python floor.
Let local inference handle obvious variables. Import names explicitly rather than with a wildcard. Let the project's
formatter and linter settle mechanical style.

Write Google-style docstrings for public APIs when no documentation convention exists. Include `Args`, `Returns`, and
`Raises` when they explain behavior beyond the signature. Document units, constraints, ownership, and side effects;
omit empty sections and redundant descriptions.

## Value Types and Time

Prefer frozen `attrs` classes and `attrs.evolve` for internal value types. Use frozen stdlib dataclasses when adding
`attrs` brings little benefit, especially in dependency-free packages and small scripts. Mutable state is legitimate
when updates are part of its model. Create mutable defaults per call or instance when sharing is unintended.

Use domain types for dates, money, and structured values. Add wrappers when they protect meaningful invariants.
Prefer enums for closed sets with named states; preserve explicit serialized values when they form an external contract.
Use ordinary mappings where a model adds no useful contract.

For timestamps representing instants, use aware datetimes and normalize to UTC for storage and instant arithmetic.
Construct current timestamps with `datetime.now(UTC)` on Python 3.11+, or `datetime.now(timezone.utc)` on older versions.
Use `zoneinfo` for named zones. A naive timestamp needs a documented source timezone before conversion; never guess one.

Calendar dates and civil-time schedules have different semantics. Preserve the local time and named zone when a future
schedule depends on them. Decide how ambiguous or nonexistent local times resolve at the boundary.
Naivety alone is not proof of a defect; an ambiguous instant or incorrect conversion is.

## Resources and Diagnostics

Prefer existing helpers, then standard-library solutions, before adding dependencies. Select a library only when the
task needs its capability.

Prefer `pathlib.Path` for filesystem operations. Specify UTF-8 for text unless the format requires another encoding.
Use context managers for resources this code owns when the API supports them. Respect caller-owned lifetimes;
use `try/finally` when a context manager does not fit.

Prefer f-strings for ordinary interpolation. Keep parameterized APIs for logging and other structured operations.
Use stdlib `logging.getLogger(__name__)` as the logging baseline, with arguments passed separately for deferred formatting.
Let applications configure handlers. Choose structured logging when consumers need structured fields, and preserve the
project's logging stack. Reserve terminal output for intentional CLI interaction and results.

Prefer subprocess argument lists. Use `check=True` when nonzero exit means failure; otherwise inspect the result.
Use a shell only when its semantics are needed, with deliberate handling of arguments and untrusted input.
