# Evaluation Harness

Use this reference to make a prompt evaluation reproducible before spending a model run.

## Fixture Contract

Each case should identify:

- case ID and behavior under test;
- exact user input and required context;
- observable success conditions;
- consequential failure paths;
- initial workspace contents;
- allowed writes and prohibited side effects;
- conversation turns and when each becomes visible;
- comparison baseline;
- clients and models required by the decision; and
- output, trace, usage, and cleanup locations.

Keep reusable fixtures inside the package only when deploying them is intentional. Keep run-specific outputs and traces
outside the package so deployment does not grow with every execution.

## Preflight Without a Model

Before the first model call:

1. Resolve the candidate and fixture by identity. Avoid author-machine paths in reusable definitions.
2. Create a fresh workspace and copy only the declared fixture contents.
3. Confirm future conversation turns, expected outputs, and grading material are outside the workspace.
4. Run every advertised fixture command and exercise its meaningful failure path.
5. Check client version and runtime help for every selected flag.
6. Verify candidate reads, workspace writes, output files, trace files, and session persistence with the narrowest
   permissions the case needs.
7. Record the exact command after shell parsing, not only a friendly reconstruction.
8. Confirm the run ceiling and the stop condition that enforces it.

A preflight failure consumes no behavioral repetition. Repair it, create a fresh workspace, and start the case again.

## Context Isolation

Use a new session for every independent case and comparison arm. Keep inputs, tools, and environment equivalent across
arms. Do not reuse a workspace whose earlier run wrote state unless continuation is the behavior under test.

For multi-turn cases:

1. Send turn 1 with no later-turn files present.
2. Inspect output, trace, and filesystem assertions before continuing.
3. Supply turn 2 through the client's continuation mechanism.
4. Recheck permissions because some clients restore a different sandbox policy on resume.
5. Attribute each artifact and token total to the turn that produced it.

## Capture Contract

Record for every started model run:

- date and source revision;
- client, version, model, and relevant settings;
- exact prompt and command;
- session or thread identifier;
- raw final output and trace location;
- filesystem changes;
- duration and token usage;
- marginal monetary cost and subscription allowance impact;
- assertion results; and
- classification as pass, prompt failure, harness failure, fixture failure, or inconclusive.

Use persistent sessions when the trace is evidence. If an ephemeral mode is necessary, capture its event stream to a
durable location during the run. A final-answer file does not replace a trajectory.

## Grade the Right Layer

Mechanical assertions fit file count, path, schema, parsed format, and allowed-write checks. Human review fits coherence,
usefulness, unstated decisions, and whether a repair preserves intent. Inspect both individual assertions and aggregate
results; a high pass count cannot cancel one severe authority or safety failure.

Do not count:

- argument-parser rejection as a model run;
- a permission denial as prompt behavior when the fixture required that access;
- an unavailable dependency as model failure;
- a leaked future-turn answer as a valid pass; or
- a result against a changed harness as directly comparable without rerunning its baseline.

## Scale by Decision

Start with the failing case and one neighboring boundary. Add a no-prompt or prior-version baseline when the decision is
whether the prompt adds value. Add clients when portability is material. Add repetitions when activation or output varies
enough to change the decision.

Report raw counts for small samples. Avoid averages, rates, and confidence language that a handful of nondeterministic
runs cannot support.
