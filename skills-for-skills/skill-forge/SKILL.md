---
name: skill-forge
description: "Create and update Agent Skills for one or more AI agents. Use when turning completed work into a skill, designing its initial invocation and description, writing or restructuring SKILL.md and bundled resources, repairing package loadability or portability, or recording licensing and provenance. Not for focused audits of existing descriptions or independent skill reviews."
license: MIT
compatibility: The bundled validators require Python 3.11+, uv, and dependency access on their first run.
metadata:
  author: Joonas Onatsu
---

# Skill Forge

Create or update the smallest skill that reliably changes agent behavior for the requested task.

Produce a reviewable candidate with author-side evidence. Perform review lite by default. Without full
independent evaluation, report at most `ready with risks` and name the unmeasured behavior.

Use the [Agent Skills specification](https://agentskills.io/specification) as the authority for package
structure and frontmatter. Do not substitute remembered vendor conventions for the specification.

## Workflow

### 1. Establish the Job

When updating a skill, inventory the complete package before editing. Read `SKILL.md` and affected instruction
resources. Inspect scripts, assets, binaries, generated files, and large references at the depth the change requires.

Before substantially changing an existing workflow, identify the externally visible behavior that must remain
stable. Preserve representative inputs, expected outcomes, known failure behavior, and available execution
evidence before editing. Distinguish requirements being preserved from defects the requested change should
correct.

Establish:

- the concrete task the skill enables;
- representative requests and successful outcomes;
- the decisions or knowledge a capable agent lacks without the skill;
- the current author and applicable license;
- whether the work is a new skill, substantial revision, or focused update;
- whether reading any external source changed the skill's guidance, workflow, structure, examples,
  terminology, or failure modes, even when every retained idea was expressed independently.

Define one coherent unit of work that composes with other skills. Inventory every subject, tool, language,
workflow, and output the skill would cover. Keep multiple aspects together only when one shared task or
decision boundary requires them. Shared popularity, one author's environment, possible integration, or
occasional co-use is insufficient. Split unrelated guidance into separate skills or omit it.

When the relationship between retained aspects is not obvious, state the shared job in the description or
body so later reviewers do not have to invent the justification.

Ground domain guidance in real execution, authoritative documentation, or existing project artifacts. Do not
ask a model to invent a skill solely from its general training knowledge. When extracting a skill from
completed work, capture:

- the procedure that produced the successful result;
- every user correction or steering decision;
- required input and output forms;
- project conventions, constraints, and failure modes the agent initially missed; and
- successful behavior worth preserving, not only failures.

Useful project evidence includes runbooks, API specifications, schemas, configuration, review comments,
issue history, version-control fixes, and recorded failures with their resolutions. Label unsupported guidance
as uncertain or omit it; do not turn plausible generic advice into asserted expertise.

For a new skill, resolve `<skill-forge-root>` to this skill's directory. Run
`python3 <skill-forge-root>/scripts/init_skill.py --help`. Use the initializer when its minimal scaffold fits
the requested package. Replace every generated placeholder before validation. Create files manually when the
scaffold would require unnecessary cleanup.

Ask the user only when a missing answer would change behavior, scope, portability, provenance, compatibility,
or cost. Proceed directly when the repository and request settle those choices.

Before adding guidance, ask whether the agent can recover it from an authoritative runtime source. Point to
that source when it is accurate and available during use. Include the information when the source is
unavailable, unreliable, or the skill must preserve non-obvious judgment that the source does not express.

### 2. Choose Scope, Invocation, and Clients

Portable is the default and needs no scope metadata. A portable skill may require tools intrinsic to its job,
but it cannot assume any surrounding paths, configuration, installed tools, client, or repository conventions.
Declare intrinsic requirements in `compatibility`, check them when used, and report missing dependencies.

A repository-specific skill must set `metadata.scope: repo-local`, name the repository near the start of its
body, and may rely on that repository's paths, commands, and conventions.

Choose the invocation goal separately from scope. Decide from the job and representative user requests whether
the agent should select the skill or the user should invoke it explicitly. If both goals remain plausible and
the choice changes routing, ask the user. An agent-selected skill needs a realistic request-time intent; an
explicit-only skill needs a verified client mechanism, because description wording alone does not enforce that
policy. A habit with neither path belongs in always-loaded instructions or another deliberately loaded artifact.

Identify how each declared client can load the skill under that goal. Do not infer invocation policy from a
portable or repository-specific label.

Do not generalize one client's discovery result to another client. When a real invocation path exists, repair
weak routing instead of abandoning the skill. When no declared client can load the behavior reliably, change
the artifact form.

Read [references/portability.md](references/portability.md) when the skill names clients, tools, paths,
environment requirements, repository commands, or product metadata.

Assess format, runtime, and client portability separately. New portable skills use fields defined by the Agent
Skills specification. Keep product metadata, invocation syntax, and runner commands in named adapters. Add an
adapter only for an explicitly targeted client whose current contract is verified.

When the user names no client, target the specification-defined core and make no client-behavior claim.
An optional adapter must not make the portable core unusable elsewhere. Treat every untested client as a
coverage limit, not a supported target.

### 3. Preserve Provenance

This workflow requires every new skill to record its current author in `metadata.author`. It also requires the
applicable license in the specification's top-level `license` field. These conservative authoring policies may
exceed a license's legal minimum.

Discover authorship and licensing from authoritative repository or upstream sources. Never guess either.

Treat an external source as attribution-bearing when reading it changes what the skill contains. This includes
adopted ideas, mechanisms, structure, examples, terminology, or failure modes, even when no wording or code is
copied. Record each such source in `ATTRIBUTIONS.md`; do not reserve attribution for ports or close
adaptations. Name the exact influence and distinguish independently expressed ideas from copied or adapted
material.

Determine legal obligations from the exact source license and the intended distribution. This workflow also
requires copied, adapted, translated, or vendored material to ship `LICENSE.upstream`. Preserve an upstream
`NOTICE` as `NOTICE.upstream` when the project supplies it or its license requires preservation.

A source used only to verify public facts or runtime behavior does not require package attribution. Cite it
near the affected claim when useful. Preserve all existing provenance files during updates.

Read [references/provenance.md](references/provenance.md) whenever an external source influenced the skill or
supplied adapted or vendored material.

### 4. Design the Package

Before choosing files and resources, establish how the intended workflow behaves. If it coordinates multiple
state changes, may repeat an operation after uncertain completion, pauses for later resumption, or shares
mutable state with another actor, read
[references/operational-workflows.md](references/operational-workflows.md).

For those workflows, identify authoritative state, required preconditions and postconditions, permitted
effects, enforcement ownership, and recovery behavior. Resolve consequential gaps before treating the
candidate as complete. Scale the contract to the task: a short procedure may express it in a few sentences;
more complex workflows may need explicit transitions and supporting executable checks.

Design for lean execution and progressive loading by default. Keep shared essentials available and load
branch-specific instructions, executable modules, and detailed external data when the selected work needs
them. Make routing possible before loading the detail it selects. Prefer summary observations before
retrieving full records.

Scale the mechanism to the skill. A small, self-contained skill may already satisfy these criteria without
additional files or infrastructure. Keep routing in metadata, shared execution guidance in `SKILL.md`, and
branch-specific material in resources. Verify the target client before making claims about what it preloads
or defers.

For each representative request, walk through execution from a capable agent's starting knowledge. Extract
only resources that improve repeated execution:

- Put essential shared instructions and decisions in `SKILL.md`.
- Put branch-specific detail in a focused reference and link it where that branch becomes relevant.
- Put repeated deterministic or fragile operations in scripts when an existing tool does not suffice.
- Put files consumed by the output in assets.

Suppose the user asks, "Turn our incident-triage workflow into a skill that reads service logs and fills our
postmortem template." A capable agent can summarize logs, but it lacks the service event schema and the team's
triage order. It would also repeat timestamp normalization.

```text
incident-summary/
├── SKILL.md
├── references/event-schema.md
├── scripts/normalize-timestamps.py
└── assets/postmortem-template.md
```

Keep triage and source ordering in `SKILL.md`. Put the stable event schema in the reference. Include the script
only when an existing tool cannot normalize timestamps reliably. Include the asset because the consumer
requires that exact template.

Routing metadata may enter broad client context. The body and each reference add context when loaded. A client
may execute a script without loading its source. Verify that behavior before relying on the context saving.

Keep each meaning in one authoritative place. Do not copy facts that a reliable live source can provide
cheaply. Keep authoring notes, run outputs, and traces outside the deployed package. Bundle reusable fixtures
only when distribution is intentional, and keep fixture skills out of normal discovery. Store them as inert
templates and materialize them only in isolated evaluation workspaces. A short, self-contained skill is
complete when it contains everything its task needs.

Read [references/workflow-patterns.md](references/workflow-patterns.md) when real prerequisites, branching,
iteration, gates, or strict output contracts make control flow consequential.

Read [references/pro-agent.md](references/pro-agent.md) when deciding whether repeated or fragile logic
belongs in a script.

### 5. Write for Reliable Behavior

**Say what needs to be said; drop everything else.**

Include content that changes the agent's decisions, actions, or understanding needed for correct execution.
Remove filler, repetition, obvious explanations, and generic advice that adds no practical value. Each
sentence must earn the attention and tokens it consumes.

Preserve necessary conditions, constraints, failure handling, and examples that resolve ambiguity. Prefer
the shortest clear and complete explanation; do not compress useful guidance into cryptic wording.

Match specificity to risk: constrain fragile operations closely and leave room for judgment where several
approaches are valid.

Teach a reusable procedure for a class of tasks rather than the answer to one example. Preserve specific
commands, formats, constraints, and templates when correct execution depends on them.

Choose a recommended default when one approach usually fits. Mention exceptions with the condition that
selects them instead of presenting an undifferentiated menu of alternatives.

Keep a non-obvious prerequisite or gotcha in `SKILL.md` when the agent must know it before it can recognize the
condition for loading a reference. Move later branch detail behind a conditional pointer.

Write the initial description from the invocation goal chosen in step 2. For agent selection, name the job
and each distinct request branch once in terms a user might use, including requests that do not name the skill.
For explicit-only use, describe the opt-in job without ambient triggers. Add an exclusion only when it prevents
likely misrouting. Read [references/description-guide.md](references/description-guide.md) for the drafting
method and checks.

Identify the dominant likely failure mode. Add an Iron Law only when one absolute constraint is the right
control. Use questions when they focus attention on a concrete decision. Add anti-patterns only when they
counter a likely or observed model default. Read
[references/writing-techniques.md](references/writing-techniques.md) when one of those techniques is
justified.

Use a checklist only when order or prerequisites matter. Rely on ordinary prose for independent rules and
judgment. Reuse the user's existing authorization; add a confirmation gate only when the eventual action
requires information or approval the user has not already supplied.

Ensure the package's described purpose matches its behavior. Disclose consequential network access, credential
use, writes, destructive actions, and authority requirements. Inspect and test bundled executables and
dependencies. Reject hidden behavior or an unexplained expansion of authority.

### 6. Preflight and Review the Draft

Complete the substantive draft before treating mechanical checks as useful evidence. Then run a cheap
structural preflight. It must complete before review lite or any model-based test. Preflight confirms:

- the specification validator accepts the package;
- local policy checks accept the package when they apply;
- the candidate and promised resources are readable;
- no scaffold placeholders remain; and
- required commands and safe test destinations exist.

Preflight proves loadability and fixture readiness. It does not prove that the skill improves behavior.

Run the vendored specification validator, resolving `<skill-forge-root>` to this skill's directory:

```bash
uv run --isolated --no-dev --project <skill-forge-root>/scripts/skills-ref \
  skills-ref validate <skill-directory>
```

Run this workflow's separate policy validator when its dependencies are available:

```bash
uv run <skill-forge-root>/scripts/quick_validate.py <skill-directory>
```

The policy validator exits 0 for a valid skill, 1 for policy failures, and 2 for invalid invocation. Neither
validator establishes behavioral quality.

Run every new or changed script with representative success, invalid-input, and dependency-failure cases.
Use safe fixtures for stateful behavior.

Walk through the smallest set of representative requests that exercises the draft's important decisions. For
a focused update, inspect the changed behavior and its nearest failure boundary. When routing changed, prepare
positive, near-miss, and ambiguous discovery cases.

Review lite makes no model calls. Preserve useful cases, observed results, and untested clients for independent
review. Do not select comparative evaluation baselines or grade comparative performance during authoring.

Read [references/testing-guide.md](references/testing-guide.md) when author-side testing needs discovery cases,
review lite, behavior cases, or an evidence handoff.

### 7. Finish and Validate

Any content change makes earlier mechanical and behavioral results stale for the changed surface. Rerun the
affected checks after the content settles.

Before delivery, verify at least:

- the result fulfills the requested use cases without unrelated behavior;
- every resource earns its context or maintenance cost;
- references are reachable at the point they become relevant;
- declared compatibility and scope match actual dependencies;
- provenance and license artifacts are complete and preserved; and
- no scaffold placeholders remain.

If removing a passage would not weaken correct execution, understanding, or recovery, remove it.

Rerun both validators after the final content change. The vendored specification source is pinned. Its locked
dependencies still require access on their first run. Report unavailable validation as unperformed, and do
not claim that another validator is equivalent.

Then follow the target repository's applicable mechanical checks and deployment workflow. Add further checks
only when the skill's domain or risk requires them. Report performed and omitted validation accurately.

If full evaluation is deferred, report at most `ready with risks`. State which behavior remains unmeasured.
Recommend full evaluation without blocking provisional use when review lite finds no material defect. Preserve
real-use failures and corrections as cases for that later evaluation.

Deliver the candidate with its intended behavior, relevant cases, author-side results, and unresolved evidence
gaps. Distinguish executable checks, heuristic walkthroughs, and actual model evaluations. Provide that
evidence to an independent skill review or the target repository's review process when the user authorizes
the full evaluation.
