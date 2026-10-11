# Attributions

- Author: Joonas Onatsu
- License: `MIT`

The package vendors and adapts upstream material, whose MIT license requires its notice to travel with the material;
keep `LICENSE.upstream` with the skill.

## First-party Sources

### Microsoft: MarkItDown

- Source: <https://github.com/microsoft/markitdown>
- License: `MIT`
- Version: tag `v0.1.7`

The MarkItDown guidance, covering its Python API surface, optional extras, exit codes, and MCP server, is checked
against this release and its documentation. No prose, code, or assets were copied.

### Firecrawl: anydoc

- Source: <https://github.com/firecrawl/anydoc>
- License: `MIT`
- Version: tag `v0.2.4`

The anydoc guidance, covering its formats, exit codes, OCR-required behavior, and language bindings, is built on this
release's documentation and measured behavior. No prose, code, or assets were copied.

### Firecrawl: pdf-inspector

- Source: <https://github.com/firecrawl/pdf-inspector>
- License: `MIT`
- Version: tag `v1.23.0` (`7a3401129cfc647816fa469d4ee6d153e5a793aa`)

The repository documentation supplied the boundary between anydoc's embedded PDF path and pdf-inspector's standalone
classification, page selection, positioned text, region extraction, and selective local OCR APIs. It also supplied the
page-index, coordinate-frame, OCR-runtime, and model-download contracts in `references/pdf_inspector.md`. No prose,
code, or assets were copied.

## Third-party Sources

### K-Dense Inc.: `markitdown` skill

- Source: <https://github.com/K-Dense-AI/scientific-agent-skills>, `skills/markitdown/`
- License: `MIT`
- Version: `4226ca8052b89b471ab4eedead6e04b0b6aa08ef`

Vendored and adapted: the MarkItDown guidance is this skill, adapted to the installed release and to this
repository's skill policy, within a package that routes among three converters.

### Firecrawl: `convert-documents-to-markdown` skill

- Source: <https://github.com/firecrawl/anydoc>, `skills/convert-documents-to-markdown/`
- License: `MIT`
- Version: read 2026-09-13

The skill supplied two ideas: write a large conversion to a file and read only the parts needed, and prefer the
language binding to the CLI inside a Node, Python, or Rust codebase. Nothing was copied.

### Matt Pocock: `writing-for-agents` skill

- Source: <https://github.com/mattpocock/skills>, `skills/productivity/writing-for-agents/`
- License: `MIT`
- Version: `c55ee46073ed923f86ce59a5eb3b6d895095d1b7`

The skill's writing principles shaped how the guidance is arranged: converter selection stays in `SKILL.md`, branch
detail sits behind one conditional pointer, and each reference states checkable completion criteria. Nothing was
copied.
