# Attributions

- Author: Joonas Onatsu
- License: `MIT`

This package is a modified version of two MIT-licensed upstream skills, whose licenses require their copyright and
permission notices to travel with the material: keep `LICENSE.upstream` and `LICENSE.upstream-skill-judge` with the
skill. The bundled validator keeps its Apache-2.0 license text at `scripts/skills-ref/LICENSE`.

## First-party Sources

### Agent Skills project: `skills-ref` validator

- Source: <https://github.com/agentskills/agentskills>, `skills-ref`
- License: `Apache-2.0`
- Version: `69ef37e9424c0a7ea9dd2293b559e43ec8176379`

Vendored as `scripts/skills-ref`, with upstream tests and development environment artifacts omitted. The runtime source
and project files are unmodified.

### Agent Skills project: skill-creation guidance

- Source: <https://agentskills.io/skill-creation/best-practices>, with the sibling pages `optimizing-descriptions`,
  `evaluating-skills`, and `using-scripts`; files under `docs/skill-creation/` in
  <https://github.com/agentskills/agentskills>
- License: `CC-BY-4.0`
- Version: `69ef37e9424c0a7ea9dd2293b559e43ec8176379`

The four official pages supplied the condensed authoring guidance on skill structure, description quality, output
evaluation, and bundled scripts. The guidance is reorganized and adapted to this skill's workflow and terminology, and
the pages are not reproduced verbatim.

## Third-party Sources

### Shawn Yang (sanyuan0704): `skill-forge` skill

- Source: <https://github.com/sanyuan0704/sanyuan-skills>, `skills/skill-forge`
- License: `MIT`
- Version: `ae75e917a003fb1dcfd6986b8728f94da7de6a6a`

Adapted: this package derives from the upstream skill, materially rewritten for portable Agent Skills authoring.

### Leonardo Flores: `skill-judge` skill

- Source: <https://github.com/softaworks/agent-toolkit>, `skills/skill-judge`
- License: `MIT`
- Version: read on or before 2026-08-21

Adapted: the review mode (`references/review.md`, `references/review-lenses.md`, and `references/rubric.md`) retains the
upstream skill's concern for actionable review, progressive disclosure, workflow fit, and concrete evidence.

### mizchi: `optimizing-descriptions` skill

- Source: <https://github.com/mizchi/skills>, `optimizing-descriptions/SKILL.md`
- License: `MIT`
- Version: `a41865b34b78f2675a6c73178377a5bcc1b492c6`

The skill supplied the distinction between agent selection and deliberate invocation, which shaped the initial
authoring guidance. Nothing was copied.

### OpenAI: `skill-creator` skill

- Source: <https://github.com/openai/skills>, `skills/.system/skill-creator/`
- License: `Apache-2.0`
- Version: `49f948faa9258a0c61caceaf225e179651397431`

The skill supplied the method of deriving resources from concrete execution needs, the explanation of context cost,
the rule that instruction precision should follow task fragility, and corroboration for bundling scripts that runs keep
rebuilding. The ideas are expressed independently, and nothing was copied.

### Anthropic: `skill-creator` skill

- Source: <https://github.com/anthropics/skills>, `skills/skill-creator/`
- License: `Apache-2.0`
- Version: `41bbe19d1a1a7eaab5e7bb9050a417e5c6cffc8f`

The skill supplied the rule that consequential behavior must match a skill's described purpose, the core-versus-adapter
portability boundary, and the full-evaluation guidance on paired baselines, qualitative artifact review, optional blind
comparison, and causal analysis after comparison. The ideas are expressed independently, and nothing was copied.

### Anthropic: `skill-creator` plugin

- Source: <https://github.com/anthropics/claude-plugins-official>, `plugins/skill-creator/skills/skill-creator/`
- License: `Apache-2.0`
- Version: `fa59bc9037741ecfa131aa27938272605710d7b2`

The plugin supplied grading that fails surface compliance and puts the burden of proof on the assertion, bundling a
helper as a script when runs keep rebuilding it, stating the reason beside a constraint, a table of contents for long
references, and observing a no-skill baseline before revising. The ideas are expressed independently, and nothing was
copied.

### Jesse Vincent: superpowers `writing-skills` skill

- Source: <https://github.com/obra/superpowers>, `skills/writing-skills/`
- License: `MIT`
- Version: `8ca22dba9a94f28898bbce59f2537ff4d87c747d`

The skill supplied the matching of guidance form to the failure it prevents, observing the unaided failure before
writing guidance, and pressure scenarios with stacked incentives for compliance skills. The ideas are expressed
independently, and nothing was copied.

### Shubhamsaboo: `awesome-llm-apps` skill linter

- Source: <https://github.com/Shubhamsaboo/awesome-llm-apps>, `agent_skills/evals/tools/skill_lint.py`
- License: `Apache-2.0`
- Version: `ca8e5b3c56e51e336449a99d79b42b45ea690b86`

The linter supplied two ideas for the bundled-reference check in `scripts/quick_validate.py`: collecting both Markdown
link targets and bare paths under the bundled resource directories, and stripping fenced code blocks first. The
implementation is independently written, and no code or wording was copied.

### Mohammad Bayat: "Designing Large Agent Skills as Deterministic, Phase-Oriented Systems"

- Source: <https://www.okbayat.com/writing/essays/phase-oriented-agent-skills-en>,
  `docs/writing/essays/phase-oriented-agent-skills-en.md` in <https://github.com/OkBayat/OkBayat.github.io>
- License: `LicenseRef-Proprietary`
- Version: `9d0ad2e4a0a3793c10335b387b5a3f3d16c41f3b`

The site's rights statement (<https://www.okbayat.com/about/rights>) reserves all rights. The essay supplied the idea
of operational design as a conditional authoring obligation: explicit state authority, enforcement ownership,
completion evidence, and recovery behavior. It also supplied the lean-execution default and preservation of behavior
before substantial workflow revisions. Nothing was
copied.

### ISO: ISO 24495-1:2023, Plain language, Part 1: Governing principles and guidelines

- Source: <https://www.iso.org/standard/78907.html>, preview of clauses 1 to 5.2.3 at
  <https://cdn.standards.iteh.ai/samples/78907/d194fac21d6a45f38bfcfec9657f7498/ISO-24495-1-2023.pdf>
- License: `LicenseRef-Proprietary`
- Version: first edition, 2023-06

ISO holds the copyright, and the standard is not free to redistribute.
The plain-language paragraph in the authoring mode restates its definition of plain
language, which the International Plain Language Federation also publishes. No other text was copied.

### ASD: ASD-STE100 Simplified Technical English

- Source: <https://www.asd-ste100.org/>
- License: `LicenseRef-Proprietary`
- Version: Issue 9, 2025-01-15

ASD holds the copyright, and the standard is free to obtain but not free to redistribute. It informed the
sentence limits and the condition before its command. The skill does not implement the standard, and no rule
text was copied.
