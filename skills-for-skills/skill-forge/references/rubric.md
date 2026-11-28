# Readiness Rubric

This file is the one definition of what a skill must pass, how deeply it was checked, and what status it earns.
Authoring's closing review and review mode both apply it; neither restates it.

## Contents

- Three judgments
- Hard gates
- Review tiers
- Evidence classes
- Verdicts
- Numeric ratings

## Three Judgments

Keep three judgments separate in every report, because each can pass while another fails:

1. **Validity:** does the package satisfy the specification and applicable repository policy?
2. **Design:** does its content plausibly guide the intended behavior without material risk or waste?
3. **Evidence:** what observed behavior supports or contradicts those claims?

A valid package can still be ineffective, and a strong static design can still lack behavioral evidence.

## Hard Gates

A hard gate is pass or fail, never a quality point. Any failed gate is a Must fix finding, and the verdict
sentence calls the skill invalid and names the gate.

- The specification validator rejects the package.
- An applicable repository-policy check rejects the package.
- Required license or provenance material is missing or inaccurate.
- A promised resource link is broken, a bundled script is unusable, or scaffold placeholder text remains.
- Instructions contradict each other so that no reliable execution path remains.
- The skill performs unsafe behavior or side effects beyond the user's authority. This includes consequential network
  access, credential use, writes, or destruction that its described purpose does not disclose.

Run the vendored specification validator, then the policy validator, and report each result separately:

```bash
uv run --isolated --no-dev --project <skill-forge-root>/scripts/skills-ref \
  skills-ref validate <skill-directory>
uv run <skill-forge-root>/scripts/quick-validate.py <skill-directory>
```

The policy validator exits 0 for a valid skill, 1 for policy failures, and 2 for invalid invocation. Name the
exact validator behind each result. A substitute validator is not equivalent to the specification validator,
since each misses what the other checks. When a validator cannot run, report it as unperformed. A passing
structural check says nothing about behavior.

## Review Tiers

**Review lite is the default.** It makes no model calls and starts no subagents. It covers:

- the hard gates above;
- the skill's contract: its job, representative requests, and intended invocation;
- four lenses on every skill: discovery, scope coherence, behavioral value, and lean execution;
- any other lens from [review-lenses.md](review-lenses.md) that the package's content makes relevant; and
- cross-file consistency.

**Full evaluation** runs controlled behavioral comparisons under the procedure in
[full-evaluation.md](full-evaluation.md). It runs only after the user authorizes its time, model allowance,
and side effects.

Recommend full evaluation strongly for a new skill, a substantial rewrite, a cross-client claim, unreliable
discovery, recurring failures, or uncertain context cost. State the likely cases, clients, repetitions, time,
allowance, side effects, and evidence gain with the recommendation. The user may defer it; deferral does not
block provisional use when review lite finds no material defect. Preserve real-use failures and corrections as
cases for the later evaluation.

## Evidence Classes

Label every piece of evidence with one class, because a reader weighs them differently:

- **Executable check:** a validator, script, or deterministic test that ran, with its output.
- **Heuristic walkthrough:** a request traced through the package by reading, with no model run.
- **Model evaluation:** an observed model run with its recorded trace.

Synthetic fixture examples are test data, not observed execution. An author's own results and claims are inputs for
review to verify. The report names which were independently checked, which remain claims, and which required behavior is
untested. An independent review catches what an author's self-review does not, such as a `SKILL.md` that routes to a
reference file nobody wrote. Treat a skill that only its author has scored as unreviewed, and re-verify it.

## Verdicts

Report the verdict as one of three words, then one sentence in the skill's terms.

| Verdict               | Condition                                                                                 |
| --------------------- | ----------------------------------------------------------------------------------------- |
| `Ready`               | No Must fix finding is open.                                                              |
| `Ready after changes` | Fixing the listed findings makes the skill ready, with no rework.                         |
| `Not ready`           | It needs rework, such as a split or a redesign, or a decision the findings cannot settle. |

**The sentence states the evidence behind the verdict.** Without a full evaluation, a `Ready` sentence names the
behavior that remains unmeasured, such as "Ready: passes review lite; discovery and execution on Codex are
unmeasured." Only a full evaluation that supports the intended job lets the sentence drop that limit. The rule
holds for an author's closing review as much as for an independent review, since neither observed the skill
running.

Give each finding one tier, ranked from consequence and likelihood rather than textual prominence:

- **Must fix:** a failed hard gate, or a material design, behavioral, or safety defect.
- **Should fix:** a maintenance risk, or a defect with a real but bounded consequence that can wait for a
  recorded follow-up.
- **Consider:** an optional improvement. Report at most five, and say how many you left out.

Two defects are always Must fix:

- **Unjustified scope mixing:** the package combines aspects that no shared job requires (the rule is under
  "One coherent job" in `SKILL.md`). Its repair is a split, so the verdict is `Not ready`.
- **Opaque specialized name:** the description relies on a tool, product, or artifact name without stating the
  capability or user intent it stands for. This is a discovery defect.

## Numeric Ratings

Assign a number only when the user needs one for a stated decision. There is no universal quality total,
because skills differ in required behavior, risk, and evidence. When a number is needed:

1. Define criteria from that skill's contract.
2. Keep hard gates outside the number.
3. Prefer observed case results to document proxies.
4. Explain the weights and label judgment-based weights as subjective.
5. Show raw observations and coverage beside the result.

The number summarizes the chosen decision model; it is not a property of the skill.
