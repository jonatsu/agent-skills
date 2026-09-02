# Attributions

## Current skill

- Skill: `skill-forge`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: adapted from upstream and materially modified

## Original authors and source

- Original author: Shawn Yang
- Copyright holder: `Copyright (c) 2025 sanyuan0704`, as stated in upstream's `LICENSE`
- Upstream project: <https://github.com/sanyuan0704/sanyuan-skills>
- Source path: `skills/skill-forge`
- Source commit: `ae75e917a003fb1dcfd6986b8728f94da7de6a6a` (dated 2026-03-02;
  upstream has since moved to `08b6572e`, 2026-05-11)

## Adaptation note

This version is derived from the upstream `skill-forge` skill and has been
materially rewritten for portable Agent Skills authoring.

Material changes include:

- treating the Agent Skills specification as the format authority;
- supporting portable and repository-specific skills;
- scaling workflows and evaluation to the change instead of requiring every
  upstream technique; and
- adding provenance, licensing, and local-policy validation.

## Upstream license

MIT. The verbatim upstream `LICENSE` ships beside this file as
`LICENSE.upstream` and MUST travel with the skill when it is redistributed or
re-deployed. Upstream publishes no `NOTICE` file, so there is no
`NOTICE.upstream`.

Verified against the primary source on 2026-08-27 — `gh api
repos/sanyuan0704/sanyuan-skills/license` reported `MIT`, and the `LICENSE` blob
itself was fetched and copied byte-for-byte. `gh repo view --json licenseInfo`
was NOT used; it misreports repositories that do carry a licence.

## Bundled Agent Skills Validator

- Component: `scripts/skills-ref`
- Project: <https://github.com/agentskills/agentskills>
- Source path: `skills-ref`
- Source commit: `69ef37e9424c0a7ea9dd2293b559e43ec8176379`
- Upstream author: Keith Lazuka, as stated in upstream `pyproject.toml`
- License: Apache-2.0; its license text is bundled at
  `scripts/skills-ref/LICENSE` with the repository-required final newline
- Modifications: upstream tests and development environment artifacts are
  omitted from the deployed runtime copy; a Ruff configuration preserves the
  upstream source unchanged under this repository's broader lint rules

Upstream supplies no `NOTICE` file at the pinned revision.
