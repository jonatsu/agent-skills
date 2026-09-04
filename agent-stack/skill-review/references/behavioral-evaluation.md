# Full Behavioral Evaluation

Use a full evaluation to determine whether a skill improves agent behavior for its declared job. This process
is runner-neutral. Client commands and event formats belong in verified adapters.

Review lite remains the default when the user defers model cost. Only a full evaluation can support `ready`.

## Establish Authority and the Run Ceiling

Before setup, state:

- the decision this evaluation must support;
- candidate and baseline revisions;
- selected clients, models, cases, and repetitions;
- expected time, model allowance, and marginal cost;
- allowed writes, prohibited side effects, and sensitive inputs; and
- the stop condition and maximum authorized run count.

Obtain user approval for costs or side effects not already authorized. Do not expand the matrix merely because
more combinations exist. Stop at the approved ceiling and preserve partial evidence.

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

Start with the smallest set that spans the important behavior. Add cases when failures expose a distinct
boundary. Preserve useful cases as regression fixtures instead of growing the suite to meet a quota.

Keep reusable fixtures in the package only when deployment is intentional. Keep run outputs and traces outside
the package.

## Preflight Without a Model

Preflight every selected client and case before the first model call:

1. Resolve candidate, baseline, and fixtures by identity and source revision.
2. Run specification and repository validators.
3. Run every advertised fixture command and its meaningful failure path.
4. Create a fresh workspace containing only declared initial inputs.
5. Keep future turns, expected outputs, and grading material outside that workspace.
6. Check client version and runtime help for every selected flag.
7. Verify candidate reads, allowed writes, output capture, trace capture, and continuation behavior.
8. Record the exact command after shell parsing.
9. Confirm the approved run ceiling and the mechanism that enforces it.

A preflight failure consumes no behavioral repetition. Repair it, recreate the workspace, and preflight again.

## Use Client Adapters

For each client, keep a small adapter that owns:

- candidate and baseline delivery;
- automatic discovery or explicit invocation;
- tool and permission configuration;
- non-interactive execution and continuation;
- output, event, trace, timing, token, and cost extraction; and
- cleanup of temporary client state.

Do not put one client's paths, commands, tool names, or event schema into the shared case contract. Verify an
adapter against the installed client version before trusting its results.

Deployment proves file placement only. It does not prove discovery, loading, or behavior.

## Isolate Comparison Arms

Use a new session and workspace for each independent case and arm. Keep prompts, inputs, tools, permissions,
settings, and output locations equivalent across arms.

Choose the baseline from the decision:

- **No skill** measures value beyond default model behavior.
- **Previous version** measures improvement and regression.
- **Alternative design** compares materially different instruction strategies.

A baseline is optional when a focused regression case already answers the decision. Record why an omitted
baseline adds too little value for its cost.

For multi-turn cases, expose each turn only when sent. Inspect artifacts and permissions before continuation.
Recheck the restored sandbox and working directory because clients may change them on resume.

## Evaluate Discovery

Use realistic positive requests, difficult near-miss negatives, and ambiguous requests. Do not supply the
candidate path or tell the agent to load it during automatic-selection cases.

Prefer an observable load signal, but verify that the client exposes one. When no signal exists, grade several
distinctive behavioral fingerprints. Validate that grader against a known explicit-invocation positive before
trusting a negative result.

Evidence that the forbidden behavior occurred is stronger than the absence of preferred vocabulary. Report
"no observable load signal" instead of claiming non-activation when the client hides selection.

Keep training prompts separate from held-out prompts during repeated description optimization. Select a
revision from held-out behavior and finish with fresh cases. Do not copy individual prompt wording into the
description to make a fixture pass.

## Evaluate Execution

Cover representative success, consequential boundaries, expected failures, and recovery. Assert outcomes
instead of exact prose or headings.

Inspect both the final artifact and the execution trace. A plausible result can hide skipped context,
unnecessary questions, repeated work, tool failures, premature completion, or unauthorized writes.

Record each started model run immediately:

- date, source revision, client, version, model, and relevant settings;
- exact prompt and command;
- session or thread identifier;
- raw output, artifacts, trace, and filesystem changes;
- duration, token use, marginal cost, and subscription impact;
- assertion results and human feedback; and
- candidate, fixture, harness, dependency, permission, contaminated, inconclusive, or pass/fail result.

Persist event streams when the trace is evidence. A final-answer file does not replace the trajectory.

## Grade the Right Layer

Use deterministic checks for paths, allowed writes, schemas, calculations, and parsed formats. Use human or
independent model judgment for coherence, usefulness, unstated decisions, and other irreducible qualities.

For every assertion, record pass or fail with concrete evidence. Reject assertions that:

- pass regardless of the comparison arm;
- fail because of fixture or harness defects;
- encode one preferred wording instead of behavior; or
- cannot be verified from the captured evidence.

When independence matters, compare outputs blind before causal analysis. Hide arm identity from the comparer.
Unblind only after the preference is recorded, then inspect the traces and skill differences that may explain
the result. A subagent is optional; a separate clean context can provide the same role boundary.

Present important artifacts to the user for qualitative review. A browser interface is optional. Conversation,
downloadable files, or another accessible artifact viewer are valid when they preserve the evidence.

## Interpret Results

Separate four questions:

1. **Effect:** Did the skill improve the intended outcome?
2. **Cost:** What extra context, tokens, time, tools, or maintenance did it require?
3. **Reliability:** Did results vary across repetitions, clients, models, or graders?
4. **Coverage:** Which requests, environments, and model classes remain untested?

Inspect individual cases before aggregate results. One severe authority or safety failure cannot be canceled by
many easy passes.

Report raw counts for small samples. Do not describe one run as a rate or use variance statistics without
enough repetitions to make them meaningful.

Diagnose inconsistent results before adding instructions. The cause may be ambiguous guidance, model variance,
a flaky environment, a weak grader, or an invalid fixture.

## Repair and Stop

Generalize from the failure, not the fixture wording. Add or strengthen the failing outcome before editing the
skill. Make the smallest repair, then rerun the failure and its nearest passing boundary.

Stop when:

- the approved ceiling is reached;
- required access or authority is unavailable;
- the user accepts the evidence and remaining risks;
- every material case passes with adequate coverage; or
- further iterations produce no meaningful improvement.

Do not call unchanged external state a candidate failure. Preserve partial evidence and name the smallest next
run that could change the decision.

## Skill-Review Regression Cases

Run [../evals/activation.json](../evals/activation.json) through each selected client's actual discovery
mechanism. Do not provide the `skill-review` path in automatic-selection arms.

Run [../evals/review-quality.json](../evals/review-quality.json) in clean contexts with the candidate supplied
explicitly. Use its package fixtures. A correct verdict alone does not pass. Require the declared finding,
evidence, consequence, repair, and validation.

The candidate skill is the object under test. Baselines, graders, and the main synthesis must not use
`skill-review` or `skill-forge` as guidance when evaluating these two subject skills.

Keep run results in a dated repository record. Do not replace reusable case definitions with one run's output.

## Numeric Ratings

Do not produce a universal quality total. Skills require different behavior, risk controls, and evidence.

When the user needs a number for a stated decision:

1. Define criteria from that skill's contract.
2. Keep validity, provenance, and safety gates outside the number.
3. Prefer observed case results to document proxies.
4. Explain weights and label judgment-based weights as subjective.
5. Show raw observations and coverage beside the result.

The number summarizes the chosen decision model. It is not an intrinsic property of the skill.
