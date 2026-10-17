# Attributions

- Author: Joonas Onatsu
- License: `MIT`

The package adapts upstream material licensed `MIT`, which requires its copyright and permission notice to travel
with the material. The notice is reproduced under "Upstream License Notice".

## Third-party Sources

### Pete Pei: `tech-writing` skill

- Source: <https://github.com/peizh/tech-writing>, `SKILL.md`
- License: `MIT`
- Version: read on or before 2026-08-21

Adapted and trimmed: this skill is built on its structure, workflow, and checklists, including the
document-composition job, the task taxonomy, examples, accessibility and error-recovery guidance, and response
modes.

### VoltAgent: `technical-writer` subagent

- Source: <https://github.com/VoltAgent/awesome-claude-code-subagents>,
  `categories/08-business-product/technical-writer.md`
- License: `MIT`
- Version: read on or before 2026-08-21

The subagent supplied the documentation-type taxonomy and a couple of review-checklist items. Nothing else was
taken, and no text was copied.

### Cursor: `pstack` `technical-writing` skill

- Source: <https://github.com/cursor/plugins>, `pstack/skills/technical-writing/SKILL.md`
- License: `MIT`
- Version: `7314f723a487ec406b6369fe5865ba034cfed166`

One of three skills that informed the reader-outcome framing, the document-mode distinctions, tutorial checkpoints,
and implementation placement guidance. Nothing was copied.

### awesomekoder: awesome-llm-apps `technical_writer` skill

- Source: <https://github.com/awesomekoder/awesome-llm-apps>, `awesome_agent_skills/writing/technical_writer.md`
- License: `Apache-2.0`
- Version: `1fcfb4fab8e20f8b543189059de2fac6d0e71720`

One of three skills that informed the reader-outcome framing, the document-mode distinctions, tutorial checkpoints,
and implementation placement guidance. Nothing was copied.

### Mindrally: skills `technical-writing` skill

- Source: <https://github.com/Mindrally/skills>, `technical-writing/SKILL.md`
- License: `Apache-2.0`
- Version: read on or before 2026-09-03

One of three skills that informed the reader-outcome framing, the document-mode distinctions, tutorial checkpoints,
and implementation placement guidance. Nothing was copied.

### Mohit Aggarwal: pm-claude-skills `house-style-enforcer` skill

- Source: <https://github.com/mohitagw15856/pm-claude-skills>, `skills/house-style-enforcer/SKILL.md`
- License: `MIT`
- Version: read on or before 2026-09-03

The skill suggested the exemplar-evidence approach behind "Match an Established House Style". Nothing was copied.

### Addy Osmani: `documentation-and-adrs` skill

- Source: <https://github.com/addyosmani/agent-skills>, `skills/documentation-and-adrs/SKILL.md`
- License: `MIT`
- Version: read on or before 2026-09-09

The skill supplied the main ideas for the decision-record section and the changelog reference: writing a record on a
cost-to-reverse trigger, a status lifecycle with superseded records kept, a rejection reason for each alternative,
and checking an existing series for its location and format before writing into it. Nothing was copied.

### Matt Pocock: `domain-modeling` skill and `ADR-FORMAT.md`

- Source: <https://github.com/mattpocock/skills>, `skills/engineering/domain-modeling/`
- License: `MIT`
- Version: `959a8e9f1edc3adbe2f7e3054bb6fbefa6696260`

The skill supplied the three-part gate for whether a decision warrants a record (hard to reverse, surprising
without context, and the result of a real trade-off) and the tiering of a record's weight to the decision's blast
radius. Nothing was copied.

### Matt Pocock: `writing-for-agents` skill

- Source: <https://github.com/mattpocock/skills>, `skills/productivity/writing-for-agents/SKILL.md`
- License: `MIT`
- Version: `c55ee46073ed923f86ce59a5eb3b6d895095d1b7`

The skill supplied the `authority map`, `locator`, and `reader-ready` leading words and checkable completion
criteria. It formerly supplied the single-owner pointer from this skill to `writing-for-humans`; the current skill
carries its own prose rules instead. Nothing was copied.

### Eren Suner: "Agent Skill for Documentation"

- Source: <https://www.skillfully.sh/blog/agent-skill-for-documentation>
- License: `LicenseRef-No-License`
- Version: published 2026-05-17

The article states no content license, so all rights remain with its author. It supplied the authority-map
workflow, explicit source-conflict handling, classification of confirmed, assumed, unknown, and conflicting
information, and delivery of unresolved evidence gaps. Nothing was copied.

### Daniele Procida: Diátaxis

- Source: <https://diataxis.fr/>, repository <https://github.com/evildmp/diataxis-documentation-framework>
- License: `CC-BY-SA-4.0`
- Version: `957c09ca40b4a1edc23874f713e01937d50d54d5`

Diátaxis supplied the four-type classification, the two classifying questions (action or understanding, study or
work), the content that typically leaks into each type, and the method of improving a set one piece at a time.
Nothing was copied due to the content license.

### Keith Patton: `diataxis-agent-skill`

- Source: <https://github.com/keithpatton/diataxis-agent-skill>
- License: `CC-BY-SA-4.0`
- Version: `5b095a5e7aebe77ce4af855809123e12d92b9efd`

The skill prompted reporting a classification with its evidence and moving leaked content out rather than blending
it. Nothing was copied due to the content license.

### Olivier Lacan: Keep a Changelog

- Source: <https://keepachangelog.com/en/1.1.0/>
- License: `MIT`
- Version: 1.1.0

The convention supplied the grouping vocabulary (added, changed, deprecated, removed, fixed, security) and the
`Unreleased` section that `references/changelog.md` describes. Nothing was copied.

### ASD: ASD-STE100 Simplified Technical English

- Source: <https://www.asd-ste100.org/>
- License: `LicenseRef-Proprietary`
- Version: Issue 9, 2025-01-15

ASD holds the copyright, and the standard is free to obtain but not free to redistribute. It informed "Write Notes
and Safety Instructions": a note carries information only, a warning marks risk of injury and a caution risk of
damage, and a safety instruction puts the signal word before the command. It also informed the procedural and
descriptive sentence classes with their limits, the condition before its command, and the six-sentence paragraph.
The skill does not implement the standard, and no rule text or dictionary entry was copied.

### ISO: ISO 24495-1:2023, Plain language, Part 1: Governing principles and guidelines

- Source: <https://www.iso.org/standard/78907.html>, preview of clauses 1 to 5.2.3 at
  <https://cdn.standards.iteh.ai/samples/78907/d194fac21d6a45f38bfcfec9657f7498/ISO-24495-1-2023.pdf>
- License: `LicenseRef-Proprietary`
- Version: first edition, 2023-06

ISO holds the copyright, and the standard is not free to redistribute. The skill restates its definition of
plain language, which the International Plain Language Federation also publishes, and builds on its four
principles. Its guideline names shaped the rules on reading context, predictive headings, separate
supplementary material, and evaluation with readers. No other text was copied.

### Thomas M. Schindler: "The Making of the International Standard for Writing in Plain Language ISO 24495-1"

- Source: <https://amwajournal.org/index.php/amwa/article/view/333>
- License: `LicenseRef-Proprietary`
- Version: AMWA Journal 39(1), 2024

The American Medical Writers Association holds the copyright. The article supplied the complete list of the
standard's guideline names, including headings that help readers predict what comes next. Nothing was copied.

### Dustin Yuchen Teng: `iso-24495-skill`

- Source: <https://github.com/danyuchn/iso-24495-skill>
- License: `MIT`
- Version: `113656b0a6a6cbeb3b3c2bb7cf3bc29349cb05cf`

The skill supplied the one-reading check in the reader-ready pass and the example of a heading that states its
message. Nothing was copied.

### Gareth Williams: `iso-24495` skills

- Source: <https://github.com/GaZmagik/iso-24495>, `skills/iso-24495-1/SKILL.md`
- License: `MIT`
- Version: `5951eb7d985018459c62428378926c07f4199794`

The skill supplied the rule that a primary audience settles conflicts between audiences, with the runbook example,
the requirement that a document work when read straight through, and the rule against carrying meaning by bold,
color, or position alone. Nothing was copied.

## Upstream License Notice

Copyright (c) 2026 Pete Pei

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
