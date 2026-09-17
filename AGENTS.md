# AGENTS.md: skills/

Instructions for agents working under `skills/`; `CLAUDE.md` is a symlink to this file.

Read the focused source before acting:

- `README.md` describes the deployed stack and the normal add, edit, remove, and sync workflows.
- `archived/README.md` defines the archive procedure and recovery commands, and its "Review is deferred" rows
  are the record of which reviews are still outstanding.
- `TODO.md` holds operational and future-feature backlog and unevaluated candidate sources.
- `../docs/evaluations/2026-09-shared-skill-review.md` holds the completed review's verdicts, evidence, and
  coverage limits. It is a dated record, not a ledger; do not add status to it.

## Commands

```bash
just skill-check <skill-dir>   # both validators over one skill, from the repository root
just skills-spec               # Agent Skills specification, whole tree
just skills-policy             # skill-forge's local policy, whole tree
just skills-descriptions       # block scalars and length in every description
just skills-deployed           # deployed skills that no longer match their committed source
just skills-deployed --skill <name> --verbose   # one skill, itemised per destination
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
- Record a review's verdict, evidence, and coverage limits in a dated file under `../docs/evaluations/` in the
  same work, and clear the "Review is deferred" note in `archived/README.md` when a deferred review completes.
- Keep an `ATTRIBUTIONS.md` source entry permanently, restated in the past tense once the material is replaced.
  Rewriting or independently re-deriving adapted material changes the current revision only; the revisions that
  carried it stay in git history, so deleting the entry hides a relationship a later reader still needs. This is why
  every embedded skill's record names its Bootlin and vendor sources even where nothing of them now remains.
- Delete a domain's `kasetto/base.yaml` entry in the same source commit that empties it. Git cannot preserve an
  empty directory, and Kasetto rejects a configured domain that is absent on a fresh clone.
- Ask what a user would have to say for a proposed skill to load, before writing it. Guidance that applies
  whenever someone writes code, or at any other moment nobody verbalizes, belongs in `agents/shared/rules/` instead.
  A skill for such a moment does not activate, and no wording repairs it.

**Never:**

- Treat a review request as authorization to change the skill. Report first unless the user also requested
  implementation.
- Spend time validating or repairing an archived skill marked deferred, unless its review is explicitly
  resumed.
- Trust the post-commit redeploy hook's exit status, a clean `git status`, or `kst`'s own report as evidence
  that a deployed copy changed or disappeared. All three answer from somewhere other than the destination.
- Hand-write a `diff -rq` against each agent's skills directory.
  `just skills-deployed --skill <name> --verbose` already reads the destination, covers every one of them,
  and fails loudly on a name no lock carries. A hand-rolled loop silently checks whichever destinations you
  remembered.
- Edit a deployed copy directly.

## Archive Without Losing Structure

- Keep every package file intact. Leave its `SKILL.md`, references, scripts, attribution, and upstream license
  files byte-identical to the last deployed version.
- Move an individual package to `archived/<skill>/`. When archiving an entire shared domain, preserve the
  domain as `archived/<domain>/<skill>/` rather than flattening its packages.
- Add `ARCHIVED.md` inside each moved package and update `archived/README.md`.
- Prune deployed copies with `./scripts/kasetto-deploy.sh`, then inspect all four destinations.

## Verify Moves and Removals Explicitly

After any move, archive, or removal:

1. Commit source changes separately from generated locks.
2. Run `./scripts/kasetto-deploy.sh` even if the post-commit hook reported success.
3. Confirm the removed name is absent from the Claude, OpenCode, Copilot, and Codex skill directories.
4. Run `just skills-sync` for the required lock-only follow-up commit.
5. Run `just skills-deployed`; require zero drift, pending files, stray backups, and unresolved entries.

Use `just skills-deployed --skill <name> --verbose` for step 3 rather than a hand-written diff, and read its
exit code against what you are proving:

- **A skill that should still be deployed:** expect one `ok` line per destination and exit 0. The evidence is
  explicit rather than an absence of output.
- **A name that should be gone:** expect exit 2, `no lock entry names the skill`. A removed skill leaves no
  lock entry, so that failure is the confirmation.
- **A skill added from a remote source:** expect exit 1 and an `UNVALIDATED` line. Neither skill validator can
  see a package with no copy under `skills/`, so the gate demands a decision: vendor it, or allowlist its URL
  in `scripts/check-skill-deploy-drift.sh`.

Neither answer is available from a hand-rolled loop, which checks only the destinations you remembered to
list and cannot tell a pruned skill from a mistyped name.

## Findings

Open the matching file when the symptom appears. Every rule above stands without it; these hold the evidence.

| Symptom                                                                                 | Read                                          |
| --------------------------------------------------------------------------------------- | --------------------------------------------- |
| A move, archive, or removal left the destination wrong, or a description broke the lock | `../docs/findings/skills-hook-and-pruning.md` |
| A skill edit deployed nothing, `kst` reports `unchanged`, or a lock looks stale         | `../docs/findings/kasetto-deploy.md`          |
| A validated skill never activates, or you need to measure whether one did               | `../docs/findings/skill-discovery-limits.md`  |
