# <Outcome> Implementation Plan

Status: <proposed or accepted>
Basis: \<accepted requirements and design revisions; actual section or ADR links>
Execution record: \<existing tracker, or the separate record section below>

<!-- Authoring scaffold: replace prompts and remove these instructions.
Use the repository's established plan format when one applies. Repeat the work-unit section
for independently verifiable outcomes. Omit Recovery when no special response is needed. -->

## Implementation Overview

Explain what changes, how the work reaches the outcome and why the dependencies determine this order.
Include a dependency diagram when it clarifies the flow.

## Shared Preflight

Name shared environment setup, applicable guidance, common checks and the default review gate.
Give each requirement an anchor. Every unit applies them by default and names only its additions
and exceptions. Record missing tools or review assignments and the work they block.

## Unit 1: <Observable Outcome>

### Outcome and Rationale

Explain what becomes possible and why this unit exists, appending the requirement and design keys it satisfies.

### Changes

Describe how the affected surfaces produce the outcome. Name verified paths and symbols where useful.
Identify tool-owned generated outputs and how unexpected changes will be inspected.

### Dependencies and Constraints

Name prerequisite units and interfaces, and any additions to or exceptions from the shared preflight.

### Verification and Completion

State commands or observations, inputs, expected success and failure results, and evidence limits.
Describe the review only where it differs from the shared default gate.

### Recovery

Explain failure interpretation, cleanup or rollback when a specific response is necessary.

## Final Integration

Verify the complete outcome against the requirements and design, including cross-unit guarantees.
Name qualification and authorization requirements for any operational cutover.

## Execution Record

Use this section only if the repository has no existing tracker or completion-record convention.
Record actual results, reviewed revisions, deviations and unresolved findings separately from the
intended approach. Planned commands and expected observations are not completion evidence.
