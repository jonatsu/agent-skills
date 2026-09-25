# Attributions

## Current skill

- Skill: `skill-forge`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: adapted from upstream and materially modified

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
