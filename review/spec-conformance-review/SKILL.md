---
name: spec-conformance-review
description: Compare an implementation, diff, pull request, or release with its accepted spec, technical design, and plan, reporting omissions, contradictions, unplanned scope, stale documents, and missing verification. Use for spec conformance, requirements coverage, “did we build what we specified, designed, or planned?”, or checking work against its spec, design, or plan, including as the final integration review; not for writing specs, work governed by no accepted spec, design, or plan, or implementing fixes.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Specification Conformance Review

Determine whether delivered behavior materially conforms to the accepted specification and its technical realization.
Review outcomes and obligations rather than demanding literal correspondence between prose and code. Classify the cause
of each mismatch before assigning blame or proposing a repair.

This supplements code, security, test, and operational review; it replaces none of them.

## Establish the Review Basis

Compare against the accepted specification when one exists, together with its compatible technical design and the
implementation plan or completion record. Without a specification, compare against the accepted technical design and
implementation plan, and report the missing specification as a coverage limit: a design and plan say how the system
realizes intent, not what the product must do, so user-visible behavior and acceptance that only a specification
would fix stay unverified. When no accepted specification, design, or plan governs the work, conformance has no basis;
say so and return the request as general code review.

Read those documents, the changed implementation, relevant tests and documentation, and available runtime evidence.
Locate them by repository convention, or from the dispatching brief; neither fixed filenames nor a pull request is
needed.

Identify the exact revisions or states under comparison. Confirm that each document was accepted by someone with
authority over it, and that each later document claims compatibility with the one it realizes: the design with the
specification, the plan with the design. When a document is proposed, ambiguous, or older than a document it depends
on, report the authority or revision gap before judging implementation conformance, and continue only the comparisons
that do not depend on that gap.

Treat each document according to its authority:

- the accepted specification owns intended observable behavior;
- technical design owns the selected system guarantees, interfaces, and internal realization;
- the implementation plan owns execution, migration, rollout, and verification obligations; and
- code, configuration, deployed artifacts, and observations establish current behavior.

The user's current instruction and accepted requirement changes outrank stored documents. A status label alone does
not prove that two documents describe the same accepted revision.

## Build the Commitment Map

Extract only concrete commitments relevant to the reviewed scope:

- required user-visible behavior and acceptance criteria, from the specification, or as the design states them
  when no specification exists;
- prohibited outcomes and negative guarantees;
- system invariants, interfaces, compatibility, and failure or recovery behavior from technical design;
- migration, rollout, rollback, cleanup, documentation, and verification obligations from the plan; and
- explicit scope and non-goals that distinguish required work from unplanned expansion.

Cite each commitment by its existing identifier or anchor, and by its words where it has none; a review introduces no
identifier scheme of its own. Preserve the chain from requirement to design guarantee to implementation surface and
evidence, and let it branch: one behavior may cross several components, and one integration observation may support
several related guarantees.

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

Prove behavioral conformance with behavioral evidence. File presence, substring searches, formatting, typing, builds,
clean version-control state, and narrow unit tests support structural claims only. Report unavailable evidence
as a coverage limit rather than assuming either conformance or failure.

Accept implementation-level variation that preserves the accepted behavior, system guarantees, safety boundaries,
compatibility, and operational obligations. Naming, file placement, decomposition, and low-level technique that differ
from a document's illustrative language are equivalent implementations, not findings.

## Classify Before Recommending Repair

Assign each material mismatch to the smallest accurate class:

- **Implementation defect:** accepted behavior or a design guarantee is not realized.
- **Evidence gap:** the implementation may conform, but available checks cannot establish the claim.
- **Unplanned scope:** the implementation adds consequential behavior or cost outside accepted scope.
- **Design gap or stale design:** requirements are accepted, but technical realization is absent, contradictory, or
  based on an older revision.
- **Specification ambiguity or staleness:** intended behavior cannot be determined, or authorized policy changed without
  a corresponding accepted revision.
- **Unpropagated accepted deviation:** an authorized implementation change exists, but governing documents and dependent
  evidence were not reconciled.

The governing documents stay as accepted: report accidental implementation behavior as a finding, and route any wish
to keep it to the document's owner as a proposed change. When evidence supports more than one class, state the
uncertainty and name the authority or observation that would distinguish them.

## Report Findings in the Active Review

Lead with material findings ordered by severity. For each finding include:

- the governing requirement, design guarantee, or plan obligation, stated in words, with its identifier in
  parentheses where one exists;
- the implementation and evidence inspected;
- the observed mismatch and its classification;
- the user, safety, compatibility, operational, or maintenance consequence;
- the smallest responsible owner or phase for correction; and
- the evidence that would close the finding.

Use the enclosing review's severity vocabulary and output format when one is established. Put a finding at a changed
line only when that line materially causes or exposes it; broader drift belongs in the review summary. Dispatched as a
final integration gate's separate conformance review, use the vocabulary the brief names and return the report to the
dispatcher, which records it with the gate's other findings. With no enclosing review, return a standalone report and
apply `writing-for-humans` and its reader-ready check to it.

Record conformance as coverage in the summary, not as per-item comments: which requirement areas were examined, what
evidence supports them, and what remained unverified. Deliver everything in the review or the returned report; post to
GitHub, change external review state, or create files only when the user requested that effect.

## Preserve Review Authority

Review does not authorize fixes. Report implementation defects before changing code, and route an accepted repair
through the normal implementation workflow. Route requirements ambiguity or change, including a missing specification
the findings show is needed, to `writing-specs`, technical gaps to `technical-design`, execution and evidence gaps to
`implementation-planning` or `test-engineer`, and security defects to `security-review`.

A conformance review is complete when it states the compared revision of each governing document and of the
implementation, gives every commitment in the map a disposition (conforms with cited evidence, a classified finding,
or unverified), and lists the coverage limits, including a missing specification. “No material mismatch found” is
supportable only for the examined scope and evidence; it is not proof that the implementation is correct in every
respect.
