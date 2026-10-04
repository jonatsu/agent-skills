---
name: define-goal
description: Turn an intention, an accepted plan, or a bounded request into a measurable goal with success criteria, verification evidence, boundaries, and stop conditions, then set it in the harness goal loop (/goal, autopilot, create_goal). Use when asked to define, set, or sharpen a goal, or to make "done" measurable before an unattended run; not for product requirements (requirements-specification), implementation plans (implementation-planning), or tasks done directly.
license: Apache-2.0
metadata:
  author: Joonas Onatsu
---

# Define Goal

Shape what the user wants into a goal an agent can pursue honestly, then arm it in the harness's goal loop so
work continues until the evidence exists. A goal names an outcome and the evidence that proves it, never an
activity. In the engineering pipeline this step follows `implementation-planning` and precedes
`incremental-implementation`; for a bounded request with no plan, it is the whole of the preparation.

Every harness with a goal feature runs the same loop: the user sets an objective, the harness resumes the agent whenever
it would stop, and something judges whether the objective is met. The objective text is the only part of the
conversation the loop reliably sends back, so it must carry everything the judge needs.

## Confirm a Goal Is Wanted

Use this skill when the user asks to define, set, or sharpen a goal, asks for goal-backed or autopilot work, or
wants "done" made measurable before a long unattended run. For an ordinary task, do the work directly: a goal
pays for itself only when a loop or a long run needs an explicit finish line.

Take the outcome from its authority rather than inventing it. An accepted plan supplies the final integration
gate, a requirements specification supplies acceptance criteria, and a bounded request supplies its own
result. When the purpose itself is unsettled, return to `idea-brainstorming`; when intended behavior or
acceptance is open, to `requirements-specification`; when the work spans several dependent units with no plan,
to `implementation-planning`.

## Write the Goal

Write the goal in five parts:

1. **Objective:** the concrete thing that will be true, and the artifact, system, or behavior it concerns.
2. **Success criteria:** the binary or quantitative thresholds that define success.
3. **Verification:** the exact commands, checks, or observations that prove each criterion, and what passing
   output looks like.
4. **Boundaries:** what is in scope, what is out, and constraints that must keep holding, such as files left
   untouched or checks that stay green.
5. **Stop conditions:** when to stop and ask instead of grinding, such as a decision the user owns, a criterion
   proved unreachable, or a boundary that would have to break.

Before arming it, the goal must answer: what will be true, what evidence proves it, what threshold separates
success from failure, which boundaries matter, and what should halt the work. Rewrite a weak goal when local
context makes the rewrite safe. An activity goal, such as "make progress", "keep investigating", or "improve
the tests", becomes an outcome or is not armed.

Make it quantitative where the domain supports it, with numbers that represent real success rather than
decorative precision:

- **Bug:** reproduce it first, then fix it; success is a check that failed before the fix and passes after.
- **Tests:** the exact command and the required pass condition.
- **Performance:** the metric, the threshold, the measurement method, and the number of runs.
- **Quality work:** an observable bar, such as lint, type check, and tests passing, a count of reviewed
  examples, or an artifact the user approves.
- **Research:** the decision the research must enable, the sources or systems in scope, and the evidence
  standard.
- **Operations:** the healthy state, the observation window, the failure threshold, and the rollback or
  escalation trigger.

Ask one short question only when a reasonable rewrite risks pursuing the wrong outcome, aimed at the missing
threshold, environment, or minimum evidence. When the user has no metric, propose the most honest binary check
available and ask them to confirm it.

Strong: "Reduce checkout API p95 latency below 250 ms on the documented slow path with the smallest safe
server-side change; verify with `npm run test:checkout` passing and the local latency benchmark showing p95
under 250 ms in 3 consecutive runs." Weak: "Make checkout faster."

## Write the Condition

Compress the goal into one condition of at most 500 characters: the end state, the command whose output proves
it, the pass signal, the boundary that matters most, and the stop condition. Some judges read only the
transcript and run no tools, so write a condition that recent command output alone can confirm. Name the
command and its pass signal, such as "`pytest tests/auth` exits 0", rather than "auth works". Ending with "or
stop and report when …" lets a judge recognize a goal that cannot be met.

## Arm the Goal

Identify the harness from your own tool list and system prompt, then read
[references/harness-goal-loops.md](references/harness-goal-loops.md) for how that harness sets, forwards, and
judges a goal. Some harnesses let only the user set one; there, hand the user the exact command to run with
the condition filled in. Set a token or credit budget only when the user asked for one. Replace an active goal
only after the user confirms the old one is finished or abandoned.

In every harness, also write the five-part goal into the session's durable checkpoint or the plan's execution
record. That copy survives a fresh session, and it is the source for every brief written while the goal runs.

## Work Toward It

Run the verification as the last step, after the last change, so the passing output is the latest evidence in
the transcript; a check that passed before a later edit no longer proves anything. No harness passes a goal to
a subagent, so restate in each brief the criteria that lane owns. When a stop condition fires, stop and report
which one, with the evidence, rather than working around it. Declare the goal met only when every success
criterion has its verification output in hand.
