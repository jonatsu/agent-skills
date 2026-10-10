# Planning and Design Skills Research

## Overview

**This document preserves the evidence behind the planning and design skills refactor.** The governing overview is
[`design-plan-skills-refactor.md`](design-plan-skills-refactor.md). This companion supports its decisions with repository
examples, archived-skill analysis, external pattern mining, provenance, and known evidence limits.

This document does not define the current framework or implementation sequence. Readers looking for the initiative's
purpose, accepted decisions, workstreams, and open questions should start with the governing overview.

## Evidence from This Repository

**The preferred plans optimize for a reader making or executing decisions.**
agent-setup's `docs/plans/agent-management/repo-consolidation.md` is an overview-level plan, while
agent-setup's `docs/plans/agent-management/agent-config-templating.md` is a detailed design. Both follow a
mostly linear argument:

1. Establish the problem, outcome, and boundary.
2. Describe current evidence and constraints.
3. Present decisions with their rationale and consequences.
4. Identify risks, rejected approaches, and unresolved work.
5. Sequence implementation and place verification beside each phase.
6. Define completion in observable terms.

Their sections have recognizable reader jobs. A reader can stop after the outcome, inspect a particular decision, or
continue into the implementation sequence without reconstructing the document's history.

**The retired knowledge-vault corpus optimized for authority and lossless history.** It contained about 10,000 lines
across 15 content documents plus a generated index. That index identified which document owned a topic, but it provided
no entry point, reading order, dependency graph, or current task. `design.md` therefore needed a second, manually
maintained companion-document map.

The corpus demonstrates several costs imposed directly by `design-forge`:

- Forked child documents can lack an H1 and a standalone purpose statement because relocation must remain verbatim.
- Parent documents retain headings whose only content is a relocation pointer, interrupting a linear reading path.
- Current rules, historical rules, corrections, provenance, and future consequences often share one passage.
- Permanent identifiers and cross-document references make decisions traceable while distributing their meaning.
- Large decision-table cells contain arguments that would be easier to follow as short sections.
- Plans accumulate design decisions, implementation detail, test strategy, and amendment history in one artifact.

The detailed verification gates in the M1 implementation plan remain valuable. Placing concrete evidence beside the
work it proves is sound; the surrounding archaeology causes the reading problem.

## Archived `design-forge`

**The skill largely succeeds at its declared job, but that job does not include designing.** It governs structure,
lifecycle, and operations over a document corpus. It also calls itself a routing skill rather than an end-to-end
workflow. It cannot guide an agent through problem framing, investigation, alternative selection, design synthesis, or
reader-oriented explanation.

The package combines:

- document types, ownership, lifecycle, indexing, and locking;
- corpus conversion, forking, amendment, and supersession;
- requirements elicitation and atomic requirement authoring;
- confidentiality labels and handling instructions;
- hardware and systems-engineering vocabulary;
- length limits and structural validation; and
- a small section catalogue that deliberately avoids design-writing guidance.

These jobs interact, but they do not share one execution boundary. The package spends most of its attention on safe
document mutation after a design exists. The user invokes a design skill because they need help creating the design.

### Mechanism Disposition

| Mechanism                                              | Working disposition                                                                        |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| Respect an established house convention                | Preserve in every document-related skill                                                   |
| One owner for each normative topic                     | Preserve as a design principle; make machine enforcement optional                          |
| Generated ownership index                              | Move to optional corpus governance; do not treat it as reader navigation                   |
| Lifecycle and supersession metadata                    | Move to optional corpus governance                                                         |
| Locked documents and append-only amendments            | Reconsider; prefer current truth plus version-control history for ordinary software design |
| Byte-identical fork protocol                           | Keep only for migrations that require proof of lossless relocation                         |
| Untitled forked children and retained pointer headings | Remove from normal authoring behavior                                                      |
| Permanent identifiers for every numbered item          | Restrict to entries with real downstream references                                        |
| Length ceilings                                        | Replace with cohesion and reader-task diagnostics                                          |
| Atomic requirement schema                              | Move to requirements engineering and apply only when its rigor is warranted                |
| Hardware and system vocabulary                         | Move to domain-specific requirements guidance                                              |
| Handling labels                                        | Keep only as advisory repository governance with an explicit security limitation           |
| Structural checker                                     | Retain with optional governance; it cannot validate design quality                         |

## Archived `idea-forge`

**The Superpowers interaction model is a stronger base than the archived `idea-forge` workflow.** The comparison uses
the current [Superpowers `brainstorming` skill](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md)
and the complete local `skills/archived/idea-forge/` package.

| Concern           | Superpowers baseline                                                | Archived `idea-forge`                                                   | Direction                                                           |
| ----------------- | ------------------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Conversation      | Natural dialogue with one question per turn                         | Seven phases and a copied progress checklist                            | Follow Superpowers                                                  |
| Initial alignment | Inspect context, then ask what matters                              | Quote the seed and success criteria verbatim, then require confirmation | Summarize only when ambiguity warrants it                           |
| Alternatives      | Present two or three approaches with tradeoffs and a recommendation | Separate Explore and Shape modes with mandatory verdict tokens          | Use conversational branches and comparisons                         |
| Critical thinking | Apply YAGNI, tradeoffs, and recommendation                          | Run a seven-question battery on every candidate                         | Retain selected diagnostics as internal prompts                     |
| Uncertainty       | Research facts, recommend choices, and ask for user judgment        | Record every open question rather than answering it                     | Distinguish facts, recommendations, assumptions, and user decisions |
| Scope             | Detect oversized requests early and decompose them                  | Split when the skeleton reaches roughly 300 to 400 lines                | Decompose before detailed exploration                               |
| Output            | Complete design and specification on its architectural path         | A skeleton whose sole consumer is `grilling`                            | Produce an explicitly incomplete design/plan draft                  |
| Gates             | Require approval before implementation                              | Require anchor, transition, path, readiness, and handoff confirmations  | Keep gates for decisions requiring user authority                   |
| Persistence       | Write a specification for architectural work                        | Write repeatedly at phase boundaries                                    | Write the draft at handoff, on request, or before context loss      |

The local skill's recorded session demonstrates the cost of its process. Shape verdicts appeared before the transition
gate, and nearly every turn exceeded the line ceiling through its escape valve. The prescribed controls did not survive
normal use. This evidence is recorded in
agent-setup's `docs/plans/archived/requirements-skill.md`.

Useful local mechanisms include early branch generation, one consequential question per turn, early scope decomposition,
a parking lot, research-backed prior art, equal scrutiny for user and agent proposals, explicit exclusions, bounded open
questions, and rejected alternatives with reasons. The omission, assumption, created-complexity, dependency, and
one-way-door tests remain useful as internal prompts.

The replacement should remove verbatim anchor confirmation, the Explore-to-Shape gate, mandatory verdict tokens, fixed
candidate counts, line ceilings, forced bluntness, repeated writes, and `grilling` as the brainstorm's sole consumer. It
should surface weak premises and recommend answers while reserving user confirmation for intent, authority, risk
acceptance, and product judgment.

### Superpowers Package Assets and Provenance

The current Superpowers package includes a visual companion, a spec-reviewer prompt, a frame template, a browser helper,
a local HTTP and WebSocket server, and Bash lifecycle scripts. The visual subsystem requires Node, Bash, browser access,
persistent processes, filesystem state, and a local network port. It belongs in an optional visualization capability
rather than the portable brainstorming core. The spec-reviewer prompt belongs to technical design or planning, and the
current brainstorming entrypoint does not route to it.

The local `idea-forge` package has no supporting resource beyond its archive record. Superpowers is MIT-licensed.
Because it is the declared base, an adapted replacement must preserve the upstream license and record Jesse Vincent and
`obra/superpowers` in the package provenance.

## Compound Engineering

**EveryInc's `ce-brainstorm` and `ce-plan` contain strong authoring principles inside elaborate runtime protocols.** The
useful patterns are:

- choose the output mode before research;
- ground the work before imposing document structure;
- distinguish product decisions, technical decisions, and implementation-time discoveries;
- ask only questions whose answers materially change the result;
- present bounded alternatives with a recommended default;
- confirm the synthesized scope before writing a substantial artifact;
- make sections earn their place through a reader need;
- lead with decisions and outcomes;
- keep one owner for each normative rule; and
- attach concrete behavioral verification to implementation work.

The replacement should avoid their unified-plan schema, large identifier registries, mandatory phase machinery, and
machine-facing artifact protocol. Those mechanisms risk reproducing the knowledge-vault failure: locally correct
sections inside a globally difficult reading experience.

Primary sources:

- [Compound Engineering: `ce-brainstorm` guide](https://github.com/EveryInc/compound-engineering-plugin/blob/main/docs/guides/ce-brainstorm.md)
- [Compound Engineering: `ce-plan` guide](https://github.com/EveryInc/compound-engineering-plugin/blob/main/docs/guides/ce-plan.md)
- [`ce-brainstorm` writing contract](https://github.com/EveryInc/compound-engineering-plugin/blob/main/skills/ce-brainstorm/references/brainstorm-sections.md)
- [`ce-plan` writing contract](https://github.com/EveryInc/compound-engineering-plugin/blob/main/skills/ce-plan/references/plan-sections.md)

## BuilderIO `visual-plan`

**BuilderIO supplies useful visualization principles inside a tool-specific publishing workflow.** The package was
reviewed at commit
[`86257760`](https://github.com/BuilderIO/skills/commit/86257760a156c7ad5248bf11fec31eaa63202614), dated
2026-09-03. The
[`visual-plan` package](https://github.com/BuilderIO/skills/tree/86257760a156c7ad5248bf11fec31eaa63202614/skills/visual-plan)
contains `SKILL.md`, a README, references for canvas, connection, document quality, an exemplar, local files, and
wireframes, plus one linked example image. It contains no local scripts, tests, or templates.

Its strongest reusable mechanisms are:

- choose the visual from the question;
- keep visuals local to the claim they explain;
- make a broad abstraction concrete through one understandable example;
- keep UI behavior, architecture explanation, and implementation detail on appropriate surfaces;
- pair visual review with a standalone, outcome-first textual plan;
- audit open decisions and surface recommended defaults; and
- verify the visual artifact itself, then revise it surgically.

The complete package is too large and tool-specific to become the portable planning core. Hosted mode depends on the
Agent-Native service, connector actions, authentication, and a browser. Local mode still depends on Node, `npx`, custom
MDX components, and ordinarily the hosted viewer. Its unpinned `@latest` commands, inconsistent installation commands,
and hard failure when its connector is unavailable conflict with graceful degradation.

The framework should retain the selection and composition principles while evaluating renderers separately. BuilderIO's
package uses the
[MIT license](https://github.com/BuilderIO/skills/blob/86257760a156c7ad5248bf11fec31eaa63202614/LICENSE),
copyright 2026 Builder.io. Any adapted material requires preserved license and provenance.

## Stellarlink Requirements Agents

**Stellarlink supplies useful elicitation patterns inside a workflow that collapses requirements, design, planning, and
implementation.** The complete package was reviewed at commit
[`f2e75c12`](https://github.com/stellarlinkco/myclaude/commit/f2e75c1263a2d5f09cdc4bb3dfe3635c635ff296),
dated 2026-05-04. Its requirements package last changed at commit
[`5a50131a`](https://github.com/stellarlinkco/myclaude/commit/5a50131a13397fdc87933adba3f504084635cb17),
dated 2026-01-26.

The package contains eight files: a plugin manifest, README, workflow guide, four agent definitions, and one pilot
command. The agents cover requirements generation, coding, review, and testing. It contains no package templates,
references, scripts, examples, tests, or visual assets. The
[`requirements` directory](https://github.com/stellarlinkco/myclaude/tree/f2e75c1263a2d5f09cdc4bb3dfe3635c635ff296/agents/requirements)
is the inspected source.

### Actual Workflow

The orchestrator scans the repository, clarifies requirements interactively, assigns a subjective completeness score,
and asks for approval. Separate agents then generate a combined specification, change production code, review the
implementation, and optionally add and run more tests. The generated specification includes the solution, exact files,
schemas, signatures, endpoints, configuration, implementation sequence, and validation plan.

The package therefore has no independent design or planning phase. Architecture is described as implicit even though
the generator makes architectural choices. Implementation order appears inside the specification and is analyzed again
by the coding agent. Review happens after implementation rather than challenging requirements, design, or planning
before code changes.

### Patterns Worth Retaining

- Ground elicitation in existing behavior, conventions, interfaces, tests, and constraints.
- Preserve confirmed intent separately from the proposed solution.
- Ask the user only about consequential behavior, scope, priority, risk, and authority gaps.
- Cover inputs, outputs, success, errors, boundaries, dependency failures, degraded behavior, and compatibility when
  relevant.
- Use observable readiness rather than a numerical score.
- Keep one explicit approval gate before implementation begins.
- Scale workflow depth with uncertainty and risk.
- Preserve useful traceability without assigning an identifier to every statement.

### Patterns Rejected

- Subjective `90/100` completeness and review gates.
- Requirements as an umbrella term for design, planning, coding, review, and testing.
- One mandatory comprehensive document regardless of cohesion or reader need.
- Exact file and signature invention before design evidence exists.
- Fixed phase counts, coverage percentages, and test pyramids independent of project risk.
- Optional testing after the implementation agent was already required to write tests.
- Claude-specific orchestration and artifact paths in a portable workflow.

The package contains material contradictions: its documents disagree on phase counts, scoring models, approval points,
artifact paths, and artifact sets. Some linked guides are located in sibling packages, and one referenced quick-start
file does not exist. The review agent lacks a shell tool while claiming to verify tests and runtime behavior.

### License Boundary

The repository uses
[GNU AGPL-3.0](https://github.com/stellarlinkco/myclaude/blob/f2e75c1263a2d5f09cdc4bb3dfe3635c635ff296/LICENSE)
and provides no package-specific alternative grant. The root README mentions separate commercial licensing but does not
supply that grant in the repository. This MIT repository should record idea-level influence and independently implement
any retained concepts. It should not copy or adapt the prompt text unless the resulting work deliberately accepts and
complies with AGPL-3.0.

The source supports keeping requirements engineering as a separate deferred workstream. It demonstrates the value of
repository-grounded elicitation and a single implementation gate, but it does not provide a suitable requirements-skill
base.

## Superpowers `writing-plans` and Plan Corpus

**Superpowers provides useful implementation-planning mechanisms inside a suite-coupled workflow that does not preserve
the accepted design boundary.** The complete `writing-plans` package and all four files under `docs/plans/` were reviewed
at commit
[`b36e0829c6d0140e93cfef2ca599b1b07d4a7797`](https://github.com/obra/superpowers/commit/b36e0829c6d0140e93cfef2ca599b1b07d4a7797),
dated 2026-08-12. The repository and package use the MIT License.

### Package Review

The [`writing-plans` skill](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/writing-plans/SKILL.md)
says that planning follows an approved design, but its discovery text also accepts requirements alone. It then chooses
file responsibilities and interfaces, labels those choices as locked in, and places architecture in the required plan
header. An incomplete requirements document can therefore enter planning while consequential design work happens
silently.

The package is portable only inside the Superpowers suite. Its required header, worktree setup, and execution handoff
name Superpowers-specific skills and fresh-subagent workflows. It requires every task to carry a test cycle, every step
to fit a two-to-five-minute action, code steps to contain complete code, and each task to end in a Git commit. Those rules
overfit focused code changes and do not adapt cleanly to configuration, migrations, documentation, generated artifacts,
or repositories with different commit and testing policies.

The bundled
[`plan-document-reviewer-prompt.md`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/writing-plans/plan-document-reviewer-prompt.md)
is not linked from the skill. It requires a dispatched reviewer after the plan is complete, while the active skill says
review is self-run, is not a subagent dispatch, and needs no second pass after repairs. The package therefore contains
two contradictory review paths.

The useful mechanisms are smaller than the package:

- cite the governing design and keep shared constraints in one place;
- map affected files and exact cross-task interfaces when the repository establishes them;
- size tasks as independently reviewable and verifiable deliverables;
- place a concrete verification command and expected observation beside the work it proves;
- check design coverage, placeholders, and cross-task interface consistency; and
- calibrate review around implementation blockers rather than stylistic preferences.

### Corpus Review

The
[`OpenCode support design`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/docs/plans/2025-11-22-opencode-support-design.md)
and
[`implementation plan`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/docs/plans/2025-11-22-opencode-support-implementation.md)
show the value of separate reader surfaces. The design explains platform context, architectural boundaries, interfaces,
startup behavior, and file responsibilities. The plan supplies executable tasks, commands, expected results, and
checkpoints.

The pair also demonstrates why a formal handoff contract is necessary. The design crosses into phased implementation,
worktree setup, test sequencing, and merge instructions. The plan never links back to the design or maps tasks to stable
requirements. It omits the designed startup skills list and `findAllSkills` API, changes function signatures without a
deviation record, and defers all real OpenCode checks while allowing clean Git state to signal completion. Its 18 tasks,
63 numbered steps, and 15 task commits make dependencies implicit while preserving many syntax-only intermediate states.

The
[`skills-improvements analysis`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/docs/plans/2025-11-28-skills-improvements-from-user-feedback.md)
uses a strong problem pattern: observed event, root cause, and impact precede a proposed resolution. It keeps open
questions, risks, success measures, and staged recommendations visible. It also repeats the same subjects across problem,
proposal, phase, metric, and recommendation sections, and embeds execution-ready prose before several workflow choices
are settled.

The
[`visual-brainstorming plan`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/docs/plans/2026-01-17-visual-brainstorming.md)
is directly executable but leaves its design mostly implicit inside large code blocks. Dependencies and generated-file
ownership are unstated. Several checks prove syntax or string presence instead of the user-visible outcome, one server
check masks failure with `|| true`, and the event wrapper allows an incoming `type` field to overwrite its own
`user-event` type while the planned test expects the opposite behavior.

### Mechanism Disposition

| Mechanism                                           | Working disposition                                                                 |
| --------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Governing design link and shared constraints        | Preserve in implementation planning                                                 |
| Observed problem, cause, and impact before solution | Preserve in technical design when current-state evidence warrants it                |
| Explicit interfaces between work units              | Preserve when verified; do not invent signatures during planning                    |
| Independently reviewable deliverables               | Preserve; size by outcome rather than minutes or file count                         |
| Verification command plus expected observation      | Preserve; require behavioral evidence where behavior is the claim                   |
| Seam-first migration with incumbent regression gate | Preserve for migrations and integrations                                            |
| Fixed path under `docs/superpowers/`                | Replace with user direction and repository convention                               |
| Superpowers execution-skill handoff                 | Move to an optional adapter; keep the portable contract harness-neutral             |
| Universal micro-TDD and per-task commit             | Reject; select TDD and commit boundaries from the work and repository               |
| Complete code in every code step                    | Reject; include code only when it resolves a fragile or non-obvious contract        |
| Exact source line ranges                            | Replace with stable symbols, responsibilities, or anchors                           |
| Unlinked reviewer subagent                          | Replace with a coherent self-review and a separate optional adversarial-review path |
| Clean Git state as completion                       | Reject; completion follows verified behavior and explicitly reported omitted checks |

The package is `ready with risks` inside its own suite and `not ready` for direct portable adoption. The replacement
should be independently written. Superpowers supplies evidence for the technical-design and implementation-planning
contracts, but its fixed template, orchestration names, and execution protocol should not define either contract.

## Goal Definition and Intent-Driven Development

**OpenAI's `define-goal` and ECC's `intent-driven-development` strengthen the existing workflow without justifying a
fourth broad skill.** Both sources were inspected on 2026-09-04. Their useful concepts fit the accepted ownership of
brainstorming, technical design, and implementation planning.

OpenAI's [`define-goal`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/define-goal/SKILL.md)
was inspected at revision `49f948faa9258a0c61caceaf225e179651397431`. Its package uses the
[Apache-2.0 license](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/define-goal/LICENSE.txt).
It contributes these useful concepts:

- distinguish a completed outcome from an activity such as improving or investigating;
- pair an outcome with evidence that would honestly establish success;
- state scope and exclusions when ambiguity affects the goal; and
- quantify only when the metric represents genuine success.

Its goal tool, active-goal state, token budgets, and execution stop conditions do not belong in brainstorming. The
portable design workflow should retain only independently expressed outcome-quality guidance.

Affaan Mustafa's
[`intent-driven-development`](https://github.com/affaan-m/ECC/blob/e04ea0b9cc8248686edf5ac751cadff550e162b8/skills/intent-driven-development/SKILL.md)
was inspected at revision `e04ea0b9cc8248686edf5ac751cadff550e162b8`. The project uses the
[MIT license](https://github.com/affaan-m/ECC/blob/e04ea0b9cc8248686edf5ac751cadff550e162b8/LICENSE).
It contributes these useful concepts:

- code establishes current technical behavior, not desired product or business policy;
- prohibited side effects can define correctness more clearly than broad quality adjectives;
- depth should scale with applicable security, data, migration, compatibility, cost, and usability risks;
- verification should name a safe environment when evidence could affect data, services, secrets, or cost; and
- obligations and checks need no forced one-to-one mapping.

Its broad activation surface combines requirements, design, planning, and implementation. Its acceptance-brief
template, identifiers, revision protocol, fixed criterion counts, priority vocabulary, and implementation continuation
would weaken the accepted activity boundaries. These mechanisms remain excluded.

The comparison does not yet establish a separate requirements-engineering skill. That job remains deferred until real
requests require PRD review, contractual or compliance requirements, stakeholder acceptance criteria, or durable
requirement identity across several designs.

### Addy Osmani `idea-refine`

Addy Osmani's
[`idea-refine`](https://github.com/addyosmani/agent-skills/tree/1c760d643497e9da289300e5eb2f5aca861503f7/skills/idea-refine)
package was inspected at revision `1c760d643497e9da289300e5eb2f5aca861503f7` on 2026-09-04. The repository uses the
[MIT license](https://github.com/addyosmani/agent-skills/blob/1c760d643497e9da289300e5eb2f5aca861503f7/LICENSE).
The package contains `SKILL.md`, two framework and criteria references, an example collection, and a directory-creation
script.

Its strongest additions are outcome-first reframing for a seed anchored on a proposed solution and explicit attention
to assumptions that could invalidate a direction. The local skill can retain those concepts without requiring a named
problem-framing formula. It should seek the smallest decision-changing evidence for a critical unknown rather than
turning brainstorming into MVP design.

The remaining workflow is too prescriptive for the accepted interaction model. Fixed phases, question counts, idea
counts, framework catalogues, scoring dimensions, MVP rules, artifact templates, save paths, and tone instructions would
recreate the process machinery this refactor removed. Its stress-test trigger also overlaps `grilling`, while its
code-level examples cross into technical design.

## Review Relevance

**`docs/evaluations/skills/2026-09-shared-skill-review.md` records the completed brainstorming replacement and the adjacent
reviews.** The
portable `brainstorming` skill replaced archived `idea-forge` after behavioral evaluation and independent review.
`grilling`, `writing-documentation`, `writing-for-humans`, and `test-engineer` are also reviewed. Their current boundaries
support separate design and planning jobs: pressure-testing, document composition, prose editing, and test-only strategy
remain outside the new contracts.

That record also settles adjacent boundaries:

- Every live locally maintained skill has been reviewed. The deferred archive set remains separate.
- Archived `design-forge` remains deferred. Its governance mechanisms stay outside ordinary design and planning.
- The Stellarlink requirements-agent lead has now been reviewed and remains evidence for a separate deferred
  requirements-engineering workstream.
- `test-engineer` owns test-only strategy and coverage. Planning should name required evidence without absorbing that
  broader job.

## Earlier Planning Source

- **Addy Osmani's `planning-and-task-breakdown` skill** was inspected at commit
  [`020ec10a788f5703108d093a4bd3d9a7c3847d36`](https://github.com/addyosmani/agent-skills/blob/020ec10a788f5703108d093a4bd3d9a7c3847d36/skills/planning-and-task-breakdown/SKILL.md)
  on 2026-09-03. Its [MIT license](https://github.com/addyosmani/agent-skills/blob/020ec10a788f5703108d093a4bd3d9a7c3847d36/LICENSE)
  permits later adaptation with preserved provenance. The future planning workstream should retain independently
  expressed guidance to inspect accepted design and repository context before sequencing, map dependencies before
  ordering work, prefer independently verifiable vertical slices where they fit, place acceptance and verification beside
  each work unit, expose high-risk work early, and make parallel work conditional on dependencies and shared contracts.
  Its refusal to overwrite incomplete plans without resolving ownership is also useful. The future design MUST keep the
  accepted design and planning boundaries: it MUST NOT require fixed `tasks/` paths, file or time thresholds, tracker
  duplication, universal approval gates, fixed checkpoint intervals, or architecture decisions inside an implementation
  plan. Evaluate those retained ideas when the implementation-planning contract becomes active; this source does not
  alter the current `brainstorming` candidate.

## Evidence Limits

The source comparisons are static reviews. The completed brainstorming workstream has controlled behavioral evidence.
The intent refresh adds author-side cases, but those new cases have no independent baseline or candidate run yet. No
behavioral evaluation has compared technical-design or implementation-planning candidates across agents, models,
clients, or representative tasks. Their trigger behavior, interaction cost, and cross-model reliability remain
unproven.
