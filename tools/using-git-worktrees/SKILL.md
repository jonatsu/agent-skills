---
name: using-git-worktrees
description: Isolate parallel work in Git worktrees, from creation through cleanup. Use when work needs its own checkout so it cannot disturb the current one, such as parallel agents, a second branch alongside the current one, or a plan run in isolation, and when finishing, removing, pruning, or repairing a worktree. Use git-commits-and-recovery for commits, stashes, and history rewriting.
license: MIT
compatibility: Requires Git.
metadata:
  author: Joonas Onatsu
---

# Using Git Worktrees

A linked worktree gives one lane of work its own files, `HEAD`, and index, so parallel lanes cannot overwrite
each other's checkout.

## 1. Detect Existing Isolation

Run these before creating anything, even when the answer looks obvious: a harness-created worktree looks like
an ordinary checkout.

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" && pwd -P)
git branch --show-current
git rev-parse --show-superproject-working-tree
```

- **`GIT_DIR` differs from `GIT_COMMON`:** you are already in a linked worktree, possibly one the harness
  created. Do not create another for the same task. Report the path and branch, or a detached `HEAD`, which
  needs a branch before the work is finished. Continue at step 4.
- **The last command prints a path:** you are inside a submodule. Git documents multiple checkouts of
  submodules as incomplete, so stop and assess the repository's submodule workflow before creating a worktree.
- **Otherwise** you are in an ordinary checkout. Create a worktree when the user asked for one, a declared
  preference in your instructions calls for one, or the current checkout holds unrelated or concurrent work.
  When none applies, ask whether to isolate the work before creating one.

## 2. Use the Harness's Worktree Mechanism When It Has One

Some agent harnesses create worktrees themselves, as a tool, a command, or a launch option, and track their
location, branch, and cleanup. When yours has one, use it and continue at step 4. A worktree made with
`git worktree add` behind such a harness's back is state it cannot see or clean up. Read that harness's
current documentation for its placement and lifecycle rather than inferring them from this skill.

## 3. Create the Worktree With Git

Record the starting state, including every registered worktree:

```bash
git rev-parse --show-toplevel
git rev-parse HEAD
git status --short
git diff --cached --name-only
git worktree list --porcelain
```

Choose the location in this order:

1. A worktree location declared in your instructions or by the user.
2. An existing project-local `.worktrees/` or `worktrees/` directory, `.worktrees/` first, but only when
   `git check-ignore --no-index <dir>` confirms Git ignores it.
3. A sibling directory outside the repository, such as `../<repo>-worktrees/<branch>`, so the main checkout
   can never stage it.

Leave `.gitignore` unchanged. If only an unignored project-local directory is available, use the sibling
default or ask the user. Resolve the destination and inspect its parent first. Stop when an existing path,
unexpected symlink, registered worktree, or branch collision makes ownership unclear.

Create a new branch from an explicit start point:

```bash
git worktree add -b <new-branch> <path> <start-point>
```

Use `git worktree add <path> <branch>` for an existing branch that is not checked out elsewhere, and
`git worktree add --detach <path> <start-point>` for disposable inspection or testing. Never use `-B` or
`--force` to get past a refusal: Git refuses to check out one branch in two worktrees, and that refusal is an
ownership signal.

If creation fails with a permission or sandbox denial, report it and ask before working in place. The
isolation was the point, and a sibling lane may be live in the current checkout.

Verify the result:

```bash
git worktree list --porcelain
git -C <path> rev-parse HEAD
git -C <path> branch --show-current
git -C <path> status --short
```

Require the expected start commit, the expected branch or detached state, and a clean status. Confirm that
the original checkout's `HEAD`, index, and status still match what you recorded.

## 4. Set Up and Record a Baseline

A new worktree holds tracked content only. Ignored and untracked local files, such as environment files,
credentials, build output, and installed dependencies, do not carry over. Follow the repository's documented
setup and toolchain. Do not guess a package manager, install dependencies the documentation does not call for,
or copy secrets from another checkout. Check that required local files exist without printing their contents.

Run the cheapest validation that is relevant to the task, even in a fresh worktree. When it fails, report the
failures and ask whether to proceed or investigate: a failing baseline makes every later failure ambiguous.

Report:

```text
Worktree ready at <absolute-path> on <branch> from <start-point>
Baseline: <command> - <result>
```

## Shared State Between Worktrees

Worktrees share the object database, branches and other refs, tags, remote-tracking refs, repository
configuration, and the stash. A commit made in one lane is visible in every other lane at once, and a ref or
configuration change affects all of them. Per-worktree configuration exists only when the repository enables
`extensions.worktreeConfig`. Recheck shared refs before rebasing, resetting, deleting a branch, integrating, or
pushing, and do not treat the stash as private to a lane. In a linked worktree `.git` is a file, not a
directory, so locate Git administrative files with `git rev-parse --git-path <name>`.

## Finishing, Removing, and Maintaining

Before integrating, removing, moving, locking, or pruning a worktree, or when one has been damaged, read
[references/finish-and-maintain.md](references/finish-and-maintain.md).
