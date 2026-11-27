---
name: change-review
description: Review a code change, such as a diff, commit range, branch, or pull request, for correctness bugs, broken project rules, and performance risks before it merges. Use when asked to review a change or pull request, to find bugs in it, or whether it is ready to merge. Maintainability and coding standards go to coding-standards, design decay to brooks-review, a security audit to security-review, and checking work against its spec to conformance-review.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Change Review

Decide whether a change works and is safe to merge, and report what stands in the way. A review authorizes a
report, not fixes: change code only when the user also asked for the fix.

When you wrote the change in this conversation, have a fresh context run this review where the harness offers
one, such as a review subagent. Your own context shares the author's assumptions, so it misses what the author
missed.

## Keep to Correctness

This review asks whether the change does what it was meant to do without breaking anything. Leave neighbouring
questions to their own reviews, and recommend one in the report when the change needs it:

- **Maintainability.** Naming, size, nesting, duplication, and comments belong to `coding-standards` and the
  language's style skill. Report one here only when it hides a bug.
- **Design decay.** When the change spreads one decision across unrelated modules, adds a dependency against the
  layering, or bends the domain model to fit, recommend `brooks-review`.
- **Security.** Report an exploitable defect you can see, such as unparameterized SQL, as a finding. When the
  change touches authentication, secrets, input parsing, deserialization, or an agent's tool surface, also
  recommend `security-review` for the whole boundary.
- **Conformance.** When a spec, design, or plan governs the work, recommend `conformance-review` as a separate
  review.
- **Tests.** Name the tests the change lacks, and leave writing them to `test-engineer`.

An explicit rule in the project's instruction files, such as `AGENTS.md` or `CLAUDE.md`, is always yours to
enforce.

## Set the Scope

Review what the user names: a commit range, a branch, a file list, or a pull request. When nothing is named,
review the working tree: run `git status`, `git diff`, and `git diff --cached`, and read each untracked file in
full. Read enough surrounding code to judge each change in context. Leave code the change did not touch alone,
unless the change breaks it.

For a generated file, such as a lockfile, a migration, or generated client code, check that it matches its
source: the generator's output for the changed source, with no hand edits. Review the source line by line
instead of the output.

## Read the Intent First

1. Read the task: the spec, plan, issue, pull request description, or request behind the change. A change is
   correct only against what it was meant to do. When no task is available, judge against what the commit
   messages claim, and say so in the report.
2. Read the tests next. They show what the author intended and what is actually verified.

## Check Every Changed Hunk

Check each changed hunk for each of these:

- **Correctness.** Look for edge cases (empty, null, boundary, error paths), off-by-one errors, race conditions,
  and state left inconsistent. Look for errors swallowed or misreported, a contract a caller relies on broken,
  and tests that pass without testing the behavior.
- **What the change calls.** Confirm that each new or changed call, import, option, and configuration key
  exists, with the signature and behavior the code assumes. Use the language server's definition and type for
  project code, and the dependency's documentation or source at the version the project pins. Model-written code
  calls functions and flags that do not exist, and they read as plausibly as real ones.
- **What calls the change.** Trace each changed signature or behavior to every caller with the language
  server's references and incoming calls, and confirm the list with a text search.
- **Language traps.** Load the skill for the change's language when one is available, and check the hunk
  against its correctness rules, such as holding a lock across an `await` in async Rust.
- **Project rules.** Check the instruction files' explicit rules, such as a required tool, a forbidden pattern,
  a boundary on where code or data lives, or a commit convention.
- **Performance.** Look for unbounded loops or fetches, repeated work inside a loop, and a blocking call on a
  hot path.

## Check What the Change Left Out

A hunk-by-hunk read sees only what is present. After the hunks, ask what the change should have touched and
did not:

- another implementation or caller of an interface the change altered;
- a migration, schema, or serialized format that the changed data shape needs;
- configuration, its defaults, or its documentation;
- documentation or a changelog that still describes the old behavior.

For each deletion, search for anything that still uses what was removed.

## Keep Only Findings You Trust

Rate each candidate finding from 0 to 100 for how sure you are that it is real and matters, and report it at
80 or above. List a finding below 80 that would be serious if true once under **Unverified**, with the check
that would settle it, and drop the rest. Where your permissions allow, run the narrowest existing test that
settles a doubtful finding; otherwise name its command. Three real findings serve the reader better than a long
list they must triage.

Give each reported finding one tier, by what the verdict needs:

- **Must fix**: broken behavior, data loss, a security hole, an explicit rule broken, poor error handling, or a
  missing test. A test is missing for a reproduced defect the change fixes, for a failure that would otherwise pass
  silently and cost something, and for anything the user or the repository's test policy asks to be tested.
- **Should fix**: a defect with bounded consequence that may wait for a recorded follow-up, such as a slow path
  that no caller runs often yet.
- **Consider**: an optional improvement, such as a simpler design, a useful refactor, or removing a test that
  repeats another test's guard. Report at most five, and say how many you left out.

The review is done when every changed hunk has passed every check, the omission check has run, and each finding
cites a file and line.

## Report

Report in this order:

1. **Verdict**: `Ready`, `Ready after changes`, or `Not ready`, then one sentence saying why. Any open Must fix
   finding rules out `Ready`; use `Not ready` when the change needs rework or a decision rather than the listed
   fixes. On a pull request, `Ready` approves and the other two request changes.
2. **Scope**: the range or files reviewed, the task you judged them against, and whether you read, scanned, or
   ran tests.
3. **Findings**, most consequential first, each tagged `F1`, `F2`, and so on. Give each its tier, the file and
   line, what is wrong with its concrete consequence, the evidence, and the specific fix.
4. **Unverified**: the suspicions below the threshold, each with the check that would settle it.
5. **Next checks**: what the tests cover, which tests you ran with their results and any change a run made to
   the tree, and the commands the caller should still run. Name each missing test by its input and expected
   result. Name the reviews you recommend next.
6. **What holds**, only when something specific should survive a revision: at most two sentences, with the file
   and line.

A clean change gets the verdict, the scope, and the next checks. Post to a pull request or change its review
state only when the user asked for that.

## Attributions

See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for the sources this skill is based on.
