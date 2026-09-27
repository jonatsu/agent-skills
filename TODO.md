# Skills Future Work

Operational and future-feature backlog for the skills stack, including candidate sources not yet evaluated.
The completed 2026-09 review's verdicts and evidence are in the
[shared-skill review](../docs/evaluations/skills/2026-09-shared-skill-review.md), and
archived reviews still deferred are the rows marked "Review is deferred" in
[archived/README.md](archived/README.md). The restored embedded skills' completed review campaign is recorded
in [../docs/evaluations/skills/2026-09-16-embedded-skill-review-ledger.md](../docs/evaluations/skills/2026-09-16-embedded-skill-review-ledger.md);
their surviving open work is below, and the embedded research notes (tooling, testing, QEMU candidates) are in
[../docs/research/embedded-skills/](../docs/research/embedded-skills/).
Repository-wide items live in [../TODO.md](../TODO.md). Roughly high-priority first; the settled/low-priority
entries sit at the bottom.

## Decide Which Skills Stay Direct and Which Go Behind the Lazy Server

Urgent, added 2026-09-28. The lazy-skills-server is finished and Codex already uses it; today it serves only
the `embedded-linux`, `development/nix`, `system-administration`, and `code-health` domains (see the lazy-tier
comment in `kasetto/base.yaml`). Evaluate the whole set: which skills stay direct, with a minimized description
in every session's listing, and which move behind the lazy server, reached on demand. Weigh how often each
fires, whether a request names its subject clearly enough to route through the server, and the listing cost:
Claude's listing budget was raised to 4% on 2026-09-28 because Haiku sessions were losing most descriptions
(`../docs/findings/skill-discovery-limits.md`). `docs/plans/agent-management/lazy-skill-loading.md` is the
design record.

## Description and Prose Pass Ledger

Every skill gets two passes: `skill-descriptions-and-triggers` on its description, and `writing-for-agents`
over the whole package. A skill missing from this table has had neither, and a blank cell means that pass is
still open. When a skill passes, add or complete its row in the same change and cite the commit. Rows before
2026-09-28 were reconstructed from Git history; a pass counts only where a commit message or evaluation record
names it. The 2026-09-07 description audit predates the description skill and does not count.

| Skill                             | Description pass                 | `writing-for-agents` pass                                               |
| --------------------------------- | -------------------------------- | ----------------------------------------------------------------------- |
| `git-commits-and-recovery`        | 2026-09-27, `05ecb1e`            | 2026-09-27, `05ecb1e`                                                   |
| `git-history-investigation`       | 2026-09-27, `8242032`            | 2026-09-27, `8242032`                                                   |
| `using-git-worktrees`             | 2026-09-27, `b10689e`            | 2026-09-27, `36bb1b4`                                                   |
| `session-handoff`                 | 2026-09-28, `f25ae32`            | 2026-09-28, `f25ae32`                                                   |
| `skill-descriptions-and-triggers` | 2026-09-28, `37f34c8`            | 2026-09-28, `37f34c8`                                                   |
| `session-skill-audit`             | 2026-09-28, `da8a0cb`            | 2026-09-28, `da8a0cb`                                                   |
| `skill-review`                    | 2026-09-28, `0067bb4`            | 2026-09-28, `0067bb4`, light: tiers, discovery lens, two negations only |
| `skill-forge`                     | 2026-09-28, `37f34c8`            | 2026-09-28, `1666cb1`                                                   |
| `context-compression`             | 2026-09-28, `2997308`            | 2026-09-25, `f0f5559f`                                                  |
| `context-architecture`            | 2026-09-28, `2997308`, no change | 2026-09-25, `8fce5a79`                                                  |
| `agents-context-docs`             | 2026-09-28, `2997308`, no change | 2026-09-25, `8fce5a79`, as `agents-management`                          |
| `python-architecture`             | 2026-09-28, `2997308`            | 2026-09-24, `4e374bf`                                                   |
| `python-async-patterns`           | 2026-09-28, `2997308`, no change | 2026-09-24, `c85d2cf`                                                   |
| `python-error-handling`           | 2026-09-28, `2997308`, no change | 2026-09-24, `819aa34`                                                   |
| `python-parallelism`              | 2026-09-28, `2997308`, no change | 2026-09-24, `c1d8db7`                                                   |
| `python-project-management`       | 2026-09-28, `2997308`            | 2026-09-24, `bf1081b`                                                   |
| `python-style`                    | 2026-09-28, `2997308`            | 2026-09-24, `e47e62d`                                                   |
| `python-testing`                  | 2026-09-28, `2997308`            | 2026-09-24, `d908951`                                                   |
| `python-typing`                   | 2026-09-28, `2997308`, no change | 2026-09-24, `272c8d2`                                                   |

## Merge skill-review Into skill-forge as a Review Mode?

Proposed 2026-09-28. `skill-forge` and `skill-review` each state what a skill is judged on (scope coherence, the
hard gates, the `ready with risks` ceiling), and the two copies can drift apart silently. One skill with an
authoring mode and a review mode would hold one rubric. The cost is size, against the preference for small
skills; progressive disclosure could keep the entry file lean by moving each mode's detail behind its own
reference. Decide by first listing every rule both packages state, since the drift risk sits in that shared
rubric rather than in the two workflows.

## Skills With No Usage — Recheck After 2026-10-08

The 2026-09-08 measurement (738 transcripts plus `skillUsage` in `.claude.json`) is not usable: the set was
redeployed and largely renamed that week, and `skillUsage` keys on the name, so every counter had reset — a
zero meant "deployed last week", not "unused".

Recheck no earlier than **2026-10-08**, once a month of sessions has accumulated under current names. `/doctor`
re-runs it; the trustworthy inputs are `skillUsage.lastUsedAt` (written only on real dispatch) and `Skill`
`tool_use` entries in `~/.config/claude/projects/*/*.jsonl` (`usageCount` never windows).

Read the full-description skills as the clean test cases — a non-trigger there is the real evidence the
description-activation entries below are waiting for: `context-architecture`, `context-compression`,
`generated-file-verify`, `git-commits-and-recovery`, `github-ops`, `repo-management`. The 21 skills set
to `name-only` are reached mainly by explicit name, so a future zero on them means "never asked for by name".

## `test-engineer` Activation Datapoint

On 2026-09-06 a session wrote new pytest integration tests — squarely `test-engineer`'s declared modes — and no
test skill surfaced in the available-skills listing; they loaded only when named. The cost was real: the
committed tests carried four defects (the material one order-dependent) that `test-engineer`'s rules name
directly. Full incident and the `searchable-code` precedent are in
[../docs/findings/skill-discovery-limits.md](../docs/findings/skill-discovery-limits.md).

The `test-engineer` and `python-testing` descriptions were edited 2026-09-06 with `Use when` clauses and literal
triggers (`test-driven-development` was correctly left alone), but **activation was not measured**. The next
session that writes or fixes tests without being told to load a skill is the datapoint: record whether the test
skills appeared and whether they loaded unprompted (a deploy-then-appear does not count). If they still do not
fire, wording is not the lever — move the behavior into always-loaded instructions, as `searchable-code`
already concluded.

## Description Activation Is Unmeasured

The 2026-09 audit rewrote 13 short capability-only descriptions to carry activation clauses and triggers
(completed 2026-09-07; findings in ../docs/evaluations/skills/2026-09-07-skill-description-audit.md, edits in git
history). Whether the wording drives activation is unmeasured and nothing depends on settling it. Two of the
13 describe a situation a user never names — `systematic-debugging` and `repo-management`; if they still do
not activate on work they cover, move their behavior to `agents/rules/` per this directory's AGENTS.md ("no
wording repairs" a moment nobody verbalizes) rather than editing the description again. The
`test-engineer`/`python-testing` datapoint is tracked above.

Separately: `interview-me` is over the 512-char soft description budget; trim when convenient.

## Invocation Control Audit

Checked 2026-09-11: no skill under `shared/` or `claude/` sets `disable-model-invocation` or `user-invocable`,
and `allowed-tools` appears once (`claude-code-setup-audit`). The one skill that rightly restricted invocation,
`find-skills` (it installs third-party code), is archived, so the worked example for "when the flag is right"
must be reconstructed.

`git-commits-and-recovery` is settled the other way: the flag never stopped `git push`, it only withheld
guidance at the moment the command ran. Safety there rests on the staging rule in `agents/rules/` plus the
`PreToolUse` guard, not on the skill's confirmation gates (as `git-ops`, it fired in 0 of 362 sessions).
What remains is the audit, not that case.

Ownership is the constraint: only owned skills can be edited, since an upstream frontmatter change is
overwritten on the next sync. Derive the owned set from `skills/kasetto/*.yaml` and the locks at audit time;
earlier figures go stale within days.

1. Audit owned skills by actual behavior: which install or execute third-party code, write outside the working
   tree, mutate git history or remotes, or transmit data externally. Prior candidates: `agents-context-docs`
   (writes files and creates symlinks), `session-reflect`, `chezmoi-dotfiles`.
2. Decide the bar. `disable-model-invocation: true` costs real capability — right for "installs code from the
   internet", arguably wrong for "writes a doc file".
3. Verify that every supported client accepts the chosen metadata before touching anything in `shared/`.
4. Record the convention in `AGENTS.md` so new skills are classified at authoring time.

Open sub-question: whether tightening `allowed-tools` rides along with this or stays separate.

## Harness Switches for Commit Attribution Trailers

`shared/tools/git-commits-and-recovery` and the global instruction files forbid an unrequested `Co-Authored-By`/`Signed-off-by`
trailer, but a harness that injects the trailer does so from its system prompt, which outranks a skill or a
memory file. Where a harness exposes a config switch, setting it removes the conflict. Those switches are
agent-level configuration and MUST NOT be named in the portable skill.

Measured 2026-09-03 by scanning the installed binaries, since the published settings docs no longer cover
attribution:

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
- Check Codex for an equivalent switch; it was not scanned.

## Portable Skill-Fixture Harness

Evaluate and design a portable runner for package-local skill fixtures before the next multi-client suite. The
manual setup exposed failures that should become deterministic preflight checks:

- Resolve candidate and fixture paths from package identity, not author-machine absolute paths.
- Copy each fixture into a fresh workspace and initialize only the repository state the case declares; keep
  future conversation turns outside the active workspace until sent.
- Validate fixture prerequisites and advertised commands before starting a model, and prove the fixture and
  trace destinations are ready without invoking one (a preflight mode).
- Apply the narrowest read/write permissions the case needs, and verify resumed sessions keep them without a
  full sandbox bypass.
- Persist prompts, outputs, full traces, durations, token use, client and model identity, source revision, and
  result — avoid ephemeral sessions when the trace is evidence.
- Distinguish command-line validation, permission failures, missing dependencies, and malformed fixtures from
  candidate behavior; never count a harness failure as a model repetition or skill failure.

## Prompt Optimizer Behavioral Evaluation

`prompt-optimizer` is statically `ready with risks`; its workflow and fixtures derive from observed failures,
but it has not been exercised as a skill (deferred to protect the weekly Codex allowance). When allowance and a
decision justify it:

- Run the seven package cases in Claude Code and Codex with the skill supplied explicitly; require correct
  layer classification before judging the proposed repair.
- Compare with no skill on denied candidate reads, future-turn leakage, and over-compliance — the cases that
  establish whether it prevents prompt edits the base model would otherwise make.
- Test discovery without naming the skill: observed prompt failure, prompt-revision comparison, new-prompt
  authoring, static prompt review, repository instruction maintenance, and Agent Skill authoring.
- Inspect traces for preflight, fixture-before-prompt ordering, one-hypothesis repair, and budget stops; a
  correct final diff fails if the trace edited before preserving the failure.
- Report token and allowance use from a first run before expanding to a full matrix or repetitions.

## Context Compression Behavioral Evaluation

The independently written `context-compression` replacement has durable fixtures and static validation; its
model evaluation is deferred to protect the weekly allowance. When allowance and a decision justify it:

- Run the six package cases on one client first, comparing with no skill and, where useful, the
  [original semantic-compression skill](https://github.com/can1357/oh-my-pi/blob/a1a07fa9e13073e1f48c5422e76e2aac5b524b49/.omp/skills/semantic-compression/SKILL.md)
  at the pinned upstream commit.
- Treat any changed negation, authority, alternative, condition, quantity, chronology, attribution, uncertainty,
  or exact identifier as a fatal failure regardless of aggregate quality.
- Require visible deletion of safe scaffolding in `safe-grammar-deletion`; check `superseded-state` for
  additive-summary failure (only one decision current, the rejected alternative and its rationale still
  legible).
- Measure the target model's actual input tokens when exposed; otherwise label word/character counts as
  proxies.
- Add a second client only if the first run supports deployment confidence or exposes a model-specific
  uncertainty; report live allowance before repetitions.

## Re-Review the Other Four Embedded Skills — Non-Urgent

The 2026-09-08 work on `yocto-openembedded-development` found defects its completed 2026-09-07 review had not,
so the same classes are worth a bounded second pass over the four skills reviewed in the same batch
(`buildroot-development`, `embedded-linux-bringup`, `kas-build-orchestration`, `u-boot-development`). Not
urgent, and not evidence those four are wrong. The four each carried native checks, which lower the exposure to
classes 1 and 4 but not 2 or 3.

Check for these four classes, each of which occurred in the Yocto package:

1. **A command that no longer exists at the pinned baseline** (e.g. `sstate-cache-management.sh` → `.py` after
   Kirkstone; `bitbake -c fetchall` removed). Extract every command and verify it against the pinned upstream.
   A provenance note about a command is also a staleness signal about it.
2. **A default environment presented as universal** (`poky.conf`, `/opt/poky/`, `tmp/` depend on the distro).
   Ask of each concrete path: what sets this, and what happens when it is set differently?
3. **An area the description advertises but no reference covers.** Grep each description's claimed triggers
   against the reference bodies.
4. **A tool interface asserted from memory.** Check flags and arity against the pinned `--help` or source.

Scope: a bounded recheck against pinned upstreams and each package's description, not new behavioral
evaluation (that and hardware qualification stay deferred per the
[review-ledger record](../docs/evaluations/skills/2026-09-16-embedded-skill-review-ledger.md)). Record findings in a
dated file under `../docs/evaluations/skills/`.

## Crypto and FIPS Depth for the Yocto Security Set

`yocto-security-hardening` routes to `meta-wolfssl` as the FIPS-capable option and states its GPL-2.0/commercial
split, but **it cannot answer "how do I ship FIPS-validated crypto"** beyond that pointer. A real treatment
needs the certificate scope, the validated module versions the layer targets, and the module boundary a
compliance-evidence package must reflect — all unverified. This is the only substantive gap left in the
three-skill set (otherwise complete as of 2026-09-08).

Placement leans toward `yocto-vulnerability-management`, which now carries the CRA provisions (Annex I SBOM,
support period), so a validated module's certificate and boundary sit closer to its compliance-evidence
material than to hardening's configure-and-verify lane. Decide placement as part of the research pass.

Related and unfinished: post-quantum crypto has no upstream answer either; the two Yocto-native candidates
(`meta-oqs`, `meta-quantum-safe`) are both self-described as experimental and never compared.

## Unevaluated Candidate Sources

Recorded and never fetched, read, or license-checked. The descriptions are path-based inferences, not evidence.
Before using any material, read the repository license and any separate prose/content license from primary
sources, record provenance, and decide whether the source overlaps an existing skill.

- [wshobson/conductor](https://github.com/wshobson/agents/tree/main/plugins/conductor): inspect as a plugin,
  including agent definitions and commands Kasetto would not deploy as skills.
- [mkobit/chezmoi-skills](https://github.com/mkobit/chezmoi-skills): compare against our
  `shared/tools/chezmoi-dotfiles` skill for coverage gaps and better patterns worth writing independently.

## Dedicated GitHub Actions Skill

Create a separate GitHub Actions skill if recurring work exceeds the short orientation in
`shared/git/github-ops/references/actions-basics.md` (intended scope: matrix and cache design, self-hosted
runners, reusable workflows, composite actions, environments and deployment gates, artifact retention, the
expression language). Do not keep expanding the orientation file into a reference manual.

Write independently from primary sources: `netresearch/github-project-skill` uses CC-BY-SA-4.0 for prose
despite MIT for scripts and assets, so its prose cannot be lifted into this MIT repository.

## Codex Skill-Description Budget

Recheck the warning that Codex shortened skill descriptions to fit its context budget. Start a fresh Codex
session and record whether it remains; if it does, compare the current common set with a curated Codex overlay
before changing deployment policy. Skill count alone does not establish which descriptions consume the budget.

## Two-Tier Memory Scoping

Investigate whether the memory store should gain a global tier alongside the per-project silos. Today every
silo is per project, so a fact true everywhere lands in whichever silo was open and only that project sees it.
`session-reflect` works around this in prose (`metadata.scope:` marks the exception for a human reader and the sweep
but routes nothing).

`microsoft/skills`' `continual-learning` reached a two-tier split independently (global for tool patterns and
cross-project conventions, repo-local for project conventions). **Treat it as convergent evidence that the gap
is structural, not as a component to adopt** — its storage is a Copilot-hook-driven SQLite database, not Claude
Code's model; nothing was used (provenance in `../docs/evaluations/skills/2026-09-shared-skill-review.md`).

Open questions:

- Does a global tier belong in the silos at all, or does silo consolidation (a repository TODO entry that would
  change what `scope:` means) solve the same problem? Settle that first; it may make this moot.
- If added, what routes a capture to it — agent judgment at write time, or a filter that actually reads
  `metadata.scope:`?
- Is decay wanted? These memories are hand-curated and few, unlike the automatically-populated store whose
  60-day/hit-count pruning would otherwise be worth copying.

## Changelog Skill Deferred

Do not port `examples/skills/changelog` from `MuhammadUsmanGM/claude-code-best-practices` (reviewed and rejected
2026-09-03). Nothing under `~/src` cuts versioned releases; the one `CHANGELOG.md` is `nix-config`'s, which
deliberately uses date headings and verbatim commit subjects rather than the consumer-facing Keep a Changelog
format the skill would push. Reconsider when a project here starts cutting versioned releases and adopts Keep a
Changelog for it (most plausibly `knowledge-vault` or `services`).

Findings worth keeping so the review is not repeated:

- A changelog entry maps to many commits, not one; a per-commit procedure cannot merge one feature's commits
  into a bullet (Keep a Changelog names commit-log-derived changelogs an antipattern).
- A fix for a bug that never shipped must not be listed, which needs the previous release boundary, not the
  commit — so curation must precede grouping.
- Licenses differ: keepachangelog.com is MIT (adaptable with attribution); semver.org is CC BY 3.0 (state the
  rules in our own words with a citation). Both verified 2026-09-03.
