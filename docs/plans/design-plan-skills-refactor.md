# Planning and Design Skills Refactor

## Overview

**This initiative will replace the archived planning and design skills with portable, human-centered workflows.** The
original idea is to make agents useful thinking partners from the first vague concept through an implementation-ready
plan. The workflows should help the user discover possibilities, preserve the original intent, make sound decisions,
and produce documents a person can follow.

**The purpose is better reasoning and communication rather than more documentation machinery.** The skills should guide
brainstorming, technical design, implementation planning, critical review, and optional visualization without forcing
every task through one rigid process or document template.

**The intended workflow keeps brainstorming, designing, and planning conceptually distinct.** Brainstorming ends with an
explicitly incomplete draft. Designing refines the solution. Planning turns a sufficiently stable design into ordered,
verifiable work. Later discoveries may return to an earlier activity when they change its decisions.

Success means the resulting skill set:

- presents useful branches and new ideas while an initial concept is still vague;
- keeps purpose and intent visible as detailed documents develop;
- supports both overview-level and detailed artifacts with clear reading paths;
- separates authoring from adversarial review;
- offers portable, optional visual plans without making a renderer the source of truth; and
- remains small and adaptable enough that agents follow it in real conversations.

## Status and Authority

**This is the overview-level plan for the refactor.** It owns the initiative's purpose, activity boundaries, document
altitudes, proposed skill architecture, workstream order, and companion-document map. Detailed companion documents own
their individual workflows and contracts. The research companion owns evidence and source analysis.

The framework remains under design. Accepted decisions are dated below. Proposals remain open until the user accepts
them or behavioral evidence settles them.

## Why the Existing Skills Are Being Replaced

**`design-forge` solves corpus governance rather than design reasoning or design writing.** Adding authoring guidance to
its existing lifecycle, ownership, locking, migration, requirements, and domain machinery would expand an already broad
job. Its useful governance mechanisms should become optional and separate.

**`idea-forge` produces useful results through a clunky interaction.** Its phase gates, fixed verdict vocabulary,
candidate limits, and repeated confirmations did not survive its recorded real session. The replacement should use
obra's Superpowers dialogue as its base while retaining early branch generation and selected diagnostic questions from
the local skill.

The evidence and complete comparisons are in
[`design-plan-skills-research.md`](design-plan-skills-research.md).

## Proposed Skill Architecture

**The replacement uses coherent jobs with explicit handoffs.** The user accepted separate technical-design and
implementation-planning skills on 2026-09-04; their activity boundaries remain stable during evaluation.

| Job                        | Input                                     | Outcome                                                                                      | Current direction                                          |
| -------------------------- | ----------------------------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| Brainstorming and ideation | An unformed idea or opportunity           | An explicitly incomplete design/plan draft with a promising direction and unresolved choices | `brainstorming`; ready for candidate authoring             |
| Technical design           | A bounded problem or brainstorming draft  | An explained, reviewable solution with behavior, boundaries, flows, and failure handling     | Separate portable `technical-design` skill accepted        |
| Implementation planning    | An accepted or sufficiently stable design | Dependency-ordered work with adjacent verification                                           | Separate portable `implementation-planning` skill accepted |
| Adversarial review         | A design or plan draft                    | Consequence-ranked findings with tiered repairs                                              | Separate critic skill with design and plan lenses          |
| Visualization              | An existing design or plan                | A portable visual companion that improves comprehension                                      | Separate optional skill; Markdown plus self-contained HTML |
| Requirements engineering   | Stakeholder needs or external obligations | Clear, testable requirements at the correct altitude                                         | Separate specialized skill; deferred                       |
| Document maintenance       | Existing authoritative documents          | Optional lifecycle, ownership, navigation, migration, and supersession                       | Separate governance skill or guidance; deferred            |

## Accepted Framework Decisions

### Brainstorming Skill Identity

**Accepted 2026-09-03 and completed 2026-09-04: the replacement skill is named `brainstorming`.** It is portable,
agent-agnostic, and sourced from `skills/shared/design/brainstorming/` under the repository's existing placement rules.
It replaced archived `idea-forge` after behavioral evaluation and independent review.

### Activity Boundaries

**Accepted 2026-09-03: brainstorming, designing, and planning are distinct activities.** They answer different questions,
have different stopping conditions, and fail in different ways.

| Activity                   | Central question                                                     | Output                                     | Ready to advance when                                                                                                     |
| -------------------------- | -------------------------------------------------------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| Brainstorming and ideation | What could this become, and what outcome is wanted?                  | An explicitly incomplete design/plan draft | The intended outcome, promising direction, scope, constraints, and open questions are legible                             |
| Designing                  | How should the system behave and fit together?                       | A coherent, reviewable design              | Behavior, boundaries, interfaces, flows, failure handling, and consequential tradeoffs are stable enough to sequence work |
| Planning                   | What work should happen, in what order, and what evidence proves it? | An implementation-ready plan               | Work units, dependencies, affected surfaces, and verification are actionable                                              |

**Accepted 2026-09-03 and extended 2026-09-04: designing and planning remain conceptually and operationally separate.**
They deploy as separate skills with an explicit shared-understanding handoff. Their artifacts and completion criteria
remain separate.

### Refinement Ownership

**Brainstorming owns fidelity refinement, designing owns solution refinement, and planning owns execution refinement.**
Intent or scope changes return to brainstorming. Behavior, architecture, interface, or failure-handling gaps return to
designing. Sequencing, dependency, touchpoint, or verification changes stay in planning.

### Minimum Brainstorming Draft

**Accepted 2026-09-03: brainstorming-draft readiness is outcome-based rather than heading-based.** The draft records the
original idea, purpose, intent, desired outcome, branches and current direction, scope, exclusions, parked ideas,
consequential constraints and assumptions, one observable success signal, bounded design questions, and the status of
decisions and recommendations. It records consequential prohibited outcomes when they define success.

Actors, prior art, detailed measurements, and rejected alternatives remain conditional. The draft is ready when a
designer can continue without reconstructing the conversation or inventing purpose, scope, or evidence of success.
Unresolved technical decisions are expected.

### Brainstorming Draft Persistence

**Accepted 2026-09-03: conversation is the working surface, and drafts advancing to technical design are written at
handoff.** The agent writes a draft immediately when the user asks to save it, regardless of whether brainstorming is
complete. An on-demand save does not imply readiness.

When an unsaved draft is at risk because context usage is filling up, the agent recommends saving and explains the
continuity risk. Chat-only completion remains available for explicitly ephemeral or abandoned ideas. The workflow avoids
rewriting the artifact after every exchange.

### Brainstorming Confirmation

**Accepted 2026-09-03: brainstorming uses one handoff-fidelity gate rather than phase-by-phase approval.** Explicit
confirmation is required before changing established purpose, intent, outcome, or scope; selecting an unchosen
consequential product branch; accepting material cost, risk, compatibility loss, or irreversibility; and handing the
draft to technical design.

The handoff question confirms that the draft captures what the user wants to refine. It does not declare the draft
complete or authorize implementation. Facts, labeled recommendations, reversible provisional assumptions, parked
tangents, requested saves, and choices already clear from the user's response need no duplicate confirmation.

### Brainstorming Draft Location and Name

**Accepted 2026-09-03: draft placement follows user direction, an existing draft, a companion map, or repository
convention in that order.** One clear existing convention may resolve the path without another approval question. When
no convention exists, the agent proposes `docs/plans/<name>-draft.md` and asks once. Outside a repository, it asks for a
destination.

The fallback filename uses two or three descriptive words in kebab-case followed by `-draft.md`, such as
`auth-flow-draft.md`. Competing conventions, a new directory, or an unrelated file collision require user direction.

### Useful Widening Evaluation

**Accepted 2026-09-03: useful widening is evaluated through vague, composable, ambiguous, already narrow, and tangential
cases.** Successful branches serve the stated purpose, differ on a consequential dimension, explain what changes and
costs, identify whether they conflict or compose, and introduce a useful new direction when the idea permits one. The
response should avoid premature architecture, generic option padding, and questions that do not narrow live branches.

### Document Altitude

**Accepted 2026-09-03: overview and detailed are distinct document altitudes.** Altitude is independent of activity and
artifact type.

| Altitude | Reader need                                    | Typical content                                                                                                            |
| -------- | ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Overview | Understand the whole initiative and its intent | Original idea, purpose, desired outcome, boundaries, major decisions, broad sequence, risks, and detailed-document map     |
| Detailed | Build or review one bounded part               | Precise behavior, responsibilities, interfaces, flows, edge cases, failure handling, implementation work, and verification |

Every overview-level plan, design, or draft should carry an `## Overview` section or the repository's established
equivalent near its beginning. That section owns the original idea, purpose, intent, desired outcome, audience, and
success conditions that must survive refinement.

A detailed document should link to its governing overview near the beginning and state how its bounded subject advances
that purpose. Agents should reread the overview before material detailed work. Adversarial review should flag locally
attractive decisions that weaken the governing intent.

### Portable Visualization

**Accepted 2026-09-03: canonical Markdown owns the plan and generated self-contained HTML provides the browser view.**

```text
<plan>.md                 canonical design or plan
<plan>.visual.html        generated visual companion
```

The HTML should work offline, use semantic HTML and CSS with inline SVG, embed its assets, remain responsive and
printable, and avoid JavaScript unless interaction provides material value. It should record the source path and content
digest, identify itself as generated, and direct edits back to Markdown. MDX and service-backed renderers may exist as
optional adapters but cannot become the only recoverable form.

## Workstreams

### Brainstorming and Ideation

**The first detailed workstream replaces `idea-forge` using obra's Superpowers interaction model.** A vague seed receives
a few useful branches, options, or adjacent ideas before narrowing. The agent asks one consequential question at a time,
recommends with reasons, researches decision-changing facts, parks tangents, and challenges promising directions
proportionately.

The output is an explicitly incomplete design/plan draft. Technical design should be able to continue without
reconstructing the conversation or inventing the user's purpose. The shipped workflow, draft contract, provenance, and
evaluation cases are in
agent-setup's `docs/plans/archived/brainstorming-skill-design.md`.

### Technical Design and Implementation Planning

**Designing and planning have separate internal contracts and deploy as separate skills.** Designing should
investigate the current architecture, resolve consequential choices, explain the chosen shape, and define behavior,
boundaries, interfaces, flows, failure handling, and operational consequences. Planning should cite that design and
produce independently verifiable work units with dependencies, affected surfaces, behavioral outcomes, and adjacent
verification.

The Superpowers `writing-plans` skill and its plan corpus have now been reviewed. The shipped contracts, artifact
boundaries, return paths, and package-shape evaluation are in
agent-setup's `docs/plans/archived/technical-design-planning-skill-design.md`.

### Adversarial Review

**Plan authoring should have a separate adversarial counterpart.** The author constructs a route to the outcome; the
critic tries to falsify it before execution makes gaps expensive. A lightweight author self-review should catch internal
consistency and completeness, while the critic independently examines intent alignment, assumptions, dependencies,
missing work, interface gaps, failure behavior, integration, migration, rollback, verification, and completion.

Findings should state evidence, consequence, the smallest sufficient repair, the recommended repair, and proof that the
repair worked. Severity should distinguish blockers, major gaps, minor weaknesses, and advisory improvements. When
useful, repairs may distinguish minimum safe, recommended, and stronger options. The critic should avoid manufactured
objections and should not edit the reviewed artifact without authorization.

### Human-Readable Documents

**Design and plan documents need a shared reading spine rather than a universal template.** Sections remain conditional,
and formatting follows the information.

1. **Front door:** title, status, altitude, intended readers, governing overview, and local scope.
2. **Overview:** original idea, purpose, intent, desired outcome, and success conditions for an overview artifact. A
   detailed artifact links to this material and states its local contribution.
3. **Reasoning body:** relevant current state and constraints, followed by decisions, rationale, proposed shape, and
   material alternatives.
4. **Action body:** implementation units and verification when the artifact is a plan. A pure design omits it.
5. **Exit:** unresolved questions, known risks, deferred work, readiness, and observable completion criteria.

Long artifacts should provide progressive disclosure. Writers should split when readers, responsibilities, lifecycles,
independently decidable topics, or implementation workstreams differ. The root retains the outcome, system shape,
decision summary, reading order, and focused links. A collection of heavily cross-referenced fragments is another form
of an unreadable monolith.

### Plan Visualization

**Visualization is an optional companion that tests comprehension.** It should choose a visual according to the question:
architecture or relationship diagrams for component structure, sequence or flow diagrams for movement, state diagrams
for behavioral transitions, dependency graphs for implementation order, and wireframes or prototypes for user
interfaces. Textual decisions do not require decorative visuals.

Visuals should sit beside the decision they clarify and avoid duplicating the plan. Product screens show the user
experience; architecture, implementation, and data-flow annotations remain outside them. The generator should verify
labels, contrast, clipping, overlap, rendering, and agreement with the canonical Markdown.

### Requirements and Document Governance

**Requirements engineering and corpus governance remain separate deferred jobs.** Atomic requirement schemas and system
or hardware vocabulary belong to specialized requirements guidance. Lifecycle, ownership, generated indexes,
supersession, migration, and restricted-content labels belong to optional governance. Byte-identical relocation is
useful only where a migration requires lossless proof. Ordinary design evolution should prefer current truth and version
control history.

## Sequence

**The refactor should deliver one vertical slice before expanding the suite.**

Steps 1 through 5 completed on 2026-09-04. Step 6 designs and evaluates the adversarial critic.

1. Write an initial portable brainstorming-skill candidate and its behavioral fixtures from the accepted detailed design.
2. Compare the candidate with no skill, archived `idea-forge`, and the Superpowers baseline.
3. Revise from observed behavior, then validate, review, and deploy the settled brainstorming skill.
4. Review the deferred planning sources and design the technical-design and implementation-planning contracts.
5. Author and behaviorally evaluate the separate `technical-design` and `implementation-planning` skills.
6. Design and evaluate the adversarial critic against stable design and plan artifacts.
7. Build the portable visual-plan companion against stable Markdown artifacts.
8. Revisit requirements engineering and document governance only with evidence that their separate jobs are needed.

Later steps must not block useful earlier work. Discoveries that invalidate an accepted framework decision return to the
overview for a user decision before dependent work continues.

## Companion Documents

| Document                                                                      | Altitude and role                                | Status                                                   |
| ----------------------------------------------------------------------------- | ------------------------------------------------ | -------------------------------------------------------- |
| agent-setup's `docs/plans/archived/brainstorming-skill-design.md`             | Detailed design for the first skill              | Shipped and archived 2026-09-04                          |
| [`design-plan-skills-research.md`](design-plan-skills-research.md)            | Detailed evidence and source record              | Active reference; planning sources reviewed 2026-09-04   |
| [`design-skills-intent-refresh.md`](design-skills-intent-refresh.md)          | Outcome, evidence, and risk refinements          | Review lite passed; behavioral evaluation pending        |
| agent-setup's `docs/plans/archived/technical-design-planning-skill-design.md` | Detailed technical-design and planning contracts | Shipped and archived 2026-09-04                          |
| Plan-critic design                                                            | Detailed adversarial-review design               | Deferred; create when producer artifacts stabilize       |
| Visual-plan design                                                            | Detailed portable-renderer design                | Deferred; create when canonical plan artifacts stabilize |
| Requirements-engineering design                                               | Detailed specialized requirements workflow       | Deferred                                                 |
| Document-governance design                                                    | Detailed lifecycle and maintenance workflow      | Deferred pending evidence of need                        |

## Deferred Agent and Subagent Definitions

**Portable agent definitions are a later layer over the skill framework.** After repository consolidation is more
complete, the user intends to add universal agent and subagent definitions adapted across supported harnesses. The
intended split is one agent for brainstorming and another for planning and designing, plus an independent plan critic.
The user's current global Claude configuration contains a `plan-critic` subagent that provides prior experience.

This overview does not define those agents' prompts, tools, model choices, delegation behavior, context contracts, review
independence, or handoff protocol. Skill responsibilities and artifact boundaries should settle first.

## Risks and Controls

### Recreating the Same State Machine

Detailed workflows can accumulate gates, modes, identifiers, and checklists until agents stop following them. Each
instruction should earn its context and interaction cost through behavioral evidence. Risk-sensitive actions may require
exact gates; ordinary judgment should retain flexibility.

### Fragmentation

Splitting every concern immediately would reproduce the navigation problem this refactor is meant to solve. The overview
keeps inactive workstreams concise. A detailed companion appears when its workstream becomes active and has enough
content to justify independent reading.

### Goal Drift

Detailed work can optimize a local mechanism while losing the initiative's purpose. Every detailed artifact links to the
overview and states its contribution. Review compares local decisions against the overview's intent and success
conditions.

### Attractive but Unsupported Structure

Static analysis can make a framework look convincing without proving that agents follow it. Behavioral evaluation must
compare outcomes, interaction cost, unnecessary questions, tool use, and traces across representative requests and
relevant model classes.

### External Runtime Coupling

External skills contain useful principles embedded in proprietary services, custom renderers, and large runtime
protocols. The portable core should retain only the behavior needed for its job. Optional adapters should degrade to
open, locally recoverable artifacts.

## Behavioral Evaluation Direction

**Evaluation should test behavior and reader outcomes rather than exact prose or headings.** Comparisons should use the
same request and environment with no skill, the previous local skill, relevant external baselines, and the proposed
replacement when the added-value question matters.

The suite should cover useful branch generation, avoidance of ceremonial alternatives, scope decomposition, draft
handoffs, backward refinement loops, design coherence, implementation sequencing, critic precision, goal-drift
detection, human-scale navigation, useful visualization, graceful visual omission, and source-to-visual agreement.

Each case should record the request, behavior under test, observable success conditions, consequential failure paths,
agent, model, client, environment, baseline, raw output, trace, and result. Human judgment should assess irreducibly
qualitative readability and usefulness. Mechanical assertions should cover paths, metadata, links, and generated
artifacts.

## Open Decisions

1. Should one critic skill contain design and plan lenses, or do those reviews need separate skills?
2. Do severity and repair tiers improve decisions enough to justify their review ceremony?
3. Which optional interactive visualization adapters justify their runtime and maintenance cost?
4. Which soft size signals should trigger navigation or a split without becoming rigid line-count gates?
5. Which governance mechanisms solve observed problems outside the knowledge-vault corpus?

## Source Review Status

The research record owns source analysis and provenance. It now covers Superpowers `writing-plans` and its complete plan
corpus at the pinned revision, Addy Osmani's planning and task-breakdown skill, and the completed Stellarlink
requirements-agent review. The adjacent `grilling`, `writing-documentation`, `writing-for-humans`, and `test-engineer` skill
reviews are also complete. No deferred source review blocks the technical-design and implementation-planning contracts.
