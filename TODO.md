# Skills Future Work

Operational and future-feature backlog for the skills stack, including candidate sources not yet evaluated.
The completed 2026-09 review's verdicts and evidence are the record in
[../docs/evaluations/2026-09-shared-skill-review.md](../docs/evaluations/2026-09-shared-skill-review.md), and
archived reviews still deferred are the rows marked "Review is deferred" in
[archived/README.md](archived/README.md). The restored embedded skills are tracked below.
Repository-wide items live in [../TODO.md](../TODO.md).

## Embedded Domain — Review Ledger

The five embedded skills were restored on 2026-09-07 with new names. This restoration covers package moves,
sibling routing, top-level license placement, and required Markdown formatting. It does not establish the
accuracy of the existing technical guidance or agent activation behavior.

Review one skill at a time using the current `skill-forge` and `skill-review` guidance. Review completion
does not mean fixes have been applied or behavioral evaluation has passed. Discovery and hardware/build
behavior remain unmeasured unless a linked review records otherwise.

Original materials are in `~/src/embedded-linux/`. Buildroot sources were located on 2026-09-07:
`docs/buildroot-manual.pdf` (2026.05, GPL-2.0) and `bootlin-training-materials/buildroot/` (training PDFs
declare CC BY-SA 3.0). The targeted Buildroot PDF comparison completed on 2026-09-07; see the review's source map.
Buildroot's attribution record and source-corresponding explanations were repaired on 2026-09-07. Full model-based
evaluation and project-specific hardware/release qualification remain outstanding.

Buildroot repository survey completed 2026-09-07 across the three subtrees in `~/src/embedded-linux/repos/`.
[Evidence and conservative proposals](../docs/evaluations/2026-09-07-buildroot-repository-survey.md): refine the existing
local-source iteration and overlay/artifact checks; add one small image-capacity subsection. The user approved these
additions, and they are implemented in the repaired Buildroot skill. The other skills' current states are below.
Buildroot/genimage first-party sources govern adoption; the survey records resolved third-party conflicts and excludes
unverified fork-specific guidance.

| Skill                                              | Review status                                         | Verdict / remaining work                                                                                                                                                                                                                                                                                                             | Evidence                                                                                                                                                                                                                                                                       |
| -------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `buildroot-development` (formerly `buildroot-dev`) | Review lite and repairs completed 2026-09-07          | **Ready with risks.** F1–F12 and approved A–C addressed; native package, hook, Kconfig, and image checks pass. Full behavioral evaluation and hardware/release qualification remain pending. Flagged 2026-09-08 for a bounded recheck — see *Re-Review the Other Four Embedded Skills*.                                              | [Repair evidence](../docs/evaluations/2026-09-07-buildroot-development-repair.md); [original review](../docs/evaluations/2026-09-07-buildroot-development-review.md)                                                                                                           |
| `embedded-linux-bringup`                           | Review lite and approved repairs completed 2026-09-07 | **Ready with risks.** F1–F15 addressed; native DT comparison/overlay and verity image checks pass. Full model evaluation and hardware/release qualification remain deferred. Flagged 2026-09-08 for a bounded recheck — see *Re-Review the Other Four Embedded Skills*.                                                              | [Repair evidence](../docs/evaluations/2026-09-07-embedded-linux-bringup-repair.md); [original review](../docs/evaluations/2026-09-07-embedded-linux-bringup-review.md)                                                                                                         |
| `kas-build-orchestration`                          | Review lite and approved repairs completed 2026-09-07 | **Ready with risks.** F1–F14 addressed; 16 native/wrapper contract cases pass. Model evaluation, real container/CI execution, builds, and release qualification remain deferred. Flagged 2026-09-08 for a bounded recheck — see *Re-Review the Other Four Embedded Skills*.                                                          | [Repair evidence](../docs/evaluations/2026-09-07-kas-build-orchestration-repair.md); [original review](../docs/evaluations/2026-09-07-kas-build-orchestration-review.md)                                                                                                       |
| `u-boot-development`                               | Review lite and approved repairs completed 2026-09-07 | **Ready with risks.** F1–F17 addressed; native environment, FIT, load-guard, helper and DM checks pass. Historical provenance uncertainty, model behavior and board qualification remain open. Flagged 2026-09-08 for a bounded recheck — see *Re-Review the Other Four Embedded Skills*.                                            | [Repair evidence](../docs/evaluations/2026-09-07-u-boot-development-repair.md); [original review](../docs/evaluations/2026-09-07-u-boot-development-review.md)                                                                                                                 |
| `yocto-openembedded-development`                   | Review lite and approved repairs completed 2026-09-07 | **Ready with risks.** F1–F12 addressed and the specification violation cleared. The CC BY-SA adaptation the provenance investigation found in the best-practices reference was re-derived independently on 2026-09-08, resolving the MIT conflict. Packaging/QA coverage added the same day. No Yocto execution or model evaluation. | [Follow-up](../docs/evaluations/2026-09-08-yocto-openembedded-development-followup.md); [repair evidence](../docs/evaluations/2026-09-07-yocto-openembedded-development-repair.md); [original review](../docs/evaluations/2026-09-07-yocto-openembedded-development-review.md) |

The `embedded-linux-bringup` review and approved F1–F15 repairs completed on 2026-09-07. The records distinguish
first-party source checks, targeted PDF comparison, native artifact tests, validator acceptance, and unmeasured behavior.
The `kas-build-orchestration` review lite completed on 2026-09-07 against kas 5.3 documentation and implementation.
Approved F1–F14 repairs are complete, including native repository/lock/cleanup/signature checks and wrapper argument
checks. Actual container/CI execution and model behavior remain unmeasured.
The `u-boot-development` review and approved F1–F17 repairs completed on 2026-09-07 against upstream v2025.10.
The bounded provenance investigation records known repair influence and unresolved historical derivation. Native helper,
environment recovery/persistence, FIT rejection, load-guard and driver-model checks pass; board security/recovery and
model behavior remain unqualified. The final restored skill, `yocto-openembedded-development`, completed review lite
and its approved F1–F12 repairs on 2026-09-07, against pinned Poky `yocto-5.0.12` sources and the Honister 3.4
migration guide. **All five embedded repairs are now complete.** No Yocto build, parse, SDK, sstate or target
operation was executed, so every technical correction there is source- and documentation-backed only.

The Yocto bounded provenance investigation reached a different conclusion from the one the package previously
asserted: `references/yocto-best-practices.md` was an established structural adaptation of Belloni's CC BY-SA 3.0
Bootlin deck, corroborated by an inherited stale command and by the introducing port brief's own instruction to
rewrite structurally lifted prose and strip attributing framing. **Resolved 2026-09-08 by independent re-derivation,
keeping MIT.** Six of the ten correspondences had already lapsed through the 2026-09-07 repair; the remaining four
were rebuilt from primary sources (`bitbake.conf`'s include order, `meta-poky/conf/distro/poky.conf`, the section's
own correctness-versus-hit-rate thesis, and the pruning tool at the pinned release). Nothing was relicensed, and the
attribution record is kept permanently rather than closed — see the convention now in `AGENTS.md`.
A third Bootlin deck (Dautheribes 2024) sits in the same source directory and is named nowhere in the package; no
source relationship was asserted, because nothing distinctive corresponds.

On 2026-09-08 the third-party skill set
[awesome-yocto-ai-agent-skills](https://github.com/prashantdivate/awesome-yocto-ai-agent-skills) (MIT, commit
`0e268dc`) was compared against `yocto-openembedded-development`. Its prose is thinner than ours and none was adopted,
but it surfaced four genuine coverage gaps, now written from pinned Poky `yocto-5.0.12` sources: packaging
(`PACKAGES`/`FILES` ordering and the `installed-vs-shipped` error), `PACKAGECONFIG`, `LAYERDEPENDS` naming collections
rather than directories, and build output not always sitting under `tmp/`. Its compliance, SBOM, CVE and bundled-script
material was reviewed and rejected as weaker than what the package already carries. **This source is evaluated;
do not re-survey it.** Attribution for the gap selection is recorded in the skill's `ATTRIBUTIONS.md`.

Full model evaluations, hardware/release qualification, and QEMU skill creation remain separate decisions.
Buildroot's completed source/deployment commits (`9a512da`, `d56586d`) are preserved.

### Re-Review the Other Four Embedded Skills — Non-Urgent

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
Full model evaluation and hardware qualification stay separately deferred as recorded above. Record findings the
normal way, in a dated file under `../docs/evaluations/`.

### Yocto Tooling Candidates for the General Skill Review

User-supplied on 2026-09-08 for a later pass over `yocto-openembedded-development`. Metadata below was read from the
GitHub API the same day; **re-check staleness before adopting any of it**, because a layer that stopped at an old
release is a liability rather than an asset. None of this is adopted yet, and a skill should route to upstream
mechanisms before third-party tooling.

| Tool                                                                                                     | What it is                                                              | State on 2026-09-08                         |
| -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------- |
| [oelint-adv](https://github.com/priv-kweihmann/oelint-adv)                                               | advanced recipe linter, the strongest general candidate here            | 86★ BSD-2-Clause, pushed 2026-09-02         |
| [yocto-kiss](https://github.com/bootlin/yocto-kiss)                                                      | a deliberately unelaborate working Yocto setup; useful as a baseline    | 206★ MIT, pushed 2026-08-24                 |
| [vscode-bitbake](https://github.com/yoctoproject/vscode-bitbake)                                         | **first-party** BitBake language support for VS Code                    | 74★, pushed 2026-09-01                      |
| [bitbake-language-server](https://github.com/Freed-Wu/bitbake-language-server)                           | editor-agnostic LSP alternative to the above                            | 18★ GPL-3.0, pushed 2026-09-07              |
| [yocto-lens](https://github.com/prashantdivate/yocto-lens)                                               | terminal UI over static analysis, layer validation, patch/licence audit | 22★ MIT, pushed 2026-07-28                  |
| [meta-buildutils](https://github.com/priv-kweihmann/meta-buildutils)                                     | build-time utility classes                                              | 12★ BSD-2-Clause, pushed 2026-07-21         |
| [oelint-vscode](https://github.com/priv-kweihmann/oelint-vscode)                                         | editor front end for oelint-adv                                         | 8★, pushed 2026-04-08                       |
| [meta-osselot](https://github.com/iris-GmbH/meta-osselot)                                                | Osselot licence-compliance integration                                  | 7★ MIT, **pushed 2025-02-18**               |
| [meta-bitbake-variable-substitution](https://github.com/coreycothrum/meta-bitbake-variable-substitution) | expand BitBake variables from external scripts                          | 3★ MIT, pushed 2026-06-29                   |
| [bbclient](https://github.com/AngryMane/bbclient)                                                        | utility commands for BitBake                                            | 6★ MIT, **pushed 2023-08-09 — likely dead** |

Konrad Weihmann ([priv-kweihmann](https://github.com/priv-kweihmann)) maintains several more embedded-development
utilities the user rates highly; worth a scan when this pass happens.

The security-relevant layers from the same list — `meta-sca`, `meta-quantum-safe`, `meta-sbom-cve-check` and
`sbom-cve-check` — are being assessed as part of the Yocto security skill work and are not repeated here.

### Yocto/OpenEmbedded Testing Coverage Is Missing

**Gap identified by the user on 2026-09-08:** `yocto-openembedded-development` says nothing about how to *test* a
Yocto build or the things it produces. That is a real omission for a skill whose diagnosis lane assumes evidence,
since the upstream test machinery is where much of that evidence comes from.

Cover the upstream mechanisms first, and confirm each against the release-matched Test Environment Manual:

- `oeqa` and its selftest suite (`oe-selftest`), the layer-level runtime tests, and how a layer supplies its own.
- `testimage` and `testexport`, and how they reach a target or QEMU.
- `ptest` — enabling `DISTRO_FEATURES += "ptest"`, the `ptest-runner`, and per-recipe `ptest` packages.
- `runqemu` as a test harness rather than as a demo.
- Reproducibility testing (`oe-check-sstate`, the `reproducible` selftest) as a build-integrity check.
- Where each of these puts results, and what a passing run does *not* prove.

Third-party candidate: [meta-shift](https://github.com/shift-left-test/meta-shift), shift-left testing for Yocto
(10★ MIT, pushed 2026-08-06). Assess it only after the upstream mechanisms are covered — it is a wrapper around
tooling the skill should be able to describe unaided.

Open question to settle first: whether this belongs in `yocto-openembedded-development` or in a separate skill.
Testing spans build-host checks, on-QEMU runtime tests and on-hardware tests, and the last of those already routes
to `embedded-linux-bringup`, so the seam is not obvious.

### Embedded QEMU Skill Candidate

Consider `embedded-qemu-emulation` for repeatable boot–test–debug workflows across embedded Linux projects, independent
of their build system. LKMC supplies useful patterns: inspectable launch commands, disposable disk state, serial logs,
debugger attachment, guest-result checks, and isolated concurrent runs. Verify mechanics against QEMU's release-matched
documentation; do not import LKMC's wrappers or assume arbitrary board images/DTBs work on `virt`. Keep hardware-dependent
validation and runtime driver diagnosis with `embedded-linux-bringup`. Assess moving its existing QEMU guidance rather
than duplicating it. Exclude general VM management, desktop virtualization, and cloud workloads. Candidate only;
creation is not yet authorized. [QEMU machine-model reference](https://www.qemu.org/docs/master/system/arm/virt.html).

## Nix Domain — Remaining Work

The 2026-09-06 nix-domain consolidation is complete except for the items below: three skills promoted from
`~/src/nix-config` (`direnv-nix-direnv`, `flake-manifest-sync` → `shared/nix/`; `generated-file-verify` →
`shared/git/`; `colmena-deploy` stays repo-local) and five archived originals fixed per their mapping-verified
fix lists and restored to `shared/nix/`. Verdicts, evidence, and coverage limits:
[../docs/evaluations/2026-09-06-nix-domain-restore.md](../docs/evaluations/2026-09-06-nix-domain-restore.md).

- **`nix-wrapper-modules` — still archived; restore after:** trimming the 795-char description; rewriting the
  `wrappedModules` deprecation as completed (the alias is gone from upstream `main`, verified 2026-09-05);
  fixing the Mode C example's `config.configFile.path` → `config.constructFiles.gitconfig.path`; re-verifying
  against current upstream (pre-1.0, already moved — `inputs.pkgs` injection is undocumented in its
  api-reference). Contingent: nix-config still holds the wrapper inputs deliberately but with no consumer —
  restore only once that decision lands in adoption; if the inputs are dropped and no other repo adopts the
  library, delete instead. The nix-packaging skill already stands alone either way.
- **Deferred full `skill-review` pass** on the eight nix-domain-consolidation skills (five restored + three
  promoted): all shipped at review lite, so verdicts are ready / ready-with-risks with discovery behavior
  unmeasured.
- **Parked named risks** (verified as risks, not defects, during the restore): nix-packaging's Electron
  dependency list may be dated for current nixpkgs; nix-flakes' deprecation/flag claims assume modern CppNix,
  Lix parity unverified; the `or`/`?` null-tolerance wording in home-manager was verified only on Determinate
  Nix 2.34.8; `direnv-nix-direnv`'s `source_url` example still pins nix-direnv 3.1.2 — refresh only after
  verifying the newer tag's hash.
- **`nix-dendritic-pattern` — deleted from the archive 2026-09-06**; its value is fully accounted for in
  nix-config (nine `dendritic-*` skills, six `den-*.md` references, the pin-debt TODO entry). It was the only
  document verified at den rev `e8e8de1e` (the rev nix-config's lock actually pins, while its live den docs
  still stamp `2040b613`); nix-config's pin-debt lane can recover it from git history
  (`skills/archived/nix/nix-dendritic-pattern/`) if needed.

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

## Containers — Review Podman Coverage

Deferred 2026-09-07 at the user's request. The `containers` skill currently names Docker and OCI containers,
but its body prefers Docker commands and its package contains no Podman, Quadlet, Containerfile, or Buildah guidance.

Review the intended Podman scope before extending the skill. Assess runtime selection, rootless operation,
Compose-provider differences, and systemd/Quadlet integration against current primary documentation.
Then propose matching description triggers and body/reference guidance; adding a Podman trigger alone would
advertise coverage the package does not yet provide. Keep Docker behavior intact and record validation limits.
No Podman support or activation behavior has been verified.

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
- **Real cost if missed.** `git-ops` (106) carries the confirmation gates that stand in for
  `disable-model-invocation`, so a non-trigger means the guidance is absent exactly when a destructive command
  runs. That makes it the most valuable of the 13 to get right, independent of how easy it is.
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

## `agents-management` Rework Behind `context-architecture`

Deferred by the 2026-09-06 grilling (decision record:
[../docs/plans/context-architecture-skill.md](../docs/plans/context-architecture-skill.md)): once
`context-architecture` has survived first real use, align `agents-management`'s templates with the named
default layout, refresh `references/loading-model.md`'s client adapters, and run both skills through the
deferred `skill-review` pass together. The minimal routing edits (description ownership line, initialize and
audit branch pointers) already shipped with the new skill; the templates deliberately did not, so they conform
to an exercised layout rather than a new one.

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
