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

1. Materialize required fixture templates in isolation, then run the specification and applicable policy validators.
2. Confirm the candidate and every promised resource are readable.
3. Run advertised commands and representative script failure paths.
4. Use safe temporary inputs and outputs for stateful script checks.

A preflight failure is not skill behavior. Repair the package or fixture before starting the test.

The bundled `SKILL.md.fixture` files are inert test inputs. Materialize them as `SKILL.md` only in a fresh
workspace, with the case's declared resources at their original relative paths. Leave source and deployed
templates unchanged. Check intended clients for accidental fixture discovery, and report unavailable catalog
evidence as a limit. Keep expected outcomes and grading material out of candidate inputs unless the case
explicitly supplies them as task evidence.

## Walk Cases Heuristically

Trace each representative request through the package without making a model call. Check whether the main file
routes every required decision and resource before its point of use. Inspect outcomes instead of exact wording
or heading names.

Use deterministic checks for files, schemas, calculations, and other mechanical facts. Use human inspection
for coherence, usefulness, unstated decisions, and unforeseen defects.

If earlier real use produced a trace, inspect it. A final artifact can hide ignored instructions, unnecessary
work, tool failures, or unauthorized writes.

## Check Loading Boundaries

Inspect representative execution paths for unnecessary loading, initialization, and retrieval. Check
instructions, executable modules, and external records separately. State what each path needs and when it
becomes necessary; verify those boundaries using available traces and deterministic checks for imports or
external calls where practical.

Distinguish intended loading behavior from observed behavior. File separation and valid links establish
organization and reachability, not selective loading. Treat actual model-context loading as unmeasured
unless the target client exposes trustworthy evidence. A review-lite walkthrough does not authorize a
model run to obtain that evidence.

Add quantitative budgets where they make these boundaries enforceable or detect regressions. The absence
of a numerical budget does not relax the default requirement for lean execution. Keep checks proportional:
a small, self-contained skill needs no loading manifest merely to satisfy this criterion.

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

Provide the candidate, intended behavior, relevant cases, author-side results, environment, and unresolved
evidence gaps to an independent skill review or the target repository's review process. Distinguish
executable checks, heuristic walkthroughs, and actual model evaluations. Label synthetic fixture examples as
test data rather than observed execution. Let the independent process choose isolation, permissions,
comparative baselines, graders, repetitions, client coverage, and readiness criteria. Preserving pre-change
requirements and execution evidence during authoring does not constitute comparative grading.

Only the full process can support `ready`. Report untested clients and failed setup truthfully.
