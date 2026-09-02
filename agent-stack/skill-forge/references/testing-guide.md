# Behavioral Evaluation

Evaluation answers whether a skill improves agent behavior, rather than whether its Markdown looks complete.
Scale the work to the change and the uncertainty.

## When Evaluation Pays

Behavioral evaluation is especially useful for:

- new skills;
- substantial rewrites;
- unreliable triggering;
- repeated workflow failures;
- skills deployed across materially different model classes; and
- instructions whose benefit is uncertain relative to their context cost.

A focused correction usually needs only a regression case for the changed behavior and nearby negative cases.

## Evaluation Shape

Record a realistic request, required inputs, observable success conditions, model or agent used, date, and
result. Prefer outcome checks over expected wording or heading names.

When useful, run the same case without the skill to establish what guidance the model actually lacks. A
baseline is most valuable before writing a new skill, but it is a recommendation rather than a delivery gate.

Test the dimensions relevant to the change:

- **Discovery:** representative positive, negative, and ambiguous requests.
- **Behavior:** successful outcomes, consequential edge cases, and recovery from expected failures.
- **Comparison:** whether the skill improves correctness, consistency, effort, or user control over the
  baseline.
- **Portability:** supported environments and deployed model classes where differences could change behavior.
- **Claims:** assertions about external tools exercised against an authoritative source or real tool version.

Preserve cases that catch likely regressions. Report untested environments or model classes instead of
implying complete coverage.

## Evaluate Discovery

Test discovery through a client where the agent chooses among registered skills. Do not provide the target
skill path or instruct the agent to load it. Observe whether the client actually loads `SKILL.md`; the final
answer alone does not prove activation.

Use realistic positive requests, close negative requests, and ambiguous cases. Positive cases should include
requests stated by outcome without the skill's exact terminology. Negative cases should share nearby terms or
artifacts while requiring another capability.

Repeat runs when nondeterministic activation could affect the decision and report raw activation counts. For
systematic description optimization, start near the official recommendation of 8–10 positive and 8–10
negative queries with three runs each. Keep focused repairs proportional by retaining the failed case and
nearby positive and negative regressions.

For repeated description optimization, keep a fixed training and validation split with similar positive and
negative proportions. Use training failures to revise the description, keep validation results out of the
revision process, and select the iteration with the best validation result. Finish with fresh cases that did
not influence any revision.

Generalize from failure categories. Do not copy words from individual prompts into the description merely to
make those cases pass. If several incremental revisions stop improving results, try a structurally different
description or reassess whether cases are realistic and correctly labeled.

## Run and Grade Output Evaluations

Start with two or three realistic cases. Give each case a prompt, optional inputs, and a human-readable
expected result. Include a consequential boundary or ambiguous case.

Run each case in a clean context with the skill and against a baseline:

- use no skill to measure value beyond default behavior; or
- use a snapshot of the previous version when evaluating a revision.

Keep prompts, inputs, environment, and output locations equivalent. Record outputs, duration, and token use
when the client exposes them.

After inspecting the first outputs, add specific and observable assertions. Avoid vague quality claims and
brittle exact-wording checks. Grade every assertion as pass or fail with concrete evidence; never award a pass
on benefit of the doubt. Use deterministic scripts for mechanical properties and human review for holistic
quality or unforeseen defects.

Inspect individual assertions and execution traces as well as aggregate results:

- assertions passing with and without the skill do not establish added value;
- assertions failing in both configurations may indicate a broken test or unsupported requirement;
- inconsistent results may indicate model variance or ambiguous instructions; and
- time or token outliers may expose unnecessary work.

Generalize repairs from the underlying failure, rerun every case after changes, and stop when further
iterations no longer produce meaningful improvement.
