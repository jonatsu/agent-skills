# The Serial MCP Server

`jonatsu/serial-mcp-server` is a fork of `es617/serial-mcp-server` that adds write pacing for slow targets. Current
known: fork commit `bceb725` (version `0.1.4.dev3`), checked 2026-09-30 against its installed source. The command is
`serial_mcp`. `pip install serial-mcp-server` installs upstream, without the pacing.

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

Names are shown with the default dot; with the separator set, they use `_`.

- `serial.list_ports`, `serial.connection_status`, `serial.connections.list`: read-only.
- `serial.open`: opens a port and returns a `connection_id`. Defaults are 115200 baud, 8N1, and `\r\n` line endings;
  `baudrate`, `bytesize`, `parity`, `stopbits`, `encoding`, `newline`, and `exclusive` override them. Opening can assert
  DTR and RTS and reset the target.
- `serial.read`, `serial.readline`, `serial.read_until` (with a `delimiter` and `timeout_ms`): read from the
  connection's buffer. Reading consumes the buffer, so the server marks these destructive.
- `serial.write`: sends `data`, with `append_newline` and per-call pacing.
- `serial.flush`, `serial.set_dtr`, `serial.set_rts`, `serial.pulse_dtr`, `serial.pulse_rts`: buffer and control
  lines; the pulse tools reset many boards.
- `serial.close`: releases the port for other tools.
- `serial.trace.status`, `serial.trace.tail`: the call trace, on by default (`SERIAL_MCP_TRACE=0` disables it;
  `SERIAL_MCP_TRACE_PAYLOADS=1` records data too).
- `serial.spec.*` and `serial.plugin.*`: protocol descriptions and device plugins, for structured protocols.

## Pacing Slow Targets

A target without receive buffering, such as a bootloader shell or a small MCU, drops characters written at full
speed. Pace the writes, either for the whole connection on `serial.open` or for one `serial.write`:

- `inter_char_delay_ms` (0 to 1000): a delay after each character.
- `chunk_size` with `chunk_delay_ms`: write in chunks, with a delay between them.

The two modes are exclusive, and per-write options replace the connection's whole pacing setting.

## Watching Alongside

`SERIAL_MCP_MIRROR=ro` or `rw` in the server's environment exposes the port through a pseudo-terminal linked at
`/tmp/serial-mcp`, or at `SERIAL_MCP_MIRROR_LINK`. The user opens that link with `tio` or `picocom` to watch, or to
type with `rw`, while the agent drives the real port.
