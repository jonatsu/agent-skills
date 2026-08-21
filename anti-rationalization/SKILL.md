---
name: anti-rationalization
description: Pre-written rebuttals to the excuses agents use to skip specs, tests, verification, reviews, scope discipline, and simplicity. Use when about to skip a lifecycle phase, justify weak validation, expand scope, or ship on insufficient evidence.
metadata:
  author: Joonas Onatsu
  license: MIT
---

# Anti-Rationalization Table

Pre-written rebuttals to lies the agent hasn't yet told. When tempted to skip a phase, check this table before proceeding.

The excuse/rebuttal table is a common community pattern; the entries below are this project's own set.

**Match evidence to risk.** These rebuttals fight *rationalized* shortcuts, not proportionate judgment. For a typo, formatting-only edit, comment, or docs-only change with no executable behavior, keep verification proportional: inspect the diff and run a lightweight relevant check if one exists. NEVER invent tests for a change that cannot break behavior.

## Process shortcuts

| Excuse | Rebuttal |
|---|---|
| "Too simple for a spec." | Acceptance criteria still apply. Five lines is fine. Zero is not. |
| "I'll write tests later." | No later exists in this session. Write the failing test first. |
| "Tests pass, ship it." | Passing tests are evidence, not proof. Did you run the specific scenario that covers the change? |
| "Quick refactor while I'm here." | Scope discipline. Touch only what's asked. Note the refactor opportunity, don't act on it. |
| "This is obvious, no need to research." | Grep before guessing. Read before assuming. Obvious is how missed callsites happen. |
| "I'll explain my approach first." | Act, then report results. Narration burns tokens and delays delivery. Still confirm first for destructive, ambiguous, or approval-gated actions. |

## Verification shortcuts

| Excuse | Rebuttal |
|---|---|
| "The types check, so it's correct." | Typecheck proves syntax, not behavior. Run the code path. |
| "I checked one case, the rest follow." | Edge cases don't follow. Test boundaries, nulls, errors, concurrency. |
| "No tests needed, it's config-only." | Config changes break systems. Verify the config loads and produces expected behavior. |
| "The old tests still pass." | Old tests cover old behavior. New behavior needs new evidence. |

## Scope shortcuts

| Excuse | Rebuttal |
|---|---|
| "Fixing this bug requires modernizing adjacent code." | No it doesn't. Fix the bug. File the modernization separately. |
| "I'll remove this dead code I noticed." | Chesterton's Fence. Understand why it exists before deleting. Confirm it's actually dead with `lsp references`. |
| "While I'm in this file, I'll also..." | Stop. One concern per change. The "also" is a separate task. |

## Complexity shortcuts (KISS)

| Excuse | Rebuttal |
|---|---|
| "We'll need this abstraction later." | Later is speculation. Two call sites make it real. One does not. |
| "This deserves its own file/module." | Does it? If it's under 40 lines and called from one place, it lives where it's used. |
| "I'll add a factory/builder/strategy for flexibility." | Solve the problem in front of you. Name the second concrete consumer or delete the pattern. |
| "A wrapper will make this cleaner." | A wrapper adds a layer to read through. Inline the logic unless it's called from multiple sites. |
| "This dependency handles it better than stdlib." | 20 lines of plain code you control beats a dependency you don't. Justify the import. |

## Applying this table

- Before skipping any lifecycle phase (spec, plan, test, review), MUST check whether the justification appears above.
- If it does, MUST follow the rebuttal.
- If the justification is genuinely novel, MUST state it explicitly so the user can evaluate it.
