---
name: brooks-lint-test-review
description: Review tests, test diffs, test strategy, and QA plans for missing regression coverage, weak assertions, brittle tests, fixture overreach, and false confidence. Use when user asks for test review, test strategy review, coverage review, QA review, regression review, or test plan review.
metadata:
  author: Joonas Onatsu
  license: MIT
---

# Test Review

## Iron Law

A test suite that passes while missing the real failure mode is worse than an
honest gap. Review for confidence, not count.

## Scope

Use for test diffs, test plans, regression strategy, acceptance criteria, and
coverage discussions.

## Workflow

1. Identify claimed behavior and failure modes.
2. Check whether tests prove the claim from the outside.
3. Look for missing regressions, weak assertions, brittle implementation detail
   checks, and fixture magic.
4. Separate "missing test" from "production design problem".
5. Recommend smallest high-value addition or rewrite.

## Review Questions

- Does test fail for right reason if behavior breaks?
- Are assertions specific enough to catch regression?
- Is coverage focused on user-visible behavior or only internals?
- Are edge cases around errors, retries, nulls, permissions, and boundaries
  actually covered?
- Do fixtures/mocks hide behavior instead of exposing it?
- Does plan define what red/green evidence should look like?

## Output Contract

For each finding:

- `Severity`
- `Confidence`
- `Evidence`
- `Gap`
- `Risk`
- `Suggested test shape`

Mention when a concern belongs in production design rather than test changes.

## Anti-Patterns

- Do not reward assertion count over signal.
- Do not demand tests for trivial pass-through code without risk.
- Do not convert behavior tests into brittle call-order checks.
- Do not hide uncertainty about framework-specific constraints.
