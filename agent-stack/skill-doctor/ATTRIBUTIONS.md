# Attributions

## `warpdotdev/common-skills` — `skill-doctor`

- **Source:** <https://github.com/warpdotdev/common-skills/tree/f3b58c81d1cfd5d8eabf2e32edb32db2b0573923/.agents/skills/skill-doctor>
- **Revision read:** `f3b58c81d1cfd5d8eabf2e32edb32db2b0573923`, fetched 2026-09-12
- **License:** MIT, Copyright (c) 2026 Denver Technologies, Inc. Preserved as `LICENSE.upstream`.

**Adapted material.** `references/efficiency.md` and `references/code-quality.md` take their verdict labels and
the description of each label from upstream's `scorers/efficiency.md` and `scorers/code-quality.md`, and the
bullet lists of assessment dimensions closely follow upstream's. The "Rubric" and "Reason" prose is upstream's,
lightly edited to name this repository's extraction instead of a condensed prose transcript.

**What changed, and why:**

- **Numeric scores removed.** Upstream attaches a score to each label (1 / 0.8 / 0.4 / 0.2) and feeds it into a
  weighted composite and an A+/A/A- ladder. This repository's assessment of that package found the grade
  unsupported: the labels are the only inputs that set it and nothing checks them. The labels are kept; the
  arithmetic is not.
- **`insufficient_evidence` added to the efficiency rubric.** Upstream offers it only for code quality, so the
  efficiency judge had to choose a waste level even with nothing to judge. A judge with no way to say
  "insufficient evidence" invents a verdict.
- **Reading-the-extraction sections are ours.** They are specific to the declared-omission excerpt and metric
  ids this repository's extractor emits, which upstream has no equivalent of.

**Not adopted:** the collector, the score aggregator, the HTML report, the letter grade, and the step that
applies proposed edits to deployed skill files.

## `alirezarezvani/claude-skills` — `skill-doctor`

- **Source:** <https://github.com/alirezarezvani/claude-skills/blob/main/engineering/skill-doctor/skills/skill-doctor/SKILL.md>
- **Influence:** reviewed as a de-branded fork of the above. Nothing from it is used. Recorded because reading
  it is what prompted this skill, and because the rubric credit belongs upstream rather than to the fork.

Both reviews are recorded in `docs/plans/evaluation/session-scoring-draft.md`, Subject A.
