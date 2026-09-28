# Compaction Backlog Processing

**What this sweep structurally cannot recover.** The first turns of a session carry the task setup, the user's
constraints, and the architectural decisions that cannot be re-derived — and they are the first thing
compaction discards. An end-of-session sweep reads what survived, so a constraint lost at compaction is lost
to this skill too, and its absence is invisible: the summary reads complete. Treat a drained entry as partial
evidence rather than a full account, and prefer whatever the transcript shows VERBATIM over the compacted
summary of it. The durable fix is upstream of here — extracting the session's constraints into a persistent
note while they are still in context — so when a session is heading for compaction with constraints only in
its early turns, say so at that point rather than trusting this backlog to reconstruct them.

## Process one entry

1. **Check the transcript still exists.** Paths decay as old sessions are cleaned up. If `transcript_path` is
   gone the entry is unrecoverable — drop it, report it as expired, and move on.
2. **NEVER read a transcript in full.** They routinely exceed the context window. Search it for the §1
   signals, or hand the entry to a subagent that returns only candidates with quoted evidence.
3. **Route to the entry's own project, not the current one.** Memory is siloed per project, and the correct
   silo is `<dirname of transcript_path>/memory/` — derive it from the breadcrumb, NEVER assume the open
   project's silo. A repo-scoped fact belongs in the `AGENTS.md`/`CLAUDE.md` at that entry's `cwd`; if that
   checkout is absent, defer it rather than guessing.
4. **Apply §2–§5 unchanged.** A candidate recovered from a transcript still goes through routing, thresholds,
   and the autonomy boundary.

The iron law holds here too: evidence MUST be quoted from the transcript. A breadcrumb proves a compaction
happened, not that anything was learned — most yield nothing, and "no candidates" is a correct result for an
entry.

## Prune

Drop an entry only once it is processed or expired, one `session_id` at a time:

```bash
sed -i '/"session_id":"<id>"/d' \
  "${CLAUDE_CONFIG_DIR:-$HOME/.config/claude}/hooks/capture-pending.jsonl"
```

Use the in-place form. The hook may append while the sweep runs, and the familiar read-filter-rewrite shape
would overwrite the file with a snapshot taken before those appends, silently dropping them.

NEVER truncate or clear the file wholesale — an unprocessed line deleted that way loses its transcript pointer
permanently. The hook may append while the sweep runs, so re-check the count afterwards and leave anything new
in place. The file is runtime state and gitignored; never stage it.
