# Skills Future Work

Operational and future-feature backlog for the skills stack. Skill-review status, evidence, and candidate
review inputs belong in [skills-review-notes.md](skills-review-notes.md). Repository-wide items live in
[../TODO.md](../TODO.md).

## Codex Skill-Description Budget

Recheck the warning that Codex shortened skill descriptions to fit its context budget. The 2026-09-02 archival
reduced the Kasetto-managed common set from 63 skills to 35, of which 25 are repository-owned shared skills.
Start a fresh Codex session and record whether the warning remains. If it does, compare the current common set
with a curated Codex overlay before changing deployment policy. Skill count alone does not establish which
descriptions consume the budget.

## OpenCode Reflect Ownership

Keep `reflect` under `claude/` while `oh-my-opencode-slim` installs and replaces OpenCode's separate copy.
Re-evaluate this only if that plugin is removed or its skill installation can be disabled. Do not deploy the
repository copy to OpenCode on top of a directory Kasetto does not own.

## Dedicated GitHub Actions Skill

Create a separate GitHub Actions skill if recurring work exceeds the short orientation in
`shared/git/github-operations/references/actions-basics.md`. Its intended scope is matrix and cache design,
self-hosted runners, reusable workflows, composite actions, environments and deployment gates, artifact
retention, and the expression language. Do not keep expanding the orientation file into a reference manual.

Write independently from primary sources. The previously inspected `netresearch/github-project-skill` uses
CC-BY-SA-4.0 for prose despite MIT licensing for scripts and assets, so its prose cannot be lifted or lightly
edited into this MIT repository.

## Pin Third-Party Sources

Third-party entries in `kasetto/base.yaml` currently track moving default branches. If unexpected upstream
changes become a practical problem, add explicit `ref:` pins and define a deliberate update procedure. A bare
`kst sync --update` also re-resolves those moving sources.

## Remove writing-great-skills from the Archive

Delete `archived/writing-great-skills` in a dedicated cleanup. The reviewed `skill-forge` and `skill-review`
already incorporate Matt Pocock's later `writing-for-agents` material, and the user has judged the archived
predecessor no longer worth preserving.

## Detect Renames Out of Deployed Groups

Fix `scripts/sync-skills-kasetto.sh` so a 100% rename out of `skills/shared/`, `skills/claude/`, or
`skills/opencode/` still selects the source scope. The current `git diff --name-only HEAD~1 HEAD` can report
only the destination path, leaving an orphaned deployed copy while the hook exits successfully. `--no-renames`
or `-M0` is the candidate change.

Verify the fix in a scratch commit for these cases:

- `shared/` to `archived/`, with other shared skills remaining;
- `shared/` to another deployed group;
- an archival that also removes an emptied domain from `kasetto/base.yaml`;
- all four shared destinations: Claude, OpenCode, Copilot, and Codex.

Keep the manual deployment and destination checks in `AGENTS.md` until this is implemented and measured.
