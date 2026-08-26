---
name: git-operations
description: "Perform Git operations safely and recover when they go wrong — staging, committing, pushing, rebasing, worktrees, stashes and history investigation. Use when a commit landed the wrong content, a rebase collapsed a branch, work vanished after a reset, stash or clean, a hook rewrote files during a commit, or another session's changes got staged; before any force-push, reset, clean, rebase of pushed work, worktree removal or branch deletion; and for 'who changed this', 'when was this added', 'which commit broke it'. Triggers: force-push, rebase, squash, fixup, autosquash, cherry-pick, reset, revert, stash, worktree, reflog, bisect, blame, git log -S, merge conflict, detached HEAD, lost commits, undo a commit, recover deleted work, git clean. NOT for repository scaffolding, hygiene files or secret scanning, which is git-repo-hygiene."
metadata:
  author: Joonas Onatsu
  license: MIT
---

# Git Operations

IRON LAW: NAME THE RECOVERY PATH BEFORE THE WRITE. Say which command brings the
state back before running the one that changes it. If the honest answer is
"nothing does", that is not a caveat to mention — it is a STOP, and the user
decides.

This is not a phased workflow: there is no order to work through, and the
sections are independent. They are decisions, arranged by how much damage
getting each one wrong does. Read the one for the operation in hand. The single
checklist, at the end, is a hand-back gate rather than a procedure — it applies
whichever section you used.

## Before any write: four facts

Each is cheap, and each has a trap that makes guessing worse than asking.

1. **Which branch, and who else is on it?** `git branch --show-current`. A shared
   or protected branch turns every rewrite into someone else's problem.
2. **Is this work already pushed?** `git status -sb` and
   `git rev-parse --abbrev-ref @{upstream}`. An absent upstream, or a repository
   with no `main`, is an ordinary state — report the gap, and NEVER reason from a
   lookup that failed as though it had returned "no".
3. **Whose dirty state is this?** Assume another session, agent or worktree is
   editing this checkout unless you have evidence otherwise: assuming wrongly
   costs a few checks, not assuming costs landing their work under your name.
   Tells, any one sufficient — files you did not create; a commit you did not
   write, dated inside your session; an mtime newer than your last read; a hook
   reporting it modified files.
4. **What recovers this?** The ladder below. When the answer is the reflog, write
   the hash down first: `git rev-parse HEAD`.

## The reversibility ladder

MUST classify the operation before running it. The recovery column is the point
of the table.

| Operation | What recovers it | Cost |
|---|---|---|
| Commit, amend, local branch move | Reflog | Cheap |
| `git reset --soft` / `--mixed` | Reflog; the worktree was never touched | Cheap |
| `git rebase` | `git rebase --abort` mid-flight, else `ORIG_HEAD` | Cheap |
| `git merge` | `git merge --abort` mid-flight, else `ORIG_HEAD` | Cheap |
| `git cherry-pick` | `git cherry-pick --abort` mid-flight, else the reflog — **no `ORIG_HEAD`** | Cheap |
| `git branch -D` | Reflog, while you still have the hash | Partial |
| `git stash` | `git stash list` — but it is shared, see below | Partial |
| `git reset --hard` with a dirty tree | Reflog for the **commits**; uncommitted edits are GONE | **None** for the edits |
| `git restore <path>` / `git checkout -- <path>` | Nothing. Overwrites the file from the index | **None** |
| `git push --force` over work you never fetched | Nothing you control | **None** |
| `git worktree remove --force` on a dirty tree | Nothing | **None** |
| `git clean -f` / `-fd` / `-fdx` | **Nothing.** No reflog, no index, no object | **None** |

**Each in-progress operation has its OWN abort; they are not interchangeable.**
Verified on git 2.43.0, 2026-08-26: `git rebase --abort` during a conflicted
cherry-pick or merge exits `fatal: No rebase in progress?` and changes nothing.
In the same run, a real rebase and a merge each set `ORIG_HEAD` to the position
before the operation, while a cherry-pick set none — and after a rebase
`HEAD@{1}` is *not* the pre-rebase tip, because a rebase writes several reflog
entries. For a rebase or merge, `ORIG_HEAD` is the reliable handle.

**Reflog retention is shorter than the number usually quoted.** Entries still
reachable from a branch tip expire at `gc.reflogExpire`, 90 days; the entries
that matter for recovery — commits orphaned by an amend, reset or branch move —
expire at `gc.reflogExpireUnreachable`, which defaults to **30 days**. Verified
against `git help config`, git 2.43.0, 2026-08-26.

`git clean` is the one everyday command with no undo at all: untracked files were
never in the object database, so nothing holds a copy.

## ⛔ Confirmation gates

MUST stop and ask. Do NOT read approval into a general instruction to "clean this
up" or "sort the branch out".

- **Any `git clean` that is not a dry run**, and **the preview MUST carry the
  same flags as the operation**. `-nd` does not preview what `-fdx` deletes: it
  omits every ignored path, which is where `.venv/`, `node_modules/`, `.env` and
  build caches live. Verified on git 2.43.0, 2026-08-26 — in a tree with three
  removable paths, `git clean -nd` listed one and `git clean -ndx` listed all
  three. So preview `-fd` with `-nd`, and `-fdx` with `-ndx`, and show the user
  the list.
- **`git push --force`.** Use `--force-with-lease --force-if-includes`, never
  the lease alone — see Pushing for why the lease is not the protection it looks
  like. Even then, ask when the branch is shared.
- **Any command that overwrites uncommitted work from the index or a commit** —
  `git reset --hard` on a dirty tree, `git restore <path>`, `git checkout --
  <path>`. These destroy exactly what `clean` does and get treated as though
  they were routine because they are spelled like navigation. Show the user
  `git status --short` and `git diff --stat` first, so what is about to go is
  named before it goes.
- **`git worktree remove --force`, or deleting a branch holding unmerged work.**
  Plain `git worktree remove` refuses a dirty tree (`fatal: contains modified or
  untracked files`) — that refusal is a safety feature, so treat reaching for
  `--force` as the gate, not the fix.
- **Rewriting anything already pushed**, and anything at all on `main`,
  `master`, `dev`, a release branch, or a protected branch.

## Staging and committing

**Stage by explicit path.** `git add -A`, `git add .` and `git commit -a` stage
whatever is dirty, which under a live sibling lane is someone else's work —
landed under your message, and clean in `git status` afterwards, leaving the
"N files changed" count as the only surviving clue. If you did not make the
change this session it is not yours to land, however obviously correct it is.

**A dirty index you did not create is a STOP.** Check
`git diff --cached --name-only` before staging. Reconcile or wait; NEVER stage on
top.

**Find the repo's commit convention before writing a message; default only when
there is none.** In this order:

1. **A documented convention wins.** `CONTRIBUTING.md`, `AGENTS.md`/`CLAUDE.md`,
   a `commitlint`/`commitizen`/`gitlint` config, a `commit-msg` hook, or a
   `commit.template`. A written rule outranks whatever the history drifted into.
2. **Otherwise infer it from the history**: `git log --oneline -30`. A consistent
   shape there is the convention, even undocumented.
3. **Only when neither exists, default to Conventional Commits** —
   `<type>(<scope>): <imperative summary>`, subject about 50 characters and hard
   capped at 72, body wrapped near 72 and present only when the *why* is not
   obvious.

MUST NOT retrofit Conventional Commits onto a repo whose history or docs show
another convention. The default is for a silent repo, not an argument for
converting a noisy one.

**NEVER use `--no-verify`**, and NEVER move a command into a script to escape a
hook. A hook in the way is a finding to report.

**Verify what the commit recorded** — `git show --stat HEAD`. This matters most
after a reset-based rebuild, where the intuitive check is the wrong one:

> **A commit records the INDEX, not the worktree.** After `git reset --soft
> <base>`, editing or deleting files on disk changes nothing about what the next
> `git commit` writes. Verified on git 2.43.0, 2026-08-26: a `--soft` reset
> followed by `rm junk.txt` and `git commit` produced a commit still containing
> `junk.txt`, with the file absent from the worktree.

## Hooks that rewrite files during a commit

**This section describes `pre-commit` (the framework) specifically**, and only
when its hook is actually installed. A `.pre-commit-config.yaml` at the root
proves nothing: without `pre-commit install` the config is inert, the commit
succeeds, and no stash, rollback or rewrite ever happens. Test the installed hook
instead, honouring a redirected hooks directory:

```bash
grep -q "pre-commit" "$(git rev-parse --git-path hooks/pre-commit)"
```

Verified on git 2.43.0, 2026-08-26: `--git-path` honours `core.hooksPath` and
resolves correctly from inside a linked worktree (both as absolute paths). In a
plain clone it returns a path relative to the **current directory** —
`../../.git/hooks/pre-commit` from two levels down — which reads fine where it
was produced, and breaks if you store the string and use it from elsewhere.

Under `husky`, `lefthook` or bare `.git/hooks` scripts none of the following
applies, because those runners do not stash — there the hook runs against your
dirty tree and its rewrite survives or fails on its own terms.

pre-commit stashes unrelated unstaged work for the run. When a rewriting hook's
output collides with that stash on restore, the fix is thrown away:

```text
[WARNING] Stashed changes conflicted with hook auto-fixes... Rolling back fixes...
```

**What happens next depends entirely on the hook's stage.** Verified on git
2.43.0 with pre-commit 4.6.2, 2026-08-26:

- **pre-commit stage** — the hook reports `files were modified by this hook`, the
  commit **ABORTS** (exit 1), nothing is lost. Loud, and harmless.
- **post-commit stage** — the commit object already exists, so it **SUCCEEDS**
  (exit 0) while the rollback discards the rewrite. HEAD then carries a stale
  generated artifact and nothing in the output says so.

After committing into a dirty tree in a repo with a post-commit rewriting hook,
MUST verify the artifact by its **content**, or by whatever drift check it has of
its own. `git status` is not the test: in the measured run it showed the artifact
modified, but indistinguishably from the sibling lane's edit that caused the
collision — which is why it prompts no follow-up.

## Pushing

Two questions, and neither is answered by `git status`: what is about to leave,
and where is it going?

```bash
git log @{upstream}..HEAD --oneline     # exactly what leaves
git remote -v                           # where it lands
```

`@{upstream}` FAILS on a branch that has never been pushed —
`fatal: no upstream configured`, which is the commonest push there is. Fall back
to the remote branch by name (`git log origin/main..HEAD --oneline`), and set
the upstream as you push: `git push -u origin HEAD`.

Stop if that list contains commits you did not write, if the remote is not the
one you expected, or if the target branch is ambiguous.

**`--force-with-lease` alone is not the protection it appears to be.** It
compares against your remote-tracking ref, so ANY background fetch — an editor's
autofetch, a `git pull` in a sibling lane, another agent — refreshes that ref and
silently downgrades the lease to a plain `--force`. Verified on git 2.43.0,
2026-08-26:

| Step | Result |
|---|---|
| `push --force-with-lease`, tracking ref stale | `! [rejected] main -> main (stale info)` — protection works |
| a bare `git fetch` happens; **same command, no local change** | `+ 4dcae6b...52a6f8b main -> main (forced update)` — the colleague's commit is destroyed |
| same scenario with `--force-if-includes` | `! [rejected] main -> main (remote ref updated since checkout)` — work preserved |

So MUST pass `--force-with-lease --force-if-includes` together (git ≥ 2.30).
`--force-if-includes` checks that the remote tip you are about to overwrite was
actually integrated into your local history, which is the question the lease was
supposed to be asking.

**A refspec built from a command substitution MUST be checked for emptiness
before use.** `set -e` does not catch a command that exits 0 with no output, and
`git push origin "${sha}:refs/tags/v1.0"` with `sha` empty becomes
`:refs/tags/v1.0` — a **tag deletion**. Verified on git 2.43.0, 2026-08-26: the
remote went from one tag to zero, reported as `- [deleted] v1.0`.

## Rewriting history

Four preconditions, all of them, before starting: the branch is not protected;
the work is unpushed or a force is approved; the dirty tree is accounted for; and
`git rev-parse HEAD` is written down.

- For fixups: `git commit --fixup=<hash>`, then
  `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash <base>`.
- **A conflict is a question about intent, so open the file and answer it.**
  `--ours` and `--theirs` applied wholesale answer a different question — which
  side wins — and that is rarely the one being asked.
- **`git rebase --abort` is the first move when a rebase goes wrong, not the last
  resort.** It restores the pre-rebase state exactly. The reflog is for after you
  have already left the rebase.
- **Prove the rewrite preserved what it should**, with
  `git range-diff <old-base>..<old-tip> <new-base>..<new-tip>`, which compares the
  two versions commit by commit and shows what changed *about the changes*. A log
  listing shows only that commits exist.

**Once work is pushed, `git revert` is the undo, not a rewrite.** It adds a
commit that reverses the change, so nobody's clone breaks and the record of both
the change and its withdrawal survives. Reverting a merge commit needs `-m` to
say which parent is mainline, and the revert itself then blocks a later re-merge
of that branch — re-apply by reverting the revert rather than re-merging.

**"Is this branch merged?" is not an ancestry question.** A squash merge writes
one new commit, so none of the branch's own hashes appear in the target and
`git merge-base --is-ancestor` reports "not merged" about work that shipped weeks
ago. Compare content, or ask the hosting side.

**A branch whose tip is a merge commit can be collapsed to nothing by a rebase**,
when its unique content lives inside the merge resolution — the branch becomes
equal to base and the content survives only in the reflog. *Reported upstream,
not measured here.* Cheap either way: check `git log --oneline base..branch` is
non-empty before and after.

## Worktrees and stashes

**A stash belongs to the repository, not to your worktree.** `refs/stash` lives
in the common Git directory — compare `git rev-parse --git-common-dir` with
`--git-dir` to see it. So a stash created in one lane appears in every other, and
a background agent's stash can revert a sibling worktree. Prefer a WIP commit on
a branch: per-worktree, visible in history, reversible.

**To set aside part of a dirty tree, stash by pathspec**:
`git stash push -u -m "<why>" -- <paths>`. A bare `git stash` takes everything,
including the work you meant to keep. Where the environment blocks `git stash
drop` and `git stash clear`, capture the content as a patch
(`git stash show -p 'stash@{N}'`) and hand the user the exact drop command rather
than leaving behind a stash nobody can remove.

**Leave a worktree before removing it.** Removing the directory your shell's cwd
sits in leaves the repository fine and the shell in a ghost directory; the
symptom (`pwd: error retrieving current directory`) appears several commands
later and reads like a corrupted repo.

**A linked worktree's `.git` is a FILE**, holding a `gitdir:` pointer rather than
being a directory. A bulk `sed`, `grep` or codemod guarded with
`--exclude-dir=.git` does NOT skip it. Verified on git 2.43.0 with GNU grep,
2026-08-26: `grep -rl gitdir wt --exclude-dir=.git` matched `wt/.git`, while the
same guard correctly skipped a real `.git` directory. Scope rewriting commands to
an explicit file list.

## Signed commits

**Do NOT read `%G?` as the answer under SSH signing.** With `gpg.format=ssh` and
no `gpg.ssh.allowedSignersFile` configured, a correctly signed commit reports
`%G?` = `N` and `--show-signature` prints `No signature`. Verified on git 2.43.0,
2026-08-26; git does emit `error: gpg.ssh.allowedSignersFile needs to be
configured` on stderr, so it is misleading rather than silent.

Two different questions, two different answers:

- *Is this signature valid?* — then **configure `gpg.ssh.allowedSignersFile`**.
  That is the fix; verification works normally afterwards. Do not build a
  workaround around a one-line misconfiguration.
- *Does this commit carry a signature at all?* — read the object header, cutting
  at the first blank line so a body line beginning `gpgsig` cannot impersonate
  one:

  ```bash
  git cat-file commit <hash> | sed -n '/^$/q;p' | grep -qE '^gpgsig(-sha256)? '
  ```

  The `sed` stops at the header/body boundary; without it the `grep` searches the
  message too, which is the whole spoof.

## Investigation and recovery

Read `references/history-investigation.md` when the question is who changed
something, when it changed, or which commit broke it.

Read `references/recovery.md` when work has already been lost or a write went
wrong: commits missing after a reset or rebase, a deleted branch, a commit
holding the wrong content, another lane's work staged or committed, a stash that
cannot be dropped.

**Do NOT load either** for an ordinary commit, push or status check, or to decide
whether an operation is safe — that decision is the ladder above, and loading a
recovery procedure in order to avoid needing one wastes the context it exists to
save.

## Anti-patterns

NEVER:

- Run a destructive command before naming what recovers it — the whole skill
  reduces to this one.
- Preview a `clean` with flags narrower than the ones you intend to run; the
  ignored paths it hides are the expensive ones.
- Use plain `--force`, or `--force-with-lease` without `--force-if-includes` —
  a background fetch turns the bare lease back into a plain force.
- Abort one in-progress operation with another's abort command; `git rebase
  --abort` does nothing during a cherry-pick or a merge.
- Use `--no-verify`, or relocate a command to dodge a hook.
- Stage with `git add -A`/`.`/`commit -a` when another lane may be live, or
  commit on top of an index you did not stage.
- Reason from a failed lookup as though it were a negative answer.
- Amend, reset or rebase without confirming HEAD is yours:
  `git log -1 --format='%h %an %s'`.
- Report a commit as done from the commit command's exit status alone when a
  rewriting hook was involved.
- Answer a history question without the command and hash that prove it.

## Before reporting done

- The operation performed is the one requested, and nothing more.
- What the commit recorded was checked against the diff, not inferred from an
  exit status.
- Any generated artifact a hook should have rewritten was checked by content.
- Remaining dirty state is stated explicitly, including whose it appears to be.
- Anything left unrun or unverifiable is named as such.
