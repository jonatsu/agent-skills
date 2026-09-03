# Archived: nix-secrets

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

One thing to expect rather than treat as a regression: the root `AGENTS.md` records that a `betterleaks git .`
history scan of this repository returns eight findings, all false positives, and one of them is an `api-key`
in this skill's example block. Archiving moves the file but not the history, so that finding persists.

## Restoring it

Restore the whole domain together, move this skill out of the deferred list, add a `nix` entry back to
`skills/kasetto/base.yaml`, and run a full `skill-review` pass before trusting it.
