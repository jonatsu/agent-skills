# Skills — future work

Open items for the skills stack. Split out of `skills/README.md` on 2026-08-21 so the
README describes how the stack works and this file tracks what is still owed. Paths are
relative to `skills/` unless noted.

- **`opencode/headroom-management`** — currently OpenCode-only; generalize it to work with
  Claude Code too, then move to `shared/`.
- **`claude/reflect`** — the OpenCode `--sessions` session-archaeology feature could be
  ported/generalized if wanted.
- **Quality-refresh pass** — triaged `skill-review` audit of pre-`skill-forge` skills (e.g.
  the `grilling` stub); report-first. Can co-review with a second model via
  OpenCode — see [../docs/skill-co-review.md](../docs/skill-co-review.md).
- **`claude-md-management` plugin** — reviewed and recommended for removal rather than a
  fork: its rubric awards 35 of 100 points for things it never reads the codebase to
  check, and its discovery searches for two filenames that do not exist. Everything it
  does is already covered by `claude/reflect` and `shared/system-prompts`. The evidence
  for each defect is in `claude/claude-md-auditor/ATTRIBUTIONS.md`.
- **Pin third-party versions** — third-party sources currently track `main`. If a surprise
  upstream change is a concern, add `ref:` pins in `kasetto/base.yaml` and roll forward
  deliberately with `kst sync --update`.
