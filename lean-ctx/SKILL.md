---
name: lean-ctx
description: Use for lean-ctx and its ctx_* MCP tools — ctx_read, ctx_search, ctx_glob, ctx_tree, ctx_shell, ctx_patch, ctx_call, ctx_expand, ctx_git_read — plus shell hook, MCP config, profiles, compression, proxy, doctor, wrap/onboard/setup/update, and rules injection. Use when picking a read mode or edit op; when a ctx_* call returns a suspicious, empty, truncated, or suspiciously complete result; when an edit is rejected or an anchor goes stale; when a read shows a [REDACTED:...] marker, a text file starts reading as binary, or a patched script loses its +x bit; when a read returns an "already in this conversation" stub; or when path-jail, project-root, install, config, or debugging problems appear.
metadata:
  author: Joonas Onatsu
  license: Apache-2.0
---

# lean-ctx

IRON LAW: Prefer lean-ctx context tools before raw read/search/shell/patch tools
when available. Keep context lean, recoverable, and verifiable. Do not assume
one host, editor, path layout, or config; inspect active tools and local setup
first.

**When lean-ctx is absent, this skill still applies — as a stop rule.** If no
`ctx_*` tools are listed this session, lean-ctx is not active here: use the
host's native read/search/shell/edit tools throughout, say once that you are
doing so, and skip the rest of this skill. NEVER wait for `ctx_*` tools to
appear, NEVER guess a tool name, and NEVER install lean-ctx to satisfy this
rule. A missing tool is a fallback, not a task.

## Three questions that decide everything here

**Reading — what do I actually need from this file?** The mode is the decision,
not an afterthought. API surface → `signatures`. Structure → `map`, and it is the
only structural mode for md/json/yaml/toml. About to edit → `anchored`. Exact
bytes → `raw`, paged with `start_line`+`limit`, because it truncates at an output
cap. Never `full` for orientation: reading more is not understanding more.

**Trusting — could this result be lying to me?** Ask before acting, because each
of these returns a plausible success. A count at 20 or 200 is a floor, never a
total. A short shell list may be silently clipped — ask for `| wc -l` in the same
call. Branch structure read from a compressed mode is not evidence. A
`[REDACTED:…]` marker is usually a display artifact, so check it with a native
read, never with `ctx_shell`, which redacts its own stdout and will confirm the
phantom.

**Editing — what is the smallest op that fails loudly?** Prefer `replace_unique`:
no anchored read, no hash to go stale, and a non-unique match errors instead of
editing the wrong line. Reach for `replace_all` only knowing it rewrites the file
at `0600` and strips `+x`. Anchored ops need a fresh `anchored` read; on CONFLICT
retry once from the anchors the error hands back, then stop. Never use `dry_run`
to check an anchor — it answers before opening the file.

Then verify with the repo's own checks, never with a `ctx_*` read of what you
just wrote.

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

Load by symptom, one at a time. The trigger is the whole point — a ref read
speculatively costs more than the trap it would have prevented.

- `references/13-silent-failure-modes.md` — when a `ctx_*` result looks wrong,
  empty, or suspiciously complete: a match count you doubt, a shell list that
  seems short, a `[REDACTED:…]` marker, or a read returning an "already in this
  conversation" stub.
- `references/14-ctx-patch-contract.md` — before a batched or non-trivial edit,
  before a rename or path sweep, and whenever `ctx_patch` rejects a call or an
  anchor goes stale. This file is the field-name authority; nothing else here is.
- `references/12-troubleshooting.md` — when a path tool reports `path escapes
  project root`, when rules files keep being rewritten, or when a deployed
  `SKILL.md` changes on its own.
- `references/01-setup-and-onboarding.md` — before running `wrap`, `onboard`,
  `setup`, `init`, or `update`, or when a setup step wants to edit shell RC files.
- `references/04-code-intelligence.md` — before trusting a symbol, callgraph, or
  "all usages" answer, and when choosing between lean-ctx and a real LSP for a
  rename.
- `references/05-advanced.md` — when reaching for a power-profile tool, the
  proxy, or the shell hook, and when `ctx_shell` refuses a redirect.
- `references/06-lifecycle.md` — after a `lean-ctx update`, or when a fix you
  just installed appears not to work.
- `references/appendix-paths-and-config.md` — before changing a config key,
  especially a path-jail key.
- `references/appendix-mcp-tools.md` — to find which tool does a job and which
  profile exposes it. Trust the per-row `Profile` column, not any total.
- `references/appendix-reference-docs.md` — **the largest file here, bigger than
  the rest combined.** Load ONE named section (e.g. `## 09 — Team, Cloud & CI`),
  never the file, and only for upstream surface no other ref covers:
  memory/knowledge, multi-agent, team/cloud/CI, analytics, security posture.

Do NOT load:

- Do NOT load any ref for a routine read, search, or edit. The gotchas below
  cover the traps that actually recur.
- Do NOT load `appendix-reference-docs.md` whole, and do NOT load it for anything
  `--help`, `doctor`, or `ctx_discover_tools` answers live. It is a snapshot
  pinned to one upstream commit; live state outranks it.
- Do NOT load a second ref speculatively "while you are here". Pick by symptom,
  read it, act.

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
- `replace_all` rewrites the file at `0600`, silently stripping `+x` from a script
  while the index keeps `100755`. The edit reports success and `git status` stays
  clean, so prefer `replace_unique` for sweeps and `chmod` back if `replace_all`
  touched an executable.
- Read-dedup is cross-agent: a file a subagent read returns as an
  `[unchanged … read-dedup]` stub in your own context, claiming it is "already in
  this conversation above" when it is not. It intercepts native reads too. Recover
  with `fresh=true`, never by re-issuing the identical read.
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
