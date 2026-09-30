---
name: embedded-linux-debugging
description: "Debug Linux on embedded boards from the kernel down to userspace: oops and panic decoding, early-boot output, kgdb over serial, JTAG on the application cores, U-Boot, gdbserver, core dumps, tracing and profiling, and Yocto debug symbols. Use when a board panics or hangs in boot, a driver crashes, or a userspace program needs remote debugging, tracing, or profiling. Board bring-up and device trees belong to embedded-linux-bringup; U-Boot porting to u-boot-development."
license: MIT
compatibility: Needs the matching kernel, U-Boot, or program build with debug symbols; kernel and U-Boot work need serial console or JTAG access through the user.
metadata:
  author: Joonas Onatsu
---

# Embedded Linux Debugging

Find why a Linux board fails, at whichever layer it fails: the bootloader, the kernel's early boot, a driver, or a
userspace program. Wiring, probes, and debug servers belong to `debug-hardware` and `debug-server-tools`; GDB itself
to `gdb-debugging`; bring-up and device trees to `embedded-linux-bringup`.

**Match the build.** Every decode, backtrace, and symbol lookup is only as good as its match with what ran: the
same `vmlinux`, the same U-Boot ELF, the same program and libraries. Record the build identity before decoding, and
treat a mismatch as a blocker rather than a caveat; the wrong symbols produce plausible, wrong answers.

**Stopping a board is an action.** Halting the kernel with kgdb or JTAG stops watchdog servicing and every service on
the board, and changing the kernel command line or `config.txt` changes its boot media. Confirm these fit the task,
and restore what the session changed.

## 1. Locate the Failing Layer

Read the last output before the failure, from the serial console:

| Last thing seen                                    | Layer         | Go to           |
| -------------------------------------------------- | ------------- | --------------- |
| Nothing, or only the boot ROM                      | Boot firmware | JTAG, section 3 |
| U-Boot or SPL banner, then silence or an exception | Bootloader    | Section 4       |
| `Starting kernel ...`, then silence                | Early kernel  | Section 2       |
| A kernel oops, panic, or `WARN`                    | Kernel        | Section 2       |
| Userspace messages, then a crash or a hang         | Userspace     | Section 5       |
| No crash, but slow, wrong, or leaking              | Any           | Section 6       |

Serial capture belongs to `serial-console-debugging`; keep the whole log, not an excerpt, since the lines before a
failure usually name its cause.

## 2. Kernel Failures

- **An oops or panic:** decode it against the matching `vmlinux` with the kernel tree's `decode_stacktrace.sh`,
  or its `faddr2line` for a `function+offset/size` frame, with `CROSS_COMPILE` set to the target's tool prefix.
- **Silence after `Starting kernel`:** add `earlycon` and `keep_bootcon`, raise output with `ignore_loglevel`, and
  find the last initcall with `initcall_debug`. On a Raspberry Pi, the wrong early-console UART can stop the boot;
  use the documented string for the model.
- **A live kernel to inspect:** kgdb over serial, with kdb for a quick look, or JTAG when the kernel cannot be
  trusted to run the debugger itself.

[references/kernel-debugging.md](references/kernel-debugging.md) holds the commands, command-line parameters, the
Raspberry Pi console strings, kgdb and `agent-proxy` setup, crash dumps, and the GDB helper scripts.

## 3. JTAG on the Application Cores

Use JTAG for a board that prints nothing, a hang with interrupts off, or a failure before any console exists. Boot
with `nokaslr`, load the matching `vmlinux`, and add `nohlt` when a halt times out on an idle core. The OpenOCD side
(SMP groups, `hwthread`, the Pi 4 target file) is in
[references/kernel-debugging.md](references/kernel-debugging.md); wiring and the Pi's `enable_jtag_gpio=1` are in
`debug-hardware`.

## 4. U-Boot

Build with `-Og` and without LTO, debug the `u-boot` ELF, and reload the symbols at `relocaddr` once U-Boot has
relocated itself. SPL runs at its link address. The procedure and the crash-output decoding are in
[references/u-boot-debugging.md](references/u-boot-debugging.md).

## 5. Userspace

- **Interactive:** `gdbserver` on the board, preferably over SSH's stdio, with the host's cross GDB pointed at the
  image's debug sysroot.
- **After the fact:** a core dump, from `core_pattern` or `systemd-coredump`, opened on the host with the cross GDB.
- **Yocto images:** get the symbols through the debug filesystem, the SDK sysroot, or `oe-debuginfod`, all built from
  the same image.

[references/userspace-and-yocto.md](references/userspace-and-yocto.md) has the setup and the Yocto features that
changed recently, including `debug-tweaks`' removal.

## 6. Tracing and Profiling

For behaviour without a crash, choose by the question: `strace` for a syscall failure, `perf` for CPU cost, ftrace and
`trace-cmd` for kernel timing and call paths, `dynamic_debug` for a driver's own messages, `kmemleak` and Valgrind for
leaks and races. Each changes timing, and some change shared kernel state that must be restored.
[references/tracing-and-profiling.md](references/tracing-and-profiling.md) has the bounded commands.

The work is done when the failure is explained by evidence from the matching build: a decoded backtrace, a register
or memory state, a trace, or a log that names the cause, with every setting the session changed restored.
