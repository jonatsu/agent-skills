---
name: lean-ctx
description: Use for lean-ctx and its ctx_* MCP tools — ctx_read, ctx_search, ctx_glob, ctx_tree, ctx_shell, ctx_patch, ctx_call, ctx_expand, ctx_git_read — plus shell hook, MCP config, profiles, compression, proxy, doctor, wrap/onboard/setup/update, and rules injection. Use when picking a read mode or edit op, when a ctx_* call returns a suspicious, empty, or suspiciously complete result, when an edit is rejected or an anchor goes stale, when path-jail or project-root errors appear, or when installing, configuring, or debugging lean-ctx.
metadata:
  author: Joonas Onatsu
  license: Apache-2.0
---

# lean-ctx

IRON LAW: Prefer lean-ctx context tools before raw read/search/shell/patch tools
when available. Keep context lean, recoverable, and verifiable. Do not assume
one host, editor, path layout, or config; inspect active tools and local setup
first.

## Workflow

```text
lean-ctx skill flow:

- [ ] Step 1: Inspect narrowly ⚠️ REQUIRED
  - [ ] Use `ctx_tree`, `ctx_glob`, `ctx_search`, `ctx_read`
  - [ ] Start `signatures`/`map`; use `anchored` before patching
- [ ] Step 2: Choose execution path ⚠️ REQUIRED
  - [ ] Use `ctx_shell` when output may be large, compressible, or worth reuse
  - [ ] Use `ctx_patch` for anchored/batch edits; retry once on stale anchors
- [ ] Step 3: Load only needed refs
- [ ] Step 4: Verify with repo-native checks ⚠️ REQUIRED
```

## Confirmation gates

- Default to no user-environment mutation for setup help. Offer manual MCP or
  agent-only init first; ask with low threshold if shell-hook or RC-file edits
  are also wanted.
- Ask before changing shell hooks, editor MCP config, proxy mode, path jail, or
  other machine-level settings.
- Ask before enabling broad access like `path_jail=false` or extra roots outside
  task scope.
- If setup docs conflict with live `doctor`, `--help`, generated appendices, or
  active tool registry, trust live state and say so.

## Load-on-demand refs

- `references/01-setup-and-onboarding.md` — install, wrap, onboard, setup
- `references/02-daily-use.md` — read/search/tree/shell/patch basics
- `references/04-code-intelligence.md` — symbols, graph, impact, quality
- `references/05-advanced.md` — power tools, proxy, shell hook, MCP
- `references/06-lifecycle.md` — update, repair, sessions, cache, migration
- `references/07-context-engineering.md` — compression, read modes, recovery
- `references/12-troubleshooting.md` — symptom → fix playbooks
- `references/13-silent-failure-modes.md` — load when a `ctx_*` result looks
  wrong, empty, or suspiciously complete
- `references/14-ctx-patch-contract.md` — load before a batched or non-trivial
  edit, and whenever `ctx_patch` rejects a call
- `references/appendix-cli-map.md` — compact CLI command map
- `references/appendix-mcp-tools.md` — MCP tool groups and profile caveats
- `references/appendix-paths-and-config.md` — config, env, path jail guidance
- `references/appendix-reference-docs.md` — generated reference documentation

## Must-remember gotchas

- Setup chain often flows: wrap → onboard → setup → bootstrap → init. (`install` is an alias for `setup`, not a separate step.)
- `update` may swap binary and rewire hooks; `setup` should not rewrite rules
  unless user opts in.
- `onboard`, `setup`, `init`, and `init --global` may edit shell profiles.
  Safer no-RC-edit paths: manual MCP config or `lean-ctx init --agent <tool>`.
- Under dotfile control, prefer manual eval snippet or
  `lean-ctx init --global --style=dropin` over automatic shell-hook flows.
- Do not store durable local policy in regenerated `AGENTS.md`; keep it in
  stable instruction/config files.
- Hook escapes: `lean-ctx-off`, `LEAN_CTX_DISABLED=1`, `LEAN_CTX_RAW=1`.
- Stale RC exports, proxy env, and `*.lean-ctx.bak` often explain surprises.
- Do not hardcode `LEAN_CTX_DATA_DIR` in editor MCP env unless deliberately
  using legacy single-dir behavior.
- Tool surface ≠ profile: `tools` changes visible tools; `profile` changes
  behavior/compression.
- Session project root can move: `ctx_*` access to a foreign tree — or a subagent
  or skill load in one — can re-root the session and jail tools out of the real
  project. Recover by reconnecting MCP, not by re-passing `cwd`.
- Compression can drop syntax: a compressed read has been seen omitting an
  `else`, inverting the control flow it displayed. NEVER conclude anything about
  branch structure from a compressed mode; re-read `full`/`raw` first.
- `ctx_search` and `ctx_glob` truncate at their result caps (defaults 20 and 200)
  with no marker, so a reported match count is a floor, not a total.
- `ctx_shell`'s `cwd` persists across calls; one out-of-tree `cwd` redirects
  every later relative-path command until it is passed again. Distinct from root
  capture — and unlike root capture, re-passing `cwd` IS the fix.
- `dry_run` does not check anchors: on anchored ops it answers "would apply"
  before opening the file, even for a fabricated hash. It MUST be a JSON boolean,
  because the string `"true"` reads as false and the edit applies.
- Archived `ctx_shell`/`ctx_execute`/`ctx_search`/`ctx_tree` output is retrievable
  with `ctx_expand(id=…)`; re-running the command pays for it twice.
- The advertised tool list is an advertising filter, not an access boundary:
  `ctx_call(name=<tool>)` resolves against the full registry.
- `ctx_patch` is standard anchored/batch path. `ctx_edit` is legacy/power-only.
- Standard-profile tools: `ctx_compose` (parallel dispatch). Power/dynamic tools: `ctx_plan`, `ctx_compile`,
  `ctx_radar`, `ctx_verify`, `ctx_load_tools`.
- Debug chain: `status`, `doctor`, `doctor integrations`, `doctor --fix`,
  `setup --fix`, `sessions doctor`, `cache prune`, `report-issue`.
- Proxy/service env can differ from foreground shell env.
- Trust generated appendices, `ctx_load_tools`, live tool lists, and `--help`
  over stale prose when docs drift.
- `auto_inject_rules` gates OpenCode/AGENTS.md and similar clients but NOT
  Claude Code CLAUDE.md; Claude Code uses separate `rules_injection` +
  `rules_scope`.
- `chmod 444` on target file does not stop injection: atomic temp-file+rename
  only needs writable containing directory.
- Rules injection is not the only writer. Writer commands (`setup`, `onboard`,
  `init`, `install`, `update`, `wrap`, `doctor --fix`, `skill`) also install
  lean-ctx's own vendored skill into each agent's skills directory, moving any
  file already there aside as `SKILL.md.bak`. Where skills are deployed from a
  source-of-truth repo, that silently replaces the deployed copy with upstream's
  — in every agent directory at once. The skill self-describes as "auto-installs
  if not present", but the observed behavior overwrites a file that IS present.

## Anti-patterns

- Do not read full files for orientation when `signatures`, `map`, or `task`
  mode answers faster.
- Do not patch with stale anchors repeatedly; refresh once, then reassess.
- Do not treat one repo's lean-ctx config as universal guidance.
- Do not point `ctx_*` tools or subagents at an out-of-project tree; use
  `ctx_git_read` for remote repos and the host's native read tool for local ones.
- Do not prescribe power-only tools unless the active profile exposes them.
- Do not read a capped result count or a "no matches" reply as proof of absence;
  confirm with a second query or a targeted read.
- Do not "correct" tool field names from the published MCP schema or from the
  server's own instructions block — both drift from the runtime. The error
  message is the contract.
- Do not reach for `ctx_execute` to get around a command `ctx_shell` blocked: it
  runs the identical gate, and differs only in write doctrine and command-size
  cap.
- Do not treat a lean-ctx writer command as read-only because the task was
  diagnostic. Where skills or rules files are deployed from a source of truth,
  re-deploy after any writer command rather than assuming it touched nothing.
- Do not use hook escapes or raw bypasses as normal workflow. Use them only for
  concrete debugging, interoperability, or recovery reasons, and return to
  lean-ctx tools/MCP when available.
