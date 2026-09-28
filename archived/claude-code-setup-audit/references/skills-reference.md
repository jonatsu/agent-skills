# Skill Recommendations

Read this when recommending that the user create a skill. `SKILL.md` carries the signal-to-skill mapping; this
file carries the file format, the invocation-control decision, and the traps that make a recommended skill
fail silently.

Create project skills in `.claude/skills/<name>/SKILL.md`. A skill may be invoked by Claude automatically when
relevant, by the user with `/skill-name`, or both.

**Do not recommend a custom skill that an installed plugin already provides.** Enumerate what is available
rather than reciting a list from memory — plugin contents change independently of this file:

```bash
claude plugin list                 # installed plugins
claude plugin details <plugin>     # that plugin's skills, commands, agents, and token cost
```

See [plugins-reference.md](plugins-reference.md) for the install contract and for when a plugin beats a custom
skill.

## Structure

```text
.claude/skills/
└── my-skill/
    ├── SKILL.md           # instructions (required)
    ├── template.yaml      # a template the skill applies
    ├── scripts/
    │   └── validate.sh    # a script the skill runs
    └── examples/          # reference material
```

Add a bundled file only when it carries something `SKILL.md` cannot: a template consumed as output, a script
whose exact behavior matters, or branch detail that would bloat the shared instructions.

## Frontmatter

```yaml
---
name: skill-name
description: What this skill does and when to use it
disable-model-invocation: true  # only the user can invoke (for side effects)
user-invocable: false           # only Claude can invoke (background knowledge)
allowed-tools: Read, Grep, Glob # restrict tool access
context: fork                   # run in an isolated subagent
agent: Explore                  # which agent type when forked
---
```

A skill restricts tools with `allowed-tools`. An *agent* uses `tools`. The wrong key is silently ignored, so
a skill documented as read-only runs with full access.

### Invocation control

| Setting                          | User | Claude | Recommend for               |
| -------------------------------- | ---- | ------ | --------------------------- |
| (omit both)                      | ✓    | ✓      | general-purpose skills      |
| `disable-model-invocation: true` | ✓    | ✗      | side effects (deploy, send) |
| `user-invocable: false`          | ✗    | ✓      | background knowledge        |

Recommend `disable-model-invocation: true` only when the skill's action is genuinely irreversible or
outward-facing. The flag withholds the guidance at the moment it is needed without preventing the underlying
command, so it is a poor substitute for a confirmation gate written into the skill itself.

## Two Traps Worth Naming in a Recommendation

**Never reference a bundled file by an absolute or `~`-rooted path** such as `~/.claude/skills/<name>/...`. It
breaks wherever `CLAUDE_CONFIG_DIR` moves the config directory, and breaks outright for a project-scoped skill
under `.claude/skills/`. Relative paths resolve against the skill directory in both scopes.

**A bundled script must probe for its toolchain rather than assume it**, and must fail loudly when a check
fails. `npx prisma validate || echo "Validation failed"` always exits 0, so the validation step it advertises
can never fail — a shape worth flagging whenever a recommendation bundles a script.

## Worked Example

One example rather than a catalogue; the shape generalises, the specific skill does not.

```yaml
---
name: create-migration
description: Create a database migration file. Use when adding or altering a table.
disable-model-invocation: true
allowed-tools: Read, Write, Bash
---

Create a migration for: $ARGUMENTS

1. Generate a migration file in `migrations/` with a timestamp prefix
2. Include up and down functions
3. Run validation: `bash scripts/validate-migration.sh`
4. Report any issues found
```

```bash
#!/usr/bin/env bash
# scripts/validate-migration.sh
# Probe PATH rather than assuming the toolchain: a skill runs on machines you
# did not set up. Fail on a real validation failure; skip only when absent.
set -euo pipefail
if ! command -v npx > /dev/null 2>&1; then
  echo "skipped: npx not on PATH" >&2
  exit 0
fi
npx prisma validate
```

## Arguments

`$ARGUMENTS` expands to everything the user typed after the skill name: `/deploy staging prod` becomes
`staging prod`. If the body never mentions `$ARGUMENTS`, the input is appended as a trailing
`ARGUMENTS: <value>` line instead, so a skill that ignores the placeholder still receives the input.

Place `$ARGUMENTS` where the value belongs in the instruction — "Create a migration for: $ARGUMENTS" — rather
than restating it, and describe the expected shape in the `description` so the user knows what to pass.

## Dynamic Context Injection

A backtick-quoted command prefixed with `!` runs before the skill content reaches Claude, and its output
replaces the placeholder:

```yaml
## Current State
- Branch: !`git branch --show-current`
- Status: !`git status --short`
```

Recommend this instead of instructing Claude to gather the same state itself: it is one deterministic
substitution rather than a tool call the model may skip.
