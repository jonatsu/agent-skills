# Skill Testing Guide

## Four Testing Areas

### 1. Triggering Tests
Does the skill activate at the right times?
- MUST test 5-10 queries that SHOULD trigger the skill
- MUST test 5-10 queries that SHOULD NOT trigger the skill
- SHOULD test 3-5 edge cases: ambiguous inputs, multi-domain queries, partial matches

### 2. Functional Tests
Does the skill produce correct outputs?
- MUST test each workflow using Given/When/Then format
- MUST test error handling: invalid inputs, missing dependencies, boundary conditions
- MUST verify output structure matches expected schema
- SHOULD verify the skill degrades gracefully when upstream resources are unavailable

### 3. Performance Comparison
Is the skill better than no skill?
- Baseline without skill: measure messages to completion, error rate, token usage, output quality
- With skill: SHOULD reduce messages, errors, and token consumption
- With skill: SHOULD improve output consistency and correctness

### 4. Claim Verification
Where the skill asserts how a tool or system behaves, is that assertion true of the real thing?
- MUST exercise each such claim against the tool itself. Reading the claim back and finding it
  plausible is NOT verification, and it is how a documented warning that never fires survives review
- MUST record the tool version and the date the claim was checked
- MUST name which claims were checked and which were not, so a reader can tell what to distrust
- MUST state what to re-run first after an upgrade
- A reference skill has no workflow to test functionally, so without this area it ships unexercised

## Quality Metrics

| Metric | Target |
|---|---|
| Trigger accuracy | 90%+ |
| False positive rate | <5% |
| Workflow completion | 95%+ without user correction |
| Error recovery | 80%+ handled gracefully |

## Iteration Signals

| Symptom | Adjustment |
|---|---|
| Under-triggering | Add trigger phrases, domain keywords, common paraphrases |
| Over-triggering | Narrow description scope, add disambiguation logic |
| Execution failures | Add validation gates, error paths, and recovery scripts for fragile operations |

## Test Inventory Requirements
- MUST maintain a test corpus of representative queries (positive, negative, edge)
- SHOULD automate triggering tests in CI to catch regressions
- MUST record metric baselines before and after skill changes
