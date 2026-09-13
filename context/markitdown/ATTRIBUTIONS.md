# Attributions

## Current Skill

- Skill: `markitdown`
- Current author: Joonas Onatsu
- Current license: MIT, inherited from the upstream package
- Status: vendored from upstream and adapted locally

## Upstream Source

- Original author: K-Dense Inc.
- Upstream project: [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)
- Source path: `skills/markitdown/`
- Source revision: `4226ca8052b89b471ab4eedead6e04b0b6aa08ef`
- Source license: MIT, verbatim in `LICENSE.upstream`
- Relationship: vendored and adapted

The upstream repository was reachable as `k-dense-ai/claude-scientific-skills` when this package was first
deployed on that revision; GitHub now redirects that name to the one above.

Every file in this package originates upstream. It was deployed from that pinned revision through Kasetto
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

## Underlying Software

- Project: [microsoft/markitdown](https://github.com/microsoft/markitdown)
- Relationship: the documented subject, verified against release `v0.1.7` and PyPI during the 2026-09-13
  review

The upstream project supplies the behavior this skill describes. Its documentation was read to verify the
API surface, extras, release dates, and package versions asserted here. No Microsoft prose, code, or assets
are copied into this package.
