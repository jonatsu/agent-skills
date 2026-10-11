# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## First-party Sources

### JGraph: draw.io `drawio` skill

- Source: <https://github.com/jgraph/drawio-mcp>, `plugins/claude-code/skills/drawio/SKILL.md`
- License: `Apache-2.0`
- Version: `c094dff49f0cb6fc227030436cf1d5264a58da5a`

The skill supplied the main ideas of the workflow: converting Mermaid to `.drawio` with the desktop CLI and its
`--layout` pass, exporting with the diagram embedded under the double extensions, filing an edge under the container
that holds both its ends, and reaching the Windows app from WSL2. Nothing was copied.

### JGraph: draw.io XML reference, style reference, and schema

- Source: <https://github.com/jgraph/drawio-mcp>, `shared/xml-reference.md`, `shared/style-reference.md`, and
  `shared/mxfile.xsd`
- License: `Apache-2.0`
- Version: `8c19abbdc3b214d6141989e5a2905defa7529902`

These files are the official description of the file format that `scripts/drawio_check.py` and
`references/xml-format.md` are written against. `references/xml-format.md` links to them; nothing was copied.

## Third-party Sources

### GitHub: awesome-copilot `draw-io-diagram-generator` skill

- Source: <https://github.com/github/awesome-copilot>, `skills/draw-io-diagram-generator/`, contributed by
  SriSatyaLokesh
- License: `MIT`
- Version: `3b2c4fb913430e6ec7ebc52a22e2aefc40015245`

The skill suggested a bundled structural validator and the defects it looks for, keeping existing cell ids and
container-relative coordinates when editing, and grid spacing for hand-placed layouts. Nothing was copied.

### GitHub: awesome-copilot `drawio` skill

- Source: <https://github.com/github/awesome-copilot>, `skills/drawio/`, contributed by parveen-dotnet
- License: `MIT`
- Version: `acdae521d2fceed7b6739e38704a7f8288a119d2`

The skill suggested decoding compressed pages before working on a diagram and giving color a meaning rather than
using it as decoration. Nothing was copied.
