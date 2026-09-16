---
name: requirements-specification
description: Turn an accepted product direction or bounded request into a reviewable requirements specification defining actors, user journeys, observable behavior, constraints, acceptance, non-goals, and change authority. Use when writing or refining a product or feature spec, PRD, SRS, requirements, user journeys, or acceptance criteria; not for ideation, architecture, implementation planning, or repository instructions.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Requirements Specification

Turn an accepted direction into the smallest durable contract that states what must be true for its users and
stakeholders. Preserve intent without deciding architecture or implementation order. A specification owns intended
observable behavior; it does not describe current code merely because that code exists.

## Establish the Specification Basis

Read the governing overview or brainstorming draft, accepted product decisions, relevant current behavior, domain
evidence, and repository conventions before asking questions. Recover established facts instead of asking the user to
repeat them.

Specification may start from either:

- an accepted brainstorming direction with a legible purpose, actors, scope, constraints, success signal, and open
  requirements questions; or
- a bounded request that already fixes its purpose and scope but still needs durable behavioral detail or acceptance.

Return to `brainstorming` when the intended outcome, actor, product direction, or scope remains genuinely open. A small,
local change needs no specification artifact when the request already settles its observable result, boundaries, and
acceptance and no later reader needs a durable contract. Hand that work directly to technical design or implementation
planning as its remaining decisions require; do not manufacture a miniature PRD.

Repository inspection establishes current behavior and technical constraints, not desired policy. Treat unsupported
users, priorities, entitlements, retention rules, service levels, and compliance duties as provisional until the user
or an authoritative product artifact supplies them.

When a term for an actor, behavior, or domain concept is contested or overloaded — two words for one thing, or one word
stretched over two — engage `domain-modeling` to settle it and record it in the project's glossary before specifying
behavior on it. Ambiguous vocabulary fixed here propagates into every downstream artifact; this is the stage where the
ubiquitous language most cheaply originates. Skip only with a stated reason, or at the user's direction.

## Separate Authority and Status

State whether the specification is proposed, accepted, superseded, or retired and identify the governing intent. An
accepted specification is authoritative for intended observable behavior within its scope. Code and reference
documentation remain authoritative for what the system currently does; a disagreement is an implementation gap, a
requirements change, or stale documentation to reconcile rather than permission to silently rewrite the specification.

Keep these categories distinguishable throughout:

- observed current behavior and external facts, with their evidence;
- accepted user or product decisions;
- recommendations awaiting a decision;
- provisional assumptions and the evidence or owner that can settle them; and
- open questions whose answers block acceptance.

Only the user or another identified requirements owner may accept or change a consequential requirement. An agent may
draft, find gaps, and recommend wording; it must not turn its own elaboration into an accepted requirement.

## Specify Observable Behavior

Define only the parts relevant to the outcome:

- purpose, affected actors, and the need or harm being addressed;
- scope, non-goals, and product-level prohibited outcomes;
- representative journeys or scenarios, including success, error, denial, interruption, and recovery where relevant;
- inputs, outputs, externally visible states and transitions, and domain rules;
- functional behavior at system boundaries without choosing internal mechanisms;
- security, privacy, accessibility, performance, retention, compliance, and operational requirements that materially
  constrain acceptance;
- dependencies on external policy, data, services, or other specifications; and
- assumptions, unresolved requirements, and decision owners.

Write requirements as observable claims. State who encounters what condition and what result must follow. Use examples
when they settle ambiguity, especially for boundary values, denials, retries, concurrency, ordering, or data isolation.
Do not use examples to smuggle in an unconfirmed rule.

Quantify only when the metric, method, population, and threshold express real success or a supplied constraint. When
honest measurement is unavailable, use a binary observation or named human judgment rather than decorative precision.

## Define Acceptance Without Designing Tests

Acceptance criteria describe evidence-bearing outcomes, not task completion or source shape. Cover consequential
positive behavior and negative guarantees. A criterion may use a concrete input and expected output, a state transition,
an externally observable invariant, or a qualified human judgment.

Keep verification design in its proper phase. The specification may require conformance to an existing protocol,
schema, policy, or reusable fixture when that artifact is itself part of the requirement. Technical design chooses the
system contracts that realize it; implementation planning chooses commands, environments, test levels, and review gates.
Do not put build commands, file paths, test-runner instructions, or implementation checklists into the specification.

Use stable requirement identifiers only when another specification, design, plan, test suite, or audit will cite them.
Prefer descriptive anchors for a small self-contained specification. If identifiers earn their cost, keep them stable
through wording changes, retire rather than recycle them, and never encode priority or document position in the ID.

## Keep the Artifact Proportional and Navigable

One cohesive outcome gets one authoritative overview. Keep a bounded specification in one file while a reader can load
and review it comfortably. Do not combine requirements, architecture, repository commands, and task order into one
`SPEC.md`; link the separate artifacts that own those concerns.

Split a large specification only when its behavioral domains can be loaded, reviewed, and changed independently. The
overview retains purpose, global scope and non-goals, shared vocabulary, cross-cutting requirements, authority, status,
and a short dependency map. Each child owns one actor journey or cohesive behavioral domain plus its local acceptance
criteria and open questions. Route children with trigger-keyed tables or standalone inclusion links; do not duplicate
the overview's requirements into every child.

Split by user-visible responsibility, not an assumed implementation layer. A frontend/backend division belongs to
technical design unless the product itself exposes those as independent contracts. Keep a shared requirement in the
overview and link to it from consumers rather than creating subtly different copies.

Resolve the artifact path in this order:

1. Use a path supplied by the user.
2. Continue the same existing specification already in scope.
3. Follow a governing artifact's companion-document map.
4. Follow a documented repository convention.
5. Follow one clear convention established by existing specifications.
6. Otherwise propose `docs/specs/<name>.md` and ask once before creating the new directory.
7. Outside a repository, ask for a destination.

Use two or three descriptive kebab-case words for the fallback name. For a modular specification, put the overview at
`docs/specs/<name>/index.md` and keep children in that directory unless an established convention says otherwise.

## Review, Accept, and Revise

Before asking for acceptance, check that:

- purpose, actors, scope, non-goals, and terminology agree;
- each requirement is observable, necessary, and implementation-neutral at the appropriate boundary;
- important success, error, denial, interruption, and recovery behavior is settled;
- acceptance criteria cover the consequential behavior without merely restating it;
- requirements do not contradict each other or verified external constraints;
- assumptions and recommendations are not disguised as decisions;
- cross-specification dependencies and shared requirements have one owner; and
- remaining questions are explicitly nonblocking or have an owner and consequence.

Present the complete specification synthesis, then ask for one confirmation that it matches the intended behavior. A
clear response accepting that synthesis is sufficient; do not ask the user to repeat it. Saving a proposed draft does
not make it accepted, and accepting it does not authorize technical design or implementation unless the request already
supplied that authority.

When an accepted requirement changes, identify the affected specifications, designs, implementation plans, tests,
documentation, and released behavior. Mark dependent artifacts stale until their owners reconcile the change. Return a
changed purpose or product scope to brainstorming. Return internal architecture consequences to technical design. Do
not edit the specification after implementation merely to make an accidental behavior look compliant.

When implementation exists and the user asks whether it matches the accepted specification, route the comparison to
`spec-conformance-review`. This skill owns authoring and authorized revision of intended behavior; it does not judge
implementation evidence.

## Handoff

Hand technical design an accepted specification or a clearly bounded accepted section. Name the governing revision,
requirements needing particular design scrutiny, negative guarantees, external constraints, unresolved nonblocking
assumptions, and any conformance artifacts. Do not prescribe components, interfaces, files, tasks, verification commands,
or rollout sequence.

A specification is ready when its intended behavior is accepted and a technical designer can realize it without
inventing product policy. If acceptance still depends on a consequential unanswered requirement, keep the specification
proposed and report the blocker.
