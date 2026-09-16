---
name: technical-design
description: Design how a bounded software system or change should realize accepted requirements before implementation planning. Use for architecture, interfaces, state and data flow, failure handling, compatibility, migration, rollout, or rollback decisions; not for ideation, requirements specification, task sequencing, or reviewing an already settled design.
license: MIT AND CC-BY-SA-4.0
metadata:
  author: Joonas Onatsu
---

# Technical Design

Turn a bounded outcome into a coherent, reviewable explanation of system behavior and structure. Settle the decisions an
implementation planner would otherwise have to invent. Keep product ideation and implementation sequencing outside the
design.

## Establish the Design Basis

Read the governing requirements specification, overview or brainstorming draft, repository instructions, relevant
implementation, tests, interfaces, operations, and prior decisions before asking questions. Recover facts from those
sources instead of asking the user to repeat them.

Technical design may start from:

- an accepted requirements specification with settled observable behavior and acceptance;
- a brainstorming draft whose bounded direction already supplies the required observable behavior and constraints; or
- a bounded request whose outcome and scope are explicit enough that widening possibilities would add no value.

Return to brainstorming when a discovery changes the intended outcome, target user, product direction, or scope. Record
the conflict and keep the former direction provisional until the user resolves it. Return missing, contradictory, or
unaccepted user-visible behavior to `requirements-specification`. Do not disguise a product decision as architecture.

When the design introduces or leans on a domain term that is vague or contested — two words for one concept, or one
word stretched over two — engage `domain-modeling` to settle and record it rather than encoding the ambiguity into
interfaces and data flow. The language can be settled at whatever stage it surfaces; when design is what exposed it,
carry the resolved term back into the specification.

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

When a governing specification exists, identify the accepted revision and trace each consequential system guarantee to
the requirement it realizes. Use existing stable requirement identifiers or anchors; do not invent an ID scheme during
design. A newer accepted specification makes the affected design provisional until the change is reconciled.

Present alternatives only when a real consequential choice remains. Explain the difference, benefit, cost, likely
failure mode, and reversibility of each live option. Recommend a direction with reasons. Facts may be researched;
product judgment and material risk acceptance remain with the user.

## Contribute Domain Expertise

Design is interactive, but the agent is not a neutral facilitator. Adopt the subject-matter expertise the design
calls for, inferred from the design basis, and contribute it by default: surface the standard designs, established
patterns, applicable best practices, likely failure modes, and relevant prior art that bear on the outcome, rather
than deferring every technical judgment to the user. The user should not have to ask for this.

Bind every contribution to the evidence discipline above. An expert contribution is a labeled recommendation,
grounded in repository inspection or authoritative research wherever the claim is changeable, with genuine
uncertainty flagged rather than smoothed into false confidence. A confident but unverified domain assertion is the
failure this stance must avoid, because a wrong premise settled here propagates into the plan and the code.

Product policy stays with the user; contribute technical and domain judgment, not product decisions. Calibrate to
who holds authority for the subject at hand: defer more and confirm when the user is the domain expert, drive when
they are relying on the agent. When that authority is unclear at the design basis, state the stance in one line —
for example, that the agent will drive the domain expertise on a named area unless the user is the authority there —
so the user can redirect cheaply instead of granting expertise each time.

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

Use arc42 for new technical-design documents by default. Inspect the repository's documentation instructions and
relevant existing designs first. When continuing a document, preserve its organization. When joining an established
design set, follow its applicable template, terminology, markup, and document boundaries. Use arc42 to check coverage
within that structure; do not create a parallel design or reorganize existing documents solely to impose arc42.
An unrelated README or incidental layout does not establish a design convention. Explicit user instructions take
precedence. Briefly state the selected convention in the design basis; routine matching needs no separate approval.

For arc42, read [the writing guide](references/arc42-writing-guide.md) and use
[the template](assets/arc42-design-template.md). Read [the worked example](references/arc42-example.md) before the first
draft to calibrate explanation and depth. Keep the twelve numbered sections in order; tailor subsections and depth.
Use a short applicability statement or reference where sufficient. Remove authoring prompts from the finished document.
Do not invent requirements, stakeholders, thresholds, or risks to fill a section. Keep status and governing-source
links in a short preamble and the planning handoff in an unnumbered appendix.

For bounded changes, state the affected boundary and baseline, explain the changed design, and link unchanged system
documentation. In arc42, sections 1 and 10 summarize or reference accepted requirements; they do not acquire product authority.
Section 9 links existing decisions rather than duplicating them. An unresolved obligation remains a gap even when its
template section is present.

Orient the reader before introducing detail. Show the structure, explain its important relationships and rationale,
then describe selected internals. Explain concepts before relying on them. Use the same component names in diagrams,
responsibility tables, interfaces, and scenarios; name the component responsible for each runtime action. Use prose
to explain causes and trade-offs, tables for comparison or lookup, and diagrams to make relationships visible.

In the handoff, identify invariants, failure modes, and rollout/recovery obligations that need particular scrutiny or
qualification, with the evidence boundary and owner where known. Link applicable policy or coding constraints instead
of duplicating their rules. Implementation planning turns these obligations into explicit practice, review, and
validation steps; keep reviewer scheduling and execution commands out of the design.

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

- purpose, scope, and observable behavior still match the governing specification or intent;
- consequential requirements map to system guarantees without invented product policy;
- consequential behavior and architecture no longer require invention;
- responsibilities, interfaces, and state or data flows agree;
- the reader can identify component responsibilities, follow an important scenario, and explain the major decisions;
- names, interfaces, state transitions, and numerical claims agree across prose, diagrams, tables, and scenarios;
- consequential invariants and prohibited behavior are settled;
- important success, error, degraded, and recovery paths are defined;
- relevant compatibility, migration, security, privacy, accessibility, and operational obligations are settled;
- assumptions are verified or have a named validation owner; and
- remaining questions are implementation-local or explicitly deferred with their cost.

Before that confirmation, pressure-test the design with `grilling`: walk its load-bearing and hard-to-reverse
decisions for the ones a reviewer would challenge, and resolve or explicitly defer each. Skip only with a stated
reason, or at the user's direction. A design handed to planning un-pressure-tested is the common source of a plan
built on an unexamined choice.

Then ask for one final confirmation that the design matches the user's understanding of the system to be planned. Earlier
confirmation of individual choices does not replace this shared-understanding check. A clear response to that final
design synthesis already supplies the confirmation; do not ask the user to repeat it.

The confirmation must follow the complete design synthesis and cover every consequential decision introduced during
design. A confirmation given before those decisions cannot confirm them. For a request to design and plan in one
conversation, finish the separate design, present its final synthesis, and stop for this confirmation. Begin the separate
implementation plan only after the user's next clear response accepts that synthesis.

If the check exposes a design gap, continue designing or record the blocker. If it exposes a changed outcome or scope,
return to brainstorming. Do not hand unresolved architecture to planning merely to keep the workflow moving.
