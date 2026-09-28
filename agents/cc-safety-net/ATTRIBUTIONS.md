# Attributions

## Current Skill

- Skill: `cc-safety-net`
- Current author: Joonas Onatsu
- Current license: MIT, inherited from the upstream package
- Status: vendored from upstream at a pinned tag, adapted locally

## Upstream Source

- Original author: J Liew (`kenryu42`)
- Upstream project: [kenryu42/cc-safety-net](https://github.com/kenryu42/cc-safety-net)
- Source path: `skills/cc-safety-net/`
- Source revision: tag `v2.4.11`, re-vendored 2026-09-28; first vendored at `v2.4.1`
- Source license: MIT, verbatim in `LICENSE.upstream`
- Relationship: vendored and adapted

Every file in this package originated upstream except this one. The vendored `SKILL.md` was taken from the
plugin cache that `cc-safety-net install --codex` wrote on 2026-09-14, and verified byte-identical to the
`v2.4.1` tag on GitHub before adaptation. On 2026-09-28 it was re-vendored to `v2.4.11` by a three-way merge
of upstream's `v2.4.1` to `v2.4.11` change into this copy, which applied cleanly and kept every local change
below.

Upstream generates this file from `src/hosts/templates/cc-safety-net.ts` and versions it with the CLI, so its
content is version-specific rather than evergreen. That is why the revision is pinned to a tag and why
`compatibility` names the version the guidance tracks: **re-vendor deliberately when the CLI is upgraded**,
rather than expecting the copy to age gracefully. The upstream sync comment pointing at that template was
dropped, because this package cannot satisfy it.

Local changes since the vendored revision:

- Every `npx -y cc-safety-net` invocation now calls the `cc-safety-net` already on `PATH`. `npx` downloads the
  latest published version, which reports on a build the installed hooks are not running — on the machine this
  was vendored for, the CLI was 2.4.0 while the plugin cache held 2.4.1.
- "Answer from the source" no longer locates the upstream repository by counting directories up from this
  file. That step assumed the skill ships inside the repository it describes, which a vendored copy does not,
  so the arithmetic would resolve into this repository instead. It now asks the package manager and accepts a
  candidate only on a `package.json` identity and version match.
- `disable-model-invocation: true` was removed, and the description gained a `BLOCKED by CC Safety Net`
  trigger. The flag never prevented a dangerous command; it only withheld the guidance at the moment one was
  blocked, which is precisely when this skill is useful. See the invocation-control reasoning in the
  repository's `AGENTS.md`.
- `license`, `compatibility` and `metadata.author` were added to satisfy this repository's skill policy
  validator, which upstream does not run.
- The description's leading colon was replaced with an em dash so the YAML scalar needs no surrounding quotes.
  Kasetto reads `description` linewise, so upstream's quoted form was stored in `kasetto.lock` with its double
  quotes included — and that stored string is what agents route on.

## Underlying Software

[cc-safety-net](https://github.com/kenryu42/cc-safety-net) is the documented subject of this skill rather than
a source it draws from. Behavior described here was verified against CLI 2.4.0 and plugin 2.4.1 on
2026-09-14, via `--help`, `rule doc`, `doctor`, `status` and `explain`. On 2026-09-28 CLI 2.4.11 was
checked with `--version`, `doctor` and `rule doc`; the two settings clarifications the `v2.4.11` merge
brought in (temp-root discards and the `**/` form of `secret_protection.allow_paths`) are upstream's text
and were not exercised here.
