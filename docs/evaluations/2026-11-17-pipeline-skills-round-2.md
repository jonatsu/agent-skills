# Evaluation: Pipeline Skills, Round 2

Date: 2026-11-17. Round 2 ran the 24 cases of `idea-brainstorming`, `technical-design`, and `implementation-planning`
that depend on supplied material: a saved draft, a spec, a design, ADRs, a plan, or a repository to inspect. Round 1
(`2026-11-17-pipeline-skills-round-1.md`) ran the other 28. Each case now names a small synthetic repository under its
skill's `evals/fixtures/`, and the runner copies it into the run's working directory.

## Verdict

All three skills improve on the base model on both Sonnet and Opus. Scores count a pass as 1 and a partial as 0.5 per
outcome, excluding outcomes the run correctly never reached:

| Skill                     | Sonnet without | Sonnet with | Opus without | Opus with |
| ------------------------- | -------------- | ----------- | ------------ | --------- |
| `idea-brainstorming`      | 0.91           | 1.00        | 0.86         | 1.00      |
| `technical-design`        | 0.94           | 0.97        | 0.87         | 0.97      |
| `implementation-planning` | 0.81           | 0.98        | 0.83         | 0.99      |

The base model already does well when the material is in front of it: it reads the supplied draft or design, keeps
the spec's identifiers, and stops at a stale design. The skills add what the base model cannot infer from the
material:

- **Document conventions.** Without the skill, both models wrote a catalog validator design in a plain structure
  (`unrelated-docs-not-convention`, 0.50 on both), and Opus gave a nine-section "compact arc42 outline" on
  `arc42-default`. Without a repository template, neither model opened a plan with an implementation overview or used
  outcome, dependency, and recovery sections (`plan-default-and-shared-preflight`, 0.62 on both).
- **Review governance.** On `review-gates-and-required-practices` and `review-availability-and-cost`, control plans
  reviewed each slice but had no fix re-review, no definition of a blocking finding, no final cross-unit review, and
  carried no reviewed revisions or unchanged conclusions forward. With the skill, both models passed all of them.
- **Implementer comprehension.** Control plans for an unfamiliar implementer led each unit with files and code rather
  than the behavior it delivers, and gave no interpretation for a failed check (0.75 and 0.58, against 1.00 with the
  skill).
- **Handoff drafts.** Saving the tool-library brainstorm, control drafts left out how the direction advances the
  governing overview, the decision status of each item, or whether the direction needs a spec before design (0.88 and
  0.81, against 1.00).

Six single outcomes stayed partial with the skill, none on both models except one: on
`current-code-not-product-policy`, both models sent the unresolved quota policy to `writing-specs` or the product
owner and never named a return to `idea-brainstorming`. The outcome applies only when the answer changes product
intent, which the runs did not assume, so the skill was not changed.

## Fixture Defects

The first run of `implementation-planning` showed four fixtures whose "accepted" designs were not settled. The
account-export design answered 404 where its spec requires an expired report, and designs relied on an "existing"
cleanup job, a web layer, a worker host, or a settings mechanism the fixture repositories did not contain. Skill runs
routed those gaps back to technical design and planned little or nothing; Sonnet wrote no plan at all for
`specification-design-traceability` and scored 0.30. Control runs planned over the gaps. That is the skill's intended
behavior, but those cases test traceability, review gates, and format handling, not gap detection.

The four designs were completed (`ec4806b`) and the five affected cases rerun on both arms and models. The table above
uses the rerun; with the settled designs, the skill arm scored 1.00 on all five on both models. The stale-design case
kept its trap, a design approved against a superseded spec revision that still includes public links, and both skill
runs caught it.

## Grading Correction for Round 1

The bundle script cut each file a run wrote at 20,000 characters. Graders marked outcomes they could not see as
partial, which penalized long documents, mostly from the skill arm. 21 round 2 bundles and 7 round 1 bundles, all
seven from the skill arm, exceeded the cut. They were rebuilt in full and regraded. Round 2 scores above use the full
grades. Round 1 changed only on `11-mixed-design-and-plan`, where outcomes graded not-reached are now graded; its
table in the round 1 record is updated.

## Method

The run and grading method is round 1's, with these changes:

- The runner copies the fixture named by a case's `fixture` field into the empty working directory, and passes a
  case's plain-string `conversation` entries as earlier turns ("Earlier in this conversation: …") before the prompt.
- Bundles name the fixture directory, and graders read fixture files when an outcome depends on them, such as whether a
  design preserved a supplied draft's decisions. Graders were told not to read the skill or its eval file.
- Files the run wrote are included whole.

96 runs (24 cases, two arms, two models), plus 20 reruns on the completed fixtures. Every control trace was searched
for the skills' frontmatter in tool results; none had it, while all skill-arm traces did.

## Limits

Round 1's limits apply: one run per cell, single-turn cases, partial blinding, Claude Code only. The fixtures are small
and were written by agents in one pass; a fixture defect shows only when a run trips on it, as four did here, so other
defects may remain in cases where both arms passed.
