---
name: brooks-lint-design-review
description: Review plans, ADRs, designs, and cross-module changes for architecture, boundaries, coupling, dependency direction, abstraction drift, and integration risk. Use when user asks for architecture review, design review, plan review, ADR review, boundary review, or system-level feedback.
metadata:
  author: Joonas Onatsu
  license: MIT
---

# Design Review

## Iron Law

Only report design issues with a concrete failure mode, maintenance cost, or
coordination risk. Skip taste-only opinions.

## Scope

Use for plans, ADRs, refactors, cross-module changes, service boundaries, and
non-trivial diffs. Prefer high-signal findings over completeness.

## Workflow

1. Classify target: `PLAN`, `ADR`, `DIFF`, `CODE`, or `MIXED`.
2. Trace intended boundaries: ownership, data flow, dependencies, extension
   points, and rollback path.
3. Ask: what becomes harder to change, test, reason about, or deploy?
4. Report only findings with evidence from target material.
5. For each finding, suggest smallest practical remedy.

## Review Questions

- Does change mix policy, orchestration, and execution in one place?
- Do dependencies point wrong direction or create hidden coupling?
- Are responsibilities duplicated across modules or layers?
- Does abstraction hide important behavior, cost, or failure modes?
- Are extension points premature, or missing where future change is likely?
- Does plan leave migration, ownership, or rollback ambiguous?
- Will change make testing or debugging materially harder?

## Output Contract

For each finding, use:

- `Severity`: `high`, `medium`, or `low`
- `Confidence`: `high`, `medium`, or `low`
- `Evidence`: exact file/section/symbol/step
- `Problem`: what is wrong
- `Impact`: why it matters
- `Remedy`: smallest credible fix

If no strong findings, say so plainly.

## Anti-Patterns

- Do not restate the design.
- Do not propose rewrites without a local fix path.
- Do not argue style as architecture.
- Do not invent constraints absent from the material.
- Do not flood output with low-confidence edge cases.
