---
name: technical-design
description: Design how a bounded software system or change should realize accepted requirements, and write its design document, before implementation planning. Use for architecture, interfaces, state and data flow, failure handling, compatibility, migration, rollout, or rollback decisions, and for writing or revising a design document or arc42 design; not for ideation, requirements specification, task sequencing, or reviewing an already settled design.
license: MIT AND CC-BY-SA-4.0
metadata:
  author: Joonas Onatsu
---

# Technical Design

Turn a bounded outcome into a coherent, reviewable explanation of system behavior and structure. Settle the decisions an
implementation planner would otherwise have to invent. Keep product ideation and implementation sequencing outside the
design.

## Establish the Design Basis

Read the governing requirements specification, overview or idea-brainstorming draft, repository instructions, relevant
implementation, tests, interfaces, operations, and prior decisions before asking questions. Recover facts from those
sources instead of asking the user to repeat them.

Technical design may start from:

- an accepted requirements specification with settled observable behavior and acceptance;
- an idea-brainstorming draft whose bounded direction already supplies the required observable behavior and
  constraints; or
- a bounded request whose outcome and scope are explicit enough that widening possibilities would add no value.

Return to idea-brainstorming when a discovery changes the intended outcome, target user, product direction, or scope. Record
the conflict and keep the former direction provisional until the user resolves it. Return missing, contradictory, or
unaccepted user-visible behavior to `writing-specs`. Do not disguise a product decision as architecture.

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
idea-brainstorming.

Check every claim about an upstream or third-party mechanism against its pinned source, never against memory or a
summary. A wrong premise settled here propagates into the plan and the code. Where no ready component does what the
design needs, write the custom step as a design task, not as a finding or an open question.

Keep evidence and judgment distinct:

- state current behavior and constraints supported by repository inspection or authoritative research;
- preserve accepted requirements and user decisions;
- label recommendations and explain their rationale;
- identify provisional assumptions and the evidence needed to settle them; and
- distinguish blocking questions from details that may safely wait for implementation.

Carry that distinction in the document's structure: its status line, the decisions section, one questions register,
and a marker on each provisional decision. Mark a provisional decision as provisional everywhere it lands, including
the questions register, where it is assumed rather than resolved. The design text states the design; provenance
narration such as "verified against" or "confirmed in" belongs in those structures or nowhere.

When a governing specification exists, identify the accepted revision and trace each consequential system guarantee to
the requirement it realizes. State the guarantee first and append the requirement's existing identifier or anchor; do
not invent an ID scheme during design. A newer accepted specification makes the affected design provisional until the
change is reconciled.

Present alternatives only when a real consequential choice remains. Explain the difference, benefit, cost, likely
failure mode, and reversibility of each live option. Recommend a direction with reasons. Facts may be researched;
product judgment and material risk acceptance remain with the user. Once decided, the document states each rejected
alternative directly, with the reason it lost.

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

## Choose the Format

Use arc42 for new technical-design documents by default. Inspect the repository's documentation instructions and
relevant existing designs first. When continuing a document, preserve its organization. When joining an established
design set, follow its applicable template, terminology, markup, and document boundaries. Use arc42 to check coverage
within that structure; do not create a parallel design or reorganize existing documents solely to impose arc42.
An unrelated README or incidental layout does not establish a design convention. Explicit user instructions take
precedence. Briefly state the selected convention in the design basis; routine matching needs no separate approval.

For arc42, read [the writing guide](references/arc42-writing-guide.md) and use
[the template](assets/arc42-design-template.md). Read [the worked example](references/arc42-example.md) before the first
draft to calibrate explanation and depth. Keep arc42's section numbers and order, and omit a section that would carry
nothing, so the numbers stay stable and the reader meets no empty headings. Tailor subsections and depth. Remove
authoring prompts from the finished document. Do not invent requirements, stakeholders, thresholds, or risks to fill
a section. Keep status and governing-source links in a short preamble and the planning handoff in an unnumbered
appendix.

For bounded changes, state the affected boundary and baseline, explain the changed design, and link unchanged system
documentation. In arc42, sections 1 and 10 reference accepted requirements rather than restating them, and they do not
acquire product authority. Section 9 links existing decisions rather than duplicating them. An unresolved obligation
remains a gap, recorded in the questions register.

A design leads implementation, then follows it: once code exists, the code wins and the design is updated to match.
The status line says so. Open items live in one questions register and one task ledger, linked from the design, never
as "not designed" in its text.

## Write for the Reader

A design is read by implementers, reviewers, and later maintainers who were not in the conversation that produced it.
Write it with `writing-documentation`, and finish with the `writing-for-humans` **reader-ready** pass before the
handoff. The bar: a first-time reader could re-derive the implementation from the documents alone, and once the design
is reviewed, any working note behind it is deletable without losing anything an implementer needs.

Orient the reader before introducing detail. Show the structure, explain its important relationships and rationale,
then describe selected internals. Explain each concept, mechanism, and component where the design first relies on it,
once. Use the same component names in diagrams, responsibility tables, interfaces, and scenarios; name the component
responsible for each runtime action. Use prose to explain causes and trade-offs, tables for comparison or lookup, and
diagrams to make relationships visible, only where each materially clarifies. Keep every canonical decision
recoverable in text.

In the handoff, identify invariants, failure modes, and rollout/recovery obligations that need particular scrutiny or
qualification, with the evidence boundary and owner where known. Link applicable policy or coding constraints instead
of duplicating their rules. Implementation planning turns these obligations into explicit practice, review, and
validation steps; keep reviewer scheduling and execution commands out of the design.

## Artifact Path

Resolve the artifact path in this order:

1. Use a path supplied by the user.
2. Continue the same existing design already in scope.
3. Follow a governing artifact's companion-document map.
4. Follow a documented repository convention.
5. Follow one clear convention established by existing artifacts.
6. Otherwise propose `docs/plans/<name>-design.md`, its place in `context-architecture`'s default layout, and
   ask once.
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
- assumptions are verified or have a named validation owner;
- remaining questions are implementation-local or explicitly deferred with their cost; and
- the design meets the reader bar in "Write for the Reader" and passes the **reader-ready** pass.

Before that confirmation, pressure-test the design with `interview-me`: walk its load-bearing and hard-to-reverse
decisions for the ones a reviewer would challenge, and resolve or explicitly defer each. Skip only with a stated
reason, or at the user's direction. A design handed to planning un-pressure-tested is the common source of a plan
built on an unexamined choice.

Then present the complete design synthesis and ask for one confirmation that it matches the user's understanding of
the system to be planned. Only a confirmation given after every consequential decision confirms them; earlier
confirmation of individual choices does not. A clear response to the synthesis is the confirmation, so do not ask the
user to repeat it. For a request to design and plan in one conversation, stop here, and begin the separate
implementation plan only after that response.

If the check exposes a design gap, continue designing or record the blocker. If it exposes a changed outcome or scope,
return to idea-brainstorming. Do not hand unresolved architecture to planning merely to keep the workflow moving.
