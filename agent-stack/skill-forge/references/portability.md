# Portability

A skill runs on machines nobody configured for it, months after it was written. It MUST NOT
depend on any environmental fact it did not verify at run time.

- [Tools](#tools) · [Project-local entry points](#a-project-local-entry-point-is-not-a-tool)
- [The two exceptions](#exception-repo-scoped-skills) · [Paths](#paths)

## Tools

Tool availability MUST be established by a `PATH` probe (`command -v <tool>`) and nothing
else. NEVER assume a tool is installed, and NEVER hardcode an install path
(`/usr/local/bin/x`, `~/.local/share/mise/installs/...`, `/opt/homebrew/...`).

When a tool is absent, the skill MUST degrade to a reported skip or a named alternative,
NEVER fail and NEVER silently continue as though the step ran.

Where several tools do the job, list them in preference order and accept any one. A single
hardcoded tool rots the moment the ecosystem moves.

## A project-local entry point is NOT a tool

**And no `PATH` probe validates one.** `just check`, `npm run lint`, `make test`,
`mise run ci`, `pre-commit run`, `nox -s tests` and `./scripts/gate.sh` are contracts of one
REPOSITORY, not of a machine.

`command -v just` succeeds on any machine that has `just`, while that repo's `check` recipe
does not exist — so the probe passes and the command still fails. That is worse than no
probe, because it reads as verification. A portable skill MUST NOT name one.

Instead, DISCOVER the repo's entry point at run time, and state the detection order: a
pre-commit config, then a task runner (`justfile`, `Makefile`, `mise.toml`, `package.json`
scripts, `pyproject` scripts), then a `scripts/`/`bin/` entry. Run what is found. When
nothing is found, report that and skip — NEVER invent a command, and NEVER assume the
conventional name is present.

## Exception: repo-scoped skills

A skill that ships inside the repository it serves MAY, and SHOULD, name that repo's
commands directly — they are its contract rather than an assumption. It MUST declare
`metadata.scope: repo-local` and name that repository near the top, so the next reader knows
the naming is deliberate and does not lift the skill somewhere it cannot work.

## Exception: a skill ABOUT a tool

Such a skill may bind to that tool, **and to nothing else.** Naming `pytest` inside a pytest
skill is its subject, not an assumption, and demanding tool-agnosticism there is incoherent.

The carve-out covers the subject ONLY: that same skill MUST still discover the repo's runner
rather than naming `just test`, MUST still probe for any tool beyond its subject, and MUST
still state what happens when its own subject is absent. Assuming a SECOND tool is the
ordinary defect wearing the subject's clothes, and it is harder to see precisely because the
first binding was legitimate.

## Paths

Paths to a skill's own bundled files MUST be relative to the skill directory, with forward
slashes. NEVER write `~/.claude/skills/<name>/...`: it breaks under `CLAUDE_CONFIG_DIR` and
for project-scoped installs alike. NEVER use backslashes, which fail on Unix.

NEVER reference the authoring machine — its absolute paths, its usernames, its specific
package manager, or a tool version only it has.
