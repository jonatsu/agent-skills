---
name: technical-design
description: Design how a bounded software system or change should behave and fit together before implementation planning. Use for architecture, interfaces, state and data flow, failure handling, compatibility, migration, rollout, or rollback decisions; not for early ideation, task sequencing, or reviewing an already settled design.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Technical Design

Turn a bounded outcome into a coherent, reviewable explanation of system behavior and structure. Settle the decisions an
implementation planner would otherwise have to invent. Keep product ideation and implementation sequencing outside the
design.

## Establish the Design Basis

Read the governing overview or brainstorming draft, repository instructions, relevant implementation, tests,
interfaces, operations, and prior decisions before asking questions. Recover facts from those sources instead of asking
the user to repeat them.

Technical design may start from either:

- a brainstorming draft with a legible purpose, selected direction, scope, constraints, and open design questions; or
- a bounded request whose outcome and scope are explicit enough that widening possibilities would add no value.

Return to brainstorming when a discovery changes the intended outcome, target user, product direction, or scope. Record
the conflict and keep the former direction provisional until the user resolves it. Do not disguise a product decision as
architecture.

## Investigate Before Deciding

Inspect the surfaces that could change the recommendation. Depending on the subject, establish current responsibilities,
public and internal interfaces, state and data flow, dependencies, tests, operational behavior, compatibility obligations,
and relevant prior decisions.

Use the smallest design depth that settles the consequential system choices. Expand the relevant analysis for security,
authorization, persistent data, migrations, compatibility, external dependencies, material cost, or difficult recovery.
Do not add sections for risks that do not apply.

Implementation and tests establish current technical behavior, not desired product or business policy. Treat target
users, priorities, pricing, retention rules, compliance duties, and service levels as intended policy only when the user
or an authoritative product artifact supplies them. Keep unsupported policy provisional or return a changed outcome to
brainstorming.

Keep evidence and judgment distinct:

- state current behavior and constraints supported by repository inspection or authoritative research;
- preserve accepted requirements and user decisions;
- label recommendations and explain their rationale;
- identify provisional assumptions and the evidence needed to settle them; and
- distinguish blocking questions from details that may safely wait for implementation.

Present alternatives only when a real consequential choice remains. Explain the difference, benefit, cost, likely
failure mode, and reversibility of each live option. Recommend a direction with reasons. Facts may be researched;
product judgment and material risk acceptance remain with the user.

## Define the System

Settle the parts relevant to the requested outcome:

- externally visible and internal behavior;
- component responsibilities and boundaries;
- interfaces, contracts, states, transitions, and data flow;
- invariants and prohibited behavior, including access and disclosure boundaries;
- validation, errors, degraded operation, recovery, and idempotency;
- security, privacy, accessibility, performance, and operational consequences;
- compatibility and migration behavior; and
- observability, rollout, and rollback when the change requires them.

Translate accepted product harms into system guarantees. Define relevant denial, disclosure, failure, and recovery
behavior without prescribing verification commands or implementation order.

Technical design decides whether rollout and rollback are required and defines their behavioral and safety obligations.
Implementation planning later orders the work and checks that implement those decisions.

Name implementation surfaces only when they establish evidence or clarify responsibility. Do not prescribe edit order,
source line ranges, commits, task assignments, or implementation status.

## Write the Design Artifact

Use an outcome-based structure rather than filling a fixed template. Give the reader enough context to understand the
governing intent, local scope, evidence, chosen system shape, behavior, interfaces, important paths, consequences,
alternatives, risks, assumptions, and open questions. End with a planning handoff that names settled obligations without
sequencing their implementation.

Use diagrams, tables, examples, state descriptions, or sequence narratives only when they materially clarify a
relationship or behavior. Keep every canonical decision recoverable in text.

Resolve the artifact path in this order:

1. Use a path supplied by the user.
2. Continue the same existing design already in scope.
3. Follow a governing artifact's companion-document map.
4. Follow a documented repository convention.
5. Follow one clear convention established by existing artifacts.
6. Otherwise propose `docs/plans/<name>-design.md` and ask once.
7. Outside a repository, ask for a destination.

Use two or three descriptive kebab-case words before `-design.md` in the fallback. Competing conventions, a new
directory, or an unrelated collision require user direction. Saving a design does not authorize implementation.

## Confirm the Handoff

Before handing the design to implementation planning, check that:

- purpose and scope still match the governing intent;
- consequential behavior and architecture no longer require invention;
- responsibilities, interfaces, and state or data flows agree;
- consequential invariants and prohibited behavior are settled;
- important success, error, degraded, and recovery paths are defined;
- relevant compatibility, migration, security, privacy, accessibility, and operational obligations are settled;
- assumptions are verified or have a named validation owner; and
- remaining questions are implementation-local or explicitly deferred with their cost.

Then ask for one final confirmation that the design matches the user's understanding of the system to be planned. Earlier
confirmation of individual choices does not replace this shared-understanding check. A clear response to that final
design synthesis already supplies the confirmation; do not ask the user to repeat it.

The confirmation must follow the complete design synthesis and cover every consequential decision introduced during
design. A confirmation given before those decisions cannot confirm them. For a request to design and plan in one
conversation, finish the separate design, present its final synthesis, and stop for this confirmation. Begin the separate
implementation plan only after the user's next clear response accepts that synthesis.

If the check exposes a design gap, continue designing or record the blocker. If it exposes a changed outcome or scope,
return to brainstorming. Do not hand unresolved architecture to planning merely to keep the workflow moving.
