---
name: coding-standards
description: "Write, refactor, and check code against language-agnostic standards: design principles, naming, comments, formatting, types, errors, logging, and code smells. Use before writing a new file or function, when refactoring, when applying the quality gate before a commit, or when checking a change against these standards. Language-specific style belongs to that language's skill (python-style), a broad PR or design review to brooks-review, and writing tests to test-engineer."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Coding Standards

Language-agnostic defaults for writing and changing code. Understand the code you change, and follow the
repository's conventions and existing patterns before inventing replacements. Apply these defaults where a
choice is undecided. Recommend a change to existing code only when incorrect behavior, a security flaw, or
concrete reliability or maintenance harm supports it, not because a default differs.

Preserve existing guarantees unless an authorized change requires otherwise. Keep each change cohesive and
scoped, and write for the next reader: clarity over cleverness. Complexity is code a reader cannot grasp
quickly, or that invites bugs on the next change; keep every change from adding it.

Load a reference when its concern is in play:

- SOLID design, the refactoring-discipline rule, the performance checklist, and pre-commit quality gates:
  `references/solid-and-quality.md`.
- Comment content, annotations, and worked examples: `references/comments.md`.
- Testing standards and the solve-the-problem-not-the-test rule: `references/testing-standards.md`.

A language-specific rule always wins over a default here where the two differ.

## Principles

- KISS: choose the simplest design that meets the stated requirements and fits the environment. Prefer the
  obvious solution over a clever or prematurely optimized one, and optimize only against a measurement.
- Scope: change only what the task asks for. A bug fix leaves the surrounding code alone. Make an incidental fix
  only when something is plainly broken and the correct behavior is already settled, and keep it local and
  reversible. Trace every change to the request or a necessary consequence of it, and fix any failure your own
  change caused.
- Defensive coding: add checks for failures that can actually occur, and trust internal code and framework
  guarantees for those that cannot.
- YAGNI: build only what the current task needs. Solve the problem you have now, and add an abstraction when the
  second use arrives.
- DRY: give each piece of knowledge one authoritative definition, and consolidate a duplicate rather than
  editing both copies. DRY governs knowledge, not lines that look alike; couple two things only when they share
  one reason to change. Same business logic in two places must be fixed; similar code that may evolve apart is
  left alone.

## Immutability

Return new values rather than mutating inputs or shared state. Immutability prevents hidden side effects, makes
changes easier to trace, and keeps concurrent code safe. Mutate deliberately, not by default: in a hot path, a
large buffer, or a language where in-place change is the idiom, keep the mutation local and documented. A
language rule with a stronger convention wins.

## Types and Interfaces

Make illegal states unrepresentable: let the type system reject invalid data instead of guarding against it at
runtime. Model a constrained value as an enum or a newtype rather than a bare string, and reach for a
discriminated union where a value carries a variant tag. In a typed language, annotate public signatures and
boundaries, and let inference cover the obvious locals. Expose the smallest public API that meets the need, and
default to private. Accept an interface or trait as a parameter, and return a concrete type. Depend on
abstractions rather than concrete implementations at a module boundary. Treat an escape from the type system,
such as `any`, an unchecked cast, or a suppressed checker error, as a cost to justify in a comment.

## Code Organization

Organize by feature or domain rather than by technical type, keep related code together, and let tests mirror
the source tree. Treat the layout below as the softest default, the starting point when nothing more specific
applies; a repository's own conventions, a framework's expected layout, or a language rule always win.

```text
src/
  <feature>/        # one directory per feature or domain, owning its logic
  core/ | domain/   # business rules, independent of I/O and frameworks
  adapters/ | io/   # boundaries: HTTP, database, filesystem, external services
  shared/ | utils/  # small, dependency-free helpers reused across features
  types/            # shared type and interface definitions, where the language separates them
tests/
  unit/             # fast, isolated tests of pure logic
  integration/      # tests across real boundaries and wired components
```

### File size and cohesion

Keep source files small and cohesive: roughly 200-400 lines, with ~800 as an upper limit. Past that limit,
extract a module; keep a larger file only when it is one cohesive unit that resists division. Test files follow
the same limits. The exception is bulk that is data rather than authored logic, such as generated code,
snapshots, fixtures, vendored sources, or a large inline test corpus, where the size is content to store rather
than code to read.

### Formatting

Let the project's formatter and linter decide layout, and match the surrounding style where none is configured.
Format only the lines your change touches: a reformatted file buries the real change in the diff and collides
with concurrent work.

## Naming

Give everything a descriptive, intention-revealing name, so the name says what the thing holds or does without
a comment. Name a function for what it does, such as `getUserById` rather than a bare `fetch` or `get`. Avoid
abbreviations except ones that are universally understood, such as `url` or `id`. Write a boolean name as a
claim that reads as a question, such as `isLoading`, `hasError`, or `canSubmit`, under the applicable language
or package convention. Keep constants and types visually distinct from ordinary values where the language draws
that distinction. A language-specific rule overrides this where a pattern is not idiomatic, and casing and
framework prefixes belong to that rule.

Give a function a name rather than passing a long anonymous closure, since a name helps both the reader and the
stack trace. Keep closures short where they are idiomatic.

## Comments

Write clear code and names first, and reach for a comment second. Use a comment to explain why: non-obvious
intent, a constraint, an algorithm choice, a workaround, or a governing decision, never to restate what the
code already shows. When a better name would remove the need, rename instead. Keep a public API's doc-comment,
which is a contract for callers who will not read the implementation. `references/comments.md` carries the
worked examples, the annotation vocabulary, and the anti-patterns.

Keep an external reference only when it prevents an editing mistake. Reference a mechanism first, then a stable
identity, then a path, and leave line numbers out. Encode a dependency in an assertion, a type, a test, or an
import, and let the comment say why. Keep affected documentation accurate when a change makes it wrong.

## Code Smells to Avoid

### Deep Nesting

Use early returns instead of stacked conditionals. Past about four levels of nesting, restructure: extract a
function or invert a guard.

### Long Functions

Keep a function focused on one job. Past roughly 50 lines it is usually doing several, so split it, unless the
length is one unavoidable sequence, such as a long switch or a builder, that a split would only obscure. Keep
the parameter list short; past three or four parameters, bundle the related ones into a type.

### Hardcoded Values

Name every non-obvious literal: a number, string, path, URL, or key. A bare literal carries no meaning, drifts
out of sync with its copies, and resists search and override. The one exception is a value self-evident in
context, such as a `0` index or a `2` that halves. Name any literal that appears more than once; that is DRY.

Read environment-specific or deployment-specific values, and secrets, from configuration or the environment. A
single-file script or one-off utility needs no configuration surface, so name such values as constants at the
top instead. Read a secret from the environment, never inline.

### Global State

Pass dependencies explicitly rather than reaching for shared mutable global state, which hides coupling and
makes tests order-dependent.

### Dead Code

Delete unused code. Version control keeps the history if you ever need it back.

## Input Validation

Validate every input at the system boundary before processing, using schema-based validation where it is
available, and fail fast with a clear message. Treat all external data as untrusted: API responses, user input,
and file content.

## Errors and Configuration

Handle every error by class. Recover from what is absent or partial by falling back to a documented default.
Fail closed on what is present but invalid: a wrong type, an out-of-range value, an unknown key. Name the
offending key and the shape you expected. When you re-raise an error, add the context the caller lacks. Surface each
failure where its user will see it, phrased so they can act on it, and record the technical detail where an
operator can find it. In a CLI or other single-artifact tool, write a clear message to stderr and exit nonzero;
in a service or UI, show a user-facing message and log the full context.

When you ship a deliverable product or application rather than a scratch script, make its behavior configurable
and treat the configuration schema as an interface: document every option and its default, and validate it on
load.

## Logging

Log in structured records rather than free text, so a machine can filter and a human can scan. Give each record
a level, the unit or aspect it came from, and the key-value context needed to trace one run. Record a timestamp
in UTC and format it as ISO-8601. Make every message identifiable to its component. Name a persisted log file
to keep runs apart and avoid clobbering: `<app>-<YYYY-MM-DD>-<HH-MM>[-<run>].log`. Add the run counter when one
app can start more than once within a minute.

## Testing

Write and structure tests to the standards in `references/testing-standards.md`: test behavior rather than
implementation, cover the edge cases, keep each test fast and isolated, and solve the problem rather than the
test. For test-first implementation of a specific behavior, load `test-driven-development`; for strategy,
coverage judgment, and adversarial validation, load `test-engineer`.
