# Behavioral Evaluation

Behavioral evaluation asks whether the skill improves agent behavior for its declared job. It complements
static review; it does not convert subjective document traits into objective numbers.

## Design Cases

For each case record:

- a realistic user request and required inputs;
- the behavior under test;
- observable success conditions;
- consequential edge cases or failure paths;
- the agent, model, client, and relevant environment;
- the comparison baseline, when used; and
- outputs, execution evidence, and result.

Start with a small set that spans the important behavior. Add cases when failures reveal a distinct boundary.
Preserve cases that catch likely regressions; do not grow a suite merely to reach a quota.

### Discovery

Use positive requests where the skill should activate, near-miss requests where similar language should not
activate it, and ambiguous requests where activation or clarification depends on context. Vary phrasing and
realism without stuffing prompts with the description's exact words.

**Prefer a load signal, but do not assume one exists.** Some clients expose no observable trace when a skill
activates: measured on Claude Code 2.1.239 on 2026-09-03, print mode emitted no skill tool call, no read of
`SKILL.md`, and nothing in the debug log beyond the skills directory being scanned — including under an
explicit `/skill-name` invocation, because the content is injected server-side. Where that holds, grade
activation from behavior instead. NEVER report "the skill did not load" when what was observed is "no signal
was available".

### Grading Activation Without a Load Signal

Build a fixture the skill's rules bite on, then check whether the output shows decisions the agent would not
otherwise make.

- **Choose a fixture that forces the skill's distinctive choice.** A naming skill needs code carrying a bad
  name already; a migration skill needs a schema to migrate. A fixture with nothing to correct cannot
  distinguish an activated skill from an idle one.
- **Grade on several independent fingerprints and set a threshold.** A single marker turns one phrasing
  choice into the whole measurement.
- **Validate the grader against a known positive before trusting any negative.** Invoke the skill explicitly,
  grade that output, and confirm the grader fires. A detector that never fires positive reports every run as
  a failure. This step is what separates `0 of 5` as evidence from `0 of 5` as a broken harness.
- **Prefer evidence that the anti-pattern appeared** over evidence that a fingerprint was absent. An agent
  that produced exactly what the skill forbids is a far stronger negative than output that merely lacked the
  skill's vocabulary.

**Vary always-loaded context with an instruction file inside the fixture directory** rather than editing the
user's real configuration. Where a client discovers project-level instructions, that gives a controlled
condition touching nothing durable. Disabling global instructions wholesale may also disable the client's
authentication path, so verify that before depending on it.

When no phrasing reaches the content at all, the finding is about the skill's form rather than its
description; `skill-forge`'s job-establishment step covers what to do instead.

### Execution

Cover representative success, consequential boundaries, expected failures, and recovery paths. Assert outcomes
rather than exact prose or heading names. Use deterministic checks for files, schemas, calculations, and other
mechanical facts; use human or blinded model judgment for qualities that cannot be reduced reliably.

Read execution traces when available. They can expose ignored instructions, unnecessary steps, repeated
reinvention, premature completion, or expensive branches that a final artifact hides.

## Skill-Review Regression Cases

Run the exact discovery cases in [../evals/activation.json](../evals/activation.json) through a client where
the agent chooses among registered skills. Do not supply the `skill-review` path or tell the agent to load it.
Use the declared positive, near-miss, and ambiguous cases, and observe whether the client loads `SKILL.md`.

Run the cases in [../evals/review-quality.json](../evals/review-quality.json) in clean contexts with
`skill-review` supplied explicitly. Use the package fixtures under `../evals/fixtures/`. A correct verdict
alone does not pass: require the finding, confidence, evidence, consequence, repair, and validation declared
for the case.

For every execution, record the client, model, date, baseline, raw result, and trace or output location. Use
the pre-`4229cbd` revision declared in the quality-case file when measuring whether the scope and discovery
changes improved review behavior. Keep results in a dated repository evaluation record rather than replacing
the reusable case definitions with one run's output.

## Choose a Baseline

Use the same request and environment for each comparison:

- **No skill** measures whether the guidance adds value beyond the model's default behavior.
- **Previous version** measures whether a revision improves behavior or introduces regressions.
- **Alternative design** compares materially different instruction strategies.

A baseline is valuable when the decision concerns added value. It is optional when a focused regression case
already answers the question or the comparison cost would exceed its usefulness.

## Useful Measurements

Choose measurements from the decision being made:

- task successes and failures by case;
- assertion passes and failures with concrete evidence;
- trigger recall, precision, false-positive rate, and false-negative rate;
- regression count or rate against the prior version;
- token and elapsed-time deltas against the same baseline;
- retries, tool failures, or unnecessary actions found in traces;
- results by client or model class where those environments materially differ; and
- human preference or usability findings for irreducibly qualitative outcomes.

Report raw counts with rates, especially for small samples. Repeated runs are needed before variability
statistics such as standard deviation become meaningful. Do not imply statistical confidence from a few
nondeterministic runs.

Remove or revise assertions that pass regardless of configuration, always fail for reasons outside the skill,
encode one preferred wording, or cannot be verified from the available output.

## Interpret Results

Separate three questions:

1. **Effect:** Did behavior improve on the intended outcome?
2. **Cost:** What extra context, tokens, time, tools, or maintenance did the improvement require?
3. **Coverage:** Which requests, environments, and model classes were and were not exercised?

Aggregate rates can hide one severe failure. Inspect per-case results and weight consequential boundaries by
their actual impact rather than their share of the test set.

Inconsistent results can indicate ambiguous instructions, model variance, a flaky environment, or an unstable
grader. Diagnose the cause before adding more rules. Generalize repairs from the underlying failure; do not
patch the skill with phrases copied from one test prompt.

## Numeric Ratings

Do not produce a universal quality total. Unlike skills can require different behavior, risk controls, and
evidence, so fixed weights create false comparability and reward rubric-shaped documents.

When the user needs a number for a stated decision:

1. Define criteria from that skill's contract.
2. Keep specification, policy, provenance, and safety gates outside the number.
3. Prefer observable case results to document proxies.
4. Explain any weighting and label judgment-based weights as subjective.
5. Show raw observations and coverage beside the result.

The number summarizes the chosen decision model; it is not an intrinsic property of the skill.
