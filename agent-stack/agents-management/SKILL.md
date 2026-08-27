---
name: agents-management
description: "Author, audit and maintain a repository's agent instruction files — AGENTS.md, CLAUDE.md, .claude/rules, .github/copilot-instructions.md and llms.txt — populated from verified repo facts and kept consistent across Claude Code, OpenCode and Copilot CLI. Use when asked to add, create, write, generate, update, refresh, sync, audit, review, score, trim or fix an AGENTS.md or CLAUDE.md, to document a repo for coding agents or for LLMs, when project instructions are being ignored or have grown too large, or on mentions of agents.md, llmstxt.org, llms.txt, copilot-instructions, memory files or project memory. Keeps AGENTS.md and CLAUDE.md in sync by symlink. NOT for authoring subagent definitions under .claude/agents, NOT for capturing session learnings, which is the reflect skill, and NOT for authoring skills, which is skill-forge."
metadata:
  author: Joonas Onatsu
  license: Apache-2.0
---

# Agents Management

IRON LAW: NEVER write, score, or recommend anything not verified against THIS
repository. Every command, path and convention MUST be located in the repo
before it is documented. Every rubric point MUST cite the evidence that earned
it. A fact that cannot be verified is reported unverified — NEVER guessed, and
NEVER settled by reasoning about whether a documented command *would* still
work.

**Scope: repository-local files only.** `./AGENTS.md`, `./CLAUDE.md`,
`./CLAUDE.local.md`, `./.claude/rules/`, `./.github/copilot-instructions.md`,
`./.github/instructions/`, `./llms.txt`, and nested per-package files. User-level
and global configuration — a home-directory config tree, machine policy — is a
different job and MUST NOT be edited, scored, or reported on here.

**The test, when a tracked file blurs the two:** in scope if a first-class agent
would load it while working *in this repository*; out of scope if it is only a
payload this repo deploys somewhere else. A repo that stores another tool's
instruction file for deployment holds a build artifact, not its own instructions
— report it as out of scope in one line rather than auditing or ignoring it
silently.

**Universality is best-effort, not a guarantee.** Three agents are first-class
because their behavior has been checked: Claude Code, OpenCode, Copilot CLI.
Others get the portable fallback in `references/loading-model.md` and an honest
statement of what was not verified. NEVER block because an agent is unrecognized.

## The fact that drives every decision here

**One repository with divergent real `AGENTS.md` and `CLAUDE.md` files gives
three agents three different readings** — Claude Code sees only `CLAUDE.md`,
OpenCode sees only `AGENTS.md`, and Copilot CLI sees both combined in undefined
order. Making one of them a symlink to the other is the only configuration where
all three read the same text. That is why the symlink step in Phase 6 is
REQUIRED rather than cosmetic.

`references/loading-model.md` owns the full matrix, its per-cell provenance, and
what to re-check after an agent upgrade. Read it before Phase 1 — every phase
depends on it, and it is the file to correct when any of this changes.

**This skill writes, but only after approval.** It reports first, proposes
diffs second, edits third. NEVER edit an instruction file before the user has
approved that specific diff.

**An instruction file is context, never enforcement.** It ranks below the user's
turn and below whatever the harness enforces in code, and it cannot promote
itself. A rule that MUST hold every time needs a hook or a gate; the file's job
is then to explain that gate, so a refused command reads as policy rather than as
a malfunction. `references/update-guidelines.md` owns the failure modes — the
autonomy grant, the self-approval, the safety rule with nothing behind it, and
vendored or generated text cited as though this repository had adopted it.

## Workflow

```text
Agents Management Progress:

- [ ] Phase 1: Establish the loaded set ⛔ BLOCKING
- [ ] Phase 2: Read every file, includes followed ⚠️ REQUIRED
- [ ] Phase 3a: AUDIT — gather rubric evidence, or mark not assessed
      Phase 3b: AUTHOR — inspect the repo for verified facts
- [ ] Phase 4a: AUDIT — score and report ⚠️ REQUIRED before any edit
      Phase 4b: AUTHOR — confirm the plan ⚠️ REQUIRED
- [ ] Phase 5: Propose diffs → approval gate ⛔ BLOCKING
- [ ] Phase 6: Apply, reconcile the symlink, then llms.txt (conditional)
- [ ] Phase 7: Verify and deliver, flagged unknowns included
```

Phases 1, 2, 5, 6 and 7 run for both branches. Take 3a/4a when the ask is to
check, score, review or trim; take 3b/4b when it is to create, write, generate
or refresh.

## Phase 1: Establish the Loaded Set ⛔ BLOCKING

Ask first: **is a live session available to answer this directly?** Ground truth
beats a filesystem guess, and it differs per agent — `references/loading-model.md`
names the command for each, and records which agent has none. Say in the report
which method was used.

Otherwise reconstruct it, from the repository root only:

```bash
# Root instruction files
ls -la AGENTS.md CLAUDE.md CLAUDE.local.md 2>/dev/null
ls -la .github/copilot-instructions.md 2>/dev/null

# Rules and path-scoped instruction directories — recursive
find .claude/rules .github/instructions -name '*.md' -exec ls -ld {} + 2>/dev/null

# Nested per-package files. The prune list skips vendored and build output
# across common ecosystems; extend it for whatever this repo actually has.
# NEVER add -type f: it excludes symlinks, and a symlink is the single most
# important thing this phase has to find. `-exec ls -ld {} +` shows each link's
# target; it is POSIX and safe for paths containing spaces, which `-printf`
# (GNU-only) and a bare `| xargs` (splits on whitespace) are not.
find . \( -name AGENTS.md -o -name CLAUDE.md -o -name CLAUDE.local.md \) \
  -not -path '*/.git/*' -not -path '*/node_modules/*' -not -path '*/vendor/*' \
  -not -path '*/target/*' -not -path '*/dist/*' -not -path '*/build/*' \
  -not -path '*/.venv/*' -exec ls -ld {} + 2>/dev/null
```

Classify every file found as **launch-loaded**, **conditional** (a nested file,
loaded when the agent works in that directory), or **not loaded by any
first-class agent**. The three MUST NOT be scored as one pool.

**Record the link target of every symlink, not just that it is one.** A link
pointing outside its own directory changes what the file means — see Phase 6.

MUST NOT report a `find` result as "the instruction files". Report it as the
candidate set, and name which method established the loaded set.

## Phase 2: Read Every File, Includes Followed ⚠️ REQUIRED

Read each launch-loaded file, then follow its includes, recording the chain.
Include syntax and depth differ per agent, and one first-class agent does not
parse includes at all — `references/loading-model.md` has the matrix. Includes
resolve relative to the **including file**, not the working directory, and an
include inside backticks or a fenced block is not an include.

Record for each entrypoint: its own line count, its effective line count with
includes expanded, and the include tree. A short file with deep includes scores
completely differently from a short file.

MUST NOT score a file whose includes were not followed. An entrypoint whose
substance lives in included rule files grades near zero on almost every
criterion when read alone, which inverts the result on the most carefully built
repositories.

## Phase 3a: AUDIT — Gather Rubric Evidence

Each criterion in `references/scoring-rubric.md` names the evidence it needs.
Gather it, or mark the criterion `not assessed` — those are the only two options.

| Criterion | Evidence to gather |
|-----------|-------------------|
| Commands and workflows | The repo's task runner or manifest, whichever it actually has |
| Architecture orientation | The real directory tree, two levels deep |
| Currency | Existence checks on referenced paths; confirm documented commands still exist in the runner |
| Non-obvious knowledge, Density, Actionability | The file text plus includes — already gathered in Phase 2 |

Currency is where fabrication is easiest and costs most: a fabricated Currency
score certifies stale instructions as fresh. Either the check ran and its result
is citable, or the criterion is `not assessed`.

## Phase 3b: AUTHOR — Inspect the Repo

**Detect the ecosystem first — it decides everything that follows.** Look for a
manifest, a lockfile, a task runner, a CI workflow, a toolchain pin. Three
outcomes, three different obligations:

| What you find | What to do |
|---|---|
| **One clear ecosystem** | ADAPT to it. Name its actual manifest, its actual commands, its actual conventions. Generic advice where the repo has a real toolchain is a wasted file |
| **Several, or a manifest that disagrees with the code** | ⚠️ ASK which is authoritative before writing. Do NOT pick the one that looks primary |
| **None — an empty or greenfield repo** | ⚠️ ASK before introducing any. Write the sections that hold regardless, and leave the ecosystem-shaped ones out |

The last row is the one that matters most. A new repository has no ecosystem
yet, and an instruction file that invents one commits the project to a package
manager, a test runner and a layout nobody chose. NEVER write a command, a
manifest path, or a toolchain convention into a repo that has not adopted it —
ask, or omit the section.

Then gather only facts you can see:

- What are the real setup, build, test and run commands? Read them out of the
  runner or manifest the detection step found. NEVER invent a
  conventional-looking command, however standard it looks for that ecosystem.
- What language and toolchain, and which linters or formatters actually exist?
- What is the directory structure, and where do the real docs live?
- What conventions are evidenced — commit style from history, a contributing
  guide, an editorconfig? What agent gotchas exist — generated files, restart
  requirements, ordering dependencies?
- What does the README already cover? An instruction file MUST NOT duplicate it.
- Does the repo ship its own skills, and does it *require* one for some path or
  operation? Only the obligation is worth writing — when it must be loaded, for
  what. NEVER restate what a skill does: the agent already receives every
  discoverable skill's description, so a summary is a no-op. And name only
  skills the repository contains; one it merely benefits from is either already
  visible or not installed, and neither case is helped by naming it.

Apply the cache test to every candidate line before it earns a place. See
`references/update-guidelines.md`.

## Phase 4a: AUDIT — Score and Report ⚠️ REQUIRED before any edit

Apply `references/scoring-rubric.md`. Score at its anchors only, per file, never
averaged across files. Report shape:

> ## Instruction File Audit
>
> **Loaded set established via**: live session command | filesystem reconstruction
>
> | File | Real or symlink | Loading | Own / effective lines |
> |---|---|---|---|
> | `./AGENTS.md` | real | launch | 60 / 640 (3 includes) |
> | `./CLAUDE.md` | symlink to AGENTS.md | launch | — |
>
> ### `./AGENTS.md` — 62/80 assessed (78%, B)
>
> | Criterion | Score | Evidence |
> |---|---|---|
> | Commands and workflows | 15/20 | runner has 9 recipes; 3 documented |
> | Currency | not assessed | no runner found to check commands against |
>
> **Weakest link**: …
> **Findings**: [red flags from the rubric]

State the weakest link explicitly. A B built on a zero needs a different fix
from a flat B.

## Phase 4b: AUTHOR — Confirm the Plan ⚠️ REQUIRED

Present the files to write or change, the section list, the ecosystem the plan
assumes and the evidence for it, and every fact that could NOT be verified.
⚠️ Get approval before writing — especially before touching an existing file;
show a diff. Where Phase 3b found no ecosystem or more than one, the question
goes here and MUST be answered before writing, not resolved by picking a
default. See `references/templates.md` for section shapes and `assets/` for
starting points.

## Phase 5: Propose Diffs → Approval Gate ⛔ BLOCKING

⛔ **Load `references/update-guidelines.md` BEFORE writing the first proposal.**
Not "consult if useful" — it holds the two tests that decide whether a line
earns its place, and a proposal written without them is a guess. Proposing
first and reading after is the failure this marker exists to stop.

Every proposal MUST carry the file, the diff, and one line on why it helps a
future session. Prefer removal: the cost of a line is paid every session, so
cutting a derivable directory tree is usually worth more than adding a section.

When a proposal is really a mechanism change, say so instead of editing prose:

| Symptom | Proposal |
|---------|----------|
| Guidance applies to one file type or subtree | Keep it in a separate file and add an imperative pointer row in the main file naming the trigger |
| File is past the point it stops being read carefully — the repo's own budget, or commonly 150–200 effective lines | Extract to pointed-to files; note that includes reorganize without reducing cost on agents that parse them, and do nothing on agents that do not. NEVER extract guidance that must not fail to load |
| Instruction must hold every time | A hook or a CI gate — an instruction file is context, not enforcement |
| Enforcement already exists and the file never mentions it | Add the orientation. A hook or deny-list that refuses a command the agent had no reason to avoid reads as an unexplained failure. The inverse of the row above, and more common |
| Repo ships its own skills and requires one for a path or operation | State the OBLIGATION — when it must be loaded, for what. NEVER describe what the skill does; the agent already has its description. Offer this; do not insist |
| `AGENTS.md` and `CLAUDE.md` both real and divergent | Reconcile to one real file plus a symlink; see Phase 6 |
| Monorepo package guidance not reaching the agent | A file in the package directory, plus a pointer row in the root file |
| Maintainer note with no value to an agent | An HTML comment — stripped before injection on some agents, cheap on all |

Then STOP and ask. NEVER apply an unapproved diff.

## Phase 6: Apply, Reconcile the Symlink, Then llms.txt

Apply approved diffs, preserving surrounding structure. Then reconcile the pair
at the repository root:

| State | Action |
|---|---|
| `AGENTS.md` real, no `CLAUDE.md` | Create `CLAUDE.md` as a symlink to `AGENTS.md` |
| `CLAUDE.md` real, no `AGENTS.md` | Create `AGENTS.md` as a symlink to `CLAUDE.md` |
| Neither exists | Author `AGENTS.md` as the real file, then symlink `CLAUDE.md` to it |
| One real, one already a symlink to it | Correct — leave it alone |
| A symlink pointing OUTSIDE its own directory | Not the pair above. See "links to shared rules" below |
| Both real | ⛔ STOP and report, per the shape below. NEVER auto-resolve — one of them holds content the other does not |

**Reporting the both-real case.** "Report it" means give the user what they need
to decide, not a notification: which sections exist in only one file, a diff of
the sections present in both, which of the two each first-class agent currently
reads, and the three options — keep A and link B to it, keep B and link A to it,
or merge into one and link. NEVER recommend a winner on length or recency alone;
the shorter, older file is often the deliberate one.

```bash
ln -s AGENTS.md CLAUDE.md    # never with -f; a real file must never be clobbered
```

MUST NOT use `ln -sf` or overwrite a regular file. If the target exists, that is
the "both real" case above.

**Monorepos:** a root symlink does not reach package directories. Where per-
package instruction files exist, mirror the same symlink inside each package
directory, and add a pointer row for each in the root file. The symlink serves
agents that discover nested files; the pointer serves agents that do not.

**Links to shared rules.** A subdirectory may hold a symlink pointing *out* of
itself to a centralized rules file, with no sibling. The pair logic above does
not apply — there is no local real file to reconcile against — but the filename
still decides everything: a lone `AGENTS.md` in a subdirectory is invisible to
an agent that only looks for `CLAUDE.md` there, however good the rules file it
points to.

**Default: promote the content, do not link to it.** Move the file into the
directory that uses it as the real `AGENTS.md`, put the sibling symlink beside
it, and leave a pointer row in the root file:

```bash
git mv .claude/rules/thing.md pkg/AGENTS.md
ln -s AGENTS.md pkg/CLAUDE.md
```

⚠️ **A vendor-named directory is the wrong home for agent-agnostic content.**
`.claude/rules/`, and any equivalent named for one agent, binds text that serves
every agent to a single vendor's namespace, and makes every other agent reach it
only through a pointer. Promotion removes that dependency; linking preserves it.
Recommending the link is the same defect as writing an instruction file that
only one agent can find, which is the thing this skill exists to prevent.

Keep the file centralized **only** when it genuinely serves several directories,
and then link both names at the **same target** — never a link to a link:

```bash
ln -s ../shared/thing.md pkg/AGENTS.md
ln -s ../shared/thing.md pkg/CLAUDE.md
```

Even then, prefer a vendor-neutral directory over a vendor-named one, and say so
in the proposal rather than silently keeping the existing home.

Report this as a finding wherever the root file cites the subdirectory as though
it already provided coverage — a centralized rules file wired to the one
filename an agent never reads is worse than no file, because it reads as done.

**llms.txt** is written only when the user asked for it. It is a link index, not
an instruction file: an H1, an optional summary blockquote, optional detail
prose, then H2 sections of links, with an `Optional` section last for secondary
links. Every link MUST resolve. Start from `assets/llms.template.txt`.

## Phase 7: Verify and Deliver

Confirm: the instruction files agree with each other and with the repo; the
symlink resolves; nothing duplicates the README; no placeholder text survived;
every llms.txt link resolves.

Then run the preservation check — structure and score answer "does this file
have the right shape", never "is the knowledge still here". Use the repo's
version control if it has any; where it has none, diff against the copy taken
before editing:

**Check every path this run touched**, not a fixed pair — Phase 6 can edit rules
files, per-package files and `llms.txt` too, and a check hardcoded to the root
pair reports clean on all of them.

```bash
# Every path edited this run. Substitute the real list; do NOT leave the default.
CHANGED="AGENTS.md CLAUDE.md"

if command -v git >/dev/null && git rev-parse --git-dir >/dev/null 2>&1; then
  # 1. Confirm the check is looking at something. Empty here means the diff
  #    found nothing — which is NOT the same as "nothing was removed".
  git diff HEAD --stat -- $CHANGED

  # 2. Removed lines. HEAD covers staged AND unstaged. The trailing space in
  #    '^--- ' matters: a DELETED `---` renders as `----`, and a filter without
  #    the space swallows it — hiding frontmatter delimiters from the very
  #    check meant to catch deletions.
  git diff HEAD -- $CHANGED | grep -E '^-' | grep -vE '^--- '

  # 3. Files created this run are untracked; no diff can see them.
  git status --porcelain -- $CHANGED
else
  echo "no git checkout — diff each path against the copy taken before editing"
fi
```

⚠️ **An empty result from step 2 is only meaningful if step 1 showed changes.**
Empty output from both means the check examined nothing, which looks identical
to a pass and is the failure mode this phase exists to prevent. Say which of the
two you observed.

Any removed line that carried a convention, a gotcha, or a reason MUST be
restored or explicitly approved for removal. An update that deletes hard-won
knowledge to meet a line budget scores *higher* afterwards, which is exactly why
the score cannot be the check.

Finally, tell the user how to confirm the result in a live session — the command
differs per agent, and one first-class agent has none. Note that at least one
agent does not pick up instruction-file edits in an already-running session.

## References

One reference is unconditional; the rest load on symptom.

| Load when | File |
|---|---|
| **Always, before Phase 1** — which agent reads what, includes, nesting, ground-truth commands | `references/loading-model.md` |
| Scoring a file, or explaining a red flag | `references/scoring-rubric.md` |
| Deciding whether a line earns its place, or proposing a diff | `references/update-guidelines.md` |
| A file is missing structure and needs section shapes | `references/templates.md` |

Do NOT load `references/templates.md` when auditing — it describes shapes, not
quality, and an audit that reaches for it starts recommending sections instead
of citing evidence. Do NOT load `references/scoring-rubric.md` when authoring
from scratch — there is nothing to score yet.

## Anti-Patterns

- **Scoring what was never read.** Reasoning about whether a documented command
  would still work, instead of checking that it is still defined.
- **Reading the entrypoint and ignoring its includes.** Inverts the score.
- **Auto-resolving two real, divergent files.** One of them holds content the
  other does not, and whichever you overwrite is the one that mattered.
- **`ln -sf` at the repository root.** Silently destroys a real file.
- **Inventing conventional-looking commands** not present in the repo, or
  assuming an ecosystem — a package manager, a test runner — the repo has not
  shown you.
- **Committing an empty repository to an ecosystem it has not chosen.** A
  greenfield repo with no manifest gets the sections that hold regardless, and a
  question about the rest — never a plausible default toolchain written in as
  though it were a finding.
- **Writing generic advice into a repo that has a real toolchain.** The mirror
  failure: where an ecosystem is present, the file MUST name its actual
  manifest, commands and conventions.
- **Writing authority into the file** — an autonomy grant, an "always finish no
  matter what", a self-approval, or a safety rule with no hook or gate behind it.
  The last is the worst: it reads as a control, and a reviewer who sees it stops
  looking for the real one.
- **Citing vendored, generated or third-party text as a convention source.**
  Content a repository stores is not guidance the repository has adopted.
- **Recommending path-scoped instruction frontmatter.** Behavior differs per
  agent and is not verified everywhere; see `references/loading-model.md`.
- **Treating nested files as launch-loaded.** They are conditional on two
  first-class agents and invisible to a third without an explicit opt-in.
- **Averaging scores across files**, or reporting a total out of 100 when a
  criterion went unassessed.
- **Padding a file to raise its score.** Every added line is a recurring cost.
  If a section exists only to satisfy the rubric, say the rubric is wrong here.
- **Duplicating the README** into an instruction file — different jobs,
  different audiences.
- **Putting instructions in llms.txt**, or link dumps in an instruction file.
- **Editing before approval**, or bundling an unapproved change with an
  approved one.
- **Editing user-level or global configuration.** Out of scope; different job.

## Pre-Delivery Checklist

- [ ] The loaded set was established, and the method is named in the report
- [ ] Every file classified launch-loaded, conditional, or not loaded
- [ ] Includes followed; effective line counts reported
- [ ] Every command, path and convention was located in the repo
- [ ] Ecosystem detected: adapted to it where one exists, asked where none or
      several do, and nothing toolchain-shaped written into a repo without one
- [ ] Every score cites its evidence; unbacked criteria say `not assessed`
- [ ] Total reported as earned over assessed, per file, never averaged
- [ ] Red flags reported even where the score is high
- [ ] No authority claimed the file cannot hold; no safety rule standing in for
      a hook or a gate; no vendored or generated text cited as a convention
- [ ] `AGENTS.md` and `CLAUDE.md` reconciled, or the both-real case reported
- [ ] Symlink created without `-f`, and it resolves
- [ ] Preservation check run; no knowledge silently dropped
- [ ] No placeholder text remains
- [ ] No file edited without an approved diff
- [ ] The user was told how to verify in a live session, and where none exists
