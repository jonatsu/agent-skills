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

With memory on, write a fact the user asked to remember, forget, or correct as one small Markdown note under
`<home>/memories/extensions/ad_hoc/notes/`. Consolidation folds the note into memory later; never edit the
generated files beside it. Where the session offers the `add_ad_hoc_note` tool, use it instead. Codex's own
memory prompt updates memory only when the user explicitly asks, so route every other candidate by the main
table.

For memory maintenance, propose a forget or correction note for each stale entry, and write it once the user
approves. The user turns memory use on or off for a session with `/memories`.
