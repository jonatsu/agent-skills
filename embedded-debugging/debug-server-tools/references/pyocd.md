# pyOCD

Checked 2026-09-30 against pyOCD 0.45.1 (`pyocd/subcommands/` and `docs/` in <https://github.com/pyocd/pyOCD>).
Install with `pipx install pyocd` or into the project's environment; `pyocd --help` and `pyocd <command> --help` are
the reference.

## Safety First

pyOCD connects with two defaults that act at the always-ask tier:

- `auto_unlock` is true: connecting to a locked nRF52 or NXP Kinetis part mass-erases it to gain access. Pass
  `-O auto_unlock=false` whenever the part's protection state is unknown. Only `-O auto_unlock` appears in pyOCD's
  own security page, so confirm the `=false` form with `pyocd gdbserver --help` or `docs/options.md` on first use.
- `jlink.power` is true: with a J-Link, pyOCD switches the probe's target power on while connected.

## Subcommands

- `pyocd list --probes`, `--targets`, or `--boards`: what is attached, and which target names pyOCD knows. A target
  missing from the list needs a CMSIS-Pack.
- `pyocd pack --find <glob>`, `pyocd pack --install <glob>`, `pyocd pack --update`: manage CMSIS-Packs for target
  support; `--pack <path>` uses one pack for a single run.
- `pyocd gdbserver -t <target>`: the GDB server. Port 3333 for the first core, plus the core number for the others
  (`--core` selects cores); telnet 4444 for semihosting; `--persist` keeps it running after GDB disconnects;
  `-S` enables semihosting. It serves localhost only unless `--allow-remote` is passed.
- `pyocd load -t <target> <file>`: flash a binary, HEX, or ELF image; `-a <address>` for a binary. `-e` chooses the
  erase: `sector` (the default, only what the image covers), `chip`, or `auto`.
- `pyocd erase -t <target>` with exactly one of `--sector <ranges>`, `--chip`, or `--mass`. On some devices mass and
  chip erase differ. All three are always-ask.
- `pyocd reset`, `pyocd run`, and `pyocd commander` (an interactive console for memory, registers, and flash).
- `pyocd rtt -t <target>`: an RTT viewer and logger, with `-a`/`-s` for the control-block search range and
  `-d <file>` to log.

Select one of several probes with `-u <unique-id>`; serial numbers omit leading zeros. Pass `-t <target>` always:
some probes, including J-Link on-board, report no target.

## With a J-Link

pyOCD drives a J-Link through SEGGER's library, so the J-Link software must be installed. Set `jlink.device` to the
exact device name for SEGGER's device handling; unset, the probe is used for low-level access only. Programming is
slower than with SEGGER's tools.
