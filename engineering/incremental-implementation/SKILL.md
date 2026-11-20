---
name: incremental-implementation
description: Execute an accepted plan or multi-file change as thin, individually verified slices, keeping the tree green between them. Use when implementing a feature or the next task from a plan, when a change spans several files, or when rolling incomplete work out behind a flag; not for planning or slicing the work itself (implementation-planning), test design (test-driven-development), or a single obvious one-file edit.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Incremental Implementation

Execute an accepted plan as working software, one verified slice at a time, so a defect surfaces in the slice
that caused it rather than in a pile of untested changes.

Take slice boundaries from the plan. When none exists, size each slice by a single observable outcome, such as
one endpoint, one component, or one migration. Decompose a larger unit with `implementation-planning`
before starting. This skill governs how you land a slice, not how you choose it.

Before starting, judge the extent of the work and of each slice. A slice may come without a sub-goal or success
signal from the plan, or you may be slicing without a plan. When such a slice's result could come out vague or drift,
propose a sub-goal and a success signal for it to the user. A slice with an obvious observable result needs none. On
an unattended run, set them yourself and record each one in the ledger as a judgment call.

## Know What Done Means

The work is done when every slice has landed green. Where a spec, technical design, or implementation plan
governs it, done also requires a separately dispatched conformance review against those documents that finds no
material mismatch. A plan from `implementation-planning` already schedules that review as its final gate; this
covers the plan-less path too. Skip it only with a stated reason, or at the user's direction.

Dispatch the review after the last slice lands. Send it to a fresh subagent or review lane whose brief names
`conformance-review` and supplies each governing document with its revision and the delivered change. The
code reviewer judges correctness and stays on that job. Fix a mismatch in the code as a new slice, then rerun the
review. Report a mismatch that needs a document changed to that document's owner instead of editing it.

For a long or unattended run, set the finish line first with `define-goal`. It writes this closing check into
the goal, so the harness re-sends it at every stop.

## Load the Skills the Work Names

A plan, handoff, or brief that names skills is an instruction to load them. Load each one when the first slice
that needs it begins. Before writing a new file, reread any skill loaded many slices earlier; its rules fade with
distance from the load. Where the repository overrides a skill's default, state which default and why. When a
named skill turns out not to apply, say so, because the plan then holds a claim to correct. This is done when
every named skill is loaded before its slice or reported as not applying.

## Run the Increment Cycle

Land one slice at a time, and finish each before starting the next:

1. **Implement** the smallest slice that produces a complete, observable behavior.
2. **Verify** it with the repository's own commands, such as tests, build, type check, and lint. Run each
   only where a change since its last run could affect its result. Add a test when the behavior has none (see
   `test-driven-development`).
3. **Commit** the verified slice as one logical change, with a message describing it, where commits are
   authorized. Otherwise leave it as one reviewable, checkpointed unit.
4. **Carry forward** to the next slice, and revisit a landed one only with cause.

Verify each slice before writing the next: a bug carried past its slice makes every later slice suspect and hides
which change caused it.

Beyond the review stages the plan places, decide from the code's complexity and the project's size whether a
maintainability review should join the correctness review. An example is `clean-code-reviewer` beside
`code-reviewer`. Ask the user for a ruling when unsure. Fold its findings in before the next slice builds on
the code. A correctness review alone misses the naming, placement, and comments that make the next change hard to
find.

## Keep Every Slice Landable

- **Green between slices.** After each slice the project builds and existing tests pass. Another
  session, or your own next step, inherits whatever state a stopping point leaves.
- **One logical change per commit.** Keep a refactor, a feature, and a config change in separate commits. A
  mixed commit hides bugs and turns a revert into an all-or-nothing choice.
- **Flag incomplete work rather than withholding it.** When a feature needs more slices than one merge should
  expose, merge it behind a default-off flag instead of holding a long-lived branch. Incomplete work then reaches
  the main line without becoming user-visible.
- **Build for reversibility.** Prefer additive changes; they revert cleanly. Keep a modification to existing
  code minimal and focused, and pair a schema migration with its rollback. Put a deletion and its replacement
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
