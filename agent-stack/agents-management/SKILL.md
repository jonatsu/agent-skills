---
name: agents-management
description: Create, maintain, and audit repo-local AGENTS.md, CLAUDE.md, scoped agent instructions, and llms.txt.
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

This skill covers repository-local context such as root and nested `AGENTS.md` or `CLAUDE.md` files,
vendor-specific instruction files, and `llms.txt`. A tracked file that this repository merely deploys into
another environment is a payload, not this repository's context.

Instruction files provide guidance. Hooks, permissions, and continuous integration provide deterministic
enforcement. When a rule must hold every time, propose or identify the enforcement mechanism and use prose
only to orient the agent.

## Choose the Branch

- **Initialize:** create a context system or add support for a target agent. Read
  [references/initialize.md](references/initialize.md), then load templates only if needed.
- **Maintain:** make a focused or broad update, repair drift, reconcile files, or migrate topology. Read
  [references/maintain.md](references/maintain.md).
- **Audit:** assess validity, loading, usefulness, coherence, or behavioral evidence without assuming edits
  are wanted. Read [references/audit.md](references/audit.md).

Read [references/loading-model.md](references/loading-model.md) when the branch must determine filenames,
precedence, includes, nesting, reload behavior, or symlink support. Load only the relevant client adapters.

## Shared Invariants

- Establish the target agents and repository boundary before judging topology.
- Preserve useful non-obvious knowledge, rationale, ordering constraints, failure modes, and generated-content
  boundaries, routed by when the agent needs them. An obligation the agent must satisfy before it can know it
  has a problem belongs in the instruction file, as one imperative line. Evidence needed only after a symptom
  appears belongs in a separate findings file that a symptom index points to. Never delete preserved evidence
  to shorten an instruction file; relocate it.
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
narrative that no longer changes any decision.

## Completion

For an edit, inspect every changed path and its removed lines. Restore any convention, reason, or gotcha that
was not deliberately superseded. Verify referenced paths and commands, link targets, intended client coverage,
generated-content boundaries, and the absence of placeholders. Use a fresh or reload-capable session when live
loading verification is available; otherwise state the limitation.

Then run `scripts/check_agent_context.py <repository-root>` and resolve every finding. It answers the accretion
test with a measurement rather than an impression, and it catches the two failures an edit cannot see from its
own diff: an evidence link that no longer resolves, and an evidence file that nothing indexes. Pass `--budget`,
`--budget-for`, `--evidence-dir` and `--exclude` when the repository's conventions differ from the defaults,
and `--help` for the full contract. Report its result rather than only that it ran.

A script the agent runs is weaker than a gate the repository runs. When the repository has a task runner,
pre-commit configuration, or continuous integration, propose wiring this check into it, so the next edit is
measured whether or not an agent loads this skill.

For an audit, deliver findings by severity with evidence, affected clients, and consequences. Keep mechanical
validity, loading and topology, content quality, whole-ruleset coherence, maintenance safety, and behavioral
evidence as separate judgments. Do not collapse them into an aggregate score or letter grade.

Preserve `ATTRIBUTIONS.md` and `LICENSE.upstream` during every update.
