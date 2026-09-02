# History-Changing and Remote Operations

Use this reference for operations that move existing refs, rewrite history, discard work, or change a remote.
Resolve the operation's actual risk before selecting commands.

## Establish the Consequential State

Inspect only the facts the operation needs:

- `git status -sb` for branch and worktree state;
- `git diff --cached --name-only` and the relevant diffs for affected content;
- `git log -1 --format='%h %an %s'` before amending, resetting, or rebasing, to confirm `HEAD` is the intended
  commit;
- `git remote -v` and the configured upstream before pushing; and
- `git rev-parse HEAD` before an operation that can move or orphan commits.

Name the recovery path before a destructive or history-rewriting operation. When no recovery exists, proceed
only when the user explicitly authorized the resolved action and target. A general request to "clean up" or
"sort out the branch" does not authorize deletion, overwriting uncommitted work, or rewriting published
history.

## Reversibility

| Operation                                        | Recovery                                                 | Cost           |
| ------------------------------------------------ | -------------------------------------------------------- | -------------- |
| Amend or local branch move                       | Reflog                                                   | Cheap          |
| `git reset --soft` or `--mixed`                  | Reflog; the worktree remains                             | Cheap          |
| Rebase                                           | `git rebase --abort` while active; otherwise `ORIG_HEAD` | Cheap          |
| Merge                                            | `git merge --abort` while active; otherwise `ORIG_HEAD`  | Cheap          |
| Cherry-pick                                      | `git cherry-pick --abort` while active; otherwise reflog | Cheap          |
| `git branch -D`                                  | Reflog while the commit remains retained                 | Partial        |
| `git reset --hard` with a dirty tree             | Reflog for commits; none for uncommitted edits           | None for edits |
| `git restore <path>` or `git checkout -- <path>` | None for overwritten edits                               | None           |
| Force-push over work never fetched               | Nothing under local control                              | None           |
| `git worktree remove --force` on a dirty tree    | None for uncommitted content                             | None           |
| `git clean -f`, `-fd`, or `-fdx`                 | None                                                     | None           |

Each active operation has its own abort. A rebase and merge set `ORIG_HEAD`; a cherry-pick does not. After a
rebase, `HEAD@{1}` is not reliably the pre-rebase tip because the operation writes several reflog entries.
Verified on git 2.43.0, 2026-08-26.

Reachable reflog entries default to a 90-day expiry. Unreachable entries, which hold commits orphaned by an
amend, reset, or branch move, default to 30 days. These are configuration defaults, not recovery guarantees.
Verified against `git help config` on git 2.43.0, 2026-08-26.

## Destructive Operations

Resolve and show the affected state before acting. Reuse an explicit request that already names the
destructive action and target; otherwise ask for authorization.

- Preview `git clean -fd` with `git clean -nd`, and `git clean -fdx` with `git clean -ndx`. The narrower
  preview omits ignored files that the wider operation deletes. Verified on git 2.43.0, 2026-08-26.
- Before overwriting work with `git reset --hard`, `git restore <path>`, or `git checkout -- <path>`, show
  `git status --short` and the relevant diff.
- Treat `git worktree remove --force` and deletion of a branch with unmerged work as destructive. A plain
  worktree removal refusal is evidence of content to inspect, not an obstacle to bypass.
- Rewriting published history requires explicit authorization and a resolved target branch. Protected and
  shared branches require the user to decide how collaborators will be affected.

## Pushing

Determine what will leave and where it will go:

```bash
git log @{upstream}..HEAD --oneline
git remote -v
```

An absent upstream is ordinary. Select a remote from repository configuration and context; do not assume
`origin`. If one remote is configured and its default branch is recorded, inspect it with:

```bash
git symbolic-ref --short refs/remotes/<remote>/HEAD
git log refs/remotes/<remote>/HEAD..HEAD --oneline
git push -u <remote> HEAD
```

If several remotes are plausible or the default ref is unavailable, stop for the missing choice. Also stop
when the outgoing range contains unexpected commits.

For an authorized force-push on Git 2.30 or newer, use `--force-with-lease --force-if-includes`. A background
fetch can refresh the remote-tracking ref and weaken a lease used alone; `--force-if-includes` checks that the
updated remote tip was integrated locally. Verified on git 2.43.0, 2026-08-26.

If the installed Git lacks `--force-if-includes`, report that the required protection is unavailable. Do not
silently fall back to a plain force or a lease alone.

Validate command substitutions before using them in refspecs. An empty source in `"${sha}:refs/tags/v1.0"`
becomes a tag deletion. Verified on git 2.43.0, 2026-08-26.

## Rewriting History

Before rewriting, confirm that the branch is not protected, published-history authorization is sufficient,
dirty state is accounted for, and the original `HEAD` hash is recorded.

- For fixups, use `git commit --fixup=<hash>` followed by an autosquash rebase from the correct base.
- Resolve conflicts from the intended content. Whole-file `--ours` or `--theirs` usually answers which side
  wins rather than what the merged result should mean.
- Abort an incorrect active operation with its own abort command before attempting recovery.
- Compare a completed rebase with `git range-diff <old-base>..<old-tip> <new-base>..<new-tip>`.
- Revert published work instead of rewriting it unless the user explicitly authorized the rewrite. Reverting a
  merge needs the intended mainline parent; reverting that revert is normally required before re-merging the
  same change.
- Do not use ancestry alone to decide whether a branch was squash-merged. Compare content or consult the
  hosting service.

A rebase of a branch whose tip is a merge commit can reportedly collapse the branch to its base when its
unique content exists only in the merge resolution. This claim is *reported, not measured here*. Confirm the
branch has unique commits or content before and after the rebase.
