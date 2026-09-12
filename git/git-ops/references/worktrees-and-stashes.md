# Worktrees and Stashes

Use this reference when isolating concurrent work, changing checkouts independently, setting changes aside,
removing a worktree, or recovering worktree or stash state.

## Concurrent Worktree Workflow

A linked worktree gives one lane its own files, `HEAD`, and index. Use one when independent work needs a
different branch or checkout, when the current worktree contains unrelated changes, or when a risky operation
should not disturb the active checkout. A lane already inside a linked worktree may create another one when
the new task needs independent ownership.

### Inspect Before Creating

Record the current repository and every registered worktree:

```bash
git rev-parse --show-toplevel
git rev-parse HEAD
git status --short
git diff --cached --name-only
git worktree list --porcelain
```

Choose an owner, explicit path, unique branch, and exact start point. Follow an existing repository or user
placement convention. Otherwise prefer a sibling path outside the repository so the main worktree cannot
stage it accidentally. If the path must be inside the repository, confirm it is already ignored with
`git check-ignore --no-index <path>`; do not silently change or commit `.gitignore`.

Resolve the destination and inspect its parent before creation. Stop if an existing path, unexpected symlink,
registered worktree, or branch collision makes ownership unclear.

Repositories with initialized submodules require extra care. Git documents multiple-checkout support for
submodules as incomplete. Stop and assess the repository's submodule workflow instead of treating a submodule
checkout as an ordinary worktree.

### Create the Lane

Create a new branch from an explicit base:

```bash
git worktree add -b <new-branch> <path> <start-point>
```

Check out an existing branch that is not active elsewhere:

```bash
git worktree add <path> <branch>
```

Use a detached worktree for disposable inspection or testing that should not move a branch:

```bash
git worktree add --detach <path> <start-point>
```

Do not use `-B` to reset an existing branch or `--force` to bypass Git's branch and path safeguards. Git
normally refuses to check out one branch in more than one worktree; treat that refusal as an ownership signal.

### Verify Isolation

After creation, verify both worktrees:

```bash
git worktree list --porcelain
git -C <path> rev-parse HEAD
git -C <path> branch --show-current
git -C <path> status --short
```

Require the expected start commit, branch or detached state, and a clean new index. Confirm that the original
worktree's `HEAD`, index, and status still match the recorded state.

### Understand Shared State

Worktrees isolate files, `HEAD`, and the index. They share the object database, ordinary refs, remote-tracking
refs, tags, common repository configuration, and `refs/stash`. Per-worktree configuration exists only when
the repository enables `extensions.worktreeConfig`. A commit created in one worktree becomes immediately
visible in the others, and a shared ref or configuration change can affect every lane.

Use `git rev-parse --git-path <name>` when locating Git administrative data; never build a path from `.git`
manually. Recheck shared refs before rebasing, resetting, deleting a branch, integrating, or pushing.

### Initialize and Establish a Baseline

A new worktree checks out tracked content. It does not inherit ignored or untracked local configuration,
credentials, build output, or dependencies from another worktree. Follow the repository's documented setup
and toolchain selection. Do not guess a package manager, install dependencies automatically, or copy secrets
from another checkout.

Check required local files without printing their contents. Run the cheapest relevant baseline validation and
record any failure that existed before the lane's changes.

### Finish and Remove Safely

Before integration or cleanup, inspect the lane and its commits:

```bash
git -C <path> status --short
git -C <path> diff
git -C <path> diff --cached
git log --oneline <integration-ref>..<worktree-branch>
```

Preserve required work in commits and confirm its integration or remote location when the task requires one.
A detached commit needs a branch or another durable ref before removing the worktree.

Leave the worktree's directory before removing it. Then use Git so it can verify cleanliness and update its
administrative state:

```bash
git worktree remove <path>
```

A refusal normally means the worktree contains changes or administrative protection. Inspect it. Do not
force removal, unlock a foreign worktree, or delete its branch unless the user explicitly authorized the
resolved loss. Branch deletion is a separate operation after removal and requires its own integration check.

### Maintain Registered Worktrees

Move a registered worktree with `git worktree move`. If its directory was moved outside Git, use
`git worktree repair` with the resolved path. Lock a long-lived worktree on removable or intermittently
mounted storage with `git worktree lock --reason <reason>`.

Preview stale administrative cleanup before applying it:

```bash
git worktree prune --dry-run --verbose
```

Pruning removes stale registration data. It does not recover or preserve files from a directory removed
outside Git.

## Harness-Managed Worktrees

Some agent harnesses create and manage their own worktrees, with their own location, branch naming, session
association, and cleanup checks. Those are client features rather than Git behavior, so read that client's
current documentation instead of inferring a lifecycle from this file. Before cleaning one up by hand, inspect
its status and run `git worktree list --porcelain`.

## Stashes

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
after a successful application. Treat conflicts as unresolved work and inspect them before continuing.

If the environment reserves stash deletion for the user, capture the entry's content and provide the exact
`git stash drop 'stash@{N}'` command rather than bypassing the control.

## Primary References

- [Git worktree](https://git-scm.com/docs/git-worktree)
- [Claude Code worktrees](https://code.claude.com/docs/en/worktrees) (Claude Code only)
