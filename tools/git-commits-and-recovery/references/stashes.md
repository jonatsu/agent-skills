# Stashes

For linked worktrees, use the `using-git-worktrees` skill.

The stash ref belongs to the repository, not one worktree. An entry created in one lane is visible from every
other lane. Prefer a work-in-progress commit on a private branch when durable, lane-specific preservation is
needed. Honor any narrower repository rule that prohibits stash use.

Inspect `git stash list` before acting. Read an unfamiliar entry with:

```bash
git stash show -p 'stash@{N}'
```

When stash use is authorized, limit a new entry to explicit paths:

```bash
git stash push -u -m "<why>" -- <paths>
```

Use `git stash apply` when recovery should preserve the stash for another attempt. `pop` removes the entry
after a successful application, leaving nothing to retry if the result was wrong. A stash applied over a
conflict is not merged automatically: treat the conflicts as unresolved work and read the conflicting files
before continuing.

If the environment reserves stash deletion for the user, capture the entry's content and provide the exact
`git stash drop 'stash@{N}'` command rather than bypassing the control.

## Primary Reference

- [Git stash](https://git-scm.com/docs/git-stash)
