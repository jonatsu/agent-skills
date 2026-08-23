# Appendix: Upstream Reference Docs

> Source: upstream `docs/reference/` at pinned commit
> `5ad09b5030254e5368e91cbd419b07564f98ea95`
> ([browse](https://github.com/yvgude/lean-ctx/tree/5ad09b5030254e5368e91cbd419b07564f98ea95/docs/reference)).
> This appendix distills operational detail for agents — not a replacement for
> the full docs. Trust live `doctor`, `--help`, generated appendices, and
> `ctx_load_tools` over static prose when versions differ.
>
> **Read ONE section, never this whole file.** It is the largest file in the
> skill — larger than every other reference combined — and it is a snapshot of
> one upstream commit. Jump to the numbered section you need. If `--help`,
> `doctor`, or `ctx_discover_tools` can answer the question, ask them instead.
> For `ctx_patch` fields, `ctx_read` mode behavior, and path-jail mechanics, the
> measured files (`12`, `13`, `14`) outrank this one.

---

## 01 — Setup & Onboarding

**Covers:** `wrap`, `onboard`, `setup`, `bootstrap`, `init`, `doctor`, `status`,
`unwrap`.

### Three setup tiers

| Tier | Command | What it does |
|------|---------|--------------|
| One-command | `lean-ctx wrap <agent>` | MCP + shell hook + daemon + verify for one agent. Undo: `unwrap`. |
| All agents | `lean-ctx onboard` | Non-interactive, connects every detected tool. |
| Full control | `lean-ctx setup` | 12-step interactive wizard. |

### Setup level (first-run menu)

| Level | inject_rules | inject_skills | Meaning |
|-------|:---:|:---:|---------|
| Minimal (default) | ✗ | ✗ | Just MCP tools, no config-file edits |
| Standard | ✓ | ✗ | MCP tools + agent rules |
| Full | ✓ | ✓ | Tools + rules + skills + shell hooks |

Persisted to `config.toml` `[setup] auto_inject_rules` / `auto_inject_skills`.

### Key commands

```bash
lean-ctx wrap cursor              # one agent, one command
lean-ctx onboard                  # all agents, zero prompts
lean-ctx setup                    # 12-step wizard
lean-ctx setup --non-interactive --yes --fix --json  # CI/headless
lean-ctx bootstrap [--json]       # = setup --non-interactive --yes --fix
lean-ctx init --global            # shell aliases only
lean-ctx init --agent <name>      # single-agent MCP + rules + skill + hook
lean-ctx doctor                   # ~27 diagnostic checks
lean-ctx doctor --fix             # auto-repair
lean-ctx doctor integrations      # per-IDE wiring health
lean-ctx doctor --json            # machine-readable
lean-ctx status                   # fast yes/no connection check
lean-ctx status --json
lean-ctx unwrap <agent>           # restore pre-wrap state from snapshot
```

### Agent must know

- **`wrap` snapshots first** — every modified file has a `*.lean-ctx.bak` backup.
  `unwrap` restores from the snapshot manifest.
- **`onboard` is the golden path** for most users. `setup` is for when you need
  to decide about proxy, telemetry, auto-updates, compression level, tool profile.
- **Rules injection is opt-in.** `setup` step 4 only runs if you chose Standard
  or Full at the first-run menu. `--skip-rules` always wins.
- **`doctor integrations` checks every detected agent** — Cursor, Claude Code,
  Codex, VS Code, JetBrains (MCP snippet), etc. Hooks verified for staleness
  (stale binary path → `lean-ctx setup --fix`).
- **`bootstrap` is the CI path** — non-interactive, exits non-zero on failure.
- **Agent keys** for `init --agent`: cursor, claude, windsurf, codex, gemini,
  antigravity, copilot, crush, pi, qoder, cline, roo, kiro, verdent, qwen, trae,
  amazonq, opencode, hermes, vscode, zed, aider, continue, neovim, emacs, sublime.

### Caveats

- `setup` may edit shell profiles. Safer no-RC-edit paths: manual MCP config or
  `lean-ctx init --agent <tool>`.
- Under dotfile control, prefer `lean-ctx init --global --style=dropin`.
- `install` is now an alias for `setup` (was a UX bug — fixed).
- Data dir is `~/.lean-ctx` (not `~/.local/share/lean-ctx`).

---

## 02 — Daily Use

**Covers:** `ctx_read` modes, `ctx_search`/`ctx_glob`/`ctx_tree`/`ctx_shell`,
cache-aware rereads, anchored edits, `gain`, `tools` profile.

### Read modes

Upstream lists ten and omits `anchored`, which the `ctx_patch` workflow
requires; it is included here. Compressed modes drop syntax and truncate
silently — `13-silent-failure-modes.md` covers which, and when.

| Mode | Returns | Use when |
|------|---------|----------|
| `auto` | lean-ctx picks best | default |
| `full` | whole file, cached | you'll edit it |
| `anchored` | `LINE:HASH` anchors | before any anchored `ctx_patch` op |
| `map` | imports + API surface | context-only file |
| `signatures` | fn/type signatures only | need the API |
| `aggressive` | heavy compression | very large file |
| `entropy` | entropy-ranked lines | huge file, dense parts |
| `task` | lines relevant to task | task-focused |
| `reference` | reference handle | output too big to inline |
| `diff` | lines changed since last read | re-checking |
| `lines:N-M` | specific range | you know where |

### Search & navigation

| MCP tool | CLI | Purpose |
|----------|-----|---------|
| `ctx_search` | `lean-ctx grep` | Regex search |
| `ctx_semantic_search` | — | Meaning-based (BM25 + embeddings) |
| `ctx_glob` | `lean-ctx find` | File glob |
| `ctx_tree` | `lean-ctx ls` | Directory map |
| `ctx_compose` | — | One call: keywords + ranked files + matches + top symbol |

### Shell execution

```bash
lean-ctx -c "cargo test"          # compressed
lean-ctx -c "cargo test" --raw    # full output
lean-ctx -t "cargo build"         # tracked: full output + recorded stats
lean-ctx raw "cmd"                # skip compression (allowlist still applies)
```

### Tool profiles

```bash
lean-ctx tools minimal    # 5 essential tools
lean-ctx tools standard   # 16 tools (balanced, incl. ctx_patch)
lean-ctx tools power      # all tools (default for existing installs)
lean-ctx tools show       # current profile
```

### Agent must know

- **Cache-aware rereads:** unchanged file re-read costs ~13 tokens (session cache
  hit). Use `fresh=true` to bypass.
- **`ctx_compose` replaces search→read→outline→read chain** (3–5 calls → 1).
- **`tools` vs `profile`:** `tools` controls *which MCP tools* are exposed;
  `profile` controls *context profiles* (compression/read-mode behavior).
- **`gain` is the only place savings are shown** — no inline "↓80% saved" footers.
- **Shell allowlist** (~200 binaries) gates what gets compressed. `lean-ctx allow
  <cmd>` adds one; `lean-ctx allow --list` shows effective list.

### Caveats

- Semantic search needs an index — builds on first use, updates in background.
- After changing tool profile, restart the AI tool so it re-reads the tool list.
- `LEAN_CTX_RAW=1` skips compression; `LEAN_CTX_DISABLED=1` bypasses everything.

---

## 03 — Memory & Knowledge

**Covers:** Session (CCP) vs persistent knowledge, checkpoint/resume,
findings/decisions, `ctx_knowledge` operations, OKF export/import, gotchas.

### Two memory layers

| Layer | Scope | Storage | Recalled |
|-------|-------|---------|----------|
| Session (CCP) | one working session | `sessions/<id>.json` | auto on new session in same project |
| Knowledge | whole project, forever | `knowledge/<project-hash>/` | on demand + auto at session start |

### Session commands

```bash
lean-ctx session task "Refactor auth [40%]"
lean-ctx session finding "JWT validation in auth/verify.rs"
lean-ctx session decision "Use session cookies, not JWT"
lean-ctx session status / save / load [id] / reset
lean-ctx sessions list / show [id] / delete <id> / cleanup [days]
lean-ctx sessions doctor [--fix]    # diagnose/repair session restore
```

### Knowledge commands

```bash
lean-ctx knowledge remember "Payments use Stripe; secret in STRIPE_WH"
lean-ctx knowledge recall "how do payments work"
lean-ctx knowledge search "stripe"
lean-ctx knowledge status / health
lean-ctx knowledge consolidate [--all]   # import session + run lifecycle
lean-ctx knowledge export --output kb.json
lean-ctx knowledge export --format okf --output ./kb-okf   # portable Markdown
lean-ctx knowledge import kb.json --merge
```

### Agent must know

- **Auto-restore is invisible but critical:** new session in same project
  auto-injects prior session's context (findings, decisions, touched files,
  progress) as `ACTIVE SESSION` block. If it doesn't work → `lean-ctx sessions
  doctor`.
- **`session` (singular) records into current session; `sessions` (plural)
  manages the store** of saved snapshots.
- **Knowledge consolidation** (`consolidate`) imports session findings first,
  then runs memory lifecycle (decay, consolidate, archive, compact). Stores are
  capacity-bounded; overflow is archived losslessly (never hard-dropped).
- **OKF export** produces vendor-neutral, git-diffable Markdown bundles.
  Deterministic (byte-identical for same knowledge).
- **Gotchas** are auto-detected recurring error patterns stored in
  `knowledge/<hash>/gotchas.json`. View with `lean-ctx gotchas list`.
- **`ctx_overview`** is the ideal first call in a new session — task-relevant
  project map combining structure, recent knowledge, and task focus.

### Caveats

- Sessions are project-scoped — changing project root breaks auto-restore.
- `sessions/latest.json` is the pointer; `sessions doctor --fix` rebuilds it.
- Knowledge reclaim uses hysteresis: triggers only at cap, settles at 75%.
  `[memory.lifecycle] reclaim_enabled = false` to trim overflow only.

---

## 04 — Code Intelligence

**Covers:** Property graph, `ctx_graph`, `ctx_impact`, `ctx_callgraph`,
`ctx_repomap`, `ctx_architecture`, `ctx_smells`, `ctx_refactor`, `ctx_review`,
visualization, heatmap.

### The graph

One **property graph** (tree-sitter; language coverage varies by release) at
`graphs/<project-hash>/index.json.zst`. Builds lazily on first use. Matches are
name-based, not reference-exact — see `04-code-intelligence.md` before trusting
an "all usages" answer.

```bash
lean-ctx graph build / status
lean-ctx index build-graph / status
```

### Key tools (all in standard profile)

| Tool | Purpose | Key actions |
|------|---------|-------------|
| `ctx_graph` | Unified graph entry | `related`, `symbol`, `impact`, `context`, `diagram`, `enrich` |
| `ctx_impact` | Blast-radius analysis | `analyze`, `diff`, `chain` |
| `ctx_callgraph` | Caller/callee tracing | `callers`, `callees`, `trace`, `risk` |
| `ctx_repomap` | PageRank over symbol graph | `max_tokens`, `focus_files` |
| `ctx_architecture` | Layers, clusters, health | `overview`, `cycles`, `hotspots`, `health`, `entrypoints` |
| `ctx_smells` | 8 graph rules | `summary`, `scan`, `rules`, `file` |
| `ctx_review` | Automated review | `review`, `diff-review`, `checklist` |
| `ctx_refactor` | LSP-backed rename | `rename`, `references`, `definition` |

### Agent must know

- **`ctx_impact` before risky refactors** — returns everything transitively
  affected.
- **`ctx_repomap` is MCP-only** (no CLI). CLI users get similar via `lean-ctx
  overview`.
- **`ctx_review` combines impact + callers + test coverage + smells** in one
  automated review.
- **`ctx_refactor` requires the relevant language server.** Configure under
  `[lsp]` if auto-detection misses one.
- **`lean-ctx heatmap`** shows which files get touched most — risk concentration.

### Caveats

- Graph is shared by `graph`, `impact`, `callgraph`, `repomap`, `architecture`,
  `smells` — not obvious from command names.
- Index scanning disabled with `LEAN_CTX_NO_INDEX=1` /
  `LEAN_CTX_DISABLE_SEARCH_INDEX=1`. Bounded with `graph_index_max_files`.

---

## 05 — Advanced & Integrations

**Covers:** Proxy lifecycle/history modes, multi-repo/RRF, provider registry,
local metering, routing aliases/tiers, gateway hardening/keys, `ctx_tools`
gateway, hooks/hook_binary, Claude OAuth vs API key, insecure/custom upstream
gates, `ctx_provider`, `ctx_pack`, `ctx_agent`/`ctx_handoff`/`ctx_share`.

### Proxy

```bash
lean-ctx proxy enable / disable / status / start / stop / cleanup
lean-ctx proxy token [--quiet]
```

**History modes** (`[proxy].history_mode` / `LEAN_CTX_PROXY_HISTORY_MODE`):

| Mode | Behaviour | Use when |
|------|-----------|----------|
| `cache-aware` (default) | Prune at frozen 16-msg strides, ≥8 recent intact | Prompt caching in play |
| `rolling` | Summarize >6 msgs old, every turn | Max raw-token reduction |
| `off` | Never prune (compression still applies) | Debugging / client manages history |

### Provider registry (`[[proxy.providers]]`)

Declare any OpenAI/Anthropic/Gemini-compatible endpoint as data:

```toml
[[proxy.providers]]
id = "foundry"
shape = "openai"
base_url = "https://acme.services.ai.azure.com"
api_key_env = "FOUNDRY_API_KEY"   # gateway-held key (optional)
local = true                       # bill at shadow rate
```

- `api_key_env` set → gateway holds credential, strips caller's.
- `local` → booked at `local_shadow_rate` instead of cloud list prices.
- Invalid entries logged/skipped; registry hot-reloaded from `config.toml`.

### Routing (`[proxy.routing]`)

```toml
[proxy.routing]
enabled = true
[proxy.routing.aliases]
"acme/fast" = "foundry:Phi-4-mini-instruct"
"claude-opus-4-5" = "claude-sonnet-4-5"
[proxy.routing.tiers]
fast = "foundry:Phi-4-mini-instruct"
standard = ""    # keep requested model
premium = ""     # never auto-downgraded
```

**Fail-open by construction:** any miss forwards unchanged.

### Gateway mode

```toml
proxy_bind_host = "0.0.0.0"
proxy_allowed_hosts = ["ai-gateway.example.com"]
proxy_max_rps = 100
```

- Non-loopback bind → provider-API-key auth fallback **hard-disabled**.
- Host allowlist extends loopback-only guard.
- Token-bucket rate limit activates (default 50 rps).
- `gateway-keys.toml`: per-person SHA-256 hashed bearer keys for metering
  identity.

### Gateway server (`--features gateway-server`)

```bash
lean-ctx gateway serve --port=8484 --admin-port=8485
lean-ctx gateway init pilot --org="Acme AG" --seats=800
lean-ctx gateway doctor --dir .
lean-ctx gateway keys add --person=bob@acme.com --team=core
lean-ctx gateway report --out=q3.html
```

### Agent must know

- **Claude Pro/Max subscriptions need an API key for proxy.** OAuth token
  rejected by custom `ANTHROPIC_BASE_URL` → login loop. `proxy enable` skips
  Claude redirect when no `ANTHROPIC_API_KEY` detected.
- **`LEAN_CTX_*_UPSTREAM` env vars are start-time only.** For service-managed
  proxy, use `config.toml` (live-reloaded every ~2s). MCP clients launch with
  stripped env → env vars invisible to proxy.
- **`lean-ctx doctor` warns on upstream drift** (env override masking config).
- **Insecure HTTP upstream** requires `allow_insecure_http_upstream = true` or
  `LEAN_CTX_ALLOW_INSECURE_HTTP_UPSTREAM=1`. Only for trusted local network.
- **Custom HTTPS upstream** requires `allow_custom_upstream = true` or
  `LEAN_CTX_ALLOW_CUSTOM_UPSTREAM=1`.
- **Counterfactual baseline** (`[proxy.baseline]`): `reference_model` +
  `local_shadow_rate_per_mtok` make avoided-cost claims auditable.
- **Provider-verified savings** (`proxy.counterfactual_metering`): uses
  Anthropic's free `count_tokens` endpoint for verified input-token counts.
  Anthropic only.
- **`ctx_provider`** brings GitHub/GitLab/Jira/Postgres into context. Auth via
  env tokens. Pipeline: execute → consolidate → BM25 + graph + knowledge.
- **`ctx_pack`** bundles curated context for sharing/CI.
- **Multi-agent tools** (`ctx_agent`, `ctx_handoff`, `ctx_share`) covered in
  detail in Journey 08.

### Caveats

- `proxy enable` modifies shell RC. Backup at `*.lean-ctx.bak`.
- `skip_agent_aliases = true` disables agent CLI aliases without affecting shell
  compression hook.
- Gateway server: admin listener binds `127.0.0.1` by default. Widening is
  explicit via `admin_bind_host`.

---

## 06 — Lifecycle

**Covers:** `update`, `uninstall`, `stop`, `restart`, `dev-install`, cache
maintenance, emergency recovery, platform notes, `report-issue`.

### Key commands

```bash
lean-ctx update [--check] [--insecure] [--skip-rules]
lean-ctx update --schedule [6h|12h|notify|off|status]
lean-ctx uninstall [--keep-config] [--keep-binary] [--dry-run]
lean-ctx stop              # stop ALL processes (daemon, proxy, orphans)
lean-ctx restart           # restart daemon (applies config.toml changes)
lean-ctx dev-install       # build release + atomic install + restart (dev only)
lean-ctx cache list / stats / invalidate <file> / clear / reset [--project] / prune
lean-ctx report-issue      # pre-filled GitHub issue with diagnostics
```

### Agent must know

- **`update` runs `post_update_rewire`** — refreshes MCP configs so editor
  reconnects to new binary. Only touches rules if you opted in.
- **`update` verifies SHA256 checksum** — refuses unverifiable binary unless
  `--insecure`.
- **`uninstall` order:** stop processes → clean RC files → MCP configs/rules →
  hooks/skills → autostart → backups → data dir → binary. Package-manager and
  in-repo dev installs are NOT touched.
- **macOS: proxy runs as LaunchAgent with `KeepAlive=true`.** Plain `kill` will
  be respawned. Always `lean-ctx stop` before manually replacing binary.
- **macOS privacy (#356):** daemon/proxy/updater LaunchAgents run under
  `sandbox-exec` with Seatbelt profile denying `~/Documents`, `~/Desktop`,
  `~/Downloads` — prevents TCC prompt on every update.
- **Emergency:** `lean-ctx-off` disables aliases for current session.
  `LEAN_CTX_DISABLED=1` bypasses all compression.
- **`cache invalidate <file>`** for surgical eviction; `cache reset --project`
  wipes only current project.

### Caveats

- `dev-install` builds from source (`cargo build --release`) — takes minutes.
  Normal users use `lean-ctx update`.
- Windows: no LaunchAgent/systemd equivalent; proxy/daemon run on demand.
- Path display normalized to forward slashes even on Windows.

---

## 07 — Context Engineering

**Covers:** radar→plan→compile→control/ledger pipeline, `ctx_compose` one-call
primitive, `ctx_expand` escape hatch, `ctx_workflow` evidence, power/dynamic
tools, `ctx_execute` sandbox, verification/proofs.

### The pipeline

```
radar (measure) → plan (allocate) → compile (materialize) → control/ledger (adjust)
```

| Tool | Purpose | Key actions/params |
|------|---------|--------------------|
| `ctx_radar` | Full budget breakdown | `format=display\|json` |
| `ctx_plan` | Phi-scored budget allocation | `task`, `--budget`, `profile` |
| `ctx_compile` | Knapsack + Boltzmann view selection | `--mode=compressed`, `--budget` |
| `ctx_control` | Overlay-based manipulation | `pin`, `exclude`, `set_priority`, `reset` |
| `ctx_ledger` | Pressure management | `status`, `evict`, `prune`, `reset` |

### Proactive context

| Tool | Purpose |
|------|---------|
| `ctx_compose` | One call: keywords + ranked files + matches + top symbol |
| `ctx_preload` | Load task-relevant files; compact L-curve summary (~50–100 tok) |
| `ctx_prefetch` | Predictive prefetch of blast-radius files |
| `ctx_fill` | Fill remaining budget with most coverage-effective files |
| `ctx_dedup` | Detect/remove duplicated content across files |

### Dynamic tool loading

```text
ctx_discover_tools query="impact analysis"
ctx_call name=ctx_impact arguments={...}
ctx_load_tools action=load category=arch
ctx_load_tools action=list
```

Categories: `arch`, `debug`, `memory`, `metrics`, `session`.

### Verification & proofs

```bash
lean-ctx verify --format both
lean-ctx proof export              # ContextProof artifact for audit
lean-ctx benchmark run / compare / scorecard
```

### Agent must know

- **`ctx_compose` is the highest-leverage everyday power tool** — replaces
  search→read→outline→read chain.
- **`ctx_expand` is the escape hatch** — zero-loss retrieval of archived tool
  output by id. Nothing is ever lost, only deferred.
- **`ctx_workflow` enforces evidence-tracked state machine** (plan→implement→
  verify→ship). Agent can't claim "done" without recorded evidence.
- **`ctx_execute` runs sandboxed** (11 languages). Only stdout enters context.
- **Most tools here are power profile.** Load on demand with `ctx_load_tools` or
  `ctx_call`.
- **`ctx_verify`/`ctx_proof`** make savings provable — useful in CI to assert
  context budget.

### Caveats

- `ctx_compose` builds on `ctx_search` — results are deliberately terse (header +
  one line per hit).
- `ctx_control` overlays are reversible and scoped (`call`, `session`, `project`).

---

## 08 — Multi-Agent Collaboration

**Covers:** `ctx_agent` sync, presence/messages/diaries/shared
knowledge/handoffs/tasks/context share, privacy/import flags, stale cleanup,
crypto audit, per-agent cost.

### Mental model

| Layer | Tool | Analogy |
|-------|------|---------|
| Presence | `ctx_agent` register/status/list | "who's online" |
| Messaging | `ctx_agent` post/read | team chat channel |
| Long-term notes | `ctx_agent` diary | each agent's lab notebook |
| Fact sharing | `ctx_agent` share_knowledge | shared whiteboard |
| Work transfer | `ctx_handoff`, `ctx_agent handoff` | baton pass |
| Task tracking | `ctx_task` | shared task board |
| Context transfer | `ctx_share` | "here, look at these files I already loaded" |

### Key operations

```text
ctx_agent action=register agent_type=cursor role=dev
ctx_agent action=status status=active message="implementing auth"
ctx_agent action=list / info / sync
ctx_agent action=post message="auth done" category=status [to_agent=<id>]
ctx_agent action=read                  # poll messages
ctx_agent action=diary category=discovery content="rate limiting in mw/rl.rs"
ctx_agent action=recall_diary / diaries
ctx_agent action=share_knowledge message="db=postgres;cache=redis"
ctx_agent action=receive_knowledge
ctx_agent action=handoff to_agent=<id> message="finished; please test"
```

### Handoff bundles (`ctx_handoff`)

```text
ctx_handoff action=create paths=["src/auth.rs","src/mw/rl.rs"]
ctx_handoff action=export write=true filename=auth-handoff.json
ctx_handoff action=pull path=auth-handoff.json
ctx_handoff action=import path=auth-handoff.json
```

Import flags: `apply_workflow`, `apply_session`, `apply_knowledge` (all default
`true`). Contradictions surfaced, not silently merged.

### Task orchestration (`ctx_task`)

```text
ctx_task action=create description="add OAuth" to_agent=<id>
ctx_task action=list / get / update / message / cancel
```

### Agent must know

- **`ctx_agent sync` is the "home screen"** — agents, statuses, unread messages,
  shared contexts in one response.
- **Diary vs shared_knowledge:** diary is private, persistent per-agent log
  (capped 100 entries). shared_knowledge is team broadcast (capped 500 facts).
- **Stale agents auto-pruned after 24h** — registry never fills with dead PIDs.
- **Messages carry `privacy` level** (Team by default) and are marked read
  per-agent.
- **`ctx_share` moves already-compressed cached context** between agents — token
  optimization, not re-reading.
- **Per-agent cost:** `lean-ctx gain --agents`, `ctx_cost action=agent`.
- **Crypto identity:** each agent has `keys/<agent-id>.key` / `.pub` for
  tamper-evident audit (`audit/trail.jsonl`).

### Caveats

- These tools are MCP-only (agents call them). No per-agent CLI beyond `buddy`.
- `ctx_agent` is standard profile; `ctx_task`, `ctx_handoff`, `ctx_share` are
  power profile.

---

## 09 — Team, Cloud & CI

**Covers:** CI integration, machine-readable output, team/shared config,
deterministic validation, automation caveats, cloud account sync, contribute.

### Team server

```bash
lean-ctx team serve --config team.toml
lean-ctx team token create --config team.toml --id ci-bot --scopes search,graph
lean-ctx team sync --config team.toml [--workspace <id>]
```

**Token scopes:** `search`, `graph`, `artifacts`, `index`, `events`,
`sessionmutations`, `knowledge`, `audit`. Least-privilege by design.

**Managed connectors** (declared in team config `connectors[]`):
- Providers: `github`, `gitlab`
- Resources: `issues`, `merge_requests`, `pipelines`
- `intervalSecs` clamped to 300s floor
- Credential lives only in injected `team.json`, never written to disk

### Cloud account (optional)

```bash
lean-ctx register <email> / login <email> / forgot-password <email>
lean-ctx sync                      # push local data to cloud
lean-ctx contribute                # anonymized compression data points
lean-ctx cloud pull-models         # refreshed adaptive compression models
lean-ctx upgrade                   # account/plan upgrade
```

### CI usage

```bash
lean-ctx bootstrap [--json]        # zero-prompt setup, exits non-zero on failure
lean-ctx serve                     # MCP server (stdio) for agent runners
lean-ctx daemon                    # background daemon
```

### Agent must know

- **`bootstrap` is the CI path** — never hangs on a prompt.
- **Provider tokens in CI** read from environment variables, never prompts.
- **`ctx_proof`/`ctx_verify`** as CI gates: "the context bundle this PR relies on
  is reproducible."
- **Cloud is opt-in.** Default signed-out state reports "Not connected to
  LeanCTX Cloud."
- **`contribute` is anonymized and aggregate** — distinct from personal `sync`.

### Caveats

- Three "share" concepts easy to conflate: team index / personal cloud sync /
  anonymized contribute.
- `team sync` runs `git fetch` on configured workspaces — run on a timer.

---

## 10 — Customization & Governance

**Covers:** Tool profile vs compression/read profile distinction,
minimal/standard/power, profile management/tuning, compression levels, config
file, themes, custom filters, rules governance, `harden`.

### Compression levels

```bash
lean-ctx compression [off|lite|standard|max]
```

| Level | When |
|-------|------|
| `off` | debugging lean-ctx itself |
| `lite` | **default** — plain prose, max fidelity |
| `standard` | balanced — denser symbolic output |
| `max` | aggressive — smallest context |

Each level expands into 4 coordinated components: agent prompt, output density,
CRP mode, token-model tuning.

### Tool profiles (MCP surface)

```bash
lean-ctx tools minimal    # 5 tools
lean-ctx tools standard   # 16 tools (incl. ctx_patch)
lean-ctx tools power      # all tools (default fallback)
```

### Context profiles (behavior tuning)

```bash
lean-ctx profile list / active / show <name> / diff <a> <b>
lean-ctx profile create <name> / set <name>
```

### Config management

```bash
lean-ctx config [show|init|schema|validate]
lean-ctx config set <key> <value>
lean-ctx config apply              # apply to running daemon
```

After editing daemon-read config: `lean-ctx restart`.

### Governance

```bash
lean-ctx rules status / init / diff / lint / sync
lean-ctx export-rules              # high-confidence knowledge → rules files
lean-ctx harden [--hard] [--undo]  # deny native Read/Grep
```

### Agent must know

- **`tools` vs `profile` is the single most confused pair.** `tools` = which MCP
  tools; `profile` = how they behave (compression/read-mode).
- **`compression` expanding into 4 hidden components** — why one flag changes
  agent behavior AND output.
- **`harden` is the strongest token-discipline lever.** Soft: sets
  `LEAN_CTX_HARDEN=1` in MCP configs. Hard: also adds Bash to Claude Code
  `permissions.deny`. Fully reversible with `--undo`.
- **`export-rules` closes the loop** from "learned once" to "always known."
- **Overrides precedence:** env → per-project `.lean-ctx.toml` → global
  `config.toml`.

### Caveats

- Default tool profile is `power` (backward compatible). Run `lean-ctx tools
  standard` to trim.
- `harden` denies native Read/Grep except immediately after an Edit (edit-verify
  still works).

---

## 11 — Analytics & Insights

**Covers:** `gain`/metrics/cost/radar/heatmap/benchmark/verify/proof,
interpreting savings, local-vs-proxy accounting, `savings` ledger, `token-report`,
`discover`/`ghost`, `dashboard`, `watch`, `cep`, `benchmark scorecard`.

### `gain` — the savings dashboard

```bash
lean-ctx gain [--live|--graph|--daily|--cost|--score|--tasks|--agents|--heatmap]
lean-ctx gain --wrapped [--period=month]
lean-ctx gain --svg [--period=all]        # shareable SVG card
lean-ctx gain --share [--base-url=...]    # self-hostable HTML page
lean-ctx gain --deep                      # everything in one shot
lean-ctx gain --json                      # machine-readable
```

### Verified savings ledger

```bash
lean-ctx savings                   # summary: gross, bounce, net, tokenizer, integrity
lean-ctx savings verify            # re-walk SHA-256 hash chain
lean-ctx savings export            # every event as JSON
```

Per-event, append-only, local-only, on by default. Opt out: `LEAN_CTX_SAVINGS_LEDGER=off`.

### Other analytics

```bash
lean-ctx token-report              # tokens + memory footprint
lean-ctx discover                  # uncompressed commands in shell history
lean-ctx ghost [--json]            # hidden token waste
lean-ctx slow-log list / clear     # slowest compressed commands
lean-ctx tee list / last / show <id> / clear   # captured output logs
lean-ctx dashboard [--port 4000]   # web UI at localhost:3333
lean-ctx dashboard --vscode        # open as editor tab
lean-ctx watch                     # live TUI event stream
lean-ctx cep                       # CEP score trends
lean-ctx benchmark run / report / eval / scorecard
lean-ctx gotchas list / stats / export / clear
lean-ctx learn [--apply]           # promote gotchas into rules
lean-ctx stats [json|reset-cep]
lean-ctx compact [path]            # compress stored agent transcripts
```

### Agent must know

- **Analytics is pull model** — nothing added to agent context. Savings live in
  CLI/dashboard.
- **`gain` bridge states:** `OFF` (proxy down → unmeasured), `proxy up, 0
  requests` (editor not routed), `connected` (engaged, numbers real).
- **`savings` ledger is auditable:** tokenizer transparency (`o200k_base`),
  bounce-netting (realized saving, not gross upper bound), tamper-evident
  SHA-256 chain.
- **`benchmark scorecard` is reproducible** — deterministic corpus, pure BM25,
  `determinism_digest` for self-verification.
- **Edit efficiency measured per applied op** — `ctx_metrics` shows anchored vs
  str_replace savings. A/B benchmark: `cargo test --test edit_reliability`.
- **`discover` + `ghost`** find waste you're not catching.

### Caveats

- `gain` only counts savings the bridge actually realised — proxy must be running
  AND intercepting.
- `savings` uses `o200k_base` tokenizer as proxy; your model's tokenizer may
  differ a few percent.
- `dashboard --vscode` requires the lean-ctx editor extension.

---

## 12 — Troubleshooting

**Covers:** `doctor`/`status`/`logs`/`cache`/`index` recovery, common failure
modes, safe escalation/reporting, `ctx_edit` migration to `ctx_patch`.

### 30-second triage

```bash
lean-ctx status                    # fast yes/no (5-line summary)
lean-ctx doctor                    # ~27 checks
lean-ctx doctor integrations       # per-IDE: MCP + hook freshness + rules
```

### Common failure modes

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| Agent ignores lean-ctx | `doctor integrations` | `setup --fix` + restart editor |
| CLI vs editor read different config | `doctor` flags stray `config.toml` in data dir | `doctor --fix` |
| `gain` shows zero | `ghost` / `discover` | verify proxy + hook |
| New chat has no memory | `sessions doctor` | `sessions doctor --fix` |
| Read/Grep denied | harden mode active | `harden --undo` |
| Shell broken after install | RC modified | `doctor --fix` / `proxy disable` |
| Search/index stuck | `index status` | `cache prune` |
| Broke after update | `doctor integrations` | `setup --fix` |
| `ctx_edit` missing | power-only since v3.8.12 | use `ctx_patch` or `lean-ctx tools power` |

### Agent must know

- **Most common cause of "not working": editor wasn't restarted** after config
  change.
- **`ctx_edit` (str_replace) is power-only since v3.8.12.** `ctx_patch`
  (anchored editing) is the successor, in standard profile. Client-aware
  advertising: clients with trusted native editor don't see `ctx_patch` in
  default surface.
- **`prefer_native_editor = true`** hides both edit tools by design (#454).
- **`report-issue`** gathers redacted diagnostic bundle for bug reports.

### Caveats

- `doctor --fix` re-runs merge-based setup — repairs MCP/rules/hook drift.
- `sessions doctor --fix` rebuilds `latest.json` pointer.
- `cache prune` removes oversized/quarantined/orphaned indexes.

---

## 13 — Security & Governance

**Covers:** Security posture, bind/auth/allowlist/rate limits, token/key
handling, SSRF/insecure-upstream boundaries, safe deployment, PathJail, shell
allowlist, secret redaction, OS sandbox, harden, role policies, workspace trust,
sensitivity policy floor.

### Defense-in-depth (all on by default)

```
ctx_read/ctx_shell → PathJail → Shell allowlist → OS sandbox → Secret redaction → result
```

### Posture control

```bash
lean-ctx security status           # posture board: jail, shell, secret redaction
lean-ctx yolo                      # OPEN: any path + any command (containment off)
lean-ctx secure                    # STRICT: restore secure defaults
lean-ctx security secrets off/on   # toggle secret redaction (separate from yolo)
```

Two independent planes: **containment** (machine from agent) and **secret
defense** (secrets from provider). `yolo` only drops containment.

### PathJail

Confines file access to resolved project root. Multi-root setups jail each root
independently. Widen via `allow_paths`/`extra_roots`; disable via `path_jail =
false`.

### Workspace trust

```bash
lean-ctx trust              # trust current project's .lean-ctx.toml
lean-ctx trust status       # show trust state + gated overrides
lean-ctx untrust            # revoke
```

Trust pinned to **both** path AND content hash of `.lean-ctx.toml` — editing
after trust re-gates it.

### Shell security modes

```toml
shell_security = "enforce"   # default — allowlist + hard blocks
shell_security = "warn"      # log violations, block nothing
shell_security = "off"       # skip gating entirely (compression stays on)
```

### Secret redaction (on by default)

```toml
[secret_detection]
enabled = true
redact = true
custom_patterns = ["MYCORP_[A-Z0-9]{20}"]
exclude_patterns = ["LCTX_PUBLIC_\\w+"]
```

### Sensitivity policy floor (off by default)

```toml
[sensitivity]
enabled = true
policy_floor = "secret"    # public < internal < confidential < secret
action = "redact"           # or "drop"
```

Levels: `secret` (secret-like paths/credentials), `confidential` (card
numbers/IBANs), `internal` (explicit tagging), `public` (default). Classifier
uses only high-precision signals.

### OS sandbox

`ctx_execute` runs under Seatbelt (macOS) or Landlock (Linux). macOS
LaunchAgents run under `sandbox-exec` with deny-`~/Documents` profile (#356).

### Agent must know

- **`lean-ctx security status`** shows live posture: STRICT/RELAXED/OPEN.
- **`yolo` is reversible** — `lean-ctx secure` restores defaults. Re-enable
  pieces granularly afterwards.
- **Docker/podman deliberately NOT in default shell allowlist** — mount flags can
  bypass PathJail.
- **`shell_strict_mode = true`** blocks `$()` and backticks.
- **`harden`** denies native Read/Grep (except after Edit). Soft: MCP config
  only. Hard: also blocks Claude Bash tool.
- **Role policies** scope what a session may do (e.g. reviewer cannot write).
- **Audit trail** (`audit/trail.jsonl`) + OWASP alignment map for security
  reviews.
- **CGB self-assessment:** graded C2 — Managed with declared gaps.

### Caveats

- `sensitivity` policy floor lives in **global** `config.toml` only — untrusted
  project file cannot lower it.
- `shell_security = "off"` disables command gating only; does NOT lift
  read-only-output doctrine (no `>`/`tee`/heredoc file writes).
- `lean-ctx doctor` surfaces relaxed security posture whenever not `enforce`.
