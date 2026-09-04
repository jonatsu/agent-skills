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

## Technical Design and Planning Evaluation Follow-Up

The bounded 2026-09-04 repair evaluation was accepted as sufficient to deploy `technical-design` and
`implementation-planning` with `ready with risks` verdicts. Keep the following as future evidence work rather than a
release gate:

- Complete Codex case 11's confirmed second turn with a workspace-write resume configuration that does not require a
  full approvals-and-sandbox bypass. Assert that it writes only the separate implementation plan from the accepted
  design. The first turn already proved that Codex writes only the design and waits for confirmation.
- Run cases 2, 3, 5, 6, 10, and 12 against the repaired revision when broader regression coverage is warranted. Cases 1,
  4, 7, 8, 9, and the two-turn handoff already have bounded evidence across Claude Code and Codex, subject to the Codex
  turn-2 limit above.
- Evaluate discovery without supplying skill paths: positive design-only and planning-only requests, near-miss
  brainstorming and review requests, requirements with unresolved architecture, and mixed design-and-plan requests.
- Add repetitions only when measuring variance would change a decision. The first two rounds consumed an unexpectedly
  large share of the Codex weekly subscription allowance, so future runs should report the live allowance before
  expanding coverage.
- Consider OpenCode and Copilot only when their behavior could change the portable-package decision. Deployment alone
  does not establish behavioral portability.

## Portable Skill-Fixture Harness

Evaluate and design a portable runner for package-local skill fixtures before the next multi-client suite. The manual
setup exposed harness failures that should become deterministic preflight checks:

- Resolve candidate and fixture paths from the package identity rather than author-machine absolute paths.
- Copy each fixture into a fresh workspace and initialize only the repository state the case declares.
- Keep future conversation turns outside the active workspace until they are sent. Codex correctly found a staged
  confirmation file during one invalid case 11 attempt.
- Validate fixture prerequisites and advertised commands before starting a model. Case 9 initially named an unavailable
  validator; its replacement now bundles and tests the required operation.
- Apply the narrowest read and write permissions needed by the case. Verify that resumed sessions retain those
  permissions without resorting to a full sandbox bypass.
- Persist prompts, outputs, full traces, durations, token use, client and model identity, source revision, and result.
  Avoid ephemeral sessions when the trace is evidence.
- Distinguish command-line validation, permission failures, missing dependencies, and malformed fixtures from candidate
  behavior. Do not count a harness failure as a model repetition or skill failure.
- Add a preflight mode that proves the fixture and trace destinations are ready without invoking a model.

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

**Re-measure before starting.** A separate defect in the same diff — `git -C "$SCRIPT_DIR"` pointing at
`scripts/` while `diff.relative = true` is set in `~/.gitconfig` — meant the hook selected no scope for any
change at all, so the rename behaviour recorded above was never observable. Fixed on 2026-09-04 with
`--no-relative`. Confirm the rename case still fails before writing a second fix for it.

## Two-Tier Memory Scoping

Investigate whether the memory store should gain a global tier alongside the per-project silos. Today every
silo is per project, so a fact true everywhere lands in whichever silo happened to be open and only that
project's sweeps and recalls will ever see it. `reflect` works around this in prose: a fact that escapes its
silo MUST say so in its own `description`, because nothing filters on frontmatter. `metadata.scope:` marks
the exception for a human reader and the maintenance sweep, but it routes nothing.

`microsoft/skills`' `continual-learning` reached a two-tier split independently — a global store for tool
patterns and cross-project conventions, a repo-local one for project conventions and team preferences. Read
at HEAD `25d6f9c81ebd1c51da6c5f4fc585658610dfdc4b` on 2026-09-03. **Treat it as convergent evidence that the
gap is structural, not as a component to adopt**: its storage is a SQLite database under `~/.copilot/` and
`.copilot-memory/`, driven by a Copilot hook schema that is not Claude Code's. Nothing was used, and the
provenance note in `skills-review-notes.md` records that.

Its compaction policy is the second idea worth weighing, because `reflect` prunes by judgment and this does
not: entries older than 60 days with a low hit count are pruned, frequently-referenced ones persist
indefinitely, and tool logs go after 7 days. A hit count implies recording reads, which the current memory
files do not do — decide whether that bookkeeping is worth its cost before copying the policy.

Open questions:

- Does a global tier belong in the memory silos at all, or does silo consolidation solve the same problem
  differently? The repository TODO's silo-consolidation entry would change what `scope:` means, and settling
  that first may make this moot.
- If a global tier is added, what routes a capture to it — an agent judgment at write time, or a filter that
  actually reads `metadata.scope:` rather than leaving it advisory?
- Is decay wanted here? These memories are hand-curated and few; automatic pruning suits an
  automatically-populated store better than a deliberate one.
