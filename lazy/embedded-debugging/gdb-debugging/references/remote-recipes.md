# Remote Recipes per Debug Server

Two terminals, or the server in the background with a log: the server owns the probe, GDB connects to its port.
Starting and troubleshooting the servers belongs to `debug-server-tools`; these are the GDB halves. `load` is in the
flash tier.

## OpenOCD

```text
target extended-remote localhost:3333
monitor reset halt
load
monitor reset init
continue
```

`monitor reset init` runs the target's init script (clocks, flash setup) as well as halting. The telnet port
(4444) takes the same commands without GDB.

## pyOCD

```text
target extended-remote localhost:3333
monitor reset halt
load
continue
```

pyOCD gives each further core the next port (3334 for core 1).

## probe-rs

```text
target extended-remote localhost:1337
```

Start the server with `probe-rs gdb --chip <chip> <elf>` (add `--reset-halt` to stop at reset). For Rust,
`probe-rs run` usually replaces the GDB session: it flashes, runs, and prints `defmt` and RTT output.

## J-Link GDB Server

```text
target extended-remote localhost:2331
monitor reset
load
continue
```

The J-Link's `monitor reset` resets and halts. RTT stays readable on port 19021 during the session.

## Multi-Core Targets

- **OpenOCD master with SMP** (the default for `rp2040.cfg` and `rp2350.cfg`): one port, 3333, with each core as a
  thread. `info threads` lists the cores and `thread <n>` switches.
- **Separate ports** (OpenOCD 0.12.0's `rp2040.cfg`, OpenOCD with `USE_CORE` set to isolate cores, and pyOCD): one GDB
  per core, on 3333, 3334, and so on.
- `set scheduler-locking on` keeps other threads, and on an SMP target other cores, from running while you step. The
  default is `replay`, which behaves as `off` outside record and replay.

## RTOS Awareness

With an RTOS, the debug server can present each task as a GDB thread. OpenOCD enables it with `-rtos <name>` on the
target, such as `-rtos FreeRTOS` or `-rtos Zephyr`, or `-rtos auto`; the firmware must keep the symbols the server
looks for. RTOS-specific setup belongs to `mcu-firmware-debugging`.
