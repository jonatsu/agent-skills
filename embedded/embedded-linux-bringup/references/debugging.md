# Embedded Linux Debugging

Choose the tool from the question: syscall failure, code location, CPU cost, timing, resource leak, or crash state.
Match symbols and source to the running/captured build. Bound duration and storage, record relevant debug settings,
and account for timing changes, watchdogs, and pauses before acting on a live target.

## Syscalls and Userspace Debuggers

For an application you are authorized to run or attach to, choose a narrow strace scope and an output file:

```bash
strace -f -e trace=openat,read,write -o trace.log ./myapp
strace -f -c ./myapp
```

For a hang, attach to the known process under a duration limit supported by the target's tools.
Keep the captured return codes and time window; provide a useful excerpt without discarding the original evidence.
Attaching changes timing, and traces may include application data. Missing files, permission errors, and blocking
calls can explain userspace behavior without a kernel or DTS edit.

Use cross-GDB with the exact executable and matching target libraries/debug information.
Set its sysroot to the corresponding development/debug tree, or use supported remote file retrieval when appropriate.
A sysroot supplies file lookup; it cannot create debug symbols absent from those files.

Prefer gdbserver over an authenticated SSH stdio transport when the target supports it:

```text
(gdb) file /path/to/matching/unstripped/myapp
(gdb) set sysroot /path/to/matching/target-sysroot
(gdb) target remote | ssh -T board gdbserver --once stdio /usr/local/bin/myapp
(gdb) continue
```

Use a trusted SSH alias and appropriate target user. Account for this transport's application-stdin limitations.
For attachment or multi-process sessions, use the installed GDB/gdbserver version's supported mode and explicitly
end the session. Inspect whether the process should resume or terminate; do not assume disconnect performs recovery.

[gdbserver has no built-in authentication](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Server.html).
If TCP is necessary, establish actual firewall/network isolation before opening the listener and verify its addresses.
The hostname part of gdbserver's `host:port` argument is ignored in the documented interface; writing `localhost`
there is not a loopback security control. Close the listener after use.
For QEMU's explicit loopback stub, see [deploy-and-iterate.md](deploy-and-iterate.md).

## CPU Profiling: Select the Subject

Use the target's available perf events and supported call-chain method.
Capture a representative operation, not an idle timer process by accident:

```bash
# Profile the command itself.
perf record -g -- ./myapp
perf report

# System-wide capture for ten seconds, including unrelated work on this target.
perf record -a -g -- sleep 10

# Counters for one command.
perf stat -- ./myapp
```

For an already running process, select its PID explicitly with the installed perf's `-p` option and a bounded duration.
Check permissions, event availability, unwind support, and lost samples before interpreting missing data.
Frame pointers, DWARF unwinding, architecture, and build flags affect stack quality.
See the matching [perf record manual](https://github.com/torvalds/linux/blob/v6.12/tools/perf/Documentation/perf-record.txt).

For flame graphs, obtain and verify the selected FlameGraph tools, then convert the recorded data:

```bash
perf script -i perf.data > stacks.txt
stackcollapse-perf.pl stacks.txt > folded.txt
flamegraph.pl folded.txt > flamegraph.svg
```

Run these as separate checked operations; an empty downstream graphic is not proof that collection succeeded.
Keep matching symbols available on the analysis host. Interpret CPU samples as on-CPU cost, not automatically
end-to-end latency or time blocked on I/O. Record workload, duration, event, sampling configuration, and build identity.

## ftrace and trace-cmd

Check the running kernel's tracing configuration and available tracers/events/functions first.
tracefs is commonly `/sys/kernel/tracing`, with older debugfs paths also possible.
Do not mount, reset, or overwrite a shared tracing session casually.

For a supported target with trace-cmd installed, a bounded command can define the capture lifetime:

```bash
trace-cmd record -p function_graph -g my_driver_probe ./reproduce-probe
trace-cmd report
```

Confirm the named function exists and the reproduction actually invokes it. A built-in probe may have occurred only
during boot; starting tracing later will not recover that event. Select suitable boot tracing or an authorized reprobe.
Use trace instances where supported when another session is active, and preserve the configuration you change.
The [ftrace documentation](https://docs.kernel.org/trace/ftrace.html) governs filter, buffer, and clock semantics.

## dynamic_debug

When supported, inspect the dynamic-debug control table and select a narrow module/file/function query.
Its location depends on the kernel's debugfs/proc configuration. Save the affected sites' prior flags first.

```bash
# Target example: changes logging for this module.
echo 'module ov5640 +p' > /sys/kernel/debug/dynamic_debug/control
```

Restore the affected settings after capture; blanket `-p` is not an exact restore when some sites were previously enabled.
For early failures, use the version-supported boot query or module dyndbg parameter in the authorized boot configuration.
Extra logging changes timing and storage demand. It is less invasive than many code changes, but is not effect-free.
See [dynamic debug](https://docs.kernel.org/admin-guide/dynamic-debug-howto.html).

## MMIO, kgdb, and kdb

Prefer driver-owned clock, pinctrl, bus, and subsystem diagnostics over `/dev/mem` access.
For a necessary raw read, verify the exact register, access width, read semantics, power/clock domain, and ownership
against the device manual before selecting `devmem`/`devmem2` syntax.
A read can clear an interrupt or fault. A saved register value is not a general undo for writes.
Follow the hardware-access contract in `SKILL.md`; no board-independent register address is safe to prescribe here.

For kernel debugging, check KGDB/KDB support, matching `vmlinux`, transport support, and recovery access.
A serial setup can use `kgdboc=ttyS0,115200 kgdbwait` when that UART and built-in configuration are appropriate.
`kgdbwait` requires kgdboc to be initialized at the relevant point; modules cannot provide the early built-in path.
Sharing the console requires coordinating terminal ownership and the debugger connection.

Writing `g` to `/proc/sysrq-trigger` can stop the kernel for debugging. Confirm that a halt and its watchdog consequences
fit the authorized operation before doing so. Network KGDB transport is not universally available in upstream kernels.
Follow the selected [kernel debugger documentation](https://docs.kernel.org/process/debugging/kgdb.html).

## Kernel Oops and Crash Dumps

Preserve the panic/oops, kernel build identity, relevant module identities, and available dump before reboot/cleanup.
Decode against the crashed kernel, not the analysis host's `uname -r` or a different capture kernel:

```bash
crash /path/to/crashed-kernel/vmlinux /path/to/vmcore
```

Check that architecture, configuration, symbols, module data, and crash-tool support match the dump.
Inside crash, `log`, `bt`, `bt -a`, `ps`, and `mod` answer different questions about the captured state.
For textual stacks, use the matching kernel's `scripts/decode_stacktrace.sh` and its required toolchain/source context.
Raw-address `addr2line` also requires accounting for relocation/KASLR; an unrelated symbol file can produce plausible noise.

`oops=panic` can turn an oops into a panic, but it does not configure kdump by itself.
Verify crash-kernel reservation, capture setup, dump destination, and recovery separately before expecting a vmcore.

## Memory Leaks and Concurrency

With `CONFIG_DEBUG_KMEMLEAK` and the required debugfs support, inspect the existing scan state and reports.
The supported control interface includes:

```text
scan          request a scan
scan=off      stop the background scanner
scan=on       start it
scan=SECONDS  set its period (default 600 seconds in Linux v6.12)
```

Write only the selected command to `/sys/kernel/debug/kmemleak`, record the changed scan settings, and restore them.
Do not clear another investigation's reports. Interpret reported objects as candidates with possible false positives
and omissions; see [kmemleak](https://docs.kernel.org/dev-tools/kmemleak.html).

Where Valgrind supports the target architecture/libc and memory budget, Memcheck and Helgrind can investigate userspace
memory errors and races. Preserve the reproduction and account for substantial timing changes.
For vgdb, run the bridge where it can reach that Valgrind instance, or configure an explicit supported remote transport.
Host-local `target remote | vgdb` does not automatically connect to Valgrind on a separate board.
Use the [Valgrind manual](https://valgrind.org/docs/manual/manual-core-adv.html) for the selected version's setup.
