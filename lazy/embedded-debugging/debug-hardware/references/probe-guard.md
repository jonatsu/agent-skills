# The Probe Guard Hook

`scripts/probe_guard.py`, in this skill's directory, is a pre-tool-use hook that makes the "always ask" tier
enforced rather than remembered. It reads each shell command an agent is about to run and stops erase, unlock,
recover, protection, option-byte, and fuse operations until the user approves. Plain flashing and every read, halt,
and reset pass. It needs only `python3`.

## When to Install It

Install it in a repository the first time hardware work starts there and the repository lacks it: look for
`.agents/hooks/probe_guard.py`. It belongs to that project, never to the user's global configuration. Tell the user
what you are adding, and ask whether they want the files committed or kept out of version control; a personal
setup may belong in the project's ignore file or in `.claude/settings.local.json`.

1. Copy `scripts/probe_guard.py` from this skill's directory to `.agents/hooks/probe_guard.py` in the project, so the
   project keeps working when the skill moves or changes.
2. Register it for each harness the project uses, as below. Merge into an existing file rather than replacing it.
3. Tell the user to start a new session, and to approve or trust the hook where the harness asks.
4. Check it by piping a sample payload to the script, as "Testing It" shows; nothing touches the hardware.

## Claude Code

`.claude/settings.json`, or `.claude/settings.local.json` for a setup kept out of version control. The hook runs
after the user accepts the workspace trust dialog, alongside the user's own hooks; the strictest answer wins.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"${CLAUDE_PROJECT_DIR}/.agents/hooks/probe_guard.py\" --harness claude"
          }
        ]
      }
    ]
  }
}
```

The hook answers `ask`, so Claude Code shows its approval prompt with the reason.

## Copilot CLI

`.github/hooks/probe-guard.json`. Copilot CLI loads project hooks from `.github/hooks/` at the git root, in addition
to the user's, and resolves `cwd` from the repository root.

```json
{
  "version": 1,
  "hooks": {
    "preToolUse": [
      {
        "type": "command",
        "bash": "python3 .agents/hooks/probe_guard.py --harness copilot",
        "cwd": ".",
        "timeoutSec": 30,
        "matcher": "bash"
      }
    ]
  }
}
```

The hook answers `ask`, which the CLI turns into an approval prompt. Copilot's cloud agent treats `ask` as deny.

## Codex

`.codex/hooks.json`. Codex loads it only for a trusted project, and runs each project hook only after the user
reviews and trusts it in `/hooks`; editing the hook later needs that approval again.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$(git rev-parse --show-toplevel)/.agents/hooks/probe_guard.py\" --harness codex",
            "statusMessage": "Checking for destructive probe commands"
          }
        ]
      }
    ]
  }
}
```

Codex hooks cannot ask: Codex rejects an `ask` answer and runs the command anyway. The guard therefore denies, and its
reason tells the agent to hand the user the command. The user runs it in their own terminal.

## What It Guards

| Tool                                 | Stopped                                                                         |
| ------------------------------------ | ------------------------------------------------------------------------------- |
| `openocd`                            | Any argument naming erase, lock or unlock, protect, `option_write`, or recover  |
| `pyocd`                              | `erase`, `-e chip` or `--erase=chip`, and `auto_unlock=true`                    |
| `probe-rs`, `cargo embed` or `flash` | `probe-rs erase`, `--allow-erase-all`, and `--chip-erase`                       |
| `JLinkExe`                           | Any `-CommandFile`, because the guard cannot read the file                      |
| GDB (`gdb`, `*-gdb`, `gdb-*`)        | A `monitor` command that erases, locks, unlocks, or recovers                    |
| `nrfjprog`, `nrfutil`                | Erase-all, page and UICR erase, `--chiperase`, recover, and `ERASE_ALL` options |
| `esptool`, `espefuse`, `idf.py`      | `erase_flash`, `erase_region`, `--erase-all`, and every eFuse burn or protect   |
| `STM32_Programmer_CLI`, `st-flash`   | Erase and option-byte writes; `st-flash erase`                                  |

OpenOCD's `flash write_image erase` passes, since it erases only what it rewrites. The guard looks through `sudo`,
`env`, `timeout`, `uvx`, `uv run`, `python -m`, variable assignments, command chains, and one level of `sh -c`.

## What It Cannot See

It reads command text, so it is best effort. These pass unseen, and the permission tiers in `SKILL.md` still apply to
them:

- an operation inside a shell script, a `just` or `make` recipe, an OpenOCD `.cfg` file, or a GDB `-x` script;
- a tool reached through an alias or a renamed binary;
- probe power switched on through a tool's configuration, such as pyOCD's `jlink.power` default;
- MCP tools. The `dbgprobe` server's `erase` does a full chip erase and unlocks secured parts, and its `flash`,
  `mem.write`, and `svd.write` change the target. Where a project configures it, add a Claude Code `permissions.ask`
  entry for each of those tools, such as `"mcp__dbgprobe__<tool>"`, taking the exact names from the tool list the
  client shows.

## Testing It

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"pyocd erase --chip"}}' \
  | python3 .agents/hooks/probe_guard.py --harness claude
```

The command should print an `ask` answer naming `pyocd`. A harmless command such as `pyocd list` prints nothing.
