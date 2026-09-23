# Attributions

## Current merged skill

- Skill: `ast-grep`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: adapted from upstream and materially modified

## Original authors and source

- Original author: Herrington Darkholme
- Upstream project: <https://github.com/ast-grep/agent-skill>
- Source paths: `ast-grep/skills/ast-grep/SKILL.md`,
  `ast-grep/skills/ast-grep/references/rule_reference.md`, and `ast-grep/skills/outline/SKILL.md`
- Source commit: `affe2b9b7c608f4e354d7e83d0583ed35e845650` (2026-09-09)

The upstream repository ships no `LICENSE` file. It declares MIT in `ast-grep/.claude-plugin/plugin.json` and
in its README ("This skill follows ast-grep's MIT license for any included documentation or examples").
`LICENSE.upstream` is therefore the MIT license text from the ast-grep project itself,
<https://github.com/ast-grep/ast-grep>, retrieved 2026-09-12.

## Additional source influence

- Official ast-grep documentation: [AI prompting](https://ast-grep.github.io/advanced/prompting),
  [rule catalog](https://ast-grep.github.io/catalog/), [Python catalog](https://ast-grep.github.io/catalog/python/),
  and [outline guide](https://ast-grep.github.io/guide/outline-code), read at documentation source commit
  `47a2c45821c05e8d8ec820cbab03f46c54ce3aa5` on 2026-09-23. These sources influenced the compact
  structural-query triggers, the selected Python examples, and outline routing.
- [`ast-grep-mcp/ast-grep.mdc`](https://github.com/ast-grep/ast-grep-mcp/blob/149e20d47bb7125fb0c1451feea2f48a98742034/ast-grep.mdc),
  read at commit `149e20d47bb7125fb0c1451feea2f48a98742034` on 2026-09-23. Its iterative rule-development
  process reinforced the example-first, decompose, test, simplify, and inspect-tree workflow. The skill
  expresses that process through the CLI and does not require the MCP server.

Both additional repositories are MIT-licensed. The documentation repository's 2022 notice matches the
existing `LICENSE.upstream`; the MCP repository's 2024 notice is preserved in `LICENSE.ast-grep-mcp`.

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
- The former `ast-grep-outline` package was adapted from the same upstream commit, then merged here on
  2026-09-23. Its staged-reading model, five navigation routes, argument guide, and limits now live in
  `references/outline.md`; its separate package and identical upstream license copy were retired.
- Every outline flag and default was re-verified against ast-grep 0.45.3 on 2026-09-12. The former package
  added the `--lang` requirement for stdin and made the top-level/member `--type` distinction explicit.
- The Markdown outline branch was independently measured locally against 0.45.3 on 2026-09-13. Upstream's
  outline package was code-only; this repository added heading navigation and the block-only matching limit.
- Description and main instructions were rewritten on 2026-09-23 to cover mapping, searching, and rewriting
  in one package while keeping the frequently loaded core short.
- The Python API-migration and generator-expression examples in `references/examples.md` are adapted from
  the official catalog. The async-without-error-handling example is independently expressed from the
  official prompting page's use case and the skill's existing relational-rule guidance.
- Upstream's "Common Use Cases" examples were folded into the reference rather than duplicated in `SKILL.md`;
  the reference's overlapping prose was condensed into tables.
- `references/rule_reference.md` renamed to `references/rule-reference.md` for this repository's naming, and
  reflowed to its 120-column Markdown ceiling.
- Frontmatter `license`, `compatibility` and `metadata.author` added per this repository's skill-forge policy.
