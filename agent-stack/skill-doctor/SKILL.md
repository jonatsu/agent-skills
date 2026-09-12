---
name: skill-doctor
description: Review real agent session history to find where this setup failed the work, and name the skill or rule repair that would have prevented it. Use to audit how recent sessions actually went, to find recurring waste or code-quality defects across them, to decide which installed skill needs a description or content fix, or to judge whether a skill that never fires should have. Runs the extractor itself. Static review of one skill package is skill-review; writing the repair is skill-forge.
license: MIT
metadata:
  author: Joonas Onatsu
  scope: repo-local
---

# Skill Doctor

Grade what the agent **did**, from sessions that already happened, and convert the result into a repair.

This skill is specific to the `agent-setup` repository: it drives that repository's `just` recipes and proposes
edits against its skill sources. It scores an axis nothing else here covers — `skill-review` inspects a package
statically, and the experimental harness compares a candidate against a baseline on fixtures. Neither sees a
real session.

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

Read `completeness.clean` before judging a session. A thin session and a badly parsed one look identical in an
excerpt, and only that field tells them apart. Judge a session whose `clean` is false only if you say so in the
finding.

### 2. Judge each session against both rubrics

Load [references/efficiency.md](references/efficiency.md) and
[references/code-quality.md](references/code-quality.md). Apply each to one session at a time, in batches small
enough that the evidence for the session under judgment is actually in context. Judging twenty sessions in one
pass is the waste the efficiency rubric exists to catch.

Both rubrics end by requiring a named cause. That clause is the point of the review: keep it even when the
verdict is positive, because a session that went well because a skill fired is evidence that skill earns its
place.

### 3. Ground every reason in the extraction

A reason must cite what the document actually contains — a metric id and its value, a `seq` from the excerpt,
or a quoted line. A reason that could have been written without reading the document is not evidence; it is the
model agreeing with itself.

Never promote an absent signal to a positive finding. "No error markers appear" is not "the session
succeeded", and `skill_observations` reports what was witnessed, never more.

### 4. Aggregate across sessions, then route

One bad session is an anecdote. Report a finding when the same cause appears across sessions, and say in how
many. Then route it:

| Cause named by the rubric                       | Goes to                                                                    |
| ----------------------------------------------- | -------------------------------------------------------------------------- |
| A skill's description did not match the request | `skill-forge`, description repair                                          |
| A skill's content is wrong, thin, or misleading | `skill-forge`, content repair                                              |
| Guidance for a moment nobody verbalizes         | `agents/rules/`, not a skill — a skill for such a moment does not activate |
| A missing check, lint rule, or hook             | the repository's gates                                                     |
| Nothing exists that would have prevented it     | a new skill, or an accepted cost stated as such                            |

Record the review under `docs/evaluations/YYYY-MM-DD-<subject>.md` as a dated record. It states what was true
against one corpus on one day; never rewrite one to match a later run.

## Never

- **Emit a letter grade, a composite score, or a rounded number.** The predecessor this replaces derived an
  A+/A/A- ladder from a four-label judgment over ~12 sessions and reported it to four decimal places. Two runs
  shared neither sample nor judge state and nothing said the grades were incomparable.
- **Average across harnesses.** Claude records an explicit error flag and a typed single-operand read; Codex
  infers errors from output text and batches reads, which costs it delivery attribution. A lower number may be
  the detector. Report per harness or report nothing.
- **Score skill usage as a virtue.** A session that solved the problem without needing a skill is a good
  session. Coverage says which skills never fire; it does not say a session should have used one.
- **Edit a deployed skill under `~/.config/*/skills` or `~/.codex/skills`.** The next `kst sync` overwrites it.
  Every accepted proposal is applied to `skills/shared/<domain>/<skill>/` and deployed from there.
- **Apply a repair inside the review.** Report first. Repairing is a separate, separately authorized step, and
  it runs through `skill-forge`.
