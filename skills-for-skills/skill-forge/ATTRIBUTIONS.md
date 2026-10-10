# Attributions

## Current skill

- Skill: `skill-forge`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: adapted from upstream and materially modified. Since 2026-09-28 the package also carries the former
  `skill-review` skill as its review mode; that skill's provenance is recorded under "Merged skill-review"
  below.

## Original authors and source

- Original author: Shawn Yang
- Copyright holder: `Copyright (c) 2025 sanyuan0704`, as stated in upstream's `LICENSE`
- Upstream project: <https://github.com/sanyuan0704/sanyuan-skills>
- Source path: `skills/skill-forge`
- Source commit: `ae75e917a003fb1dcfd6986b8728f94da7de6a6a` (dated 2026-03-02; upstream has since moved to
  `08b6572e`, 2026-05-11)

## Adaptation note

This version is derived from the upstream `skill-forge` skill and has been materially rewritten for portable
Agent Skills authoring.

Material changes include:

- treating the Agent Skills specification as the format authority;
- supporting portable and repository-specific skills;
- scaling author-side checks and the independent-review handoff to the change; and
- adding provenance, licensing, and local-policy validation.

## Upstream license

MIT. The verbatim upstream `LICENSE` ships beside this file as `LICENSE.upstream` and MUST travel with the
skill when it is redistributed or re-deployed. Upstream publishes no `NOTICE` file, so there is no
`NOTICE.upstream`.

Verified against the primary source on 2026-08-27 — `gh api repos/sanyuan0704/sanyuan-skills/license` reported
`MIT`, and the `LICENSE` blob itself was fetched and copied byte-for-byte. `gh repo view --json licenseInfo`
was NOT used; it misreports repositories that do carry a licence.

## Bundled Agent Skills Validator

- Component: `scripts/skills-ref`
- Project: <https://github.com/agentskills/agentskills>
- Source path: `skills-ref`
- Source commit: `69ef37e9424c0a7ea9dd2293b559e43ec8176379`
- Upstream author: Keith Lazuka, as stated in upstream `pyproject.toml`
- License: Apache-2.0; its license text is bundled at `scripts/skills-ref/LICENSE` with the
  repository-required final newline
- Modifications: upstream tests and development environment artifacts are omitted from the deployed copy;
  bundled runtime source and project files are unmodified

Upstream supplies no `NOTICE` file at the pinned revision.

## Bundled-Reference Check in `scripts/quick_validate.py`

The 2026-09-04 revision added a check that every relative path `SKILL.md` promises must exist inside the skill
directory. Reading `agent_skills/evals/tools/skill_lint.py` from
<https://github.com/Shubhamsaboo/awesome-llm-apps> (Apache-2.0, commit
`ca8e5b3c56e51e336449a99d79b42b45ea690b86`) supplied two ideas the check adopts: collecting both Markdown link
targets and bare paths under the specification's bundled resource directories, and stripping fenced code
blocks first because a fenced path is an illustration rather than a promise.

The implementation is independently written against this skill's existing structure and its own portability
rule, and no code, wording, or message text was copied. The evaluation that preceded it rejected the rest of
that script — it duplicates `skills-ref` with a hand-rolled YAML parser, and its remaining heuristics encode a
different project's house conventions. The escaping-path error and the anchor handling have no upstream
counterpart. No upstream license file is required, because nothing was copied or adapted.

## Official Agent Skills Authoring Guidance

The 2026-09-02 revision incorporated independently condensed guidance from these official Agent Skills pages:

- [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
- [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)
- [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills)
- [Using scripts in skills](https://agentskills.io/skill-creation/using-scripts)

The source files are under `docs/skill-creation/` at Agent Skills repository commit
`69ef37e9424c0a7ea9dd2293b559e43ec8176379`. That documentation is licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This skill reorganizes, condenses, and adapts the
guidance to its existing workflow and terminology; it does not reproduce the pages verbatim.

## mizchi's Optimizing Descriptions

- Author: mizchi.
- Source: [`optimizing-descriptions/SKILL.md`](https://github.com/mizchi/skills/blob/a41865b34b78f2675a6c73178377a5bcc1b492c6/optimizing-descriptions/SKILL.md).
- Revision: `a41865b34b78f2675a6c73178377a5bcc1b492c6`.
- License status: the pinned repository README says skills without an individual license default to MIT at
  the owner's discretion; this skill has no top-level license field or bundled `LICENSE.txt`.
- Influence: the distinction between agent selection and deliberate invocation prompted clearer initial
  authoring guidance. This skill treats invocation independently of portable or repository-specific scope.
  The description-drafting part of that guidance lived in `references/description-guide.md` until
  2026-09-28, when it moved to the `writing-skill-descriptions` skill, then named `skill-descriptions-and-triggers`.

The updated wording and cases are independently written. No mizchi prose, examples, code, templates, or
client-specific deployment procedure is copied or adapted.

## OpenAI Skill Creator

The 2026-09-04 revision consulted the
[OpenAI `skill-creator` package](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator)
at commit `49f948faa9258a0c61caceaf225e179651397431`. OpenAI publishes it under Apache-2.0. It influenced the
independently written method that derives resources from concrete execution needs. It also influenced the
explanation of context cost and the rule that instruction precision should follow task fragility.

No OpenAI prose, code, examples, templates, or product metadata are copied or adapted. The OpenAI-specific
`agents/openai.yaml` generator and its Codex assumptions are deliberately excluded from the portable core.

## Anthropic Skill Creator

The same revision consulted the
[Anthropic `skill-creator` package](https://github.com/anthropics/skills/tree/41bbe19d1a1a7eaab5e7bb9050a417e5c6cffc8f/skills/skill-creator)
at commit `41bbe19d1a1a7eaab5e7bb9050a417e5c6cffc8f`. Anthropic publishes it under Apache-2.0. It influenced the
independently written package-safety rule that consequential behavior must match the described purpose. Its
client-specific evaluation system also helped establish the core-versus-adapter portability boundary.

No Anthropic prose, code, schemas, examples, evaluator prompts, or interface assets are copied or adapted.
Its Claude-specific runner, viewer, subagent workflow, and package format are deliberately excluded.

## Operational Workflow Design

- Author: Mohammad Bayat.
- Source: [Designing Large Agent Skills as Deterministic, Phase-Oriented Systems](https://www.okbayat.com/writing/essays/phase-oriented-agent-skills-en).
- Project: `OkBayat/OkBayat.github.io`.
- Source path: `docs/writing/essays/phase-oriented-agent-skills-en.md`.
- Source commit: `9d0ad2e4a0a3793c10335b387b5a3f3d16c41f3b`, resolved through the file's commit history.
- Consulted: 2026-09-15.
- Rights status: the website's [rights statement](https://www.okbayat.com/about/rights) reserves rights to
  original content and supplies no blanket open-source license for the repository.

The essay influenced the decision to make operational design a conditional authoring obligation, including
explicit state authority, enforcement ownership, completion evidence, and recovery behavior. It also
influenced the lean-execution default across instructions, modules, and data, loading-boundary verification,
and preservation of behavior before substantial workflow revisions. The wording, examples, diagram, and
acceptance fixtures are independently written. No source prose, code, schemas, diagrams, or templates are
copied or adapted. Existing package license and provenance are preserved.

## Merged skill-review

On 2026-09-28 the separate `skill-review` skill (same author, MIT) merged into this package as its review mode.
Its workflow became `references/review.md`, its lenses `references/review-lenses.md`, and its behavioral
evaluation `references/full-evaluation.md`. Its hard gates, review tiers, verdicts, and numeric-rating policy
became part of the single rubric in `references/rubric.md`. Its `evals/activation.json` cases joined this
package's activation file, and its `evals/review-quality.json` and four fixtures moved here unchanged in name.
Every source entry that skill carried moves over below, restated where the merge changed which file holds the
material.

### Original author and source of skill-review

- Original author: Leonardo Flores
- Copyright holder: `Copyright (c) 2026 Leonardo Flores`, as stated in upstream's `LICENSE`
- Upstream project: [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit)
- Source path: `skills/skill-judge`
- Exact source revision: unknown. The initial local attribution in commit `165701f` of the author's private
  configuration repository recorded the upstream project, skill path, and MIT license but did not record a commit
  or tag.
- Later comparison snapshot: `3027f20f3181758385a1bb8c022d4041dfb4de84`, upstream HEAD as observed on
  2026-08-27. It predates the local addition and provides an auditable comparison point; it does not establish
  which revision was originally adapted.
- License: MIT. The verbatim upstream `LICENSE` ships as `LICENSE.upstream-skill-judge`, renamed from
  skill-review's `LICENSE.upstream` because this package's `LICENSE.upstream` already carries the
  sanyuan0704 license. It MUST travel with the skill when it is redistributed or re-deployed. Upstream
  publishes no `NOTICE` file.
- License verification: on 2026-08-27, `gh api repos/softaworks/agent-toolkit/license` reported `MIT`, and the
  `LICENSE` blob itself was fetched and copied byte-for-byte. An earlier inlined copy had omitted the copyright
  line and was replaced that day.

skill-review retained the upstream skill's purpose and its concern for actionable review, progressive
disclosure, workflow fit, and concrete evidence, and replaced its fixed structural rubric with a contract-based
review that separates validity, design judgment, and behavioral evidence. Material changes from upstream:

- Cut the philosophy preamble ("what is a Skill", training-cost tables, the hot-swappable-LoRA analogy) as
  material the model already holds.
- Removed the ASCII-art boxes, folding their content into tables and prose.
- Neutralized provider-specific framing so the skill is agent-agnostic.
- Consolidated the useful failure-pattern diagnoses into consequence-based questions, now in
  `references/review-lenses.md`.
- Rewrote frontmatter to the specification's top-level `license` field and retained `metadata.author`.
- Retained Expert/Activation/Recoverable/Redundant as qualitative diagnoses, cross-file consistency checks,
  freedom calibration, the acts-now/acts-safely/still-works questions, evidence legibility, and the portability
  distinctions.
- Removed the eight-dimension 120-point grade, line-weighted knowledge ratios, structural quotas, portability
  score caps, and mandatory praise.
- Added separate hard gates, consequence-based findings, readiness verdicts, proportional behavioral
  evaluation, and decision-specific metrics.

### skill-review's full evaluation influences

skill-review's 2026-09-04 revision consulted the
[Anthropic `skill-creator` package](https://github.com/anthropics/skills/tree/41bbe19d1a1a7eaab5e7bb9050a417e5c6cffc8f/skills/skill-creator)
at commit `41bbe19d1a1a7eaab5e7bb9050a417e5c6cffc8f` (Apache-2.0). It influenced the independently written
guidance for paired baselines, qualitative artifact review, optional blind comparison, and causal analysis
after comparison, now in `references/full-evaluation.md`. No Anthropic prose, code, schemas, evaluator prompts,
interface assets, or package conventions were copied or adapted. Its Claude-specific runner, viewer, fixed
counts, subagent workflow, and `.skill` packaging remain excluded.

The same revision incorporated lessons from this repository's `docs/plans/evaluation/prompt-eval-harness.md`
and `docs/evaluations/skills/technical-design-planning-initial.md`: the preflight, permission, future-turn
isolation, durable trace, failure classification, continuation, and model-allowance requirements. Those are
same-author project evidence rather than third-party material.

### skill-review's operational review and lean execution

Mohammad Bayat's
[Designing Large Agent Skills as Deterministic, Phase-Oriented Systems](https://www.okbayat.com/writing/essays/phase-oriented-agent-skills-en)
(`OkBayat/OkBayat.github.io`, `docs/writing/essays/phase-oriented-agent-skills-en.md`, commit
`9d0ad2e4a0a3793c10335b387b5a3f3d16c41f3b`, consulted 2026-09-15) influenced skill-review's operational-contract,
recovery, loading, and preservation review criteria through the skill-forge changes recorded above under
"Operational Workflow Design". The site's [rights statement](https://www.okbayat.com/about/rights) reserves
rights to original content. The review wording and cases are independently written; no source prose, code,
diagrams, or templates were copied or adapted.

## Skill-Creator Comparison Ideas (2026-09-28)

The 2026-09-28 merge revision adopted ideas from three sources, compared in this repository's
`docs/research/skill-authoring-sources/skill-creator-comparison.md`. Every sentence is independently written;
no prose, code, examples, tables, templates, or evaluator prompts were copied or adapted, so no upstream
license file is required. Each source's license is recorded for traceability, not because it governs this
expression.

### Anthropic skill-creator plugin

- Author: Anthropic
- Project: [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
- Source path: `plugins/skill-creator/skills/skill-creator/` (`SKILL.md`, `agents/grader.md`)
- Commit: `fa59bc9037741ecfa131aa27938272605710d7b2`
- License: Apache-2.0, per `plugins/skill-creator/LICENSE` and the skill's `LICENSE.txt`; no `NOTICE` file
- Ideas retained: grading that fails surface compliance, puts the burden of proof on the assertion, and checks
  the output's own claims (`references/full-evaluation.md`, "Grade the Right Layer"); bundling a helper as a
  script when traces show every run rebuilding it (`references/pro-agent.md`); stating the reason beside a
  constraint instead of capitalized emphasis (`references/writing-techniques.md`); a table of contents for
  long references (`references/authoring.md`, step 4); observing a no-skill baseline before revising
  (`references/authoring.md`, step 1). Its Claude-specific runner, subagent arms, viewer, and `.skill`
  packaging remain excluded.

This is a different repository and commit from the `anthropics/skills@41bbe19` package credited above.

### OpenAI skill-creator

- Project: [openai/skills](https://github.com/openai/skills), path `skills/.system/skill-creator/`
- Commit: `49f948faa9258a0c61caceaf225e179651397431`, the revision already credited above
- License: Apache-2.0, per that skill's `LICENSE.txt`; no `NOTICE` file
- Ideas retained: corroboration for bundling scripts that runs keep rebuilding and for a table of contents on
  long references. Its product metadata and Codex assumptions remain excluded.

### obra/superpowers writing-skills

- Author: Jesse Vincent
- Project: [obra/superpowers](https://github.com/obra/superpowers), path `skills/writing-skills/`
  (`SKILL.md`, `testing-skills-with-subagents.md`)
- Commit: `8ca22dba9a94f28898bbce59f2537ff4d87c747d`
- License: MIT, `Copyright (c) 2025 Jesse Vincent`, per the repository's root `LICENSE`
- Ideas retained: matching the guidance form to the failure it prevents, with recipes free of nuance clauses and
  exemption clauses treated as unreliable scoping (`references/writing-techniques.md`); observing the unaided
  failure before writing guidance and dropping guidance whose control already succeeds
  (`references/authoring.md`, step 1); pressure scenarios with stacked incentives and a forced choice for
  compliance skills, and treating an agent's own suggestion for clarity as a hypothesis
  (`references/full-evaluation.md`). Its `anthropic-best-practices.md` was not used, because its license status
  is unclear. Its persuasion techniques, mandatory per-edit subagent testing, and Claude-specific paths remain
  excluded.
