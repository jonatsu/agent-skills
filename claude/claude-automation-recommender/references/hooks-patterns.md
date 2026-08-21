# Hooks Recommendations

Hooks run commands in response to Claude Code events. Ideal for enforcement and
automation that must happen consistently.

**Contents**
- [The hook contract](#the-hook-contract) — read before writing any hook
- [Cost model](#cost-model)
- [Formatting and lint hooks](#formatting-and-lint-hooks)
- [Type-checking hooks](#type-checking-hooks)
- [Test runner hooks](#test-runner-hooks)
- [Protection hooks](#protection-hooks)
- [Notification hooks](#notification-hooks)
- [Detection → recommendation](#detection--recommendation)

**Note**: These are common patterns. Use web search for tools not listed here.

---

## The Hook Contract

A hook recommendation that omits this contract gets implemented wrong. Include
the relevant parts in any hook the report recommends.

**Placement.** User and project hooks go in `.claude/settings.json` (or
`settings.local.json`, or the user-level settings file) under a top-level
`hooks` key:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": "…" }]
      }
    ]
  }
}
```

Plugin hooks live in `hooks/hooks.json` and use a `{"description": …, "hooks":
{…}}` wrapper.

**Input.** Every command hook receives a JSON object on **stdin** — nothing is
passed as an argument. Common fields: `session_id`, `cwd`, `hook_event_name`.
For `PreToolUse`/`PostToolUse`: `tool_name`, `tool_input`, and (PostToolUse)
`tool_response`. The edited path is `.tool_input.file_path`, so every
file-scoped hook starts by extracting it:

```bash
file_path=$(jq -r '.tool_input.file_path // empty')
[ -n "$file_path" ] || exit 0
```

The `// empty` guard matters: a matcher that also catches `Bash` yields no
`file_path`, and an unguarded hook then runs against the literal string `null`.

**Output and exit codes.**

| Exit | Meaning |
|------|---------|
| `0` | Success; stdout shown in the transcript |
| `2` | Blocking error; **stderr is fed back to Claude** |
| other | Non-blocking error; execution continues |

`PreToolUse` may instead print JSON to stdout to decide explicitly:

```json
{ "hookSpecificOutput": { "permissionDecision": "deny" }, "systemMessage": "Why" }
```

`permissionDecision` is `allow`, `deny`, or `ask`.

**Matchers** filter by tool name, are case-sensitive, and accept regex:
`"Edit|Write"`, `"Bash"`, `"*"`, `"mcp__.*"`.

**Timeouts** default to 60s for command hooks, 30s for prompt hooks; set
`"timeout": <seconds>` per hook.

**Hooks load at session start.** Editing `settings.json` does not affect the
running session — Claude Code must be restarted. Say this whenever recommending
a hook. Use `/hooks` to inspect what is loaded and `claude --debug` to trace
execution.

**Hooks run in parallel** and cannot see each other's output. Design them
independently.

---

## Cost Model

Every `PostToolUse` hook adds latency to every matching edit. State the cost
when recommending one.

| Pattern | Typical cost per edit | Notes |
|---------|----------------------|-------|
| Format one file | 50-300 ms | Safe default |
| Lint one file | 100-500 ms | Safe default |
| Type-check whole project | **1-30 s** | `tsc --noEmit` and `mypy` have no cheap single-file mode; recommend only on small projects, or move to a `Stop` hook |
| Run one related test file | 0.5-5 s | Acceptable when the mapping is reliable |
| Run the full test suite | **Minutes** | NEVER recommend on `PostToolUse` |

Cheaper placements for expensive checks: a `Stop` hook (runs once when Claude
finishes) or the existing pre-commit framework.

---

## Formatting and Lint Hooks

### Prettier (JavaScript/TypeScript)

**Detect**: `.prettierrc`, `.prettierrc.json`, `prettier.config.js`

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path // empty' | { read -r f; [ -n \"$f\" ] && npx prettier --write --ignore-unknown \"$f\"; } || true",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

`--ignore-unknown` makes Prettier skip files it does not handle, so the hook can
match every edit without erroring on `.py` or `.rs`.

### ESLint (JavaScript/TypeScript)

**Detect**: `.eslintrc*`, `eslint.config.js`

Same shape, with `npx eslint --fix "$f"`. Guard the extension so the hook stays
quiet on non-JS files:

```bash
case "$f" in *.js|*.jsx|*.ts|*.tsx) npx eslint --fix "$f" ;; esac
```

### Ruff (Python)

**Detect**: `ruff.toml`, `.ruff.toml`, `[tool.ruff]` in `pyproject.toml`

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path // empty' | { read -r f; case \"$f\" in *.py) ruff format \"$f\" && ruff check --fix \"$f\" ;; esac; } || true",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Black / isort (Python)

**Detect**: `black` or `isort` in `pyproject.toml`, `setup.cfg`

Same shape: `black "$f" && isort "$f"` inside the `*.py` case.

### gofmt (Go)

**Detect**: `go.mod` — use `gofmt -w "$f"` inside a `*.go` case.

### rustfmt (Rust)

**Detect**: `Cargo.toml` — use `rustfmt "$f"` inside a `*.rs` case.

### Already have pre-commit?

If `.pre-commit-config.yaml`, Husky, or lefthook is configured, these hooks
duplicate checks that already run at commit time. Recommend a single
`Stop`-event `pre-commit run --files …` instead, or nothing at all.

---

## Type-Checking Hooks

**Detect**: `tsconfig.json`, `mypy.ini`, `pyrightconfig.json`

Whole-project type checks are expensive (see [Cost model](#cost-model)).
Recommend on the `Stop` event rather than per edit:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          { "type": "command", "command": "npx tsc --noEmit", "timeout": 120 }
        ]
      }
    ]
  }
}
```

Exit 2 with the errors on stderr to push them back to Claude for a fix; exit 0
to report without blocking.

---

## Test Runner Hooks

**Detect**: `jest.config.*`, `vitest.config.*`, `pytest.ini`, `tests/`

Only worth recommending when a source file maps predictably to a test file.
Jest and Vitest can do the mapping themselves:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path // empty' | { read -r f; case \"$f\" in *.ts|*.tsx|*.js|*.jsx) npx jest --bail --findRelatedTests \"$f\" --passWithNoTests ;; esac; }",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

For pytest, map `src/foo/bar.py` → `tests/foo/test_bar.py` and skip when the
file does not exist. NEVER recommend a bare `pytest` or `npm test`.

---

## Protection Hooks

Cheap (no subprocess beyond `jq`) and the highest-value category.

### Block edits to secrets and lock files

**Detect**: `.env*`, `credentials.json`, `secrets.yaml`, `*.lock`,
`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Cargo.lock`, `poetry.lock`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path // empty' | { read -r f; case \"$f\" in *.env|*.env.*|*credentials.json|*secrets.y*ml|*package-lock.json|*yarn.lock|*pnpm-lock.yaml|*Cargo.lock|*poetry.lock) echo \"Blocked: $f is protected. Change it through its tool or by hand.\" >&2; exit 2 ;; esac; }"
          }
        ]
      }
    ]
  }
}
```

Exit 2 blocks the tool call and shows the stderr message to Claude, which then
explains the block rather than retrying.

### Require confirmation instead of blocking

Swap the `exit 2` for a stdout JSON payload with
`"permissionDecision": "ask"` when the path should be editable with approval.

---

## Notification Hooks

Fire when Claude Code notifies the user. Matchers filter by notification type.

| Matcher | Triggers when |
|---------|---------------|
| `permission_prompt` | Claude needs permission for a tool |
| `idle_prompt` | Claude is waiting for input (60+ seconds) |
| `auth_success` | Authentication succeeds |
| `elicitation_dialog` | An MCP tool needs input |

Pick the command for the platform — the macOS-only examples that circulate for
this are silent no-ops on Linux:

| Platform | Sound | Desktop notification |
|----------|-------|---------------------|
| macOS | `afplay /System/Library/Sounds/Ping.aiff` | `osascript -e 'display notification "Claude is waiting" with title "Claude Code"'` |
| Linux | `paplay /usr/share/sounds/freedesktop/stereo/message.oga` | `notify-send "Claude Code" "Claude is waiting"` |
| WSL2 | `powershell.exe -c '[console]::beep(880,200)'` | `powershell.exe -c "New-BurntToastNotification -Text 'Claude Code'"` (needs BurntToast), or `notify-send` under WSLg |

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Waiting for input'"
          }
        ]
      }
    ]
  }
}
```

---

## Detection → Recommendation

| If you see | Recommend | Cost |
|------------|-----------|------|
| Prettier config | Format edited file on Edit/Write | Low |
| ESLint config | Lint-fix edited file on Edit/Write | Low |
| Ruff / Black config | Format edited Python file | Low |
| `go.mod` | gofmt on edited file | Low |
| `Cargo.toml` | rustfmt on edited file | Low |
| `tsconfig.json` | `tsc --noEmit` on **Stop**, not per edit | High |
| Test config with reliable mapping | Related tests on edited file | Medium |
| `.env` / secrets files | PreToolUse block | None |
| Lock files | PreToolUse block | None |
| `.pre-commit-config.yaml` | Nothing — already covered at commit time | — |
| Long unattended sessions | Notification hooks | None |
