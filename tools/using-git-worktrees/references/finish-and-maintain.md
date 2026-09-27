# Finishing and Maintaining Worktrees

Read this before integrating, removing, moving, locking, or pruning a worktree, or when a worktree has been
damaged. For a worktree the harness created, read the harness's documentation for its cleanup first, then
inspect the worktree's status and `git worktree list --porcelain` before touching it by hand.

## Finish and Remove Safely

Before integration or cleanup, inspect the lane and its commits:

```bash
git -C <path> status --short
git -C <path> diff
git -C <path> diff --cached
git log --oneline <integration-ref>..<worktree-branch>
```

Preserve required work in commits, and confirm its integration or remote location when the task requires one.
A detached commit needs a branch or another durable ref before the worktree is removed.

Leave the worktree's directory before removing it. Then remove it with Git, so Git can verify that the tree is
clean and update its administrative state:

```bash
git worktree remove <path>
```

A refusal normally means the worktree contains changes or is locked. Inspect it. Do not force removal, unlock
a foreign worktree, or delete its branch unless the user explicitly authorized the resulting loss. Deleting the
branch is a separate operation after removal and needs its own integration check.

## Maintain Registered Worktrees

Move a registered worktree with `git worktree move`. If its directory was moved outside Git, run
`git worktree repair` with the resolved path. Lock a long-lived worktree on removable or intermittently
mounted storage with `git worktree lock --reason <reason>`.

Preview stale administrative cleanup before applying it:

```bash
git worktree prune --dry-run --verbose
```

Pruning removes stale registration data only. It does not recover or preserve files from a directory that was
removed outside Git.

## Worktree Problems

**`pwd: error retrieving current directory`, or every command failing at once**: the shell's working
directory was removed, most likely by a worktree or scratch-directory removal. The repository is fine. Recover
with a `cd` to a live directory, issued from outside whatever tool holds the dead working directory.

**A worktree was removed with uncommitted content**: nothing recovers that content. Its committed history is
still in the shared object database, and `git worktree list` and the branch reflogs show what the branch
pointed at.

**`git worktree remove` refuses**: the tree is dirty. Read what is there before forcing anything; the refusal
is the last thing standing between that work and the case above.

**Stale administrative entries after a directory was deleted by hand**: run `git worktree prune`, which
touches bookkeeping only.

## Primary Reference

- [Git worktree](https://git-scm.com/docs/git-worktree)
