---
name: kasetto-skill-tool
description: Configure and troubleshoot Kasetto synchronization of AI agent skills, MCP servers, commands, and instructions. Use for kasetto.yaml, kasetto.lock, kst add/remove/sync, source pins, inherited configuration, destination selection, stale deployed copies, lock drift, or assets that fail to update or disappear after removal.
license: MIT
compatibility: Requires the Kasetto `kst` CLI. Tested against 3.8.0; check runtime help on other versions.
metadata:
  author: Joonas Onatsu
---

# Kasetto

Manage declarative agent assets without modifying the wrong scope or losing reproducibility. Treat
`kst <command> --help` and the official [configuration](https://kasetto.dev/docs/configuration),
[commands](https://kasetto.dev/docs/commands), and [sync contract](https://kasetto.dev/docs/how-sync-works)
as the runtime authorities.

## Workflow

1. Run `kst --version`, then locate and read the active config and lock. Confirm the global or project scope
   and every targeted agent or explicit destination. An explicit `destination` overrides agent presets.
2. Prefer `kst add` and `kst remove` for simple source changes because they preserve YAML comments. They sync
   by default; use `--dry-run` to preview or `--no-sync` to edit only. Change inherited entries in the parent
   config.
3. Use `ref:` for an immutable tag or commit and `branch:` for a moving branch. Omitted pins try `main`, then
   `master`. Use `sub-dir:` to choose a discovery root. For a deeper skill, use
   `{ name: foo, path: nested/parent }`; `path` names the parent of `foo/SKILL.md`.
4. Preview and apply with the same config, scope, and update flags, adding `--dry-run` only to the preview.
   Then run `kst list` and `kst doctor`. Inspect the report and destinations after a nonzero exit because valid
   partial changes may already exist. Commit both `kasetto.yaml` and `kasetto.lock` for project configs.

## Lock and Update Semantics

- A local project's config directory is its root and holds its lock; a remote config uses the invoking
  directory. Relative destinations and local sources resolve from that root. Relative `extends` paths resolve
  from the declaring file, but inherited local sources still resolve from the root config's directory.
- Extended asset lists merge by source, pin, and `sub-dir` identity. A child entry with the same identity
  replaces its parent entry.
- A plain sync honors the lock, including local sources and `"*"` membership. Use
  `kst sync --update <name>` after changing one source; naming any asset re-resolves its entire source. To find
  a new wildcard member, name an already locked sibling or use bare `--update`. To prune a removed member,
  name it while it remains locked, name a sibling, or use bare `--update`. Bare update also advances every
  moving remote source.
- `kst lock --check` fully checks skill lock drift and checks revision drift for tracked non-skill assets. It
  does not write the lock or destinations, but it may fetch, re-resolve, and populate the source cache.
  `kst sync --locked` never fetches; every destination must match the lock, or one verified installed copy must
  remain to repair the others.
- Each selected skill directory is the deployment payload: Kasetto hashes and copies every file. Keep
  repository-only tooling outside it, keep skill names unique within each destination, and edit source
  packages instead of deployed copies. Sync and clean prune only assets tracked by the selected lock, so
  separate configs can share a destination. Preview `kst clean`; it clears every asset in that lock.

## Kasetto 3.8.0 Checks

Apply these locally reproduced checks on 3.8.0 and recheck them on later versions:

- Keep skill frontmatter `description` on one physical line. Kasetto reads it linewise, so folded or literal
  YAML scalars such as `>-` and `|` are stored as the marker instead of the description.
- When removing the final skill from a configured `sub-dir`, remove that source entry in the same change. If
  the directory disappears first, sync fails and keeps the old lock entry and deployed copy.
- Do not deploy an empty directory inside a skill. Kasetto copies empty directories but does not hash them, so
  deleting one later can report unchanged and leave the destination directory. Remove it before deployment.
  If one is already stale, preview `kst clean` for the exact scope, clean, then sync.
