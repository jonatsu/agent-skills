# Troubleshooting

## Fast debug ladder

1. `lean-ctx status`
2. `lean-ctx doctor`
3. `lean-ctx doctor integrations`
4. `lean-ctx doctor --fix` or `lean-ctx setup --fix`
5. `lean-ctx sessions doctor`
6. `lean-ctx cache prune`
7. `lean-ctx report-issue`

## Shell hook issues

- Use `lean-ctx-off` to disable current shell hook.
- Use `LEAN_CTX_DISABLED=1` for one command.
- Use `LEAN_CTX_RAW=1` when compression hides needed output.
- Check RC files for stale exports and `*.lean-ctx.bak` restore points.

## MCP issues

- Confirm editor sees the MCP server and active tool list.
- Reload config for env/settings changes; restart editor for tool-list changes.
- Avoid stale `LEAN_CTX_DATA_DIR` unless legacy single-dir mode is intentional.
- Distinguish installed tools from loaded profile tools.

## Project-root capture (path jail)

**Symptom**: `ctx_*` path tools report `path escapes project root: <your file>
(root: <some other tree>)`. The reported root is a directory the session recently
touched — a research clone, a subagent's working dir, an agent config dir — not
the project.

**Triggers** (observed on 3.9.x): absolute-path `ctx_read`/`ctx_shell` into a
foreign tree, with no `cwd` change; a subagent working in one, which re-roots the
parent session; loading a skill or config from a directory that is itself a
project.

**Markers are not only `.git`.** `package.json`, `Cargo.toml`, `pyproject.toml`,
`go.mod`, `go.work`, `Makefile`, and `CMakeLists.txt` all capture, so stripping
`.git` from a scratch clone does not prevent it. Treat any common project file as
a marker rather than working from a list.

**The root latches to the OUTERMOST marker-bearing ancestor of the touched path,
not the nearest**, so the captured root can sit far above the file that triggered
it. It can still land on a *subdirectory* of the tree you touched, and that is the
same rule rather than an exception: it happens when the tree's own top level
carries no marker while a nested directory does — exactly what a `.git`-stripped
clone with a `package.json` under `docs/` looks like.

**Exposure is concentrated at session start.** Once a marker-bearing project root
IS set, an absolute path into a foreign tree fails closed instead of re-rooting.
The dangerous window is the first `ctx_read`/`ctx_shell` of a session, while no
root is set — which is why loading a skill from a config directory that is itself
a project captures so reliably.

**Recovery**: reconnect the MCP server (in Claude Code, `/mcp`). The root is
latched and persisted — nothing clears it on a timer, so do NOT wait it out.
Re-passing `cwd=<project root>` to `ctx_shell` is rejected, and the rejected call
still runs in the captured root, appending a
`[cwd: requested path rejected by project-root jail …]` line to the output. Read
the tail before trusting the result; that notice is missing only when the session
lock times out.

**Root oracles** (there is no root-resolution log): the `(root: …)` string in any
jail error, and the `Session state … root: …` line in `lean-ctx doctor`.

**One jail error IS worth retrying.** A message reading `Auto-detected … Retry the
read.` is language-cache auto-registration, not capture: retry once and it
succeeds. It is the only jail-shaped error that a retry fixes — every other one
should not be retry-looped, least of all by re-passing `cwd`.

**While jailed**: native file read/write/edit tools pass through; native shell
does not — it returns the jail error or runs in the captured root.

**Prevention**: read remote repos with `ctx_git_read` rather than cloning
locally; read a local foreign tree with the host's native read tool. Treat an
absolute path into another project as the trigger, not just `cwd`.

**Config levers** (ask first; see appendix-paths-and-config): `project_root`,
`extra_roots`, `read_only_roots`.

**No config key suppresses capture.** `allow_auto_reroot` gates only one of three
re-root paths and already defaults to `false`, so setting it to `false` is a no-op
and setting it to `true` only widens the third path. The levers above widen the
jail so the real project stays reachable; they do NOT stop the root from moving.
The only switch that disables the jail outright is `path_jail = false`, which gives
up containment entirely.

## Patch issues

- Stale anchor: refresh anchored read and retry once.
- Wrong file root: the root may have moved — see "Project-root capture".
- Legacy edit tool missing: use `ctx_patch` or load power tools if needed.

## Proxy issues

- Check proxy `status` before assuming traffic is routed.
- Compare foreground env with service env.
- Disable proxy before testing direct provider failures.

## Rules injection reappearing

**Symptom**: lean-ctx keeps rewriting CLAUDE.md, AGENTS.md, or similar
instruction files on startup despite manual edits or removal.

**Fix — Claude Code (CLAUDE.md)**:
1. Set `rules_injection = "off"` and `rules_scope = "project"` in config.
2. Run `lean-ctx setup --fix` to apply.
3. CLAUDE.md injection uses a separate gating mechanism from other clients.

**Fix — OpenCode / Cursor / Codex (AGENTS.md)**:
1. Set `auto_inject_rules = false` in config.
2. Run `lean-ctx setup --fix` to apply.

**Why file permissions don't help**: lean-ctx writes rules via atomic
temp-file+rename, which only requires write permission on the *containing
directory*, not the target file itself. `chmod 444` on the target file is
ineffective. Do NOT use `chattr +i` or directory `chmod 555` as primary
fixes — config is the correct fix; those are broad machine-level changes.

## Skill files rewritten

**Symptom**: a hand-authored `SKILL.md` under an agent's skills directory shrinks
or changes wording, its frontmatter `metadata` block disappears, and a
`SKILL.md.bak` appears beside it carrying the same mtime. The skill's active
description becomes upstream's ("Context Engineering for AI Agents … Auto-installs
if not present").

**Cause**: lean-ctx writer commands (`setup`, `onboard`, `init`, `install`,
`update`, `wrap`, `doctor --fix`, `skill`) install lean-ctx's own vendored skill
as part of the same hook/rules rewrite cycle. Every agent directory lean-ctx
knows about is written in one pass.

**Confirm it**: compare mtimes across agent directories — an install writes them
within the same second; check the new file's mode, which carries the writer's
umask rather than the surrounding files'; diff it against `SKILL.md.bak`.

**Recover**: re-deploy from the source of truth. Do NOT simply restore
`SKILL.md.bak` — that is whatever happened to be deployed at overwrite time, and
it may itself be stale relative to the source repo.

**Guard**: no config key is known to gate skill installation the way
`rules_injection` and `auto_inject_rules` gate rules files. Verify against
`--help` and `doctor` on the running version rather than assuming one exists, and
treat every writer command as mutating: re-deploy after it.
