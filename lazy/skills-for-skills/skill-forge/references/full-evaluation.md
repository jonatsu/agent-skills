# Full Behavioral Evaluation

Determine whether a skill improves agent behavior for its declared job through controlled runs. The process is
runner-neutral; client commands and event formats belong in verified adapters.

## Contents

- Establish authority and the run ceiling
- Design cases from the skill contract
- Keep fixtures inert
- Preflight the harness
- Use client adapters
- Isolate comparison arms
- Evaluate discovery
- Evaluate execution
- Grade the right layer
- Interpret results
- Repair and stop
- Regression cases for this skill

## Establish Authority and the Run Ceiling

Before setup, state:

- the decision this evaluation must support;
- candidate and baseline revisions;
- selected clients, models, cases, and repetitions;
- expected time, model allowance, and marginal cost;
- allowed writes, prohibited side effects, and sensitive inputs; and
- the stop condition and maximum authorized run count.

Obtain the user's approval for costs or side effects not already authorized. Size the matrix to the decision
rather than to the combinations available. Stop at the approved ceiling and preserve partial evidence.

## Design Cases From the Skill Contract

For each case record:

- a stable case ID and realistic user request;
- required inputs and initial workspace contents;
- the behavior under test;
- observable success conditions;
- consequential edge cases and failure paths;
- allowed writes and prohibited side effects;
- conversation turns and when each becomes visible; and
- output, trace, usage, and cleanup locations.

Start with the smallest set that spans the important behavior. Add a case when a failure exposes a distinct
boundary, and keep useful cases as regression fixtures rather than growing the suite to a quota.

**Add pressure scenarios when the skill's value is compliance.** A skill that enforces a rule an agent is
tempted to skip has not been tested until the temptation is present. Write a realistic request that stacks
competing incentives, such as a deadline, sunk effort, or an authority figure urging the shortcut, and end it
in a forced choice between the rule and the shortcut. A skill that holds only when nothing pushes against it
fails in exactly the situation it exists for.

When the subject is itself a reviewing skill, test whether the reviewer identifies the supported defect, cites
relevant evidence, explains its consequence, and proposes a proportionate repair. Include valid alternatives
the reviewer could wrongly flag. A correct verdict alone is insufficient, and an unsupported finding is a
review failure.

## Keep Fixtures Inert

Fixture skills stay out of normal skill discovery, because a client that catalogs one offers it as a real
skill. Ship each as a `SKILL.md.fixture` template or outside deployed discovery paths. Materialize it as
`SKILL.md` only in a fresh, isolated workspace, with the case's declared resources at their original relative
paths, and leave source and deployed templates unchanged. Check the intended clients for accidental fixture
exposure, and report a client whose catalog cannot be inspected as a verification limit. Keep expected outcomes
and grading material out of the candidate workspace unless the case supplies them as task evidence.

## Preflight the Harness

Preflight every selected client and case before the first model call:

1. Resolve candidate, baseline, and fixtures by identity and source revision.
2. Materialize required fixture templates in isolation, then run the rubric's hard-gate validators.
3. Run every advertised fixture command and its meaningful failure path.
4. Create a fresh workspace containing only declared initial inputs.
5. Keep future turns, expected outputs, and grading material outside that workspace.
6. Check the client version and runtime help for every selected flag.
7. Verify candidate reads, allowed writes, output capture, trace capture, and continuation behavior.
8. Record the exact command after shell parsing.
9. Confirm the approved run ceiling and the mechanism that enforces it.

A preflight failure consumes no behavioral repetition. Repair it, recreate the workspace, and preflight again.

## Use Client Adapters

Give each client a small adapter that owns:

- candidate and baseline delivery;
- automatic discovery or explicit invocation;
- tool and permission configuration;
- non-interactive execution and continuation;
- output, event, trace, timing, token, and cost extraction; and
- cleanup of temporary client state.

Keep one client's paths, commands, tool names, and event schema out of the shared case contract. Verify an
adapter against the installed client version before trusting its results. Parallel subagents are one client's
way to run arms concurrently; a separate clean session serves the same role elsewhere.

Deployment proves file placement only, not discovery, loading, or behavior.

## Isolate Comparison Arms

Use a new session and workspace for each independent case and arm. Keep prompts, inputs, tools, permissions,
settings, and output locations equivalent across arms.

Choose the baseline from the decision:

- **No skill** measures value beyond default model behavior.
- **Previous version** measures improvement and regression.
- **Alternative design** compares materially different instruction strategies.

A baseline is optional when a focused regression case already answers the decision; record why an omitted
baseline adds too little value for its cost.

For multi-turn cases, expose each turn only when sent. Inspect artifacts and permissions before continuation,
and recheck the restored sandbox and working directory, because clients may change them on resume.

## Evaluate Discovery

Run the discovery cases prepared under [testing-guide.md](testing-guide.md). In automatic-selection cases,
withhold the candidate path and any instruction to load it.

Prefer an observable load signal, after verifying that the client exposes one. When none exists, grade several
distinctive behavioral fingerprints, and validate that grader against a known explicit-invocation positive
before trusting a negative result. Evidence that the forbidden behavior occurred is stronger than the absence
of preferred vocabulary. Report "no observable load signal" rather than claiming non-activation when the
client hides selection.

The `skill-descriptions-and-triggers` skill owns trigger-rate measurement and description optimization,
including repetitions, thresholds, and held-out queries.

## Evaluate Execution

Cover representative success, consequential boundaries, expected failures, and recovery. Assert outcomes rather
than exact prose or headings.

Inspect both the final artifact and the execution trace. A plausible result can hide skipped context,
unnecessary questions, repeated work, tool failures, premature completion, or unauthorized writes. When several
runs each write the same helper, record it as evidence for bundling a script under
[pro-agent.md](pro-agent.md).

Record each started model run immediately:

- date, source revision, client, version, model, and relevant settings;
- exact prompt and command;
- session or thread identifier;
- raw output, artifacts, trace, and filesystem changes;
- duration, token use, marginal cost, and subscription impact;
- assertion results and human feedback; and
- candidate, fixture, harness, dependency, permission, contaminated, inconclusive, or pass/fail result.

Persist event streams when the trace is evidence; a final-answer file does not replace the trajectory.

## Grade the Right Layer

Use deterministic checks for paths, allowed writes, schemas, calculations, and parsed formats. Use human or
independent model judgment for coherence, usefulness, unstated decisions, and other irreducible qualities.

Grade strictly:

- **Genuine completion passes; surface compliance fails.** An output with the asserted heading, keyword, or
  file but without the underlying task done is a fail.
- **The assertion carries the burden of proof.** When the captured evidence does not show the pass, record a
  fail.
- **Check the output's own claims.** List the facts it states, the steps it says it took, and the checks it
  says passed, then verify each against the trace and artifacts. An unverified self-claim is not evidence.

Record pass or fail with concrete evidence for every assertion. Reject an assertion that:

- passes regardless of the comparison arm;
- fails because of fixture or harness defects;
- encodes one preferred wording instead of behavior; or
- cannot be verified from the captured evidence.

When independence matters, compare outputs blind before causal analysis. Hide arm identity from the comparer,
unblind only after the preference is recorded, and then inspect the traces and skill differences that may
explain the result.

Present important artifacts to the user for qualitative review through any channel that preserves the
evidence, such as the conversation, downloadable files, or a viewer.

## Interpret Results

Separate four questions:

1. **Effect:** did the skill improve the intended outcome?
2. **Cost:** what extra context, tokens, time, tools, or maintenance did it require?
3. **Reliability:** did results vary across repetitions, clients, models, or graders?
4. **Coverage:** which requests, environments, and model classes remain untested?

Inspect individual cases before aggregates. One severe authority or safety failure outweighs any number of easy
passes.

Report raw counts for small samples. One run is a count, not a rate, and variance statistics need enough
repetitions to mean something.

Diagnose inconsistent results before adding instructions. The cause may be ambiguous guidance, model variance,
a flaky environment, a weak grader, or an invalid fixture. Asking the agent afterward how the skill could have
been clearer yields a hypothesis for the next revision, not evidence; a rerun confirms or refutes it.

## Repair and Stop

Generalize from the failure, not the fixture wording. Add or strengthen the failing outcome before editing the
skill, make the smallest repair, and rerun the failure with its nearest passing boundary.

Stop when:

- the approved ceiling is reached;
- required access or authority is unavailable;
- the user accepts the evidence and remaining risks;
- every material case passes with adequate coverage; or
- further iterations produce no meaningful improvement.

Unchanged external state is not a candidate failure. Preserve partial evidence and name the smallest next run
that could change the decision.

## Regression Cases for This Skill

When the subject is `skill-forge` itself, baselines, graders, and the main synthesis work without
`skill-forge` as guidance, because a grader following the candidate's own rules cannot judge them.

- Run [../evals/activation.json](../evals/activation.json) through each selected client's actual discovery
  mechanism, without supplying the skill path.
- Run [../evals/behavior.json](../evals/behavior.json) for authoring mode and
  [../evals/review-quality.json](../evals/review-quality.json) for review mode in clean contexts, with the
  candidate supplied explicitly. `fixture` paths are relative to the case file; materialize them as
  "Keep fixtures inert" describes.

Require each case's declared outcomes or assertions. Preserve existing cases, and add one where revised
criteria introduce a distinct boundary. Keep run results in a dated record outside the package, and keep
reusable case definitions separate from any one run's output.
