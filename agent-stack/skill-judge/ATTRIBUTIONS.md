# Attributions

## Current skill

- Skill: `skill-judge`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: adapted from upstream and materially trimmed

## Original author and source

- Original author: Leonardo Flores
- Copyright holder: `Copyright (c) 2026 Leonardo Flores`, as stated in upstream's
  `LICENSE`
- Upstream project:
  [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit)
- Source path: `skills/skill-judge`
- Source commit: `3027f20f3181758385a1bb8c022d4041dfb4de84`. **Not recorded at
  adaptation time** — this is upstream's HEAD as of 2026-08-27, dated
  2026-03-05, which predates the 2026-07-27 commit that added this skill here.
  It is therefore the commit adapted from unless upstream rewrote history.

## Adaptation note

Kept the evaluation instrument: the eight scored dimensions (D1–D8), the
120-point total and grade scale, the Expert/Activation/Redundant knowledge-ratio
scan, the evaluation protocol, the report template, and the failure-pattern
catalog.

Material changes from the upstream skill:

- Cut the ~40-line philosophy preamble ("what is a Skill", training-cost tables,
  hot-swappable-LoRA analogy) as material the model already holds. Replaced with a
  two-line statement of intent. This originally cross-referenced a sibling skill for
  vocabulary; those pointers were removed on 2026-08-27, because that skill sets
  `disable-model-invocation: true` and so cannot be reached from here. Every term is
  now defined in place.
- Removed the ASCII-art boxes (activation-flow diagram, quick-check panel),
  folding their content into tables and prose.
- Neutralized provider-specific framing ("Claude" → "the agent/model") so the
  skill is agent-agnostic.
- Rewrote the failure patterns as a standalone diagnosis catalogue, each entry naming
  the dimension it hits. It briefly borrowed a sibling skill's vocabulary; that was
  reversed on 2026-08-27 for the reachability reason above, and the catalogue moved to
  `references/failure-patterns.md`.
- Rewrote frontmatter to this repo's conventions (`metadata.author` /
  `metadata.license`) and added an Iron Law.

## Upstream license

MIT. The verbatim upstream `LICENSE` ships beside this file as
`LICENSE.upstream` and MUST travel with the skill when it is redistributed or
re-deployed. Upstream publishes no `NOTICE` file, so there is no
`NOTICE.upstream`.

The licence text was previously inlined here **without its copyright line**,
which made it neither a verbatim reproduction nor compliant with MIT's own
requirement that the copyright notice travel with the software. Replaced on
2026-08-27 with the byte-for-byte file.

Verified against the primary source on 2026-08-27 — `gh api
repos/softaworks/agent-toolkit/license` reported `MIT`, and the `LICENSE` blob
itself was fetched and copied byte-for-byte. `gh repo view --json licenseInfo`
was NOT used; it misreports repositories that do carry a licence.
