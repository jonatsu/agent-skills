# Scoring portability under D8

Portability is a **hard cap on D8**, not a deduction. A skill is universal by nature: it runs
on machines nobody configured for it, long after it was written.

Cap D8 at **10** when the skill depends on an environmental fact it never verifies, and at
**5** when that dependency is silent — no probe, no fallback, no message.

## Read `metadata.scope` before forming an opinion

**Detection is not a judgement call.** Only `repo-local` earns the exemption for naming a
repository's runners and paths. Treat an absent key as `portable`: a skill carrying local
bindings without declaring repo-local scope is a portable skill with a defect, and the cap
applies at full strength.

NEVER infer repo-local intent from the bindings themselves. That reasoning excuses every
instance of the defect this cap exists to catch, and it is the excuse a well-written skill
makes most convincingly. A `repo-local` declaration that never names its repository is itself
a finding.

## Decide which kind of dependency it is

A skill that *uses* a tool incidentally MUST NOT assume it. A skill that *documents* a tool
obviously requires that tool, and demanding tool-agnosticism there is incoherent — do NOT cap
a skill for naming its own subject. Require instead that it states its degradation path: what
the agent does when the tool is absent.

A tool skill whose opening rule says "prefer these tools when available" and never names the
alternative has the same defect in a different place, and that IS capped.

**A tool-subject skill is exempt for its subject and for nothing else.** Cap it normally where
it assumes a SECOND tool, names a project-local runner, hardcodes a path, or binds to an
ecosystem that is not the thing it documents. A pytest skill may say `pytest -x`; the same
skill saying `just test`, or assuming a config directory, has the ordinary defect — and it is
easy to wave through, because the first binding was legitimate and the second looks like more
of the same.

## What to check

- Tool availability established by a `PATH` probe (`command -v <tool>`) and nothing else. An
  assumed tool is a defect even when the authoring machine has it.
- No project-local entry point named by a portable skill. `just check`, `npm run lint`,
  `make test`, `pre-commit run`, `./scripts/gate.sh` are ONE repository's contract, not a
  machine's — and `command -v just` passes while that repo's `check` recipe is still absent,
  so the probe reassures without testing anything. The repo's runner must be DISCOVERED at run
  time, in a stated detection order, with a reported skip when none is found.
- Absent tool degrades to a reported skip or a named alternative — never a crash, and never
  silent continuation that reads as a pass.
- No hardcoded install paths (`/usr/local/bin/x`, `~/.local/share/mise/...`,
  `/opt/homebrew/...`), no authoring-machine paths or usernames.
- Bundled files referenced relative to the skill directory, never `~/.claude/skills/<name>/…`,
  which breaks under `CLAUDE_CONFIG_DIR` and for project-scoped installs. Forward slashes
  only; a backslash path fails on Unix.
- Where several tools do the job, more than one is accepted. A single hardcoded tool rots when
  the ecosystem moves.

A skill that pins one tool by name is not wrong today and will be wrong later, which is
exactly the failure this cap exists to catch.

## Claims about observable behavior need provenance

A skill asserting how a tool behaves — result caps, silent truncation, which op resets a file
mode — is only as good as its last measurement, and it rots invisibly because nothing fails
when the tool updates.

Expect a version and a date on measured claims, and treat a package full of unstamped
empirical assertions as unverifiable rather than usable. Deduct where a reader has no way to
tell which claims to re-check after an upgrade.
