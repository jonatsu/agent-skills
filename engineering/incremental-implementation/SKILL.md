---
name: incremental-implementation
description: Execute an accepted plan or multi-file change as thin, individually verified slices, keeping the tree green between them. Use when implementing a feature or the next task from a plan, when a change spans several files, when about to write a large batch of code, or when rolling incomplete work out behind a flag; not for planning or slicing the work itself (implementation-planning), test design (test-driven-development), or a single obvious one-file edit.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Incremental Implementation

Execute an accepted plan as working software, one verified slice at a time, so a defect surfaces in the slice
that caused it rather than in a pile of untested changes. Write for an implementer who has a plan or a clear
change in hand and is about to start typing.

Take slice boundaries from the plan. When none exists, size each slice by a single observable outcome — one
endpoint, one component, one migration — and decompose a larger unit with `implementation-planning` before
starting. This skill governs how you land a slice, not how you choose it.

## Run the Increment Cycle

Land one slice at a time, and finish each before starting the next:

1. **Implement** the smallest slice that produces a complete, observable behavior.
2. **Verify** it against the repository's own commands — tests, build, type check, lint — running each only
   where the slice could have affected it. Add a test when the behavior has none (see `test-driven-development`).
3. **Commit** the verified slice as one logical change, with a message describing it.
4. **Carry forward** to the next slice; do not revisit a landed one without cause.

Do not accumulate unverified work. Once a slice is written, verify it before writing the next: a bug carried
past its slice makes every later slice suspect and hides which change caused it. Rerun a check only after a
change that could affect its result — re-running it on unchanged code proves nothing new.

## Keep Every Slice Landable

- **Green between slices.** After each slice the project builds and existing tests pass. Never leave the tree
  broken across a stopping point where another session, or your own next step, inherits it.
- **One logical change per commit.** Keep a refactor, a feature, and a config change in separate commits. A
  mixed commit hides bugs and turns a revert into an all-or-nothing choice.
- **Flag incomplete work rather than withholding it.** When a feature needs more slices than one merge should
  expose, merge it behind a default-off flag instead of holding a long-lived branch, so incomplete work reaches
  the main line without becoming user-visible.
- **Build for reversibility.** Prefer additive changes; they revert cleanly. Keep a modification to existing
  code minimal and focused, pair a schema migration with its rollback, and never delete something and replace
  it in the same commit — separate them so either half can be reverted alone.
- **Default to safe.** New behavior takes the conservative default; anything risky or destructive is opt-in.

## Recognize Drift

Stop and re-slice when you notice:

- more than a screenful of code written without a verifying run;
- unrelated changes accumulating in one slice, or a "while I'm here" edit to a file the slice does not need;
- the tree left broken, or large uncommitted work piling up, between slices;
- an incomplete feature about to become user-visible because the flag is "later."

The move against each is the same: shrink the slice until it verifies, commit what is green, and record anything
out of scope as a separate task rather than folding it in.

## Close Against the Spec

When an accepted specification or design governs the work, close the change by comparing the result against it with
`spec-conformance-review`. A formal plan built with `implementation-planning` already schedules this gate; this covers
the plan-less path — a large batch of code written without one — where nothing else would. Skip only with a stated
reason, or at the user's direction.
