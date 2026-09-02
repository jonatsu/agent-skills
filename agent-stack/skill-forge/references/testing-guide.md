# Behavioral Evaluation

Evaluation answers whether a skill improves agent behavior, rather than whether its Markdown looks complete. Scale the
work to the change and the uncertainty.

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

Record a realistic request, required inputs, observable success conditions, model or agent used, date, and result. Prefer
outcome checks over expected wording or heading names.

When useful, run the same case without the skill to establish what guidance the model actually lacks. A baseline is most
valuable before writing a new skill, but it is a recommendation rather than a delivery gate.

Test the dimensions relevant to the change:

- **Discovery:** representative positive, negative, and ambiguous requests.
- **Behavior:** successful outcomes, consequential edge cases, and recovery from expected failures.
- **Comparison:** whether the skill improves correctness, consistency, effort, or user control over the baseline.
- **Portability:** supported environments and deployed model classes where differences could change behavior.
- **Claims:** assertions about external tools exercised against an authoritative source or real tool version.

Preserve cases that catch likely regressions. Report untested environments or model classes instead of implying complete
coverage.
