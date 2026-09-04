# Archived: nixos-config

**Archived 2026-09-03** with the whole `nix/` domain, pending consolidation with the repository-local skills
in `~/src/nix-config`. Last deployed from `skills/shared/nix/` to Claude Code, OpenCode, Copilot CLI and
Codex.

## Why

`~/src/nix-config` is the only consumer of any Nix skill in this setup, and it already ships its own
`.agents/skills/` set written against its actual flake. Keeping a second, general copy deployed globally on
four agents spends discovery budget in every session, including the sessions that never touch Nix, and
creates two places where the same guidance can drift apart. The domain is archived whole rather than skill by
skill so the consolidation can be decided once, with the full set in front of whoever does it.

This is a deployment decision, not a quality judgment.

## Review status

**Review complete.** Reviewed 2026-09-03 by Codex, verdict `ready with risks` after a `not ready` first pass;
the record is in `docs/evaluations/2026-09-shared-skill-review.md`. Its review is NOT deferred
and must not be recorded as such by a later archive sweep.

That review shortened the description below the discovery budget, added a system-mutation boundary before
every activation, rollback, installation and garbage-collection path, replaced a stale `stateVersion` literal
with a first-install placeholder, and replaced an absolute ban on editing generated hardware configuration
with a regeneration-safe policy. No behavioral evaluation ran, so its activation gate remains unmeasured on a
real task.

## One defect found later, not repaired

`SKILL.md` links `../home-manager/references/settings-trees-and-merges.md`, a relative path into a *different
skill's* directory. It resolved only because Kasetto deploys every skill flat into one directory, so the two
packages happened to be siblings at the destination. It still resolves inside `archived/nix/`. It would break
if this skill were restored without `home-manager`, and it would break under any deployment tool that did not
flatten. Found 2026-09-03 during the domain archival, left alone because repairing a link on a skill leaving
deployment buys nothing; fix it during the consolidation, either by inlining the hazard or by restoring both
packages together.

## Restoring it

Restore the whole domain together, add a `nix` entry back to `skills/kasetto/base.yaml`, and re-review: the
2026-09-03 verdict covers the package as it was, and the consolidation will change it.
