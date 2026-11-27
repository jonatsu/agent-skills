# Attributions

- Author: Joonas Onatsu
- License: `MIT`

The package adapts upstream material whose MIT license requires its notice to travel with the material; keep
`LICENSE.upstream` with the skill.

## Third-party Sources

### Addy Osmani: agent-skills `code-reviewer` agent

- Source: <https://github.com/addyosmani/agent-skills>, `agents/code-reviewer.md`
- License: `MIT`
- Version: `2686b620fc1fed2e8f60c704839c766b8594c6b6`

The agent supplied the correctness checks, reading the task and then the tests before the code, the Critical,
Required, and Optional tiers, the verdict, and the verification part of the report. Its structure and some
phrases were adapted; the prose was rewritten.

### Anthropic: claude-plugins-official `pr-review-toolkit` `code-reviewer` agent

- Source: <https://github.com/anthropics/claude-plugins-official>,
  `plugins/pr-review-toolkit/agents/code-reviewer.md`
- License: `Apache-2.0`
- Version: `fa59bc9037741ecfa131aa27938272605710d7b2`

The agent supplied the 0 to 100 confidence rating with 80 as the report threshold, instruction-file compliance
as a review check, and the working-tree diff as the default scope. No text was copied.

### FerroxLabs: wayland `code-reviewer` skill and agent

- Source: <https://github.com/FerroxLabs/wayland>,
  `src/process/resources/skills-library/bodies/skills/software-engineering/code-reviewer/SKILL.md` and
  `src/process/resources/skills-library/bodies/agents/engineering/code-reviewer/SKILL.md`
- License: `AGPL-3.0-or-later`
- Version: `4c030c7b01c241df7b6e3535635a970f10d781af`

The repository's `package.json` declares the licence, and each file's frontmatter claims Apache-2.0. The two files
supplied four ideas: checking that the APIs model-written code calls exist, checking what a change leaves out or
deletes, checking a generated file against its source, and naming each missing test. Every rule was written
independently, and no text or code was copied.
