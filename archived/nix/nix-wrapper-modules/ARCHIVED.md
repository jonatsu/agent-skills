# Archived: nix-wrapper-modules

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

**Unreviewed.** This skill sat in **Pending Review** in `skills/skills-review-notes.md` and moves to
**Pending Review, Deferred via Archival**. Archival defers its review; it does not complete it.

Known before archiving, from the description gate rather than from a review of this package: the description
is 795 characters against the 512 repository budget. That is a warning, not a failure, and it was left alone
because repairing a description on a skill leaving deployment buys nothing. It is the largest overshoot in
the collection, so start there when the review resumes.

## Restoring it

Restore the whole domain together, move this skill out of the deferred list, add a `nix` entry back to
`skills/kasetto/base.yaml`, and run a full `skill-review` pass before trusting it.
