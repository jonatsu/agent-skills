# Attributions

## Current Skill

- Skill: `conformance-review`, named `spec-conformance-review` until 2026-10-04
- Current author: Joonas Onatsu
- Current license: MIT
- Status: original implementation with independently expressed idea-level influence

## Warp `check-impl-against-spec`

- Upstream publisher: Warp
- Copyright holder: Denver Technologies, Inc.
- Upstream project: [warpdotdev/common-skills](https://github.com/warpdotdev/common-skills)
- Source path:
  [`.agents/skills/check-impl-against-spec/SKILL.md`](https://github.com/warpdotdev/common-skills/blob/f3b58c81d1cfd5d8eabf2e32edb32db2b0573923/.agents/skills/check-impl-against-spec/SKILL.md)
- Source revision: `f3b58c81d1cfd5d8eabf2e32edb32db2b0573923`, inspected 2026-09-11
- Source license:
  [MIT](https://github.com/warpdotdev/common-skills/blob/f3b58c81d1cfd5d8eabf2e32edb32db2b0573923/LICENSE)
- Relationship: idea-level influence, independently expressed

The source informed material rather than literal comparison, checking missing behavior, contradictions, unplanned
scope, and omitted validation or migration, accepting harmless implementation variation, and folding findings into an
active review without manufacturing alignment comments.

This skill independently replaces Warp's fixed `spec_context.md`, `pr_diff.txt`, `pr_description.md`, and `review.json`
contract with repository-discovered artifacts and portable output. It separates requirements, technical design, and
implementation-plan authority; compares resulting state and behavioral evidence as well as a diff; classifies the source
of drift; and supports working-tree, pull-request, release, and post-deployment reviews.

No upstream prose, examples, code, templates, or assets are copied, adapted, translated, or vendored. The repository's
MIT license applies to this independently written skill, so no `LICENSE.upstream` is required.

## Addy Osmani, “How to write a good spec for AI agents”

- Original author: Addy Osmani
- Source: [addyosmani.com/blog/good-spec/](https://addyosmani.com/blog/good-spec/)
- Published: 2026-01-13; read 2026-09-11
- Source license: no reuse license stated on the page; not relied on
- Relationship: idea-level influence, independently expressed

The article informed conformance checks as the return path from implementation evidence to a living specification. This
skill retains no source prose, examples, images, templates, code, or assets.
