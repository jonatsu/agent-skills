# probe-rs

Checked 2026-09-30 against probe-rs 0.32.0 (`probe-rs-tools` in <https://github.com/probe-rs/probe-rs>) and the
documentation at <https://probe.rs/docs/>. Install from the probe.rs installation page; one package provides
`probe-rs`, `cargo-embed`, and `cargo-flash`. `probe-rs <command> --help` is the reference.

## Setup on Linux

Install the udev rules from <https://probe.rs/files/69-probe-rs.rules> into `/etc/udev/rules.d/`, then run
`udevadm control --reload` and `udevadm trigger`. If access still fails, add the user to the `plugdev` group. On
WSL2, udev may not be running: start it with `[boot] command="service udev start"` in `/etc/wsl.conf`. Installing
rules and editing `/etc` need the user.

## Subcommands

- `probe-rs list`: attached probes. `probe-rs info`: the probe and the target it sees.
- `probe-rs chip list`: target names; pass the exact one with `--chip`.
- `probe-rs run --chip <chip> <elf>`: flash, run, and print RTT and `defmt` output. This is the usual Rust loop, often
  set as the cargo runner.
- `probe-rs download --chip <chip> <file>`: flash only; `--verify` checks it. `--chip-erase` erases the whole chip
  first (always-ask).
- `probe-rs attach --chip <chip> <elf>`: attach to a running target's RTT without flashing.
- `probe-rs gdb --chip <chip> <elf>`: a GDB server on `localhost:1337` by default, not 3333; change it with
  `--gdb-connection-string`. `--reset-halt` halts at reset.
- `probe-rs dap-server`: the Debug Adapter Protocol server for editors.
- `probe-rs erase --chip <chip>`: erases all non-volatile memory. It has no sector option; it is always-ask.
- `cargo embed` and `cargo flash`: the project-level front ends, configured by `Embed.toml`.

Common options: `--probe VID:PID[:serial]` selects a probe, `--protocol swd|jtag`, `--speed <kHz>`,
`--connect-under-reset`, and `--non-interactive`.

**`--allow-erase-all`** permits erasing all memory, "including security keys and 3rd party firmware", even under
read-only protection. It is always-ask, and so is the equivalent environment variable `PROBE_RS_ALLOW_ERASE_ALL`.

## Target Coverage

- RP2040 (`RP2040`) and RP2350 in two variants, `RP235x` for the Arm cores and `RP235x_riscv` for RISC-V.
- ESP32 family: the Xtensa ESP32, ESP32-S2, and ESP32-S3, and the RISC-V C2, C3, C5, C6, H2, and P4 among others.
- Cortex-A: `RaspberryPi4B` over JTAG only (`probe-rs gdb --protocol jtag --chip RaspberryPi4B`; state the protocol,
  since SWD is not supported there), and `RaspberryPi5B`, present in the target files but not otherwise documented.

## With a J-Link

probe-rs drives a J-Link over USB itself, so SEGGER's software is not needed on Linux beyond udev access. It is slower
than SEGGER's tools. On Windows it needs the probe switched to a WinUSB driver, which breaks SEGGER's own tools for that
probe until switched back; on WSL2 with `usbipd`, the Linux route avoids that.
