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
- scaling workflows and evaluation to the change instead of requiring every upstream technique; and
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
