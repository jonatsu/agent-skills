# Attributions

## Current skill

- Skill: `ast-grep`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: adapted from upstream and materially modified

## Original authors and source

- Original author: Herrington Darkholme
- Upstream project: <https://github.com/ast-grep/agent-skill>
- Source paths: `ast-grep/skills/ast-grep/SKILL.md`, `ast-grep/skills/ast-grep/references/rule_reference.md`
- Source commit: `affe2b9b7c608f4e354d7e83d0583ed35e845650` (2026-09-09)

The upstream repository ships no `LICENSE` file. It declares MIT in `ast-grep/.claude-plugin/plugin.json` and
in its README ("This skill follows ast-grep's MIT license for any included documentation or examples").
`LICENSE.upstream` is therefore the MIT license text from the ast-grep project itself,
<https://github.com/ast-grep/ast-grep>, retrieved 2026-09-12.

## Adaptation note

Upstream's workflow, rule taxonomy, `stopBy: end` guidance, metavariable rules, and debugging checklist are
retained; both files are reorganized and rewritten around them.

Material changes:

- Every documented flag and output claim re-verified against ast-grep 0.45.3 on 2026-09-12.
- **Corrected:** upstream's `--json` example shows `$$$REST` capturing `[1, 2]`. The real output also includes
  the unnamed separator nodes, so `console.log($ARG, $$$REST)` over `console.log("value", 1, 2)` yields three
  `multi` entries — `1`, `,`, `2`. The skill now states this.
- **Corrected:** the reference's troubleshooting list told the reader to use `dump_syntax_tree`, an MCP tool
  name with no CLI equivalent. Replaced with `--debug-query=cst`.
- **Added:** a Rewriting section, absent upstream — `run --rewrite`, a rule's `fix:` field, the preview-by-
  default behavior of both, `--update-all` and `--interactive`, and the `ast-grep new` / `ast-grep test`
  scaffolding. Verified by execution.
- Description rewritten to cover rewriting as well as search and to route structural mapping to the sibling
  `ast-grep-outline` skill.
- Upstream's "Common Use Cases" examples were folded into the reference rather than duplicated in `SKILL.md`;
  the reference's overlapping prose was condensed into tables.
- `references/rule_reference.md` renamed to `references/rule-reference.md` for this repository's naming, and
  reflowed to its 120-column Markdown ceiling.
- Frontmatter `license`, `compatibility` and `metadata.author` added per this repository's skill-forge policy.
