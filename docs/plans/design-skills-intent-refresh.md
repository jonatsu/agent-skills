# Design Skills Intent Refresh

## Status

**Candidate implemented and review lite completed 2026-09-04; full behavioral evaluation remains pending.** The user
authorized implementation after `skill-forge` finished and review after `skill-review` settled.

This plan is the complete implementation authority for the deferred work. The implementation agent should need no
conversation history or fresh source mining. External sources remain evidence and provenance records, not live workflow
dependencies.

## Objective

Strengthen `brainstorming`, `technical-design`, and `implementation-planning` with clearer intent, evidence, and risk
handling. Preserve the accepted boundary between product exploration, system design, and implementation sequencing.

The completed changes must provide these outcomes:

- brainstorming narrows activity statements into observable outcomes before design handoff;
- brainstorming records one useful success signal without inventing quantitative precision;
- repository evidence remains distinct from desired product or business policy;
- negative guarantees remain visible from product intent through implementation evidence;
- design and planning depth scales with relevant uncertainty, consequence, and verification risk; and
- no new requirements-engineering workflow appears inside the three existing skills.

## Execution Constraint

Do not begin this plan while the work in
[`skill-forge-and-skill-review-refresh.md`](skill-forge-and-skill-review-refresh.md) remains active. That work currently
changes shared authoring and review behavior, evaluation conventions, and provenance guidance.

At implementation time, use this file as the design and planning authority. Inspect the target files for current state
and conflicts, but do not reopen the accepted product decision without contrary evidence. If the completed refresh
changes a repository command or mechanical package rule, follow the new rule and record the adjustment. Return only a
conflicting workflow boundary or changed outcome to the user.

The implementation must not invoke `intent-driven-development` or `define-goal` as a workflow. Their retained concepts
are independently expressed below. Do not install either source package.

## Current Execution Record

The implementation candidate includes all nine planned cases, the three skill changes, provenance updates, and current
framework documentation. Author-side mechanical validation produced these results:

- `jq empty`, required-case presence, and case-ID uniqueness passed for all three behavior files;
- both skill validators passed for `brainstorming`, `technical-design`, and `implementation-planning`;
- every applicable pre-commit hook passed for each changed file; and
- `just check` passed through every gate except the Kasetto lock audit.

An earlier lock audit reported the three changed design skills and the concurrently edited `skill-review`. The review
work has since settled, which removes that isolation blocker. Synchronization may follow the candidate source commit.

Review lite found no material defect and assigned `ready with risks`. No model-based baseline or candidate run has run.
The verdict permits provisional use but does not establish behavioral effectiveness across clients or models.

## Accepted Decisions

01. **Improve the existing three skills.** Do not add an `intent-driven-development`, `acceptance-criteria`, or
    requirements-engineering skill in this change.
02. **Keep requirements engineering deferred.** Revisit it only after real requests show an independent job such as PRD
    review, contractual requirements, compliance obligations, or stakeholder acceptance handoffs.
03. **Test behavior before changing skill prose.** Add the accepted regression cases first, then run a baseline where the
    available evaluation procedure permits one.
04. **Require an observable success signal at brainstorming handoff.** Detailed measurements remain conditional. A
    qualitative outcome must not receive fabricated precision.
05. **Keep authority explicit.** Code and tests establish current technical behavior. They do not establish desired
    users, priorities, policies, service levels, retention rules, or compliance duties.
06. **Carry negative guarantees across the workflow.** Brainstorming owns product harms and exclusions. Technical design
    owns system invariants and prohibited behavior. Planning owns implementation evidence for accepted guarantees.
07. **Scale depth without named modes or fixed templates.** Risk and uncertainty determine detail. Do not introduce
    “Quick Capture,” “Full Acceptance Brief,” or fixed criterion counts.
08. **Preserve artifact authority.** Technical design owns behavior and guarantees. Implementation planning owns the
    verification route, environment, and execution order.
09. **Recover outcomes from proposed solutions.** When a seed embeds a mechanism before its purpose, preserve the
    mechanism as a branch and establish the actor and desired outcome before narrowing.
10. **Prioritize assumptions by consequence.** Keep a direction provisional when an unresolved assumption could
    invalidate it. Seek the smallest evidence that could change the decision before design handoff.

## Non-Goals

- Add acceptance-criterion identifiers, revision logs, priorities, or a universal acceptance template.
- Require measurements for every qualitative product outcome.
- Add goal-tool state management or long-running execution controls.
- Let brainstorming define architecture, interfaces, detailed failure behavior, or verification plans.
- Let technical design prescribe test files, commands, implementation order, or task ownership.
- Let implementation planning revise accepted product intent or system behavior silently.
- Create a parallel specification artifact for every small change.
- Require named ideation frameworks, fixed question or idea counts, scoring matrices, or an MVP template.
- Copy source prose, examples, templates, schemas, or workflows.
- Edit the archived brainstorming or design-and-planning design records as current-state documentation.

## Source Evidence and Provenance

### OpenAI `define-goal`

- Project: [OpenAI Skills](https://github.com/openai/skills)
- Source:
  [`skills/.curated/define-goal/SKILL.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/define-goal/SKILL.md)
- Source revision: `49f948faa9258a0c61caceaf225e179651397431`, inspected 2026-09-04
- License:
  [Apache-2.0](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/define-goal/LICENSE.txt)
- Relationship: idea-level influence with independent expression

Retain these concepts:

- distinguish a completed outcome from an activity such as “improve,” “investigate,” or “make progress”;
- state the affected artifact, system, environment, actor, or visible behavior when it clarifies the outcome;
- pair the outcome with evidence that would honestly demonstrate success;
- make scope and exclusions explicit when ambiguity matters; and
- quantify only when the metric represents real success.

Do not retain goal creation, active-goal state, token budgets, execution stop conditions, or tool-specific procedures.
Those concerns belong to goal execution rather than product brainstorming.

### ECC `intent-driven-development`

- Author: Affaan Mustafa
- Project: [Everything Claude Code](https://github.com/affaan-m/ECC)
- Source:
  [`skills/intent-driven-development/SKILL.md`](https://github.com/affaan-m/ECC/blob/e04ea0b9cc8248686edf5ac751cadff550e162b8/skills/intent-driven-development/SKILL.md)
- Source revision: `e04ea0b9cc8248686edf5ac751cadff550e162b8`, inspected 2026-09-04
- License: [MIT](https://github.com/affaan-m/ECC/blob/e04ea0b9cc8248686edf5ac751cadff550e162b8/LICENSE)
- Relationship: idea-level influence with independent expression

Retain these concepts:

- separate current technical facts from user intent and authoritative product policy;
- scale detail with applicable security, data, migration, compatibility, integration, cost, and usability risks;
- state prohibited side effects when they define correctness;
- select verification methods that fit the claim and the operational risk;
- name a safe environment when verification could affect data, services, secrets, or cost; and
- allow several checks to support one obligation or one check to support several obligations.

Do not retain its broad activation surface, acceptance-brief template, criterion identifiers, revision protocol, fixed
criterion count, priority vocabulary, implementation continuation, or generic risk table. Those mechanisms would merge
requirements, design, planning, and execution.

### Addy Osmani `idea-refine`

- Author: Addy Osmani
- Project: [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
- Source package:
  [`skills/idea-refine/`](https://github.com/addyosmani/agent-skills/tree/1c760d643497e9da289300e5eb2f5aca861503f7/skills/idea-refine)
- Source revision: `1c760d643497e9da289300e5eb2f5aca861503f7`, inspected 2026-09-04
- License:
  [MIT](https://github.com/addyosmani/agent-skills/blob/1c760d643497e9da289300e5eb2f5aca861503f7/LICENSE)
- Relationship: idea-level influence with independent expression

Retain these concepts:

- recover the affected actor and desired outcome when a seed starts from a proposed solution;
- preserve the proposed solution as a live branch unless the user already made it a constraint;
- distinguish assumptions by their consequence for the selected direction; and
- seek the smallest decision-changing evidence for an assumption that could invalidate that direction.

Do not retain named framing formulas, fixed phases, question counts, idea counts, framework catalogues, scoring matrices,
MVP rules, artifact templates, mandatory save paths, scripts, stress-test routing, or tone instructions.

### Licensing Treatment

Keep each target skill's current MIT license and existing upstream license files. Record idea-level influence in each
affected `ATTRIBUTIONS.md`. State that the new prose is independently expressed. Do not copy source wording.

If implementation instead copies or closely adapts Apache-2.0 expression, stop and reassess the package license,
notices, modification statement, and distribution obligations. This plan does not authorize that change.

## Affected Surfaces

| Surface                                                            | Responsibility                                                                 |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| `skills/shared/design/brainstorming/evals/behavior.json`           | Goal quality, qualitative outcomes, negative outcomes, and anti-ceremony cases |
| `skills/shared/design/technical-design/evals/behavior.json`        | Authority boundary and negative-guarantee design behavior                      |
| `skills/shared/design/implementation-planning/evals/behavior.json` | Negative evidence, verification cardinality, and safe environments             |
| `skills/shared/design/brainstorming/SKILL.md`                      | Outcome quality and handoff readiness                                          |
| `skills/shared/design/technical-design/SKILL.md`                   | Fact authority, proportional depth, and system guarantees                      |
| `skills/shared/design/implementation-planning/SKILL.md`            | Evidence mapping and verification safety                                       |
| Three `ATTRIBUTIONS.md` files                                      | Pinned source provenance for retained ideas                                    |
| `docs/plans/design-plan-skills-research.md`                        | Detailed source comparison and rejected mechanisms                             |
| `docs/plans/design-plan-skills-refactor.md`                        | Current framework decisions and companion-plan link                            |

Do not change descriptions or skill names. The jobs and activation boundaries remain unchanged. Do not create scripts,
references, templates, or fixtures unless a behavioral case needs a repository fixture that inline context cannot
represent reliably.

## Implementation Sequence

### 1. Establish Behavioral Cases Before Prose Changes

Add all accepted cases before editing any `SKILL.md`. Preserve the existing JSON schema and naming style. Keep prompts
independent from the proposed wording, so they test outcomes rather than phrase matching.

#### Brainstorming: Activity Goal Repair

Add `activity-goal-repair` to `brainstorming/evals/behavior.json`.

Suggested prompt:

> We have decided to focus on first-time setup, but the goal is still “improve onboarding.” Prepare this direction for
> technical design without inventing implementation details.

Required outcomes:

- identifies “improve onboarding” as an activity or aspiration rather than a verifiable outcome;
- proposes or elicits an observable user or system result before handoff;
- preserves the established first-time setup scope;
- avoids architecture, implementation tasks, and arbitrary numerical targets; and
- leaves a consequential product choice with the user when context cannot settle it.

#### Brainstorming: Qualitative Success Without Decorative Precision

Add `qualitative-success-signal`.

Suggested prompt:

> Help shape a small peer-support ritual whose purpose is to make new maintainers feel safe asking basic questions. We
> do not have enough participants for meaningful statistical targets.

Required outcomes:

- records an observable qualitative success signal suitable for review or user confirmation;
- does not invent percentages, sample sizes, survey thresholds, deadlines, or adoption targets;
- distinguishes the desired human outcome from a proposed mechanism; and
- keeps detailed measurement design conditional.

#### Brainstorming: Critical Prohibited Outcome

Add `product-level-must-not`.

Suggested prompt:

> Shape a dashboard export feature. Administrators need the filtered records, and the export must never expose another
> tenant's data. Leave technical authorization design for the next phase.

Required outcomes:

- records cross-tenant disclosure as a consequential prohibited outcome;
- keeps the guarantee visible in the design handoff;
- does not invent authorization architecture or test procedures; and
- distinguishes the required product guarantee from a technical recommendation.

#### Brainstorming: Reject Acceptance-Brief Ceremony

Add `no-premature-acceptance-brief`.

Suggested prompt:

> I have an early idea for helping households coordinate emergency supplies. Brainstorm what it could become and write
> all acceptance criteria with IDs, priorities, verification methods, and a revision log.

Required outcomes:

- performs useful widening and narrowing at brainstorming altitude;
- records the requested outcome, scope, constraints, and useful success signals when known;
- declines or defers architecture-dependent acceptance detail;
- does not create a fixed acceptance-brief template merely because the prompt requests one; and
- explains that detailed requirements or design evidence needs a later, appropriately scoped activity.

#### Brainstorming: Solution-Anchored Seed

Add `solution-anchored-seed`.

Suggested prompt:

> I want to brainstorm an AI chatbot that handles customer support questions. We have not decided which support outcome
> matters most.

Required outcomes:

- distinguishes the proposed chatbot from the unresolved customer or support outcome;
- surfaces relevant outcome framings before treating the chatbot as the selected direction;
- keeps the chatbot visible as a possible branch rather than silently discarding it;
- asks exactly one question that resolves the consequential outcome choice; and
- avoids chatbot architecture and implementation tasks.

#### Brainstorming: Direction-Critical Assumption

Add `direction-critical-assumption`.

Suggested prompt:

> We chose volunteer pickup for the neighbourhood tool library, but we have no evidence that anyone will volunteer
> reliably. Prepare the brainstorm for technical design.

Required outcomes:

- identifies reliable volunteer participation as an assumption whose failure could invalidate the direction;
- distinguishes that critical assumption from uncertainties that can safely wait;
- keeps the direction provisional instead of handing it to technical design as settled;
- names the smallest evidence that could resolve the assumption before handoff; and
- avoids MVP architecture and implementation planning.

#### Technical Design: Current Behavior Is Not Desired Policy

Add `current-code-not-product-policy` to `technical-design/evals/behavior.json`.

The case should use either a small fixture or supplied repository evidence. The current code should cap free accounts at
100 exports each month. No authoritative product artifact should state that policy.

Suggested prompt:

> Design the export quota behavior. The repository currently limits free accounts to 100 exports each month. Treat the
> code as evidence and determine what still needs product authority.

Required outcomes:

- records the limit as verified current behavior when inspection supports it;
- does not present the limit as desired pricing, entitlement, or contractual policy;
- labels the intended quota as a product decision or provisional assumption;
- continues only design work that does not depend on the unresolved policy; and
- returns an outcome or scope change to brainstorming when the answer changes product intent.

#### Technical Design: Negative Guarantee Ownership

Add `negative-guarantee-design`.

Required outcomes:

- turns an accepted “must not” product outcome into explicit system invariants and boundary behavior;
- covers relevant success, denial, failure, and disclosure paths;
- keeps verification commands and implementation order out of the design; and
- hands the settled guarantee to planning as a design obligation.

#### Implementation Planning: Negative Evidence and Safe Verification

Add `negative-guarantee-verification` to `implementation-planning/evals/behavior.json`.

Use an accepted design that prohibits cross-tenant export disclosure. Include a real integration environment and a
production environment that the agent lacks authority to probe.

Required outcomes:

- traces the negative guarantee to one or more implementation units;
- requires behavioral evidence for allowed and denied tenant combinations;
- names the isolated integration environment and synthetic data requirements;
- does not authorize production probes or real sensitive data;
- permits one integration check to support several related obligations; and
- does not force one test per criterion or one criterion per test.

**Verification:** run `jq empty` on each changed behavior file. Run the repository's supported candidate procedure for
the new cases before prose edits where practical. Record unsupported clients, unavailable runners, contamination, and
harness failures separately from candidate behavior. A static case definition alone does not prove behavior.

### 2. Refine `brainstorming`

Edit only the existing `Work Conversationally` and `Draft and Handoff` responsibilities. Keep the current widening,
one-question, user-control, persistence, path-resolution, and fidelity-confirmation rules.

Add these independently expressed rules after the direction starts to narrow:

- test whether the stated goal describes a completed outcome or only an activity;
- sharpen an activity from available context when that choice is reversible and well supported;
- ask one consequential question when the missing outcome would change product direction;
- identify at least one observable success signal before technical-design handoff;
- prefer a binary observation or human-review judgment when honest measurement is unavailable; and
- quantify only when the metric, method, and threshold represent genuine success.

Add these rules for framing and assumption handling:

- when a seed proposes a solution before its purpose, surface the affected actor and desired outcome first;
- preserve that solution as a live branch unless the user already made it a constraint or decision;
- treat a changed framing as a recommendation until the user confirms it;
- order assumptions by whether their failure would invalidate the direction, change it, or safely wait; and
- seek the smallest decision-changing evidence for the most consequential unresolved assumption.

Keep an affected direction provisional until evidence settles its critical assumption or the user accepts the risk.
Do not require a named framing formula, formal assumption taxonomy, MVP, or validation plan.

Add this authority boundary near the existing research rule:

> Repository evidence establishes current technical behavior and constraints. It does not establish desired product or
> business policy. Treat unsupported target users, priorities, entitlements, service levels, retention rules, and
> compliance duties as user-supplied constraints or provisional assumptions.

The exact final wording may change for cohesion, but it must preserve that distinction.

Extend the draft contract so every design handoff records one observable success signal. Record consequential prohibited
outcomes when they define the desired result. Keep detailed measures, prior art, and rejected alternatives conditional.

Update readiness so a handoff requires a legible outcome, direction, scope, constraints, success signal, and bounded
open questions. Do not require a metric, acceptance-criterion set, or formal specification.

**Verification:** run the six new brainstorming cases and the existing `vague-single-outcome`, `ambiguous-seed`,
`handoff-fidelity`, and `backward-refinement` cases. Confirm no regression in one-question behavior, incomplete handoff
altitude, or user authority.

### 3. Refine `technical-design`

Keep the current entry boundary, repository investigation, alternative analysis, system definition, artifact authority,
and final confirmation.

Add the current-behavior authority rule under `Investigate Before Deciding`. The rule should state:

- implementation and tests establish current technical facts;
- an authoritative product artifact may establish intended policy within its scope;
- code names and current limits do not establish target users, priorities, pricing, retention, compliance, or desired
  service levels; and
- unsupported product rules remain assumptions or return to brainstorming for a decision.

Extend `Define the System` with explicit invariants and prohibited behavior. The design should translate accepted
product-level harms into system boundaries, denial behavior, information-disclosure limits, and recovery obligations.
Planning still owns the verification command and execution sequence.

Add proportional depth without a named mode. A bounded low-risk change may stay compact. Security, authorization,
persistent data, migrations, compatibility, external dependencies, cost, or difficult recovery require corresponding
design depth when applicable. Do not add a generic risk table or require irrelevant sections.

Extend the handoff check to confirm that consequential invariants and prohibited behavior are settled. Keep
implementation-local verification details outside that check.

**Verification:** run `current-code-not-product-policy`, `negative-guarantee-design`, and the existing
`01-bounded-design`, `03-repository-grounded-design`, `04-consequential-choice`, and `05-return-to-brainstorming` cases.
The results must not add task order or silently decide product policy.

### 4. Refine `implementation-planning`

Keep the accepted-design gate, dependency mapping, independently verifiable work units, exact inspected surfaces, and
claim-matched verification.

Extend `Specify Each Work Unit` so verification covers accepted negative guarantees when relevant. Do not add a
separate mandatory field when the existing verification or design-obligations text remains clear.

Add these rules under `Match Verification to the Claim`:

- one obligation may require several checks across different boundaries;
- one check may support several obligations when the evidence genuinely overlaps;
- do not force a one-to-one mapping between tests and acceptance conditions;
- name the environment and safe data when verification can mutate state, contact services, expose secrets, or incur
  cost; and
- report unavailable safe evidence rather than substituting an unauthorized live check.

Preserve the rule that behavioral claims need behavioral evidence. Static checks may still prove separate structural
claims. Do not turn planning into a test-only strategy or requirements workflow.

**Verification:** run `negative-guarantee-verification` plus existing cases `06-accepted-design`,
`10-compatible-migration`, and `12-verification-theater`. Confirm that verification remains adjacent to the work and
that no production authority is inferred.

### 5. Record Provenance and Framework Decisions

Update each affected `ATTRIBUTIONS.md` only for concepts retained in that skill:

- `brainstorming`: add OpenAI `define-goal` for outcome quality and honest quantification. Add ECC for the technical-fact
  and product-policy boundary plus product-level prohibited outcomes. Add Addy Osmani's `idea-refine` for
  solution-anchored reframing and consequence-ranked assumptions.
- `technical-design`: add ECC for the authority boundary, proportional risk depth, and explicit negative guarantees.
- `implementation-planning`: add ECC for safe verification environments, prohibited-side-effect evidence, and
  non-bijective mapping between obligations and checks.

Each entry must use the pinned revision and license recorded above. State idea-level influence and independent
expression. Do not alter the existing relationship to Superpowers or Addy Osmani.

Add both source assessments to `docs/plans/design-plan-skills-research.md`. Record retained concepts, rejected
mechanisms, source revision, inspection date, license, and workflow-boundary consequences. Avoid repeating the entire
implementation plan there.

Update `docs/plans/design-plan-skills-refactor.md` in two places:

1. Extend the minimum brainstorming draft with an observable success signal and consequential prohibited outcomes.
2. Add this plan to the companion-document table as the accepted, deferred implementation authority.

Do not edit archived design records. They describe the shipped 2026-09-04 baseline and remain historical evidence.

**Verification:** inspect every source link at its pinned revision. Confirm every retained idea has one provenance
record and every current framework statement agrees with the changed skill contracts.

### 6. Validate the Three Skill Changes

Validate each independently before the combined repository check:

```bash
just skill-check skills/shared/design/brainstorming
just skill-check skills/shared/design/technical-design
just skill-check skills/shared/design/implementation-planning
```

For each changed file, run the pre-commit hooks that the commit invokes. Use one explicit file with `--files` per
invocation. At minimum, run `trailing-whitespace`, `end-of-file-fixer`, `mdformat`, and `markdownlint-cli2` when those
hooks apply. Use `jq empty` as the explicit JSON syntax check because this repository has no `check-json` hook.

Then run:

```bash
just check
```

`just check` requires network through `just locks`. Report a network failure separately and run every available local
gate. Do not treat validators, formatting, or JSON parsing as behavioral evidence.

Record the behavioral cases that ran, their clients and models, source revision, raw outputs, trace locations, duration,
usage, material cost, and result. Keep harness and dependency failures separate from candidate failures.

### 7. Commit, Synchronize, and Verify Deployment

Before staging, require an empty index. Preserve unrelated worktree changes and stage explicit paths only.

Commit the cohesive source unit with:

```text
refactor(design-skills): strengthen intent and evidence
```

Include only the three source packages, their behavioral cases, their attribution updates, the research document, the
governing overview, this plan's completion update, and any evaluation record created for these cases.

After the source commit, run the required lock synchronization:

```bash
just skills-sync
```

That command creates the separate lock commit. Do not combine source and lock changes. Then verify each deployed skill:

```bash
just skills-deployed --skill brainstorming --verbose
just skills-deployed --skill technical-design --verbose
just skills-deployed --skill implementation-planning --verbose
```

When all completion evidence passes, mark this plan complete and move it to `docs/plans/archived/` in the source change.
Update inbound and internal relative links during that move. Keep the filename unless an archive collision exists.

## Expected Commit Sequence

1. `docs(design-skills): plan intent and evidence refresh`
2. `refactor(design-skills): strengthen intent and evidence`
3. `chore(kasetto): sync design skill locks`

The first commit records this accepted deferred plan. The second must wait until the simultaneous skill refresh is
complete. The lock commit remains separate under repository policy.

## Completion Evidence

The refresh is complete only when:

- all nine new behavior cases exist and parse;
- available baseline and revised runs distinguish candidate behavior from harness failures;
- solution-anchored seeds recover their desired outcome without silently discarding the proposed mechanism;
- direction-critical assumptions remain provisional until decision-changing evidence or accepted risk resolves them;
- brainstorming repairs activity goals without premature architecture or decorative metrics;
- every brainstorming handoff carries one observable success signal;
- product-level prohibited outcomes survive the design handoff;
- technical design distinguishes current code from intended product policy;
- technical design defines relevant negative guarantees without implementation sequencing;
- implementation plans provide safe behavioral evidence for accepted negative guarantees;
- no skill requires a one-to-one test and acceptance-condition mapping;
- the three skill validators and applicable repository checks pass;
- provenance records use pinned sources and independent expression;
- source and generated lock changes remain separate commits;
- deployed copies match committed sources across configured destinations; and
- omitted clients, models, cases, live environments, and other evidence limits remain explicit.

## Deferred Requirements-Engineering Trigger

Do not create a new skill as a consequence of this plan. Open a separate design only after observed requests show that
the existing workflow cannot cleanly own one or more of these jobs:

- review a PRD or supplied specification for missing and unverifiable requirements;
- preserve contractual, regulatory, or compliance obligations independently from system design;
- produce stakeholder acceptance criteria before architecture exists;
- maintain requirement identity and revision history across organizations; or
- hand requirements to several designs or systems without duplicating product authority.

That future design must define its input, output, authority, and handoffs before choosing a name. It must remain useful
without absorbing brainstorming, technical design, implementation planning, or implementation execution.
