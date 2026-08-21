---
name: claude-md-auditor
description: Audit CLAUDE.md and Claude Code memory files against a scored rubric, then propose targeted fixes. Use when asked to check, audit, review, score, improve, update, trim, or fix a CLAUDE.md, when asked whether project memory is any good or why Claude is ignoring it, when a CLAUDE.md has grown too large, or on mentions of CLAUDE.local.md, .claude/rules, memory files, project memory, or CLAUDE.md maintenance. Covers scope precedence, @imports, path-scoped rules, and what actually loads. NOT for capturing session learnings into memory — that is the reflect skill — and NOT for authoring an agent instruction file from scratch, which is agent-repo-docs.
allowed-tools: Read, Glob, Grep, Bash, Edit, WebFetch
metadata:
  author: Joonas Onatsu
  license: Apache-2.0
---

# CLAUDE.md Auditor

IRON LAW: NEVER award or deduct a point you cannot cite evidence for. A
criterion whose evidence was not gathered is reported `not assessed` and its
points leave the denominator. Reasoning about whether a documented command
*would* still work is fabrication, not assessment.

**Audit the loaded set, not the file on disk.** Memory arrives from four scopes,
`@` imports expand into it, and subdirectory files load only on demand. An audit
that reads `./CLAUDE.md` and stops has scored a fraction of what Claude sees.
Read `references/loading-model.md` before Phase 1 — every phase below depends on
it.

**This skill writes, but only after approval.** It reports first, proposes diffs
second, and edits third. NEVER edit a memory file before the user has approved
that specific diff.

## Workflow

```text
CLAUDE.md Audit Progress:
- [ ] Phase 1: Establish the loaded set ⛔ BLOCKING
- [ ] Phase 2: Read every file, imports included ⚠️ REQUIRED
- [ ] Phase 3: Gather rubric evidence (or mark criteria not assessed)
- [ ] Phase 4: Score and report ⚠️ REQUIRED before any edit
- [ ] Phase 5: Propose diffs → approval gate ⛔ BLOCKING
- [ ] Phase 6: Apply, then verify
- [ ] Pre-delivery checklist
```

### Phase 1: Establish the Loaded Set ⛔ BLOCKING

Ask first: **is a live session available to answer this directly?** If so,
`/context` → **Memory files** is ground truth and beats any filesystem guess.
Say in the report which method was used.

Otherwise reconstruct it. Resolve the config directory rather than assuming
`~/.claude`:

```bash
CFG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"

# User and managed scope
ls -la "$CFG/CLAUDE.md" "$CFG/rules/" 2>/dev/null
ls -la /etc/claude-code/CLAUDE.md 2>/dev/null   # Linux/WSL managed policy

# Ancestors of the working directory — these load at launch
d=$(pwd); while [ "$d" != "/" ]; do
  ls -la "$d/CLAUDE.md" "$d/.claude/CLAUDE.md" "$d/CLAUDE.local.md" 2>/dev/null
  d=$(dirname "$d")
done

# Project rules — recursive; `**` needs globstar in bash, so use find
find .claude/rules -type f -name '*.md' 2>/dev/null

# Subdirectory files — discovered, but load ON DEMAND, not at launch
find . -type f \( -name CLAUDE.md -o -name CLAUDE.local.md \) \
  -not -path '*/node_modules/*' -not -path '*/.git/*' \
  -not -path '*/vendor/*' -not -path '*/target/*' 2>/dev/null

# Files at paths Claude Code never reads — findings, not memory
find . -type f \( -name '.claude.md' -o -name '.claude.local.md' \) 2>/dev/null
ls -la AGENTS.md 2>/dev/null   # only loaded if a CLAUDE.md imports it
```

Then classify every file found as **launch-loaded**, **conditional** (a
subdirectory file or a `paths:`-scoped rule), or **never loaded**. The three are
not equivalent and MUST NOT be scored as one pool.

MUST NOT report a `find` result as "the memory files". Report it as the
candidate set, and say which of the two methods established the loaded set.

### Phase 2: Read Every File, Imports Included ⚠️ REQUIRED

Read each launch-loaded file, then follow its `@` imports to a depth of four,
recording the chain. Imports resolve relative to the **importing file**, not the
working directory, and imports inside backticks or fenced blocks are not
imports.

Record for each entrypoint: its own line count, its effective line count with
imports expanded, and the import tree. A short file with deep imports scores
completely differently from a short file.

MUST NOT score a file whose imports were not followed. An entrypoint whose
substance lives in imported rule files grades D on almost every criterion when
read alone, which inverts the result on the most carefully built setups.

### Phase 3: Gather Rubric Evidence

Each criterion in `references/scoring-rubric.md` names the evidence it needs.
Gather it, or mark the criterion `not assessed` — those are the only two options.

| Criterion | Evidence to gather |
|-----------|-------------------|
| Commands and workflows | The task runner or manifest: `package.json`, `justfile`, `Makefile`, `pyproject.toml`, `Cargo.toml`, CI workflow |
| Architecture orientation | The real directory tree, two levels deep |
| Currency | `test -e` on referenced paths; confirm documented commands still exist in the runner |
| Non-obvious knowledge, Density, Actionability | The file text plus imports — already gathered in Phase 2 |

Currency is where fabrication is easiest and costs most: a fabricated Currency
score certifies stale instructions as fresh. Either the check ran and its result
is citable, or the criterion is `not assessed`.

### Phase 4: Score and Report ⚠️ REQUIRED before any edit

Apply `references/scoring-rubric.md`. Score at its anchors only, per file, never
averaged across files.

Report shape:

> ## CLAUDE.md Audit
>
> **Loaded set established via**: `/context` | filesystem reconstruction
>
> | File | Scope | Loading | Own / effective lines |
> |---|---|---|---|
> | `./CLAUDE.md` | project | launch | 60 / 640 (3 imports) |
> | `./packages/api/CLAUDE.md` | project | on demand | 40 / 40 |
>
> ### `./CLAUDE.md` — 62/80 assessed (78%, B)
>
> | Criterion | Score | Evidence |
> |---|---|---|
> | Commands and workflows | 15/20 | `justfile` has 9 recipes; 3 documented |
> | Architecture orientation | 10/15 | … |
> | Non-obvious knowledge | 20/20 | … |
> | Density | 10/15 | … |
> | Currency | not assessed | no runner found to check commands against |
> | Actionability | 7/10 | … |
>
> **Weakest link**: …
> **Findings**: [red flags from the rubric — wrong filenames, contradictions
> across scopes, duplication between scopes, oversized files with no rules
> extracted]

State the weakest link explicitly. A B built on a zero needs a different fix
from a flat B.

### Phase 5: Propose Diffs → Approval Gate ⛔ BLOCKING

See `references/update-guidelines.md` for what earns a place in a memory file,
with worked good-versus-bad pairs. See `references/templates.md` for section
shapes when a file is missing structure.

Every proposal MUST carry the file, the diff, and one line on why it helps a
future session. Prefer removal: the cost of a line is paid every session, so
cutting a derivable directory tree is often worth more than adding a section.

When a proposal is really a mechanism change, say so instead of editing prose:

| Symptom | Proposal |
|---------|----------|
| Guidance applies to one file type or subtree | Extract to a `paths:`-scoped rule under `.claude/rules/` |
| File is over 200 effective lines | Extract path-scoped rules; note that imports reorganize without reducing cost |
| Instruction must hold every time | A hook — CLAUDE.md is context, not enforcement |
| `AGENTS.md` exists, no `CLAUDE.md` | Add `CLAUDE.md` containing `@AGENTS.md`, or symlink |
| Instruction keeps getting lost mid-session | Move it to the project root; nested files are not re-injected after compaction |
| Maintainer note with no value to Claude | Wrap in a block-level HTML comment — stripped before injection, so it costs nothing |

Then STOP and ask. NEVER apply an unapproved diff.

### Phase 6: Apply, Then Verify

Apply approved diffs with Edit, preserving surrounding structure. Afterward,
tell the user to confirm with `/context` in a new session — an edited file that
does not appear under **Memory files** did not take effect, and this skill
cannot observe that from outside a session.

## Anti-Patterns

- **Scoring what was never read.** The original of this skill scored
  "Architecture" and "Currency" from the CLAUDE.md text alone and told the model
  to run commands "mentally". That is the defect this rubric exists to prevent.
- **Reading the entrypoint and ignoring its imports.** Inverts the score on
  imported setups.
- **Hardcoding `~/.claude/CLAUDE.md`.** Reports the user file as missing
  wherever `CLAUDE_CONFIG_DIR` is set.
- **Recommending `.claude.md` or `.claude.local.md`.** Neither is ever read.
  Advising them sends personal instructions into a file that silently does
  nothing.
- **Treating subdirectory files as launch-loaded.** They are conditional.
  Pooling them with the root file misstates what Claude actually has.
- **Averaging scores across files**, or reporting `X/100` when a criterion went
  unassessed.
- **Padding a file to raise its score.** Every added line is a recurring cost.
  If a section only exists to satisfy the rubric, the rubric is wrong for that
  repo — say so.
- **Editing before approval**, or bundling an unapproved change with an approved
  one.
- **Auditing auto memory.** Different system, different directory, out of scope.

## Pre-Delivery Checklist

- [ ] The loaded set was established, and the method is named in the report
- [ ] Every file is classified launch-loaded, conditional, or never loaded
- [ ] Imports were followed to depth four; effective line counts reported
- [ ] Every score cites its evidence; unbacked criteria say `not assessed`
- [ ] Total reported as `earned / assessed`, per file, never averaged
- [ ] Red flags reported even where the score is high
- [ ] No file was edited without an approved diff
- [ ] The user was told to verify with `/context`
