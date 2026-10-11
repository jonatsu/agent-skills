# Attributions

- Author: Joonas Onatsu
- License: `MIT`

The package adapts upstream material, whose MIT license requires its notice to travel with the material; keep
`LICENSE.upstream` with the skill. The upstream agent-skill repository ships no license file and declares MIT in its
metadata, so `LICENSE.upstream` holds the MIT notice of the ast-grep project itself. `LICENSE.ast-grep-mcp` holds the
notice of the MCP repository.

## First-party Sources

### Herrington Darkholme: ast-grep agent skill

- Source: <https://github.com/ast-grep/agent-skill>, `ast-grep/skills/ast-grep/SKILL.md`,
  `ast-grep/skills/ast-grep/references/rule_reference.md`, and `ast-grep/skills/outline/SKILL.md`
- License: `MIT`
- Version: `affe2b9b7c608f4e354d7e83d0583ed35e845650`

The workflow, rule taxonomy, `stopBy: end` guidance, metavariable rules, and debugging checklist are adapted from the
upstream skill and rewritten around the skill's own structure. The outline reference is adapted from the upstream
outline skill.

### Herrington Darkholme: ast-grep documentation

- Source: <https://ast-grep.github.io/>, the [AI prompting](https://ast-grep.github.io/advanced/prompting),
  [rule catalog](https://ast-grep.github.io/catalog/), [Python catalog](https://ast-grep.github.io/catalog/python/),
  and [outline guide](https://ast-grep.github.io/guide/outline-code) pages
- License: `MIT`
- Version: `47a2c45821c05e8d8ec820cbab03f46c54ce3aa5`

The pages shaped the structural-query triggers and the outline routing. The Python API-migration and
generator-expression examples in `references/examples.md` are adapted from the catalog.

### Herrington Darkholme: ast-grep MCP server

- Source: <https://github.com/ast-grep/ast-grep-mcp>, `ast-grep.mdc`
- License: `MIT`
- Version: `149e20d47bb7125fb0c1451feea2f48a98742034`

The rule file's iterative rule-development process shaped the skill's example-first, decompose, test, simplify, and
inspect-tree workflow, which the skill expresses through the CLI. Nothing was copied.
