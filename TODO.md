# Skills Future Work

Operational and future-feature backlog for the skills stack, including candidate sources not yet evaluated.
The completed 2026-09 review's verdicts and evidence are in the
[shared-skill review](../docs/evaluations/skills/2026-09-shared-skill-review.md), and
archived reviews still deferred are the rows marked "Review is deferred" in
[archived/README.md](archived/README.md). The restored embedded skills' completed review campaign is recorded
in [../docs/evaluations/skills/2026-09-16-embedded-skill-review-ledger.md](../docs/evaluations/skills/2026-09-16-embedded-skill-review-ledger.md);
their surviving open work is below, and the embedded research notes (tooling, testing, QEMU candidates) are in
[../docs/research/embedded-skills/](../docs/research/embedded-skills/).
Repository-wide items live in [../TODO.md](../TODO.md) and [../BACKLOG.md](../BACKLOG.md). Roughly
high-priority first; the settled/low-priority entries sit at the bottom.

## Probe the Lazy Tier on Codex and Copilot

Added 2026-09-28, when the specialized skills moved under `shared/lazy/`
([the plan](../docs/plans/archived/lazy-tier-layout.md) records the split and the layout).

Codex was probed on 2026-09-28 with codex-cli 0.157.0 (`codex exec`, low reasoning effort, a scratch
workspace, two fresh sessions). Asked to review a Python file's style, it called `find_skills` with "python
style", then `load_skill` for `python-style`, and answered by that skill. Asked for a commit message, the
control, it called neither. Its listing held the 31 direct skills and Codex's own system skills, and no lazy
skill. Every description was cut to 100–170 characters, with a median of 166, so most lose their "Use when"
clause: `coding-standards` stops at "Use bef". `codex exec` printed no warning, so the cut is silent there.

Copilot was probed on 2026-10-04 with GitHub Copilot CLI 1.0.91 (`copilot -p`, its default model, a scratch
workspace). Asked to review a Python file's style, it called `find_skills` with "python style", then `load_skill`
for `python-style`. Asked for a commit message, the control, it called neither. Whether Copilot also truncates
skill descriptions was not checked.

Still open:

- Settle the Codex description cap. The user raised `skills.max_context_tokens` to 3000 the same day to see how
  it goes. A re-probe then showed Codex cutting every description at the same length, 286–290 characters: 3 of
  the 30 local direct skills arrive whole, and `repo-management` (295) and `git-history-investigation` (294)
  lose only their last words. The Codex configuration reference documents only `path` and `enabled` under
  `skills.config`, with no per-skill override or name-only mode (checked 2026-09-12). The ways out are a
  higher cap, or descriptions that put their routing words in the first 280 characters.

The user also plans to revisit the domain names and to rename some skills; neither is scheduled.

## Description and Prose Pass Ledger

Every skill gets two passes: `skill-descriptions-and-triggers` on its description, and `writing-for-agents`
over the whole package. A skill missing from this table has had neither, and a blank cell means that pass is
still open. When a skill passes, add or complete its row in the same change and cite the commit. Rows before
2026-09-28 were reconstructed from Git history; a pass counts only where a commit message or evaluation record
names it. The 2026-09-07 description audit predates the description skill and does not count. A cell marked
`unnamed` cites a content update whose commit does not name the pass; the user accepted it as that pass.

A skill that produces documents also gets judged against the intent of the 2026-09-28 writing refresh: noise is
judged in context, the reader does not share the writer's knowledge, and every document the skill produces goes
through `writing-documentation` and the `writing-for-humans` reader-ready pass. An instruction to annotate
sources or status "throughout" turns into per-sentence noise; carry status in the document's structure instead,
as `requirements-specification` and `technical-design` do.

| Skill                             | Description pass                 | `writing-for-agents` pass                         |
| --------------------------------- | -------------------------------- | ------------------------------------------------- |
| `git-commits-and-recovery`        | 2026-09-27, `05ecb1e`            | 2026-09-28, `bf0a58d`                             |
| `git-history-investigation`       | 2026-09-27, `8242032`            | 2026-09-27, `8242032`                             |
| `using-git-worktrees`             | 2026-09-27, `b10689e`            | 2026-09-27, `36bb1b4`                             |
| `session-handoff`                 | 2026-09-28, `f25ae32`            | 2026-09-28, `bd1ba4e`                             |
| `skill-descriptions-and-triggers` | 2026-09-28, `37f34c8`            | 2026-09-28, `2c0a4ee`                             |
| `session-skill-audit`             | 2026-09-28, `da8a0cb`            | 2026-09-28, `da8a0cb`                             |
| `skill-forge`                     | 2026-09-28, `9fe08b0`            | 2026-09-28, `9fe08b0`, merged with `skill-review` |
| `context-compression`             | 2026-09-28, `2997308`            | 2026-09-25, `f0f5559f`                            |
| `context-architecture`            | 2026-09-30, `d586c9d`            | 2026-09-30, `28da2bd`                             |
| `agents-context-docs`             | 2026-09-30, `f8435a5`            | 2026-09-30, `f8435a5`                             |
| `python-architecture`             | 2026-09-28, `2997308`            | 2026-09-24, `4e374bf`                             |
| `python-async-patterns`           | 2026-09-28, `2997308`, no change | 2026-09-24, `c85d2cf`                             |
| `python-error-handling`           | 2026-09-28, `2997308`, no change | 2026-09-24, `819aa34`                             |
| `python-parallelism`              | 2026-09-28, `2997308`, no change | 2026-09-24, `c1d8db7`                             |
| `python-project-management`       | 2026-09-28, `2997308`            | 2026-09-24, `bf1081b`                             |
| `python-style`                    | 2026-09-28, `2997308`            | 2026-09-24, `e47e62d`                             |
| `python-testing`                  | 2026-09-28, `2997308`            | 2026-09-24, `d908951`                             |
| `python-typing`                   | 2026-09-28, `2997308`, no change | 2026-09-24, `272c8d2`                             |
| `interview-me`                    | 2026-09-28, `cb64a9b`            | 2026-09-28, `cb64a9b`                             |
| `idea-brainstorming`              | 2026-09-28, `7fd41bd`, no change | 2026-09-28, `7fd41bd`                             |
| `session-reflect`                 | 2026-09-28, `8f249b6`            | 2026-09-28, `8f249b6`                             |
| `systemd-units`                   | 2026-09-28, `a0b9f38`            | 2026-09-28, `a0b9f38`                             |
| `docker-podman-containers`        | 2026-09-28, `f92701a`            | 2026-09-28, `f92701a`                             |
| `writing-for-humans`              | 2026-09-28, `e999023`            | 2026-09-28, `e999023`                             |
| `writing-documentation`           | 2026-09-28, `1742834`            | 2026-09-28, `1742834`                             |
| `requirements-specification`      | 2026-09-28, `1d620a6`, no change | 2026-09-28, `1d620a6`                             |
| `technical-design`                | 2026-09-28, `a842df8`            | 2026-09-28, `a842df8`                             |
| `implementation-planning`         | 2026-09-28, `accf233`, no change | 2026-09-28, `accf233`                             |
| `test-engineer`                   | 2026-09-28, `7702d54`, unnamed   | 2026-09-28, `7702d54` and `add69c3`, unnamed      |
| `coding-standards`                | 2026-09-28, `73a6774`, unnamed   | 2026-09-28, `73a6774`, unnamed                    |
| `writing-readmes`                 | 2026-09-30, `28da2bd`            | 2026-09-30, `28da2bd`                             |
| `to-questionnaire`                | 2026-09-28, `e1f25db`            | 2026-09-28, `e1f25db`                             |
| `domain-modeling`                 | 2026-09-28, `f5cf1f9`            | 2026-09-28, `f5cf1f9`                             |
| `spec-conformance-review`         | 2026-09-28, `d0bc8da`, no change | 2026-09-28, `d0bc8da`                             |
| `security-review`                 | 2026-09-28, `7f3d35f`            | 2026-09-28, `7f3d35f`                             |
| `writing-prompts`                 | 2026-09-28, `d55d5dd`, new skill | 2026-09-28, `d55d5dd`, new skill                  |
| `prompt-debugging`                | 2026-09-28, `d55d5dd`            |                                                   |
| `document-conversion`             | 2026-09-28, `83bc4a0`            | 2026-09-28, `83bc4a0` and `861d3ea`               |
| `github-ops`                      | 2026-09-28, `7c7a61f`, no change | 2026-09-28, `7c7a61f`                             |
| `repo-management`                 | 2026-09-30, `28da2bd`            | 2026-09-30, `28da2bd`                             |
| `bash-shell`                      | 2026-09-28, `ef71b3f`, no change | 2026-09-28, `ef71b3f`                             |
| `posix-shell`                     | 2026-09-28, `ef71b3f`            | 2026-09-28, `ef71b3f`                             |
| `cc-safety-net`                   | 2026-09-28, no change            | 2026-09-28, no change, vendored upstream          |
| `ast-grep`                        | 2026-09-28, `3392f10`, no change | 2026-09-28, `3392f10`                             |
| `just-task-runner`                | 2026-09-28, `8976754`, no change | 2026-09-28, `8976754`                             |
| `kasetto-skill-tool`              | 2026-09-28, `f4bcb13`            | 2026-09-28, `f4bcb13`                             |
| `chezmoi-dotfiles`                | 2026-09-28, no change            | 2026-09-28, no change                             |
| `mise-tools`                      | 2026-09-28, `9ae6e8a`            | 2026-09-28, `9ae6e8a`                             |
| `drawio-diagrams`                 | 2026-09-29, `1fe21f2`            | 2026-09-29, `1fe21f2`                             |
| `lint-config-audit`               | 2026-09-30, `9b0b52f`, new skill | 2026-09-30, `9b0b52f`, new skill                  |
| `note-for-later`                  | 2026-09-30, `b691642`, new skill | 2026-09-30, `b691642`, new skill                  |
| `debug-hardware`                  | 2026-09-30, `606289f`, new skill | 2026-09-30, `7ba3a4a`, probe guard hook added     |
| `debug-server-tools`              | 2026-09-30, `606289f`, new skill | 2026-09-30, `606289f`, new skill                  |
| `gdb-debugging`                   | 2026-09-30, `0de84b5`, new skill | 2026-09-30, `0de84b5`, new skill                  |
| `mcu-firmware-debugging`          | 2026-09-30, `b2bcd2f`, new skill | 2026-09-30, `b2bcd2f`, new skill                  |
| `embedded-linux-debugging`        | 2026-09-30, `8450467`, new skill | 2026-09-30, `8450467`, new skill                  |
| `serial-console-debugging`        | 2026-09-30, `911b361`, new skill | 2026-09-30, `911b361`, new skill                  |

## Skills With No Usage — Recheck After 2026-10-08

The 2026-09-08 measurement (738 transcripts plus `skillUsage` in `.claude.json`) is not usable: the set was
redeployed and largely renamed that week, and `skillUsage` keys on the name, so every counter had reset — a
zero meant "deployed last week", not "unused".

Recheck no earlier than **2026-10-08**, once a month of sessions has accumulated under current names. `/doctor`
re-runs it; the trustworthy inputs are `skillUsage.lastUsedAt` (written only on real dispatch) and `Skill`
`tool_use` entries in `~/.config/claude/projects/*/*.jsonl` (`usageCount` never windows).

Read the full-description skills as the clean test cases — a non-trigger there is the real evidence the
description-activation entries below are waiting for: `context-architecture`, `context-compression`,
`git-commits-and-recovery`, `github-ops`, `repo-management`. The 21 skills set
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

## Invocation Control Audit

Checked 2026-09-11: no skill under `shared/` or `claude/` sets `disable-model-invocation` or `user-invocable`,
and `allowed-tools` appeared once, in `claude-code-setup-audit`, archived 2026-09-28. The one skill that rightly
restricted invocation, `find-skills` (it installs third-party code), is archived, so the worked example for "when
the flag is right" must be reconstructed.

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

## Prompt Debugging Behavioral Evaluation

`prompt-debugging` (renamed from `prompt-optimizer` on 2026-09-28) is statically `ready with risks`; its workflow
and fixtures derive from observed failures, but it has not been exercised as a skill (deferred to protect the
weekly Codex allowance). When allowance and a
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
  `shared/lazy/tools/chezmoi-dotfiles` skill for coverage gaps and better patterns worth writing independently.
- [a5c-ai/babysitter](https://github.com/a5c-ai/babysitter): research the `graph` fields in its skills'
  frontmatter and whether our skills should adopt something like them. The user flagged them on 2026-09-30,
  handing over [`jtag-swd-debug`](https://github.com/a5c-ai/babysitter/tree/main/library/specializations/embedded-systems/skills/jtag-swd-debug)
  as reference material for the embedded debugging skills; that skill is the example to start from. At commit
  `feb68abe397acc14f32b34984975c48fedba2b33` (MIT), the fields are typed edges into babysitter's "atlas"
  knowledge graph: `graph:` lists `domains`, `specializations`, `skillAreas`, and `roles` as prefixed ids such
  as `skill-area:rtos-programming`. `packages/atlas/scripts/generate-library-nodes.mjs` turns each into an edge
  such as `lib_requires_skill_area`, `graph-quality.mjs` scores the result, and the target ids live under
  `packages/atlas/graph/`. Whether anything reads the generated graph at run time is unverified; that, and
  whether such edges could drive our lazy-skill discovery (`find_skills`), are the open questions.
- [openai/skills `define-goal`](https://github.com/openai/skills/tree/main/skills/.curated/define-goal): the user
  flagged it on 2026-10-04 for evaluation. Read at commit `b0401f07213a66414d84a65cb50c1d226f99485a` (the last
  change to that path, 2026-05-21): the package holds `SKILL.md`, `LICENSE.txt` (Apache-2.0) and an `agents/`
  directory that was not read. The skill turns a fuzzy intention into a measurable goal: a concrete outcome,
  verification evidence, scope bounds, and a stop condition, with heuristics per work type and a rule to reject
  pure activity goals such as "keep investigating". It then calls the Codex goal tools `get_goal` and
  `create_goal`, which Claude Code does not have, so adoption means keeping the quality bar and dropping the
  tool steps. Check overlap with `idea-brainstorming`, `requirements-specification` and the "state the outcome
  and what done means" rule in the global instructions before writing anything. Adapting it keeps the Apache-2.0
  licence and needs an `ATTRIBUTIONS.md`.

## Session Backtrace Skill

Build `session-backtrace` in `shared/agents/`: on request ("where are we", "bt"), rebuild the session's task
stack from its full transcript rather than from the compaction summary, and draw it as a stack with done,
current, and remaining steps. Feasibility was assessed on 2026-09-30 and deferred by the user. It is a check on
the task-list, checkpoint, and working-notes rules, and the recovery when a session did not keep them.

Source: ducktape's `skills/backtrace/SKILL.md` at `4ad338af25ea537dc7f817390b2e25c2a7a903f0`
(<https://github.com/agentydragon/ducktape>), AGPL-3.0, so take ideas only and write the text independently. A
copy of it is in `.scratch/research/ducktape/backtrace/`, which is scratch and may be gone. Its history
recovery leans on a `session_logs` skill that was never fetched.

What the assessment established:

- **Size is feasible when tool output is skipped.** This session's transcript was 26 MB across five
  compactions, and every real user message together came to about 53 KB (about 13,000 tokens). A bundled script
  prints the spine (user messages, compaction summaries, assistant prose) and the agent reads that in full.
- **Finding the current transcript is the hard part.** After a compaction, the session ID the agent sees is
  not the transcript's file name: the working ID `e0d6a72d` belonged to `c7c88a93-….jsonl`. Newest-by-mtime is
  wrong when sibling sessions share a repository. For Claude, the PreCompact breadcrumb in
  `~/.config/claude/hooks/capture-pending.jsonl` records each session's ID and `transcript_path`; use it as the
  anchor. When the transcript stays ambiguous, report a partial backtrace labelled as such.
- **Harness coverage:** Claude and Codex first. Codex keeps transcripts under `~/.codex/sessions/`.
  `src/tools/session-scoring/` already parses both formats, but a global skill cannot import a repository
  tool, so the skill bundles its own stdlib script. Copilot's transcript location and format are unverified;
  the Copilot test session in the root `TODO.md` locates them.
- **Risks:** Claude's transcript fields (`isCompactSummary`, `isMeta`, the `compact_boundary` system subtype)
  are undocumented and can change, so test the script against a real transcript. Transcripts can hold
  secrets; the output stays local.
- **Keep it separate from `session-handoff`,** which briefs a different recipient; this answers the user now.

## Dedicated GitHub Actions Skill

Create a separate GitHub Actions skill if recurring work exceeds the short orientation in
`shared/git/github-ops/references/actions-basics.md` (intended scope: matrix and cache design, self-hosted
runners, reusable workflows, composite actions, environments and deployment gates, artifact retention, the
expression language). Do not keep expanding the orientation file into a reference manual.

Write independently from primary sources: `netresearch/github-project-skill` uses CC-BY-SA-4.0 for prose
despite MIT for scripts and assets, so its prose cannot be lifted into this MIT repository.

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
