# History-Changing and Remote Operations

Resolve the operation's actual risk before selecting commands.

## Establish the Consequential State

Inspect only the facts the operation needs:

- `git status -sb` for branch and worktree state;
- `git diff --cached --name-only` and the relevant diffs for affected content;
- `git log -1 --format='%h %an %s'` before amending, resetting, or rebasing, to confirm `HEAD` is the intended
  commit;
- remote names from `git remote` and the configured upstream before pushing; and
- `git rev-parse HEAD` before an operation that can move or orphan commits.

Name the recovery path before a destructive or history-rewriting operation. When no recovery exists, proceed
only when the user explicitly authorized the resolved action and target. A general request to "clean up" or
"sort out the branch" does not authorize deletion, overwriting uncommitted work, or rewriting published
history.

## Reversibility

| Operation                                 | Recovery                        | Cost           |
| ----------------------------------------- | ------------------------------- | -------------- |
| Amend or local branch move                | Reflog                          | Cheap          |
| `git reset --soft` or `--mixed`           | Reflog; worktree remains        | Cheap          |
| Rebase                                    | Abort; otherwise `ORIG_HEAD`    | Cheap          |
| Merge                                     | Abort; otherwise `ORIG_HEAD`    | Conditional    |
| Cherry-pick                               | Abort; otherwise reflog         | Cheap          |
| `git branch -D`                           | Reflog while commit is retained | Partial        |
| `git reset --hard` with a dirty tree      | Reflog for commits              | None for edits |
| `git restore` or `git checkout -- <path>` | None for overwritten edits      | None           |
| Force-push over work never fetched        | Nothing under local control     | None           |
| `git worktree remove --force` (dirty)     | None for uncommitted content    | None           |
| `git clean -f`, `-fd`, or `-fdx`          | None                            | None           |

Each active operation has its own abort; run it before anything else. [recovery.md](recovery.md) covers
reading `ORIG_HEAD` and the reflog once an operation has completed.

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
- Treat deletion of a branch with unmerged work as destructive. Worktree removal belongs to the
  `using-git-worktrees` skill.
- Rewriting published history requires explicit authorization and a resolved target branch. Protected and
  shared branches require the user to decide how collaborators will be affected.

## Pushing

Determine what will leave and where it will go. List remote names with `git remote`. Remote URLs can contain
embedded credentials, so retrieve a URL only when required and never print or report it without redacting
user information.

When an upstream is configured, inspect its outgoing range:

```bash
git log @{upstream}..HEAD --oneline
```

Resolve and inspect a configured push ref separately because it can differ from the upstream:

```bash
git rev-parse --abbrev-ref --symbolic-full-name @{push}
git log @{push}..HEAD --oneline
```

An absent upstream or push ref is ordinary. Resolve the push remote from `branch.<name>.pushRemote`,
`remote.pushDefault`, the branch's upstream remote, or an unambiguous single remote, in that order. Do not
assume `origin`. If several remotes remain plausible, stop for the missing choice.

Resolve the destination branch explicitly. If it already exists, fetch that branch and compare the exact
remote tip with `HEAD`:

```bash
git ls-remote --exit-code --heads <remote> refs/heads/<branch>
git fetch --no-tags <remote> refs/heads/<branch>
git log FETCH_HEAD..HEAD --oneline
git push --dry-run --porcelain <remote> HEAD:refs/heads/<branch>
```

If the destination does not exist, use the remote default branch only to establish the new branch's base.
Push with an explicit destination after inspecting the outgoing commits:

```bash
git push -u <remote> HEAD:refs/heads/<branch>
```

Stop when the outgoing range or dry-run mapping contains unexpected commits or refs.

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
