# Author-Side Skill Testing and Review Lite

Test whether the draft executes its intended paths before independent review. Then perform review lite by
default. These checks support provisional use but do not establish comparative value.

## Define the Cases

Start with the smallest set that exercises the draft's important decisions. Record:

- a realistic request and required inputs;
- the behavior under test;
- observable success conditions;
- consequential failure paths;
- the target client and relevant environment; and
- the output, result, and known limits.

A focused update usually needs the changed behavior and its nearest failure boundary. Preserve cases that an
independent review can reuse.

## Preflight Without a Model

Run this preflight before review lite. Repeat it before a later model-based test when the package or fixture changed:

1. Run the specification and applicable policy validators.
2. Confirm the candidate and every promised resource are readable.
3. Run advertised commands and representative script failure paths.
4. Use safe temporary inputs and outputs for stateful script checks.

A preflight failure is not skill behavior. Repair the package or fixture before starting the test.

## Walk Cases Heuristically

Trace each representative request through the package without making a model call. Check whether the main file
routes every required decision and resource before its point of use. Inspect outcomes instead of exact wording
or heading names.

Use deterministic checks for files, schemas, calculations, and other mechanical facts. Use human inspection
for coherence, usefulness, unstated decisions, and unforeseen defects.

If earlier real use produced a trace, inspect it. A final artifact can hide ignored instructions, unnecessary
work, tool failures, or unauthorized writes.

## Prepare Discovery Cases When Routing Changed

Prepare cases for a client where the agent chooses among registered skills. The later full evaluation must not
provide the target skill path or instruct the agent to load it. Prefer an observable load signal when the
client exposes one.

Use realistic positive requests, close negative requests, and ambiguous cases. Positive cases should include
requests stated by outcome without the skill's exact terminology. Negative cases should share nearby terms or
artifacts while requiring another capability.

Some clients expose no trustworthy load signal. Record that limitation for independent behavioral review. Do
not infer non-activation from the final answer alone.

## Review Lite and Handoff

### Perform Review Lite by Default

Review the settled package heuristically without starting subagents or model evaluations. Inspect:

- whether one coherent job owns every instruction and resource;
- whether the description covers intended requests and excludes nearby work;
- whether instructions, examples, scripts, references, and assets agree;
- whether format, runtime, and client claims match available evidence;
- whether provenance, licensing, safety, and authority boundaries are complete; and
- whether the package and author-side checks satisfy their stated completion conditions.

Report hard or material defects and leave the skill unavailable for provisional use. When no material defect
remains, report `ready with risks`. This status means the package passed author-side inspection while
behavioral effectiveness remains unproven. Name untested clients and missing discovery evidence as risks. Do
not claim `ready` from review lite.

Review lite is the default because it is quick and avoids unnecessary model cost. Provisional real use can
expose failures that become durable cases. It does not replace a controlled comparison.

### Recommend Full Evaluation

Strongly recommend full independent evaluation for new skills, substantial rewrites, cross-client claims, or
recurring failures. Let the user defer it when time or model allowance is limited. Deferral does not block
provisional use when review lite finds no material defect.

Provide the candidate, cases, observed results, environment, and limits to an independent skill review or the
target repository's review process. Let that process choose isolation, permissions, baselines, graders,
repetitions, client coverage, and readiness criteria.

Only the full process can support `ready`. Report untested clients and failed setup truthfully.
