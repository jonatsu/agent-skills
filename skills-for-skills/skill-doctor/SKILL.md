---
name: skill-doctor
description: Audit recorded agent sessions to find where agent-setup's skills and rules failed the work, and name the repair that would have prevented it. Use to review how recent sessions went, to find recurring waste or code-quality defects across them, to decide which skill needs a description or content fix, or to judge whether a skill that never fires should have. Use skill-review for a static review of one skill, and skill-forge or skill-descriptions-and-triggers to write the repair.
license: MIT
metadata:
  author: Joonas Onatsu
  scope: repo-local
---

# Skill Doctor

Grade what the agent **did**, from sessions that already happened, and convert the result into a repair.

This skill is specific to the `agent-setup` repository: it drives that repository's `just` recipes and proposes
edits against its skill sources. It is the only review here that reads real sessions.

**The finding is the product, not the score.** A session that went badly is only interesting once you can name
what would have prevented it. Every judgment below ends in that name or it is discarded.

## Workflow

### 1. Collect the evidence yourself

```bash
just session-coverage                                    # which skills fire, per harness
just extract-sessions --out .scratch/doctor/<date> --limit 20
```

`extract-sessions` writes one document per session plus an index, at `0600`. Each document carries metric
values keyed by metric id, a declared-omission excerpt, and a `completeness` block.

Read two fields before judging a session.

`completeness.clean` — a thin session and a badly parsed one look identical in an excerpt, and only this tells
them apart. Judge a session whose `clean` is false only if you say so in the finding.

`extraction.degradation` — what the budget ladder cut to make the excerpt fit. `null` means nothing was cut.
Otherwise it names the window used and any cap applied to model or human text, in that order of severity: a
`user_cap` means a person's words were shortened, so weigh a correction you can only partly read accordingly.
`exceeded: true` means the anchors alone did not fit and the excerpt was emitted whole instead — that is the
session with the most errors and corrections, and it is the one worth reading closely rather than skipping.

### 2. Judge each session against both rubrics

Load [references/efficiency.md](references/efficiency.md) and
[references/code-quality.md](references/code-quality.md). Apply each to one session at a time, in batches small
enough that the evidence for the session under judgment is actually in context. Judging twenty sessions in one
pass is the waste the efficiency rubric exists to catch.

Both rubrics end by requiring a named cause. That clause is the point of the review: keep it even when the
verdict is positive, because a session that went well because a skill fired is evidence that skill earns its
place.

Judge a session by its outcome. A session that solved the problem without a skill is a good session: coverage
says which skills never fire, not that a session should have used one.

### 3. Ground every reason in the extraction

A reason must cite what the document actually contains — a metric id and its value, a `seq` from the excerpt,
or a quoted line. A reason that could have been written without reading the document is not evidence; it is the
model agreeing with itself.

Treat an absent signal as unknown. "No error markers appear" is not "the session succeeded", and
`skill_observations` reports what was witnessed, never more.

### 4. Aggregate across sessions, then route

One bad session is an anecdote. Report a finding when the same cause appears across sessions, as the named
cause and the count of sessions that showed it. Labels and counts are the whole result; a letter grade or
composite score would imply a comparability between runs that no two samples or judges share.

Report each harness separately. Claude records an explicit error flag and a typed single-operand read; Codex
infers errors from output text and batches reads, which costs it delivery attribution, so a lower number may be
the detector.

Before comparing coverage across harnesses, or calling a silent skill a description defect, check what each
client was shown. Claude's `skillOverrides` can set a skill to `name-only`, which keeps it installed and
invocable while withholding its description, and the extractor does not read that setting.
`docs/findings/session-measurement-thresholds.md` has the evidence.

Then route each finding:

| Cause named by the rubric                       | Goes to                                                                           |
| ----------------------------------------------- | --------------------------------------------------------------------------------- |
| A skill's description did not match the request | `skill-descriptions-and-triggers`                                                 |
| A skill's content is wrong, thin, or misleading | `skill-forge`                                                                     |
| Guidance for a moment nobody verbalizes         | `agents/shared/rules/`, not a skill — a skill for such a moment does not activate |
| A missing check, lint rule, or hook             | the repository's gates                                                            |
| Nothing exists that would have prevented it     | a new skill, or an accepted cost stated as such                                   |

Record the review under `docs/evaluations/skills/YYYY-MM-DD-<subject>.md` as a dated record. It states what
was true against one corpus on one day; never rewrite one to match a later run. The review ends at the report:
each repair is a separately authorized change.
