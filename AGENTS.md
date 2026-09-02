# AGENTS.md: skills/

Instructions for agents working under `skills/`. `CLAUDE.md` is a symlink to this file.

Read the focused source before acting:

- `README.md` describes the deployed stack and normal add, edit, remove, and sync workflows.
- `skills-review-notes.md` is the authoritative review ledger and explains why the review exists.
- `archived/README.md` defines the archive procedure and recovery commands.
- `TODO.md` contains operational and future-feature backlog only. It is not a skill-review ledger.

## Authoring and Review

- Use `skill-forge` when creating, editing, restructuring, or replacing a skill.
- Use both `skill-review` and `skill-forge` for every skill review. `skill-review` governs assessment and evidence;
  `skill-forge` governs proposed repair shape and any separately authorized edits.
- A review request does not authorize changing the skill. Report first unless the user also requested implementation.
- Update `skills-review-notes.md` in the same work. Move every completed skill to **Reviewed**, including a skill that is
  replaced or removed. Move a restored archived skill out of the deferred list when its review begins.
- Archived skills marked as deferred remain unreviewed. Do not spend time validating or repairing them unless their review
  is explicitly resumed.

## Archive Without Losing Structure

- Keep every package file intact. Leave its `SKILL.md`, references, scripts, attribution, and upstream license files
  byte-identical to the last deployed version.
- Move an individual package to `archived/<skill>/`. When archiving an entire shared domain, preserve the domain as
  `archived/<domain>/<skill>/` instead of flattening its packages.
- Add `ARCHIVED.md` inside each moved package and update `archived/README.md` and `skills-review-notes.md`.
- If a shared domain becomes empty, remove its entry from `kasetto/base.yaml` in the same source commit. Git cannot preserve
  an empty directory, and Kasetto rejects a configured domain that is absent on a fresh clone.
- Prune deployed copies with `./scripts/kasetto-deploy.sh`, then inspect all four destinations. A clean worktree or a green
  hook does not prove that a deployed copy disappeared.

## Verify Moves and Removals Explicitly

The post-commit hook maps changed paths with `git diff --name-only HEAD~1 HEAD`. Git rename detection normally reports only
the destination of a 100% rename. A move from `skills/shared/` to `skills/archived/` therefore hides the source path, and an
archive-only commit selects no shared deployment scope. This was reproduced on `84cd615` on 2026-08-27.

An accompanying `skills/kasetto/base.yaml` edit does select all shared scopes. That happened on `ab8baac` on 2026-09-02
when two domains were emptied. Do not rely on that incidental trigger: the generated lock rewrite was then rolled back when
pre-commit restored already-dirty lock files.

| Change | Hook behavior |
|---|---|
| Edit, add, or delete within a deployed group | Selects that group |
| Move between domains inside `shared/` | Selects all shared destinations |
| Move from `shared/` to `archived/` with no recognized config edit | Silently selects nothing |
| Move between deployment groups | Selects the destination but can miss the source |
| Edit `kasetto/base.yaml` | Selects Claude, OpenCode, Copilot, and Codex shared scopes |

After any move, archive, or removal:

1. Commit source changes separately from generated locks.
2. Run `./scripts/kasetto-deploy.sh` even if the post-commit hook reported success.
3. Confirm the removed name is absent from Claude, OpenCode, Copilot, and Codex skill directories.
4. Run `just skills-sync` for the required lock-only follow-up commit.
5. Run `just skills-deployed`; require zero drift, pending files, stray backups, and unresolved entries.

The hook defect remains tracked in `TODO.md`. The candidate repair is `--no-renames` or `-M0` on the changed-path diff;
do not apply that runtime change as unrelated cleanup.
