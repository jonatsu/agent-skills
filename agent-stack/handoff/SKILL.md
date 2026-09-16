---
name: handoff
description: Create a work handoff for a fresh session, another agent, machine, or person. Use for a short next-task pointer, a fuller continuity brief, a paste-ready session primer, or a saved handoff document. Excludes durable project documentation and memory capture.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Handoff

A handoff transfers what the recipient needs to continue. Its most valuable content is session-only knowledge
that cannot be recovered from the repository, issue tracker, plans, or current machine state.

Do not recap the conversation or inventory everything inspected. Cite durable artifacts and let the recipient
read them.

## A Handoff Is Ephemeral

A handoff is disposable transfer state, never a system of record. A `PRIME` prompt exists only until the
terminal buffer clears; a `DOCUMENT` saved under `.scratch/`, a temporary directory, or any other gitignored
path can be reclaimed or lost before the next session opens it. Treat every handoff as if it may not survive.

A handoff must therefore never be the only home for anything the work depends on. A decision, agreement,
constraint, or piece of derived context that outlives the session belongs in a durable, version-controlled
artifact — a plan, specification, ADR, glossary, or committed note — written before or alongside the handoff,
not deferred to it. The handoff points to those artifacts; it does not stand in for them. When the session
produced durable knowledge that is still only in a gitignored handoff or the conversation, record it in a
tracked document first, then write the handoff that points to it.

## Choose the Smallest Sufficient Handoff

Use a **pointer handoff** when the recipient can recover the work state and only needs a clear next task. This
is the default for a new task in an established workflow, such as naming the next skill to review.

Use a **stateful handoff** when continuity depends on unfinished work, multiple connected tasks, decisions,
deviations, blocked paths, or substantial session-only context.

Length follows continuity risk. A pointer may be two or three sentences. A stateful handoff may need several
sections. Do not promote a pointer into a stateful brief merely because more repository facts are available.

Apply brevity to recoverable context first. Never omit material session-only context to keep a pointer short;
switch to a stateful handoff when that context no longer fits clearly in the pointer form.

## Preserve Session-Only Context

Before writing either form, deliberately check what would disappear with this session:

- standing operating instructions the user set for the session, especially at its start — a required tool or
  method such as "use sequential-thinking for all complex design work", a scope limit, or a working
  convention; these bind the continuing work too and are among the most frequently dropped, so carry them
  forward in the recipient's own terms rather than paraphrasing them away;
- user preferences, corrections, and one-off instructions stated during the work;
- decisions and agreements that have not been recorded elsewhere, including the reason that settled them;
- nuances, exceptions, and boundaries that affect how the next task should be interpreted;
- rejected approaches and dead ends whose repetition would cost meaningful time;
- deliberate deviations, parked work, and scope that a new agent might otherwise undo or expand; and
- an unfinished line of reasoning or current lean that the recipient must continue.

Include an item only when it changes the recipient's action, decision, or interpretation, or prevents costly
re-derivation. Preserve the operative detail and its reason. Omit conversational chronology and incidental
preferences that do not affect the work.

This check is mandatory even for a pointer handoff. If it finds nothing relevant, keep the pointer short; do
not add a placeholder saying that no context exists.

## Verify Only What You Pass

Confirm every path, branch, commit, command result, or other factual state included in the handoff during the
current turn. Mark unverified claims as unverified.

Do not gather a standard Git inventory unless the handoff needs those facts. Volatile state is usually better
expressed as an instruction to inspect it, such as `run git status -sb`, than as a snapshot that will become
stale.

Name the command behind a verification claim and state what the check did not cover when that limit matters.
Never write "should work" as completed state.

## Pointer Handoff

Lead with the next task and its completion condition. Then cite the workflow or artifact the recipient should
read. Add session-only context only when the context-loss check found something material.

The repository, paths, and artifacts in the examples below are invented.

Example:

```text
Review `payments-api` next. Read `docs/review-process.md`, follow its review workflow, and start from the
service package.
```

If the session established a relevant preference, add it directly:

```text
Review `payments-api` next. Read `docs/review-process.md` and follow its review workflow. The user wants the
review to focus on silent retry paths in the payment client; broad endpoint coverage is out of scope.
```

A pointer handoff normally needs no headings, repository summary, Git history, file inventory, or list of
checks already defined by the cited workflow.

## Stateful Handoff

Lead with `NEXT`: the immediate task and a concrete completion condition. Add only the sections that carry
material content:

- `CONTEXT`: session-only preferences, decisions, nuances, rejected options, and unfinished reasoning.
- `STATE`: unfinished or completed work whose exact status affects the next action, with verification
  evidence.
- `READ`: durable artifacts required to act, in reading order, with a stable section or symbol when useful.
- `LOCKED`: settled decisions and the reason that settled each one.
- `SCOPE`: deliberately parked or excluded work and why it remains out of bounds.
- `OPEN`: decisions the recipient must make now, the current lean, and what the decision depends on.
- `DEVIATIONS`: intentional departures from the written plan and their reasons.
- `PROCESS`: environment or workflow traps already encountered and worth avoiding.

Merge or omit sections when that makes the brief clearer. A human or agent consumes the output, so stable
headings are not a formal interface.

Point to plans, specifications, issues, ADRs, commits, and code instead of reproducing them. Record a file
inspected and left unchanged only when the conclusion prevents a likely or expensive repeated investigation.

Read `references/example-brief.md` only when a substantial stateful handoff needs a worked shape.

## Delivery Mode

Use `PRIME` when the same work continues in a fresh context. Return one fenced block that the user can paste
as the first message. Do not save it to disk.

A pasted prompt is size-limited by the terminal, not by the model. Above roughly 4 KB — about 3,000
characters, or 40–50 lines — many terminals silently corrupt a large paste: the start and end arrive intact
while the middle is truncated or collapsed, with no error and nothing to recover the lost lines from, and a
client that folds a multi-line paste behind a collapsed view can hide the damage entirely. Refuse by default
to emit a `PRIME` handoff that exceeds this threshold. Say why, then either switch to `DOCUMENT`, whose saved
file is immune to paste corruption, or split the material so the durable context lives in a tracked artifact
and the prompt only points to it. Emit an oversized `PRIME` block only when the user explicitly overrides this
refusal after being told the risk. The 4 KB figure is environment-dependent; treat it as a conservative
default the user may raise or lower for their terminal.

Use `DOCUMENT` when the user asks for a file or the work passes to another machine or person.

Write to the path the user names. When the work passes to another machine or person and no path was named,
ask for one: a temporary directory is the wrong destination there, because the platform reclaims it on reboot
or by cleanup and the handoff can disappear before its recipient opens it.

A temporary directory suits one narrow case, a short-lived convenience on this machine. Save the Markdown
under the operating system's temporary directory then. Probe for `mktemp`; if unavailable, use the platform's
temporary-directory mechanism.

Read an existing target before writing and do not overwrite it without authorization. Use repository-relative
paths when the document may travel to another machine, and identify the repository once.

Infer the delivery mode from the request. `PRIME` is the default: use it when the request names no file and no
other machine or person. The mode is genuinely ambiguous only when the request sends the work outside this
session without saying where, and that is the case to ask about.

## Safety and Completion

Never include secrets, credentials, private URLs, or unnecessary personal data. Name the secret's location
rather than its value.

Before delivery, confirm:

- the next action is obvious on a skim;
- any durable decision or context the work depends on is recorded in a git-tracked artifact, not left to
  survive only in this handoff;
- standing operating instructions the user set for the session are carried forward in the recipient's terms;
- a `PRIME` handoff is within the paste-size limit, or the user has overridden the refusal knowingly;
- the session-only context scan was performed and every material result survived;
- every included fact was verified or labeled unverified;
- durable material is cited rather than copied;
- no line exists merely because it was easy to collect;
- deliberately excluded work is visible when omission could be misread; and
- the recipient can resolve every reference without access to the prior conversation.
