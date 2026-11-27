---
name: brooks-review
description: "Review code for design decay, such as change propagation, knowledge duplication, accidental complexity, dependency disorder, and domain model distortion, with Symptom → Source → Consequence → Remedy findings drawn from twelve classic engineering books. Use when asked about design smells, decay, or the long-term maintainability of a change, file, or module. A correctness review of a change before merge belongs to change-review."
license: MIT
metadata:
  author: hyhmrright
---

# Brooks-Lint — PR Review

## Setup

Read in order:

1. `references/common.md` — Iron Law, Project Config, Report Template, Health Score
2. `references/source-coverage.md` — book coverage, exceptions, tradeoffs
3. `references/decay-risks.md` — symptom definitions and source attributions
4. `pr-review-guide.md` (this directory) — the analysis process

## Process

**Scope:** if the user did not specify files or paste code, apply Auto Scope Detection
(`references/common.md`) first.

1. Understand the review scope, then scan for each decay risk in the order specified (Steps 1–6 of the guide)
2. Run the Quick Test Check (Step 7 of the guide) — skip for docs-only or non-production changes
3. Apply the Iron Law to every finding
4. Output using the Report Template from common.md

**Mode line in report:** `PR Review`
