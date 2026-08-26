# Skills — future work

Open items for the skills stack. Split out of `skills/README.md` on 2026-08-21 so the
README describes how the stack works and this file tracks what is still owed. Paths are
relative to `skills/` unless noted. Repository-wide items live in
[../TODO.md](../TODO.md).

- **`opencode/headroom-management`** — currently OpenCode-only; generalize it to work with
  Claude Code too, then move to `shared/`.
- **`claude/reflect` — re-evaluate the OpenCode side.** `reflect` stays in `claude/`
  rather than moving to `shared/`: OpenCode's `skills/reflect/` is auto-installed by the
  `oh-my-opencode-slim@2.2.8` plugin, so a shared copy would be a collision rather than a
  deploy — Kasetto does not own that directory, and the plugin reinstalls its own version.
  The drift is accepted for now. Revisit once it is decided whether the plugin stays and
  whether its skill auto-install can be disabled. Detected 2026-08-21 while evaluating the
  two skills:
  - Of the 13 OpenCode skill directories no lock owns, 8 match the plugin's bundled set
    (`clonedeps`, `codemap`, `deepwork`, `oh-my-opencode-slim`, `reflect`, `simplify`,
    `verification-planning`, `worktrees`) and `release-smoke-test` matches a skill upstream
    keeps under `.agents/`. The other four — `common`, `config-benchmark`,
    `opencode-plugins`, `writing` — are unexplained.
  - The installed copy hardcodes `/home/user/.local/share/opencode/opencode.db`, a
    contributor's own machine path, so its `--sessions` mode cannot run here. Upstream has
    since fixed it; the local copy is frozen at the 2026-07-12 install.
  - The plugin's skill-sync keeps its own manifest and atomically replaces skill
    directories, so a hand deletion is unlikely to survive a sync. Not verified further.
  - This blocks decision 14 and the M3 stage of
    [../docs/plans/knowledge-vault/design.md](../docs/plans/knowledge-vault/design.md), both of which
    assume a shared `reflect`.
  - The material worth keeping is already folded into `claude/reflect`; see its
    `ATTRIBUTIONS.md`. The `--sessions` archaeology idea is declined rather than deferred —
    §8's compaction backlog covers that ground Claude-natively.
- **Quality-refresh pass** — triaged `skill-review` audit of pre-`skill-forge` skills (e.g.
  the `grilling` stub); report-first. Can co-review with a second model via
  OpenCode — see [../docs/skill-co-review.md](../docs/skill-co-review.md).
- **`claude-md-management` plugin** — reviewed and recommended for removal rather than a
  fork: its rubric awards 35 of 100 points for things it never reads the codebase to
  check, and its discovery searches for two filenames that do not exist. Everything it
  does is already covered by `claude/reflect` and `shared/system-prompts`. The evidence
  for each defect is in `shared/agents-management/ATTRIBUTIONS.md`.
- **`shared/writing-for-humans` — evaluate a burstiness check.** Deferred 2026-08-24
  while reviewing three AI-writing skills for adoptable material. The idea comes from
  [israelsaba/ai-writing-detector-skill](https://github.com/israelsaba/ai-writing-detector-skill)
  (MIT): score sentence-length variation as a coefficient of variation, `std/mean`, and
  treat a low score as the rhythm tell. It is the only countable test for rhythm anyone
  in that review offered, and the skill currently has none — "vary sentence length" is
  the one rule there with no way to fail it against a specific passage.
  - Not adopted as written, for two reasons. Its thresholds (human above 0.40,
    algorithmic below 0.35) cite no study in anything retrievable, and shipping an
    unsourced number as a gate is the kind of confident-looking assertion the skill
    itself bans. And a CV needs computing, so it is a script, not a rule — which makes
    it a companion check like `check-doc-corpora.sh`, not a line in `SKILL.md`.
  - To evaluate: measure the CV of a dozen real documents from `docs/plans/` and of a
    few known-model-written passages, and see whether the distributions separate at all
    on this corpus before picking any threshold. If they do not separate, record that
    and close the item — a negative result here is worth as much as the check.
- **`shared/git-operations` — regrade and improve.** Written 2026-08-26 to replace
  `git-master`, whose SUL 1.0 licence could not be carried. Two independent `skill-judge`
  passes scored it 86/120 then 91/120, both Grade C; every defect each raised was verified
  in a scratch repo and fixed, but **the 91 is the score for the version the second grader
  read, not the one on disk** — the post-fix package has never been graded. Open items:
  - Re-run `skill-judge` from a fresh subagent against the current package. Both prior
    rounds found real defects the previous round missed, so a third is not ceremony.
  - The skill has never been used on a real task. Trigger behaviour is unmeasured in both
    directions, and none of the confirmation gates has fired in anger.
  - `SKILL.md` grew from 260 to 363 lines across the two fix rounds, all additive. The next
    substantive addition should displace something rather than append.
  - One claim is still marked *reported, not measured*: that rebasing a branch whose tip is
    a merge commit can collapse it to empty. Measure it or cut it.
- **`shared/github-operations` — regrade and improve.** Written 2026-08-26. One `skill-judge`
  pass scored 88/120, Grade C; every defect was re-measured against live `gh` and fixed, but
  the score belongs to the graded version, not the fixed one. The skill has never run against
  a real task.
  - **The defect that pass caught is worth remembering as a pattern, not just a fix.** The
    draft claimed sub-issues had no `gh` CLI surface, citing a real measurement — `gh issue
    --help` genuinely has zero occurrences of "sub-issue". But the flags live on the
    subcommands: `gh issue edit --add-sub-issue` and `gh issue create --parent` shipped in
    v2.94.0 on 2026-06-10. A correct measurement of the wrong object licensed a false
    generalisation, which is the failure the skill's own Iron Law exists to prevent. The
    corrected form is now the skill's worked example.
  - Claims still marked *reported, not measured*: the head-ref-equals-base auto-close, the
    `gh search code` under-reporting, and the four Actions traps. The first two need a
    repository to mutate; read-only probing cannot settle them.
  - Re-run `skill-judge` from a fresh subagent, with read-only `gh` authorisation and an
    explicit ban on mutations — that authorisation is what made this pass useful, since three
    of its findings were refutations of claims no amount of reading would have caught.
- **A proper GitHub Actions skill — deferred 2026-08-26, deliberately.**
  `shared/github-operations` ships `references/actions-basics.md` as a short orientation and
  says so in the file: enough Actions grounding to do PR and repository work, explicitly not a
  reference manual. Its closing section lists what it does not cover — matrix strategy,
  caching design, self-hosted runners, reusable-workflow authoring, composite actions,
  environments and deployment gates, artifact retention, the expression language — and that
  list is the scope of the skill owed here. **The boundary is the point: if
  `actions-basics.md` starts growing to meet Actions questions, that is the signal to build
  this, not to keep extending the reference.**
  - The evidence is already gathered. Mining `netresearch/github-project-skill` on 2026-08-26
    found its Actions material to be a **second coherent skill of roughly 82 KB across eight
    files** (`actionlint-guide`, `actions-upgrade-guide`, `reusable-workflow-pitfalls`,
    `reusable-workflow-security`, `workflow-bash-patterns`, `ci-runner-capacity`,
    `agentic-workflows`, `pages-and-collector-workflows`) — and that package's own README says
    CI/CD is delegated elsewhere, so a quarter of its payload contradicts its stated scope.
    That is the split to copy, not the sprawl.
  - **Licence: facts only.** That upstream is `LICENSE-MIT` for scripts and assets but
    **CC-BY-SA-4.0 for all prose** ("skill definitions, documentation, references"). Nothing
    written can be lifted or lightly edited; re-derive from primary sources and write fresh,
    exactly as `git-operations` had to.
  - **Do not repeat its transcription defects.** `ci-runner-capacity.md` copies GitHub's
    published concurrency-limit table with **no verification date**, and
    `actions-upgrade-guide.md` is 70–80% a version inventory that Renovate invalidates. Both
    are live-recoverable and both drift while reading as authoritative.
  - Claims worth measuring first, all currently marked *reported, not measured* in
    `actions-basics.md`: the reusable-workflow permissions **intersection**; `GITHUB_TOKEN`
    not raising events; a renamed job wedging a required status check; a `pull_request` rerun
    reusing the original merge commit and so testing the old base; `sha_pinning_required`
    failing at `Set up job`; and the `push` vs `merge_group` trigger gap under a merge queue.
    Several need a scratch repository with workflows enabled, which read-only probing cannot
    reach — so budget for that, or keep the markers.
- **Third-party skill pointers — captured 2026-08-26, unevaluated.** Four sources handed over
  for later evaluation. **Nothing below has been fetched, read, or licence-checked**: the
  capture was explicitly scoped to recording the URLs, so every characterisation here is
  inferred from the path alone and none of it is evidence. Before any adoption, each needs the
  full treatment the `writing-for-humans` entry above demonstrates — the raw `LICENSE` file
  read directly (NEVER `gh repo view --json licenseInfo`, which reports `null` for repos that
  do carry one), a check for a separate content licence on reference prose, and a named reason
  it would or would not be adopted as written.
  - The content-licence check is not a formality. `netresearch/agent-rules-skill`, evaluated in
    this stack earlier, is MIT for code and **CC-BY-SA-4.0 for content** — the reference prose.
    Share-alike would propagate into any adapted text and collide with the Apache-2.0
    obligations `shared/agents-management` already carries. Check for this per source, before
    lifting prose rather than after.
  - <https://github.com/modem-dev/skills/tree/main/write-discoverable-code> — name suggests
    code-discoverability guidance. Adjacency to check: `shared/system-prompts` and
    `shared/technical-writing`, and whether it overlaps `agents-management`'s llms.txt lane.
  - <https://github.com/microsoft/skills/tree/main/.github/skills/continual-learning> — name
    suggests session-learning capture. Adjacency to check: `claude/reflect`, which owns that
    lane here, including its compaction backlog. Note the path: it ships under `.github/skills/`,
    so its scope conventions may be Copilot-shaped rather than portable.
  - <https://github.com/wshobson/agents/tree/main/plugins/conductor> — a plugin rather than a
    bare skill, so it may carry agent definitions or commands that this stack deploys
    differently; Kasetto installs skill directories, not plugins.
  - <https://github.com/stellarlinkco/myclaude/tree/master/agents/requirements> — an agent
    definition, not a skill, and on `master` rather than `main`. Adjacency to check:
    `shared/design-forge`, which owns the requirements-document contract, and the deliberate
    decision recorded there NOT to use `references/authoring.md`'s atomic `FR-`/`NFR-` schema.
- **Pin third-party versions** — third-party sources currently track `main`. If a surprise
  upstream change is a concern, add `ref:` pins in `kasetto/base.yaml` and roll forward
  deliberately with `kst sync --update`.
