# Test Strategy Method

The method behind `TEST-STRATEGY` mode. Load it when the deliverable is a plan rather than test code.

- [Pick the entry move](#pick-the-entry-move)
- [Step 1: Name the behaviors, not the units](#step-1-name-the-behaviors-not-the-units)
- [Step 2: Rank by risk](#step-2-rank-by-risk)
- [Step 3: Allocate levels](#step-3-allocate-levels)
- [Step 4: Choose an oracle for each](#step-4-choose-an-oracle-for-each)
- [Step 5: Sweep the coverage taxonomy](#step-5-sweep-the-coverage-taxonomy)
- [Step 6: Record testability blockers](#step-6-record-testability-blockers)
- [Step 7: Declare non-goals](#step-7-declare-non-goals)
- [Suite health rules](#suite-health-rules)
- [Deliverable template](#deliverable-template)

## Pick the entry move

Three starting points, and they diverge immediately. MUST identify which one before step 1.

| Starting point          | First move                                                                | Failure mode to avoid                                               |
| ----------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| A change or feature     | Diff the behavior, not the code: what can a user now do, or no longer do? | Planning coverage for the whole subsystem the diff touched          |
| A bug                   | Ask what class the bug belongs to, then plan for the class                | One regression test for the one reported input                      |
| A system or legacy tree | Find the highest-risk seam that is testable today; plan outward from it   | A grand plan nobody executes, or a rewrite disguised as a test plan |

For a legacy tree with no tests, characterization tests come first: pin current behavior as-is, bugs included,
so a refactor has a baseline. MUST label them as characterization, not as specifications - they encode what
the system does, and somebody will later mistake that for what it should do.

## Step 1: Name the behaviors, not the units

Write each item as an observable behavior with a subject and an outcome: "an expired token is rejected with
401", not "AuthService.validate". A plan built from module names tests the structure that exists rather than
the promises the system makes, and it dies at the next refactor.

For each behavior, record the **consequence of it being wrong**. That sentence is the input to step 2 and the
justification for every cost the plan asks for. Behaviors whose failure costs nothing are where a plan gets to
say "no test".

Sources, in order: the acceptance criteria or issue, the public interface (API routes, CLI surface, exported
functions, events, schemas), the error paths that interface admits to, and the incident or bug history.

## Step 2: Rank by risk

Risk = likelihood of being wrong x blast radius when it is. Neither factor alone ranks anything.

Likelihood rises with: recent change, high churn, concurrency, weak types at the boundary, hand-rolled
parsing, sequencing and retries, cache invalidation, anything with a clock or a timezone, and code no current
author wrote.

Blast radius rises with: data loss or corruption, security and authorization, money, silent wrongness (the
worst class - it has no alarm), cross-tenant leakage, irreversibility, and how many downstream consumers trust
the output.

Rank the list and put the ranking in the deliverable. A ranked list survives a budget cut; an unranked one
gets truncated arbitrarily at whatever point the team ran out of time.

## Step 3: Allocate levels

For each behavior, the deciding question is: **what would this level catch that the cheaper level below it
cannot?** No answer means do not test it there.

| Level                 | Buys                                                             | Costs                                 | Use when                                                                    |
| --------------------- | ---------------------------------------------------------------- | ------------------------------------- | --------------------------------------------------------------------------- |
| Unit                  | Fast, precise localization, exhaustive input coverage            | Proves nothing about wiring           | Logic with real branching, algorithms, parsers, calculations                |
| Integration           | Real collaborator behavior - schema, transaction, serialization  | Slower, needs setup                   | Anything crossing a persistence, network, or process boundary               |
| Contract              | Both sides of an interface stay compatible, tested independently | Needs a shared artifact               | Services or teams that deploy separately                                    |
| End-to-end            | The assembled system actually starts and serves                  | Slowest, flakiest, worst localization | A handful of critical user journeys, and the smoke path                     |
| Property-based        | Whole input classes at once; finds inputs nobody imagined        | Needs an invariant worth stating      | Round-trips, encoders, sorting, idempotency, anything with an algebraic law |
| Manual or exploratory | Judgment, aesthetics, and the unknown-unknowns                   | Not repeatable, not a gate            | Usability, visual output, first pass on a novel area                        |

**Size is a second axis, and it is not the same question as level.** Level asks how much of the system is
exercised; size asks what the test is allowed to *touch* - small (one process, no network, no disk, no
sleeping), medium (one machine: localhost, a temp dir, a local database), large (several machines or a real
external system). The two are independent: an integration test can be small, a unit test that reaches a shared
fixture on disk is not. Record both, because size - not level - decides whether a test can run in a fast
hermetic parallel shard, and it is the axis a slow suite is usually failing on. (The small/medium/large
framing is from *Software Engineering at Google*, ch. 11.)

Rules that resolve most arguments:

- MUST NOT mock what you are trying to prove. A test whose collaborators are all mocks proves the mocks agree
  with each other.
- Mock at the boundary you do not own (third-party network, payment provider, clock), not at the boundary you
  do.
- The same behavior tested at three levels is one behavior with two maintenance liabilities. Choose the
  cheapest level that can actually fail for the right reason.
- When a behavior is only reachable end-to-end, that is a testability finding (step 6), not a level decision.

### Making the exploratory row actionable

"Manual or exploratory" in the table above is a real allocation, not a shrug - but it only produces findings
if it is chartered. An uncharted session is browsing, and it reports as "looked fine".

A charter is four lines, written before the session starts:

- **Explore** the area, feature, or seam.
- **With** the data, roles, tools, or conditions to use.
- **To discover** the class of problem being hunted: crashes, wrong output, confusing states, missing
  feedback, unhandled input.
- **Timebox** decided up front, never when interest runs out.

The session's output is notes, NEVER a verdict: what was covered, what was NOT reached, bugs found, questions
raised. MUST NOT report a charter as a gate - it is not repeatable, so nothing regressed when it stops
passing, and treating it as one launders judgment into evidence.

Charter rather than skip, because exploratory testing is the only row in the table that can find a problem
nobody thought to specify. Every other row confirms or denies something already named in step 1. A plan that
allocates no exploratory time has silently assumed its own behavior list is complete - the same failure as
omitting non-goals, one level up.

## Step 4: Choose an oracle for each

The oracle is how a wrong answer is recognized. Naming scenarios without oracles is the most common way a plan
looks complete and produces assertion-free tests.

| Oracle               | Shape                                                      | Fits                                                                                   |
| -------------------- | ---------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Exact value          | `f(x) == expected`                                         | Small, stable, meaningful outputs                                                      |
| Invariant / property | A law that holds for all inputs                            | Round-trips, ordering, conservation, idempotency                                       |
| Differential         | Compare against a reference or the previous implementation | Rewrites, ports, optimizations                                                         |
| Metamorphic          | A known relation between two runs' outputs                 | No expected value exists, but scaling or reordering the input has a predictable effect |
| Golden file          | Diff against a reviewed, committed artifact                | Large structured output; MUST be human-reviewable or it is a rubber stamp              |
| Error contract       | Specific type, code, and message shape                     | Every failure path worth naming                                                        |

An oracle that only asserts "did not throw" is not an oracle, and neither is a status code. `200` says the
request was handled, never that the payload is right - pair it with a shape check (schema, contract, or
named-field assertions) or the response can change past recognition without failing a test.

## Step 5: Sweep the coverage taxonomy

MUST walk this list per high-risk behavior rather than recalling edge cases freely. Recall reliably misses
whole categories; a sweep makes the misses deliberate. Most entries will not apply - say so and move on.

- **Equivalence classes**: partition the input domain, one representative per class.
- **Boundaries**: at, either side of, and beyond every limit - 0, 1, n, n+1, empty, single, max, overflow.
- **Null and absence**: null, undefined, empty string, empty collection, missing field, explicit null vs
  absent.
- **Type and shape**: wrong type, extra fields, unicode, very long, control characters, malformed encoding.
- **State transitions**: legal transitions, illegal ones, and re-entering a state. Draw the machine if there
  is one.
- **Decision tables**: for combinatorial rules, enumerate the condition combinations rather than sampling
  them.
- **Pairwise**: when parameters explode combinatorially, cover all pairs instead of all tuples.
- **Error and exception paths**: every `raise`/`throw`/error return the interface admits, triggered
  deliberately.
- **Failure injection**: dependency down, slow, returning garbage, half-written response, disk full, OOM.
- **Retry and idempotency**: the same request twice, a retry after partial success, at-least-once delivery.
- **Concurrency and ordering**: two writers, out-of-order arrival, lost update, deadlock, races on shared
  state.
- **Time**: timezone, DST, leap day, clock skew, expiry exactly at the boundary, timeout, long-running.
- **Persistence and migration**: forward migration, rollback, old rows written by the previous version.
- **Compatibility**: old client against new server and the reverse; a serialized artifact from the prior
  release.
- **Authorization**: each role against each operation, plus the cross-tenant case. Absence of a test here is a
  vulnerability, not a gap.
- **Resource limits**: pagination past the end, large payload, unbounded growth, connection-pool exhaustion.
- **Observability**: does a failure produce a diagnosable signal? Untestable silence is a finding.

## Step 6: Record testability blockers

When a behavior cannot be tested at the level its risk demands, that is a finding for the implementation lane
\- MUST report it, MUST NOT fix it here. Name the blocker, the change that would unblock it, and who owns it.

Usual suspects: a clock read inline instead of injected, randomness with no seed, global or static mutable
state, network or filesystem calls buried in a constructor, no seam between decision and side effect, a
private method carrying the whole risk, and output that exists only as a log line.

## Step 7: Declare non-goals

Every plan leaves things uncovered. A plan that does not say which one is claiming total coverage by omission,
and the reader will believe it.

For each: what is not tested, why (cost, low risk, covered elsewhere, blocked), and what would change the
answer. "Not tested" with a reason is a decision; "not tested" silently is a hole.

## Suite health rules

Carry these into the plan, because they decide whether the suite is still trusted a year later.

- A flaky test is a failing test. Quarantine with a deadline and an owner, or delete it. Retry-until-green
  destroys the signal the suite exists for.
- Ask what the suite would CATCH, not what it covers. Break the production code deliberately - flip a
  comparison, drop a guard, return a constant - and see whether anything goes red. A mutation nothing kills is
  the finding, and it is the only evidence that separates tests which assert from tests which merely execute.
  Mutation tooling (Stryker, PIT, mutmut, cargo-mutants) automates the sweep; by hand, three deliberate breaks
  in the riskiest function tell you most of what a coverage report will not.
- Synchronize on the condition, never on the clock. A fixed sleep is simultaneously too long on the machine
  that is fast and too short on the one that is loaded, and it is the largest single source of flake. Wait for
  the state you actually need - the element, the row, the log line, the exit.
- Bind to the contract, not to the incidental representation: roles and labels over CSS paths, documented
  fields over positional index, exit codes over stdout formatting. A test that breaks on a rename no user
  could observe is coupled to the wrong thing, and its failures teach the team to ignore failures.
- Tests MUST be order-independent and self-seeding. Shared mutable fixtures are the usual cause when they are
  not.
- Run the suite where it will be judged. CI differs from a developer machine in fonts, rendering, parallelism,
  resource contention and network path, so a suite green only locally has not really been run. Where the
  environments must differ, make the difference explicit and reviewable rather than incidental.
- Every test names the behavior it protects in its title. `test_case_3` is a test nobody will dare delete or
  fix.
- New coverage arrives with the change that needs it. "Tests in a follow-up PR" is the plan's most common lie.

## Deliverable template

```markdown
## Scope
<what this covers, and the entry move used>

## Ranked risks
| # | Behavior | If wrong | Likelihood | Blast radius |
|---|---|---|---|---|

## Coverage plan
| Behavior | Level | Size | Oracle | Taxonomy categories applied | Exists? |
|---|---|---|---|---|---|

## Existing coverage
<files inspected, what they already prove, what they leave open>

## Testability blockers
| Blocker | Unblocking change | Owner |
|---|---|---|

## Exploratory charters   <!-- omit this section when no exploratory time is allocated -->
| Explore | With | To discover | Timebox |
|---|---|---|---|

## Non-goals
| Not tested | Why | What would change this |
|---|---|---|

## Open questions
<each with: the answer's effect on the plan>

Verdict: STRATEGY
```
