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
- **Pin third-party versions** — third-party sources currently track `main`. If a surprise
  upstream change is a concern, add `ref:` pins in `kasetto/base.yaml` and roll forward
  deliberately with `kst sync --update`.
