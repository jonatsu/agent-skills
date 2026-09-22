# Attributions

## Current Skill

- Skill: `document-conversion`, named `markitdown` until 2026-09-13
- Current author: Joonas Onatsu
- Current license: MIT, inherited from the upstream package
- Status: vendored from upstream, adapted locally, then rescoped to route between two converters

The package was renamed on 2026-09-13 when `anydoc` joined it. The skill had covered MarkItDown alone; it now
owns the conversion decision itself, and MarkItDown is one of the two implementations behind it. Every file
below predates that rename except where the anydoc section says otherwise.

## Upstream Source

- Original author: K-Dense Inc.
- Upstream project: [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)
- Source path: `skills/markitdown/`
- Source revision: `4226ca8052b89b471ab4eedead6e04b0b6aa08ef`
- Source license: MIT, verbatim in `LICENSE.upstream`
- Relationship: vendored and adapted

The upstream repository was reachable as `k-dense-ai/claude-scientific-skills` when this package was first
deployed on that revision; GitHub now redirects that name to the one above.

Every file in this package originated upstream except `references/markitdown_setup.md`, written here on
2026-09-13. It was deployed from that pinned revision through Kasetto
until 2026-09-13, when a review moved it into this repository so that the repository's own skill validators
would cover it and its defects could be repaired. Later upstream revisions add citation behavior unrelated to
document conversion and are deliberately not tracked.

Local changes since the vendored revision:

- Installation and examples target MarkItDown 0.1.7 rather than 0.1.6, and instructions no longer assume a
  dedicated virtual environment when a compatible `markitdown` is already on `PATH`.
- Bundled scripts are invoked through an explicitly resolved skill root rather than a bare relative path.
- References to sibling skills that exist only in the upstream collection are removed.
- `references/migration.md`, covering 0.0.x-to-0.1.6 history, and the Azure sections of
  `references/cloud_and_ocr.md` are dropped as unused here.
- The 2026-09-13 rescope moved MarkItDown's installation material out of `SKILL.md` into the locally written
  `references/markitdown_setup.md`, so the routing decision reaches the reader first, and generalized
  `scripts/inspect_installation.py` to report both converters rather than MarkItDown alone.

## Influencing Source — anydoc's Own Skill

- Original author: Firecrawl
- Source: [firecrawl/anydoc](https://github.com/firecrawl/anydoc), `skills/convert-documents-to-markdown/`
- Source license: MIT
- Relationship: read and reviewed, ideas adopted; no wording, structure, or code copied

That package was reviewed on 2026-09-13 before this skill gained its anydoc section, and the review returned
`not ready` for adoption here: its OCR rule told the agent to retry a failed conversion against a hosted
service without stating that the whole document leaves the machine, and it duplicated this skill's job. It
was therefore not vendored.

Two of its ideas were adopted, and neither is recoverable from `anydoc --help`:

- write a large conversion to a file and read the parts needed, rather than streaming it all into context;
- prefer the language binding to the CLI when working inside a Node, Python, or Rust codebase.

The anydoc prose here was written from `anydoc --help` and from behavior measured against 0.2.4 on
2026-09-13, so no upstream expression is reproduced and no second `LICENSE.upstream` is owed.

## Underlying Software

Both are documented subjects of this skill rather than sources it draws from.

| Project                                                         | Verified against                                                      |
| --------------------------------------------------------------- | --------------------------------------------------------------------- |
| [microsoft/markitdown](https://github.com/microsoft/markitdown) | release `v0.1.7` and PyPI, during the 2026-09-13 review               |
| [firecrawl/anydoc](https://github.com/firecrawl/anydoc)         | 0.2.4, crates.io, npm, and the GitHub release assets, same-day review |

Both upstream projects supply behavior this skill describes. Their documentation was read to verify the API
surfaces, extras, exit codes, release dates, and package versions asserted here. No Microsoft or Firecrawl
prose, code, or assets are copied into this package.

## Influencing Source — pdf-inspector

- Original author: Firecrawl
- Source: [firecrawl/pdf-inspector](https://github.com/firecrawl/pdf-inspector)
- Source revision: `v1.23.0` (`7a3401129cfc647816fa469d4ee6d153e5a793aa`)
- Source license: MIT
- Relationship: documentation influenced independently written guidance; no wording, code, or assets copied

The repository documentation was evaluated on 2026-09-22 before pdf-inspector became the third branch in this
skill's routing table. It established the boundary between anydoc's embedded PDF path and pdf-inspector's
standalone classification, page selection, positioned text, region extraction, and selective local OCR APIs.
It also supplied the page-index, coordinate-frame, OCR-runtime, model-download, and hosted-fallback boundaries
recorded in `references/pdf_inspector.md`.

## Influencing Source — writing-for-agents

- Original author: Matt Pocock
- Source: [mattpocock/skills](https://github.com/mattpocock/skills),
  `skills/productivity/writing-for-agents/`
- Source revision: `c55ee46073ed923f86ce59a5eb3b6d895095d1b7`
- Source license: MIT
- Relationship: writing principles applied to independently written guidance; no wording, code, or assets copied

The source was read on 2026-09-22 at the user's direction. Its context-pointer, information-hierarchy,
co-location, completion-criterion, single-source, and pruning principles shaped this revision. They kept
converter selection in `SKILL.md`, moved pdf-inspector branch detail behind one conditional pointer, and gave
the reference checkable completion criteria.

Both new sources influenced independently written guidance. The existing `LICENSE.upstream` remains the
license of the originally vendored K-Dense package; no material from either source was copied or redistributed,
so neither license text is added as another upstream file.
