# Tracing and Profiling on Embedded Linux

Choose the tool from the question: syscall failure, CPU cost, timing, or resource leak. Match symbols and source to
the running build. Bound duration and storage, record relevant debug settings, and account for timing changes,
watchdogs, and pauses before acting on a live target. Debuggers, kgdb, and crash analysis are in `SKILL.md` and the
other references.

## Syscalls

For an application you are authorized to run or attach to, choose a narrow strace scope and an output file:

```bash
strace -f -e trace=openat,read,write -o trace.log ./myapp
strace -f -c ./myapp
```

For a hang, attach to the known process under a duration limit supported by the target's tools.
Keep the captured return codes and time window; provide a useful excerpt without discarding the original evidence.
Attaching changes timing, and traces may include application data. Missing files, permission errors, and blocking
calls can explain userspace behavior without a kernel or DTS edit.

Yocto's `tools-debug` image feature installs `strace` but not `ltrace`; `ltrace` comes from meta-oe and must be added
to the image explicitly.

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

## MMIO

Prefer driver-owned clock, pinctrl, bus, and subsystem diagnostics over `/dev/mem` access.
For a necessary raw read, verify the exact register, access width, read semantics, power/clock domain, and ownership
against the device manual before selecting `devmem`/`devmem2` syntax.
A read can clear an interrupt or fault. A saved register value is not a general undo for writes.
No board-independent register address is safe to prescribe here, and a write is always-ask.

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
