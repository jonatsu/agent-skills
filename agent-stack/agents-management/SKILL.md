---
name: agents-management
description: Create, maintain, and audit repo-local AGENTS.md, CLAUDE.md, scoped agent instructions, and llms.txt. Owns instruction-file internals; the documentation layout above them — which documents exist and how they are organized and routed — belongs to context-architecture, which is also the entry point for repositories with no established layout.
license: Apache-2.0
compatibility: Requires Python 3.9 or later on PATH for scripts/check_agent_context.py. Every other capability works without it.
metadata:
  author: Joonas Onatsu
---

# Agents Management

Build and maintain the smallest repository-local context system that gives each intended agent accurate,
useful guidance.

Repository facts are the authority for commands, paths, architecture, and conventions. Verify each claim
against the repository or label it unverified. Do not infer an ecosystem for a greenfield repository or choose
between conflicting manifests without evidence.

## Scope

This skill covers instruction files and the context around them: root and nested `AGENTS.md` or `CLAUDE.md`
files, vendor-specific instruction files, and `llms.txt`. **Scope follows the file, not the repository.** A
ruleset authored here and loaded at user or machine scope is an instruction file, and the tests below bind
harder there, because every word is charged to every session of every agent rather than to one repository's. A
tracked file this repository only relays into another environment, such as a deployed copy of something
authored elsewhere, is a payload rather than context.

Instruction files provide guidance. Hooks, permissions, and continuous integration provide deterministic
enforcement. When a rule must hold every time, propose or identify the enforcement mechanism and use prose
only to orient the agent.

## Choose the Branch

- **Initialize:** create instruction files or add support for a target agent. When the repository has no
  established documentation layout, the layout decision comes first and belongs to `context-architecture` —
  start there; it invokes this branch as the executor. Then read
  [references/initialize.md](references/initialize.md), and load templates only if needed.
- **Maintain:** make a focused or broad update, repair drift, reconcile files, or migrate topology. Read
  [references/maintain.md](references/maintain.md).
- **Audit:** assess validity, loading, usefulness, coherence, or behavioral evidence without assuming edits
  are wanted. Read [references/audit.md](references/audit.md). This branch's object is instruction files;
  auditing the documentation system above them — genres, routing coverage, layout — belongs to
  `context-architecture`, which delegates the instruction-file level back here.

Read [references/loading-model.md](references/loading-model.md) when the branch must determine filenames,
precedence, includes, nesting, reload behavior, or symlink support. Load only the relevant client adapters.

## Shared Invariants

- Establish the target agents and repository boundary before judging topology.
- Preserve useful non-obvious knowledge, rationale, ordering constraints, failure modes, and generated-content
  boundaries, routed by when the agent needs them. An obligation the agent must satisfy before it can know it
  has a problem belongs in the instruction file, as one imperative line. Evidence needed only after a symptom
  appears belongs in a separate findings file that a symptom index points to. Never delete preserved evidence
  to shorten an instruction file; relocate it.
- The symptom index may live outside the instruction file, in the evidence directory's own `README.md`, with
  the instruction file routing to it. That trade is real rather than free: an instruction file arrives without
  being asked for, an index only when something follows the route. So keep on the floor the symptoms an agent
  meets **while already in trouble**, and leave the ones it looks up deliberately to the index. A symptom
  owned by a subtree belongs to that subtree's instruction file and should never reach the root at all.
- **Write in plain language, and size detail to consequence.** An instruction file is read under load by
  something deciding what to do next, so every sentence carries a fact, a constraint, or an action, and each
  one leads with the rule rather than its rationale — an agent that stops reading mid-passage must still have
  the obligation. Prefer the specific term to the general one, and ordinary words to impressive ones. Omit
  filler, repetition, hedging, and praise for the repository or its tools. Brevity never costs a constraint, a
  risk, an ordering dependency, or a trade-off: state what the reader must not get wrong in as much detail as
  getting it wrong would cost.
- Never overwrite or automatically reconcile two divergent real context files. Show their unique and
  conflicting content, explain which clients receive each file, and ask which content should survive.
- Reuse authorization in the user's request. Ask only when an unresolved choice changes topology, public
  behavior, compatibility, data preservation, cost, or scope.
- Do not create vendor-specific files merely because the skill recognizes them. Every file must serve a target
  client or a verified repository need.
- Keep `llms.txt` conditional. It indexes documentation for language models; it is not an instruction file.
- Report unknown loading behavior and unavailable evidence without blocking useful work for recognized
  capabilities.

For additions, apply two tests. The **cache test** asks whether the agent can recover the fact cheaply from
the repository or authoritative runtime help. The **behavior test** asks whether the instruction changes
likely agent behavior. Retain a derivable fact only when it adds a reason, constraint, ordering dependency, or
failure mode that the source does not show.

Those two tests judge a single addition. The **accretion test** judges the file: an edit that adds an
obligation must leave the instruction file no longer than it found it, or state what it relocated and where.
Every passage in a bloated instruction file passed the other two tests on the day it arrived, so neither one
can detect accumulation. A file that only grows becomes an incident log whose rules compete for attention with
narrative that no longer changes any decision. Satisfy it by relocating detail, never by cutting a qualifier
the reader must not get wrong and never by compressing clear guidance into cryptic density: the target is the
shortest wording that stays clear and complete, not the shortest wording.

## Completion

For an edit, inspect every changed path and its removed lines. Restore any convention, reason, or gotcha that
was not deliberately superseded. Verify referenced paths and commands, link targets, intended client coverage,
generated-content boundaries, and the absence of placeholders. Use a fresh or reload-capable session when live
loading verification is available; otherwise state the limitation.

Then run `scripts/check_agent_context.py <repository-root>` and resolve every finding. It answers the accretion
test with a measurement rather than an impression, and it catches the two failures an edit cannot see from its
own diff: an evidence link that no longer resolves, and an evidence file that nothing reaches. It follows
exactly one hop through the evidence directory's own index, and only when an instruction file routes to that
index, so deleting the route reports every file the index carried. Pass `--budget`,
`--budget-for`, `--evidence-dir` and `--exclude` when the repository's conventions differ from the defaults,
and `--help` for the full contract. Report its result rather than only that it ran.

**`--names` is what points the script at a ruleset whose files are not called `AGENTS.md` or `CLAUDE.md`**, so
pass it whenever the files under review carry their own names. Without it the run measures the default set and
reports it clean, which reads as a pass for files it never opened. Check the count it prints against the files
you meant to cover, and exclude any archived copies the names would also match.

A script the agent runs is weaker than a gate the repository runs. When the repository has a task runner,
pre-commit configuration, or continuous integration, propose wiring this check into it, so the next edit is
measured whether or not an agent loads this skill.

For an audit, deliver findings by severity with evidence, affected clients, and consequences. Keep mechanical
validity, loading and topology, content quality, whole-ruleset coherence, maintenance safety, and behavioral
evidence as separate judgments. Do not collapse them into an aggregate score or letter grade.

Preserve `ATTRIBUTIONS.md` and `LICENSE.upstream` during every update.
