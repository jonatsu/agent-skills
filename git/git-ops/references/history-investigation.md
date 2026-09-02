# History Investigation

Load this when the question is who changed something, when it changed, or which commit broke it. All of it is
read-only.

This file deliberately does NOT restate flags or command syntax: `git help log`, `git help blame` and
`git help bisect` are reachable and correct whenever a history question is being asked, and a copy here would
drift. What follows is what those pages do not tell you.

## Pick the Cheapest Tool That Can Answer It

| The question                                    | Reach for      |
| ----------------------------------------------- | -------------- |
| When did this exact string appear or disappear? | `git log -S`   |
| Which commits touched lines matching a pattern? | `git log -G`   |
| Who last changed these lines?                   | `git blame -L` |
| What did this commit actually do?               | `git show`     |
| Which commit first broke a deterministic check? | `git bisect`   |
| Where has my local HEAD been?                   | `git reflog`   |

Order matters: `bisect` costs one build or test run per step, and `log -S` frequently answers the same
question in one command. Reach for `bisect` when you have a deterministic check and no idea where to look, not
as a first move.

## The Pickaxe Silently Misses a Pure Rename

`-S` counts occurrences **per file pair**, so a commit that only moves code changes no count anywhere and does
not match. Measured on git 2.43.0, 2026-08-26, on a commit that moved `loadConfig` from `a.c` to `b.c`:

| Command                                 | Finds the move commit? |
| --------------------------------------- | ---------------------- |
| `git log -S "loadConfig"`               | **No**                 |
| `git log -S "loadConfig" --pickaxe-all` | **No**                 |
| `git log -S "loadConfig" --no-renames`  | **Yes**                |

The default rename detection records the change as `R100 a.c b.c`, one pair with no content change.
`--no-renames` splits it into `D a.c` + `A b.c`, two pairs that each change a count, and the pickaxe then
matches.

**`--pickaxe-all` is not the fix**, and reaching for it here is the common mistake: it changes only which
files are *displayed* for a commit that already matched, never whether it matches. In the same measurement it
widened the file list from `a.c` to `a.c main.c` and left the matched commits identical.

So when `-S` finds an introduction but no removal, suspect a move before concluding the code is still live,
then re-run with `--no-renames`.

`-G` is the wider net: it matches any diff *line* matching the regex, added or removed, so it catches
reformatting and movement that `-S` skips, at the cost of noise.

## Treat an Empty Result as a Broken Query First

Before reporting that something never existed, prove the query works by running it against a string you know
is present. Pathspec typos, a wrong branch, and a literal-vs-regex mix-up all produce a confident empty
result.

## Treat a Positive Text Result as a Coincidence First

`git log --grep` searches prose written by people and bots, and is the weakest evidence available. An issue or
PR number in a message routinely belongs to a different repository because dependency-bump commits embed
upstream changelogs wholesale, upstream issue numbers included. Confirm with content evidence before treating
a message match as proof.

## Blame Points at the Last Edit

A reformat, a rename sweep or a whitespace fix rewrites every line's attribution, so blame's answer is often
about noise. `-w`, `-C` and `-M` reduce it. The technique that actually gets through: once a commit is
identified as noise, re-run blame from just before it with `git blame <hash>~1 -L …`, then repeat. Blame
yields a hash; the answer is usually in `git show <hash>`.

## Bisect Is Only as Good as Its Check

A flaky test makes `git bisect` report a random commit with complete confidence, and nothing in the output
reveals it. Confirm the check is deterministic by running it twice on the known-bad commit before starting.
Mark untestable commits skipped rather than guessing at good or bad, and always reset the session when
finished. An abandoned bisect leaves the repository on an arbitrary detached commit that will be mistaken for
a real state later.

Bisect finds where the check *started failing*, which is not always where the defect was introduced: a latent
bug can be exposed by an unrelated change.

## Reporting

MUST cite the command and its output. A history answer without a hash is an assertion, not a finding. Include
the command, the hash and subject, the path, and the diff or line context supporting the claim.

Where several commits touch the same lines, or blame lands on a reformat, say what remains unproven instead of
naming the most plausible commit. Where the conclusion rests on a name-matched text search rather than a
reference-resolving tool, say that too. A claim of "no other callers" from a text search misses dynamic
dispatch, names built from strings, and callers in languages the search never covered.
