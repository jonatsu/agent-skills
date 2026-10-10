# Archived skills

Skills kept for reference that no longer deploy anywhere. **Nothing in this
directory reaches any agent.**

The configuration that installs these skills names each skill group it deploys
as a Kasetto `sub-dir`, and none names `archived`. A directory here is therefore
invisible to deployment, with no exclusion list to maintain.

## What lives here

The embedded domain was restored on 2026-09-07 and now lives in `../embedded-linux/`. Its five skills use the
names `buildroot-development`, `embedded-linux-bringup`, `kas-build-orchestration`, `u-boot-development`, and
`yocto-openembedded-development`. Their review progress is tracked in
[../TODO.md](../TODO.md#re-review-the-other-four-embedded-skills--non-urgent).

A row saying "Review is deferred" is the authoritative record that the package's review is still outstanding.
The 2026-09 review campaign's own ledger is retired; its verdicts and evidence are in
agent-setup's `docs/evaluations/skills/2026-09-shared-skill-review.md`, which records no status.

| Skill | Archived | Why |
|---|---|---|
| `anti-rationalization` | 2026-09-02 | Review lite completed 2026-09-07: invalid under current policy, with additional design defects. Remains archived; review and proposed disposition (agent-setup's `docs/evaluations/skills/2026-09-07-archived-skill-review-batch-1.md`). |
| `claude-code-setup-audit` | 2026-09-28 | Retired at the user's direction because it saw no use; it had not been through the description or `writing-for-agents` passes. See its `ARCHIVED.md`. |
| `design-forge` | 2026-09-02 | Temporarily removed from deployment. Its corpus contract and checker remain archived as reference material. Review is deferred. See its `ARCHIVED.md`. |
| `find-skills` | 2026-09-02 | Retired at the user's direction. Its cross-agent source catalogue, trust model and installation workflow require continuing maintenance against external services and agent interfaces; Codex's system `skill-installer` now covers its narrower installation lane. The security and provenance material remains useful as a reference. See its `ARCHIVED.md`. |
| `generated-file-verify` | 2026-09-28 | Nix-specific guidance for one repository; merged into the agent memory of the author's Nix configuration repository. See its `ARCHIVED.md`. |
| `headroom-management` | 2026-08-26 | The Headroom proxy it manages was rejected, so the skill governs a tool this setup no longer runs. See its `ARCHIVED.md`. |
| `idea-forge` | 2026-09-02 | Replaced by portable `brainstorming` after behavioral evaluation and independent review completed 2026-09-04. Retained intact as historical evidence and an evaluation baseline. See its `ARCHIVED.md`. |
| `lean-ctx` | 2026-08-27 | lean-ctx was removed from this setup, so every `ctx_*` trigger in the skill names a tool that no longer exists. Its three locally-measured reference files are why this is an archive rather than a deletion, and its Apache-2.0 `LICENSE.upstream`/`NOTICE.upstream` must stay with the directory. See its `ARCHIVED.md`. |
| `system-prompts` | 2026-09-02 | Temporarily removed from deployment because it is not currently in use. Review is deferred. See its `ARCHIVED.md`. |
| `token-optimiser` | 2026-09-02 | Temporarily removed from deployment because it is not currently in use. Review is deferred. See its `ARCHIVED.md`. |

## Archiving a skill

1. `git mv <group>/<name> archived/<name>`, using `git mv` so history and rename
   detection survive. When archiving a complete domain, preserve it as
   `archived/<domain>/<name>` instead of flattening its skills.
2. Write `ARCHIVED.md` inside the moved skill package: the date, why it was archived,
   what it was deployed to last, and where any successor lives. **Leave
   `SKILL.md` byte-identical to what was last deployed**: the reference copy is
   only worth keeping if it is exactly what ran.
3. Add a row to the table above.
4. Update whatever named the skill or domain as live: `README.md`, and any open item in
   `TODO.md` that planned future work on it.
5. The skill leaves the agents when the installing configuration next bumps its pin
   to this repository. If the archival empties a group, that bump must also drop the
   group's `sub-dir`, so say so in the commit body. Confirm the removal there, against
   each agent's skills directory.
