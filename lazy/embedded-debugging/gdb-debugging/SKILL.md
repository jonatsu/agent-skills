---
name: gdb-debugging
description: "Drive GDB, or LLDB where a toolchain uses it, to debug embedded and cross-compiled programs over a debug server, a gdbserver on embedded Linux, or a core dump. Use for choosing gdb-multiarch or an architecture-specific GDB, connecting and loading, hardware breakpoint and watchpoint limits, optimized code, batch runs, Rust, or LLDB equivalents. Starting the server belongs to debug-server-tools; kernel and kgdb work to embedded-linux-debugging."
license: MIT
compatibility: Needs a GDB (gdb-multiarch or a toolchain's own) or LLDB, the program's ELF with debug symbols, and a reachable debug server, gdbserver, or core file.
metadata:
  author: Joonas Onatsu
---

# GDB Debugging

Debug a program that runs somewhere other than the host: an MCU behind a debug server, a process on an embedded
Linux board behind `gdbserver`, or a crash captured as a core file. The server side belongs to `debug-server-tools`;
kernel and early-boot debugging to `embedded-linux-debugging`; fault analysis on MCUs to `mcu-firmware-debugging`.
The permission tiers from `debug-hardware` apply: `load` writes flash, so it needs the task's agreement.

Current known: GDB 18.1 and LLDB from LLVM 23.1.2, checked 2026-09-30 against their manuals and sources. GDB's own
`help <command>` and LLDB's `help <command>` are the reference for flags.

## 1. Choose the Debugger

Start with `gdb-multiarch`, a GDB built with `--enable-targets=all`, which covers Arm, AArch64, RISC-V, Xtensa, MIPS,
AVR, and more. Switch to the target's own GDB, such as `arm-none-eabi-gdb`, Espressif's `xtensa-esp32-elf-gdb`, or a
Yocto SDK's `aarch64-poky-linux-gdb`, in any of these cases:

- the user asks for it, or the project's scripts or IDE configuration name it;
- `set architecture` with no argument does not list the target's architecture, which means this build lacks it;
- `gdb-multiarch` misreads the ELF, the registers, or the target description, because a vendor's GDB carries
  patches upstream does not.

`gdb --configuration` shows how a GDB was built, including Python support, which Rust pretty-printers and many
project scripts need.

Use LLDB when the project's toolchain is LLVM-based and ships it, or the user prefers it.
[references/lldb.md](references/lldb.md) maps the commands in this skill to LLDB and lists what LLDB cannot do here:
it has no flash `load`.

## 2. Connect

Load the ELF that carries debug symbols, not a stripped image or a raw binary, then connect:

```text
file build/firmware.elf
target extended-remote localhost:3333
monitor reset halt
load
monitor reset halt
```

- `target extended-remote` keeps GDB connected when the program exits or is detached, and allows `run` and
  `attach`; `target remote` drops the connection and supports neither. Prefer extended-remote with a debug server.
- The port depends on the server: OpenOCD and pyOCD 3333, probe-rs 1337, J-Link GDB Server 2331. The server-specific
  sequences, multi-core views, and RTOS awareness are in [references/remote-recipes.md](references/remote-recipes.md).
- `monitor <command>` passes a command to the server uninterpreted, so its syntax is the server's.
- `load` writes the ELF's loadable sections through the server, which programs flash where it can. It is in the
  flash tier.
- `disconnect` leaves the target halted for a later connection; `detach` releases it running.

For a process on embedded Linux, run `gdbserver` on the board and point the host GDB at the board's files:

```text
# on the target
gdbserver :2345 /usr/bin/app            # or: gdbserver --attach :2345 <pid>
# on the host
set sysroot /path/to/sdk/sysroot
target extended-remote <board-ip>:2345
```

The host needs unstripped copies of the program and libraries that match the target's exactly. `set sysroot`
points at a tree mirroring the target's `/lib` and `/usr/lib`; `set debug-file-directory` points at separate
debug-info files, such as a Yocto SDK's `.debug` directories; `set substitute-path <from> <to>` maps build paths to
the local source tree. `gdbserver` has no security of its own, so keep it off untrusted networks.

## 3. Break and Watch Within Hardware Limits

Code in flash takes only hardware breakpoints, and an MCU has few: the Arm TRMs give ranges, and the chip vendor
chooses the count.

| Core          | Hardware breakpoints | Watchpoints |
| ------------- | -------------------- | ----------- |
| Cortex-M0/M0+ | 1 to 4               | 1 or 2      |
| Cortex-M3/M4  | 2 or 6               | 1 or 4      |
| Cortex-M7     | 4 or 8               | 2 or 4      |
| Cortex-M33    | 4 or 8               | 2 or 4      |

- Use `hbreak` for code in flash, or rely on `set breakpoint auto-hw on` (the default), which picks hardware
  breakpoints when the server reports a memory map.
- When the server reports no limit, set it: `set remote hardware-breakpoint-limit 4` and
  `set remote hardware-watchpoint-limit 2` with the chip's counts. Otherwise GDB accepts too many and fails at
  resume with `Could not insert hardware breakpoints:` followed by
  `You may have requested too many hardware breakpoints/watchpoints.` Delete or disable some and continue.
- `watch` breaks on a write that changes the value, `rwatch` on a read, and `awatch` on either; the last two exist
  only in hardware. A watchpoint on a stack variable ends when its frame returns; `watch -location <expr>` watches
  the address instead. A large struct or a compound expression can need more comparators than the chip has.
- Breakpoint `commands` with `silent` and `continue` log values without stopping for long:

```text
break uart_rx_isr
commands
  silent
  printf "rx=%x\n", byte
  continue
end
```

## 4. Read Optimized Code

Embedded builds are usually optimized, so expect `<optimized out>` for values the compiler kept in registers.
Recover them from another variable or a register, or rebuild the unit under investigation with `-Og`. Inlined
functions appear in backtraces and `info frame` says when a frame is inlined; `finish` cannot report an inlined
call's return value, so step to the next line and print the variable that received it. A breakpoint on an inlined
call site may move to the next line.

## 5. Batch Runs and Scripts

A batch run makes a capture reproducible and fits in a log:

```bash
gdb-multiarch -batch -nx -ex "target extended-remote localhost:3333" -ex "monitor reset halt" \
  -ex "info registers" -ex "bt" build/firmware.elf
```

- `-batch` exits after the commands, disables paging and confirmation, and returns nonzero when a command fails;
  `-nx` skips init files, so the run does not depend on the user's `~/.gdbinit`.
- `-x <file>` runs a command file; `-iex` runs a command before the program loads, which is where settings such as
  `set auto-load safe-path` go.
- `set logging enabled on` with `set logging file <path>` records a session; the older `set logging on` is
  deprecated.
- A project `.gdbinit` loads only from a directory on the auto-load safe path; otherwise GDB warns that its
  auto-loading "has been declined". Read the file before trusting it, since it can run any command, then add its
  directory with `add-auto-load-safe-path`.

## 6. Rust

`rust-gdb` wraps GDB with Rust's pretty-printers and source-path mapping; set `RUST_GDB=gdb-multiarch` (or the
target's GDB) to use a cross debugger with it. GDB's Rust support prints types and values well but cannot evaluate
`match`, closures, or generics without explicit type parameters, and `break B::f` looks for a crate named `B`.
`defmt` logging over RTT belongs to `mcu-firmware-debugging`.

## 7. Core Dumps

`gdb <elf> <core>` opens a core file from embedded Linux; prefix a core file whose name starts with a digit with
`./`, or GDB treats it as a process ID. GDB builds for bare-metal targets usually lack core-file support and ignore
the argument. Match the ELF and the sysroot to the build that crashed. Getting the core off the target belongs to
`embedded-linux-debugging`.

The work is done when the answer comes from the target's state: the backtrace, registers, variables, or watchpoint
hits that explain the behaviour, captured in the output, with any flash writes kept within their tier.
