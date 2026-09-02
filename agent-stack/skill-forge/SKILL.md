---
name: skill-forge
description: Creates and updates Agent Skills that follow the agentskills.io specification. Use for authoring SKILL.md, improving skill instructions, designing progressive disclosure, adding scripts or references, repairing skill discovery, making a skill portable or repository-specific, and recording provenance for adapted skills. Excludes qualitative scoring of completed skills, global agent instructions, tool descriptions, and third-party skill installation.
license: MIT
compatibility: The bundled specification validator requires Python 3.11+, uv, and dependency access on its first run.
metadata:
  author: Joonas Onatsu
---

# Skill Forge

Create or update the smallest skill that reliably changes agent behavior for the requested task.

Use the [Agent Skills specification](https://agentskills.io/specification) as the authority for package
structure and frontmatter. Do not substitute remembered vendor conventions for the specification.

## Workflow

### 1. Establish the Job

Read the existing skill and all bundled resources when updating one. For new skills, establish:

- the concrete task the skill enables;
- representative requests and successful outcomes;
- the decisions or knowledge a capable agent lacks without the skill;
- whether the work is a new skill, substantial revision, or focused update;
- whether the skill is portable or repository-specific; and
- whether any material derives from another source.

Ask the user only when a missing answer would change behavior, scope, portability, provenance, compatibility,
or cost. Proceed directly when the repository and request settle those choices.

Before adding guidance, ask whether the agent can recover it from an authoritative runtime source. Point to
that source when it is accurate and available during use. Include the information when the source is
unavailable, unreliable, or the skill must preserve non-obvious judgment that the source does not express.

### 2. Choose the Scope

Portable is the default and needs no scope metadata. A portable skill may require tools intrinsic to its job,
but it must declare relevant environment requirements in `compatibility` and must not assume authoring-machine
paths, repository commands, or undeclared surrounding tools.

A repository-specific skill must set `metadata.scope: repo-local`, name the repository near the start of its
body, and may rely on that repository's paths, commands, and conventions.

Read [references/portability.md](references/portability.md) when the skill names tools, paths, environment
requirements, or repository commands.

Treat frontmatter portability separately from runtime portability. New skills use fields defined by the Agent
Skills specification. Add vendor-specific extensions only when the user explicitly targets that vendor and
accepts reduced portability.

### 3. Preserve Provenance

Every newly authored skill records its current author in `metadata.author` and its license in the
specification's top-level `license` field. Discover both from authoritative repository or upstream sources;
never guess them.

An upstream-derived skill must also ship `ATTRIBUTIONS.md`, the upstream license text as `LICENSE.upstream`,
and the upstream `NOTICE` as `NOTICE.upstream` when the upstream project supplies or requires one. Preserve
these files during updates.

Read [references/provenance.md](references/provenance.md) when creating or updating an adapted or vendored
skill.

### 4. Design the Package

Start with `SKILL.md`. Add a resource only when it improves an actual execution path:

- Put essential shared instructions and decisions in `SKILL.md`.
- Put branch-specific detail in a focused reference and link it where that branch becomes relevant.
- Put reusable deterministic or fragile operations in scripts.
- Put files consumed by the output, rather than as instructions, in assets.

Keep each meaning in one authoritative place. Do not copy facts that a reliable live source can provide
cheaply. A short, self-contained skill is complete when it contains everything its task needs.

Read [references/workflow-patterns.md](references/workflow-patterns.md) when real prerequisites, branching,
iteration, gates, or strict output contracts make control flow consequential.

Read [references/pro-agent.md](references/pro-agent.md) when deciding whether repeated or fragile logic
belongs in a script.

### 5. Write for Reliable Behavior

Write instructions that change decisions or outcomes. Match specificity to risk: constrain fragile operations
closely and leave room for judgment where several approaches are valid.

Descriptions state what the skill does and when it applies. Cover each distinct trigger branch once. Add an
exclusion only when it prevents likely misrouting. Read
[references/description-guide.md](references/description-guide.md) when creating a description or repairing
discovery behavior.

Identify the dominant likely failure mode. Add an Iron Law only when one absolute constraint is the right
control. Use questions when they focus attention on a concrete decision. Add anti-patterns only when they
counter a likely or observed model default. Read
[references/writing-techniques.md](references/writing-techniques.md) when one of those techniques is
justified.

Use a checklist only when order or prerequisites matter. Rely on ordinary prose for independent rules and
judgment. Reuse the user's existing authorization; add a confirmation gate only when the eventual action
requires information or approval the user has not already supplied.

### 6. Evaluate Proportionately

For a new skill or substantial rewrite, behavioral evaluation is recommended. Compare realistic tasks with and
without the skill when the benefit is uncertain or costly to infer. Test multiple deployed model classes when
model differences could affect the result. Preserve useful evaluation cases so regressions can be reproduced.

For a focused update, test the changed behavior and nearby failure modes. Do not require a full baseline or
model matrix when it would provide little additional evidence.

Read [references/testing-guide.md](references/testing-guide.md) when designing behavioral evaluations or
diagnosing a skill that triggers or performs incorrectly.

### 7. Finish the Content, Then Validate

Complete substantive writing, package design, resource routing, and behavioral evaluation before running
mechanical validators. Do not use `skills-ref`, `quick_validate.py`, linters, or formatters as an early proxy
for evaluating the content. Any content change after a mechanical check makes that result stale.

Before mechanical validation, verify at least:

- the result fulfills the requested use cases without unrelated behavior;
- every instruction and resource earns its context or maintenance cost;
- references are reachable at the point they become relevant;
- declared compatibility and scope match actual dependencies;
- provenance and license artifacts are complete and preserved; and
- no scaffold placeholders remain.

Run new or changed scripts with representative success and failure inputs before the final mechanical checks.

After the content has settled, run the vendored specification validator, resolving `<skill-forge-root>` to
this skill's directory:

```bash
uv run --isolated --no-dev --project <skill-forge-root>/scripts/skills-ref \
  skills-ref validate <skill-directory>
```

The vendored source is pinned so validation does not depend on a moving upstream checkout. Its locked Python
dependencies still require access on the first run. If `uv`, Python 3.11+, or initial dependency access is
unavailable, report specification validation as unperformed. Do not claim that another validator is
equivalent.

Run this skill's local-policy validator when its dependencies are available:

```bash
python3 scripts/quick_validate.py <skill-directory>
```

Then follow the target repository's applicable mechanical checks and deployment workflow. Add further checks
only when the skill's domain or risk requires them. Report performed and omitted validation accurately.
