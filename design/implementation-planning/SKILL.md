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

Read the governing design, repository instructions, relevant implementation, tests, interfaces, migrations, operational
assets, and configured tooling before decomposing work. Cite the design and keep shared constraints in one authoritative
home.

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
architecture, interfaces, failure policy, compatibility, or migration strategy to technical design. Return changed
purpose or product scope to brainstorming.

Repository inspection may settle implementation-local facts and ordinary techniques already constrained by the design
and local conventions. Do not use that allowance to hide a public-behavior, compatibility, material-cost, or
architecture decision.

Check acceptance from the design's substance, not its status label. A document is not accepted for planning when it
contains consequential recommendations awaiting confirmation, unresolved behavioral or safety obligations, or
architecture added after the user's latest confirmation. Return those gaps to technical design before decomposing work.

## Map Dependencies Before Ordering

Identify prerequisites, baseline evidence, contracts or seams that unlock later work, consumers and producers, risky
assumptions worth testing early, and integration or migration dependencies. Include rollout, rollback, cleanup, and
documentation dependencies when the governing design requires them.

Size work units by independently verifiable outcome. Prefer a vertical slice that produces observable behavior. Use a
foundation unit only when it establishes a meaningful contract or seam and has useful verification of its own. Split
further when risk, reviewability, or repository workflow requires it; do not split by arbitrary minutes or file count.

Order units by dependency and risk rather than imposing universal phases. Parallel work requires disjoint ownership or
an accepted stable interface. Keep shared files, generated artifacts, and dependency-ordered changes with one owner.

## Specify Each Work Unit

For every unit, make these facts recoverable without forcing one rigid template:

- **Outcome:** the behavior, capability, migration state, or visible result;
- **Design obligations:** the accepted decisions or requirements it satisfies;
- **Affected surfaces:** verified files, symbols, configuration, data, documentation, or operational assets;
- **Dependencies:** prerequisites, consumed and produced interfaces, and downstream unlocks;
- **Implementation guidance:** the smallest useful explanation of the change and local constraints;
- **Verification:** commands or observations, expected results, and the claim each check proves;
- **Failure and recovery:** expected failure interpretation, cleanup, rollback, or next action when relevant; and
- **Completion:** the evidence that makes the unit reviewable and safe to hand onward.

Use exact paths and symbols only after repository inspection establishes them. Prefer stable identities and
responsibilities to source line ranges. A plan may include focused API declarations, interfaces, schemas, configuration
fragments, migrations, or non-obvious algorithms when they materially clarify an accepted design. Do not pre-write
routine complete files or duplicate the future source of truth.

Assign generated files, dependency locks, migrations, documentation, and operational configuration to the unit whose
outcome requires them. Do not allow tools to modify unlisted surfaces by implication.

## Match Verification to the Claim

Place verification beside the work it proves. State the command, input, or observation; expected success; relevant
failure result; environment or dependency; check level; and any obligation left unverified.

Behavioral outcomes require behavioral tests or real-system observations. Formatting, linting, typing, builds, syntax
checks, substring searches, and clean version-control state may be necessary, but they do not prove behavior.

Use test-driven development when a focused automated test can state the changed observable behavior. Do not impose it on
documentation, mechanical configuration, exploratory integration, or work whose suitable evidence lies at another
boundary. Follow repository commit policy instead of requiring one commit per work unit.

End the complete plan with system-level verification traced to the governing outcome. File existence, task completion,
or clean version-control state alone cannot establish completion.

## Write and Check the Plan

Resolve the plan path in this order:

1. Use a path supplied by the user.
2. Continue the same existing plan already in scope.
3. Follow the governing design's companion-document map.
4. Follow a documented repository convention.
5. Follow one clear convention established by existing artifacts.
6. Otherwise propose `docs/plans/<name>-implementation-plan.md` and ask once.
7. Outside a repository, ask for a destination.

Use two or three descriptive kebab-case words before `-implementation-plan.md` in the fallback. Link the plan and design
to each other while preserving their authority: the design owns system behavior; the plan owns execution order.

Before calling the plan ready, check design coverage, dependency order, interface consistency, ownership, verified
touchpoints, placeholders, verification strength, and final integration evidence. Make unavailable checks and unresolved
risks visible. An implementer should be able to execute without reconstructing the design conversation.

Saving or completing a plan does not authorize implementation. Continue only when the user's request already supplied
that authority; otherwise present the plan and stop before changing the system.
