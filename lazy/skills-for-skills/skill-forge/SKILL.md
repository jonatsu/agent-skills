---
name: skill-forge
description: "Create, edit, review, and evaluate Agent Skills. Use when turning completed work into a skill, writing or restructuring SKILL.md and bundled resources, repairing loadability or portability, or recording provenance, and when judging whether a skill is correct, effective, or ready, from a static check to a behavioral comparison against a baseline. Use writing-skill-descriptions when only the description is in question."
license: MIT
compatibility: The bundled validators require Python 3.11+, uv, and dependency access on their first run.
metadata:
  author: Joonas Onatsu
---

# Skill Forge

Build and judge Agent Skills. A good skill is the smallest package that reliably changes agent behavior for
its task, and both modes below serve that one standard.

`<skill-forge-root>` in any command means this skill's directory.

## Choose the Mode

- **Author** when the request creates, extracts, edits, restructures, or repairs a skill package. Read
  [references/authoring.md](references/authoring.md) and follow its steps.
- **Review** when the request asks whether a skill is correct, effective, safe, or ready, or compares a skill
  against a revision or baseline. Read [references/review.md](references/review.md) and follow its steps.
- **Neither** when only a description is in question, whether drafting, auditing, or measuring its triggering.
  Use the `writing-skill-descriptions` skill instead.

When a request names a skill without establishing the job, ask whether the user wants it built or changed, or
judged. A review request authorizes a report. Switch to authoring for a repair only when the user authorizes
that repair, then rerun the affected review.

Both modes report readiness against [references/rubric.md](references/rubric.md). Read it before stating any
status, verdict, or readiness claim.

## Shared Essentials

**The Agent Skills specification is the authority** for package structure and frontmatter
(<https://agentskills.io/specification>). The vendored validator in `scripts/skills-ref` implements it.
Remembered vendor conventions are not a substitute, because the vendors' own validators disagree with the
specification.

**One coherent job.** Inventory every subject, tool, language, workflow, and output the skill covers. Keep
aspects together only when one shared task or decision boundary requires them. Shared popularity, one author's
environment, possible integration, or occasional co-use is insufficient. When the relationship is not obvious,
the package states the shared job, so a reviewer never has to invent the justification.

**Portable is the default.** A portable skill needs no scope metadata and assumes no surrounding paths,
configuration, installed tools, client, or repository conventions. A repository-specific skill sets
`metadata.scope: repo-local` and names its repository near the start of its body. Read
[references/portability.md](references/portability.md) whenever a skill names clients, tools, paths,
environment requirements, repository commands, or product metadata.

**Model runs need authorization.** A control run, a behavioral evaluation, or a trigger measurement spends
time and model allowance. Start one only after the user authorizes that cost and any side effects, within a
stated run ceiling.

**Run outputs stay outside the package.** Keep authoring notes, traces, and results elsewhere. Ship fixture
skills only as inert `SKILL.md.fixture` templates, as described in
[references/full-evaluation.md](references/full-evaluation.md#keep-fixtures-inert).
