# Attributions

## Current skill

- Skill: `ast-grep-outline`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: adapted from upstream with light modification

## Original authors and source

- Original author: Herrington Darkholme
- Upstream project: <https://github.com/ast-grep/agent-skill>
- Source path: `ast-grep/skills/outline/SKILL.md`
- Source commit: `affe2b9b7c608f4e354d7e83d0583ed35e845650` (2026-09-09)

The upstream repository ships no `LICENSE` file. It declares MIT in `ast-grep/.claude-plugin/plugin.json` and
in its README ("This skill follows ast-grep's MIT license for any included documentation or examples").
`LICENSE.upstream` is therefore the MIT license text from the ast-grep project itself,
<https://github.com/ast-grep/ast-grep>, retrieved 2026-09-12.

## Adaptation note

The body is substantially upstream's: the staged reading model, the five use cases with their commands, the
argument guide, and the limits section.

Material changes:

- Every flag and default re-verified against `ast-grep outline --help` at 0.45.3 on 2026-09-12.
- **Added:** `--lang` is required for stdin input, which upstream's argument guide omits.
- **Added:** the note that filtering by a member type such as `method` returns nothing at the top level, made
  explicit rather than implied.
- Description rewritten to state the triggering situations and to route pattern matching and rewriting to the
  sibling `ast-grep` skill.
- Directory renamed from `outline` to `ast-grep-outline` to match the frontmatter name, since skill names must
  be unique across every domain in this repository.
- Frontmatter `license`, `compatibility` and `metadata.author` added per this repository's skill-forge policy.
