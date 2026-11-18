# Client Loading Adapters

Use this reference only when topology or verification depends on client behavior. Treat the known adapters as
maintained defaults for their stated conditions, not as universal rules.

## Contents

- Capability discovery
- Known compatibility default
- What loads by itself and what needs a route
- Known client details: Claude Code, Codex, OpenCode, Copilot CLI
- Portable degradation

## Capability Discovery

For each target client, determine:

- canonical repository-local filenames and precedence;
- root and nested-file discovery;
- include or pointer behavior;
- path or glob scoping;
- size limits and truncation;
- reload behavior and any live loaded-context inspection;
- symlink support in both the client and target filesystem.

Prefer current vendor documentation, local help, or a controlled observation. Record the client version and
evidence date when the result can drift. If evidence is unavailable, state what is unknown and use only
verified capabilities. Do not invent an adapter or claim complete coverage.

Refresh an adapter when the client changes materially, evidence conflicts, or setup verification fails.
Ordinary content updates do not require repeated online research.

## Known Compatibility Default

For repositories targeting Claude Code, Codex, OpenCode, and Copilot CLI on a filesystem with symlinks, use a
real `AGENTS.md` and a sibling `CLAUDE.md` symlink to it. Every client then reads the same content:

| Repository state         | Claude Code                       | Codex                      | OpenCode                                           | Copilot CLI                          |
| ------------------------ | --------------------------------- | -------------------------- | -------------------------------------------------- | ------------------------------------ |
| `AGENTS.md` only         | read since 2.1.277 *(documented)* | read *(documented)*        | read *(documented)*                                | read *(documented)*                  |
| `CLAUDE.md` only         | read *(documented)*               | not read unless configured | fallback when `AGENTS.md` is absent *(documented)* | read *(documented)*                  |
| Both real and divergent  | `CLAUDE.md` only                  | `AGENTS.md`                | `AGENTS.md`                                        | both, with no defined conflict order |
| One real and one symlink | same content                      | same content               | same content                                       | same content                         |

Keep the symlink even though current Claude Code reads `AGENTS.md` alone. Claude Code reads `CLAUDE.md` only on
versions before 2.1.277, in some first sessions after an upgrade, and when its `AGENTS.md` plugin is disabled.

When creating the pair, make `AGENTS.md` real and use `ln -s AGENTS.md CLAUDE.md`. Never use `ln -f` or
replace an existing real file. If symlinks are unsupported, preserve one canonical source and use the least
duplicative verified adapter available; report any synchronization burden.

Sources, read 2026-11-18: Claude Code memory documentation (<https://code.claude.com/docs/en/memory>, installed
2.1.326) and Codex `AGENTS.md` guide (<https://developers.openai.com/codex/guides/agents-md>, installed 0.169.0).
OpenCode and Copilot CLI documentation was last re-read on 2026-09-16; neither prints a version on its pages.

## What Loads by Itself and What Needs a Route

A route in the floor is guidance the agent may ignore. Measured sessions show agents reach most documents by
search or by links between documents, and take a floor route for a minority of reads. So deliver a rule by the
strongest mechanism the target clients share:

- **Every session needs it:** the floor itself, as one imperative line.
- **Work in one subtree needs it:** a nested instruction file the client loads by itself (Claude Code when it
  touches a file there; OpenCode V2 as the agent reads into the subtree), plus a trigger-keyed floor route for
  clients that do not descend or whose descent is unverified. Codex loads nested files only on the path from
  the repository root to the working directory, so a session started at the root needs the route.
- **Work on matching files needs it, Claude Code only:** a path-scoped rule (below), with the same route as the
  portable fallback.
- **Evidence or reference read at need:** a routed document that is also findable by search.

## Known Client Details

### Claude Code

- Reads `CLAUDE.md` and `CLAUDE.local.md` from the working directory and every directory above it at launch.
  Reads `AGENTS.md` instead when neither exists there, since 2.1.277; the **Project instructions** setting
  changes which files load.
- Loads a subdirectory's `CLAUDE.md` once Claude reads, writes, or edits a file in that subdirectory, including
  a single-file `cat` or `head` through Bash.
- `@path` imports expand recursively to a depth of four hops, relative to the importing file. An import
  organizes a long file but does not reduce its context cost, because the imported file loads with it.
- Path-scoped rules are files under `.claude/rules/` with a `paths` frontmatter field of glob patterns. One loads
  when Claude reads, writes, or edits a matching file, including through a symlinked path.
- The documentation targets "under 200 lines per CLAUDE.md file" because "Longer files consume more context and
  reduce adherence", and warns that of two contradicting instructions, "Claude may pick one arbitrarily".
- `/context` reports the loaded memory files; `/doctor prompt-audit` (2.1.283 and later) reports stale,
  missing-reference, and conflicting instructions without editing them.

### Codex

- Builds the instruction chain once per run, or once per interactive session; restart to pick up edits.
- Reads `~/.codex/AGENTS.override.md`, or else `~/.codex/AGENTS.md`, then walks from the repository root down to
  the working directory. In each directory it takes the first of `AGENTS.override.md`, `AGENTS.md`, and any name
  in `project_doc_fallback_filenames`, one file per directory. Files nearer the working directory come later and
  override earlier guidance.
- Does not read files below the working directory, and does not read `CLAUDE.md` unless it is listed as a
  fallback name.
- Stops adding files once the combined size reaches `project_doc_max_bytes`, 32 KiB by default, and skips empty
  files. Runtime `@`-include expansion is not documented.
- Delivers the chain as a message headed "# AGENTS.md instructions". To list what loaded, run
  `codex --ask-for-approval never "Show which instruction files are active."`.

### OpenCode

Two current major versions differ materially; V1 is still the default install and V2 is rolling out (2026-09).

- **V1:** prefers `AGENTS.md`; `CLAUDE.md` is a fallback only when `AGENTS.md` is absent (disable via
  `OPENCODE_DISABLE_CLAUDE_CODE`). Traverses upward from the working directory and does not discover descendant
  package files. Does not expand file references as runtime includes; a trigger-keyed route can tell the model
  to read another file.
- **V2:** discovers `AGENTS.md` only. The `CLAUDE.md` fallback is dropped, so move any `CLAUDE.md`-only
  guidance into `AGENTS.md`. It also discovers descendant `AGENTS.md` files as the agent reads into
  subdirectories, nearest-first. Runtime `@`-reference expansion is unverified, and the config `instructions`
  array is currently unimplemented.
- Neither version has a confirmed command that reports the actual loaded instruction set; a config dump is not
  equivalent.

### Copilot CLI

- Reads `AGENTS.md`, `CLAUDE.md` (and `.claude/CLAUDE.md`), `.github/copilot-instructions.md`, and `GEMINI.md`,
  plus personal `~/.copilot/copilot-instructions.md` and modular `*.instructions.md` sets.
- Combines applicable instruction sources and does not define a conflict order; identical copies are deduped.
- `@relative` includes expand immediately and recursively in `copilot-instructions.md`, `AGENTS.md`, and
  `CLAUDE.md`, but not in `GEMINI.md` or `*.instructions.md`; absolute and `~/` paths are rejected. `applyTo`
  glob scoping on `*.instructions.md` frontmatter is documented but was not independently exercised.
- `/instructions` lists the files discovered for the session and toggles them individually.
- Requires a fresh session to pick up edits: exit and resume (`copilot --continue`) or start a new one
  (`/new`).

## Portable Degradation

For an unfamiliar client, discover its capabilities before adding an adapter. Keep `AGENTS.md` as the
vendor-neutral canonical source when compatible. Add another filename or vendor-specific directory only when
verified as necessary.

When include expansion or nested discovery is unknown, use a trigger-keyed route in the canonical root file
that names the condition and target path. A route is guidance rather than guaranteed runtime loading, so
report that limitation, and keep any rule the agent must not miss in the floor itself. Avoid unverified
path-scoping frontmatter.

Nested files need their own verified adapters. For the known four-client target, place a real `AGENTS.md` and
sibling `CLAUDE.md` symlink in each relevant package, then add a root route for clients that do not descend.
