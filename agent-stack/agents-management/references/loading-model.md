# Client Loading Adapters

Use this reference only when topology or verification depends on client behavior. Treat the known adapters as
maintained defaults for their stated conditions, not as universal rules.

## Capability Discovery

For each target client, determine:

- canonical repository-local filenames and precedence;
- root and nested-file discovery;
- include or pointer behavior;
- path or glob scoping;
- reload behavior and any live loaded-context inspection;
- symlink support in both the client and target filesystem.

Prefer current vendor documentation, local help, or a controlled observation. Record the client version and
evidence date when the result can drift. If evidence is unavailable, state what is unknown and use only
verified capabilities. Do not invent an adapter or claim complete coverage.

Refresh an adapter when the client changes materially, evidence conflicts, or setup verification fails.
Ordinary content updates do not require repeated online research.

## Known Compatibility Default

For repositories targeting Claude Code, OpenCode, and Copilot CLI on a filesystem with symlinks, use a real
`AGENTS.md` and a sibling `CLAUDE.md` symlink to it. This is the established compatibility default:

| Repository state         | Claude Code           | OpenCode                                           | Copilot CLI                          |
| ------------------------ | --------------------- | -------------------------------------------------- | ------------------------------------ |
| `AGENTS.md` only         | not read *(reported)* | read *(documented)*                                | read *(documented)*                  |
| `CLAUDE.md` only         | read *(measured)*     | fallback when `AGENTS.md` is absent *(documented)* | read *(documented)*                  |
| Both real and divergent  | `CLAUDE.md`           | `AGENTS.md`                                        | both, with no defined conflict order |
| One real and one symlink | same content          | same content                                       | same content                         |

The OpenCode column describes the V1 default install. OpenCode V2 (rolling out 2026-09) discovers `AGENTS.md`
only and drops the `CLAUDE.md` fallback, so the pair still works there — V2 reads the real `AGENTS.md` and
ignores the symlink — but a repository that put guidance only in `CLAUDE.md` loses it under V2.

When creating the pair, make `AGENTS.md` real and use `ln -s AGENTS.md CLAUDE.md`. Never use `ln -f` or
replace an existing real file. If symlinks are unsupported, preserve one canonical source and use the least
duplicative verified adapter available; report any synchronization burden.

The Claude Code `AGENTS.md` result is repeated user observation, not a controlled measurement. Claude Code
documentation was verified against version 2.1.269 on 2026-09-16, and its instruction-loading model was
unchanged between 2.1.239 and 2.1.269. OpenCode and Copilot CLI documentation was re-read on 2026-09-16;
neither prints a version on its documentation pages, and OpenCode's is versioned only as V1 and V2 (below).

## Known Client Details

### Claude Code

- Uses `CLAUDE.md` repository context in the measured setup.
- Discovers nested context on demand according to documentation.
- Parses relative includes to a documented depth of four.
- Path scoping uses a `paths` frontmatter field of glob patterns, not an `applyTo` field; it is documented as
  loading, and matching follows a symlinked path since 2.1.198. The earlier 2.1.239 non-load observation
  predates that fix, so re-measure before relying on it in a critical path.
- `/context` reports the loaded memory files; `/memory` browses auto-memory.

### OpenCode

Two current major versions differ materially; V1 is still the default install and V2 is rolling out (2026-09).

- **V1:** prefers `AGENTS.md`; `CLAUDE.md` is a fallback only when `AGENTS.md` is absent (disable via
  `OPENCODE_DISABLE_CLAUDE_CODE`). Traverses upward from the working directory and does not discover descendant
  package files. Does not expand file references as runtime includes; a trigger-keyed route can tell the model
  to read another file.
- **V2:** discovers `AGENTS.md` only — the `CLAUDE.md` fallback is dropped, so move any `CLAUDE.md`-only
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
report that limitation. Avoid unverified path-scoping frontmatter.

Nested files need their own verified adapters. For the known three-client target, place a real `AGENTS.md` and
sibling `CLAUDE.md` symlink in each relevant package, then add a root route for clients that do not descend.
