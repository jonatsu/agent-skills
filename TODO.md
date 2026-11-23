# Skills Future Work

The backlog for the skills in this repository, including candidate sources not yet evaluated. Roughly high
priority first; settled and low-priority entries sit at the bottom. An entry leaves this file once it is done,
handled elsewhere, or stale; Git history keeps it, and anything a later reader needs moves to its durable home
first.

Reviews are recorded in the author's private configuration repository, which also deploys the skills: the
completed 2026-09 review in its `docs/evaluations/skills/2026-09-shared-skill-review.md`, and the restored
embedded skills' campaign in `docs/evaluations/skills/2026-09-16-embedded-skill-review-ledger.md`. References
below to "agent-setup" name that repository. Archived reviews still deferred are the rows marked "Review is
deferred" in `archived/README.md` on the `archived` branch.

## Description and Prose Pass Ledger

Every skill gets two passes: `writing-skill-descriptions` on its description, and `writing-for-agents`
over the whole package. A skill missing from this table has had neither, and a blank cell means that pass is
still open. When a skill passes, add or complete its row in the same change and cite the commit. Rows before
2026-09-28 were reconstructed from Git history; a pass counts only where a commit message or evaluation record
names it. The 2026-09-07 description audit predates the description skill and does not count. A cell marked
`unnamed` cites a content update whose commit does not name the pass; the user accepted it as that pass.

A skill that produces documents also gets judged against the intent of the 2026-09-28 writing refresh: noise is
judged in context, the reader does not share the writer's knowledge, and every document the skill produces goes
through `writing-documentation` and the `writing-for-humans` reader-ready pass. An instruction to annotate
sources or status "throughout" turns into per-sentence noise; carry status in the document's structure instead,
as `writing-specs` and `technical-design` do.

| Skill                            | Description pass                 | `writing-for-agents` pass                         |
| -------------------------------- | -------------------------------- | ------------------------------------------------- |
| `git-commits-and-recovery`       | 2026-09-27, `05ecb1e`            | 2026-09-28, `bf0a58d`                             |
| `git-history-investigation`      | 2026-09-27, `8242032`            | 2026-09-27, `8242032`                             |
| `using-git-worktrees`            | 2026-09-27, `b10689e`            | 2026-09-27, `36bb1b4`                             |
| `session-handoff`                | 2026-09-28, `f25ae32`            | 2026-09-28, `bd1ba4e`                             |
| `writing-skill-descriptions`     | 2026-09-28, `37f34c8`            | 2026-09-28, `2c0a4ee`                             |
| `session-skill-audit`            | 2026-09-28, `da8a0cb`            | 2026-09-28, `da8a0cb`                             |
| `skill-forge`                    | 2026-09-28, `9fe08b0`            | 2026-09-28, `9fe08b0`, merged with `skill-review` |
| `context-compression`            | 2026-09-28, `2997308`            | 2026-09-25, `f0f5559f`                            |
| `context-architecture`           | 2026-09-30, `d586c9d`            | 2026-09-30, `28da2bd`                             |
| `agents-context-docs`            | 2026-09-30, `f8435a5`            | 2026-09-30, `f8435a5`                             |
| `python-architecture`            | 2026-09-28, `2997308`            | 2026-09-24, `4e374bf`                             |
| `python-async-patterns`          | 2026-09-28, `2997308`, no change | 2026-09-24, `c85d2cf`                             |
| `python-error-handling`          | 2026-09-28, `2997308`, no change | 2026-09-24, `819aa34`                             |
| `python-parallelism`             | 2026-09-28, `2997308`, no change | 2026-09-24, `c1d8db7`                             |
| `python-project-management`      | 2026-09-28, `2997308`            | 2026-09-24, `bf1081b`                             |
| `python-style`                   | 2026-09-28, `2997308`            | 2026-09-24, `e47e62d`                             |
| `python-testing`                 | 2026-09-28, `2997308`            | 2026-09-24, `d908951`                             |
| `python-typing`                  | 2026-09-28, `2997308`, no change | 2026-09-24, `272c8d2`                             |
| `interview-me`                   | 2026-09-28, `cb64a9b`            | 2026-09-28, `cb64a9b`                             |
| `idea-brainstorming`             | 2026-09-28, `7fd41bd`, no change | 2026-09-28, `7fd41bd`                             |
| `session-reflect`                | 2026-09-28, `8f249b6`            | 2026-09-28, `8f249b6`                             |
| `systemd-units`                  | 2026-09-28, `a0b9f38`            | 2026-09-28, `a0b9f38`                             |
| `docker-podman-containers`       | 2026-10-04, `3316fdd2`           | 2026-09-28, `f92701a`                             |
| `writing-for-humans`             | 2026-10-17, `68011bd3`           | 2026-09-28, `e999023`                             |
| `writing-documentation`          | 2026-09-28, `1742834`            | 2026-09-28, `1742834`                             |
| `writing-specs`                  | 2026-09-28, `1d620a6`, no change | 2026-09-28, `1d620a6`                             |
| `technical-design`               | 2026-09-28, `a842df8`            | 2026-09-28, `a842df8`                             |
| `implementation-planning`        | 2026-09-28, `accf233`, no change | 2026-09-28, `accf233`                             |
| `test-engineer`                  | 2026-09-28, `7702d54`, unnamed   | 2026-09-28, `7702d54` and `add69c3`, unnamed      |
| `coding-standards`               | 2026-09-28, `73a6774`, unnamed   | 2026-09-28, `73a6774`, unnamed                    |
| `repo-landing-docs`              | 2026-09-30, `28da2bd`            | 2026-09-30, `28da2bd`                             |
| `to-questionnaire`               | 2026-09-28, `e1f25db`            | 2026-09-28, `e1f25db`                             |
| `domain-modeling`                | 2026-09-28, `f5cf1f9`            | 2026-09-28, `f5cf1f9`                             |
| `conformance-review`             | 2026-09-28, `d0bc8da`, no change | 2026-09-28, `d0bc8da`                             |
| `security-review`                | 2026-09-28, `7f3d35f`            | 2026-09-28, `7f3d35f`                             |
| `writing-prompts`                | 2026-09-28, `d55d5dd`, new skill | 2026-09-28, `d55d5dd`, new skill                  |
| `prompt-debugging`               | 2026-09-28, `d55d5dd`            | 2026-10-06, `7fe44be0`                            |
| `document-conversion`            | 2026-09-28, `83bc4a0`            | 2026-09-28, `83bc4a0` and `861d3ea`               |
| `github-ops`                     | 2026-09-28, `7c7a61f`, no change | 2026-09-28, `7c7a61f`                             |
| `repo-setup`                     | 2026-09-30, `28da2bd`            | 2026-09-30, `28da2bd`                             |
| `bash-shell`                     | 2026-09-28, `ef71b3f`, no change | 2026-09-28, `ef71b3f`                             |
| `posix-shell`                    | 2026-09-28, `ef71b3f`            | 2026-09-28, `ef71b3f`                             |
| `cc-safety-net`                  | 2026-09-28, no change            | 2026-09-28, no change, vendored upstream          |
| `ast-grep`                       | 2026-09-28, `3392f10`, no change | 2026-09-28, `3392f10`                             |
| `just-task-runner`               | 2026-09-28, `8976754`, no change | 2026-09-28, `8976754`                             |
| `kasetto-skill-tool`             | 2026-09-28, `f4bcb13`            | 2026-09-28, `f4bcb13`                             |
| `chezmoi-dotfiles`               | 2026-10-04, `46487dd3`           | 2026-09-28, no change                             |
| `mise-tools`                     | 2026-09-28, `9ae6e8a`            | 2026-09-28, `9ae6e8a`                             |
| `drawio-diagrams`                | 2026-09-29, `1fe21f2`            | 2026-09-29, `1fe21f2`                             |
| `repo-audit`                     | 2026-09-30, `9b0b52f`, new skill | 2026-09-30, `9b0b52f`, new skill                  |
| `note-for-later`                 | 2026-09-30, `b691642`, new skill | 2026-09-30, `b691642`, new skill                  |
| `debug-hardware`                 | 2026-09-30, `606289f`, new skill | 2026-09-30, `7ba3a4a`, probe guard hook added     |
| `debug-server-tools`             | 2026-09-30, `606289f`, new skill | 2026-09-30, `606289f`, new skill                  |
| `gdb-debugging`                  | 2026-09-30, `0de84b5`, new skill | 2026-09-30, `0de84b5`, new skill                  |
| `mcu-firmware-debugging`         | 2026-09-30, `b2bcd2f`, new skill | 2026-09-30, `b2bcd2f`, new skill                  |
| `embedded-linux-debugging`       | 2026-09-30, `8450467`, new skill | 2026-09-30, `8450467`, new skill                  |
| `serial-console-debugging`       | 2026-09-30, `911b361`, new skill | 2026-09-30, `911b361`, new skill                  |
| `define-goal`                    | 2026-10-04, `2e67ef7e`           | 2026-10-04, `66bec2da`, new                       |
| `dispatching-subagents`          | 2026-10-06, `53799042`           | 2026-10-06, `53799042`                            |
| `incremental-implementation`     | 2026-10-06, `6b63f8c6`           | 2026-10-06, `6b63f8c6`                            |
| `systematic-debugging`           | 2026-10-06, `4df4e36f`           | 2026-10-06, `4df4e36f`                            |
| `test-driven-development`        | 2026-10-06, `650df591`           | 2026-10-06, `650df591`                            |
| `systemd-networking`             | 2026-10-06, `5ed8ca1a`           | 2026-10-06, `5ed8ca1a`                            |
| `nix-secrets`                    | 2026-10-06, `87752c31`           | 2026-10-06, `87752c31`                            |
| `direnv-nix-direnv`              | 2026-10-06, `2ef12257`           | 2026-10-06, `2ef12257`                            |
| `nix-packaging`                  | 2026-10-06, `6d6273aa`           | 2026-10-06, `6d6273aa`                            |
| `nix-flakes`                     | 2026-10-06, `6e19432d`           | 2026-10-06, `6e19432d`                            |
| `home-manager`                   | 2026-10-06, `cc25507a`           | 2026-10-06, `cc25507a`                            |
| `nixos-config`                   | 2026-10-06, `1ff8e87d`           | 2026-10-06, `1ff8e87d`                            |
| `apt-fetch-emulation`            | 2026-10-11, `2b958871`, imported | 2026-10-11, `2b958871`, imported                  |
| `brooks-audit`                   | 2026-10-18, no change            | 2026-10-18, `f925aa52`, vendored upstream         |
| `brooks-debt`                    | 2026-10-18, no change            | 2026-10-18, `e3c48194`, vendored upstream         |
| `brooks-health`                  | 2026-10-18, no change            | 2026-10-18, `042f69b7`, vendored upstream         |
| `brooks-review`                  | 2026-10-18, no change            | 2026-10-18, `b465472d`, vendored upstream         |
| `brooks-sweep`                   | 2026-10-18, no change            | 2026-10-18, `81f027d9`, vendored upstream         |
| `brooks-test`                    | 2026-10-18, no change            | 2026-10-18, `f23636e6`, vendored upstream         |
| `buildroot-development`          | 2026-10-18, `92a2dda6`           | 2026-10-18, `92a2dda6`                            |
| `embedded-linux-bringup`         | 2026-10-18, `3a577ab4`           | 2026-10-18, `3a577ab4`                            |
| `kas-build-orchestration`        | 2026-10-18, `53031e6a`           | 2026-10-18, `53031e6a`                            |
| `u-boot-development`             | 2026-10-18, `363f8dd8`           | 2026-10-18, `363f8dd8`                            |
| `yocto-openembedded-development` | 2026-10-18, `db055117`           | 2026-10-18, `db055117`                            |
| `yocto-security-audit`           | 2026-10-18, `4548d5d8`           | 2026-10-18, `4548d5d8`                            |
| `yocto-security-hardening`       | 2026-10-18, `50b2a490`           | 2026-10-18, `50b2a490`                            |
| `yocto-vulnerability-management` | 2026-10-18, `6b1e4d9a`           | 2026-10-18, `6b1e4d9a`                            |
| `hardware-security-keys`         | 2026-11-23, `ca60763`            | 2026-11-23, `ca60763`                             |

## `test-engineer` Activation Datapoint

On 2026-09-06 a session wrote new pytest integration tests — squarely `test-engineer`'s declared modes — and no
test skill surfaced in the available-skills listing; they loaded only when named. The cost was real: the
committed tests carried four defects (the material one order-dependent) that `test-engineer`'s rules name
directly. Full incident and the `searchable-code` precedent are in
agent-setup's `docs/findings/skill-discovery-limits.md`.

The `test-engineer` and `python-testing` descriptions were edited 2026-09-06 with `Use when` clauses and literal
triggers (`test-driven-development` was correctly left alone), but **activation was not measured**. The next
session that writes or fixes tests without being told to load a skill is the datapoint: record whether the test
skills appeared and whether they loaded unprompted (a deploy-then-appear does not count). If they still do not
fire, wording is not the lever — move the behavior into always-loaded instructions, as `searchable-code`
already concluded.

Usage from 2026-10-08 to 2026-11-16 (`docs/evaluations/2026-11-16-skill-usage.md`) points that way: no agent
loaded `test-engineer` on its own, and its six loads were all typed by the user, while `python-testing` loaded
21 times by agents.

## `writing-skill-descriptions` Misses Descriptions Inside a Larger Change

The user reports that `writing-skill-descriptions` usually loads on its own, but not always. A datapoint from
2026-11-16: while proposing a change to `cli-ui-ux` that included a broader description, the agent drafted the
new description in its proposal without loading the skill, and loaded it only after the user asked. The miss
happened before `skill-forge` was loaded, so `skill-forge`'s own pointer to this skill could not help. The
description names drafting and revising a description, but not a description changed as one part of a wider
skill edit or proposal. Tune the wording for that branch, then measure it with the skill's own trigger method:
realistic skill-change requests that include a description, against near misses such as editing a skill body.

## Description Activation Is Unmeasured

The 2026-09 audit rewrote 13 short capability-only descriptions to carry activation clauses and triggers (completed
2026-09-07; findings in agent-setup's `docs/evaluations/skills/2026-09-07-skill-description-audit.md`, edits in git
history). Whether the wording drives activation is unmeasured and nothing depends on settling it. Two of the 13 describe
a situation a user never names — `systematic-debugging` and `repo-management` (now `repo-setup`, its description
rewritten around "set up a repository"); if they still do not activate on work they cover, move their behavior into the
agents' always-loaded rules in agent-setup, per `AGENTS.md` ("no wording repairs" a moment nobody verbalizes), rather
than editing the description again. The `test-engineer`/`python-testing` datapoint is tracked above.

Usage from 2026-10-08 to 2026-11-16 (`docs/evaluations/2026-11-16-skill-usage.md`): agents loaded
`systematic-debugging` three times and `repo-management` (now `repo-setup`) five times on their own. Five direct-tier skills
never loaded at all: `context-compression`, `domain-modeling`, `git-history-investigation`, `github-ops`, and
`writing-specs`.

The user moved `context-compression`, `domain-modeling`, `writing-specs` (agent-setup `aab1bb2a`), and
`git-history-investigation` (agent-setup `2038566c`) to the lazy tier. `github-ops` stays direct with its
description unchanged: in headless main sessions it loads on every substantive GitHub request, and a revised
description scored no better (`docs/evaluations/2026-11-16-github-and-history-triggers.md`). Short questions such
as "did the latest run pass?" still rarely load it.

## Pre-commit Stash Wipes Parallel Subagents' Edits

Find a fix, in any repository, for commits that lose edits other agents are making in the same working tree.
On 2026-11-16 the main session committed one batch of a dash pass while three subagents were still editing.
pre-commit stashes every unstaged change before its hooks run and restores the stash afterwards. One
subagent's edits made inside that window vanished twice, and a hook reported "files were modified by this hook"
for changes it never made.

The configuration cannot turn this off. In pre-commit 4.6.2, `pre_commit/commands/run.py` sets
`stash = not args.all_files and not args.files`, so a hook run from `git commit` always stashes, and no
`.pre-commit-config.yaml` key reaches that flag. Whether prek, the Rust reimplementation, offers a no-stash mode
is unknown; it is installed through mise but has no version set. Candidate fixes, none tried yet:

- give each editing subagent its own worktree, as guidance in `dispatching-subagents` and the agents' rules;
- a git hook wrapper that runs `pre-commit run --files <staged paths>`, which skips the stash but checks the
  working-tree content rather than the staged content, so it can pass a commit whose staged version would fail;
- a no-stash mode in prek, if one exists.

Until then, the session memory rule is to make no commit while subagents edit the same tree.

## Invocation Control Audit

Checked 2026-09-11: no skill in this repository sets `disable-model-invocation` or `user-invocable`,
and `allowed-tools` appeared once, in `claude-code-setup-audit`, archived 2026-09-28. The one skill that rightly
restricted invocation, `find-skills` (it installs third-party code), is archived, so the worked example for "when
the flag is right" must be reconstructed.

`git-commits-and-recovery` is settled the other way: the flag never stopped `git push`, it only withheld
guidance at the moment the command ran. Safety there rests on the staging rule in agent-setup's always-loaded
rules plus the `PreToolUse` guard, not on the skill's confirmation gates (as `git-ops`, it fired in 0 of 362 sessions).
What remains is the audit, not that case.

Ownership is the constraint: only the skills in this repository can be edited. agent-setup also installs
third-party skills from upstream, and a frontmatter change to one of those is overwritten on the next sync.

1. Audit owned skills by actual behavior: which install or execute third-party code, write outside the working
   tree, mutate git history or remotes, or transmit data externally. Prior candidates: `agents-context-docs`
   (writes files and creates symlinks), `session-reflect`, `chezmoi-dotfiles`.
2. Decide the bar. `disable-model-invocation: true` costs real capability — right for "installs code from the
   internet", arguably wrong for "writes a doc file".
3. Verify that every supported client accepts the chosen metadata before changing any skill.
4. Record the convention in `AGENTS.md` so new skills are classified at authoring time.

Open sub-question: whether tightening `allowed-tools` rides along with this or stays separate.

## Check the agent-setup Evaluation Harness

agent-setup builds the evaluation harness, `agent-eval-tool` in `src/tools/agent-eval-tool/`, that will run this
repository's eval cases. Check its progress whenever
evaluation work starts here, and at least monthly, in the status line of
`docs/plans/evaluation/skill-evaluation-redesign.md` there. Once the harness runs, move this repository's
evaluations onto it and stop running them by hand.

## Compare `skill-forge` With Anthropic's `skill-creator` Plugin

Check `skill-forge` against Anthropic's official `skill-creator` plugin, including the assets that ship beside the
skill: its agents and its evaluation pipeline, which could improve this repository's authoring and evaluation setup.
Source: <https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator/skills/skill-creator>.
`skill-forge`'s `ATTRIBUTIONS.md` already credits the plugin's skill at `fa59bc9037741ecfa131aa27938272605710d7b2`
for ideas only; the agents and the pipeline have not been evaluated. Weigh the pipeline against agent-setup's
evaluation harness (see "Check the agent-setup Evaluation Harness" above). The plugin is `Apache-2.0`, so adapting
material brings that license's obligations. Raised 2026-10-11.

## Compare the Custom Agents With Anthropic's `pr-review-toolkit` Plugin

Check the custom agent definitions in agent-setup against Anthropic's `pr-review-toolkit` plugin:
<https://github.com/anthropics/claude-plugins-official/tree/main/plugins/pr-review-toolkit>. The work belongs to
agent-setup, which owns those definitions; it is recorded here so it is not lost, and moves there when picked up.
Raised 2026-10-11.

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

## Behavioral Evaluations Left by Completed Plans

This skill shipped with static review only, and its plan closed with the model runs still deferred:

- `skill-forge`, including its review mode, which absorbed `skill-review` on 2026-09-28. The 2026-09-04 refresh
  left it `ready with risks` with no baseline or candidate run.

## Deferred Engineering Pipeline Designs

The planning and design skills refactor deferred two companions until the pipeline's artifacts stabilized:

- **A visual-plan companion** that renders a canonical Markdown plan for human review, portable across agents.
- **Document governance**: a lifecycle and maintenance workflow for design records, with the useful parts of the
  archived `design-forge` corpus contract. Start it only with evidence that the job is needed.

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

## Compute the Brooks Health Scores in a Script

The six `brooks-*` skills ask the model to compute scores in prose. `references/common.md` gives a base score of
100 with per-finding deductions by strictness preset, and `brooks-health/health-guide.md` redistributes dimension
weights, floors and rounds them, and then needs a rule that two runs must agree. That arithmetic belongs in code.
Add a small script to each package that takes the finding counts, the preset and the skipped dimensions and prints
the score, keep the tables as its data, and have each guide say to run it and report its number. Each package
carries its own copy, because a skill may not run another skill's script. A prompt audit on 2026-11-18 raised it
as two findings with no replacement text. Move two related rules into the same script: `brooks-debt`'s Pain times
Spread priority bands, and `brooks-health`'s caps on how many findings to report, which become a documented input
limit while the prose says to report the most severe findings.

## Bare-Metal Conventions for `arm-assembly`

`arm-assembly` covers base AAPCS32 and its variants, Linux userspace system calls, and ARMv7-A privileged code, and
its `SKILL.md` states that bare-metal and RTOS conventions are outside that scope. Add a reference for reading
bare-metal AArch32 code. Cover the ARMv7-M exception model (hardware-stacked frame, `EXC_RETURN` values, vector
table layout), semihosting calls, startup code that copies `.data` and zeroes `.bss`, and the service-call conventions
of common RTOSes. Ground it in the ARMv7-M Architecture Reference Manual, Arm's semihosting specification, and each
RTOS's own port sources, then remove the exclusion from the skill's scope statement.

## Better Sources for Testing Timing and Interrupts in MCU Firmware

The C and C++ testing skill's advice on testing MCU timing, interrupt handlers, and concurrency rests on thin
evidence. Section 6.4 of `docs/evaluations/2026-11-23-c-cpp-embedded-sources/c-cpp-testing.md` holds what exists. Only
the fake clock and the directly called time callback have an expert source, Grenning's free conference paper (PDF page
17). Calling an interrupt service routine from a test, register-level fakes for interrupt state, and the limits of host
tests are inference or come from one low-authority article. Find primary or expert sources: Grenning's and Feathers'
books, vendor application notes from ST, NXP, Nordic, TI, or Microchip, RTOS test documentation, and published talks.
Then mark each piece of the skill's advice with its source, or drop the piece that no source supports.

## Patch Headers for Patches Carried in Build Layers

`linux-kernel-development` and `u-boot-development` tell an agent to give a patch carried in a build layer the
header its build system's patch policy requires, and to read the field names from that build system's manual. The
build-system skills, `yocto-openembedded-development` and `buildroot-development`, do not yet describe those policies:
Yocto's `Upstream-Status:` values and Buildroot's patch requirements. Add each from its project's manual at the
release the skill targets, with the check that enforces it, such as OE-Core's patch QA test or Buildroot's
`check-package`.

## Risk Scan for Third-Party Skills

Vet an upstream skill for risky code before adopting, adapting or re-pinning it. Raised 2026-10-10 by a
session that evaluated [Skills-Manager](https://github.com/jiweiyeah/Skills-Manager) (v2.2.0, commit
`bc3c8bd`, MIT) and rejected it as a tool: it has no lockfile, deploys symlinks and hard-codes Claude Code's
skills path. Its pre-install risk scan, in `crates/core/src/services/risk/`, is the pattern worth keeping:

- It parses the code blocks out of a skill's Markdown and its scripts.
- It matches them against rules such as `curl | sh`, remote fetches and credential reads.
- When the rules find nothing but the skill does contain code, it sends the skill to an LLM for a second
  review.
- It caches each result per skill revision.

Here it would run on an upstream skill before its material is adapted into this repository. The same scan
would also serve the pin-time gate in agent-setup, which deploys third-party skills pinned by commit.

Write an independent implementation with rules that fit our own sources. MIT would allow copying the upstream
rules, but the set is small, and borrowing the pattern avoids the dependency. Keep the LLM step out of
`just check`, because each run costs a model call.

## Repair the Context Documents Skills

`docs/evaluations/2026-11-18-context-docs-skills-review.md` rates `agents-context-docs` and
`context-architecture` `not ready`. Both skills are repaired from its findings: search findability beside
routes, must-follow rules in files the client loads by itself, a current loading reference with Codex, and
boundary and goals slots in the floor template. Whether the search-findability rules raise how often agents
reach the right document is unmeasured. Open work:

- Re-review both skills against the record's controlled comparison, which hit its ceiling: in a small
  repository every route and search condition reached the document. Aim for "ready with risks" at most. A
  harder follow-up, with a task the floor has no route for or a larger document set, is optional and needs the
  user's go-ahead for its runs.
- Compare both agents' floor-route rate before and after agent-setup's routing rule ("Instruction Routes" in the
  global rules; agent-setup `84964278` and `4ab748c5`, live from 2026-11-18 16:20 +02:00). Run it once at
  least 100 discovered first reads per agent follow that time, with the same mining method as the record.

## Prose-Limit Tests or a Third-Party Prose Checker

Open question for the user: should the repository keep its own test for prose-style limits, or move that job to a
maintained third-party checker? The user questioned such tests on 2026-11-18, after the sentence-limit test failed CI
by reading a "2,000 words" budget as a limit (fixed in `c480d92`). On 2026-10-11 they said they prefer third-party
checkers to home-grown ones.

The only such test, `tests/test_writing_sentence_limits.py`, measures no prose. It checks that the seven skills that
copy `writing-for-humans`'s sentence limits still state the same numbers, which the rule that every skill carries its
own copy of a shared rule requires. The options:

1. Keep the drift test as it is. No prose checker can do this job, because it compares stated numbers across skills
   rather than measuring sentences. Its cost is a regex that can misread a new phrasing, as on 2026-11-18.
2. Drop the drift test, and rely on updating every copy by hand when the limit changes. A limit that is changed in
   one place and missed in another then goes unnoticed.
3. Keep the drift test, and also measure the skills' own prose with a maintained checker such as Vale and a
   sentence-length rule. This adds a capability the repository does not have today. Its cost is tuning out false
   positives on code blocks, tables, and lists.

Recommendation: option 1. The test guards rule consistency, not prose style, so the preference for third-party
checkers does not apply to it. Take up option 3 separately only if measuring the skills' own sentences is wanted;
if it is, use Vale rather than writing a measurer here.

Decided on 2026-11-19: the user chose option 1. Option 3 stays open until measuring the skills' own sentences is
wanted.

## Worked Example for `test-engineer`

`test-engineer` has no worked example: its strategy reference teaches by rule alone, and its deliverable template
is an empty skeleton. Take the example from a real testing engagement, never an invented one, because an invented
example shows the format without showing the method works on a real system. When such an engagement happens, carry
one behavior through risk, level, size, oracle, taxonomy sweep, and non-goal, in about 25 lines in
`references/test-strategy.md`. Public `test-engineer` skills have no worked example to borrow either.

## Recount `writing-for-humans` Loads

The 2026-11-16 usage count (`docs/evaluations/2026-11-16-skill-usage.md`) found `writing-for-humans` loaded in
only 5 main sessions across 1,245 transcripts, although agents write prose people read in most sessions. Its
description now triggers before any such writing, and the writing, commit, and GitHub skills tell agents to load
it instead of pointing to it for depth. From 2026-12-04, two weeks after that change, recount its loads with the
same method and compare. If loads stay rare, measure the description with a trigger evaluation.

## Unevaluated Candidate Sources

Recorded and never fetched, read, or license-checked. The descriptions are path-based inferences, not evidence.
Before using any material, read the repository license and any separate prose/content license from primary
sources, record provenance, and decide whether the source overlaps an existing skill.

- [wshobson/conductor](https://github.com/wshobson/agents/tree/main/plugins/conductor): inspect as a plugin,
  including agent definitions and commands Kasetto would not deploy as skills.
- [mkobit/chezmoi-skills](https://github.com/mkobit/chezmoi-skills): compare against our
  `tools/chezmoi-dotfiles` skill for coverage gaps and better patterns worth writing independently.
- [a5c-ai/babysitter](https://github.com/a5c-ai/babysitter): research the `graph` fields in its skills'
  frontmatter and whether our skills should adopt something like them. The user flagged them on 2026-09-30,
  handing over [`jtag-swd-debug`](https://github.com/a5c-ai/babysitter/tree/main/library/specializations/embedded-systems/skills/jtag-swd-debug)
  as reference material for the embedded debugging skills; that skill is the example to start from. At commit
  `feb68abe397acc14f32b34984975c48fedba2b33` (MIT), the fields are typed edges into babysitter's "atlas"
  knowledge graph: `graph:` lists `domains`, `specializations`, `skillAreas`, and `roles` as prefixed ids such
  as `skill-area:rtos-programming`. `packages/atlas/scripts/generate-library-nodes.mjs` turns each into an edge
  such as `lib_requires_skill_area`, `graph-quality.mjs` scores the result, and the target ids live under
  `packages/atlas/graph/`. Whether anything reads the generated graph at run time is unverified; that, and
  whether such edges could drive on-demand skill discovery in the installing setup, are the open questions.
- [mohitmishra786/low-level-dev-skills](https://github.com/mohitmishra786/low-level-dev-skills): mine for
  inspiration on further low-level and embedded skills, noted on 2026-10-24. It is MIT-licensed and already a
  source for `gdb-debugging`, `debug-server-tools`, `arm-assembly`, `qemu-emulation`, and
  `reverse-engineering-methodology`, each pinned at commit `bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608`, which
  was also upstream `HEAD` on 2026-10-24. Only the paths those packages name were read
  (`skills/debuggers/`, `skills/embedded/openocd-jtag/`, `skills/low-level-programming/assembly-arm/`,
  `skills/qemu/`, `skills/security/reverse-engineering`). The rest of the repository is unread: list its
  skill directories, check each against our skills for coverage gaps, and write any adopted material
  independently or carry the MIT notice per `skill-forge`'s `references/provenance.md`.

## Session Backtrace Skill

Build `session-backtrace` in `agents/`: on request ("where are we", "bt"), rebuild the session's task
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
  tool, so the skill bundles its own stdlib script. Copilot CLI 1.0.91 (checked 2026-10-04) keeps one
  directory per session, `~/.copilot/session-state/<session-id>/`, or under `$COPILOT_HOME`. Its `events.jsonl`
  holds one event per line with `type`, `data`, `id`, `parentId` and `timestamp`, with types such as
  `user.message`, `assistant.message`, `tool.execution_start` and `skill.invoked`. Beside it, `workspace.yaml`
  records the session's `cwd`, `client_name`, timestamps and `summary_count`, which anchors a session to its
  repository without trusting the newest mtime. `~/.copilot/session-store.db` is a SQLite index with `sessions`,
  `turns` and a full-text search index. No stored session had been compacted, so the compaction event's form is
  still unseen.
- **Risks:** Claude's transcript fields (`isCompactSummary`, `isMeta`, the `compact_boundary` system subtype)
  are undocumented and can change, so test the script against a real transcript. Transcripts can hold
  secrets; the output stays local.
- **Keep it separate from `session-handoff`,** which briefs a different recipient; this answers the user now.

## `usability-engineering` Eval Gaps

The `ui-ux-skills/usability-engineering` evaluation (`docs/evaluations/2026-11-16-usability-skill.md`) has no case for
review mode, the holistic review, or a voice interface, and ran once per model on one client. Add
a case for each, built on fixtures unlike the existing five, and rerun with at least two repetitions. While
there, make `evals/grade.py` ignore a report that says it gives no score.

## `accessibility-engineering` Eval Gaps

The `ui-ux-skills/accessibility-engineering` evaluation (`docs/evaluations/2026-11-16-accessibility-skill.md`) has no case
for review mode, the quick check and its 300-word cap, a target the user sets at AAA, a document or
native app under EN 301 549 clauses 10 and 11, or a clean page where the agent finds no failure and must still
refuse to write "conforms". It ran once per model on one client. Add a case for each, such as a review of a diff
that adds a sticky header and a 20-pixel icon button, and rerun with at least two repetitions. The description
has no trigger for contrast, alt text, ARIA, or a procurement conformance report (VPAT); add one only if a
trigger evaluation shows misses.

## `tui-ui-ux` Sibling Skill

Build `tui-ui-ux` beside `ui-ux-skills/cli-ui-ux` for full-screen terminal interfaces: layout, keybindings,
focus, resizing, redraw, screen-reader behaviour, and a TUI review order. `cli-ui-ux` covers one-shot commands
and inline prompts and states full-screen interfaces as out of scope, because they need a different checklist.
Decided by the user on 2026-11-07 while designing `cli-ui-ux`. Candidate sources from that session's survey,
unread in full: `hyperb1iss/hyperskills` `tui-design` (MIT) and `wimpysworld/nix-config` `tui-design`
(BlueOak-1.0.0). Check each license at a pinned commit before adapting anything.

## CI/CD Skill

Build a general CI/CD skill covering GitHub Actions and GitLab CI; the user needs it soon (decided 2026-11-18).
Intended scope on both platforms: pipeline structure, matrix and cache design, self-hosted runners, reusable
workflows and templates, environments and deployment gates, secrets, artifact retention, and each platform's
expression or rules language. `tools/github-ops/references/actions-basics.md` stays a short orientation and points
to the new skill rather than growing into a reference manual.

Write independently from primary sources: `netresearch/github-project-skill` uses CC-BY-SA-4.0 for prose
despite MIT for scripts and assets, so its prose cannot be lifted into this MIT repository.

## Decide Which Skills Support Windows

Decide which skills should also work on Windows. Most skills here target Linux only, and the user needs Windows support
for some of them later (stated 2026-11-23); macOS is out of scope, because the user does not use it. No skill has been
assessed yet, and which ones need Windows is unknown. `system-administration/hardware-security-keys` is laid out for the
addition: each reference keeps its operating-system facts under a `## Linux` heading, so a `## Windows` section can sit
beside it, while the vendor CLIs that run on both stay in the shared sections. Its `compatibility` field says Linux and
would change with that section.

## Changelog Skill Deferred

Do not port `examples/skills/changelog` from `MuhammadUsmanGM/claude-code-best-practices` (reviewed and rejected
2026-09-03). None of the author's projects cuts versioned releases; the one `CHANGELOG.md` among them is the Nix
configuration repository's, which
deliberately uses date headings and verbatim commit subjects rather than the consumer-facing Keep a Changelog
format the skill would push. Reconsider when a project here starts cutting versioned releases and adopts Keep a
Changelog for it. The `repo-landing-docs` skill carries changelog templates for both forms and the rules for
writing an entry; only a procedure that drafts entries from the commits since a release stays deferred.

Findings worth keeping so the review is not repeated:

- A changelog entry maps to many commits, not one; a per-commit procedure cannot merge one feature's commits
  into a bullet (Keep a Changelog names commit-log-derived changelogs an antipattern).
- A fix for a bug that never shipped must not be listed, which needs the previous release boundary, not the
  commit — so curation must precede grouping.
- Licenses differ: keepachangelog.com is MIT (adaptable with attribution); semver.org is CC BY 3.0 (state the
  rules in our own words with a citation). Both verified 2026-09-03.
