# Attributions

## Current Skill

- Skill: `drawio-diagrams`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: original work with independently expressed idea-level influence

No prose, code, template, or asset from any source below was copied or adapted, so no `LICENSE.upstream` ships
with the package. `scripts/drawio_check.py` was written from the draw.io file format, not from either upstream
script. Every CLI behavior the skill states was checked against draw.io desktop 31.5.3 on Linux under WSL2 on
2026-09-29, with the draw.io source code and documentation as references for the format.

## jgraph `drawio` skill

- Original author: JGraph Ltd, the maintainers of draw.io
- Upstream project: <https://github.com/jgraph/drawio-mcp>
- Source path: `plugins/claude-code/skills/drawio/SKILL.md`
- Source commit: `c094dff49f0cb6fc227030436cf1d5264a58da5a`
- Source license: Apache-2.0 (repository license)
- Relationship: idea-level influence, independently expressed

It informed converting Mermaid to `.drawio` with the desktop CLI in preference to placing cells by hand; the CLI's
`--layout` pass for XML-authored diagrams; exporting with the diagram embedded under the double extensions
`.drawio.png` and `.drawio.svg`; filing an edge under the innermost container that holds both its ends; reaching
the Windows app from WSL2 through `/mnt/c`; `--disable-gpu` as the answer to a GPU-process failure; and leaving XML
comments out of generated files. Its XML and style references are linked at a pinned commit from
`references/xml-format.md` as the official source.

## awesome-copilot `draw-io-diagram-generator` skill

- Original author: SriSatyaLokesh, contributed to GitHub's awesome-copilot collection
- Upstream project: <https://github.com/github/awesome-copilot>
- Source path: `skills/draw-io-diagram-generator/`
- Source commit: `3b2c4fb913430e6ec7ebc52a22e2aefc40015245`
- Source license: MIT (repository license; the skill declares none of its own)
- Relationship: idea-level influence, independently expressed

It informed a bundled structural validator and the defects it looks for (root cells, unique ids, dangling
parents and edge endpoints, missing geometry); keeping existing cell ids and container-relative coordinates when
editing; floating edges that use `sourcePoint` and `targetPoint`; and the grid spacing and shape sizes for
hand-placed layouts. Its scripts refuse compressed pages, which is why this skill's checker decodes them instead.

## awesome-copilot `drawio` skill

- Original author: parveen-dotnet, contributed to GitHub's awesome-copilot collection
- Upstream project: <https://github.com/github/awesome-copilot>
- Source path: `skills/drawio/`
- Source commit: `acdae521d2fceed7b6739e38704a7f8288a119d2`
- Source license: MIT (repository license; the skill declares none of its own)
- Relationship: idea-level influence, independently expressed

It informed decoding compressed pages before working on a diagram, and giving color a meaning rather than using it
as decoration.
