---
name: context-architecture
description: "Design, restructure, or audit a repository's agent-facing context system — which documents exist, how they are organized, indexed, and kept true — including a named default documentation layout for repositories without one. Use when setting up agent docs, deciding where knowledge should live, restructuring or sharding context files, or measuring navigation efficiency with a walk test. Instruction-file internals route to agents-management. Triggers on: agent docs, context map, docs layout, walk test."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Context Architecture

Build the smallest repository context system that lets a cold-started agent orient, act, and report using only
the files present. Agent-facing documentation is a retrieval system competing for a finite attention budget,
not a document set: judge every choice by the expected cost of assembling sufficient, correct context for a
task, plus the maintenance cost of keeping that assembly correct as the repository changes.

## Scope and Ownership

This skill owns the system level: which documents exist, the genre each belongs to, how the floor file routes
to them, when to shard, and how the whole is measured. Instruction-file internals — writing and maintaining
`AGENTS.md`/`CLAUDE.md` content, scoped instructions, `llms.txt` — belong to `agents-management`; invoke it as
the executor for those files. Extracting a repeated procedure into a skill belongs to `skill-forge`.

Repository facts are the authority. Verify every claim about the repository against it or label the claim
unverified. An existing repository's established conventions outrank this skill's defaults.

## Choose the Branch

- **Design:** the repository has no established layout, or a new area needs one. Read
  [references/default-layout.md](references/default-layout.md), apply it lazily (create a directory on first
  need, never for completeness), then hand instruction-file creation to `agents-management`.
- **Restructure:** an existing context system misroutes, bloats, or mixes genres. Diagnose against the model
  below before moving anything; propose structural moves rather than silently applying them, and preserve
  stable anchors other documents cite.
- **Audit:** assess navigation efficiency without assuming edits are wanted. Run the checker (below), read
  [references/walk-test.md](references/walk-test.md) for the behavioral measurement, and delegate
  instruction-file internals to `agents-management`'s audit branch. Deliver findings by severity with
  evidence; record measurements as a dated file in the repository's evaluations genre.

Read [references/writing-rules.md](references/writing-rules.md) before writing or reviewing any agent-facing
document in any branch.

## The Model

Five concerns, in order of leverage. Topology is deliberately last.

1. **Floor discipline.** The always-loaded file taxes every session of every agent. It carries only never-miss
   rules and the routing index; everything else is a pointer. Grow it from observed failures — every floor
   rule should trace to a failure it prevents — and apply `agents-management`'s accretion test to keep it from
   becoming an incident log.
2. **Read-when sharpness.** Every index entry, document header, and skill description is a load/skip
   classifier. Phrase it as the trigger condition ("read before gating a change"), never the topic
   ("verification"). It must work under the lowest common denominator of identifier plus text search, with no
   client discovery features assumed.
3. **Genre separation with declared authority.** Each document belongs to exactly one genre, and each genre
   declares its update semantics and its place in the override chain (stored guidance is advisory; live code
   and the user's current instruction outrank it). The genre table and named default layout live in
   [references/default-layout.md](references/default-layout.md). Mixing genres — a living reference inside a
   frozen decision, state notes inside the floor — is the root failure behind most context rot.
4. **Truth maintenance.** One owner per fact; generate what is derivable from code and never hand-edit the
   output; stamp non-obvious facts with what they were verified against, not just when; gate what enters
   (no secrets, no speculation, no unverified recall); schedule consolidation and pruning, not only appending.
5. **Lazy topology.** Hub-and-spoke. Shard a hub only when its own index no longer fits one comfortable read;
   add a routing level only when the number of hubs does the same. Graphs emerge from evidence; never design
   one up front.

## Cross-Agent Invariants

- Durable state lives in agent-neutral files in the repository. The floor is `AGENTS.md`, with `CLAUDE.md` as
  a symlink where a client requires that name.
- Client capabilities — skill auto-discovery, subagents, lifecycle hooks, proprietary memory, auto-compaction
  — are progressive enhancement. Every one of them gets a files-based fallback: any skill's trigger condition
  also appears as a read-when line in the floor's routing table, so an agent with no discovery still finds the
  workflow.
- Deterministic obligations belong to repository-run gates (pre-commit, CI, task runner), which fire whichever
  agent edits. Prose orients; gates enforce. When a rule must hold every time, propose the gate.

## Enforcement

Run `scripts/check_context_architecture.py <repository-root>` after any change and resolve every finding. It
measures the system level: documents no index reaches, routing entries without a read-when condition, and
line-number references that rot. Pair it with `agents-management`'s `check_agent_context.py` for the
instruction-file level; neither substitutes for the other. Propose wiring both into the repository's gates.

Scripts prove structure, not behavior. The behavioral acceptance gate is the walk test in
[references/walk-test.md](references/walk-test.md); a context system nobody has walked is unmeasured, and its
efficiency claims are hypotheses.

## Completion

- Every created or moved document sits in exactly one genre and is reachable from the floor's routing table.
- The floor is no longer than the work found it, or the report states what was relocated and where.
- Both checkers pass, or every remaining finding is reported with a reason.
- Structural moves, deferred decisions, and unverified claims are reported explicitly.
- An audit ends with a dated record in the evaluations genre, not only a conversation reply.
