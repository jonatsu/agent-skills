# Attributions

This skill is original work. Nothing here is copied, adapted, or translated from another project, and
`metadata.license` is the repository default (MIT). This file is a courtesy ledger, not a licence obligation.

## Idea sources

- [fugazi/test-automation-skills-agents](https://github.com/fugazi/test-automation-skills-agents) (MIT),
  `references/testing-anti-patterns.md`, read 2026-08-24 at `HEAD`. Reading it prompted five additions, each
  written from scratch and generalized well past that file's Playwright and Selenium framing: testing
  framework code rather than your own (`SKILL.md`); and, in `references/test-strategy.md`, that a status code
  is not an oracle, that synchronization belongs on the condition rather than the clock, that tests should
  bind to the contract rather than the incidental representation, and that a suite must run where it will be
  judged. No code, prose, identifiers, or examples were carried over.

  The same repository's `skills/qa-manual-istqb/`, read 2026-08-25 at `HEAD`, prompted one further addition:
  the exploratory-charter shape in `references/test-strategy.md`, which makes the level table's "Manual or
  exploratory" row actionable. Upstream ships a charter as a fill-in template; the version here is a
  written-from-scratch four-line form plus the rule that a charter reports notes and NEVER a verdict. Its
  ISTQB estimation, monitoring-metrics, entry/exit-criteria and traceability-matrix material was evaluated and
  deliberately rejected as process machinery this lane does not want. Again, no text travelled.

- [sarathsomana/tech-skills](https://github.com/sarathsomana/tech-skills) (MIT), `skills/test-engineer/`, read
  2026-08-24 at rev `3595ee02`. Prompted two rules, both rewritten from the idea: that exit status rather than
  parsed output settles pass/fail, and that a bounded retry loop must escalate with what it tried. Its own
  architecture, personas and artifact schema were not adopted, and its per-layer coverage targets are rejected
  here as an anti-pattern.

- [0King0P/Claude-Skills](https://github.com/0King0P/Claude-Skills) `test-engineer/SKILL.md` and
  [grasberg/sofia-workspace](https://github.com/grasberg/sofia-workspace) `skills/test-engineer/SKILL.md`,
  both read 2026-08-24. **Neither repository carries a licence** (verified: `/license` returns 404 and the
  `license` field is null on both), so both are all-rights-reserved and nothing was copied from either in any
  form. Reading them prompted two additions written entirely from scratch: mutation testing as the measure of
  what a suite would catch, and the tautological-assertion anti-pattern. Ideas are not protectable; text is,
  and none travelled.

- [kui04/nix-config](https://github.com/kui04/nix-config) `users/.config/pi/skills/test-engineer/`, read
  2026-08-24 at rev `e8e53963`. **Also carries no licence** (same verification), so again nothing was copied.
  Reading it prompted the stale-expectation triage rule, the framework-identification gate, and the test-size
  axis. For the last of these the underlying source is *Software Engineering at Google* ch. 11, cited directly
  in `references/test-strategy.md` in preference to this repository.
