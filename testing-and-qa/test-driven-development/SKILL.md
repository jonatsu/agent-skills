---
name: test-driven-development
description: Implement a feature or bug fix test-first, with red-green-refactor proof. Use when asked for TDD, red-green-refactor, or a test-first fix or feature, or before production code when a focused automated test can state the expected result; not for test strategy, coverage, or tests-only work (test-engineer).
license: MIT
metadata:
  author: Joonas Onatsu
---

# Test-Driven Development

Use a proportionate red-green-refactor loop for an observable feature or bug fix. Its evidence is a focused test that
failed for the intended missing behavior, then passed after the smallest production change.

`test-engineer` owns tests-only strategy, coverage, and validation work. This skill owns the implementation lifecycle
when production code will change.

## Establish the Test Seam

Before editing production code:

1. Follow the requirements the accepted plan or the repository sets for this change; a missing plan is no reason to
   write one before a focused test.
2. Read nearby tests, the existing behavior, and the repository's test configuration.
3. State the behavior, input or trigger, expected result, and an oracle derived independently of the
   implementation.
4. Take the test command, runner, and assertion and mock libraries from repository tooling or neighboring tests.

If the behavior is unclear, clarify it before inventing an assertion. If no useful automated seam exists, use the most
direct available validation and report what automated regression evidence remains absent.

## Test Worthiness

Add a test only when it protects changed observable behavior, a durable contract, or a reproduced defect. Do not add one
merely because a function, line, private helper, constant, configuration text, or coverage target is new.

Name a plausible production bug the test would catch; when you cannot, test a consumer-visible result instead, or skip
the test and validate directly.

Test pure logic directly with real inputs and outputs, and prefer externally visible behavior and durable contracts over
private calls, source text, or incidental structure. Unit tests may mock only genuine side-effect boundaries, such as
external I/O, time, randomness, or processes, and only the boundary the behavior under test needs. Integration and
end-to-end tests use real dependencies in an isolated environment; otherwise classify them accurately. Use
`test-engineer` when selecting a test level, oracle, or mock strategy needs deeper analysis.

## Red

Write one focused test for the next behavior that passes the test-worthiness gate. Run it and confirm that it fails because
the behavior is missing or wrong, rather than because of setup, syntax, or a broken environment.

A test that already passes may cover existing behavior. Refine the scenario or explain why it cannot provide red-step
proof.

## Green

Make the smallest production change that makes the focused test pass. Re-run it, then run wider validation when the
change's risk or repository rules require it.

## Refactor

After green, improve names, remove duplication, or simplify structure without changing behavior. Re-run the affected
tests after each meaningful refactor. Start the next behavior with a new red step.

## Existing Code and Stale Tests

Preserve existing production code that predates a failing test. Identify the behavior to protect, and add a
characterization or focused regression test where useful.

When an existing expectation conflicts with intended product behavior, treat it as a requirements question. Do not
silently weaken or rewrite the assertion to obtain green.

## Report Honestly

A green test closes neither the unit's planned independent review nor its final validation gate, and a self-review is
not that review.

Before completion, state:

- the behavior added or fixed;
- the test command and observed red and green results;
- wider validation run, if any; and
- tests or risks still absent, and why.

If no focused test failed first, report the work as validated implementation, not TDD.
