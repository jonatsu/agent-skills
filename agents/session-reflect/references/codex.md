# Codex CLI

The home is `${CODEX_HOME:-~/.codex}`; it is written `<home>` below.

## Where things live

- **Memory**: generated, not hand-written. With `[features] memories = true`, Codex distils past sessions that
  have sat idle (six hours by default, `memories.min_rollout_idle_hours`) into files under `<home>/memories/`, or
  `<home>/memories_v2/` on a home that started on the newer store. Memory is global rather than per project, and
  Codex injects a summary into later sessions unless `memories.use_memories = false`. Treat those files as
  generated state and leave them unedited: a later pass rewrites them.
- **User instructions**: `<home>/AGENTS.override.md` if present, else `<home>/AGENTS.md`.
- **Project instructions**: one file per directory from the repository root down to the working directory,
  `AGENTS.override.md`, then `AGENTS.md`, then any name in `project_doc_fallback_filenames`.
- **Session logs**: JSONL rollouts at `<home>/sessions/YYYY/MM/DD/rollout-<timestamp>-<id>.jsonl`; the first
  record is `session_meta`.

## Writing a memory

Codex learns from the session itself, so a preference stated plainly in the session usually reaches its memory
without a write. A capture that must hold from the next session on goes to instructions instead.

When the `memories` tools appear in the session, `add_ad_hoc_note` saves a note for a fact the user asked Codex
to remember. Use it for those facts, and route the rest by the main table. The tools sit behind the
undocumented `memories.dedicated_tools` setting, so check for them in the session rather than assuming either
way.

Memory maintenance has nothing to prune by hand; the user turns memory use on or off for a session with
`/memories`.
