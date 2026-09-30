# Kernel Debugging

Checked 2026-09-30 against Linux v7.2's `Documentation/` and `scripts/`, and OpenOCD master. Paths below are in the
kernel tree; older kernels keep the debugging guides under `Documentation/dev-tools/` instead of
`Documentation/process/debugging/`.

## Contents

- Build options
- Decoding an oops or panic
- Crash dumps
- Getting output when nothing prints
- kgdb and kdb
- JTAG on the application cores
- GDB helper scripts

## Build Options

- Debug info: `CONFIG_DEBUG_INFO` is no longer set directly. Select it through the "Debug information" choice:
  `CONFIG_DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT`, `CONFIG_DEBUG_INFO_DWARF4`, or `CONFIG_DEBUG_INFO_DWARF5`, which needs
  `CONFIG_DEBUG_KERNEL`. A config fragment that says only `CONFIG_DEBUG_INFO=y` sets a symbol with no prompt.
- Leave `CONFIG_DEBUG_INFO_REDUCED` off for the GDB scripts, and keep `CONFIG_FRAME_POINTER` where the architecture
  supports it.
- `nokaslr` on the command line, or `CONFIG_RANDOMIZE_BASE=n`, keeps `vmlinux` addresses valid for any GDB stub:
  kgdb, JTAG, or QEMU.

## Decoding an Oops or Panic

Preserve the oops text, the kernel's build identity, the loaded modules, and any dump before a reboot or cleanup.
Decode against the kernel that crashed, never the analysis host's `uname -r` or a different build: an unrelated
symbol file produces plausible noise.

```bash
export CROSS_COMPILE=aarch64-linux-gnu-     # the target's tool prefix, or the host's addr2line is used
./scripts/decode_stacktrace.sh vmlinux <source-base-path> <modules-path> < oops.txt
./scripts/faddr2line vmlinux meminfo_proc_show+0x5/0x568
```

- `decode_stacktrace.sh` reads the oops on standard input; `-r <release>` finds `vmlinux` in the usual install
  locations instead, and `LLVM=1` selects the LLVM tools.
- `faddr2line` takes `function+offset/size`, which survives KASLR; the `/size` disambiguates duplicate symbol names.
  It prints inlined frames as `(inlined by)` chains.
- Plain `addr2line -e vmlinux <address>` works only on absolute addresses, so only with KASLR off or its offset
  subtracted.
- A module's frame decodes against its `.ko`; `objdump -dS <module>.ko` shows the code around a function.

Command-line settings that change what a crash does:

| Parameter               | Effect                                                                              |
| ----------------------- | ----------------------------------------------------------------------------------- |
| `panic=<seconds>`       | Reboot after a panic: 0 waits forever, negative reboots at once                     |
| `oops=panic`            | Turn every oops into a panic; with `panic=`, a reboot                               |
| `panic_on_warn=1`       | Panic on `WARN()`, useful to trigger a dump at the warning                          |
| `print-fatal-signals=1` | Log fatal signals that kill userspace processes                                     |
| `ignore_loglevel`       | Print every kernel message to the console                                           |
| `loglevel=8`            | Print messages below level 8, which includes `KERN_DEBUG`; `loglevel=7` excludes it |

Most have a sysctl counterpart under `/proc/sys/kernel/`, such as `panic_on_oops` and `panic_on_warn`.

## Crash Dumps

`oops=panic` turns an oops into a panic, but it does not configure kdump by itself. Verify the crash-kernel
reservation, capture setup, dump destination, and recovery separately before expecting a vmcore. Analyse one with
the matching kernel:

```bash
crash /path/to/crashed-kernel/vmlinux /path/to/vmcore
```

Check that architecture, configuration, symbols, module data, and crash-tool support match the dump. Inside `crash`,
`log`, `bt`, `bt -a`, `ps`, and `mod` answer different questions about the captured state.

## Getting Output When Nothing Prints

- `earlycon` with no options takes the early console from the device tree's `stdout-path`. With options it names
  the UART: `earlycon=uart8250,mmio32,<addr>` or `earlycon=pl011,<addr>`. The PL011 early driver needs the bootloader
  to have set the UART up already.
- `console=ttyS0,115200n8` (8250) or `console=ttyAMA0,115200` (PL011) sets the real console. `keep_bootcon` keeps the
  early console alive past the handover, for a failure in that window. `initcall_debug` logs each initcall, which finds
  where boot stops.
- Raspberry Pi strings, from Raspberry Pi's documentation, go in `cmdline.txt`. Choosing the wrong UART can stop the
  board booting.
  - Pi 4, 400, CM4: the default console is the mini UART, `earlycon=uart8250,mmio32,0xfe215040`, with
    `enable_uart=1` in `config.txt`, which fixes the core clock at 250 MHz. The PL011 alternative is
    `earlycon=pl011,mmio32,0xfe201000`, after moving the console to it.
  - Pi 5: the debug header labelled UART is `UART10`, `/dev/ttyAMA10`:
    `earlycon=pl011,0x107d001000,115200n8` and `console=serial0,115200`, where `serial0` resolves to `ttyAMA10`.
- When still nothing prints, halt the cores over JTAG (below) and read the kernel log from memory with the GDB
  scripts' `lx-dmesg`.

## kgdb and kdb

Build with `CONFIG_KGDB`, `CONFIG_KGDB_SERIAL_CONSOLE`, and `CONFIG_KALLSYMS`; add `CONFIG_KGDB_KDB` for the kdb
shell and `CONFIG_MAGIC_SYSRQ` to enter it on demand. `CONFIG_STRICT_KERNEL_RWX` blocks software breakpoints; turn it
off, use hardware breakpoints, or pass `rodata=off` where the option cannot be disabled (arm64).

```text
kgdboc=ttyS0,115200 kgdbwait     # kgdbwait must follow kgdboc, and needs the driver built in
```

- Enter the debugger with `echo g > /proc/sysrq-trigger`, SysRq-G, a terminal break, or `kgdbwait` at boot.
  Stopping the kernel stops everything, including watchdog servicing: confirm the halt fits the task first.
- Connect: `gdb vmlinux`, `set serial baud 115200`, `target remote /dev/ttyUSB0`. A Ctrl-C from GDB does not
  interrupt a running kgdboc target; a proxy that sends SysRq-G does.
- One UART for both console and kgdb needs a splitter such as `agent-proxy`
  (<https://git.kernel.org/pub/scm/utils/kernel/kgdb/agent-proxy.git>): `agent-proxy 5550^5551 0 /dev/ttyUSB0,115200`,
  then `telnet localhost 5550` for the console and `target remote localhost:5551` in GDB. kgdboc and `kgdbcon` cannot
  share a tty that is the active system console.
- `kgdboc_earlycon=<name>` extends kgdb into early boot, with the driver built in.
- kdb alone, on the console: `console=ttyS0,115200 kgdboc=ttyS0,115200 nokaslr`, then `help`, `ps`, `bt`, `dmesg`,
  `lsmod`, and `go`.

## JTAG on the Application Cores

Wiring and target files are in `debug-hardware` and `debug-server-tools`. On the Linux side:

- Boot with `nokaslr`, and load the matching `vmlinux` with debug info.
- Add `nohlt` when a halt times out on an idle core: WFI gates the core clock that JTAG needs, and `nohlt` makes the
  idle loop busy-wait instead. It needs `CONFIG_GENERIC_IDLE_POLL_SETUP`.
- In OpenOCD, `aarch64 smp on` halts and resumes all cores in the SMP group together, and `-rtos hwthread` presents the
  cores as GDB threads. `targets` lists the cores and selects one when SMP is off. `aarch64 maskisr on`, the default,
  masks interrupts while single-stepping, so a step does not land in an interrupt handler.
- The Pi 4's `target/bcm2711.cfg` defines four `aarch64` cores with SMP off by default; set `USE_SMP` to group them.
  OpenOCD master has no Pi 5 target file; use J-Link or probe-rs there.

## GDB Helper Scripts

With `CONFIG_GDB_SCRIPTS`, run `make scripts_gdb`, then start `gdb vmlinux` in the build directory. If GDB declines
`vmlinux-gdb.py`, add `add-auto-load-safe-path /path/to/linux-build` to `~/.gdbinit`. The helpers include
`lx-symbols` (loads module symbols from the build tree), `lx-dmesg`, `lx-ps`, `lx-lsmod`, `lx-cmdline`, `lx-version`,
`lx-iomem`, and `lx-fdtdump`, and functions such as `$lx_current()` (x86 and arm64 only). They work over kgdb, JTAG,
and QEMU alike.
