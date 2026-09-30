---
name: debug-server-tools
description: "Run and troubleshoot the server that connects a debugger to an embedded target through a probe: OpenOCD (including Espressif's fork), pyOCD, probe-rs, and SEGGER J-Link GDB Server. Use when picking a tool for a probe and target, writing OpenOCD configs, starting a GDB server, flashing through one, reading RTT, handling multi-core targets, or when the server cannot connect or halt. Wiring and probe hardware belong to debug-hardware; GDB itself to gdb-debugging."
license: MIT
compatibility: Needs at least one of OpenOCD, pyOCD, probe-rs, or the SEGGER J-Link software installed, and a probe the host can see.
metadata:
  author: Joonas Onatsu
---

# Debug Server Tools

A debug server owns the probe and exposes the target to a debugger, usually as a GDB remote port. This skill picks
the server, starts it safely, proves the connection, and flashes through it within the permission tiers. The probe
must already be visible to the host and wired; `debug-hardware` covers that and defines the tiers. GDB commands
belong to `gdb-debugging`.

Current known, checked 2026-09-30: OpenOCD release 0.12.0 (January 2023; its master branch is far ahead), pyOCD
0.45.1, probe-rs 0.32.0, Espressif's `openocd-esp32` v0.12.0-esp32-20260831, SEGGER J-Link software 9.80. None was
exercised on hardware for this skill; confirm each option with the tool's `--help` before relying on it.

## 1. Choose the Tool

| Probe or target           | Tool                                                                                                             |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Pico probe or Debug Probe | OpenOCD, pyOCD, or probe-rs (CMSIS-DAP)                                                                          |
| J-Link                    | J-Link GDB Server for SEGGER's flash loaders and device support; OpenOCD, pyOCD, or probe-rs work at basic level |
| RP2350                    | OpenOCD master or a Raspberry Pi build (release 0.12.0 lacks it), or probe-rs                                    |
| ESP32 family              | `openocd-esp32` (ESP-IDF installs it), or probe-rs                                                               |
| Raspberry Pi 4            | OpenOCD `target/bcm2711.cfg`, or probe-rs over JTAG                                                              |
| Raspberry Pi 5            | J-Link GDB Server (`BCM2712_A76_n`), or probe-rs (`RaspberryPi5B`)                                               |
| A Rust project            | probe-rs, which also runs `defmt` logging                                                                        |

When the `dbgprobe` MCP server (`es617/dbgprobe-mcp-server`) is configured, it can drive a J-Link directly, with
RTT and SVD register decoding. It supports J-Link only; for a CMSIS-DAP probe, or any protocol its J-Link backend
does not cover, use the tools above. It does not gate flash or erase, so apply the tiers to its tools as to any
command.

Prefer the tool the project already configures: a checked-in `openocd.cfg`, `Embed.toml`, `.cargo/config.toml`
runner, or IDE launch file records a working setup.

Each tool needs its own udev rules on Linux; a probe that `lsusb` lists but the tool cannot open is missing them. The
tool references say which file to install.

## 2. Start the Server

- Run the server in the background with its output captured to a log, and read the log before connecting a client:
  the probe, target, and core lines there say whether it connected.
- Before starting, check that no earlier server still holds the probe or the port (`ss -ltnp`, `pgrep -a openocd`).
  A stale server is the usual cause of "address already in use" and of a probe that "cannot be found".
- Keep the server on localhost. OpenOCD and pyOCD listen on loopback by default; the J-Link GDB Server on Linux
  listens on every interface unless given `-LocalhostOnly 1`.
- Start at a low clock (1 MHz or less) until the connection is proven.

| Tool              | GDB port                      | Other ports                         |
| ----------------- | ----------------------------- | ----------------------------------- |
| OpenOCD           | 3333 (next core 3334, and on) | telnet 4444, Tcl 6666               |
| pyOCD             | 3333 (plus the core number)   | telnet 4444, probe server 5555      |
| probe-rs `gdb`    | `localhost:1337`              | none; RTT through `attach` or `run` |
| J-Link GDB Server | 2331                          | SWO 2332, telnet 2333, RTT 19021    |

## 3. Prove the Connection, Then Flash

Attach, halt, and read something known: the program counter, a core register, or the chip ID. Only then load code.

Flashing is in the task-agreement tier. Use the tool's own programmer or GDB's `load` through the server; both
erase the sectors they write, which is part of flashing. Anything that erases beyond the image, unlocks, recovers,
or writes option bytes is always-ask. These commands and options are in that tier:

- **OpenOCD:** `flash erase_sector`, `flash erase_address` (whole bank when length is 0, and `unlock` removes
  protection first), every `<driver> mass_erase`, `stm32f1x unlock` (mass-erases a locked part), `stm32f2x unlock`,
  `stm32l4x unlock`, `stm32l4x option_write`, and `nrf52_recover`, `nrf53_recover`, `nrf91_recover`.
- **pyOCD:** `pyocd erase --chip` and `--mass`, `-e chip` on `load` or `gdbserver`, and any connection to an nRF52
  or Kinetis part without `-O auto_unlock=false`, since pyOCD unlocks a locked part by mass-erasing it.
- **probe-rs:** `probe-rs erase`, which always erases all non-volatile memory, `--chip-erase`, and
  `--allow-erase-all`, which permits erasing protected memory and security keys.
- **J-Link:** Commander's `Erase`, the GDB Server's `monitor flash erase`, and the STM32 unlock dialog.
- **ESP32:** `program_esp` with `encrypt`, and anything that burns eFuses.

## 4. When the Server Cannot Connect or Halt

Work from the log's first error:

1. **No probe:** the host cannot see it (see `debug-hardware`), the udev rules are missing, or two probes are
   attached and none is selected (OpenOCD `adapter serial`, pyOCD `-u`, probe-rs `--probe`, J-Link `-USB`).
2. **No target:** power, wiring, or the wrong transport; OpenOCD needs `transport select swd` or `jtag` to match.
3. **Connects, then loses the target:** firmware disables the debug pins, sleeps, or resets in a loop. Connect under
   reset (OpenOCD `reset_config srst_only connect_assert_srst`, probe-rs `--connect-under-reset`, or the J-Link
   device name that enables it), or use the target's rescue path in `debug-hardware`'s target reference.
4. **Wrong target description:** a core name instead of the exact device, or an OpenOCD release older than the
   target file needs.
5. **Protected part:** stop and report the protection state; recovery is always-ask.

## 5. Tool References

Read the reference for the chosen tool before writing its commands:

- [references/openocd.md](references/openocd.md): configs, transports, multi-core RP2040 and RP2350, `program`,
  connect-under-reset, RTT, and Espressif's fork.
- [references/pyocd.md](references/pyocd.md): subcommands, packs, options, and RTT.
- [references/probe-rs.md](references/probe-rs.md): subcommands, chip names, `cargo embed`, and GDB.
- [references/jlink-gdb-server.md](references/jlink-gdb-server.md): options, monitor commands, RTT, SWO, and
  semihosting.

The work is done when the server's log shows the target connected, a debugger or the tool can halt it and read a
register, and any flashing stayed within its tier.
