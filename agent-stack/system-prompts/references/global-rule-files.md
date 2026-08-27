# Global Rule Files

Load when the prompt under review or under authorship is a **global rule file** —
the per-user file a tool loads in every session regardless of the project open.
Skip it for system prompts, agent definitions, tool descriptions and API prompts;
none of the mechanics here apply to them.

**Not for a repository's `AGENTS.md` or `CLAUDE.md`.** Those are
`agents-management`'s, which owns the repo-local loading matrix and states that
user-level configuration is a different job. This file is that job.

**Contents**
- [Where the file lives](#where-the-file-lives)
- [Precedence](#precedence)
- [What delegated contexts inherit](#what-delegated-contexts-inherit)
- [Two tests that only apply here](#two-tests-that-only-apply-here)
- [Corrections to circulating claims](#corrections-to-circulating-claims)
- [Provenance](#provenance)

---

## Where the file lives

| Tool | Global rule file |
|---|---|
| Claude Code | `~/.claude/CLAUDE.md`, or under `$CLAUDE_CONFIG_DIR` |
| Codex | `~/.codex/AGENTS.override.md`, else `~/.codex/AGENTS.md`, or under `$CODEX_HOME` |
| OpenCode | `~/.config/opencode/AGENTS.md` |
| Copilot CLI | `~/.copilot/instructions.md` |

**Verify against current vendor documentation rather than trusting this table.**
These paths are the fastest-rotting content in this skill, and a file at a name
the tool does not read is invisible with nothing reporting it. `AGENTS.md` is the
portable name; a symlink from the tool-specific name keeps one copy.

## Precedence

**A correct rule that is overridden is not in force.** Where precedence is
undocumented, flag the conflict rather than reasoning about which wins.

For Codex, global loads first, then project root down to the working directory,
one file per directory, concatenated so later text overrides earlier — so **a
global rule can be silently overridden by a project file**. Substitute the
equivalent for another tool; do not assume this one generalises.

## What delegated contexts inherit

Subagents rarely receive the same set as the main session, the difference is
usually undocumented, and it decides where a rule must live.

Measured for Claude Code: rule files, imports, the memory index and the skill
list are present at spawn, while MCP instructions and the agent roster arrive
only with the first tool result. **A subagent that answers without calling a tool
decides on the rule files alone.**

Delegated contexts also often run smaller models, which is why the reader-model
calibration in `SKILL.md` enumerates them separately. A global file a frontier
model follows may already be failing in a subagent, invisibly from the main
session.

## Two tests that only apply here

`SKILL.md`'s REVIEW tests all apply. Two more exist because a global file is
injected into every session unconditionally:

**Universality — does this apply in every session?** A global file is always
injected, so conditional content dilutes every session it does not apply to. Move
it out and point at it. Split on this axis *before* considering length.

**Scope — is this rule at the right level?** Project specifics in a global file
cost every unrelated session. Global policy in a project file silently fails
everywhere else.

Also weight Currency higher here than elsewhere: global files outlive every
project they were written for, and nothing in any repository invalidates them.
Update a rule in the same change that invalidates it, and prune on a schedule —
nothing signals staleness.

**Keep to standard Markdown for anything that must work across tools.** Imports
and glob-scoping frontmatter are the portability trap: a rule depending on either
is silently absent wherever the mechanism is missing.

**Do not let a model generate the file.** Generated rules state the obvious,
which then costs context in every session to say — and the one controlled study
on this found generated files made task success *worse*.

## Corrections to circulating claims

Each appears widely, each was traced to its primary source, and an agent may
carry the wrong version.

| Circulating claim | What the source says |
|---|---|
| "Models follow ~150–200 instructions; you get ~100–150 slots" | Absent from the cited paper; two unrelated results merged. No threshold is established |
| "Past the limit it ignores all instructions uniformly" | Inverted. Degradation is selective and favours what comes first; uniform failure only past ~300 |
| "32 KiB is the technical maximum" | One tool's configurable loader cap, which silently truncates. Not a general limit |
| "Rules are re-injected on every tool call" | Vendor docs say rules load at launch; path-scoped ones trigger on matching reads, "not on every tool use" |
| "`globs:` loads rules unconditionally" | `globs:` is not a recognised key; `paths` is |
| "Emphasis keywords improve adherence" | Vendor guidance is a conditional tip naming only `IMPORTANT`, for one line at a time |
| "Positive directives hurt without examples" | The example condition was never tested; the clause is invented |
| "Imports reduce context cost" | Vendor docs: imports "load at launch". An import is a filing decision, not a saving |
| "Architecture overviews help agents navigate" | Measured: time-to-relevant-file unchanged with or without |

**Open the source before repeating a number.** Where that is impractical, cite it
as consensus and attach no paper.

## Provenance

Every row and mechanism above comes from a rules-audit merge dated 2026-08-27,
which states it read all primary sources directly on that date. **None of it has
been re-verified inside this skill**, so grade it DOCUMENTED-at-one-remove: good
enough to act on, not good enough to quote as measured. The per-tool paths and
the Claude Code inheritance result are the two most likely to have rotted; re-check
them first after any tool upgrade.
