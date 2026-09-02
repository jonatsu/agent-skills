# Recovery

Load this when something has already gone wrong. For deciding whether an
operation is safe, use the ladder in
[history-changing-operations.md](history-changing-operations.md) instead.

- [First move, always](#first-move-always)
- [Commits missing after a reset, rebase or amend](#commits-missing-after-a-reset-rebase-or-amend)
- [A branch was deleted](#a-branch-was-deleted)
- [The commit recorded the wrong content](#the-commit-recorded-the-wrong-content)
- [Another lane's work got staged or committed](#another-lanes-work-got-staged-or-committed)
- [A generated artifact did not move](#a-generated-artifact-did-not-move)
- [Stash problems](#stash-problems)
- [Worktree problems](#worktree-problems)
- [Detached HEAD](#detached-head)
- [What has no recovery](#what-has-no-recovery)

## First Move, Always

STOP writing. Every additional command is another reflog entry between you and
the state you want, and a second bad guess can bury the first.

```bash
git reflog --date=iso | head -30
git status --short
git stash list
```

The reflog holds every position HEAD has occupied, and almost everything below is
a way of reading a hash out of it. HEAD's reflog is per-worktree; branch reflogs
live in the common directory.

**Check the clock before promising a recovery.** The
[history-changing operations reference](history-changing-operations.md) records
the reflog retention defaults. The operative one here is the 30-day default for
unreachable entries, which is what every case below depends on. Past that,
`git fsck --lost-found` is the remaining hope, and only until the next `git gc`.

MUST record the current hash before attempting any repair: `git rev-parse HEAD`.
A repair that goes wrong is recoverable only if you can name where you started.

## Commits Missing After a Reset, Rebase, or Amend

Try `ORIG_HEAD` first. A reset, rebase, or merge sets it to the position before
the operation:

```bash
git log ORIG_HEAD --oneline -10
git branch rescue/<name> ORIG_HEAD      # never reset straight onto it
```

**Do not assume it exists.** A cherry-pick sets no `ORIG_HEAD`, and after a
rebase `HEAD@{1}` is not the pre-rebase tip either, because a rebase writes
several reflog entries (both verified on git 2.43.0, 2026-08-26). When
`ORIG_HEAD` is absent or looks wrong, read `git reflog` and pick the hash by its
message.

Then **branch, do not reset.** A branch is additive and costs nothing if the hash
was wrong; a reset moves the very thing you are trying to save.

An amended commit's original is `HEAD@{1}` immediately after the amend, before
anything else moves HEAD. An operation still in progress is better abandoned than
repaired. Each has its own abort (`git rebase --abort`, `git merge --abort`,
`git cherry-pick --abort`), which restores the prior state exactly.

For a commit that is in no reflog because it was never on a branch you moved to,
`git fsck --lost-found` lists dangling objects. Read them with
`git show <hash>` before assuming which one is wanted.

## A Branch Was Deleted

`git branch -D` prints the hash it deleted. If that output is still on screen,
`git branch <name> <hash>` restores it exactly.

Otherwise the branch's own reflog is gone with it, so search HEAD's. However,
**grepping for the branch name finds the wrong commit**, and finds it
confidently. HEAD's reflog records commits as `commit: <message>`; the branch
name appears only on the `checkout: moving from/to <branch>` lines, and both of
those carry the **branch point**, not the tip. Verified on git 2.43.0,
2026-08-26: after deleting a two-commit branch, the grep returned only the branch
point and the true tip sat on an unmatched line.

```text
f2cb4d5 checkout: moving from wip/parser to main     <-- grep matches, WRONG hash
1aafd89 commit: test: cover the empty case           <-- the tip, unmatched
0e3ece0 commit: fix: handle empty input
f2cb4d5 checkout: moving from main to wip/parser     <-- grep matches, WRONG hash
```

Restoring from that hash gives an **empty** branch and reads as "the work was
never committed". So use the grep to locate the *region*, never the hash: find
the `checkout: moving from <branch>` line, then take the entry immediately
**above** it, which is the last position HEAD held while on that branch.

Prefer the reliable route and skip the grep entirely:

```bash
git fsck --lost-found          # dangling commit 1aafd89…; the tip, directly
git show <hash>                # confirm before restoring
git branch <name> <hash>
```

## The Commit Recorded the Wrong Content

First establish what it actually recorded, because the usual assumption is wrong
after a reset-based rebuild:

```bash
git show --stat HEAD
git cat-file -p HEAD^{tree}
```

If the tree still contains a file you deleted on disk, the index-not-worktree
rule in `SKILL.md` is why. Stage the intended state and amend:

```bash
git add -- <the paths you actually mean>
git commit --amend --no-edit
git show --stat HEAD
```

Amend only while the commit is unpushed and HEAD is yours. Confirm with
`git log -1 --format='%h %an %s'` first. If it is pushed, add a follow-up commit
instead.

## Another Lane's Work Was Staged or Committed

This is recoverable without touching anyone's files, because both commands below
move only the index and HEAD:

```bash
git log -1 --format='%h %an %s'          # confirm the commit is yours first
git reset --soft HEAD~1                  # undo the commit, keep everything staged
git restore --staged -- <foreign-path>   # unstage what is not yours
git commit -m "<your original message>"
git log --oneline -1 -- <foreign-path>   # their file's last commit is still theirs
```

The foreign file on disk is never touched by either step. Do NOT reach for a
worktree-level restore (`git restore <path>`, `git checkout -- <path>`) here because
that discards their working state, which is the one thing you are trying to
protect. Some environments block those two commands outright for this reason.

If the commit has been pushed, do not rewrite it. Revert the foreign paths in a
new commit and say what happened.

## A Generated Artifact Did Not Move

Confirm it by content or its own drift check, never by `git status` (the reason
is in [rewriting-hooks.md](rewriting-hooks.md)). Then regenerate it, and commit
the artifact ALONE by explicit path. A second `git add -A` here re-stages the
sibling lane's edit that caused the collision in the first place.

## Stash Problems

`git stash list` first, always. An entry you do not recognise probably belongs to
another lane, since the stash is repository-wide. Read it before touching it:

```bash
git stash show -p 'stash@{N}'
```

To recover content without consuming the entry, use `git stash apply` rather than
`pop`; `pop` drops the entry on success and leaves you with nothing to retry if
the merge was wrong.

Where `git stash drop` and `git stash clear` are blocked by the environment, save
the content as a patch and hand the user the exact command:

```bash
git stash show -p 'stash@{N}'    # capture the output to a file yourself
# then ask the user to run:  git stash drop 'stash@{N}'
```

A stash restored over a conflict is not automatically merged. Read the
conflicting files before continuing.

## Worktree Problems

**`pwd: error retrieving current directory`, or every command failing at once**:
the shell's cwd was removed, most likely by a worktree or scratch-directory
removal. The repository is fine. Recovery is a `cd` to a live directory, issued
from outside whatever tool holds the dead cwd.

**A worktree was removed with uncommitted content**: nothing recovers it. Its
committed history is still in the common object database. `git worktree list`
and the branch reflogs will show what the branch pointed at.

**`git worktree remove` refuses**: it is refusing because the tree is dirty. Read
what is there before forcing it; the refusal is the last thing standing between
that work and the case above.

**Stale administrative entries** after a directory was deleted by hand:
`git worktree prune`, which touches bookkeeping only.

## Detached HEAD

Not an error state, and nothing is lost while you are in it. To keep the work,
name it before moving:

```bash
git branch <name>          # from the detached position
git switch <name>
```

If you already moved away, the position is `HEAD@{1}` in the reflog.

## What Has No Recovery

Read the **None** rows of the ladder in
[history-changing-operations.md](history-changing-operations.md) rather than
trusting a copy here. Arriving here after one of those, the work is gone and the
only remaining question is what to say.

Report what was lost, how, and what would have caught it. Then STOP. Do NOT walk
the user through `fsck`, an editor's local history, or an IDE's backup directory
on the chance something turns up: a speculative recovery costs them time they do
not have and reads as though a real path exists. If a genuine long shot applies,
such as an editor retaining undo history or a branch being pushed before the
force-push, name it once, precisely, and say it is a long
shot.
