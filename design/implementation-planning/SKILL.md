---
name: implementation-planning
description: Turn an accepted technical design into dependency-ordered, independently verifiable implementation work. Use for implementation plans, task decomposition, affected surfaces, sequencing, migration execution, and adjacent verification; not for unresolved product scope, architecture invention, or implementation itself.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Implementation Planning

Turn an accepted design into an actionable route to completed, verified behavior. Write for a capable implementer who
may not know the repository, decision history, or local tooling. Preserve design obligations and keep consequential
product or architecture decisions outside the plan.

## Verify the Design Basis

Read the governing requirements specification and design, repository instructions, relevant implementation, tests,
interfaces, migrations, operational assets, and configured tooling before decomposing work. Cite the specification and
design when they exist, and keep each shared constraint in its authoritative home.

Consume accepted designs in arc42 or the repository's own format without requiring reformatting. Refer to their actual
sections and decision records. Derive work units from dependencies and outcomes, never from design chapter order.

Planning normally requires an accepted technical design. Requirements alone are insufficient when behavior,
architecture, interfaces, failure handling, compatibility, or migration choices remain open. A small change may use an
existing implementation or settled repository convention as design authority when no consequential design decision
remains; state that basis instead of manufacturing a design document.

**If unresolved consequential design controls all remaining work, stop after reporting the gaps.** Do not emit a
conditional implementation plan, turn design decisions into implementation units, or sketch the work that would follow
each possible answer. Resume planning after the design is settled. When only one branch is blocked, plan only genuinely
independent, already-designed branches and state the limit.

When the design is incomplete, record the exact gap, its downstream consequence, and the design section or owner that
must resolve it. Stop only the blocked branch; independent, already-designed work may continue. Return missing behavior,
architecture, interfaces, failure policy, compatibility, or migration strategy to technical design. Return missing or
contradictory intended behavior and acceptance to `requirements-specification`. Return changed purpose or product scope
to brainstorming.

Repository inspection may settle implementation-local facts and ordinary techniques already constrained by the design
and local conventions. Do not use that allowance to hide a public-behavior, compatibility, material-cost, or
architecture decision.

Check acceptance from the design's substance, not its status label. A document is not accepted for planning when it
contains consequential recommendations awaiting confirmation, unresolved behavioral or safety obligations, or
architecture added after the user's latest confirmation. Return those gaps to technical design before decomposing work.
When an accepted specification exists, require the design to name a compatible revision; a newer accepted requirement
keeps the affected planning branch blocked until technical design reconciles it.

## Establish Required Practices

Inspect the applicable repository instructions, language/coding rules, configured checks, and available skill catalog.
Resolve which guidance applies to the actual work, including packaging, parsing, security, tests, generated artifacts,
and deployment when relevant. Do not invent skill names, assume authoring-machine paths, or load the full catalog.
Reuse guidance already read in the session unless it changed. Explicit user decisions and repository requirements
outrank skill defaults; a generic recommendation does not authorize an incidental tooling or framework migration.

Define shared environment setup, coding guidance, and review procedures once in a shared preflight section. Give each
shared requirement a short name or anchor. Each affected unit references the requirements it uses and explains its
exceptions. Name the skill or authoritative rule, the work that triggers it, and when it must be read before editing
or verification. An unattached appendix or a general instruction to "follow best practices" is insufficient.
Record missing required guidance or unavailable tooling as a prerequisite with its owner and downstream effect.
Require completion evidence for the applicable coding rules and checks, not merely a claim that a skill was loaded.

## Map Dependencies Before Ordering

Identify prerequisites, baseline evidence, contracts or seams that unlock later work, consumers and producers, risky
assumptions worth testing early, and integration or migration dependencies. Include rollout, rollback, cleanup, and
documentation dependencies when the governing design requires them.

Size work units by independently verifiable outcome. Prefer a vertical slice that produces observable behavior. Use a
foundation unit only when it establishes a meaningful contract or seam and has useful verification of its own. Split
further when risk, reviewability, or repository workflow requires it; do not split by arbitrary minutes or file count.
A unit whose title needs an "and" to describe it, or that spans two independent subsystems, is two units.

Order units by dependency and risk rather than imposing universal phases. Parallel work requires disjoint ownership or
an accepted stable interface. Keep shared files, generated artifacts, and dependency-ordered changes with one owner.

## Specify Each Work Unit

Use [the plan template](assets/implementation-plan-template.md) unless explicit user instructions or an established
repository plan convention supplies the structure. Preserve an existing plan's organization when extending it.
An unrelated document does not establish a plan convention. Read [the worked plan](references/implementation-plan-example.md)
before the first draft to calibrate detail; its paired design illustrates the design-to-plan boundary.

Start with a short implementation overview: what changes, how the work reaches the outcome, and which dependencies
determine the order. Put this explanation before paths and commands. Include a dependency diagram when the flow needs
one. Then give each unit these sections: Outcome and rationale; Changes; Dependencies and constraints; Verification
and completion; and Recovery when a failure needs a specific response. Follow repository headings when they differ.

Explain how the changes produce the outcome in connected prose, rather than presenting a list of files to edit.
Within that structure, make these facts recoverable:

- **Outcome:** the behavior, capability, migration state, or visible result;
- **Requirements and design obligations:** the accepted behavior and technical decisions it satisfies;
- **Affected surfaces:** verified files, symbols, configuration, data, documentation, or operational assets;
- **Dependencies:** prerequisites, consumed and produced interfaces, and downstream unlocks;
- **Required practices:** applicable skills, coding rules, and the preflight step that applies them;
- **Implementation guidance:** the smallest useful explanation of the change and local constraints;
- **Verification:** commands or observations, expected results, the claim each check proves, and relevant negative
  guarantees;
- **Review gates:** reviewer responsibility, timing, scope, evidence, and what blocks dependent work;
- **Failure and recovery:** expected failure interpretation, cleanup, rollback, or next action when relevant; and
- **Completion:** the evidence that makes the unit reviewable and safe to hand onward.

Use exact paths and symbols only after repository inspection establishes them. Prefer stable identities and
responsibilities to source line ranges. A plan may include focused API declarations, interfaces, schemas, configuration
fragments, migrations, or non-obvious algorithms when they materially clarify an accepted design. Do not pre-write
routine complete files or duplicate the future source of truth.

Assign generated files, dependency locks, migrations, documentation, and operational configuration to the unit whose
outcome requires them. Identify expected generated outputs and the tools that own them. Inspect unexpected changes
before including them; explain necessary consequences and keep unrelated changes outside the work. An unexpected
output that changes scope or a consequential contract returns to the appropriate design or authority boundary.

## Match Verification to the Claim

Place verification beside the work it proves. State the command, input, or observation; expected success; relevant
failure result; environment or dependency; check level; and any obligation left unverified.

Map evidence according to the claim rather than forcing one test for each acceptance condition. One obligation may need
several checks across different boundaries. One check may support several obligations when its evidence genuinely
overlaps.

Name the environment and safe data when verification can mutate state, contact services, expose secrets, or incur cost.
Report unavailable safe evidence instead of substituting an unauthorized live check.

Behavioral outcomes require behavioral tests or real-system observations. Formatting, linting, typing, builds, syntax
checks, substring searches, and clean version-control state may be necessary, but they do not prove behavior.

Use test-driven development when a focused automated test can state the changed observable behavior. Do not impose it on
documentation, mechanical configuration, exploratory integration, or work whose suitable evidence lies at another
boundary. Follow repository commit policy instead of requiring one commit per work unit.

End the complete plan with system-level verification traced through the design to the governing requirements and
outcome. File existence, task completion, or clean version-control state alone cannot establish completion.

## Put Review Stages in the Work

The plan must state who reviews, when, how, and what evidence closes the gate. Put the applicable stages in the work
units and dependency order, not just in a closing recommendation:

1. **Before implementation:** the implementer checks scope, prerequisites, required practices, test seams, and failure
   or recovery scenarios. Give sensitive or irreversible work deeper scrutiny before coding; name an early independent
   review when a concrete risk or repository requirement warrants its cost.
2. **During implementation:** perform self-review, the applicable test loop, coding-rule checks, and proportionate
   integration validation. Record observed outcomes; a command written in the plan is not a result.
3. **After a substantive unit:** an independent reviewer examines the exact change and its evidence before dependent
   work proceeds. Identify the role or assignment mechanism. Independence requires someone other than the implementer;
   a second self-review cannot be labeled independent. For a small low-impact change, a documented self-review and
   focused checks may suffice unless repository policy requires more. State that choice and its reason.
4. **After corrections:** the implementer owns repairs; the reviewer checks the changed findings and affected evidence.
   Track severity, location, concrete failure or violated requirement, correction, and blocking status. Required checks
   and blocking findings must be resolved before the unit closes. Record nonblocking follow-ups with an owner and reason.
5. **At system completion and operational cutover:** review cross-unit behavior, migration/recovery, packaging, and the
   applicable qualification evidence. Before consequential external actions, review the exact proposed operation and
   obtain only authorization not already supplied. Unit approval does not supply deployment or risk acceptance.

When an accepted requirements specification governs the outcome, make `spec-conformance-review` or an equivalent
requirements-to-implementation comparison part of the final integration gate. Feed its material findings into the
existing review record; do not create a parallel approval path.

Use one focused independent review per substantive unit and one final integration review for multi-unit changes as
the default. Prefer compact handoffs containing base/head revisions, the relevant diff/contracts, test evidence, and
open findings. Reuse the reviewer and unchanged evidence; do not replay full session history or review every file or
commit separately. Broaden a recheck only for changed scope, new failures, or a concrete dependency impact.
Scale the strategy to the work instead of imposing independent agents or a full audit on every minor edit.

Review may be performed by a person, another agent, or a separate session where the environment and authorization allow.
Naming a reviewer does not authorize subagent/model calls or their cost. If required independent review is unavailable,
record the missing assignment and keep the dependent completion gate open; continue independent authorized work.
Neither the implementer nor reviewer may waive a consequential requirement or uncovered risk on the user's behalf.

## Write and Check the Plan

Keep intended work distinct from execution evidence. The plan states actions and expected observations; the repository's
existing tracker or completion-record convention holds actual results, deviations, reviewed revisions, and unresolved
findings. Link that record rather than creating a competing ledger. If no convention exists, use one clearly separated
execution-record section in the plan. Do not scatter status through explanatory prose or present expected results as
observations. Update the intended approach when an authorized adaptation changes it, retaining the reason in the record.

Resolve the plan path in this order:

1. Use a path supplied by the user.
2. Continue the same existing plan already in scope.
3. Follow the governing design's companion-document map.
4. Follow a documented repository convention.
5. Follow one clear convention established by existing artifacts.
6. Otherwise propose `docs/plans/<name>-implementation-plan.md` and ask once.
7. Outside a repository, ask for a destination.

Use two or three descriptive kebab-case words before `-implementation-plan.md` in the fallback. Link the specification,
design, and plan while preserving their authority: the specification owns intended observable behavior, the design owns
its technical realization, and the plan owns execution order.

Before calling the plan ready, check requirement and design coverage, source-revision consistency, dependency order,
interface consistency, ownership, verified touchpoints, required-practice preflight, review-stage placement, reviewer
assignment, finding-resolution gates, review cost, verification strength, and final integration evidence. Remove
placeholders and expose unavailable checks and unresolved risks. Require the completion record to identify applied
guidance, reviewed revisions, results, finding dispositions, and unverified obligations. An implementer should not need
to reconstruct the specification or design conversation.

Read the plan as an unfamiliar implementer: can you identify the first action, explain what it unlocks, understand how
each unit achieves its outcome, recognize completion, and respond to a failed check? Check that shared preflight
references resolve and that the final integration gate proves the complete behavior. Headings and command lists alone
do not establish an actionable plan.

Saving or completing a plan does not authorize implementation. Continue only when the user's request already supplied
that authority; otherwise present the plan and stop before changing the system.
