# What Each Agent Actually Reads

Repository-local files only. User-level and global configuration is out of scope
for this skill and is not described here.

**Contents**
- [The matrix](#the-matrix)
- [Why the symlink is required](#why-the-symlink-is-required)
- [Includes](#includes)
- [Nested and per-package files](#nested-and-per-package-files)
- [Path-scoped instructions](#path-scoped-instructions)
- [Ground truth in a live session](#ground-truth-in-a-live-session)
- [Files that are never read](#files-that-are-never-read)
- [Unrecognized agents: the portable fallback](#unrecognized-agents-the-portable-fallback)
- [Provenance](#provenance)

---

## The matrix

Three agents are first-class because their behavior was checked. Every cell
carries how it is known:

| Stamp | Means |
|---|---|
| *measured* | Observed directly, at a stated version and date |
| *reported* | Observed by the skill's user across sessions, not reproduced under test. Weaker than measured — say so when it is load-bearing |
| *documented* | Stated by the vendor's own documentation, read on a stated date, not exercised |
| *unverified* | Neither |

| | `AGENTS.md` | `CLAUDE.md` | Nested files | Parsed includes | Path-scoping |
|---|---|---|---|---|---|
| **Claude Code** | not read *(reported)* | read *(measured)* | discovered, on demand *(documented)* | yes, depth 4 *(documented)* | frontmatter exists but **did not fire** *(measured)* |
| **OpenCode** | read *(documented)* | fallback only, when no `AGENTS.md` *(documented)* | **not discovered** — upward traversal only *(documented)* | **none — not parsed** *(documented)* | none *(documented)* |
| **Copilot CLI** | read *(documented)* | read *(documented)* | nearest-wins *(documented)* | yes *(documented)* | `applyTo` frontmatter *(documented, unverified here)* |

Copilot CLI also reads `.github/copilot-instructions.md`, and combines every
applicable instruction file rather than picking one. Its documentation declines
to define a precedence order between them and advises against conflicting
instructions.

OpenCode resolves the first match in each category and stops; where both exist,
only `AGENTS.md` is used. A separate config-declared instructions list is
additive to it rather than an override.

## Why the symlink is required

One repository, three agents, three different readings:

| Repo has | Claude Code | OpenCode | Copilot CLI |
|---|---|---|---|
| `AGENTS.md` only | nothing | `AGENTS.md` | `AGENTS.md` |
| `CLAUDE.md` only | `CLAUDE.md` | `CLAUDE.md` | `CLAUDE.md` |
| both, real, divergent | `CLAUDE.md` only | `AGENTS.md` only | both, combined, undefined order |
| both, one a symlink | same text | same text | same text |

Only the last row makes the three agree. On Copilot the symlink additionally
collapses two names to one file, which its documented removal of duplicate
identical files should then handle cleanly — inference from that rule, not a
documented statement about symlinks.

`AGENTS.md` is the real file when creating from scratch: it is the open
convention, OpenCode prefers it, Copilot reads it, and only Claude Code needs
the link.

**Both real and divergent is a STOP, never an auto-fix.** Each file holds
content the other does not, or they would not have diverged. Report it and let
the user choose what survives.

## Includes

Where includes are parsed, they resolve relative to the **including file**, not
the working directory, and an include written inside backticks or a fenced block
is not an include. Depth limits and path constraints differ per agent; Copilot
CLI documents that included files must stay inside the repository and rejects
absolute and home-relative paths.

**OpenCode does not parse includes at all.** Its documentation is explicit that
a written file reference is a convention instructing the model to read the file
with its own tool, not an import the runtime expands. Guidance that depends on
an include silently does not arrive there.

This is why the pointer table is the portable mechanism: a row in the main file
naming the auxiliary file and the trigger for opening it works whether or not
the agent has a parser.

**Phrase a pointer as an imperative naming its trigger**, never as a description
of what the harness does. One external evaluation reports that an agent
acknowledges a "read the nearest file" instruction without acting on it absent
explicit prompting. That result is undated and unreproduced here, so treat the
pointer table as **effective but unmeasured**, and give it the strongest phrasing
available rather than assuming it arrives.

## Nested and per-package files

- **Claude Code** discovers nested instruction files and loads them on demand
  when working in that directory. A root symlink does not reach them — mirror
  the symlink inside each package directory that has its own file.
- **Copilot CLI** applies nearest-wins across the directory tree.
- **OpenCode** traverses *upward* from the working directory only. It never
  descends, so a per-package file is invisible to it unless its config declares
  the paths explicitly.

Therefore: per-package file, plus a per-package symlink, plus a pointer row in
the root file. Each covers what the others miss.

## Path-scoped instructions

Three agents, three different stories, and no recommendation follows from any of
them:

- **Claude Code** — the frontmatter key exists and is documented, but did not
  fire when measured. A rule carrying it was not in the loaded set after files
  matching its globs had been read. Treat such a file as **not loaded**.
- **Copilot CLI** — documents a glob-scoped frontmatter key on files in a
  dedicated instructions directory, reportedly honored by the CLI. Not verified
  here.
- **OpenCode** — no such mechanism.

MUST NOT recommend path-scoping. Where guidance applies to one subtree, put it
in its own file and point at it. That works on all three.

## Ground truth in a live session

Ask the running agent rather than guessing from the filesystem. The command
differs, and one agent has none:

- **Claude Code** — the context inspection command reports which memory files
  loaded.
- **Copilot CLI** — an instructions command lists the files discovered for the
  session and toggles them individually. Copilot does not pick up edits to
  instruction files in an already-running session; a fresh session is required.
- **OpenCode** — **none confirmed.** A config-dump debug subcommand exists and
  shows the resolved config, but nothing documents it as reporting which
  instruction files were actually loaded. Say so rather than inventing a command.

Exact invocations change between releases; ask the agent or check its help
output rather than trusting a transcription here.

## Files that are never read

Report these as findings, not as memory:

- Dot-prefixed variants of the instruction filenames. They are not read by any
  first-class agent, and recommending one sends instructions into a file that
  silently does nothing.
- A per-package file in a repository whose only agent is OpenCode, with no
  config declaration — see nesting above.
- A rule file carrying path-scoping frontmatter on Claude Code — see above.

## Unrecognized agents: the portable fallback

For any agent not in the matrix, do the things that work without a parser and
without vendor-specific frontmatter:

1. `AGENTS.md` at the repository root, as the real file.
2. A symlink from whatever filename that agent reads, if it is known.
3. In-document pointer rows for anything not in the main file.
4. No reliance on include expansion, and no path-scoped frontmatter.

State plainly which of the agent's behavior was not verified. NEVER block
because an agent is unrecognized, and NEVER claim coverage that was not checked.

## Provenance

- Claude Code cells marked *measured*: observed on Claude Code 2.1.239,
  2026-08-25 and 2026-08-26. The path-scoping result is a negative — the rule
  files were absent from the loaded set after matching files were read.
- The Claude Code `AGENTS.md` cell is *reported*, not measured: repeated
  user observation across sessions, never reproduced under test. **It is also
  the cell the symlink requirement rests on**, so it carries the weakest stamp
  and the heaviest load. Measuring it directly is the single highest-value
  correction anyone can make to this file. It is hard to measure in a repo where
  the two filenames are already symlinked, since both then resolve to identical
  bytes and no observation separates them — use a repo with two distinct real
  files, or a scratch one.
- OpenCode and Copilot CLI cells marked *documented*: vendor documentation read
  2026-08-26, not exercised here. **Agent versions not recorded** — the docs
  were read as current rather than pinned, so a behavior change since then
  would not show. Record the version when next confirming these.
- Re-check the *measured* cells first after any Claude Code upgrade; they are
  the ones a release can silently flip.
