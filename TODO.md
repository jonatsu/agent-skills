# Skills Future Work

Operational and future-feature backlog for the skills stack, including candidate sources not yet evaluated.
The completed 2026-09 review's verdicts and evidence are the record in
[../docs/evaluations/2026-09-shared-skill-review.md](../docs/evaluations/2026-09-shared-skill-review.md), and
archived reviews still deferred are the rows marked "Review is deferred" in
[archived/README.md](archived/README.md). The restored embedded skills' completed review campaign is recorded
in [../docs/evaluations/2026-09-16-embedded-skill-review-ledger.md](../docs/evaluations/2026-09-16-embedded-skill-review-ledger.md);
their surviving open work is below, and the embedded research notes (tooling, testing, QEMU candidates) are in
[../docs/research/embedded-skills/](../docs/research/embedded-skills/).
Repository-wide items live in [../TODO.md](../TODO.md).

## Re-Review the Other Four Embedded Skills — Non-Urgent

**Trigger:** the 2026-09-08 work on `yocto-openembedded-development` found several defects that its completed
2026-09-07 review had not, so the same classes are worth a bounded second pass over the four skills reviewed in the
same batch. None of this is urgent and none of it is evidence that those four are wrong — it is a targeted recheck,
not a re-run of the reviews.

**Weigh one difference before assuming equal risk.** Yocto's was the only review in the batch with *no* execution
evidence at all; the other four each carried native checks (Buildroot: package, hook, Kconfig, image; U-Boot:
environment, FIT, load-guard, helper, driver model; kas: 16 native/wrapper contract cases; bring-up: DT
comparison/overlay and verity image). Execution catches class 1 below and some of class 4, so the exposure is
genuinely lower there. It does not catch classes 2 or 3.

Check for these four classes, each of which actually occurred in the Yocto package:

1. **A command that no longer exists at the pinned baseline.** `sstate-cache-management.sh` was rewritten as `.py`
   after Kirkstone; `bitbake -c fetchall` was removed. Extract every command invocation and verify it against the
   pinned upstream rather than reading it for plausibility. Both of these read fine.
2. **A default environment presented as universal.** `poky.conf`, `/opt/poky/`, and `tmp/` were all stated as facts
   when each depends on the selected distro. The analogues: Buildroot assuming `output/` or one `BR2_EXTERNAL`
   layout, U-Boot assuming a board's image names or a `u-boot.bin`, kas assuming a config shape, bring-up assuming a
   toolchain or distro layout. Ask of each concrete path or filename: what sets this, and what happens when it is set
   differently?
3. **An area the description advertises but no reference covers.** Yocto's description promised task-failure
   diagnosis while `do_package`/`do_package_qa` appeared nowhere in four references. Grep each description's claimed
   triggers against the reference bodies.
4. **A tool interface asserted from memory.** Check flags and arity against the pinned `--help` or source. This one
   bites authors and reviewers equally.

Two of these were visible in existing artifacts and still missed: the `sstate-cache-management.sh` line was already
recorded in `ATTRIBUTIONS.md` as reproduced near-verbatim from a 2020 deck, and nobody asked whether it still ran.
**A provenance note about a command is also a staleness signal about it.**

Scope: a bounded recheck against pinned upstreams and each package's own description, not new behavioral evaluation.
Full model evaluation and hardware qualification stay separately deferred, as recorded in the
[review-ledger record](../docs/evaluations/2026-09-16-embedded-skill-review-ledger.md). Record findings the
normal way, in a dated file under `../docs/evaluations/`.

## Crypto and FIPS Depth for the Yocto Security Set

Deferred with its cost stated when `yocto-security-hardening` was designed and again when it was written on
2026-09-08: the skill routes to `meta-wolfssl` as the FIPS-capable option and states its GPL-2.0/commercial
split, but **it cannot answer "how do I ship FIPS-validated crypto"** beyond that pointer. A real treatment
needs the certificate scope, which validated module versions the layer targets, and the module boundary a
compliance evidence package must reflect — all unverified.

**Now the only substantive gap left in the three-skill set**, which is otherwise complete as of 2026-09-08.
The placement question is also sharper than it was: `yocto-vulnerability-management` now carries the CRA
provisions read from the regulation itself, including the Annex I SBOM requirement and the support period, so
a validated module's certificate and boundary sit closer to that skill's compliance-evidence material than to
hardening's configure-and-verify lane. Decide placement as part of the research pass, not before it.

Related and separately unfinished: post-quantum crypto has no upstream answer either, and the two Yocto-native
candidates (`meta-oqs`, `meta-quantum-safe`) are both self-described as experimental and have never been
compared side by side.

## `test-engineer` Did Not Trigger on Real Test-Writing Work

**Observed 2026-09-06, in this repository, and it is a discovery failure rather than a skill defect.** A
session wrote four new pytest integration tests for `services/tests/test_crawl4ai_integration.py` — squarely
the `TEST-IMPLEMENTATION` and `REGRESSION` modes `test-engineer` declares — and **no test skill appeared in
the session's available-skills listing at any point**. `test-engineer`, `python-testing` and
`test-driven-development` are all deployed under `~/.config/claude/skills/`, so the packages were present and
the agent simply never saw them offered. They were loaded only after the user asked directly, by name.

**What the listing did offer, in a repository containing no Nix at all**, was eight Nix skills
(`direnv-nix-direnv`, `flake-manifest-sync`, `generated-file-verify`, `home-manager`, `nix-flakes`,
`nix-packaging`, `nix-secrets`, `nixos-config`) plus `writing-for-humans`, and later `agents-management` and
`context-architecture`.

**That inversion is explained and is not the finding.** The user confirmed on 2026-09-06 that the Nix entries
came from a parallel session's updates to those skills, so their presence reflects a concurrent edit rather
than ranking, truncation, or sampling. Do not re-derive a listing-behaviour theory from them. What remains
unexplained is only the absence of the test skills, which makes their descriptions the live hypothesis rather
than one of two competing ones.

The skills that *did* surface on their merits share a shape the test skills lacked: `agents-management` names
the literal artifacts `AGENTS.md` and `CLAUDE.md`, and it appeared once those files were being edited.

Cost of the miss, measured rather than assumed. Loading the two skills afterwards found four defects in the
already-committed tests, the material one being that **they were order-dependent** — the readiness poll lived
inside one test, so `pytest -m integration -k streamable` failed three tests on a boot race and had never
been run. A second was a docstring carrying a **false rationale**, claiming to catch a `Mount`-for-`Route`
swap that mutation testing showed it never caught. A third was an auth assertion that passed against a
missing route. `test-engineer`'s "ask what the suite would CATCH" and "tests MUST be order-independent and
self-seeding" rules each name one of these directly. Mutation testing happened at all only because of the
`brief-the-test-engineer-to-mutation-test` memory; nothing prompted the order-independence check.

**Descriptions edited 2026-09-06; activation deliberately NOT measured.** `test-engineer`'s description was
`Design testing strategies, implement test-only coverage, and report fresh validation evidence.` — 106
characters, which fails three of `skill-forge`'s own description checks independently of this incident: no
activation condition, internal jargon (`test-only coverage`, `fresh validation evidence`) instead of language
a user would type, and no path from a request phrased by outcome. It now carries a `Use when` clause, literal
triggers, and an exclusion pointing at `test-driven-development`. `python-testing` gained a `Triggers on:`
token list naming `conftest.py` and `test_*.py`, mirroring the shape that worked for `agents-management`.

The user chose to ship the edits and let the next real test-writing session be the observation, rather than
spend a session on the controlled experiment. **So the edits are unmeasured, and that is the open item.**
Treat the next session that writes tests as the datapoint, and record the outcome here either way — a
non-trigger after the rewrite would be strong evidence that wording is not the lever, which is exactly the
`searchable-code` result in `docs/findings/skill-discovery-limits.md`: repaired across five findings, every
gate green, and it still never activated.

**`test-driven-development` was deliberately left alone.** Its description already excludes "test-only
strategy, coverage, or validation work", and this session wrote tests *after* a working implementation, so
its non-trigger was correct behaviour. An earlier revision of this entry named all three skills; that was
wrong, and broadening it would damage a correctly scoped package.

Related: the repository-wide **Python Skill Set Behavioral Evaluation** section already notes that no
behavioral evidence exists for `python-testing`. This is the first recorded instance of it failing to
activate on work it names.

### Outcome to record

**The next session that writes or fixes tests without being told to load a skill is the datapoint.** Record
here which of `test-engineer` and `python-testing` appeared in its available-skills listing, and whether it
loaded them unprompted. Both results are worth writing down:

- **They trigger** — wording was the lever; the audit below becomes worth executing on the same pattern.
- **They still do not** — wording is not the lever, and that matches `searchable-code` in
  `../docs/findings/skill-discovery-limits.md` (repaired across five findings, every gate green, never
  activated). At that point stop editing descriptions and move the behavior into always-loaded instructions,
  which is what that finding already concluded for a skill whose subject nobody verbalizes.

Do not count a listing appearance that follows a deploy of that same skill as evidence. Both skills surfaced
immediately after their 2026-09-06 redeploy, and the user confirmed the same effect explains the Nix entries
above. A skill a session just edited surfaces for that reason alone.

## Description Audit — 13 Skills Share the Shape That Failed

**Description-focused review completed 2026-09-07; all 13 descriptions expanded with user authorization.**
[Findings and candidate wording](../docs/evaluations/2026-09-07-skill-description-audit.md) distinguish three priority
revisions, three optional refinements, and an initial recommendation to preserve seven descriptions.
The review found all 13 passing both validators and unchanged since this queue was added in `6d947f6`.
The accepted descriptions now clarify `systematic-debugging`'s test-review boundary, expose `repo-management`'s
baseline artifacts, and limit `containers`' Kubernetes scope to workload hardening.
The three optional refinements are also applied: `chezmoi-dotfiles` names managed artifacts and drift symptoms;
`mise-tools` names config files and qualifies failures and migration as mise work; `systemd` names unit extensions
and user-service failures while routing networking configuration to `systemd-networking`.
The user rejected preserving the other seven merely because no defect was proven: the original 120-character
limit was an error, and descriptions should explain the supported work and triggers.
Approved expanded descriptions are now applied to `git-ops`, `github-ops`, `kasetto`, `just-task-runner`,
`systemd-networking`, `bash-shell`, and `posix-shell`, retaining their neighboring-skill boundaries.
Activation is still unmeasured; deployment or a listing appearance after editing is not activation evidence.
The earlier `0c91d24` already revised `test-engineer` and `python-testing`; preserve those edits.
The review corrects the assumption below that debugging and repository setup lack request-time intent:
both support concrete user tasks. Short length or absence of `Use when` alone does not establish a defect.
The historical audit follows; its activation hypothesis and the natural-observation prerequisite remain unmeasured.

Swept 2026-09-06 across all 45 deployed skills, prompted by the `test-engineer` non-trigger above. The
distribution is bimodal, and the split is a repository era rather than a judgment: descriptions written under
the old narrow limit are pure capability statements, while everything written since carries an activation
clause.

**No edits made. This is a review queue, not a defect list** — the hypothesis that wording drives activation
is itself unmeasured, so executing this before the outcome above is recorded would be 13 more unverified
rewrites.

| Length band   | Count | Shape                                                  |
| ------------- | ----- | ------------------------------------------------------ |
| 74–107 chars  | 13    | capability only, **no `Use when` clause**, no triggers |
| 221–350 chars | 11    | `Use when` present, no literal trigger tokens          |
| 380–614 chars | 18    | `Use when`, most with `Triggers on:`                   |

**Rank by whether the subject is a named artifact or an unspoken moment**, because the two fail differently:

- **Highest risk — no artifact for a request to match.** `systematic-debugging` ("Debug non-obvious failures,
  regressions, and flaky tests"), `repo-management` ("repository baseline files, hooks, community templates,
  and read-only hygiene audits"). Both describe a *situation*, and a user in that situation does not name it.
  This is the `searchable-code` failure mode, so treat rewriting them as unlikely to be sufficient on its own.
  `AGENTS.md` in this directory already states the rule that settles them: guidance for "a moment nobody
  verbalizes" belongs in `agents/rules/`, and "no wording repairs it". Apply that test to these two before
  drafting any replacement description.
- **Lower risk — a strong literal tool token is present**, which is the property that demonstrably works for
  `agents-management` (it names `AGENTS.md` and `CLAUDE.md`, and surfaced once those were edited):
  `chezmoi-dotfiles`, `github-ops` (`gh`), `kasetto`, `mise-tools`, `containers` (`Dockerfiles`, `Compose`),
  `just-task-runner`, `systemd`, `systemd-networking`, `bash-shell`, `posix-shell`. `bash-shell` and
  `posix-shell` additionally cross-reference each other, which is the exclusion pattern the newer descriptions
  use and worth preserving in any rewrite.

**A routing collision was introduced on 2026-09-06 and needs resolving in the same pass.** `test-engineer`'s
new description claims `flaky test` as a trigger, and `systematic-debugging` claims flaky tests as subject
matter. They are genuinely different jobs — one asks whether the suite would catch a bug, the other finds a
root cause — but neither description says so. Whichever is edited second should carry the exclusion.

**Out of scope, deliberately:** `skills/shared/agent-stack/skill-review/evals/fixtures/*` also appear in the
short band (`opaque-just-task-runner` at 29 chars, `contextual-just-task-runner`, `mixed-dotfiles-nix`,
`database-reporting`). Those are eval fixtures whose descriptions are the thing under test —
`opaque-just-task-runner` exists *because* its description is opaque. Never "fix" them.

Two length outliers, unrelated to the above: `grilling` at 614 chars is the only skill over the repository's
512 soft budget, and `agents-management` at 342 has no `Use when` clause but is the one skill with direct
evidence of activating anyway.

## Unevaluated Candidate Sources

Recorded 2026-08-26 and never fetched, read, or license-checked. The descriptions are path-based inferences,
not evidence. Before using any material, read the repository license and any separate prose or content license
from primary sources, record provenance, and decide whether the source overlaps an existing skill.

- [wshobson/conductor](https://github.com/wshobson/agents/tree/main/plugins/conductor): inspect as a plugin,
  including agent definitions and commands that Kasetto would not deploy as skills.
- [stellarlinkco requirements agents](https://github.com/stellarlinkco/myclaude/tree/master/agents/requirements):
  compare with archived `design-forge` and its deliberate rejection of a universal atomic `FR-` and `NFR-`
  schema.
- [firecrawl/pdf-inspector](https://github.com/firecrawl/pdf-inspector), recorded 2026-09-13 and **not yet
  fetched or read**: a candidate third converter for `shared/context/document-conversion`, from the same
  publisher as `anydoc`. That skill currently routes two cases to nothing it owns — *"bounding boxes, page
  coordinates, or screenshots: neither; use a layout-aware parser"*, and a scanned or image-only PDF, where
  both converters can only send the whole document to a hosted service. **Whether this fills either gap is
  the open question, not an assumption.** Read it against that routing table before adding a third branch,
  since the skill was rescoped specifically to stop two converters competing for one request. Check the
  licence and whether it processes locally or uploads: the last Firecrawl package reviewed here was
  `not ready` precisely because it omitted that its OCR path transmits the entire document.

## Codex Skill-Description Budget

Recheck the warning that Codex shortened skill descriptions to fit its context budget. The 2026-09-02 archival
reduced the Kasetto-managed common set from 63 skills to 35, of which 25 are repository-owned shared skills.
Start a fresh Codex session and record whether the warning remains. If it does, compare the current common set
with a curated Codex overlay before changing deployment policy. Skill count alone does not establish which
descriptions consume the budget.

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

## Invocation Control Is Unapplied Across the Owned Skills

Carried here 2026-09-11 from `~/.config/claude/TODO.md`, and **the state it describes has since become
absolute**: checked 2026-09-11, no skill under `shared/` or `claude/` sets `disable-model-invocation` or
`user-invocable` at all, and `allowed-tools` appears exactly once, in `claude-code-setup-audit`. The one skill
that restricted invocation and rightly did — `find-skills`, which installs third-party code from GitHub, a
side effect no gate inside a skill can undo — is archived and therefore deployed nowhere. So the worked
example for "when the flag is right" now has to be reconstructed rather than pointed at.

**The `git-ops` half of this question is settled and settled the other way**, and `AGENTS.md` records the
reasoning: the flag never stopped an agent running `git push`, it only withheld the guidance at the moment the
dangerous command ran, and OpenCode ignores the key entirely. Safety there rests on the skill's own
confirmation gates. So what remains is the audit, not that case.

**Ownership is the constraint that makes it need care.** Only owned skills can be edited: a frontmatter change
to an upstream skill is overwritten on the next sync, and making it stick means forking, which trades away
upstream updates for one line of frontmatter. So classify by ownership before classifying by side effect, and
treat an upstream skill with a genuine side-effect problem as a separate decision — fork, or accept and
document — rather than a quick fix. Any figures a previous pass wrote down are stale within days; derive the
owned set from `skills/kasetto/*.yaml` and the locks at audit time.

Steps, once the ownership split is settled:

1. Audit the owned skills by actual behavior rather than by name: which install or execute third-party code,
   write outside the working tree, mutate git history or remotes, or transmit data externally. Candidates
   named on the last pass were `agents-management`, `reflect` and `chezmoi-dotfiles`; `agents-management` both
   writes files and creates symlinks.
2. Decide the bar. `disable-model-invocation: true` costs real capability — the model can no longer reach the
   skill when it would help. Clearly right for "installs code from the internet"; arguably wrong for "writes a
   doc file".
3. Verify OpenCode's handling before touching anything in `shared/`, since those deploy to four agents and a
   Claude-only frontmatter key may be inert or rejected elsewhere. Unverified so far.
4. Record the resulting convention in `AGENTS.md` so new skills are classified at authoring time rather than
   in the next audit.

Open sub-question: whether tightening `allowed-tools` rides along with this or stays separate.

## Skills With No Usage Signal — Recheck After 2026-10-08

Measured 2026-09-08 across 738 Claude Code transcripts (2026-08-09 to 2026-09-08) and `skillUsage` in
`.claude.json`: 28 of the 50 skills deployed there had a lifetime counter of zero and no transcript hit.
**None of that is evidence of disuse.** Every skill directory carried an mtime inside the preceding week — the
set was redeployed and largely renamed in that window (`bash-pro` → `bash-shell`, `git-master` → `git-ops`,
`python-type-safety` → `python-typing`, `technical-writing` → `writing-documentation`, among others) — and
`skillUsage` keys on the name, so the counters reset with each rename. A zero then meant "deployed last week".

**Recheck no earlier than 2026-10-08**, by which point a month of sessions will have accumulated under the
current names. `/doctor` re-runs the measurement. The inputs are `skillUsage` — `usageCount` is a lifetime
total that never windows, while `lastUsedAt` is trustworthy for skills because it is written only on real
dispatch — and `Skill` tool_use entries in `~/.config/claude/projects/*/*.jsonl`.

**The recheck was partly compromised the same day it was scheduled.** Two commits set 21 of the 28 to
`name-only`, which removes the description the model matches against, so those are now reached mainly by being
named explicitly and a future zero on them will mean "never asked for by name" rather than "considered and
passed". That is an acceptable trade for domain skills that would be invoked deliberately anyway, and a
murkier one for `python-async-patterns` or `direnv-nix-direnv`, which were expected to fire on their own.
Weigh the two groups differently, and read the full-description group as the clean test cases:
`context-architecture`, `context-compression`, `flake-manifest-sync`, `generated-file-verify`, `git-ops`,
`github-ops` and `repo-management`.

This shares its outcome with the description-audit entries above. A non-trigger on a skill that still carries
a full description is the same evidence those entries are waiting for.

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
