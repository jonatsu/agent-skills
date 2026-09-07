# Archived skills

Skills kept for reference that no longer deploy anywhere. **Nothing in this
directory reaches any agent.**

Kasetto discovers skills through three configs that name `skills/shared`,
`skills/claude` and `skills/opencode` explicitly — nothing globs `skills/*`. A
directory beside those is therefore invisible to deployment with no exclusion
list to maintain, and it cannot drift back into a deploy by accident. That is the
whole mechanism; there is no separate opt-out to remember.

## What lives here

The embedded domain was restored to `../shared/embedded/` on 2026-09-07. Its five skills now use the names
`buildroot-development`, `embedded-linux-bringup`, `kas-build-orchestration`, `u-boot-development`, and
`yocto-openembedded-development`. Their review progress is tracked in
[../TODO.md](../TODO.md#embedded-domain--review-ledger).

A row saying "Review is deferred" is the authoritative record that the package's review is still outstanding.
The 2026-09 review campaign's own ledger is retired; its verdicts and evidence are in
`../../docs/evaluations/2026-09-shared-skill-review.md`, which records no status.

| Skill | Archived | Why |
|---|---|---|
| `anti-rationalization` | 2026-09-02 | Review lite completed 2026-09-07: invalid under current policy, with additional design defects. Remains archived; [review and proposed disposition](../../docs/evaluations/2026-09-07-archived-skill-review-batch-1.md). |
| `brooks-lint-debt-scan` | 2026-09-02 | Review lite completed 2026-09-07: invalid under current policy. Remains archived pending repair decision; [review](../../docs/evaluations/2026-09-07-archived-skill-review-batch-1.md). |
| `brooks-lint-design-review` | 2026-09-02 | Review lite completed 2026-09-07: invalid under current policy. Remains archived pending repair decision; [review](../../docs/evaluations/2026-09-07-archived-skill-review-batch-1.md). |
| `brooks-lint-maintainability-review` | 2026-09-02 | Review lite completed 2026-09-07: invalid under current policy. Remains archived pending repair decision; [review](../../docs/evaluations/2026-09-07-archived-skill-review-batch-1.md). |
| `brooks-lint-test-review` | 2026-09-02 | Review lite completed 2026-09-07: invalid under current policy. Remains archived; assess overlap with `test-engineer` before restoration. [Review](../../docs/evaluations/2026-09-07-archived-skill-review-batch-1.md). |
| `design-forge` | 2026-09-02 | Temporarily removed from deployment. Its corpus contract and checker remain archived as reference material. Review is deferred. See its `ARCHIVED.md`. |
| `find-skills` | 2026-09-02 | Retired at the user's direction. Its cross-agent source catalogue, trust model and installation workflow require continuing maintenance against external services and agent interfaces; Codex's system `skill-installer` now covers its narrower installation lane. The security and provenance material remains useful as a reference. See its `ARCHIVED.md`. |
| `headroom-management` | 2026-08-26 | The Headroom proxy it manages was rejected, so the skill governs a tool this setup no longer runs. See its `ARCHIVED.md`. |
| `idea-forge` | 2026-09-02 | Replaced by portable `brainstorming` after behavioral evaluation and independent review completed 2026-09-04. Retained intact as historical evidence and an evaluation baseline. See its `ARCHIVED.md`. |
| `lean-ctx` | 2026-08-27 | lean-ctx was removed from this setup, so every `ctx_*` trigger in the skill names a tool that no longer exists. Its three locally-measured reference files are why this is an archive rather than a deletion, and its Apache-2.0 `LICENSE.upstream`/`NOTICE.upstream` must stay with the directory. See its `ARCHIVED.md`. |
| `nix/nix-wrapper-modules` | 2026-09-03 | Archived pending consolidation with the repo-local skills in `~/src/nix-config`; the rest of the `nix/` domain was fixed and restored on 2026-09-06, this one deliberately stayed — its restore is contingent on nix-config's held wrapper inputs gaining a consumer (fix list in `../TODO.md`). Review is deferred. See its `ARCHIVED.md`. |
| `python-idioms` | 2026-09-06 | Consolidated into scoped Python rules and general tools/workflow guidance after review lite. The package is preserved intact; specialist Python skills remain active. See its `ARCHIVED.md`. |
| `security-audit` | 2026-09-02 | Removed with the intact `review/` domain while unused, then reviewed and replaced on 2026-09-04 by the independently written `shared/review/security-review`. The archived package stays as the source its method came from. See its `ARCHIVED.md`. |
| `semantic-compression` | 2026-09-02 | Reviewed and replaced by the independently written `shared/context/context-compression` skill. The archived package remains the historical behavior and provenance baseline. See its `ARCHIVED.md`. |
| `system-prompts` | 2026-09-02 | Temporarily removed from deployment because it is not currently in use. Review is deferred. See its `ARCHIVED.md`. |
| `token-optimiser` | 2026-09-02 | Temporarily removed from deployment because it is not currently in use. Review is deferred. See its `ARCHIVED.md`. |

## Archiving a skill

1. `git mv skills/<group>/<name> skills/archived/<name>` — use `git mv` so
   history and rename detection survive. When archiving a complete shared domain, preserve
   it as `skills/archived/<domain>/<name>` instead of flattening its skills.
2. Write `ARCHIVED.md` inside the moved skill package: the date, why it was archived,
   what it was deployed to last, and where any successor lives. **Leave
   `SKILL.md` byte-identical to what was last deployed** — the reference copy is
   only worth keeping if it is exactly what ran.
3. Add a row to the table above.
4. **Prune the deployed copy by hand, then confirm with `ls` against each agent's
   skills directory.** The post-commit hook will NOT do it — usually without
   saying so — and the two reasons are worth knowing rather than rediscovering;
   see below. `git status` cannot see the orphan, because it lives outside this
   repository.
5. Update whatever named the skill or domain as live: `skills/README.md`, `skills/kasetto/base.yaml`, the header
   comment in `scripts/kasetto-deploy.sh`, and any open item in
   `skills/TODO.md` that planned future work on it.

## The prune step is manual, for two separate reasons

**One of them is silent, and it fires on every archival.** The post-commit hook
maps a commit's changed paths to Kasetto scopes with `git diff --name-only HEAD~1
HEAD`, and git's rename detection collapses a 100% rename to its **destination
path only**. An archival is `skills/shared/…` → `skills/archived/…`, so nothing
matches `^skills/shared/`, no scope is selected, and the hook exits 0 having done
nothing — no warning, no output, ~0.02s. Reproduced on `84cd615`
(`writing-great-skills`), where the skill was still deployed to all three agents
afterwards; `git diff --no-renames --name-only 84cd615~1 84cd615` shows the four
source paths the default invocation hides. Tracked in `skills/TODO.md`; the
candidate fix is `--no-renames` on that diff.

Recovery is `./scripts/kasetto-deploy.sh`, which prunes correctly as long as the
group still holds a skill to name. That was enough for `writing-great-skills`:
`0 updated 0 added 1 removed 64 unchanged`, confirmed by `ls`.

**The second reason is loud, and it fires only when archiving empties a group.**
`scripts/kasetto-deploy.sh` names every local skill in a scope's group as
`--update <name>...`, because a plain `kst sync` trusts the locked hash and never
re-reads a local source. When archiving empties a group, there are no names left
to pass, and the script falls back to a plain sync that **cannot prune**:

```text
WARN: skills/<group> holds no skills, so no locked sibling can be named.
WARN: falling back to a plain sync, which cannot prune. Re-resolve by hand:
WARN:   cd skills/kasetto/<scope> && kst sync --project --update
```

Verified 2026-08-26 while archiving `headroom-management`: with the source
directory deleted from disk, `kst` did not error — it reported
`headroom-management unchanged` and did nothing, because it answered from the
lock rather than the disk. A bare `--update` re-resolved correctly and reported
`removed`.

**So an archived skill stays deployed until someone runs that command**, and two
things that look like they would catch it do not:

- `just skills-owned` skips `~/.config/opencode/skills` entirely — a
  `skip_targets` entry in `scripts/check-skill-ownership.sh` while the OpenCode
  side is reworked.
- `git status` shows nothing, because the orphan is outside this repository.

Confirm the prune with `ls` against the destination, never with `git status`.

A bare `--update` is safe for a scope whose only source is local. **Do not use it
on a scope carrying remote third-party sources** — it re-resolves moving refs
there too, which is a different change than the one you meant to make.
