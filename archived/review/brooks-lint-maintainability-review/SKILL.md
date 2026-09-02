---
name: brooks-lint-maintainability-review
description: Review code, diffs, PRs, and refactors for complexity, naming drift, duplication, hidden control flow, error handling gaps, and maintainability risks. Use when user asks for code review, diff review, PR review, maintainability review, readability review, or refactor feedback.
metadata:
  author: Joonas Onatsu
  license: MIT
---

# Maintainability Review

## Iron Law

Find few issues that will cost future engineers time. Ignore cosmetic nits a
formatter, linter, or local convention already owns.

## Scope

Use for diffs, files, PRs, refactors, and implementation plans that may create
maintenance debt.

## Workflow

1. Identify change surface and dominant risk: complexity, duplication, naming,
   error handling, state flow, or API shape.
2. Compare against nearby patterns; respect repo-local conventions first.
3. Look for places where intent becomes harder to read or behavior easier to
   misuse.
4. Report only findings with clear maintenance impact.
5. Suggest smallest refactor or guard that improves clarity.

## Review Questions

- Is one function/module doing too many jobs?
- Did names drift from real behavior or domain language?
- Is logic duplicated with likely divergence risk?
- Are invariants implicit instead of enforced?
- Are errors swallowed, normalized badly, or handled inconsistently?
- Does control flow depend on hidden state or ordering assumptions?
- Did public API surface grow without clear need?

## Output Contract

Use one section per finding:

- `Severity`
- `Confidence`
- `Evidence`
- `Problem`
- `Impact`
- `Minimal fix`

Prefer 0-5 findings. If everything else is weak or subjective, omit it.

## Anti-Patterns

- Do not review formatting or trivial style.
- Do not ask for abstraction "for cleanliness" alone.
- Do not recommend broad rewrites when extraction or guard clauses suffice.
- Do not mark unfamiliar code as wrong without evidence.
- Do not treat personal preference as debt.
