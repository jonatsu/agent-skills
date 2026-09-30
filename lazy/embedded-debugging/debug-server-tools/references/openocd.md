# OpenOCD

Checked 2026-09-30 against `doc/openocd.texi` and `tcl/` on OpenOCD master (commit `21f88d78`) and release 0.12.0.
Release 0.12.0 dates from January 2023; distribution packages often ship it, so check `openocd --version` and prefer a
recent build when a target file is missing.

## Contents

- Invocation
- Multi-core RP2040 and RP2350
- Flashing
- Connect under reset
- RTT
- Espressif's fork
- Error messages

## Invocation

An OpenOCD run combines an interface file, a target (or board) file, and commands. Order matters: a `-c` that sets
a variable must come before the `-f` that reads it.

```bash
openocd -f interface/cmsis-dap.cfg -c "transport select swd" -c "adapter speed 1000" \
  -f target/rp2040.cfg -l openocd.log
```

- Interfaces: `interface/cmsis-dap.cfg` (Pico probe, Debug Probe) and `interface/jlink.cfg`.
- `adapter speed <kHz>` sets the clock; 0 means RTCK on JTAG.
- `transport select swd` or `jtag` picks the transport when the adapter supports both.
- `adapter serial <string>` selects one probe of several; for a J-Link it also matches the nickname.
- Ports: GDB 3333 for the first target (plus one per further target), telnet 4444, Tcl 6666. OpenOCD listens on
  loopback by default; `bindto 0.0.0.0` widens it, so leave it unset.
- `-l <file>` writes the log; `-d3` raises its detail when diagnosing.
- Board files (`-f board/<name>.cfg`) bundle the interface and target for a known development board.

The telnet port accepts OpenOCD commands directly (`telnet localhost 4444`), and GDB reaches the same commands with
`monitor <command>`.

## Multi-Core RP2040 and RP2350

- **Release 0.12.0 `rp2040.cfg`:** two targets, `rp2040.core0` on port 3333 and `rp2040.core1` on 3334.
  `set USE_CORE 0` or `1` gives one core.
- **Master `rp2040.cfg`:** the default is `USE_CORE SMP`, both cores as one SMP target with `-rtos hwthread` on port
  3333, where GDB shows each core as a thread. `0` or `1` gives one core; another value gives isolated cores on
  separate ports. The flash driver changed from `rp2040_flash` to `rp2xxx`.
- **`rp2350.cfg` (master only):** `USE_CORE` is a list of `cm0`, `cm1` (Cortex-M33) or `rv0`, `rv1` (RISC-V), default
  `{ cm0 cm1 }` as one SMP group. It must match the architecture the chip booted; listing both kinds lets OpenOCD pick
  the running one. `RESCUE` and `SWD_MULTIDROP` variables also exist.
- **Rescue:** `-c "set RESCUE 1"` before the target file runs the rescue and exits; restart without it, then load code.

## Flashing

`program` initializes, runs `reset init`, writes, optionally verifies, and optionally resets and exits:

```bash
openocd -f interface/cmsis-dap.cfg -f target/rp2040.cfg -c "adapter speed 5000" \
  -c "program firmware.elf verify reset exit"
openocd -f board/stm32f3discovery.cfg -c "program firmware.bin exit 0x08000000"
```

A `.bin` needs its address; an ELF or HEX carries its own. `program` erases only the sectors it writes. From GDB,
`load` does the same, followed by `monitor reset halt` or `monitor reset init`.

Reset modes: `reset run` starts the target, `reset halt` halts it at the reset vector before any code runs, and
`reset init` halts and runs the target's init script (clocks, flash setup), which a flash write usually needs.

## Connect Under Reset

For a part whose firmware disables SWD, remaps the pins, or sleeps, hold reset while connecting:

```text
reset_config srst_only connect_assert_srst
```

It needs the reset line wired and `srst_nogate`, which the STM32F1 and F4 target files already set. OpenOCD's own
description names the use: "unable to connect to your target due to incorrect options byte config or illegal program
execution".

## RTT

```text
rtt setup <address> <size> "SEGGER RTT"
rtt start
rtt server start <port> <channel>
```

`rtt setup` names where to search for the control block: its start address, the search size, and the ID string, which
defaults to `SEGGER RTT`. `rtt start` searches, and `rtt server start` exposes a channel as raw TCP. Raspberry Pi's
example for an RP2040: `rtt setup 0x20000000 2048 "SEGGER RTT"`, `rtt start`, `rtt server start 60000 0`, then
`nc localhost 60000`. `rtt channels` lists what the target offers.

## Espressif's Fork

ESP32 parts need `openocd-esp32` (<https://github.com/espressif/openocd-esp32>), which ESP-IDF installs; upstream
OpenOCD lacks the Xtensa and ESP-specific support. Take the project's exact arguments from
`debug_arguments_openocd` in `build/project_description.json`. For chips with the built-in USB-Serial-JTAG, the
fork's `board/esp32c3-builtin.cfg` and similar files select it; install the fork's `contrib/60-openocd.rules` for
access. The fork adds `program_esp <image> <offset> [verify] [reset] [exit]` and
`program_esp_bins <build_dir> <json_file> [verify] [reset] [exit]`; an `encrypt` argument writes encrypted flash,
which is always-ask.

## Error Messages

Read the first error, not the last:

- `Error: unable to find a matching CMSIS-DAP device` or `No J-Link device found`, or a `LIBUSB_ERROR_*`: the probe
  is not visible, is held by another process, or lacks a udev rule.
- `JTAG scan chain interrogation failed`, `Error connecting DP`, or `cannot read IDR`: wiring, power, speed, or the
  wrong transport; lower the speed first.
- `Error: couldn't bind ... to socket: Address already in use`: an earlier server still runs.
- `Can't find target/<name>.cfg`: this OpenOCD build predates the target file.
