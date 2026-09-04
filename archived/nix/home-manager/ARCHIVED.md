# Archived: home-manager

**Archived 2026-09-03** with the whole `nix/` domain, pending consolidation with the repository-local skills
in `~/src/nix-config`. Last deployed from `skills/shared/nix/` to Claude Code, OpenCode, Copilot CLI and
Codex.

## Why

`~/src/nix-config` is the only consumer of any Nix skill in this setup, and it already ships its own
`.agents/skills/` set written against its actual flake. Keeping a second, general copy deployed globally on
four agents spends discovery budget in every session, including the sessions that never touch Nix, and
creates two places where the same guidance can drift apart. The domain is archived whole rather than skill by
skill so the consolidation can be decided once, with the full set in front of whoever does it.

This is a deployment decision, not a quality judgment. Nothing here was found wrong.

## Review status

**Unreviewed.** Archival defers its review; it does not complete it. `skills/archived/README.md` carries
the deferred record.

Known before archiving, from the `nix-dendritic-pattern` review rather than from a review of this package:
its description was 862 characters against the 512 repository budget. That is a warning, not a failure, and
it was left alone because repairing a description on a skill leaving deployment buys nothing.

## Restoring it

Restore the whole domain together. Two other packages depend on this one's
`references/settings-trees-and-merges.md` for the shallow-merge hazard: `nix-dendritic-pattern` names it in
prose, and `nixos-config` links it as `../home-manager/references/settings-trees-and-merges.md`. That second
form is a live relative link across two skill directories, which resolved only because Kasetto deploys every
skill flat into one directory; it still resolves inside `archived/nix/`, and it would break the moment either
skill were restored without the other.

Then clear its deferred note in `skills/archived/README.md`, add a `nix` entry back to
`skills/kasetto/base.yaml`, and run a fresh `skill-review` pass before trusting it.
