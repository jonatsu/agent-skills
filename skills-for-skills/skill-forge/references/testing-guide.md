# Author-Side Testing

Check that the draft executes its intended paths before its closing review lite. These checks support
provisional use but do not establish comparative value.

## Define the Cases

Start with the smallest set that exercises the draft's important decisions. Record:

- a realistic request and required inputs;
- the behavior under test;
- observable success conditions;
- consequential failure paths;
- the target client and relevant environment; and
- the output, result, and known limits.

A focused update usually needs the changed behavior and its nearest failure boundary. Keep cases in a form an
independent review can reuse.

## Walk Cases Heuristically

Trace each representative request through the package without a model call. Check that the main file routes
every required decision and resource before its point of use, and inspect outcomes rather than exact wording
or heading names.

Use deterministic checks for files, schemas, calculations, and other mechanical facts. Use human inspection for
coherence, usefulness, unstated decisions, and unforeseen defects.

When earlier real use produced a trace, inspect it. A final artifact can hide ignored instructions, unnecessary
work, tool failures, or unauthorized writes.

## Check Loading Boundaries

Walk the representative paths with the questions under "Lean Execution and Information Hierarchy" in
[review-lenses.md](review-lenses.md).

## Prepare Discovery Cases for New or Changed Routing

Prepare discovery cases when creating a skill or changing its invocation route, even without an observed
activation failure.

For agent selection, write realistic positive requests, close negative requests, and ambiguous cases. State
positive requests by outcome, without the skill's exact terminology. Give negative requests nearby terms or
artifacts while requiring another capability. The later run happens in a client where the agent chooses among
registered skills, without the target path or an instruction to load it.

For explicit-only use, include a deliberate invocation and near misses from ordinary surrounding work. Test the
client's enforcement mechanism separately from the description wording, since one cannot prove the other.

Some clients expose no trustworthy load signal. Record that limit for the evaluation, and never infer
non-activation from the final answer alone.
