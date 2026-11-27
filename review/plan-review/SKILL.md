---
name: plan-review
description: Review an implementation plan before it is built, whether a plan document, a plan-mode plan, or a short written proposal. Use when asked to critique or review a plan, whether a plan is ready to build, or whether it is over-built. Writing the plan goes to implementation-planning, pressure-testing it by interviewing the user to interview-me, and reviewing a design or architecture to architecture-review.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Plan Review

Decide whether a plan will deliver what it promises, and report what would make it fail. Start from doubt: a plan
earns `Ready` through evidence, not through the absence of an obvious flaw. A review authorizes a report, so hand
each fix back to the plan's author and change nothing the plan describes.

## Review in Nine Steps

Run all nine steps on every plan, in order, at a depth that fits it. For a short plan a step may take one
sentence; a plan document gets each unit checked and the full coverage map. Run a step even when you expect
nothing from it, because a small plan fails at the step it skipped.

1. **Establish the basis.** Find what the plan must achieve: the request, spec, or design behind it, its
   acceptance criteria and constraints, and the success signal for the whole result. With no written basis, take
   the criteria from the stated request and report the missing basis. When the plan rests on a design decision
   that is still open, the verdict is `Not ready`: name the decision and send it to `technical-design`, because
   planning cannot settle it.
2. **Ground every claim.** Check each thing the plan asserts about the code, APIs, tools, or environment against
   its source: the files, the language server's definitions and references, or the dependency's documentation at
   the version the project pins. A plan that needs a capability the environment lacks, or an approach the
   platform forbids, fails here, before any other step matters.
3. **Check coverage both ways.** Map each acceptance criterion to the plan items that satisfy it, and each item
   back to a criterion. Count prohibitions and negative guarantees as criteria, since a plan misses them
   silently. A criterion no item covers is a gap, usually Must fix. An item no criterion asks for is unmapped
   scope, usually Should fix or Consider.
4. **Check proportion.** For each component, dependency, abstraction, or configuration option, ask what breaks if
   it is deleted. When nothing concrete breaks, it is speculative: the plan must justify it, not you its removal.
   Then ask whether a smaller plan reaches the same outcome, and name that plan concretely.
5. **Check structure and order.**
   - No unit uses what a later unit produces.
   - The riskiest assumption is tested early, before the work that depends on it.
   - Each unit ends in a result that can be verified on its own; a unit whose title needs an "and" is two units.
   - Units planned in parallel touch separate files, or share only an agreed, stable interface.
6. **Check verification.** Each unit names the evidence that proves its claim: a command or observation, its
   expected result, and what it proves. A behavioral claim needs a behavioral test or a real-system observation;
   a build, lint, type check, or clean tree proves no behavior. The plan ends with a system-level check tied to
   the success signal, and names who reviews each substantive unit and when.
7. **Check failure and recovery.** Name the edge cases plausible for this change, such as an empty input, a
   concurrent run, or a partial failure, rather than a generic list. Each step that can fail halfway has a
   cleanup or rollback. Each irreversible step, such as a schema drop, a force-push, or a deletion, passes
   through an explicit confirmation. Stopping after any unit leaves the system working.
8. **Run a premortem.** Assume the plan was carried out and failed. Name the most likely reasons, and turn each
   one the earlier steps did not find into a finding. Working back from the failure finds risks that a forward
   check misses.
9. **Check that it can be carried out.** Read the plan as its implementer, who may be a smaller model with none
   of the author's context. The first action is clear, each term is defined, each path and symbol exists, and
   each command has been run once. A step the implementer would have to ask about is a finding.

## Ground Every Finding

Cite the evidence for each finding: the plan text, and the file and line, source, or stated premise that confirms
or refutes it. Put what you could not check under Unverified, and claim that something "already exists" or
"already handles" a case only with evidence. Point at what is wrong and the direction of the fix, and leave the
rewriting to the author.

The review is done when all nine steps have run, and each finding cites its evidence or sits under Unverified.

## Report

1. **Verdict**: `Ready`, `Ready after changes`, or `Not ready`, then one sentence saying why. Any open Must fix
   finding rules out `Ready`; use `Not ready` when the plan needs rework or rests on an open design decision.
2. **Scope**: the plan and its revision, the basis judged against, and how you checked it. When the plan has more
   than a handful of items, include the coverage map: each criterion with its covering items, gaps and unmapped
   items marked.
3. **Findings**, most consequential first, each tagged `F1`, `F2`, and so on. Give each its tier, where it is in
   the plan, what is wrong and the failure it leads to, the evidence, and the smaller or corrected alternative.
   - **Must fix**: the plan cannot deliver its success signal as written, such as an impossible step, a gap, a
     unit that depends on a later one, or a behavioral claim with no behavioral check.
   - **Should fix**: a risk or excess that a recorded follow-up can carry, such as an unmapped item or a missing
     rollback for a step that rarely fails.
   - **Consider**: an optional improvement. Report at most five, and say how many you left out.
4. **Unverified**: what you flagged but could not check, each with the check that would settle it.
5. **Next checks**: what would settle each unverified claim, such as running a command or prototyping the riskiest
   unit, and the reviews to run next, such as `architecture-review` when a finding reaches the design.
6. **What holds**, only when something specific should survive a rewrite: at most two sentences, with its place
   in the plan.

A clean plan gets the verdict, the scope, and the next checks.

## Attributions

See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for the sources this skill is based on.
