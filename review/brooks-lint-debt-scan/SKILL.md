---
name: brooks-lint-debt-scan
description: "Scan plans, diffs, file sets, or architecture slices for technical debt worth paying down now: risky shortcuts, migration gaps, temporary code likely to calcify, and missing cleanup follow-ups. Use when user asks for debt scan, tech debt review, health check, sweep, broad risk scan, or cleanup audit."
metadata:
  author: Joonas Onatsu
  license: MIT
---

# Debt Scan

## Iron Law

Only call something debt if it creates future drag, defect risk, or migration
cost. Temporary code with a clear owner and exit path is not automatically debt.

## Scope

Use for broad scans where full line-by-line review would be noisy.

## Workflow

1. Determine artifact: plan, diff, file set, or architecture slice.
2. Look for shortcuts likely to harden into defaults.
3. Separate immediate debt from acceptable trade-offs.
4. Prioritize by cost of delay and blast radius.
5. Recommend defer, fix now, or track explicitly.

## Debt Signals

- TODO behavior without owner or expiry condition
- parallel code paths with no removal plan
- leaky abstractions or one-off exceptions in shared paths
- hidden migration assumptions
- config/flags likely to become permanent
- manual steps missing automation or validation
- broad fallback logic masking real failures

## Output Contract

Return up to 5 items:

- `Priority`: `fix-now`, `track`, or `ignore`
- `Confidence`
- `Evidence`
- `Debt`
- `Why now`
- `Smallest next step`

If scan finds no meaningful debt, say so.

## Anti-Patterns

- Do not label all unfinished work as debt.
- Do not confuse roadmap incompleteness with engineering debt.
- Do not produce vague "monitor this" advice.
- Do not recommend cleanup with no owner or trigger.
