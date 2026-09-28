# Attributions

## Current Skill

- Skill: `brooks-review`
- Current author: hyhmrright (vendored, deployment transforms only)
- Current license: MIT, inherited from the upstream package
- Status: vendored from upstream, deployment-adapted (paths and description shape)

## Upstream Source

- Original author: hyhmrright
- Upstream project: [hyhmrright/brooks-lint](https://github.com/hyhmrright/brooks-lint)
- Source path: `skills/brooks-review/`
- Source revision: `29fd7761cdb59a1bd9d2b5b6458277807c674c4f`
- Source license: MIT, verbatim in `LICENSE.upstream`
- Relationship: vendored

## Vendored Files

The skill body and guides originate upstream unchanged except for the deployment
transforms below. The shared framework files under `references/` are copied
verbatim from the upstream `skills/_shared/` directory:

- `common.md`
- `source-coverage.md`
- `decay-risks.md`
- `test-decay-risks.md`
- `remedy-guide.md`
- `custom-risks-guide.md`

## Deployment Transforms Applied On Import

- The folded YAML `description` scalar was collapsed to a single double-quoted
  physical line, because Kasetto reads skill descriptions linewise and a folded
  scalar would deploy as the block marker rather than the text.
- `../_shared/<file>` references were rewritten to `references/<file>`, and the
  whole upstream `_shared/` set was vendored into this package's `references/`
  directory, because this repository deploys each skill as a flat, self-contained
  package with no shared sibling directory.
- `license: MIT` and `metadata.author` were added to frontmatter per this
  repository's skill-authoring policy.
