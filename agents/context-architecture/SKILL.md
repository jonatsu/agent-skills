---
name: context-architecture
description: "Design, restructure, or audit a repository's documentation system for agents and maintainers: document layout, genres, routing, sharding, and walk-test measurement. Also checks whether docs, from one README to the whole tree, are still true: stale claims, duplicated or unowned facts, and plans whose status misleads. Use its named default layout when a repository has none. Instruction-file internals route to agents-context-docs."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Context Architecture

Build the smallest repository documentation system that lets a cold-started reader orient, act, and report
using only the files present. The reader is usually an agent and often a new maintainer, and both are served by
the same design. Documentation is a retrieval system competing for a finite attention budget, not a document
set: judge every choice by the expected cost of assembling sufficient, correct context for a task, plus the
maintenance cost of keeping that assembly correct as the repository changes.

## Scope and Ownership

This skill owns the system level: which documents exist, the genre each belongs to, how the floor file routes
to them, when to shard, whether they still tell the truth, and how the whole is measured. Instruction-file
internals — writing and maintaining `AGENTS.md`/`CLAUDE.md` content, scoped instructions, `llms.txt` — belong
to `agents-context-docs`; invoke it as the executor for those files. Extracting a repeated procedure into a
skill belongs to `skill-forge`.

Repository facts are the authority for current behavior. Accepted requirements are the authority for intended
observable behavior within their scope. Verify each claim against its applicable authority or label it unverified. An
existing repository's established conventions outrank this skill's defaults.

## Choose the Branch

- **Design:** the repository has no established layout, or a new area needs one. Read
  [references/default-layout.md](references/default-layout.md), apply it lazily (create a directory on first
  need, never for completeness), then hand instruction-file creation to `agents-context-docs`. The same file
  answers where a single new document goes, such as working notes, a how-to, or research, when the repository
  has no convention for it.
- **Restructure:** an existing context system misroutes, bloats, or mixes genres. Diagnose against the model
  below before moving anything; propose structural moves rather than silently applying them, and preserve
  stable anchors other documents cite.
- **Audit:** assess navigation efficiency and coverage without assuming edits are wanted. Run the checker
  (below), read [references/walk-test.md](references/walk-test.md) for the behavioral measurement, and delegate
  instruction-file internals to the `agents-context-docs` skill's audit branch. Coverage is a separate
  question from navigation, and the walk test cannot ask it: compare the decisions the repository visibly
  made — framework and dependency choices, data models, authentication strategies, anything expensive to
  reverse — against the records in its decisions genre, and report an unrecorded one as a gap. Deliver
  findings by severity with evidence; record measurements as a dated file in the repository's evaluations
  genre.
- **Truth audit:** check whether documents still tell the truth, from one README to the whole tree: stale
  claims, duplicated or unowned facts, copies of volatile facts, misleading status, and knowledge in the wrong
  home. Read [references/truth-audit.md](references/truth-audit.md) and follow its steps; it ends in an action
  menu the user selects from.

Read [references/writing-rules.md](references/writing-rules.md) before writing or reviewing any agent-facing
document in any branch.

## The Model

Five concerns, in order of leverage. Topology is deliberately last.

1. **Floor discipline.** The always-loaded file taxes every session of every agent. It carries only never-miss
   rules and the routing index; everything else is a pointer. Grow it from observed failures — every floor
   rule should trace to a failure it prevents. Apply the `agents-context-docs` skill's accretion test to keep
   the floor from becoming an incident log.

   **A floor over its budget is a routing defect until routing is proven clean.** Diagnose before trimming:
   trimming under budget pressure deletes meaning a word at a time, while moving one route block can free hundreds of
   words and make its contents more reachable. When a section does move, the never-miss obligation stays as one
   imperative line and its trigger, exceptions and rationale go to the hub — "archive before reporting done"
   stays, while its trigger details leave.

   Routing is the first lever but not always an available one: a ruleset loaded at user or machine scope has
   no hub to route to, because no second file loads in every session of every harness. There the register and
   the accretion test are the whole remedy — shorten by deleting what changes no decision, never by thinning a
   rule.

2. **Read-when sharpness.** Every index entry, document header, and skill description is a load/skip
   classifier. Phrase it as the trigger condition ("read before gating a change"), never the topic
   ("verification"). It must work under the lowest common denominator of identifier plus text search, with no
   client discovery features assumed. Keep structural routes distinct from inline references so an incidental
   mention cannot masquerade as a usable path.

3. **Genre separation with declared authority.** Each document belongs to exactly one genre, and each genre declares
   its update semantics and its place in the override chain. Live code outranks descriptions of current behavior;
   accepted specifications govern intended observable behavior; the user's current instruction outranks stored
   guidance. The genre table and named default layout live in
   [references/default-layout.md](references/default-layout.md). Mixing genres — a living reference inside a
   frozen decision, state notes inside the floor — is the root failure behind most context rot.

4. **Truth maintenance.** One owner per fact, and the owner is the file someone must touch when the fact
   changes; everywhere else carries a pointer. Generate what is derivable from code and never hand-edit the
   output; stamp non-obvious facts with what they were verified against, not just when; gate what enters
   (no secrets, no speculation, no unverified recall); schedule consolidation and pruning, not only appending.

5. **Lazy topology.** Hub-and-spoke. Put a destination directly in the floor only when the agent must choose it
   there; route related destinations through a read-when hub before direct entries crowd the floor. Shard a hub
   only when its own index no longer fits one comfortable read. Graphs emerge from evidence; never design one
   up front.

## Cross-Agent Invariants

- Durable state lives in agent-neutral files in the repository. The floor is `AGENTS.md`, with `CLAUDE.md` as
  a symlink where a client requires that name.
- Client capabilities — skill auto-discovery, subagents, lifecycle hooks, proprietary memory, auto-compaction
  — are progressive enhancement. Every one of them gets a files-based fallback reachable from the floor. Put
  a skill's trigger in the floor only when it is a floor-level choice; otherwise route the floor to a focused
  skill or workflow index whose own read-when entries expose the trigger without taxing unrelated sessions.
- Deterministic obligations belong to repository-run gates (pre-commit, CI, task runner), which fire whichever
  agent edits. Prose orients; gates enforce. When a rule must hold every time, propose the gate.

## Enforcement

Run `scripts/check_context_architecture.py <repository-root>` after any change and resolve every finding. It
measures the system level: documents no structural route reaches, routing entries without a trigger condition,
and line-number references that rot. The default structural route is a trigger-keyed list item whose first
physical line starts with `Read when`, `Symptom`, `Read before`, or `If you`, then names the condition and a
Markdown document link. A trigger-keyed routing table or standalone Markdown inclusion link also routes for
compatibility. Inline links and incidental backticked paths do not establish reachability. See
[references/writing-rules.md](references/writing-rules.md) for the exact forms and table headers.
Pair it with the `agents-context-docs` skill's `check_agent_context.py` for the instruction-file level;
neither substitutes for the other. Propose wiring both into the repository's gates.

**Run both before calling a restructure done, because they can be made to disagree.** Moving an evidence index
off the floor satisfies this checker and, unless the instruction file still routes to the index, orphans every
file that index carried by the other one. The handshake is the route: the floor names the index, the index
names the evidence. Losing either end is a finding in one checker and silence in the other.

One unreachable parent reports as many findings as it has children, so read a batch of unreachable files as one
broken route rather than as many problems — and check that the parent's own entries are structural, since a
route landing on an index whose links are prose stops there.

Scripts prove structure, not behavior. The behavioral acceptance gate is the walk test in
[references/walk-test.md](references/walk-test.md); a context system nobody has walked is unmeasured, and its
efficiency claims are hypotheses.

## Completion

- Every created or moved document sits in exactly one genre and is reachable through structural routes rooted
  in the floor.
- The floor is no longer than the work found it, or the report states what was relocated and where.
- Both checkers pass, or every remaining finding is reported with a reason.
- Structural moves, deferred decisions, and unverified claims are reported explicitly.
- An audit ends with a dated record in the evaluations genre, not only a conversation reply.
