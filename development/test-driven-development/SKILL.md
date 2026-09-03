---
name: test-driven-development
description: Guide test-first implementation of observable feature and bug-fix behavior. Use before production code when a focused automated test can state the expected result; not for test-only strategy, coverage, or validation work.
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

1. Read nearby tests, the existing behavior, and the repository's test configuration.
2. State the behavior, input or trigger, expected result, and an independently derived oracle.
3. Discover the relevant test command from repository tooling or neighboring tests. Never assume a language, runner,
   assertion API, or mock library.

If the behavior is unclear, clarify it before inventing an assertion. If no useful automated seam exists, use the most
direct available validation and report what automated regression evidence remains absent.

## Test Worthiness

Add a test only when it protects changed observable behavior, a durable contract, or a reproduced defect. Do not add one
merely because a function, line, private helper, constant, configuration text, or coverage target is new.

Name the production change that should make the test fail. If none is a bug, redesign around a consumer-visible result or
omit the test and use the most direct relevant validation.

Test pure logic directly with real inputs and outputs. Unit tests may mock only genuine side-effect boundaries, such as
external I/O, time, randomness, or processes. Integration and end-to-end tests use real dependencies in an isolated
environment; otherwise classify them accurately.

## Red

Write one focused test for the next behavior that passes the test-worthiness gate. Run it and confirm that it fails because
the behavior is missing or wrong, rather than because of setup, syntax, or a broken environment.

A test that already passes may cover existing behavior. Refine the scenario or explain why it cannot provide red-step
proof. Do not claim test-driven development without that proof.

## Green

Make the smallest production change that makes the focused test pass. Re-run it, then run wider validation when the
change's risk or repository rules require it.

Keep the test's oracle independent of the implementation. Prefer externally visible behavior and durable contracts over
private calls, source text, or incidental structure. Mock only the side-effect boundary needed to preserve the behavior
under test. Use `test-engineer` when selecting a test level, oracle, or mock strategy needs deeper analysis.

## Refactor

After green, improve names, remove duplication, or simplify structure without changing behavior. Re-run the affected
tests after each meaningful refactor. Start the next behavior with a new red step.

## Existing Code and Stale Tests

Do not delete or discard existing production code merely because it predates a failing test. Preserve it, identify the
behavior to protect, and add a characterization or focused regression test where useful.

When an existing expectation conflicts with intended product behavior, treat it as a requirements question. Do not
silently weaken or rewrite the assertion to obtain green.

## Report Honestly

Before completion, state:

- the behavior added or fixed;
- the test command and observed red and green results;
- wider validation run, if any; and
- tests or risks still absent, and why.

If no focused test failed first, report the work as validated implementation, not TDD.
