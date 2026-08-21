# How CLAUDE.md Actually Loads

Audit findings are only as good as this model. Score against what Claude Code
really loads, not against what the file looks like in an editor.

Sourced from the official memory documentation, read 2026-08-21. Version-gated
claims name their minimum version; re-verify with `/context` on the machine in
front of you rather than trusting this file when the two disagree.

**Contents**
- [Scopes and load order](#scopes-and-load-order)
- [Filenames that do not exist](#filenames-that-do-not-exist)
- [Ancestors load at launch, subdirectories load on demand](#ancestors-load-at-launch-subdirectories-load-on-demand)
- [Imports](#imports)
- [Rules directories](#rules-directories)
- [AGENTS.md](#agentsmd)
- [Size, cost, and enforcement](#size-cost-and-enforcement)
- [Compaction](#compaction)
- [Verifying what loaded](#verifying-what-loaded)
- [Auto memory is a different system](#auto-memory-is-a-different-system)

---

## Scopes and Load Order

Loaded broadest first, so a project instruction lands in context *after* a user
instruction:

| Scope | Location | Notes |
|-------|----------|-------|
| Managed policy | Linux/WSL `/etc/claude-code/CLAUDE.md`; macOS `/Library/Application Support/ClaudeCode/CLAUDE.md`; Windows `C:\Program Files\ClaudeCode\CLAUDE.md` | Cannot be excluded by any user setting |
| User | `~/.claude/CLAUDE.md` | Personal, all projects |
| Project | `./CLAUDE.md` **or** `./.claude/CLAUDE.md` | Team-shared via source control |
| Local | `./CLAUDE.local.md` | Personal, this project; gitignore it |

Managed content can also be inlined as a `claudeMd` string in
`managed-settings.json`. That key is honored only in managed and policy
settings — setting it in user, project, or local settings does nothing.

**The user path follows the config directory.** When `CLAUDE_CONFIG_DIR` is set,
user-scope files live under that directory, not `~/.claude`. An audit that
hardcodes `~/.claude/CLAUDE.md` reports the user file as missing on every
relocated setup. Resolve it as `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/CLAUDE.md`.

Discovered files are **concatenated, never overridden**. A "conflict" between
two scopes is not resolved by precedence — both texts are in context, and Claude
may follow either. Flag contradictions as defects; do not assume the narrower
file wins.

## Filenames That Do Not Exist

`.claude.md` and `.claude.local.md` are not memory filenames. Claude Code never
reads them. They circulate widely in third-party guidance, so treat a repo
containing one as a finding: the author believed it was loaded and it was not.

The real local-override name is `CLAUDE.local.md`.

## Ancestors Load at Launch, Subdirectories Load on Demand

Claude Code walks **up** the directory tree from the working directory, reading
`CLAUDE.md` and `CLAUDE.local.md` at each level. Ordering runs from the
filesystem root down to the working directory, so the closest file is read last.
Within one directory, `CLAUDE.local.md` is appended after `CLAUDE.md`.

Files in **subdirectories** below the working directory are discovered but not
loaded at launch. They enter context when Claude reads a file in that
subdirectory.

This is the mechanism most often described wrongly. Parent-directory traversal
does not reach `./packages/*/CLAUDE.md` from the repo root — those are children.
A monorepo's per-package files work through on-demand loading, which means a
package file is absent from context until something in that package is read.
When auditing a monorepo, say which files are launch-loaded and which are
conditional; they are not equivalent.

`claudeMdExcludes` skips files by glob against absolute paths, merges across
settings layers, and cannot exclude managed policy files.

`--add-dir` does **not** load memory files from the extra directory unless
`CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` is set.

## Imports

`@path/to/import` pulls another file in. The mechanics that matter for an audit:

- Relative paths resolve against **the file containing the import**, not the
  working directory. Absolute paths work too.
- Imports recurse to a maximum depth of **four hops**.
- Import parsing **skips code spans and fenced code blocks**. Wrapping a path in
  backticks — `` `@README` `` — keeps it literal.
- Imported content **loads at launch and costs context**. Splitting a large file
  into imports improves organization and changes nothing about token cost.
- An import in a *project* file whose path resolves outside the working
  directory is external and triggers a one-time approval dialog. Declining
  disables those imports permanently and silently. Imports in user-scope files
  load without a dialog.

**A file cannot be judged by its own line count.** A 60-line CLAUDE.md whose
body is four `@rules/*.md` imports may carry a thousand lines into every
session. Follow every import before scoring size, coverage, or duplication —
scoring the entrypoint alone inverts the result on exactly the setups that took
the most care.

## Rules Directories

`.claude/rules/**/*.md` is the structured alternative to one long file. All `.md`
files are discovered recursively.

- No `paths:` frontmatter → loaded at launch, same priority as
  `.claude/CLAUDE.md`.
- With `paths:` frontmatter (glob list) → loaded when Claude reads a matching
  file, not on every tool use.
- User-level `~/.claude/rules/` loads before project rules.
- Symlinks are resolved, so a shared rules directory can be linked into many
  repos. Circular symlinks are handled.

A brace group in `paths` multiplies expansion; the whole list shares a budget of
1,000 expanded patterns. Patterns over budget are used unexpanded and then match
nothing. A `[` that cannot be read as a bracket expression makes that one
pattern match nothing — escape a literal one as `\[`.

Recommend a path-scoped rule over a CLAUDE.md section whenever guidance applies
to one file type or subtree. It is the only mechanism that removes tokens from
sessions that do not need them.

## AGENTS.md

Claude Code reads `CLAUDE.md`, not `AGENTS.md`. A repo with only `AGENTS.md` has
**no** Claude memory, however good that file is. The fixes are a `CLAUDE.md`
containing `@AGENTS.md` (plus any Claude-specific additions below it), or a
symlink where no additions are needed.

## Size, Cost, and Enforcement

- Target **under 200 lines** per file. CLAUDE.md files load in full regardless of
  length; longer files cost context every session and measurably reduce
  adherence.
- The cost is **recurring, not one-time**. Every session pays for every line.
  This is the argument for cutting content Claude can derive from the codebase.
- CLAUDE.md is delivered as a **user message after the system prompt**. It is
  context, not enforced configuration, and compliance is not guaranteed. An
  instruction that must hold every time belongs in a hook; an instruction needed
  at system-prompt level needs `--append-system-prompt`.
- **Block-level HTML comments are stripped** before injection. `<!-- note -->`
  is free maintainer commentary that costs no tokens. Comments inside code
  blocks are preserved, and everything is visible when the file is opened with
  Read.

## Compaction

Project-root CLAUDE.md survives `/compact` — it is re-read from disk and
re-injected. Nested CLAUDE.md files and `paths:`-scoped rules are **not**
re-injected; they reload only when Claude next reads a matching file.

An instruction that must survive a long session belongs at the project root, not
in a nested file. "It worked earlier in the session and stopped" is the symptom.

## Verifying What Loaded

Never infer the loaded set from the filesystem when a session can answer:

| Tool | Answers |
|------|---------|
| `/context` → **Memory files** | Which files actually loaded. Ground truth |
| `/memory` | Lists memory locations across scopes, including files that do not exist yet; opens them for editing |
| `InstructionsLoaded` hook | Logs which instruction files loaded, when, and why. Best for debugging path-scoped and lazy-loaded rules |
| `/doctor` | Proposes trims for a checked-in CLAUDE.md — cuts derivable content, keeps pitfalls and rationale. Requires v2.1.206+ |

## Auto Memory Is a Different System

Auto memory — what Claude writes for itself — lives in
`~/.claude/projects/<project>/memory/` with a `MEMORY.md` index. Only the first
200 lines or 25 KB of that index load per session; topic files load on demand.

It is **out of scope for a CLAUDE.md audit**. Do not score it, do not merge the
two, and do not propose moving content between them without being asked. When
the user's real question is "capture what we learned", that is `claude/reflect`,
not this skill.
