---
name: prompt-debugging
description: Debug and repair an existing LLM prompt from observed failures using controlled fixtures, traces, and regression runs. Use when a prompt produces wrong, inconsistent, over-cautious, over-compliant, malformed, or costly output, or when comparing prompt revisions; not for writing or improving a prompt without recorded failures (writing-prompts), repository instruction maintenance, or Agent Skill authoring.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Prompt Debugging

Repair an existing prompt by turning observed failure into reproducible evidence, one falsifiable hypothesis, and the
smallest verified prompt change.

**Preserve the failure in an outcome-based fixture, and pass harness preflight, before the first prompt edit.** A
response that looks wrong may expose a prompt defect, a broken fixture, an unavailable dependency, a
permission boundary, missing prompt delivery, or model variance. Editing before classifying that layer destroys the
evidence and often patches the wrong system.

## Keep the Job Narrow

The target is an existing prompt with an observed failure, or a set of prompt revisions to compare against concrete
behavior: a system or developer prompt, agent definition, tool description, task or API prompt, instruction file, or
few-shot set.

The user may authorize both diagnosis and repair in one request. A review-only request does not authorize editing the
prompt, changing a harness, or running cost-incurring evaluations.

## Establish the Decision and Budget

State what the evaluation must decide: reproduce a defect, choose between revisions, validate a repair, assess discovery,
or decide readiness. Record the actual prompt text and every instruction source the target receives, including
precedence, dynamic injection, tools, memory, and delegated context when relevant.

Collect or establish:

- the exact request or input;
- the observed output and trace, when available;
- the desired behavior and its independently derived oracle;
- client, model, version, reasoning or sampling settings, tools, and environment;
- allowed writes and prohibited side effects;
- the comparison baseline; and
- the run, token, time, monetary, or subscription-allowance ceiling.

Obtain explicit authority before a run incurs material cost or consumes a limited allowance not already authorized.
Recheck the live allowance before expanding a suite. Treat a subscription as zero marginal monetary cost while still
reporting token, latency, quota, and opportunity cost.

## Preserve the Failure

Write or strengthen the fixture before changing the prompt. Assert observable behavior rather than headings, wording, or
the presence of a file alone. Include the realistic input, required context, success conditions, consequential failure
paths, allowed writes, turn sequence, and evidence to retain.

Make the case discriminating. It should force the decision the prompt is meant to change. A fixture with no relevant
choice cannot distinguish compliance from default model behavior. When a failure concerns activation, use several
behavioral fingerprints or an observable load signal rather than one keyword.

Keep future conversation turns outside the active workspace until their turn begins. A model that discovers a staged
confirmation, answer, or expected output has not passed a multi-turn fixture.

## Preflight the Harness

Read [references/evaluation-harness.md](references/evaluation-harness.md) and complete its preflight before any model
run.

Use runtime help or current authoritative documentation for client flags, model names, and configuration. Dated command
lines are evidence about one version, not permanent syntax.

## Reproduce and Classify

Run the unmodified prompt in a clean context. Preserve the prompt, client command, output, trace, duration, usage, and
result. Inspect the trace as well as the final answer; a polished answer can hide prompt non-delivery, unnecessary work,
permission failures, premature completion, or a future-turn leak.

Classify the failure before proposing a prompt edit:

1. **Harness failure:** invocation, permission, dependency, workspace, capture, or session-continuation defect.
2. **Fixture failure:** missing input, ambiguous oracle, contradictory expectations, leaked future state, or an
   advertised command that cannot run.
3. **Delivery failure:** the prompt did not load, lost precedence, was truncated, or activated for the wrong request.
4. **Under-compliance:** the prompt contained the right obligation but the model did not apply it.
5. **Over-compliance:** the model followed an overbroad obligation and that compliance caused the bad outcome.
6. **Authority failure:** prose claims permission, enforcement, or product authority the prompt does not hold.
7. **Variance or external failure:** the prompt is not yet implicated because nondeterminism or an external dependency
   explains the observation.

Only delivery, under-compliance, over-compliance, or authority failures normally justify a prompt change. Repair harness
and fixture failures at their own layer, then reproduce before touching the prompt. Read
[references/failure-diagnosis.md](references/failure-diagnosis.md) for the observed patterns behind this classification.

## Make One Falsifiable Repair

State one hypothesis linking the observed behavior to one prompt mechanism. Change the smallest instruction, placement,
boundary, example, or escape hatch that can falsify it. Remove or reconcile any rule the change duplicates or
contradicts. Change one mechanism per attempt, so a passing rerun shows which change mattered.

Write the repair for the failure category, in the prompt's own terms; fixture vocabulary pasted into the prompt passes
one case and generalizes to none. Preserve accepted behavior, authority boundaries, downstream formats, and
compatibility. Ask before a repair changes public behavior, architecture, cost priority, or a working prompt outside
the authorized scope.

Useful repairs depend on the diagnosis:

- Make an all-blocked branch terminal when the model acknowledges the blocker but continues anyway.
- Put confirmation after the complete decision it authorizes when an earlier approval is applied to later choices.
- Narrow a condition and state its exception when an absolute rule suppresses valid independent work.
- Add a concrete fallback when missing context makes the model invent an answer or stop without a recovery path.
- Remove or narrow a rule when the model obeyed it and over-compliance caused the failure.
- Move enforcement into code or permissions when prose cannot guarantee the required control.

## Prove Green Without Expanding Blindly

Rerun the exact failing case with the repaired prompt. Then run the nearest boundary cases that could regress: the
exception to a new stop rule, a legitimate approval path after a new gate, or a small case after adding a heavyweight
workflow.

Hold every variable but the one under test equal, and rerun the baseline whenever the harness changed. The harness
reference's "Context Isolation" and "Scale by Decision" sections set when to add clients or repetitions.

Stop when the authorized budget or allowance is reached. Preserve partial evidence and name the missing assertion. Do not
weaken a fixture or call a harness failure a model pass to finish the run.

## Record and Deliver

Keep validity, design judgment, and behavioral evidence separate. A mechanically valid prompt may still fail, and a
plausible repair without a green run remains unverified.

Deliver:

- the prompt diff;
- the failure category and hypothesis behind each change;
- exact client commands and relevant flags;
- red and green results with output and trace locations;
- duration, tokens, quota, and material monetary cost;
- harness or fixture failures excluded from behavioral counts;
- coverage limits, residual risks, and deferred cases; and
- the resulting readiness decision without implying statistical confidence from a small sample.

Raw traces may contain system instructions, machine paths, request identifiers, tool results, or sensitive data. Inspect
and sanitize them before committing. Prefer durable outcome fixtures and an evidence summary over bulk-committing opaque
client logs.
