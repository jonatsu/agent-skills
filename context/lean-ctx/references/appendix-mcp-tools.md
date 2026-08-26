# Appendix — MCP Tool Map

> Source: upstream `yvgude/lean-ctx` generated registry
> (`docs/reference/generated/mcp-tools.md`) and profile map
> (`docs/reference/appendix-mcp-tools.md`).
> Pinned commit: `5ad09b5030254e5368e91cbd419b07564f98ea95`.
> Trust live `ctx_discover_tools` / `ctx_load_tools list` over this file.
>
> **This file is an inventory, not a contract.** For `ctx_patch` field names and
> `ctx_read` mode behavior, `14-ctx-patch-contract.md` and
> `13-silent-failure-modes.md` are authoritative — they are measured against a
> running server, this table is copied from a pinned snapshot.

Eighty tools are documented below. The **Profile** column shows the smallest tool
profile that exposes each one (`M` minimal, `S` standard, `P` power). Set your
profile with `lean-ctx tools <minimal|standard|power>`.

## Tool profiles at a glance

**No total is given here on purpose.** The snapshot's own numbers disagree with
its rows — the prose named 5 minimal and 16 standard tools while the table marks
7 rows `M` and 20 `S`, and three different grand totals appeared in one file.
Counts drift every release and nothing here fails loudly when they do. Ask the
running server instead:

```text
lean-ctx tools show          # active profile
ctx_discover_tools query=""  # everything reachable right now
```

Documented membership, as a starting point only:

- **minimal:** `ctx_read`, `ctx_shell`, `ctx_search`, `ctx_glob`, `ctx_tree` —
  plus `shell` (an alias of `ctx_shell`) and `ctx_session`, which carry `M` in
  the table below.
- **standard adds:** `ctx_compose`, `ctx_explore`, `ctx_knowledge`,
  `ctx_callgraph`, `ctx_graph`, `ctx_delta`, `ctx_execute`, `ctx_expand`,
  `ctx_overview`, `ctx_url_read`, `ctx_patch`. Further rows are marked `S`
  below; where the two disagree, believe the live tool list.
- **power:** everything remaining.

---

## 1. Core — read / search / shell

| Tool | Purpose | Key params / actions | Profile |
|------|---------|----------------------|---------|
| `ctx_read` | Read a file with session cache + compression; re-reads ~13 tokens when unchanged. **`anchored` is required before any anchored `ctx_patch` op** and is missing from upstream's mode list. Compressed modes drop syntax and truncate silently — see `13-silent-failure-modes.md` | `path`*, `mode` (full\|raw\|map\|signatures\|**anchored**\|diff\|aggressive\|entropy\|task\|reference\|lines:N-M\|auto), `start_line`, `limit`, `fresh` | M |
| `ctx_multi_read` | Read many files in one call (same modes). Deprecated → use `ctx_read` with `paths=['a.rs','b.rs']` | `paths[]`*, `mode`, `fresh` | S |
| `ctx_smart_read` | Auto-pick the optimal read mode for a file. Deprecated → `ctx_read` auto-selects mode when omitted | `path`* | P |
| `ctx_delta` | Incremental diff — only lines changed since last read | `path`* | S |
| `ctx_edit` | Legacy search-and-replace edit; preimage guards, backup. Prefer `ctx_patch` | `path`*, `new_string`*, `old_string`, `replace_all`, `create` | P |
| `ctx_patch` | **Hash-anchored line edits.** Ops: `set_line`, `replace_lines`, `insert_after`, `delete`, `replace_symbol`, `replace_unique`, `replace_all`, `create`. The anchored ops need `ctx_read(mode="anchored")` first. **Do NOT take field names from this row — see `14-ctx-patch-contract.md`, which is measured against the runtime.** Two traps that used to live here and were wrong: the replacement field is `new_text`, never `new_body`; and batches are NOT all-or-nothing — a failed op does not stop later ops, so verify each intended change landed | `path`*, `ops[]` — per-op fields in `14-ctx-patch-contract.md` | S |
| `ctx_fill` | Budget-aware context fill within a token limit | `paths[]`, `budget`*, `task` | P |
| `ctx_symbol` | Read just one named symbol block (fn/struct/class). Deprecated → `ctx_search(action="symbol")` | `name`*, `file`, `kind` | P |
| `ctx_outline` | List all symbols of a file with signatures (tree-sitter; language coverage varies by release) | `path`*, `kind`, `match`, `format` | P |
| `ctx_retrieve` | Fetch uncompressed original from cache (CCR) | `path`*, `query` | P |
| `ctx_shell` | Run shell commands with pattern compression (~95 patterns) | `command`*, `raw`, `cwd`, `env`, `timeout_ms` | M |
| `shell` | Alias of `ctx_shell` (same compression) for clients whose model reaches for a native `shell`/`bash` tool | `command`*, `raw`, `cwd` | M |
| `ctx_search` | Search code; `action` picks engine (default regex). regex(pattern) \| semantic(query) \| symbol(name, AST-exact; or handle=path#name@Lline) \| reindex \| find_related(file_path,line). `anchored=true` tags hits for `ctx_patch`. Run `ctx_compose` FIRST for understanding. | `action`, `pattern`, `query`, `name`, `handle`, `path`, `include`, `max_results`, `anchored`, `mode`, `top_k` | M |
| `ctx_glob` | Find files by glob pattern (respects .gitignore; multi-root via paths) | `pattern`*, `path`, `paths[]`, `max_results`, `ignore_gitignore` | M |
| `ctx_tree` | Compact directory tree with file counts per directory | `path`, `depth`, `show_hidden`, `paths`, `respect_gitignore` | M |
| `ctx_semantic_search` | Semantic search (BM25 + embeddings / hybrid). Deprecated → `ctx_search(action="semantic")` | `query`*, `action` (search\|reindex\|find_related), `mode` (bm25\|dense\|hybrid), `top_k` | S |
| `ctx_compose` | **PRIMARY TOOL** — call FIRST for understanding code. Returns ranked files with relevant symbol source inline. Combines BM25 lexical+semantic+associative retrieval+submodular optimization. One compose replaces search→read→symbol chain. | `task`*, `path` | S |
| `ctx_explore` | Iterative, deterministic exploration → compact `path:start-end` citations (BM25 + static graph + AST symbols, bounded turns); cheaper than `ctx_compose` for locating code across files | `query`*, `path`, `max_turns`, `citation` | S |
| `ctx_execute` | Sandboxed code execution (11 languages: js, ts, python, shell, ruby, go, rust, php, perl, r, elixir); only stdout enters context | `language`*, `code`*, `action`, `timeout`, `intent`, `items`, `path` | S |
| `ctx_multi_repo` | Multi-repo management + cross-repo search (RRF). `ctx_search`/`ctx_glob`/`ctx_tree`/`ctx_read` accept `repo=<alias>` arg to target registered roots. | `action`* (add_root\|remove_root\|list_roots\|search\|status\|save_config), `alias`, `query`, `mode`, `roots` | P |
| `ctx_url_read` | Fetch a web page, PDF, RSS/Atom feed, or YouTube video as compressed, cited context (HTML→Markdown, PDF→text, feeds→dated items, transcript; GitHub blob/raw URLs auto-resolve); SSRF-guarded | `url`*, `mode` (auto\|markdown\|text\|links\|facts\|quotes\|transcript), `query`, `max_tokens`, `max_items`, `timeout_secs` | S |
| `ctx_git_read` | Read a remote git repo via a cached shallow clone instead of scraping its web page | `url`*, `mode` (overview\|tree\|read\|grep), `path`, `ref`, `query`, `max_tokens` | P |

## 2. Memory & knowledge

| Tool | Purpose | Key actions | Profile |
|------|---------|-------------|---------|
| `ctx_knowledge` | Persistent project knowledge base across sessions | remember\|recall\|search\|relate\|consolidate\|timeline\|rooms\|wakeup\|status\|export\|remove; `mode` (semantic\|exact), `category` | S |
| `ctx_compress` | Context checkpoint for long conversations | `include_signatures` | S |
| `ctx_compress_memory` | Compress memory/config files (CLAUDE.md, .cursorrules); backs up `.original.md` | `path`* | P |
| `ctx_artifacts` | Context-artifact registry with BM25 search | list\|status\|index\|reindex\|search\|remove | P |
| `ctx_index` | Build & manage the code index | status\|build\|build-full | P |

## 3. Session & multi-agent

| Tool | Purpose | Key actions | Profile |
|------|---------|-------------|---------|
| `ctx_session` | Cross-session memory (CCP): tasks, findings, decisions, snapshots | status\|load\|save\|task\|finding\|decision\|snapshot\|restore\|resume\|diff\|verify | M |
| `ctx_checkpoint` | Snapshot / diff / restore the agent's code changes via a shadow git history kept outside the project's `.git` | snapshot\|log\|diff\|restore; `message`, `from`, `to`, `ref`, `path`, `limit` | P |
| `ctx_agent` | Multi-agent coordination + message bus + stigmergic scent field | register\|list\|post\|read\|handoff\|sync\|diary\|share_knowledge\|receive_knowledge\|claim\|release\|brief\|return | S |
| `ctx_share` | Share cached file contexts between agents | push\|pull\|list\|clear | P |
| `ctx_task` | Multi-agent task orchestration (A2A) | create\|update\|list\|get\|cancel\|message | P |
| `ctx_handoff` | Context Ledger Protocol — deterministic handoff bundles (hashed, local-first) | create\|show\|list\|pull\|export\|import | P |
| `ctx_workflow` | Workflow state machine with evidence tracking | start\|status\|transition\|complete\|evidence_add\|evidence_list\|stop | P |

## 4. Code intelligence & graph

| Tool | Purpose | Key actions | Profile |
|------|---------|-------------|---------|
| `ctx_graph` | Unified code graph: deps, symbols, impact. File-level dependency graph queries. | build\|related\|symbol\|impact\|context\|diagram; `action`* (neighbors\|impact\|path\|diff\|diagram), `path`, `to`, `since`, `depth`, `kind` | S |
| `ctx_callgraph` | Call-graph queries (BFS, trace, risk). Callers/callees for one symbol (function call edges, not const/var refs). | callers\|callees\|trace\|risk; `symbol`, `from`, `to`, `depth`, `file` | S |
| `ctx_impact` | Graph-based impact / blast-radius analysis | analyze\|diff\|chain\|build\|update\|status; `path`, `depth`, `root` | S |
| `ctx_architecture` | Architecture analysis over the property graph — understand module structure without reading every file | overview\|clusters\|layers\|cycles\|entrypoints\|hotspots\|health; `path`, `root`, `format` | S |
| `ctx_repomap` | PageRank-ranked map of the most important symbols | `max_tokens`, `focus_files[]`, `path` | S |
| `ctx_routes` | Extract HTTP routes (Express, Flask, FastAPI, Actix, Spring, Rails, Next.js) | `method`, `path` | S |
| `ctx_refactor` | LSP-backed refactoring. Single-phase edits (replace_symbol_body, reformat) work headless; two-phase ops (_preview+_apply) need JetBrains IDE. | rename\|references\|definition\|implementations\|safe_delete\|inline\|replace_symbol_body\|reformat; `action`*, `name_path`, `new_name`, `new_body` | S |
| `ctx_review` | Automated code review (impact, callers, tests, smells) | review\|diff-review\|checklist; `path`, `depth` | P |
| `ctx_smells` | Code-smell detection (8 rules over property graph): dead_code, long_function, god_file, complexity, etc. | scan\|summary\|rules\|file; `rule`, `path`, `root`, `format` | P |
| `ctx_pack` | Context Package Manager (PR packs, installable context) | pr\|create\|list\|info\|install\|export\|import\|auto_load | S |

## 5. Analytics & gain

| Tool | Purpose | Key actions | Profile |
|------|---------|-------------|---------|
| `ctx_metrics` | Session token stats, cache rates, per-tool savings, signature backend ratios | — | P |
| `ctx_radar` | Full context-budget breakdown (prompt, messages, tools, reads, shell) | `format` (display\|json) | P |
| `ctx_cost` | Local cost attribution per agent/tool | report\|agent\|tools\|reset\|json\|status; `agent_id`, `limit` | P |
| `ctx_gain` | Gain report incl. "Wrapped" summary | status\|report\|score\|wrapped\|agents\|json; `period` (week\|month\|all), `model`, `limit` | P |
| `ctx_heatmap` | File-access heatmap | status\|directory\|cold\|json; `path` | P |
| `ctx_benchmark` | Benchmark compression modes for a file/project | `path`*, `action`, `format` | P |
| `ctx_analyze` | Entropy analysis — recommends optimal compression mode for a file path | `path`* | P |
| `ctx_compare` | Preview compression — original vs the bytes lean-ctx would emit, with token counts + line diff (read-only) | `path` \| `content`+`ext` \| `command`+`output` | P |
| `ctx_feedback` | Harness feedback for LLM output tokens & latency | record\|report\|reset\|json\|status; `llm_input_tokens`, `llm_output_tokens`, `model`, `latency_ms`, `intent` | P |
| `ctx_discover` | Find missed compression opportunities in shell history | `limit` | P |
| `ctx_verify` | Verification observability + ContextProofV2 | stats\|proof\|v2; `format` (summary\|json\|both) | P |
| `ctx_proof` | Export machine-readable ContextProofV1 (Verifier, SLO, Pipeline, Provenance) | export*; `format`, `write`, `max_evidence`, `filename` | P |

## 6. Advanced — providers / plugins / proactive context

| Tool | Purpose | Key actions | Profile |
|------|---------|-------------|---------|
| `ctx_provider` | External context providers (GitHub, GitLab, Jira, Postgres, MCP bridges) | discover\|list\|status\|refresh\|configure\|query\|gitlab_issues\|gitlab_mrs; `provider`, `resource`, `iid`, `labels`, `limit` | P |
| `ctx_tools` | MCP Tool-Catalog Gateway — route/proxy unlimited downstream MCP servers at constant context cost | find\|call\|list\|refresh; `query`, `tool`, `arguments` | P |
| `ctx_plugins` | Plugin management | list\|enable\|disable\|info\|hooks; `name` | P |
| `ctx_rules` | Cross-agent rules governance (ContextOps) | sync\|diff\|lint\|status\|init; `agent` | P |
| `ctx_skillify` | Codify recurring session-diary + knowledge patterns into versioned, git-committable `.cursor/rules/skillify-*.mdc` (precision-biased, idempotent) | mine\|list\|status\|promote; `slug` | P |
| `ctx_summary` | Record + recall AI session summaries (semantic when warm, else lexical); auto-captured on the checkpoint cadence | recall\|record\|list; `query`, `top_k` | P |
| `ctx_package` | Save/resume portable context packages (session + summaries + knowledge bundle) for agent handoffs or session persistence | save\|resume\|list\|info; `path`, `description` | P |
| `ctx_overview` | Task-relevant project map — ideal at session start. PageRank on symbol graph, ~10x cheaper than `ctx_compose`. | `task`, `path` | S |
| `ctx_preload` | Proactively load task-relevant files; compact L-curve summary (~50-100 tokens vs ~5000 for individual reads) | `task`*, `path` | P |
| `ctx_prefetch` | Predictive prefetch for blast-radius files via graph + task signals | `root`, `task`, `changed_files[]`, `budget_tokens`, `max_files` | P |

## 7. Meta — context-field-theory / dispatch / dynamic tools

| Tool | Purpose | Key actions | Profile |
|------|---------|-------------|---------|
| `ctx_call` | Call any lean-ctx tool by name (lazy-loading). Categories: arch, debug, memory, batch, agent, util. Cannot invoke itself. | `name`*, `arguments` | P |
| `ctx_discover_tools` | Keyword search across all available tools. Empty query lists all. Use with `ctx_call` for static-tool-list clients. | `query` | P |
| `ctx_load_tools` | Load/unload dynamic tool categories at runtime. Categories: arch, debug, memory, metrics, session. Core is always loaded. | load\|unload\|list; `category` | P |
| `ctx_control` | Context Field Theory — overlay-based context manipulation (exclude, include, pin, unpin, set_view, set_priority, mark_outdated, reset, list, history). Reversible, scoped to call/session/project. | `action`* (exclude\|include\|pin\|unpin\|set_view\|set_priority\|mark_outdated\|reset\|list\|history), `target`, `value`, `scope`, `reason` | P |
| `ctx_plan` | Context planning (CFT) with Phi scoring + budget allocation. Selects files for context. | `task`*, `budget`, `profile` (ultra_lean\|balanced\|forensic) | P |
| `ctx_compile` | Context compilation via knapsack + Boltzmann view selection. Build minimal context package within token budget. | `mode` (handles\|compressed\|full), `budget` | P |
| `ctx_context` | Session-context overview — cached files, seen files, session state, CRP mode | — | P |
| `ctx_ledger` | Context-ledger ops for pressure management | status\|reset\|evict; `targets` | P |
| `ctx_cache` | Session-cache operations | status\|clear\|invalidate; `path` | P |
| `ctx_dedup` | Cross-file deduplication — analyze shared imports/code, then apply dedup hints for `ctx_read` output | analyze\|apply | P |
| `ctx_intent` | Structured intent input with routing policy | `query`*, `format`, `project_root` | P |
| `ctx_response` | Compress LLM response text (strip filler, TDD). No-op when CRP mode is off. | `text`* | P |
| `ctx_expand` | Zero-loss retrieval of archived tool outputs. See `[Archived:ID]` → `ctx_expand(id=ID)`. | retrieve\|list\|search_all; `id`, `head`, `tail`, `query`, `session_id`, `start_line`, `end_line` | P |
| `ctx_transcript_compact` | Compact an OpenAI-format message array deterministically: keep system + fresh tail verbatim, replace older turns with a recoverable summary, offload raw turns into session memory. Returns JSON `{messages, stats}`. | `messages`*, `focus_topic`, `fresh_tail_tokens`, `protect_min_messages` | P |

`*` = required parameter.

## Notes

1. `power` enables every registered tool; `ToolProfile::is_tool_enabled()`
   returns `true` for everything under power.
2. `ctx_load_tools` controls *dynamic* categories (`arch`, `debug`, `memory`,
   `metrics`, `session`) independently of the static profile filter.
3. Lazy clients use `ctx_call` + `ctx_discover_tools` + `ctx_load_tools` to reach
   tools not in their active profile without listing every one upfront. The
   advertised tool list is an advertising filter, not an access boundary.
4. `ctx_edit` is legacy/power-only; prefer `ctx_patch` for all edits.
5. `ctx_multi_read`, `ctx_smart_read`, `ctx_semantic_search`, `ctx_symbol` are
   deprecated — folded into `ctx_read` / `ctx_search` respectively. Hidden from
   `tools/list` but still callable for one release.
6. Generated registry/appendices are authoritative for counts and schemas.
   Regenerate with `cargo run --example gen_docs --features dev-tools`.

---

## lean-md addon (`.lmd.md` render pipeline)

`.lmd.md` / `.lean-md` rendering is provided by the **external lean-md addon**
(`dasTholo/lean-md`), not by lean-ctx itself. `ctx_md_render` / `ctx_md_check` are
exposed by the addon's MCP server once installed (`lean-ctx addon add @dasTholo/lean-md`); a
`.lmd.md` passed to `ctx_read` is returned **raw** — lean-ctx never renders it
(rendering is an explicit addon call). The `@directive` catalog and `@lean-md` header fields live in the
addon repo.

- **Addon repo:** <https://github.com/dasTholo/lean-md> — the `@directive`
  catalog and `@lean-md` header fields are documented there. This skill carries
  no lean-md reference of its own.
