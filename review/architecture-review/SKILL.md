---
name: architecture-review
description: Review a software architecture for soundness, whether a design document, ADR, or spec before it is built, or an existing system's structure. Use when asked whether a design or architecture is sound, to review a design or ADR before committing to it, or what breaks if a structural decision is wrong. Writing a design goes to technical-design, a structural decay audit of a codebase to brooks-audit, and a code change to change-review.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Architecture Review

Decide whether a system's shape is sound, for a design not yet built or an architecture that exists, and report
what would make it fail. Start from doubt: an architecture earns `Ready` through evidence, not through the absence
of an obvious flaw. A review authorizes a report, so hand the redesign back to its author and change nothing under
review.

## Establish What It Must Meet

Proportion is judged against requirements, so settle them first. Read the design, spec, or ADR, and the
requirements it claims to realize: load and data volume, growth, availability and recovery targets, latency,
compliance, and who owns each part. When the design depends on a requirement nobody stated, report the gap as a
finding, and judge against what the documents do state.

For an existing system, map its structure with `brooks-audit` when it is available. Read the code that holds each
boundary in question, and ground each dependency in its real callers with the language server's references and
call hierarchy.

## Apply Each Question That Fits

Apply each question that fits the target, and skip the rest rather than inventing a concern.

1. **Proportion and placement.** Is the shape proportional to the problem, with its boundaries drawn where they
   belong? Flag a design built for a hypothetical future or too small for its real load, and a component doing
   work that belongs elsewhere. Where the design adopts a style, such as layers or ports and adapters, check that
   its cost pays for itself where it is applied; a simple data-entry path needs no full layering. The
   `architecture-styles` skill holds the signals that a style earns its cost.
2. **Feasibility.** Can it ship as drawn? Flag a design that needs a change from a team that does not own the
   system, an approval nobody holds, or a break in a promised contract or deprecation timeline. When it abandons
   an existing decision, pattern, or stack, ask what it gains over evolving the current one and how the
   transition runs.
3. **Blast radius.** If this is wrong, what breaks, and how far does it reach? Separate the reversible from the
   irreversible: a wrong data model or public interface costs more than a choice that can be unwound.
4. **Hidden coupling.** Name the dependencies the design does not: shared mutable state, an ordering requirement
   between components, an implicit contract two modules both assume, or framework and storage types that leak
   into the core logic. Check whether each stated boundary is enforced by a check, such as an import rule in CI,
   or held only by convention, which erodes under change.
5. **Failure, scale, and operation.** Walk concurrency, partial failure, retries, and input an order of magnitude
   larger than expected. Ask what happens when a dependency is slow, down, or changes its interface without
   notice. Ask which signal reports each failure and who receives it, including a change that reports success but
   produces a wrong result. Ask whether recovery has been tested: a backup restored, a failover, a rollback.
   When the design states quality targets, check that each has a measure and the load it holds at, that the
   capacity estimate's inputs are marked, and that every single point of failure is removed or accepted.
6. **Data.** Name the owner of each piece of data and the components allowed to change it. Check that each
   consistency choice, strong or eventual, fits what the readers of that data need.
7. **Trust boundaries.** Are they where the design believes? Flag input treated as trusted without a stated
   reason, a boundary that moves once you trace the real call path, and a privilege that crosses a line the
   design draws elsewhere.
8. **Unstated assumptions.** Surface what the design leans on but never states: timing, an external resource's
   availability, data integrity, or a security or financial consequence. Check that each consequential,
   hard-to-reverse decision is recorded with its reason, such as in an ADR, so a later change can tell a
   deliberate choice from an accident.

## Ground Every Finding

Cite the evidence for each finding: the design text, a file and line, or a tool result. Put what you could not
check under Unverified, and claim that something "already handles" a case only with evidence. Point at what is
wrong and the direction of the fix, and leave the redesign to the author.

The review is done when every question that fits has been applied, and each finding cites its evidence or sits
under Unverified.

## Report

1. **Verdict**: `Ready`, `Ready after changes`, or `Not ready`, then one sentence saying why. Any open Must fix
   finding rules out `Ready`; use `Not ready` when the shape itself needs rework.
2. **Scope**: the documents and revisions or the tree examined, the requirements judged against, and how: reading,
   structural mapping, or tool queries.
3. **Findings**, most consequential first, each tagged `F1`, `F2`, and so on. Give each its tier, where it is (a
   section, or a file and line), the failure it causes and the condition that triggers it, the evidence, and the
   direction of the fix.
   - **Must fix**: it causes a failure under the stated requirements, or it is irreversible once built, such as a
     data model that cannot hold a required case.
   - **Should fix**: a risk the stated requirements do not reach yet, which a recorded follow-up can carry.
   - **Consider**: an optional improvement. Report at most five, and say how many you left out.
4. **Unverified**: what you flagged but could not check, each with what would settle it, such as a load test or a
   prototype.
5. **Next checks**: the reviews to run next, such as `security-review` for a trust boundary.
6. **What holds**, only when something specific should survive a revision: at most two sentences, with its
   location.

When the caller asks for an implementation brief, add it last: the fixes as a dependency-ordered task list that a
later session can carry out without redoing the reasoning. Write a report file only when the caller asks, where
the repository's conventions keep such records.

A sound architecture gets the verdict, the scope, and the next checks.

## Attributions

See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for the sources this skill is based on.
