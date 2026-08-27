# Skills — future work

Open items for the skills stack. Split out of `skills/README.md` on 2026-08-21 so the
README describes how the stack works and this file tracks what is still owed. Paths are
relative to `skills/` unless noted. Repository-wide items live in
[../TODO.md](../TODO.md).

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
  does is already covered by `claude/reflect` and `shared/agent-stack/system-prompts`. The evidence
  for each defect is in `shared/agent-stack/agents-management/ATTRIBUTIONS.md`.
- **`shared/writing/writing-for-humans` — evaluate a burstiness check.** Deferred 2026-08-24
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
- **`shared/git/git-operations` — third regrade done 2026-08-26, all findings fixed.** Written
  2026-08-26 to replace `git-master`, whose SUL 1.0 licence could not be carried. Three
  independent `skill-judge` passes: 86/120, then 91/120, then **107/120 (Grade B)**. Every
  defect each round raised was reproduced in a scratch repo before being fixed, and the
  third round's four command-level defects were **re-verified independently** rather than
  taken on the grader's word. What that round found, all now fixed:
  - **`references/recovery.md` gave a deleted-branch recovery command that returns the wrong
    hash** — the worst defect class a recovery document can have, a confident wrong answer
    instead of an error. `git reflog | grep -i "<branch>"` matches only the
    `checkout: moving from/to <branch>` lines, which carry the **branch point**; the tip sits
    on an unmatched `commit:` line. Restoring from it yields an EMPTY branch and reads as
    "the work was never committed". Reproduced: true tip `1aafd89`, grep returned only
    `f2cb4d5`. Replaced with `git fsck --lost-found` as the primary route.
  - "`--git-path` … (both as absolute paths)" was false under the very configuration the
    skill names four lines later: husky sets `core.hooksPath` **relatively**, so the path is
    relative too (`../../.husky/pre-commit` from two levels down). Only a linked worktree is
    unconditionally absolute.
  - The pre-commit detector false-positived on any hand-written hook mentioning "pre-commit"
    in a comment, routing the agent into guidance the same section disclaims. Now matches
    pre-commit's own generated banner.
  - The push fallback hardcoded `origin/main` in a skill whose own opening says a repository
    with no `main` is ordinary — a Broken Own Rule. Now discovers `origin/HEAD`.
  - Signing had **zero description coverage**, so the section answering "why does git report
    `No signature` on my signed commit" could not fire on that question. Keywords added.
  - **The length instruction was honoured by displacement, not appending.** `SKILL.md` is
    368 lines against 363 before — net +5 while absorbing every fix, because 118 lines moved
    into two new references: `signed-commits.md` (44) and `rewriting-hooks.md` (74), each
    with a symptom-shaped load trigger and a "do NOT load" line.
  - **Still true and still the main gap: the skill has never been used on a real task.**
    Trigger behaviour is unmeasured in both directions, and no confirmation gate has fired
    in anger. Grading is not exercise.
  - One claim stays marked *reported, not measured*, by decision 2026-08-26: that rebasing a
    branch whose tip is a merge commit can collapse it to empty. Leaving the marker is honest
    and costs nothing; measuring it was declined rather than deferred.
  - Worth keeping from the round: the grader reproduced **22 empirical assertions and 21 held
    exactly**, including the `gpgsig` message-body spoof, which is real — an unsigned commit
    whose body begins `gpgsig -----BEGIN SSH SIGNATURE-----` reads as signed without the
    `sed '/^$/q;p'` guard. That guard is load-bearing, not decoration.
- **`shared/git/github-operations` — second regrade done 2026-08-26, all findings fixed.** Two
  `skill-judge` passes: 88/120, then **103/120 (Grade B)**. Both ran with read-only `gh`
  authorisation and an explicit mutation ban, which is what made them useful — several
  findings in each round were refutations no amount of reading would have produced.
  - **The pattern both rounds caught is the same one, and it is worth remembering over any
    individual fix: a correct measurement of the WRONG OBJECT licenses a false
    generalisation.** Round one: the draft claimed sub-issues had no `gh` surface, citing a
    true measurement (`gh issue --help` genuinely has zero occurrences of "sub-issue") — but
    the flags live on the SUBCOMMANDS, `gh issue edit --add-sub-issue` and `gh issue create
    --parent`, shipped v2.94.0 on 2026-06-10. Round two found the identical shape twice more:
    "`gh pr review` has no resolve verb" (true) was widened into "replying to a review thread
    needs GraphQL" (false — REST has `POST …/comments/{id}/replies`), and a CLI measurement
    was used to settle an API question. The skill now says explicitly that there are **three
    surfaces, not two**, and that REST must be ruled out before concluding GraphQL.
  - **The worst defect was that the skill's own flagship command reproduced the failure it
    exists to prevent.** The subcommand-discovery loop keyed on a section header
    `AVAILABLE COMMANDS` — which `gh run` and `gh workflow` use, but `gh issue`, `gh pr`,
    `gh repo` and `gh release` do NOT (they use `GENERAL COMMANDS` + `TARGETED COMMANDS`).
    Independently reproduced: the loop iterated **zero times** on `gh issue`, printed
    nothing, and an agent reads that as "no such flag" — the exact false conclusion the
    twelve lines above it refute. Fixed, plus a zero-result guard that MUST report discovery
    failure rather than absence, a `/^[A-Z]/{f=0}` reset (the old form leaked `FLAGS` and
    `LEARN` into the loop) and a `gsub` for the trailing colon.
  - **A rate-limit fact was simply wrong**: "presents as a 403, not a 429". GitHub's REST
    documentation, read verbatim 2026-08-26, says **both** primary and secondary limits
    return "a `403` **or** `429` response". A handler written to the old rule retries
    straight into the other code. Now states both, plus the `retry-after` /
    `x-ratelimit-reset` guidance that was missing entirely.
  - `SKILL.md` is 287 lines. The description was narrowed and re-fitted under the 1024-char
    ceiling — it hit 1056 on the first attempt, which is the ceiling the root `AGENTS.md`
    warns a keyword-dense description reaches easily.
  - **Deferred by decision, not oversight: general issue-management coverage.** The old
    description advertised "issues and sub-issues" while the body carried sub-issues only as
    a methodological worked example — no issue types, no `blocked-by`/`blocking`
    relationships, no `gh issue list` filtering, all of which shipped with v2.94.0. Rather
    than grow the skill, the description now says "Not general issue management". If Issues
    2.0 work becomes common, that is the signal to add the surface — same boundary discipline
    as the deferred Actions skill below.
  - Claims still marked *reported/documented, not measured*, all by decision 2026-08-26: the
    head-ref-equals-base auto-close, the `gh search code` under-reporting, the four Actions
    traps, and the GraphQL `userErrors` fail-open. The last was previously **unmarked** and is
    the most load-bearing claim in `graphql-operations.md`; it now carries its marker, and it
    is the one to confirm the first time a real mutation runs. All need mutations, which the
    read-only authorisation forbids.
  - **Still true: the skill has never run against a real task.** Trigger behaviour is
    unmeasured in both directions.
- **A proper GitHub Actions skill — deferred 2026-08-26, deliberately.**
  `shared/git/github-operations` ships `references/actions-basics.md` as a short orientation and
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
    obligations `shared/agent-stack/agents-management` already carries. Check for this per source, before
    lifting prose rather than after.
  - <https://github.com/modem-dev/skills/tree/main/write-discoverable-code> — name suggests
    code-discoverability guidance. Adjacency to check: `shared/agent-stack/system-prompts` and
    `shared/writing/technical-writing`, and whether it overlaps `agents-management`'s llms.txt lane.
  - <https://github.com/microsoft/skills/tree/main/.github/skills/continual-learning> — name
    suggests session-learning capture. Adjacency to check: `claude/reflect`, which owns that
    lane here, including its compaction backlog. Note the path: it ships under `.github/skills/`,
    so its scope conventions may be Copilot-shaped rather than portable.
  - <https://github.com/wshobson/agents/tree/main/plugins/conductor> — a plugin rather than a
    bare skill, so it may carry agent definitions or commands that this stack deploys
    differently; Kasetto installs skill directories, not plugins.
  - <https://github.com/stellarlinkco/myclaude/tree/master/agents/requirements> — an agent
    definition, not a skill, and on `master` rather than `main`. Adjacency to check:
    `shared/design/design-forge`, which owns the requirements-document contract, and the deliberate
    decision recorded there NOT to use `references/authoring.md`'s atomic `FR-`/`NFR-` schema.
- **Pin third-party versions** — third-party sources currently track `main`. If a surprise
  upstream change is a concern, add `ref:` pins in `kasetto/base.yaml` and roll forward
  deliberately with `kst sync --update`.
- **`agent-stack` group review findings, 2026-08-27.** A skill-forge + skill-judge pass over
  all six skills in `shared/agent-stack/`. `agents-management` (111/120, A) and
  `system-prompts` (100/120, B) were fixed in the same session; everything below is
  **unfixed backlog** for the other four. Scores: `skill-judge` 98/120 B, `skill-forge`
  95/120 C, `find-skills` 93/120 C, `writing-great-skills` 92/120 C. ⚠️ D1/D5 are
  **provisional** for `skill-forge`, `find-skills` and `writing-great-skills` — their
  `references/` were not read, so those three totals are soft.
  - ~~**Licence compliance, and the only items here that are not style.** `skill-forge` and
    `skill-judge` both declare upstream adaptation in `ATTRIBUTIONS.md` and ship no
    `LICENSE.upstream`, which `skill-forge` itself requires of adapted skills.
    `skill-judge` inlines MIT text under "Upstream license (MIT)" that is **missing the
    copyright line**, so it is not a verbatim reproduction and satisfies neither
    `skill-forge`'s rule nor MIT's own notice requirement. Neither records a holder or a
    primary-source read date, which `skill-forge` also mandates. Verify each against
    `gh api repos/OWNER/REPO/license` and the LICENSE file itself, not `gh repo view`.~~
    **FIXED 2026-08-27.** Both now ship a byte-for-byte `LICENSE.upstream` fetched from
    the upstream `LICENSE` blob, and both `ATTRIBUTIONS.md` record the holder, the
    verification method and the read date. Verified via `gh api
    repos/OWNER/REPO/license` plus the blob itself: `sanyuan0704/sanyuan-skills` MIT
    `Copyright (c) 2025 sanyuan0704`; `softaworks/agent-toolkit` MIT `Copyright (c) 2026
    Leonardo Flores`. Neither upstream publishes a `NOTICE`, so no `NOTICE.upstream` was
    needed. `skill-judge`'s source commit was never recorded at adaptation time; it is
    now pinned to upstream HEAD `3027f20f` and **marked as an inference**, sound because
    that commit is dated 2026-03-05 and this skill landed here 2026-07-27.
  - **`skill-judge` depends on a skill no skill can invoke.** It tells the agent to consult
    `writing-great-skills` for vocabulary in three places, and names it in its description.
    `writing-great-skills` sets `disable-model-invocation: true`, and its own text states the
    consequence: only the user, typing its name, can invoke it. Resolve by inlining the few
    terms `skill-judge` needs, or by dropping the key — note the root `AGENTS.md` records
    that OpenCode ignores that key entirely, so behaviour already differs per agent.
  - **`skill-forge` ↔ `skill-judge` trigger collision — the same defect that got
    `prompt-optimizer` archived.** "improve this skill" fires both: `skill-forge`'s
    description claims "improve a skill" and the literal trigger `'improve skill'`,
    `skill-judge`'s claims "improving a SKILL.md" and "how do I make this skill better".
    Routing is one-way — `skill-judge` defers to `skill-forge` for authoring; `skill-forge`
    carries **no NOT clause at all** and names `skill-judge` only in its body, which loads
    after triggering. `skill-forge` also advertises "prompt engineering", which is
    `system-prompts`' whole subject. Add NOT clauses routing review/score → `skill-judge`
    and prompt work → `system-prompts`.
    **Recount correction, 2026-08-27:** the original entry called `skill-forge` "the only
    one of the six that lacks one". It is not. `grep -c "NOT for"` gives find-skills 1,
    system-prompts 1, agents-management 1, and **0 for `skill-forge`, `skill-judge` and
    `writing-great-skills`** — three of six. `skill-judge` routes in prose ("Complements
    skill-forge (authoring); this is the grading lane") but carries no NOT clause, so the
    routing gap is wider than the entry claimed.
  - **`skill-forge` breaks three of its own checklist items.** It mandates a "do NOT load"
    block twice and ships none across nine references. It forbids topic-label load triggers
    ("says what is inside; never when to pay for it") and uses them — "for keyword bombing
    and good/bad examples", "for proven workflow patterns and anti-patterns". And its
    documented `python3 scripts/quick_validate.py` does a bare `import yaml` with no probe
    or fallback, against its own rule that an absent dependency MUST degrade to a reported
    skip; the working invocation (`uv run --with pyyaml …`) exists only in this repo's root
    `AGENTS.md`, which the skill's readers do not have.
  - **`find-skills` carries three stale bindings and a dangling reference.**
    **Partly fixed 2026-08-27:** the `skill-review` → `skill-judge` pointer (`:31`) and the
    "deterministic" overstatement (`:76`) are done; the self-update section is held pending
    the remove-or-declare decision below. ~~It points at a
    sibling skill named `skill-review`, which does not exist — it is `skill-judge`.~~ Its
    self-update section names the repo as `agent-skills` (it is `agent-setup`), the path as
    `shared/find-skills/` (it is `shared/agent-stack/find-skills/`), and warns about being
    "overwritten on the next store update" — skillsmgr-era text; Kasetto has no store. That
    section is also an undeclared repo binding: either remove it or declare
    `metadata.scope: repo-local` and name the repository in the opening lines. ~~Separately,
    its L1 verification is called "deterministic" while the script correctly probes and
    skips — the same candidate passes with shellcheck present and reports `skip` without it.
    Reword to "deterministic given the tools present".~~ Confirmed against
    `scripts/verify_skill.sh`, which probes with `command -v` and calls `skip()` for the
    hidden-Unicode scan, the secret scan, shellcheck and semgrep independently. Reworded,
    and a line added telling the reader that a clean exit is not a clean candidate.
  - **`writing-great-skills` was never brought up to repo conventions**, which its own
    `ATTRIBUTIONS.md` half-discloses ("body and GLOSSARY.md preserved verbatim from
    upstream"): zero RFC 2119 keywords in 86 lines, no NEVER list, and `GLOSSARY.md` at 201
    lines exceeds `SKILL.md` + `ATTRIBUTIONS.md` combined — which `skill-forge` forbids.
    Decide deliberately: apply the conventions, or record in `ATTRIBUTIONS.md` that verbatim
    preservation is the point and exempts it. Today the exemption is implied, not stated.
  - **Two skills here give contradictory authoring advice, and neither acknowledges the
    other.** `writing-great-skills` argues that steering by prohibition backfires and a
    prohibition should be kept only as a hard guardrail; `skill-forge` §5.6 and
    `skill-judge`'s D3 both make an explicit NEVER list a scored requirement, capped at 3
    for "no anti-patterns". Both positions are defensible. The silence is not.
  - ~~**One defect shipped verbatim in two skills.** `skill-forge` and `skill-judge` both say
    a skill gave "four answers to a question the running tool answers once" — the example
    lists 81, 76 and 63, which is **three** claimed answers against 80 actual. Fix in both.~~
    **FIXED 2026-08-27, in `skill-forge` only — the entry above was wrong to say "in both".**
    `skill-judge:45` reads "81 in the title, 76 in **two notes**, and 63 by its own
    arithmetic": four instances of three distinct values, and internally coherent.
    `skill-forge:43` had condensed that to "as 81, 76 and 63", dropping the clause the
    count rested on. A one-file off-by-one, now repaired by restoring the instance detail.
    `skill-judge` was correct and was left untouched.
