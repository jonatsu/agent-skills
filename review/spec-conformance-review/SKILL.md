---
name: spec-conformance-review
description: Compare an implementation, diff, pull request, or release with its accepted requirements specification and technical design, reporting material omissions, contradictions, unplanned scope, stale artifacts, and missing verification. Use for spec conformance, requirements coverage, “did we build what we specified?”, or review with approved spec context; not for writing specs, general code review without an accepted spec, or implementing fixes.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Specification Conformance Review

Determine whether delivered behavior materially conforms to accepted requirements and their technical realization.
Review outcomes and obligations rather than demanding literal correspondence between prose and code. Classify the cause
of each mismatch before assigning blame or proposing a repair.

This supplements code, security, test, and operational review; it does not replace them. Fold conformance findings into
an active review when one exists, otherwise return a standalone findings report.

## Establish the Review Basis

Read the accepted requirements specification, compatible technical design, implementation plan or completion record,
changed implementation, relevant tests and documentation, and available runtime evidence. Follow repository conventions
to locate them; do not require fixed filenames or a pull request.

Identify the exact revisions or states under comparison. Confirm that the specification was accepted by someone with
requirements authority and that the design claims compatibility with it. If the specification is proposed, ambiguous,
or newer than the design, report the authority or revision gap before judging implementation conformance. Continue only
comparisons that do not depend on that gap.

Treat each artifact according to its authority:

- the accepted specification owns intended observable behavior;
- technical design owns the selected system guarantees, interfaces, and internal realization;
- the implementation plan owns execution, migration, rollout, and verification obligations; and
- code, configuration, deployed artifacts, and observations establish current behavior.

The user's current instruction and accepted requirement changes outrank stored artifacts. A status label alone does not
prove that two artifacts describe the same accepted revision.

## Build the Commitment Map

Extract only concrete commitments relevant to the reviewed scope:

- required user-visible behavior and acceptance criteria;
- prohibited outcomes and negative guarantees;
- system invariants, interfaces, compatibility, and failure or recovery behavior from technical design;
- migration, rollout, rollback, cleanup, documentation, and verification obligations from the plan; and
- explicit scope and non-goals that distinguish required work from unplanned expansion.

Use existing stable requirement identifiers or anchors. Do not invent an identifier scheme during review. Preserve the
chain from requirement to design guarantee to implementation surface and evidence, but do not require one requirement,
one code location, and one test to correspond mechanically. One behavior may cross several components, and one
integration observation may support several related guarantees.

## Compare Behavior and Evidence

Inspect both the diff and resulting state. A diff shows what changed; it cannot prove what the complete system now does.
Use behavioral tests, conformance fixtures, safe runtime observations, schemas, migrations, generated artifacts, and
other claim-matched evidence where available.

Check for:

- required behavior that is absent or observably different;
- behavior that contradicts an accepted requirement or design guarantee;
- prohibited behavior or disclosure that remains possible;
- significant new behavior, dependency, interface, or operational burden outside accepted scope;
- required compatibility, migration, rollout, rollback, cleanup, or documentation work that is missing; and
- verification that is absent, too narrow, unsafe, or incapable of proving its stated claim.

Do not use file presence, substring searches, formatting, typing, builds, clean version-control state, or passing narrow
unit tests as proof of behavioral conformance. They may support separate structural claims. Report unavailable evidence
as a coverage limit rather than assuming either conformance or failure.

Allow implementation-level variation when it preserves the accepted behavior, system guarantees, safety boundaries,
compatibility, and operational obligations. Naming, file placement, decomposition, and low-level technique are not
findings merely because the design or plan used different illustrative language.

## Classify Before Recommending Repair

Assign each material mismatch to the smallest accurate class:

- **Implementation defect:** accepted behavior or a design guarantee is not realized.
- **Evidence gap:** the implementation may conform, but available checks cannot establish the claim.
- **Unplanned scope:** the implementation adds consequential behavior or cost outside accepted scope.
- **Design gap or stale design:** requirements are accepted, but technical realization is absent, contradictory, or
  based on an older revision.
- **Specification ambiguity or staleness:** intended behavior cannot be determined, or authorized policy changed without
  a corresponding accepted revision.
- **Unpropagated accepted deviation:** an authorized implementation change exists, but governing artifacts and dependent
  evidence were not reconciled.

Do not rewrite a specification to make accidental implementation behavior compliant. Do not reject a safe equivalent
implementation merely because it differs from an example. When evidence supports more than one class, state the
uncertainty and name the authority or observation that would distinguish them.

## Report Findings in the Active Review

Lead with material findings ordered by severity. For each finding include:

- the governing requirement, design guarantee, or plan obligation;
- the implementation and evidence inspected;
- the observed mismatch and its classification;
- the user, safety, compatibility, operational, or maintenance consequence;
- the smallest responsible owner or phase for correction; and
- the evidence that would close the finding.

Use the enclosing review's severity vocabulary and output format when one is established. Put a finding at a changed
line only when that line materially causes or exposes it; broader drift belongs in the review summary. When no enclosing
review exists, return a standalone report rather than inventing a repository file or external system.

Do not add comments merely to state that an item conforms. Summarize coverage instead: which requirement areas were
examined, what evidence supports them, and what remained unverified. Do not post to GitHub, change external review state,
or create files unless the user requested that effect.

## Preserve Review Authority

Review does not authorize fixes. Report implementation defects before changing code, and route an accepted repair
through the normal implementation workflow. Route requirements ambiguity or change to `requirements-specification`,
technical gaps to `technical-design`, execution and evidence gaps to `implementation-planning` or `test-engineer`, and
security defects to `security-review`.

A conformance review is complete when the compared revisions, covered commitments, material findings, classifications,
evidence, and coverage limits are explicit. “No material mismatch found” is supportable only for the examined scope and
evidence; it is not proof that the implementation is correct in every respect.
