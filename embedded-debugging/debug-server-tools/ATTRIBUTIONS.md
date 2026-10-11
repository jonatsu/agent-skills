# Attributions

- Author: Joonas Onatsu
- License: `MIT`

The package adapts material from low-level-dev-skills, whose MIT license requires its notice to travel with the
material; keep `LICENSE.upstream` with the skill.

## First-party Sources

### The OpenOCD developers: OpenOCD

- Source: <https://github.com/openocd-org/openocd>, `doc/openocd.texi` and `tcl/`
- License: `GPL-2.0-or-later AND GFDL-1.2-or-later`
- Version: master at `21f88d7815edfb7632548090934c51017604f450`, cross-checked against `v0.12.0`

The OpenOCD guidance in `references/openocd.md` is built on the manual and the shipped configuration scripts: ports and
binding, adapter and transport selection, multi-core targets, flashing, connect-under-reset, RTT, and error messages.
Facts are restated in original words; no text or script is copied.

### The pyOCD developers: pyOCD

- Source: <https://github.com/pyocd/pyOCD>, `pyocd/subcommands/` and `docs/`
- License: `Apache-2.0`
- Version: `v0.45.1`

The pyOCD guidance in `references/pyocd.md` is built on the subcommand implementations and documentation. Nothing was
copied.

### The probe-rs developers: probe-rs

- Source: <https://github.com/probe-rs/probe-rs>, `probe-rs-tools/`
- License: `MIT OR Apache-2.0`
- Version: `v0.32.0`

The probe-rs guidance in `references/probe-rs.md` is built on the command-line tools' source: Linux setup, subcommands,
and target coverage. Nothing was copied.

### Espressif: openocd-esp32

- Source: <https://github.com/espressif/openocd-esp32>, including `contrib/60-openocd.rules`
- License: `GPL-2.0-or-later`
- Version: `v0.12.0-esp32-20260831`

The fork's board configs and udev rules supplied the Espressif section of `references/openocd.md`. Nothing was copied.

### SEGGER: J-Link GDB Server

- Source: <https://kb.segger.com/J-Link_GDB_Server>
- License: `LicenseRef-Proprietary`
- Version: J-Link software 9.80

The knowledge-base page states no open license, so all rights remain with SEGGER. It supplied the startup options,
monitor commands, and RTT and SWO behavior that `references/jlink-gdb-server.md` restates. Nothing was copied.

## Third-party Sources

### mohitmishra786: low-level-dev-skills

- Source: <https://github.com/mohitmishra786/low-level-dev-skills>, `skills/embedded/openocd-jtag/`
- License: `MIT`
- Version: `bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608`

Adapted into `references/openocd.md`: the script-mode `program ... verify reset exit` pattern, the distinction between
`reset run`, `reset halt`, and `reset init`, and the shape of an error-message section.
