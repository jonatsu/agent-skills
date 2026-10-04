---
name: incremental-implementation
description: Execute an accepted plan or multi-file change as thin, individually verified slices, keeping the tree green between them. Use when implementing a feature or the next task from a plan, when a change spans several files, when about to write a large batch of code, or when rolling incomplete work out behind a flag; not for planning or slicing the work itself (implementation-planning), test design (test-driven-development), or a single obvious one-file edit.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Incremental Implementation

Execute an accepted plan as working software, one verified slice at a time, so a defect surfaces in the slice
that caused it rather than in a pile of untested changes.

Take slice boundaries from the plan. When none exists, size each slice by a single observable outcome, such as
one endpoint, one component, or one migration, and decompose a larger unit with `implementation-planning`
before starting. This skill governs how you land a slice, not how you choose it.

## Know What Done Means

The work is done when every slice has landed green and, where a spec, technical design, or implementation plan
governs it, a separately dispatched conformance review against those documents finds no material mismatch. A
plan from `implementation-planning` already schedules that review as its final gate; this covers the plan-less
path too. Skip it only with a stated reason, or at the user's direction.

Dispatch the review after the last slice lands, to a fresh subagent or review lane whose brief names
`spec-conformance-review` and supplies each governing document with its revision and the delivered change. The
code reviewer judges correctness and stays on that job. Fix a mismatch in the code as a new slice, then rerun the
review. Report a mismatch that needs a document changed to that document's owner instead of editing it.

For a long or unattended run, set the finish line first with `define-goal`, which writes this closing check into
the goal so the harness re-sends it at every stop.

## Run the Increment Cycle

Land one slice at a time, and finish each before starting the next:

1. **Implement** the smallest slice that produces a complete, observable behavior.
2. **Verify** it with the repository's own commands, such as tests, build, type check, and lint, running each
   only where a change since its last run could affect its result. Add a test when the behavior has none (see
   `test-driven-development`).
3. **Commit** the verified slice as one logical change, with a message describing it.
4. **Carry forward** to the next slice, and revisit a landed one only with cause.

Verify each slice before writing the next: a bug carried past its slice makes every later slice suspect and hides
which change caused it.

## Keep Every Slice Landable

- **Green between slices.** After each slice the project builds and existing tests pass, because another
  session, or your own next step, inherits whatever state a stopping point leaves.
- **One logical change per commit.** Keep a refactor, a feature, and a config change in separate commits. A
  mixed commit hides bugs and turns a revert into an all-or-nothing choice.
- **Flag incomplete work rather than withholding it.** When a feature needs more slices than one merge should
  expose, merge it behind a default-off flag instead of holding a long-lived branch, so incomplete work reaches
  the main line without becoming user-visible.
- **Build for reversibility.** Prefer additive changes; they revert cleanly. Keep a modification to existing
  code minimal and focused, pair a schema migration with its rollback, and put a deletion and its replacement
  in separate commits, so either half reverts alone.
- **Default to safe.** New behavior takes the conservative default; anything risky or destructive is opt-in.

## Recognize Drift

Stop and re-slice when you notice:

- more than a screenful of code written without a verifying run;
- unrelated changes accumulating in one slice, or a "while I'm here" edit to a file the slice does not need;
- the tree left broken, or large uncommitted work piling up, between slices;
- an incomplete feature about to become user-visible because the flag is "later."

The move against each is the same: shrink the slice until it verifies, commit what is green, and record anything
out of scope as a separate task rather than folding it in.
