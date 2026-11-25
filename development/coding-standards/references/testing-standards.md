# Testing Standards

Load this when writing tests, judging whether coverage is adequate, or planning what to test.

## What Deserves a Test

A test is the last guard, not the first. Catch each possible failure at the cheapest level that can catch it:

1. Design it out. Parse input at the system boundary into types that cannot hold invalid values, and let
   constructors enforce invariants. The compiler or the parser then rejects the failure.
2. Make it loud. Validate at the boundary and fail fast with a clear error, assert internal invariants, and exit
   nonzero. The failure then shows the first time the code runs.
3. Test what remains: each behavior whose failure would otherwise pass silently and cost something. Examples are
   a wrong result, a wrong signature, lost work, a deleted file, a leaked secret, a race, or a broken contract
   between components.

Loud checks replace tests of input variations, not tests of logic: a calculation that returns a wrong value fails
silently, so it still gets a test. Test a validator at the boundary, once for each rule whose failure would let
dangerous input through, rather than every function with every bad input. Where correctness depends on a large
input space, as in a parser or an encoder, write one property-based test or fuzz target instead of many
hand-picked examples.

A reproduced defect always earns a regression test, loud or not, because it has shown that it happens. When the
fix makes the whole defect class impossible, the type or parser that now rejects it is the regression guard.

Leave out a test that repeats what another test already guards. Leave out a failure that shows loudly the first
time the code runs, before it ships, and an edge case that is unlikely to break. Writing a test first changes
when it is written, not whether it is worth writing. Test more deeply when the repository's test policy or the
user asks for it.

## Where to Test

Test behavior at the level where it must hold, not the implementation that delivers it. Unit-test pure logic
with real inputs and outputs, mocking only a genuine side-effect boundary such as a third-party service, the
network, or the clock. Integration-test across real boundaries, and drive the whole path end to end for
anything a user runs or calls. When a change crosses a boundary, write the integration or end-to-end test that
covers it. A green unit suite over mocked boundaries says nothing about the wired system. Run each check across
all its affected files at once. Formatting, linting, and a green build do not prove behavior.

## How to Write a Test

Structure each test as arrange, act, assert, and keep its assertions focused on one behavior. Give each test a
descriptive name that reads as a specification, and keep it isolated so it runs alone and in any order. Keep unit
tests fast, so the feedback loop stays tight. Set coverage goals by risk and rate of change rather than a blanket
percentage, and track the trend to catch a regression. Treat a green suite as a merge gate for production
changes. Write suites that read as documentation of how the system behaves.

Plan the scope up front, aligned with the requirements. Separate what must be validated from how it is
implemented, and include manual steps for a high-risk or UX-heavy change that automation does not cover. Hold
each test to the standard of the code it guards. Keep it simple, make it fail when the behavior breaks, and
keep it quiet on unrelated changes. Change a test only when a requirement or independent evidence shows it
wrong, and say why. When you change core logic, write the test first to pin the requirement. Report what you
exercised and what you left uncovered. When verification is blocked, find another route, preserve the work, and
name the missing evidence before continuing.

## Solve the Problem, Not the Test

Understand the requirement and implement the correct algorithm for it. Make the solution correct for every valid
input, not only the cases a test names. Tests verify correctness; they do not define it. Use the standard tools
and the real logic, never a hard-coded value or a special case that fakes a passing result. When the
requirement is infeasible or a test encodes the wrong expectation, say so and stop rather than bend the code to
pass.
