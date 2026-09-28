---
name: session-reflect
description: End-of-session or on-demand sweep that distills this session's uncaptured learnings into durable homes, prunes stale or superseded memories, and drains the compaction backlog. Use for /session-reflect, "capture learnings", "prune memories", or "check pending captures".
license: MIT
compatibility: Requires Claude Code. Section 8 additionally requires the PreCompact capture hook.
metadata:
  author: Joonas Onatsu
---

# Session Reflect — Self-Improvement Sweep

Distill the current session into durable improvements so the same corrections, feedback, and manual work are
never re-derived. Routing by scope, the graduated ladder, and the autonomy boundary are defined here; this
skill is their authoritative source.

**Iron law: capture only what actually happened in this session.** Never invent a learning to fill the sweep.
Every candidate must cite the turn or action it came from. If nothing qualifies, say so plainly and stop.

## 1. Scan the session for candidates

Look for each signal:

- **Corrections** — the user corrected an approach, output, or assumption.

- **Preferences** — the user stated how they want things done ("always…", "never…", "from now on…", "I
  prefer…").

- **Avoidable mistakes** — something went wrong that a captured guard would prevent next time.

- **Repetition** — a command sequence, script, or manual step recreated, re-typed, or re-derived ~2–3× or
  more.

- **Reusable patterns** — a method or role useful beyond this task (candidate skill or agent prompt).

- **Operational discoveries** — a non-obvious fact about the current repo (paths, gotchas, sudo/permission
  boundaries, service quirks).

- **Re-derivation** — the session rebuilt something a durable artifact already held. This is the one signal
  that measures the setup rather than the work, so scan for it explicitly:

  - a file re-read that a handoff brief had already summarized,
  - a fact re-established that has a memory file,
  - a path or command rediscovered that `AGENTS.md` or a rules file documents,
  - a decision re-litigated that an ADR already settled.

  Each instance is evidence that an artifact exists but failed — wrong content, wrong home, or a description
  the search could not match. Record which of those three it was, because the fix differs: rewrite, move, or
  re-word the trigger. Absent an evaluator, this is the only feedback signal available on whether the captures
  are working at all, and it costs nothing to collect because the re-derivation already happened in front of
  you. A session that re-derives nothing is the observation worth reporting too.

This session is not the only source: §8 covers earlier sessions whose detail was compacted away before anyone
captured it.

## 2. Route each candidate by scope

| Candidate                                     | Destination                                                   |
| --------------------------------------------- | ------------------------------------------------------------- |
| Cross-repo behavior / preference / correction | The current project's memory silo (`feedback`/`user`)         |
| Standing behavioral rule                      | The user-level `CLAUDE.md`, or an instruction file it imports |
| Repo-specific operational fact                | Current repo's `AGENTS.md` / `CLAUDE.md`                      |
| Repeated command sequence                     | In-repo script / justfile recipe                              |
| Cross-repo reusable method or role            | Whatever source owns the user-level skills or agents          |
| Repo-specific reusable method or role         | Repo's `.claude/{skills,agents}`                              |

Route each candidate to its own scope: keep a repo-specific fact in the repo, and send a preference that spans
repositories to memory rather than filing it under the repo it happened to surface in.

**There is no global memory store.** Silos are per project, so a fact true everywhere still lands in whichever
silo is open, and only that project's sweeps and recalls will ever see it. Nothing filters on frontmatter, so
such a fact MUST carry its scope in its own description or it is unreachable from anywhere else.

**Establish what owns a destination before writing to it.** A user-level skills or agents directory may be a
deployment artifact rather than a source: a sync tool installs real copies into it and overwrites them on the
next run, so a capture written there is destroyed without any error. Determine the owner from the environment
at the time of the capture, never from a remembered path or a previous session. Look for a manifest, lock
file, or tracked source that claims the directory, and check whether the deployed copy is under version
control at all. When something owns it, the durable home is the source that deploys it and the capture goes
there; when nothing claims it, the directory is itself the home.

**Check the destination before proposing a new artifact.** Read what already lives there — the memory silo,
the rules file, the repo's `AGENTS.md`, the deployed skills and agents. When something already covers the
candidate, extend it; a near-duplicate is worse than no capture, because two artifacts on one subject drift
apart and neither is authoritative.

## 3. Apply the graduated ladder (thresholds)

Promote to the cheapest durable form that fits:

- Note / `AGENTS.md` entry — recurring knowledge or gotcha, ~2 encounters.
- In-repo script / recipe — manual command sequence, ~3 uses.
- Skill / agent prompt — reusable method or role, ~3–5 uses **and** useful beyond one repo.
- `CLAUDE.md` / rules change — any confirmed correction or stated standing preference (once is enough).

Below threshold → list the candidate in the report as "deferred", don't codify.

**Apply an addressability filter before the threshold.** Ask what class of thing the failure was, and codify
only the third:

- A capability limit — the model or the task was simply hard. A rule cannot fix it and will fire forever on
  sessions it does not help.
- A one-off environment fault — a flaky network, a half-applied config, a race. Recording it teaches a
  superstition.
- A defect in the setup — a tool whose contract surprised you, a rule that said the wrong thing, a step nobody
  documented. This is the only kind worth a durable artifact.

Then fix it at the lowest level that can express the fix. A stale fact is a context fix, not a workflow
rewrite; a surprising tool contract belongs in that tool's reference, not in an always-loaded rules file.
Reach for the higher level only when the failure keeps recurring after the lower one was tried. Skipping this
filter is how an instruction corpus grows by accretion: every annoyance becomes a line, and nothing is ever
the wrong size.

Threshold is necessary, not sufficient. Anything written to the user-level `CLAUDE.md` or a file it imports
at launch is re-read at every session start and applied to sessions it was never written for. Before
codifying one, state what it costs when it fires on the wrong session: a rule that makes the agent more eager,
more expensive, or more invasive needs a benefit that clearly outweighs that. Narrow the wording to the case
actually observed.

## 4. Respect the autonomy boundary

- **Light** (repo notes, `AGENTS.md` entries, in-repo scripts): create directly, then report what changed.
- **Heavy** (new/edited skills, agent prompts, global `CLAUDE.md`/rules): propose first — show the exact text,
  the destination, and whether it is global- or repo-scoped — and write only after the user approves.

## 5. Write the captures

- **Memory**: one fact per file with `name`, `description`, and `metadata.type`
  (`user | feedback | project | reference`), plus a one-line pointer in `MEMORY.md`. Read a neighbouring file
  in the same silo and match its frontmatter rather than a remembered schema — some fields are written by
  tooling and MUST NOT be hand-typed, and a hand-written file that omits them is structurally unlike its
  neighbours. Delete memories proven wrong.
- **Set `metadata.scope:`** when the fact does not belong to the silo holding it — `machine` for a fact about
  this machine, `global` for one true in every repository. Omit it for an ordinary repo-scoped fact, which is
  the default and needs no marker. The field is advisory and nothing filters on it, so a fact that escapes
  its silo MUST also say so in its `description`; the field serves the maintenance sweep and the human
  reader, the description serves recall.
- **Everything that must reach retrieval goes in the `description`.** Recall matches against the description
  text; nothing filters on frontmatter. A fact that is machine-wide or true across every repository MUST say
  so there, because the silos are per-project and no silo fits such a fact. A fact with a foreseeable expiry
  MUST name the condition there too ("while the vendored hook is in use"), since nothing else will surface it
  when the condition is met.
- **Update by delta, never by wholesale rewrite.** When revising an existing memory or an instruction file,
  change the lines that are wrong and leave the rest untouched. A model asked to regenerate an accumulated
  document drops what it judges low-priority, and the measured failure is severe — a rewritten context
  playbook has collapsed from 18k tokens to 122 in one pass, scoring below never having adapted at all.
  Rewrite whole only when the user asks for it.
- `feedback`/`project` bodies: add **Why:** and **How to apply:** lines. Link related memories with
  `[[name]]`.
- **Repo files**: match the file's existing structure and voice; convert relative dates to absolute (today is
  discoverable via the session context).
- **New skills/agents**: follow `skill-forge` conventions for skills; match the existing `agents/*.md`
  frontmatter for agents.
- **Never carry a secret into a capture.** Transcripts, logs, and scrollback hold credentials, tokens,
  hostnames, and client-identifying detail. A captured fact states the mechanism without the secret — name the
  file a credential lives in, never its value. These files are committed to a repository intended for
  publication.
- After any material config edit, run the repo hygiene gate (formatter/linter/pre-commit) on the changed files
  before calling it done.

## 6. Report

Summarize as a table: **candidate → destination → action** (written / proposed / deferred-below-threshold),
each with its evidence. List heavy proposals awaiting approval in a separate block so the user can approve or
reject them individually.

## 7. Memory maintenance (periodic)

Global memory grows and goes stale. When invoked with a maintenance intent ("prune memories", "review
memories") or roughly every ~10 captures, sweep the current project's memory silo for entries to retire:

- **Expired** — the expiry condition named in the memory's description has been met. Mark it and correct the
  pointer; do not silently leave it recallable, because an expired memory is worse than a missing one. A
  missing fact produces a question, a stale one produces confident wrong action.
- **Self-invalidated** — the memory names a condition for its own removal ("update or remove once X") and X
  has happened.
- **Superseded** — a newer memory or a committed rule now covers it (e.g. a `feedback` memory that has since
  been promoted into `CLAUDE.md`).
- **Duplicate** — two files cover the same fact; merge into one.
- **Wrong / drifted** — the memory contradicts the current repo, config, or the user's latest guidance.
- **Dangling** — before acting on any memory, verify the files, flags, and paths it names still exist; a
  memory is only as current as its last write.

Deleting a memory changes user data: **propose deletions and merges, don't perform them silently.** Present
each candidate with its reason and evidence, and act only on approval. When a memory is deleted or merged,
also remove or update its one-line pointer in `MEMORY.md`. Recalled memories may be stale — re-verify against
live files before recommending anything based on them.

## 8. Compaction backlog (`capture-pending.jsonl`)

The `PreCompact` hook appends one breadcrumb per compaction to
`${CLAUDE_CONFIG_DIR:-~/.config/claude}/hooks/capture-pending.jsonl` — fields `ts`, `session_id`, `cwd`,
`transcript_path`, `trigger`. Each line marks a session whose detail was summarized away, and is the only
surviving pointer back to it. Nothing else reads this file.

**Always report the count. Drain it on request or once it grows past ~20.**

```bash
wc -l < "${CLAUDE_CONFIG_DIR:-$HOME/.config/claude}/hooks/capture-pending.jsonl" 2>/dev/null || echo 0
```

Include the count in the §6 report even when not draining, so the backlog stays visible instead of
accumulating silently.

Read [references/compaction-backlog.md](references/compaction-backlog.md) when draining the backlog.
