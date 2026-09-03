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
`shared/git/github-ops/references/actions-basics.md`. Its intended scope is matrix and cache design,
self-hosted runners, reusable workflows, composite actions, environments and deployment gates, artifact
retention, and the expression language. Do not keep expanding the orientation file into a reference manual.

Write independently from primary sources. The previously inspected `netresearch/github-project-skill` uses
CC-BY-SA-4.0 for prose despite MIT licensing for scripts and assets, so its prose cannot be lifted or lightly
edited into this MIT repository.

## Changelog Skill Deferred

Do not port `examples/skills/changelog` from `MuhammadUsmanGM/claude-code-best-practices`. Reviewed and
rejected 2026-09-03. Nothing under `~/src` cuts versioned releases, and the single `CHANGELOG.md` is
`nix-config`'s, which uses date headings, keeps each commit subject verbatim as the entry heading, and expands
entries into maintainer-facing prose. Keep a Changelog condenses many commits into one terse consumer bullet
under a version, so the skill would push a format the one repository with a changelog has deliberately
rejected, and that repository already documents its convention in its own `CLAUDE.md`.

Reconsider when a project here starts cutting versioned releases for consumers and adopts Keep a Changelog for
it, most plausibly `knowledge-vault` or `services`.

Three findings worth keeping, so the review is not repeated:

- **A changelog entry maps to many commits, not one.** Keep a Changelog 1.1.0 names commit-log-derived
  changelogs an antipattern for exactly this reason. A procedure that enumerates commits and then filters them
  per commit cannot merge one feature's ten commits into one bullet.
- **A fix for a bug that never shipped must not be listed.** Deciding that needs the previous release boundary
  rather than the commit, so no per-commit rule can reach it. This is the clearest evidence that curation has
  to precede grouping rather than follow it.
- **The two authoritative sources carry different licenses.** keepachangelog.com is MIT, Olivier Lacan, so its
  material may be adapted with attribution. semver.org is CC BY 3.0, so state the version-bump rules as facts
  in our own words with a citation rather than adapting its prose. Both verified 2026-09-03.

Traps for whoever eventually writes it: `git describe --tags --abbrev=0` exits 128 when no tag exists rather
than returning empty, and matches lightweight non-release tags; the format requires the
`[x.y.z]: <compare-url>` link footer, without which every version heading is a dead link; deprecations,
removals and breaking changes come first, per the specification's own emphasis.

## Harness Switches for Commit Attribution Trailers

`shared/git/git-ops` forbids an unrequested `Co-Authored-By` or `Signed-off-by` trailer, and the same rule is
mirrored into the global instruction files. Prose is the weakest available lever: a harness that injects the
trailer does so from its system prompt, which outranks both a skill and a memory file. Where a harness exposes
a configuration switch, setting it removes the conflict instead of arguing with it. Those switches are
agent-level configuration and MUST NOT be named inside the skill, which stays portable across all four agents.

Measured 2026-09-03 by scanning the installed binaries, since the published settings documentation no longer
carries an attribution section. `rg` skips binaries by default, so `-a` is required; without it the Claude
Code scan reports a false negative.

| Agent                     | Key                                              | Effect                                                                                                                      |
| ------------------------- | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| Claude Code 2.1.239       | `attribution.commit` (string)                    | Attribution text for commits, including any trailers. An empty string hides attribution                                     |
| Claude Code 2.1.239       | `attribution.pr` (string)                        | The same for pull request descriptions                                                                                      |
| Claude Code 2.1.239       | `attribution.sessionUrl` (boolean, default true) | Appends the `Claude-Session` trailer and PR-body link for web and Remote Control sessions                                   |
| Claude Code 2.1.239       | `includeCoAuthoredBy` (boolean, default true)    | Deprecated by the binary's own description in favour of `attribution`. Prefer `attribution.commit: ""`                      |
| Claude Code 2.1.239       | `includeGitInstructions` (boolean, default true) | Includes the built-in commit and PR workflow instructions in the system prompt. This is the injection the skill argues with |
| GitHub Copilot CLI 1.0.80 | `includeCoAuthoredBy` (boolean)                  | Declared in `sdk/index.d.ts` alongside other terminal settings. The config file was not located under `~/.copilot`          |

Open work:

- Decide whether to set `attribution.commit: ""` in this repository's deployed Claude Code settings, and
  whether `includeGitInstructions: false` removes wanted behavior along with the trailer.
- Locate the Copilot CLI configuration file and record its path before setting anything there.
- Check OpenCode and Codex for equivalent switches. Neither was scanned.

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
