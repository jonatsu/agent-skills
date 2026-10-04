---
name: writing-specs
description: Write the spec for a product, app, tool, or feature from an accepted direction or bounded request, as a reviewable requirements specification of its actors, user journeys, observable behavior, constraints, acceptance, non-goals, and change authority. Use when writing or refining a spec, PRD, SRS, requirements, user journeys, or acceptance criteria; not for ideation, architecture, implementation planning, or repository instructions.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Writing Specs

Write the spec: the formal, written statement (a requirements specification) of what a finished product, app, tool,
or feature must do. It states who uses it, what they do with it, the behavior they observe, the constraints it must
respect, how acceptance is judged, what is out of scope, and who may change the spec. It names no components, files,
or tasks; the design and the plan own those. Keep it the smallest durable contract that preserves intent. The spec owns
intended observable behavior; it does not describe current code merely because that code exists.

## Establish the Spec Basis

Read the governing overview or idea-brainstorming draft, accepted product decisions, relevant current behavior, domain
evidence, and repository conventions before asking questions. Recover established facts instead of asking the user to
repeat them.

A spec may start from:

- an accepted idea-brainstorming direction with a legible purpose, actors, scope, constraints, success signal, and open
  requirements questions;
- a bounded request that already fixes its purpose and scope but still needs durable behavioral detail or acceptance;
  or
- a technical design in progress that began deciding user-visible behavior, user journeys, or acceptance that no spec
  covered, where the user accepted the proposal to write one. Take that behavior over as proposed requirements, and
  treat the design's choices on it as recommendations, not decisions.

Return to `idea-brainstorming` when the intended outcome, actor, product direction, or scope remains genuinely open.
Whether to write a spec is the user's decision. A small, local change needs none when the request already settles its
observable result, boundaries, and acceptance and no later reader needs a durable contract; hand that work directly to
`technical-design` or `implementation-planning` as its remaining decisions require, because a spec written only to fill
a stage has no reader.

Repository inspection establishes current behavior and technical constraints, not desired policy. Treat unsupported
users, priorities, entitlements, retention rules, service levels, and compliance duties as provisional until the user
or an authoritative product artifact supplies them.

When a term for an actor, behavior, or domain concept is contested or overloaded (two words for one thing, or one word
stretched over two), engage `domain-modeling` to settle it and record it in the project's glossary before specifying
behavior on it. Ambiguous vocabulary fixed here propagates into every downstream artifact, and this is the stage where
the shared language most cheaply originates. Skip only with a stated reason, or at the user's direction.

## Separate Authority and Status

State whether the spec is proposed, accepted, superseded, or retired and identify the governing intent. An accepted spec
is authoritative for intended observable behavior within its scope. Code and reference documentation remain
authoritative for what the system currently does. A disagreement between them is an implementation gap, a requirements
change, or stale documentation to reconcile; the spec changes only through its owner, never to make accidental behavior
look compliant.

Keep these categories distinguishable through the document's structure:

- observed current behavior and external facts, with their evidence;
- accepted user or product decisions;
- recommendations awaiting a decision;
- provisional assumptions and the evidence or owner that can settle them; and
- open questions whose answers block acceptance.

Carry them in the status line, a decisions list, one open-questions register, and a marker on each assumed
requirement. The text of a requirement states the requirement only; provenance narration such as "confirmed with the
customer" or "verified against the code" belongs in those structures or nowhere.

Only the user or another identified requirements owner may accept or change a consequential requirement. An agent may
draft, find gaps, and recommend wording; its own elaboration stays a recommendation until that owner, often the
customer, has reviewed it. Before specifying behavior on a role, route, or state that another requirement names, check
that it is defined and could work.

## Specify Observable Behavior

Define only the parts relevant to the outcome:

- purpose, affected actors, and the need or harm being addressed;
- scope, non-goals, and product-level prohibited outcomes;
- representative journeys or scenarios, including success, error, denial, interruption, and recovery where relevant;
- inputs, outputs, externally visible states and transitions, and domain rules;
- functional behavior at system boundaries without choosing internal mechanisms;
- security, privacy, accessibility, performance, retention, compliance, and operational requirements that materially
  constrain acceptance;
- dependencies on external policy, data, services, or other specs; and
- assumptions, unresolved requirements, and decision owners.

Write requirements as observable claims. State who encounters what condition and what result must follow. Where the
project has no form of its own, write each requirement as one sentence in EARS (the Easy Approach to Requirements
Syntax) with "shall": `When <trigger>, the <system> shall <response>.` Define each priority by its consequence
("Critical: the customer cannot ship without it"). A Notes field states what the requirement does not cover and stops;
it never argues for the requirement.

Use examples when they settle ambiguity, especially for boundary values, denials, retries, concurrency, ordering, or
data isolation. An example illustrates a confirmed rule; one that implies an unconfirmed rule is marked provisional
like the rule itself.

Quantify only when the metric, method, population, and threshold express real success or a supplied constraint. When
honest measurement is unavailable, use a binary observation or named human judgment rather than decorative precision.

## Define Acceptance Without Designing Tests

Acceptance criteria describe evidence-bearing outcomes, not task completion or source shape. Cover consequential
positive behavior and negative guarantees. A criterion may use a concrete input and expected output, a state transition,
an externally observable invariant, or a qualified human judgment.

Keep verification design in its proper phase. The spec may require conformance to an existing protocol, schema, policy,
or reusable fixture when that artifact is itself part of the requirement. Technical design chooses the system contracts
that realize it; implementation planning chooses commands, environments, test levels, and review gates. Build
commands, file paths, test-runner instructions, and implementation checklists therefore stay out of the spec.

Use stable requirement identifiers only when another spec, design, plan, test suite, or audit will cite them. Prefer
descriptive anchors for a small self-contained spec. If identifiers earn their cost, keep them stable through wording
changes, retire rather than recycle them, and never encode priority or document position in the ID.

## Keep the Artifact Proportional and Navigable

One cohesive outcome gets one authoritative overview. Keep a bounded spec in one file while a reader can load and
review it comfortably. Keep architecture, repository commands, and task order in the separate artifacts that own them,
and link those from the spec rather than merging them into one `SPEC.md`.

Split a large spec only when its behavioral domains can be loaded, reviewed, and changed independently. Split by
user-visible responsibility, not an assumed implementation layer; a frontend/backend division belongs to technical
design unless the product itself exposes those as independent contracts. The overview retains purpose, global scope and
non-goals, shared vocabulary, cross-cutting requirements, authority, status, and a short dependency map. Each child owns
one actor journey or cohesive behavioral domain plus its local acceptance criteria and open questions. Route children
with trigger-keyed tables or standalone inclusion links. Each shared requirement lives once, in the overview, and
consumers link to it, because copies drift into subtly different requirements.

Resolve the artifact path in this order:

1. Use a path supplied by the user.
2. Continue the same existing spec already in scope.
3. Follow a governing artifact's companion-document map.
4. Follow a documented repository convention.
5. Follow one clear convention established by existing specs.
6. Otherwise propose `docs/specs/<name>.md`, its place in `context-architecture`'s default layout, and ask once
   before creating the new directory.
7. Outside a repository, ask for a destination.

Use two or three descriptive kebab-case words for the fallback name. For a modular spec, put the overview at
`docs/specs/<name>/index.md` and keep children in that directory unless an established convention says otherwise.

## Write for the Reader

A spec is read by people who were not in the conversation that produced it: designers, testers, reviewers, and the
customer. It fails when they cannot read it, however correct its requirements. Write it with `writing-documentation`,
and finish with the `writing-for-humans` **reader-ready** pass before asking for acceptance.

Explain each domain concept, actor role, and external system where the spec first relies on it, once. State scope,
governing sources, and versions once, in the preamble. Lead each sentence with the requirement or behavior, and append
an identifier only where traceability needs it.

## Review, Accept, and Revise

Before asking for acceptance, check that:

- purpose, actors, scope, non-goals, and terminology agree;
- each requirement is observable, necessary, and implementation-neutral at the appropriate boundary;
- important success, error, denial, interruption, and recovery behavior is settled;
- acceptance criteria cover the consequential behavior without merely restating it;
- requirements do not contradict each other or verified external constraints;
- assumptions and recommendations are not disguised as decisions;
- cross-spec dependencies and shared requirements have one owner;
- remaining questions are explicitly nonblocking or have an owner and consequence; and
- the complete document passes the `writing-for-humans` **reader-ready** pass.

Present the complete spec synthesis, then ask for one confirmation that it matches the intended behavior. A clear
response accepting that synthesis is sufficient and needs no repetition. Saving a proposed draft does not make it
accepted, and accepting it does not authorize technical design or implementation unless the request already supplied
that authority.

When an accepted requirement changes, identify the affected specs, designs, implementation plans, tests, documentation,
and released behavior. Mark dependent artifacts stale until their owners reconcile the change. Return a changed purpose
or product scope to `idea-brainstorming`, and internal architecture consequences to `technical-design`.

When implementation exists and the user asks whether it matches the accepted spec, route the comparison to
`conformance-review`. This skill owns authoring and authorized revision of intended behavior; it does not judge
implementation evidence.

## Handoff

Hand technical design an accepted spec or a clearly bounded accepted section. Name the governing revision, requirements
needing particular design scrutiny, negative guarantees, external constraints, unresolved nonblocking assumptions, and
any conformance artifacts. Leave components, interfaces, files, tasks, verification commands, and rollout sequence to
the design and the plan.

A spec is ready when its intended behavior is accepted and a technical designer can realize it without inventing
product policy. If acceptance still depends on a consequential unanswered requirement, keep the spec proposed and
report the blocker.
