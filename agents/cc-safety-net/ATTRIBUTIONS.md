# Attributions

- Author: Joonas Onatsu
- License: `MIT`

The package vendors and adapts upstream material, whose MIT license requires its notice to travel with the
material; keep `LICENSE.upstream` with the skill.

## First-party Sources

### J Liew (kenryu42): `cc-safety-net` skill

- Source: <https://github.com/kenryu42/cc-safety-net>, `skills/cc-safety-net/SKILL.md`
- License: `MIT`
- Version: tag `v2.4.11` (`bbade36ac6314a1bce762aa94948a6dc1a35e8ae`)

The skill text is the upstream skill, vendored and adapted to call the installed CLI and to this repository's skill
policy.

### J Liew (kenryu42): `cc-safety-net` CLI source code

- Source: <https://github.com/kenryu42/cc-safety-net>, `src/`
- License: `MIT`
- Version: tag `v2.4.11` (`bbade36ac6314a1bce762aa94948a6dc1a35e8ae`)

The skill's behavior guidance and its "answer from the source" step rest on the CLI source. Upstream generates the
skill from `src/hosts/templates/cc-safety-net.ts` and versions it with the CLI, so the guidance tracks this release.
