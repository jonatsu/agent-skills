# The Serial MCP Server

`jonatsu/serial-mcp-server` is a fork of `es617/serial-mcp-server` that adds write pacing, port logs, file sending,
and scripts. Current known: release `v0.2.4`, checked 2026-10-29 against its source. The command is `serial_mcp`.
Install it with `pip install git+https://github.com/jonatsu/serial-mcp-server.git`; `pip install serial-mcp-server`
installs upstream, which lacks these features.

## Adding It to One Project

The server is added per project, never to the user's global configuration. Add it where the project needs it,
tell the user, and start a new session so the harness loads it. Each harness asks for approval or trust before
running a project's server.

Set `SERIAL_MCP_TOOL_SEPARATOR=_`. The server's tool names contain dots by default (`serial.open`), which Claude's and
OpenAI's tool-name rules reject; with `_` they become `serial_open` and so on.

**Claude Code and Copilot CLI** both read `.mcp.json` at the repository root:

```json
{
  "mcpServers": {
    "serial": {
      "type": "stdio",
      "command": "serial_mcp",
      "args": [],
      "env": { "SERIAL_MCP_TOOL_SEPARATOR": "_" }
    }
  }
}
```

- Claude Code prompts for approval before using a project server; until then `claude mcp list` shows it as pending.
  `claude mcp add --scope project serial -- serial_mcp` writes the same file.
- Copilot CLI loads it only after the user trusts the folder, and reads `.github/mcp.json` too; `.mcp.json` wins when
  both exist. Its documentation's example adds `"tools": ["*"]`; add that field if Copilot does not list the tools.
  `copilot mcp add` writes the user's global file, so edit `.mcp.json` by hand instead.

**Codex** reads `.codex/config.toml` in the project, for trusted projects only:

```toml
[mcp_servers.serial]
command = "serial_mcp"
env = { SERIAL_MCP_TOOL_SEPARATOR = "_" }
```

`codex mcp add` writes the user's global `~/.codex/config.toml`; check `codex mcp add --help` before using it, and
edit the project file by hand otherwise.

Whether these files belong in the project's version control is the user's call; a personal debugging aid may belong in
the project's ignore file instead.

## Tools

Names are shown with the default dot; with the separator set, they use `_`. The server keeps its files in one data
directory, `.serial_mcp/` by default (`SERIAL_MCP_SPEC_ROOT` moves it), found upwards from the working directory or
beside the nearest `.git/`. Keep its `logs/` and `traces/` subdirectories out of version control: they hold device
output, including any password typed into a console.

- `serial.list_ports`, `serial.connection_status`, `serial.connections.list`: read-only.
- `serial.open`: opens a port and returns a `connection_id`. Defaults are 115200 baud, 8N1, and `\r\n` line endings;
  `baudrate`, `bytesize`, `parity`, `stopbits`, `encoding`, `newline`, and `exclusive` override them. Opening can assert
  DTR and RTS and reset the target.
- `serial.configure`: changes pacing, encoding, or newline on an open connection. Use it instead of reopening, which
  can reset the target.
- `serial.read`, `serial.readline`, `serial.read_until` (with a `delimiter` and `timeout_ms`): read from the
  connection's buffer. Reading consumes the buffer, so the server marks these destructive. Keep `max_bytes` near
  its default of 4096: a large read across a full boot overflows the tool result. The buffer holds 1 MiB and drops
  the oldest unread bytes beyond that; `serial.connection_status` reports them as `dropped_bytes`.
- `serial.write`: sends `data`, with `append_newline` and per-call pacing.
- `serial.send_file`: sends a file of at most 1 MiB from `SERIAL_MCP_FILES_DIR`, by default `.serial_mcp/files/`, with
  the connection's pacing. It refuses any path outside that directory. Use it for long input, such as a U-Boot
  environment.
- `serial.flush`, `serial.set_dtr`, `serial.set_rts`, `serial.pulse_dtr`, `serial.pulse_rts`: buffer and control
  lines; the pulse tools reset many boards.
- `serial.close`: releases the port for other tools.
- `serial.log.start`, `serial.log.stop`, `serial.log.status`, `serial.log.mark`: record the connection's traffic to
  files under `SERIAL_MCP_LOG_DIR`, by default `.serial_mcp/logs/`. `log: true` on `serial.open` starts one at open,
  and `SERIAL_MCP_LOG=1` logs every connection. The start call returns the file paths, so search those files for a
  long capture. The server never deletes log files.
- `serial.script.run`, `serial.script.status`, `serial.script.cancel`, `serial.script.list`,
  `serial.script.template`: run a checked send-and-expect script, described below.
- `serial.trace.status`, `serial.trace.tail`: the call trace, on by default (`SERIAL_MCP_TRACE=0` disables it;
  `SERIAL_MCP_TRACE_PAYLOADS=1` records data too).
- `serial.spec.*` and `serial.plugin.*`: protocol descriptions and device plugins, for structured protocols.

## Pacing Slow Targets

A target without receive buffering, such as a bootloader shell or a small MCU, drops characters written at full
speed. Pace the writes for the whole connection on `serial.open` or `serial.configure`, or for one `serial.write`:

- `inter_char_delay_ms` (0 to 1000): a delay after each character.
- `chunk_size` with `chunk_delay_ms` (up to 1000): write in chunks, with a delay between them.

The two modes are exclusive, and per-write options replace the connection's whole pacing setting. A paced write
estimated to take longer than `SERIAL_MCP_MAX_WRITE_SECONDS`, 60 by default, is rejected before any byte is sent.

## Scripts for Repeatable Sequences

A script is a text file of lines to send and `@expect` patterns to wait for, with directives such as `@prompt`,
`@fail_on`, `@timeout`, and `@send_file`. Prefer one for a sequence that must run the same way each time, such as a
boot smoke test. The server checks the whole script before sending anything. A run starts a port log by default and
writes a result file. While it runs, it blocks writes, control lines, and flushes on its connection, but reads stay
available. Script files live in `SERIAL_MCP_SCRIPTS_DIR`, by default `.serial_mcp/scripts/`; `serial.script.template`
returns a starting point. `serial_mcp_script` runs a script without an agent, for example in CI, and exits `0` on
pass and `1` on fail.

## Watching Alongside

`SERIAL_MCP_MIRROR=ro` or `rw` in the server's environment exposes each connection through a pseudo-terminal linked at
a numbered path: `/tmp/serial-mcp0` for the first, or the same numbering on the base `SERIAL_MCP_MIRROR_LINK` sets.
`serial.open` returns the link. The user opens it with `tio` or `picocom` to watch, or to type with `rw`, while the
agent drives the real port. The mirror does not work on Windows.
