# Client Loading Adapters

Use this reference only when topology or verification depends on client behavior. Treat the known adapters as maintained
defaults for their stated conditions, not as universal rules.

## Capability Discovery

For each target client, determine:

- canonical repository-local filenames and precedence;
- root and nested-file discovery;
- include or pointer behavior;
- path or glob scoping;
- reload behavior and any live loaded-context inspection;
- symlink support in both the client and target filesystem.

Prefer current vendor documentation, local help, or a controlled observation. Record the client version and evidence date
when the result can drift. If evidence is unavailable, state what is unknown and use only verified capabilities. Do not
invent an adapter or claim complete coverage.

Refresh an adapter when the client changes materially, evidence conflicts, or setup verification fails. Ordinary content
updates do not require repeated online research.

## Known Compatibility Default

For repositories targeting Claude Code, OpenCode, and Copilot CLI on a filesystem with symlinks, use a real `AGENTS.md`
and a sibling `CLAUDE.md` symlink to it. This is the established compatibility default:

| Repository state | Claude Code | OpenCode | Copilot CLI |
|---|---|---|---|
| `AGENTS.md` only | not read *(reported)* | read *(documented)* | read *(documented)* |
| `CLAUDE.md` only | read *(measured)* | fallback when `AGENTS.md` is absent *(documented)* | read *(documented)* |
| Both real and divergent | `CLAUDE.md` | `AGENTS.md` | both, with no defined conflict order |
| One real and one symlink | same content | same content | same content |

When creating the pair, make `AGENTS.md` real and use `ln -s AGENTS.md CLAUDE.md`. Never use `ln -f` or replace an
existing real file. If symlinks are unsupported, preserve one canonical source and use the least duplicative verified
adapter available; report any synchronization burden.

The Claude Code `AGENTS.md` result is repeated user observation, not a controlled measurement. Claude Code 2.1.239
measurements and current vendor documentation were last checked on 2026-08-25 and 2026-08-26. OpenCode and Copilot CLI
documentation was read on 2026-08-26 without recorded versions. These facts were not refreshed during the 2026-09-02
rewrite because external documentation access was unavailable.

## Known Client Details

### Claude Code

- Uses `CLAUDE.md` repository context in the measured setup.
- Discovers nested context on demand according to documentation.
- Parses relative includes to a documented depth of four.
- Documented path-scoping frontmatter did not load in the 2.1.239 observation. Treat it as unavailable until reverified.
- Its context inspection command can show loaded memory files. Obtain the current invocation from local help.

### OpenCode

- Prefers `AGENTS.md`; `CLAUDE.md` is a fallback only when `AGENTS.md` is absent.
- Traverses upward from the working directory and does not discover descendant package files.
- Does not expand file references as runtime includes. An imperative pointer can tell the model to read another file.
- No command has been confirmed to report the actual loaded instruction set. A config dump is not equivalent.

### Copilot CLI

- Reads both `AGENTS.md` and `CLAUDE.md`, plus `.github/copilot-instructions.md` where applicable.
- Combines applicable instruction sources and does not define a conflict order.
- Documents nearest-file behavior, includes, and `applyTo` scoping. The scoping behavior was not independently exercised.
- Requires a fresh session to pick up instruction-file edits according to the documentation read in 2026-08.

## Portable Degradation

For an unfamiliar client, discover its capabilities before adding an adapter. Keep `AGENTS.md` as the vendor-neutral
canonical source when compatible. Add another filename or vendor-specific directory only when verified as necessary.

When include expansion or nested discovery is unknown, use an imperative pointer in the canonical root file that names
the trigger and target path. A pointer is guidance rather than guaranteed runtime loading, so report that limitation.
Avoid unverified path-scoping frontmatter.

Nested files need their own verified adapters. For the known three-client target, place a real `AGENTS.md` and sibling
`CLAUDE.md` symlink in each relevant package, then add a root pointer for clients that do not descend.
