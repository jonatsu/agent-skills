# AGENTS.md: skills/

Instructions for agents working under `skills/`; `CLAUDE.md` is a symlink to this file.

Read the focused source before acting:

- `README.md` describes the deployed stack and the normal add, edit, remove, and sync workflows.
- `skills-review-notes.md` is the authoritative review ledger and explains why the review exists.
- `archived/README.md` defines the archive procedure and recovery commands.
- `TODO.md` holds operational and future-feature backlog only. It is not a skill-review ledger.

## Commands

```bash
just skill-check <skill-dir>   # both validators over one skill, from the repository root
just skills-spec               # Agent Skills specification, whole tree
just skills-policy             # skill-forge's local policy, whole tree
just skills-descriptions       # block scalars and length in every description
just skills-deployed           # deployed skills that no longer match their committed source
just skills-sync               # the lock-only follow-up commit every skill commit needs
./scripts/kasetto-deploy.sh    # redeploy; run it even when the hook reported success
```

**Running only one validator is the mistake the pair exists to prevent.** The specification validator passes a
file that breaks every repository policy, and the policy validator does not check frontmatter shape at all.
Report them separately; never describe one as covering the other. `just skill-check` runs both even when the
first fails, and accepts a path relative to wherever you are.

## Boundaries

**Always:**

- Use `skill-forge` when creating, editing, restructuring, or replacing a skill.
- Use both `skill-review` and `skill-forge` for every skill review. `skill-review` governs assessment and
  evidence; `skill-forge` governs proposed repair shape and any separately authorized edits.
- Load `kasetto` before adding, editing, moving, archiving, restoring, removing, deploying, or verifying a
  skill. Its portable tool guidance complements this file's hook and lock workflow.
- Keep a skill's `description` an inline YAML scalar. Neither validator catches a folded one;
  `scripts/check-skill-descriptions.sh` does.
- Update `skills-review-notes.md` in the same work. Move every completed skill to **Reviewed**, including one
  that is replaced or removed. Move a restored archived skill out of the deferred list when its review begins.
- Delete a domain's `kasetto/base.yaml` entry in the same source commit that empties it. Git cannot preserve an
  empty directory, and Kasetto rejects a configured domain that is absent on a fresh clone.

**Never:**

- Treat a review request as authorization to change the skill. Report first unless the user also requested
  implementation.
- Spend time validating or repairing an archived skill marked deferred, unless its review is explicitly
  resumed.
- Trust the post-commit redeploy hook's exit status, a clean `git status`, or `kst`'s own report as evidence
  that a deployed copy changed or disappeared. All three answer from somewhere other than the destination.
- Edit a deployed copy directly.

## Archive Without Losing Structure

- Keep every package file intact. Leave its `SKILL.md`, references, scripts, attribution, and upstream license
  files byte-identical to the last deployed version.
- Move an individual package to `archived/<skill>/`. When archiving an entire shared domain, preserve the
  domain as `archived/<domain>/<skill>/` rather than flattening its packages.
- Add `ARCHIVED.md` inside each moved package and update `archived/README.md` and `skills-review-notes.md`.
- Prune deployed copies with `./scripts/kasetto-deploy.sh`, then inspect all four destinations.

## Verify Moves and Removals Explicitly

After any move, archive, or removal:

1. Commit source changes separately from generated locks.
2. Run `./scripts/kasetto-deploy.sh` even if the post-commit hook reported success.
3. Confirm the removed name is absent from the Claude, OpenCode, Copilot, and Codex skill directories.
4. Run `just skills-sync` for the required lock-only follow-up commit.
5. Run `just skills-deployed`; require zero drift, pending files, stray backups, and unresolved entries.

## Findings

Open the matching file when the symptom appears. Every rule above stands without it; these hold the evidence.

| Symptom                                                                                 | Read                                          |
| --------------------------------------------------------------------------------------- | --------------------------------------------- |
| A move, archive, or removal left the destination wrong, or a description broke the lock | `../docs/findings/skills-hook-and-pruning.md` |
| A skill edit deployed nothing, `kst` reports `unchanged`, or a lock looks stale         | `../docs/findings/kasetto-deploy.md`          |
