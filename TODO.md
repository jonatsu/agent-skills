# Skills Future Work

Operational and future-feature backlog for the skills stack, including candidate sources not yet evaluated.
The completed 2026-09 review's verdicts and evidence are the record in
[../docs/evaluations/2026-09-shared-skill-review.md](../docs/evaluations/2026-09-shared-skill-review.md), and
reviews still deferred are the rows marked "Review is deferred" in
[archived/README.md](archived/README.md). Repository-wide items live in [../TODO.md](../TODO.md).

## Nix Domain Restore Verdicts and Fix Lists

The consolidation the 2026-09-03 archival deferred to ran on 2026-09-06: a per-skill content-mapping pass over
`archived/nix/` against `~/src/nix-config`'s repo-local skills and reference docs, with every fix item below
verified by its mapping lane (wrong claims were tested, not inferred). Verdict: **six of the seven skills stay
global and are worth restoring once fixed**; `nix-dendritic-pattern` was deleted from the archive on
2026-09-06 (see its bullet below). The
harvest direction into nix-config is already applied there (its `CHANGELOG.md` 2026-09-06 entry lists the
items), so restoring these skills is now purely an agent-setup job: fix, validate, restore the domain per
`archived/README.md` (the live `shared/nix/` domain and its `kasetto/base.yaml` entry already exist since the
2026-09-06 promotions — move the fixed skills in and clear the deferred rows), and run the deferred
`skill-review` pass on each. The nixos-config/home-manager pair cross-link each other, so restore them
together or inline the linked hazard.

- **`nix-flakes` — restore after:** rewriting the "allowed `nixConfig` keys" paragraph (the 13-key "restricted
  set" is wrong; per `NixOS/nix` `src/libflake/config.cc` the auto-applied whitelist is `bash-prompt`,
  `bash-prompt-prefix`, `bash-prompt-suffix`, `flake-registry`, `commit-lock-file-summary`, everything else
  needs `--accept-flake-config` or per-value trust); correcting IRON LAW 2 (tracked-but-dirty files ARE
  visible to flake eval — only untracked/ignored files are invisible); fixing
  `defaultPackage.<system>.package` → `defaultPackage.<system>` in references/advanced-commands.md; stripping
  rot-prone token/package counts from references/mcp-nixos.md and re-verifying its `system=` param against the
  live server schema.
- **`nix-packaging` — restore after:** resolving the `nix-wrapper-modules` cross-reference to stand alone;
  fixing the invalid Nix in the .deb example (`stdenv.cc.cc.lib` in a function argset is a syntax error);
  removing the local-path `src` example that contradicts its own IRON LAW; `lib.fakeSha256` → `lib.fakeHash`
  throughout; `buildFHSUserEnv` → `buildFHSEnv`; adding `appimageTools.wrapType2`/`.extract` as the canonical
  AppImage route (the manual `--appimage-extract` unpackPhase fails on non-executable store files); rewriting
  references/binary-overlay-pattern.md's non-evaluating example; modernizing `rec` toward the
  `(finalAttrs: …)` pattern.
- **`nix-secrets` — restore after:** correcting or cutting the agenix-rekey layer, whose option surface
  drifted wrong (`hostIdentities` plural does not exist — `hostPubkey` is singular; `storageMode` has no
  default and aborts unset; generators are `generator.script`, not `generator.generator`+`length`;
  `masterKeyPath` is likely fabricated) — nix-config's source-verified `docs/reference/agenix-rekey.md` is the
  correction source, and shrinking the section to a verified when-to-graduate pointer is the cheaper valid
  shape; stripping den vocabulary ("host aspect nixos class", "per aspect"); fixing the invalid
  `nix-store -qR .#…` verify command (`nix path-info -r` on the built toplevel); repairing the malformed
  agenix-rekey decision-matrix row; replacing the `api-key: supersecretvalue` example that trips betterleaks.
  Its sops-nix half is unique — no other asset covers it; spot-check `sops.useSystemdActivation` before
  redeploy.
- **`nixos-config` — restore after:** resolving its live link to
  `../home-manager/references/settings-trees-and-merges.md` (restore the pair together or inline the hazard);
  correcting the `nixos-generate-config` overstatement its lane flagged; optionally adding
  `nixos-rebuild list-generations` and the `steam-run`-needs-unfree note. Its 2026-09-03 review verdict
  (`ready with risks`) predates these edits, so it re-reviews with the rest despite the completed row.
- **`home-manager` — restore after:** rewriting Step 2's wrong claim (`osConfig ? services` is NOT a type
  error on null — tested on Nix 2.34.8: `null ? foo` → `false`, `null.foo or d` → `d`; plain selection is the
  real hazard) and its echo in the anti-patterns; trimming the 862-char description to ≤512; adding the
  mcp-nixos HM-index-often-empty weakness note; re-measuring the rev-pinned `emptyValue` type table on
  restore.
- **`nix-wrapper-modules` — restore after:** trimming the 795-char description; rewriting the `wrappedModules`
  deprecation as completed (the alias is gone from upstream `main`, verified 2026-09-05); fixing the Mode C
  example's `config.configFile.path` → `config.constructFiles.gitconfig.path`; re-verifying against current
  upstream (pre-1.0, already moved — `inputs.pkgs` injection is undocumented in its api-reference). Contingent:
  if nix-config's held wrapper inputs are dropped and no other repo adopts the library, this one has no
  consumer — leave it archived instead.
- **`nix-dendritic-pattern` — deleted from the archive 2026-09-06**; its value is fully accounted for in
  nix-config (nine `dendritic-*` skills, six `den-*.md` references, the pin-debt TODO entry). It was the only
  document verified at den rev `e8e8de1e` (the rev nix-config's lock actually pins, while its live den docs
  still stamp `2040b613`); nix-config's pin-debt lane can recover it from git history
  (`skills/archived/nix/nix-dendritic-pattern/`) if needed.

The three promotions the same mapping pass approved (`direnv-nix-direnv`, `flake-manifest-sync` →
`shared/nix/`; `generated-file-verify` → `shared/git/`) shipped move-don't-copy on 2026-09-06 with their strip
lists applied; `colmena-deploy` stays repo-local in nix-config. One item deliberately skipped: the
`direnv-nix-direnv` `source_url` example still pins nix-direnv 3.1.2 — refresh it only after verifying the
newer tag's hash. Their review tier is review lite, so they join the restored nix skills' deferred
`skill-review` pass.

## Unevaluated Candidate Sources

Recorded 2026-08-26 and never fetched, read, or license-checked. The descriptions are path-based inferences,
not evidence. Before using any material, read the repository license and any separate prose or content license
from primary sources, record provenance, and decide whether the source overlaps an existing skill.

- [wshobson/conductor](https://github.com/wshobson/agents/tree/main/plugins/conductor): inspect as a plugin,
  including agent definitions and commands that Kasetto would not deploy as skills.
- [stellarlinkco requirements agents](https://github.com/stellarlinkco/myclaude/tree/master/agents/requirements):
  compare with archived `design-forge` and its deliberate rejection of a universal atomic `FR-` and `NFR-`
  schema.

## Python Preference Placement Resolved

The user approved retiring `python-idioms` on 2026-09-06. Persistent preferences now belong to
`agents/rules/python.md`; language-independent search recovery belongs to `agents/rules/tools.md`;
general commenting and testing policies belong to `agents/rules/workflow.md`.
This resolves the temporary duplication and the proposal for another engineering-patterns skill.
The archive preserves the original package and its provenance.
See [the consolidation review](../docs/evaluations/2026-09-06-python-idioms-rule-consolidation.md).

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

## Prompt Optimizer Behavioral Evaluation

The restored `prompt-optimizer` is statically `ready with risks`. Its workflow and fixtures derive from observed prompt,
fixture, and harness failures, but the composed skill has not been exercised as a skill because the 2026-09-04 planning
evaluation consumed most of the available weekly Codex allowance.

When allowance and decision need justify it:

- Run the seven package cases in Claude Code and Codex with the skill supplied explicitly. Require correct layer
  classification before judging the proposed repair.
- Compare the restored skill with no skill on denied candidate reads, future-turn leakage, and over-compliance. These
  cases establish whether it prevents prompt edits the base model would otherwise make.
- Test discovery without naming the skill: observed prompt failure, prompt-revision comparison, new-prompt authoring,
  static prompt review, repository instruction maintenance, and Agent Skill authoring.
- Inspect traces for preflight, fixture-before-prompt ordering, one-hypothesis repair, and budget stops. A correct final
  diff does not pass if the trace edited before preserving the failure.
- Rerun the closest boundary after any repair. Do not expand to a full client matrix or repetitions until a first run
  measures token and allowance use.

## Context Compression Behavioral Evaluation

The independently written `context-compression` replacement has durable package fixtures and static validation. Its
behavioral model evaluation is deferred to protect the current weekly subscription allowance.

When allowance and decision need justify it:

- Run the six package cases first on one client, comparing the new skill with no skill and the archived
  `semantic-compression` behavior where that baseline applies.
- Treat any changed negation, authority, alternative, condition, quantity, chronology, attribution, uncertainty, or
  exact identifier as a fatal failure regardless of aggregate quality.
- Require visible deletion of safe grammatical scaffolding in `safe-grammar-deletion`; a faithful but ordinary prose
  summary does not establish that the skill changes compression behavior.
- Inspect `superseded-state` for additive-summary failure: only one decision may remain current, while the rejected
  alternative and its useful rationale remain legible.
- Measure the target model's actual input tokens when the client exposes them. Otherwise label word or character counts
  as proxies.
- Add the second client only if the first run supports deployment confidence or exposes a model-specific uncertainty.
  Report live allowance before repetitions or a wider matrix.

## Python Skill Set Behavioral Evaluation

The six `python-` skills were built, validated and deployed on 2026-09-04, and no behavioral evidence exists for
any of them. The design is in
[../docs/plans/archived/python-skill-set-draft.md](../docs/plans/archived/python-skill-set-draft.md), which
carries the full reasoning behind each item here.

- **Discovery among the five remaining sibling descriptions is unmeasured.** They share a prefix and a subject; the two
  deliberate boundaries exist only as prose: `python-async-patterns` versus `python-testing` for async tests,
  and `python-typing` versus `python-project-management` for mypy configuration. Measure positive requests per
  skill, near-miss requests across both boundaries, and requests that legitimately need two.
- **The claim that the superseded wshobson material was largely model recall is inference from its text**, not
  measurement. Nothing depends on settling it.

Five specialist descriptions remain available across repositories. Recheck their cost against the Codex description
budget when measuring discovery. `python-idioms` is archived by consolidation decision; evaluating its activation is no
longer a prerequisite for retirement. The predecessor's evidence remains in `../docs/findings/skill-discovery-limits.md`.

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

## Re-Measure Rename Detection Out of Deployed Groups

**Establish whether this defect exists before fixing it.** The claim was that a 100% rename out of
`skills/shared/`, `skills/claude/`, or `skills/opencode/` fails to select the source scope, because Git rename
detection reports only the destination path — leaving an orphaned deployed copy while the hook exits
successfully. It was reproduced on `84cd615` on 2026-08-27.

That reproduction is not evidence. A second defect in the same diff — `git -C "$SCRIPT_DIR"` pointing at
`scripts/` while `~/.gitconfig` sets `diff.relative = true` — meant the hook selected no scope for **any**
change, so nothing about rename handling was observable. Fixed on 2026-09-04 with `--no-relative`. The rename
case may have failed for that reason alone.

Measure in a scratch commit for these cases, which remain the right ones:

- `shared/` to `archived/`, with other shared skills remaining;
- `shared/` to another deployed group;
- an archival that also removes an emptied domain from `kasetto/base.yaml`;
- all four shared destinations: Claude, OpenCode, Copilot, and Codex.

If a defect survives, `--no-renames` or `-M0` on the changed-path diff is one candidate repair, not a settled
one; choose it against what the measurement actually shows. Keep the manual deployment and destination checks
in `AGENTS.md` either way — they guard the hook's uninformative exit status, not this defect specifically.

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
provenance note in `../docs/evaluations/2026-09-shared-skill-review.md` records that.

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
