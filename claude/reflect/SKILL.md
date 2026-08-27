---
name: reflect
description: End-of-session (or on-demand) self-improvement sweep. Reviews the current conversation for uncaptured learnings — user corrections, stated preferences, avoidable mistakes, repeated command sequences, reusable patterns, and repo-specific operational discoveries — and routes each to its durable home (global memory, CLAUDE.md/rules, a repo's AGENTS.md/CLAUDE.md, an in-repo script, or a skill/agent). Also runs a periodic memory-maintenance pass that flags stale, superseded, duplicate, or self-invalidated memories for pruning, and drains the compaction backlog of sessions whose detail was summarized away before capture. Use when the user runs /reflect, says "capture learnings", "write this down", "update your rules/skills", "prune/review memories", "process the compaction backlog", "check pending captures", or at the end of a substantive session. Creates light artifacts directly; proposes heavy ones (skills, agents, global rules) and any memory deletion before acting.
metadata:
  author: Joonas Onatsu
  license: MIT
---

# Reflect — Self-Improvement Sweep

Distill the current session into durable improvements so the same corrections,
feedback, and manual work are never re-derived. This skill operationalizes the
`## Self-Improvement` section of `~/.config/claude/rules/WORKFLOW.md`, which
owns routing by scope and the autonomy boundary. The graduated ladder in §3
below is the authoritative copy; that file points here for it rather than
restating it.

**Iron law: capture only what actually happened in this session.** Never invent
a learning to fill the sweep. Every candidate must cite the turn or action it
came from. If nothing qualifies, say so plainly and stop.

## 1. Scan the session for candidates

Look for each signal:

- **Corrections** — the user corrected an approach, output, or assumption.
- **Preferences** — the user stated how they want things done ("always…",
  "never…", "from now on…", "I prefer…").
- **Avoidable mistakes** — something went wrong that a captured guard would
  prevent next time.
- **Repetition** — a command sequence, script, or manual step recreated,
  re-typed, or re-derived ~2–3× or more.
- **Reusable patterns** — a method or role useful beyond this task (candidate
  skill or agent prompt).
- **Operational discoveries** — a non-obvious fact about the current repo
  (paths, gotchas, sudo/permission boundaries, service quirks).
- **Re-derivation** — the session rebuilt something a durable artifact already
  held. This is the one signal that measures the setup rather than the work, so
  scan for it explicitly:
  + a file re-read that a handoff brief had already summarized,
  + a fact re-established that has a memory file,
  + a path or command rediscovered that `AGENTS.md` or a rules file documents,
  + a decision re-litigated that an ADR already settled.

  Each instance is evidence that an artifact exists but failed — wrong content,
  wrong home, or a description the search could not match. Record which of those
  three it was, because the fix differs: rewrite, move, or re-word the trigger.
  Absent an evaluator, this is the only feedback signal available on whether the
  captures are working at all, and it costs nothing to collect because the
  re-derivation already happened in front of you. A session that re-derives
  nothing is the observation worth reporting too.

This session is not the only source: §8 covers earlier sessions whose detail
was compacted away before anyone captured it.

## 2. Route each candidate by scope

| Candidate | Destination |
|---|---|
| Cross-repo behavior / preference / correction | Global memory (`feedback`/`user`) |
| Standing behavioral rule | `~/.config/claude/CLAUDE.md` (or `rules/`) |
| Repo-specific operational fact | Current repo's `AGENTS.md` / `CLAUDE.md` |
| Repeated command sequence | In-repo script / justfile recipe |
| Cross-repo reusable method or role | Global `~/.config/claude/{skills,agents}` |
| Repo-specific reusable method or role | Repo's `.claude/{skills,agents}` |

Don't mix scopes: repo trivia never goes to global memory; global preferences
never get buried in one repo.

**Check the destination before proposing a new artifact.** Read what already
lives there — the memory silo, the rules file, the repo's `AGENTS.md`, the
deployed skills and agents. When something already covers the candidate, extend
it; a near-duplicate is worse than no capture, because two artifacts on one
subject drift apart and neither is authoritative.

## 3. Apply the graduated ladder (thresholds)

Promote to the cheapest durable form that fits:

- Note / `AGENTS.md` entry — recurring knowledge or gotcha, ~2 encounters.
- In-repo script / recipe — manual command sequence, ~3 uses.
- Skill / agent prompt — reusable method or role, ~3–5 uses **and** useful
  beyond one repo.
- `CLAUDE.md` / rules change — any confirmed correction or stated standing
  preference (once is enough).

Below threshold → list the candidate in the report as "deferred", don't codify.

**Apply an addressability filter before the threshold.** Ask what class of thing
the failure was, and codify only the third:

- A capability limit — the model or the task was simply hard. A rule cannot fix
  it and will fire forever on sessions it does not help.
- A one-off environment fault — a flaky network, a half-applied config, a race.
  Recording it teaches a superstition.
- A defect in the setup — a tool whose contract surprised you, a rule that said
  the wrong thing, a step nobody documented. This is the only kind worth a
  durable artifact.

Then fix it at the lowest level that can express the fix. A stale fact is a
context fix, not a workflow rewrite; a surprising tool contract belongs in that
tool's reference, not in an always-loaded rules file. Reach for the higher level
only when the failure keeps recurring after the lower one was tried. Skipping
this filter is how an instruction corpus grows by accretion: every annoyance
becomes a line, and nothing is ever the wrong size.

Threshold is necessary, not sufficient. Anything written to `CLAUDE.md` or
`rules/` is re-read at every session start and applied to sessions it was never
written for. Before codifying one, state what it costs when it fires on the
wrong session: a rule that makes the agent more eager, more expensive, or more
invasive needs a benefit that clearly outweighs that. Narrow the wording to the
case actually observed.

## 4. Respect the autonomy boundary

- **Light** (repo notes, `AGENTS.md` entries, in-repo scripts): create
  directly, then report what changed.
- **Heavy** (new/edited skills, agent prompts, global `CLAUDE.md`/rules):
  propose first — show the exact text, the destination, and whether it is
  global- or repo-scoped — and write only after the user approves.

## 5. Write the captures

- **Global memory**: one fact per file with frontmatter
  (`type: user | feedback | project | reference`), plus a one-line pointer in
  `MEMORY.md`. Check for an existing file that already covers it and update it
  rather than duplicating; delete memories proven wrong.
- **Set `scope:`** — `repo:<name>` (default), `machine`, or `global`. Silos are
  per-project, so a fact true everywhere has no silo that fits and drifts into
  always-loaded instruction files instead. The field records the intent.
- **Set `valid_until:`** when the fact has a foreseeable expiry — a version, a
  migration, a pending fix. `null` (or omitted) means "true until disproved".
  Retire an expired fact by setting the field, NEVER by deleting the file:
  invalidate but do not discard, because the history is what stops the same
  wrong conclusion being re-derived.
- **Both fields are advisory, so put what must reach retrieval in the
  `description`.** Recall matches against the description text; nothing filters
  on frontmatter. A `machine`- or `global`-scoped fact MUST therefore say so in
  its description, and a fact with a known expiry MUST name the condition there
  ("until lean-ctx 3.10", "while the vendored hook is in use"). The fields serve
  the maintenance sweep and the human reader; the description serves the search.
- **Update by delta, never by wholesale rewrite.** When revising an existing
  memory or an instruction file, change the lines that are wrong and leave the
  rest untouched. A model asked to regenerate an accumulated document drops what
  it judges low-priority, and the measured failure is severe — a rewritten
  context playbook has collapsed from 18k tokens to 122 in one pass, scoring
  below never having adapted at all. Rewrite whole only when the user asks for
  it.
- `feedback`/`project` bodies: add **Why:** and **How to apply:** lines. Link
  related memories with `[[name]]`.
- **Repo files**: match the file's existing structure and voice; convert
  relative dates to absolute (today is discoverable via the session context).
- **New skills/agents**: follow `skill-forge` conventions for skills; match the
  existing `agents/*.md` frontmatter for agents.
- **Never carry a secret into a capture.** Transcripts, logs, and scrollback
  hold credentials, tokens, hostnames, and client-identifying detail. A
  captured fact states the mechanism without the secret — name the file a
  credential lives in, never its value. These files are committed to a
  repository intended for publication.
- After any material config edit, run the repo hygiene gate
  (formatter/linter/pre-commit) on the changed files before calling it done.

## 6. Report

Summarize as a table: **candidate → destination → action** (written /
proposed / deferred-below-threshold), each with its evidence. List heavy
proposals awaiting approval in a separate block so the user can approve or
reject them individually.

## 7. Memory maintenance (periodic)

Global memory grows and goes stale. When invoked with a maintenance intent
("prune memories", "review memories") or roughly every ~10 captures, sweep
`~/.config/claude/projects/<project>/memory/` for entries to retire:

- **Expired** — `valid_until` has passed, or the condition it names has been
  met. Mark it and correct the pointer; do not silently leave it recallable,
  because an expired memory is worse than a missing one. A missing fact produces
  a question, a stale one produces confident wrong action.
- **Self-invalidated** — the memory names a condition for its own removal
  ("update or remove once X") and X has happened.
- **Superseded** — a newer memory or a committed rule now covers it (e.g. a
  `feedback` memory that has since been promoted into `CLAUDE.md`).
- **Duplicate** — two files cover the same fact; merge into one.
- **Wrong / drifted** — the memory contradicts the current repo, config, or
  the user's latest guidance.
- **Dangling** — before acting on any memory, verify the files, flags, and
  paths it names still exist; a memory is only as current as its last write.

Deleting a memory changes user data: **propose deletions and merges, don't
perform them silently.** Present each candidate with its reason and evidence,
and act only on approval. When a memory is deleted or merged, also remove or
update its one-line pointer in `MEMORY.md`. Recalled memories may be stale —
re-verify against live files before recommending anything based on them.

## 8. Compaction backlog (`capture-pending.jsonl`)

The `PreCompact` hook appends one breadcrumb per compaction to
`${CLAUDE_CONFIG_DIR:-~/.config/claude}/hooks/capture-pending.jsonl` — fields
`ts`, `session_id`, `cwd`, `transcript_path`, `trigger`. Each line marks a
session whose detail was summarized away, and is the only surviving pointer
back to it. Nothing else reads this file.

**Always report the count. Drain it on request or once it grows past ~20.**

```bash
wc -l < "${CLAUDE_CONFIG_DIR:-$HOME/.config/claude}/hooks/capture-pending.jsonl"
```

Include the count in the §6 report even when not draining, so the backlog stays
visible instead of accumulating silently.

**What this sweep structurally cannot recover.** The first turns of a session
carry the task setup, the user's constraints, and the architectural decisions
that cannot be re-derived — and they are the first thing compaction discards. An
end-of-session sweep reads what survived, so a constraint lost at compaction is
lost to this skill too, and its absence is invisible: the summary reads complete.
Treat a drained entry as partial evidence rather than a full account, and prefer
whatever the transcript shows VERBATIM over the compacted summary of it. The
durable fix is upstream of here — extracting the session's constraints into a
persistent note while they are still in context — so when a session is heading
for compaction with constraints only in its early turns, say so at that point
rather than trusting this backlog to reconstruct them.

### Process one entry

1. **Check the transcript still exists.** Paths decay as old sessions are
   cleaned up. If `transcript_path` is gone the entry is unrecoverable — drop
   it, report it as expired, and move on. NEVER retain a dangling entry.
2. **NEVER read a transcript in full.** They routinely exceed the context
   window. Search it for the §1 signals, or hand the entry to a subagent that
   returns only candidates with quoted evidence.
3. **Route to the entry's own project, not the current one.** Memory is siloed
   per project, and the correct silo is `<dirname of transcript_path>/memory/`
   — derive it from the breadcrumb, NEVER assume the open project's silo. A
   repo-scoped fact belongs in the `AGENTS.md`/`CLAUDE.md` at that entry's
   `cwd`; if that checkout is absent, defer it rather than guessing.
4. **Apply §2–§5 unchanged.** A candidate recovered from a transcript still
   goes through routing, thresholds, and the autonomy boundary.

The iron law holds here too: evidence MUST be quoted from the transcript. A
breadcrumb proves a compaction happened, not that anything was learned — most
yield nothing, and "no candidates" is a correct result for an entry.

### Prune

Drop an entry only once it is processed or expired, one `session_id` at a time:

```bash
sed -i '/"session_id":"<id>"/d' \
  "${CLAUDE_CONFIG_DIR:-$HOME/.config/claude}/hooks/capture-pending.jsonl"
```

Use the in-place form. A `>` redirect into a temp file is rejected outside
`/tmp` by lean-ctx's write doctrine, so the read-filter-rewrite shape fails
here even though it is the more familiar idiom.

NEVER truncate or clear the file wholesale — an unprocessed line deleted that
way loses its transcript pointer permanently. The hook may append while the
sweep runs, so re-check the count afterwards and leave anything new in place.
The file is runtime state and gitignored; never stage it.
