# Worktrees and Stashes

Use this reference when isolating parallel work, setting changes aside, removing a worktree, or recovering
from worktree or stash state.

## Worktrees

A linked worktree has its own `HEAD`, index, and worktree but shares repository objects, refs, and stashes.
Inspect `git worktree list` and the target worktree's status before changing or removing it.

- Leave a worktree before removing its directory. Removing the current working directory leaves the shell in a
  dead path and causes later commands to fail with unrelated-looking `pwd` errors.
- Plain `git worktree remove` refuses a dirty worktree. Inspect the content; do not replace the refusal with
  `--force` without explicit authorization to discard the resolved files.
- `git worktree prune` removes stale administrative entries after a directory disappeared. It does not recover
  uncommitted content.

A linked worktree's `.git` is a file containing a `gitdir:` pointer. A recursive command guarded only by
`--exclude-dir=.git` can still edit it. Scope bulk edits to an explicit file list. Verified with GNU grep and
git 2.43.0, 2026-08-26.

## Stashes

The stash ref belongs to the repository, not one worktree. An entry created in one lane is visible from every
other lane. Prefer a work-in-progress commit on a private branch when durable, lane-specific preservation is
needed.

Inspect `git stash list` before acting. Read an unfamiliar entry with:

```bash
git stash show -p 'stash@{N}'
```

To stash only intended paths, use an explicit pathspec:

```bash
git stash push -u -m "<why>" -- <paths>
```

Use `git stash apply` when recovery should preserve the stash for another attempt. `pop` removes the entry
after a successful application. Treat conflicts as unresolved work and inspect them before continuing.

If the environment reserves stash deletion for the user, capture the entry's content and provide the exact
`git stash drop 'stash@{N}'` command rather than bypassing the control.
