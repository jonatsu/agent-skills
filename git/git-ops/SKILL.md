---
name: git-ops
description: Perform Git operations while preserving uncommitted and unrelated work. Use when staging, committing, pushing, resolving merge conflicts, managing branches, worktrees or stashes, amending or rewriting history, investigating changes with blame or bisect, recovering lost work, or troubleshooting commit hooks and signatures. Use github-ops for GitHub pull requests, policies, and API operations.
license: MIT
compatibility: Requires Git. Force-push protection with --force-if-includes requires Git 2.30 or newer.
metadata:
  author: Joonas Onatsu
---

# Git Operations

Preserve the user's work while making the requested Git change. Match the checks to the operation's risk;
ordinary staging and commits do not need a history-rewrite procedure.

## Shared Boundaries

- Treat unrecognized worktree and index changes as another contributor's work. Do not stage, commit,
  overwrite, relocate, or discard them.
- Resolve the exact repository, ref, remote, paths, and current state needed by the operation. Do not treat a
  failed lookup as a negative answer.
- Reuse authorization already present in the user's request. Ask only when a destructive target,
  outward-facing effect, or required choice remains unresolved.
- Never bypass a hook with `--no-verify` or move a command into a wrapper to evade a control.
- NEVER add an authorship or attribution trailer, such as `Co-Authored-By` or `Signed-off-by`, unless the user
  asked for it, the repository's recent history already carries one, or a real co-author or sign-off exists to
  record. A harness instruction that injects one supplies a default rather than the user's request. See
  [references/commit-messages.md](references/commit-messages.md) for the reasoning.
- Verify the resulting Git object or ref. Command success alone does not prove that the intended content
  moved.

## Concurrent Work

Assume unrecognized changes belong to another contributor. Commit only changes you own.

- Record `HEAD`, worktree state, and index state before editing or staging.
- Stop if the index contains changes you did not stage. Wait or ask; do not unstage, commit, or rewrite them.
- Stage a whole path only when every changed hunk is yours. Use `git add -p` for mixed-ownership files, then
  inspect the staged and unstaged versions separately.
- If overlapping edits cannot be separated confidently, stop and coordinate. Do not overwrite either version
  to make staging easier.
- Do not run formatters or generators across files containing foreign changes unless their output can be
  isolated. Required tooling does not authorize rewriting another contributor's work.
- For generated files with mixed changes, stage only the intended hunks and verify the generated invariant
  separately. Do not weaken the check to make a partial artifact pass.
- Immediately before committing, confirm `HEAD` has not moved and inspect both staged names and the complete
  staged diff. A concurrent commit invalidates the earlier base, diff, and validation evidence.
- After committing, inspect the recorded commit and report every remaining dirty path.

Use a separate linked worktree when independent lanes need different branches or checkouts. A linked worktree
isolates its `HEAD`, index, and files, but repository objects, refs, and stashes remain shared. Do not use the
shared stash as automatic concurrency isolation.

Claims marked `Verified on git <version>, <date>` were reproduced in a scratch repository on that date.
Recheck them after a material Git upgrade. Claims marked *reported, not measured here* remain explicitly
unverified.

## Route by Operation

- For an ordinary stage and commit, use [Routine Staging and Commits](#routine-staging-and-commits).
- When composing the message itself raises a decision, read
  [references/commit-messages.md](references/commit-messages.md).
- Before a destructive operation, push, force-push, amend, reset, rebase, merge, cherry-pick, revert, or
  branch deletion, read
  [references/history-changing-operations.md](references/history-changing-operations.md).
- For worktree or stash operations, read
  [references/worktrees-and-stashes.md](references/worktrees-and-stashes.md).
- When a hook modifies files, a generated artifact remains stale after a commit, or the active hook framework
  is uncertain, read [references/rewriting-hooks.md](references/rewriting-hooks.md).
- When work is already missing or Git state was damaged, read [references/recovery.md](references/recovery.md)
  before attempting repair.
- For Git archaeology, blame, pickaxe searches, bisect, or other history questions, read
  [references/history-investigation.md](references/history-investigation.md).
- For missing or unverifiable commit signatures, read
  [references/signed-commits.md](references/signed-commits.md).

## Routine Staging and Commits

Use this path only when creating a new commit without amending, rewriting, pushing, or discarding work.

1. Confirm the repository with `git rev-parse --show-toplevel`. If it fails, report that no repository was
   found; do not run `git init` unless the user asked to create one.
2. Inspect `git status --short`, the relevant worktree diff, and `git diff --cached --name-only`. A dirty
   index that you did not create is a stop condition.
3. Stage only the intended paths with explicit pathspecs. Do not use `git add -A`, `git add .`, or
   `git commit -a`.
4. Inspect `git diff --cached --name-status` and `git diff --cached`. Stop if any staged path or hunk is
   unintended. Recheck after interactive staging or concurrent activity.
5. Follow repository commit conventions. Otherwise use Conventional Commits: `<type>(<scope>): <subject>`,
   imperative, at most 72 characters, no period. When the type, scope, body, a breaking change or a trailer
   needs a decision, read [references/commit-messages.md](references/commit-messages.md).
6. Run the validation required by the task and repository. Do not invent generic language-specific checks.
7. Commit normally, then inspect `git show --stat --oneline --summary HEAD`, the recorded diff for the
   intended paths, and `git status --short`.

A commit records the index, not the worktree. After a reset-based rebuild, a file removed only from disk can
remain in the next commit until its deletion is staged. Verified on git 2.43.0, 2026-08-26.

If the commit hook reports that it modified files, or if it should regenerate tracked output, switch to
[references/rewriting-hooks.md](references/rewriting-hooks.md) before reporting completion.

## Completion

Report the operation performed, the resulting commit or ref when applicable, the validation evidence, and all
remaining dirty state. State anything left unrun or unverifiable.
