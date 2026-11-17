# Evaluation: Pipeline Skills, Round 1

Date: 2026-11-17. The question was whether `idea-brainstorming`, `technical-design`, and `implementation-planning`
change agent behavior on the cases in their `evals/behavior.json`, which had never run against a model. This round
covers the 28 cases that need no supplied material. The other cases need synthetic fixtures first; `TODO.md` lists
them.

## Verdict

All three skills improve on the base model, on both Sonnet and Opus. Scores below count a pass as 1 and a partial as
0.5 per outcome, excluding outcomes the run correctly never reached and the defective case
`10-compatible-migration`:

| Skill                     | Sonnet without | Sonnet with | Opus without | Opus with |
| ------------------------- | -------------- | ----------- | ------------ | --------- |
| `idea-brainstorming`      | 0.81           | 0.93        | 0.82         | 0.93      |
| `technical-design`        | 0.79           | 0.92        | 0.79         | 0.90      |
| `implementation-planning` | 0.71           | 1.00        | 0.79         | 0.97      |

The largest gains are where the base model overreaches. Without the skill, both models planned
`07-requirements-with-design-gap` by inventing the missing architecture (queued jobs, encryption scheme, status codes)
instead of returning the gaps to technical design. Both designed `no-spec-design-grows-large` without proposing a spec.
On `multi-outcome-scope` neither asked which outcome to explore first, and on `ambiguous-seed` both listed
interpretations before one anchoring question. With the skill, each of those passed on both models.

Two skill gaps showed on both models:

- **`idea-brainstorming` skips the composition judgment for several outcomes.** On `composable-branches`, the rule for
  decomposing several independently valuable outcomes (ask only which comes first) overrode the earlier rule to say
  whether branches conflict or compose. Both models split the waitlist and surplus sharing into separate outcomes and
  asked which to explore first, never whether they share a purpose.
- **`technical-design` stops the whole design when no spec covers user-visible behavior.** On
  `no-spec-design-grows-large`, both models proposed the spec correctly and then wrote no design at all. The skill says
  to stop deciding that behavior; it does not say to continue the design that holds under any answer, which the case
  expects.

One partial also repeated on both models: on `no-premature-acceptance-brief`, the response said detailed acceptance
belongs in a spec but not that architecture-dependent evidence belongs to technical design or planning.

## Case Defects

- **`implementation-planning/10-compatible-migration`** asks to plan "the accepted migration" but supplies no design.
  Both skill runs correctly refused to plan without a design to cite, as the skill requires, and scored 0.31 against
  1.00 for the base model, which planned from the one-sentence summary. The case needs a design fixture and moves to
  the fixture list.
- **`technical-design/small-change-arc42`** outcome 1 expects "concise applicability statements" for arc42 sections.
  The skill and its `references/arc42-writing-guide.md` say to omit a section that would carry nothing rather than
  fill it with an applicability line. The skill runs followed the skill; the outcome is stale.

## Method

Each case ran once per model (Sonnet and Opus) and arm, 112 runs, as a headless Claude Code main session:
`claude -p --no-session-persistence --disable-slash-commands --permission-mode acceptEdits`, with `Read`, `Glob`,
`Grep`, `Write`, and `Edit` allowed, in an empty working directory under `/var/tmp`. The one case with a fixture
repository (`09-small-change-without-universal-tdd`) got a copy of it. The skill arm prefixed the prompt with "Read the
skill at `<path>/SKILL.md` and follow it for this task" and pointed at a copy of the skill without its `evals/` folder,
exposed through `--add-dir`. The control arm got the bare prompt and a `--disallowedTools` rule denying reads under the
deployed skills directory. A single `Read(path)` deny rule covers every file-reading tool.

The control arm leaked twice before it was clean, and each leak would have hidden the skills' effect:

- `--add-dir` on the skill copies, first passed to both arms, let 55 of 56 control runs find and read the skill.
- Without that, 10 of 56 control runs still read the deployed copy under `~/.config/claude/skills/`, because the
  global instructions name the skills and `Read` was allowed everywhere. The deny rule closed it, and a check of every
  control trace for skill frontmatter in tool results found none.

Grading was blind. A script turned each run into a bundle holding the case prompt, the behavior under test, the
outcomes, the final response, the files the run wrote, and its tool calls, with every call that touched a skill path
removed; bundle names were shuffled and the arm key kept apart. Three Sonnet subagents graded about 37 bundles each,
marking every outcome pass, partial, fail, or not-reached (for a later stage the run correctly stopped before, such as
a handoff after the user confirms). Every skill-arm fail and partial, and the control misses behind the largest gains,
were checked against their runs.

## Limits

One run per cell measures each case coarsely, and a single disagreement moves a case score by a large step. The cases
are single-turn, so outcomes about later turns were graded not-reached rather than tested. Graders saw the skill's
influence in some final responses ("the skill requires …"), so blinding is partial. Only Claude Code was run.
