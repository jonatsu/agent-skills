# Embedded Linux Debugging

## Contents

- [strace — System Call Tracer](#strace--system-call-tracer)
- [Remote GDB Debugging (gdbserver)](#remote-gdb-debugging-gdbserver)
- [perf — Performance Profiling](#perf--performance-profiling)
- [ftrace — In-Kernel Function Tracer](#ftrace--in-kernel-function-tracer)
- [dynamic_debug — Enable pr_debug() at Runtime](#dynamic_debug--enable-pr_debug-at-runtime)
- [devmem / devmem2 — Peek and Poke Physical Registers](#devmem--devmem2--peek-and-poke-physical-registers)
- [kgdb / kdb — In-Kernel Debugger](#kgdb--kdb--in-kernel-debugger)
- [crash — Kernel Analysis Tool](#crash--kernel-analysis-tool)
- [kmemleak — Kernel Memory Leak Detector](#kmemleak--kernel-memory-leak-detector)
- [Kernel Oops / Panic Analysis](#kernel-oops--panic-analysis)
- [valgrind — Memory Error Detector](#valgrind--memory-error-detector)
- [Quick Diagnostics Reference](#quick-diagnostics-reference)

## strace — System Call Tracer

`strace` intercepts and records the system calls a process makes.

```bash
strace ./myapp                        # trace a new process
strace -p <pid>                       # attach to a running process
strace -f ./myapp                     # follow forked children
strace -c ./myapp                     # per-syscall stats (count, time)
strace -e open,read,write ./myapp     # only these syscalls
strace -e trace=network ./myapp       # all network syscalls
strace -e trace=signal ./myapp        # signal-related only
strace -o /tmp/strace.log ./myapp     # write to file (stderr busy)
strace -f -c ./myapp                  # follow forks + stats
```

| Symptom                | strace use                                              |
| ---------------------- | ------------------------------------------------------- |
| Process hangs silently | `strace -p <pid>` — see the blocking syscall            |
| File-not-found errors  | `strace -e openat ./app` — see which paths are tried    |
| Network failures       | `strace -e trace=network ./app` — see connect/bind/send |
| Permission denied      | `strace -e openat,access ./app` — see EACCES calls      |

## Remote GDB Debugging (gdbserver)

Embedded targets rarely run a full GDB. Use `gdbserver` on the target and cross-GDB on the host.

### Target side

```bash
gdbserver :2345 ./myapp [args]        # start a program under gdbserver
gdbserver --attach :2345 <pid>        # attach to a running process
gdbserver --multi :2345               # multi-process (re-run without restart)
```

### Host side

```bash
aarch64-linux-gnu-gdb ./myapp         # cross GDB (or the Yocto SDK's GDB)

# In the GDB shell:
(gdb) set sysroot /opt/poky/4.3/sysroots/cortexa53-poky-linux
(gdb) set solib-search-path /opt/poky/4.3/sysroots/cortexa53-poky-linux/usr/lib
(gdb) target remote 192.168.1.100:2345
(gdb) continue
```

Multi-mode (re-run programs from the host without restarting gdbserver):

```bash
(gdb) target extended-remote 192.168.1.100:2345
(gdb) set remote exec-file /usr/bin/myapp
(gdb) run
```

`set sysroot` is critical — without it GDB cannot find shared-library debug symbols and backtraces show `??` frames.

## perf — Performance Profiling

```bash
# Record CPU cycles for a duration (-g = call graph, needed for flame graphs)
perf record -g -- sleep 30
perf report
perf record -g ./myapp
```

### Flame Graph Generation

Requires Brendan Gregg's FlameGraph scripts.

```bash
# On target: record with call graph, then on host
perf script | stackcollapse-perf.pl | flamegraph.pl > flamegraph.svg

# Or copy perf.data to host and generate there
scp root@target:/tmp/perf.data .
perf script -i perf.data | stackcollapse-perf.pl | flamegraph.pl > flamegraph.svg
```

### perf stat — Event Counters

```bash
perf stat ./myapp
perf stat -e cache-misses,cache-references,instructions ./myapp
```

## ftrace — In-Kernel Function Tracer

`ftrace` is the kernel's built-in tracer. It needs:

```
CONFIG_FTRACE=y
CONFIG_DYNAMIC_FTRACE=y        # zero-overhead when disabled
CONFIG_FUNCTION_TRACER=y
CONFIG_FUNCTION_GRAPH_TRACER=y
CONFIG_SCHED_TRACER=y
```

Accessed via `tracefs`, usually at `/sys/kernel/tracing` (or `/sys/kernel/debug/tracing` on older kernels).

```bash
mount -t tracefs nodev /sys/kernel/tracing   # if not already mounted
cd /sys/kernel/tracing

cat available_tracers                         # nop, function, function_graph, ...
echo function_graph > current_tracer          # call depth + duration
echo 1 > tracing_on
./myapp
echo 0 > tracing_on
cat trace | head -100
```

### Trace a specific function and its callees

```bash
echo do_sys_open > set_graph_function
echo function_graph > current_tracer
echo 1 > tracing_on
./myapp
echo 0 > tracing_on
cat trace
```

### trace-cmd (higher-level ftrace frontend)

```bash
trace-cmd list -t                             # tracers
trace-cmd list -e                             # events
trace-cmd list -f                             # functions

trace-cmd record -p function_graph -g my_driver_probe ./myapp
trace-cmd report | head -200

trace-cmd record -l 'spi_*' -p function_graph # filter by name pattern
trace-cmd record -e irq:irq_handler_exit -e irq:irq_handler_entry

# Remote collection (avoid filling target storage)
trace-cmd listen -p 6578                       # on host
trace-cmd record -N <host-ip>:6578 -p function_graph   # on target

trace-cmd reset                                # clear buffers
```

## dynamic_debug — Enable pr_debug() at Runtime

`dynamic_debug` turns individual `pr_debug()`/`dev_dbg()` sites on and off without a rebuild — the fastest way to get a
driver's own debug output during a probe failure. Needs `CONFIG_DYNAMIC_DEBUG=y`; control file is
`/sys/kernel/debug/dynamic_debug/control` (debugfs must be mounted).

```bash
# See every controllable debug site and its current flags
cat /sys/kernel/debug/dynamic_debug/control | head

# Enable all debug prints in one module (+p = print)
echo 'module ov5640 +p' > /sys/kernel/debug/dynamic_debug/control

# Enable one file, one function, or one line
echo 'file drivers/media/i2c/ov5640.c +p' > /sys/kernel/debug/dynamic_debug/control
echo 'func ov5640_probe +p' > /sys/kernel/debug/dynamic_debug/control
echo 'file ov5640.c line 1200-1260 +p' > /sys/kernel/debug/dynamic_debug/control

# Add source location + function name to each line (+pfl)
echo 'module ov5640 +pfl' > /sys/kernel/debug/dynamic_debug/control

# Turn it back off (-p)
echo 'module ov5640 -p' > /sys/kernel/debug/dynamic_debug/control
```

Enable at boot for a probe that fails before userspace by adding `dyndbg="module ov5640 +p"` (or `<module>.dyndbg=+p`)
to the kernel command line. Output lands in `dmesg`. This is read-safe; it only changes logging verbosity.

## devmem / devmem2 — Peek and Poke Physical Registers

`devmem2` (and BusyBox `devmem`) read and write physical addresses through `/dev/mem` — useful for confirming a pinmux,
clock-gate, or peripheral register value the kernel is not exposing in sysfs. **Reads are a safe diagnostic; writes are
a hardware mutation and MUST pass the skill's confirmation gate — a wrong write can hang or damage the SoC.**

```bash
# READ a 32-bit register (safe)
devmem2 0x020e0000 w
devmem 0x020e0000 32          # BusyBox form

# WRITE a 32-bit value (MUTATION — confirm first, record the old value to restore)
devmem2 0x020e0000 w 0x00000005
# reverse: write the value you captured with the read back to the same address
```

Common use: verify the bootloader/kernel programmed a mux or clock register as the DTS intended, when a device is silent
but probe "succeeded". Prefer the clock (`clk_summary`) and pinctrl debugfs views first; drop to `devmem` only when you
need the raw register and confirm before writing.

## kgdb / kdb — In-Kernel Debugger

`kgdb` lets a host GDB debug the kernel itself over a serial line (or KGDB-over-NET); `kdb` is the built-in low-level
shell front end. Needs `CONFIG_KGDB=y`, `CONFIG_KGDB_SERIAL_CONSOLE=y`, and ideally `CONFIG_DEBUG_INFO=y` for symbols.

Enable a serial port as the KGDB channel, at boot or at runtime:

```bash
# Boot: share the console UART with kgdb, and break early
#   kernel cmdline:  kgdboc=ttyS0,115200 kgdbwait

# Runtime: attach kgdb to a UART after boot
echo ttyS0 > /sys/module/kgdboc/parameters/kgdboc

# Drop into the debugger on demand (sysrq-g), then connect host GDB
echo g > /proc/sysrq-trigger
```

On the host, connect the cross-GDB to the same serial line:

```bash
aarch64-linux-gnu-gdb vmlinux
(gdb) set serial baud 115200
(gdb) target remote /dev/ttyUSB0
(gdb) bt
(gdb) continue
```

`kgdbwait` halts the kernel very early so you can set breakpoints before the fault; pair it with `earlycon` so you still
see boot output. Debugging the kernel over the same UART as the console requires the shared `kgdboc` console setup
above.

## crash — Kernel Analysis Tool

`crash` analyses live kernels and kernel core dumps (vmcore).

```bash
crash /usr/lib/debug/lib/modules/$(uname -r)/vmlinux /proc/vmcore

# Inside the crash shell:
crash> bt            # backtrace of current context
crash> bt -a         # backtrace all tasks
crash> log           # kernel message buffer (dmesg equivalent)
crash> ps            # list all processes
crash> files <pid>   # open files for a PID
crash> kmem -i       # kernel memory info
crash> mod           # loaded modules
```

`crash` is the primary tool when a panic produces a vmcore via kdump. It can also attach to a running kernel for live
inspection.

## kmemleak — Kernel Memory Leak Detector

Requires `CONFIG_DEBUG_KMEMLEAK=y`.

```bash
mount -t debugfs none /sys/kernel/debug        # if not mounted
echo scan > /sys/kernel/debug/kmemleak         # manual scan (auto runs every 10 min)
cat /sys/kernel/debug/kmemleak                 # read leak report
echo clear > /sys/kernel/debug/kmemleak        # clear reported leaks
```

Each entry shows the allocation call stack. The auto-scan interval is set by `CONFIG_DEBUG_KMEMLEAK_AUTO_SCAN`; disable
it and scan manually for tighter, targeted testing.

## Kernel Oops / Panic Analysis

An oops/panic prints the faulting address and a symbol+offset call stack. Decode it:

```bash
addr2line -s -f -e vmlinux <hex-address>       # a single address
./scripts/decode_stacktrace.sh vmlinux [src/] < oops.txt > decoded.txt   # full report
aarch64-linux-gnu-objdump -d vmlinux | grep -A 20 "<symbol>"             # disassemble
```

`ARCH` and `CROSS_COMPILE` must be set correctly when running kernel scripts on the host.

| Kernel param / config    | Effect                                                 |
| ------------------------ | ------------------------------------------------------ |
| `oops=panic`             | Treat every oops as a panic (enables kdump collection) |
| `CONFIG_PANIC_ON_OOPS=y` | Same, compile-time                                     |
| `CONFIG_PANIC_TIMEOUT=5` | Reboot 5 s after panic                                 |
| `panic=5`                | Cmdline: reboot after N seconds                        |

## valgrind — Memory Error Detector

Runs on the target when glibc and enough RAM are available.

```bash
valgrind --tool=memcheck --leak-check=full ./myapp   # memory errors, leaks
valgrind --tool=helgrind ./myapp                     # threading errors

# GDB bridge:
valgrind --vgdb=yes --vgdb-error=0 ./myapp           # terminal 1
aarch64-linux-gnu-gdb ./myapp                        # terminal 2 (host)
(gdb) target remote | vgdb
```

Not suitable for bare-metal or extremely constrained targets — use it only with a full glibc userspace and adequate RAM.

## Quick Diagnostics Reference

| Problem                           | Tool                          | Key option                 |
| --------------------------------- | ----------------------------- | -------------------------- |
| Process hangs / blocked           | `strace -p`                   | see blocking syscall       |
| Startup failure (file not found)  | `strace -e openat`            | trace open calls           |
| Silent driver probe, no logs      | `dynamic_debug`               | `echo 'module <m> +p'`     |
| Confirm a raw register value      | `devmem2` (read)              | peek physical address      |
| Slow function / CPU hotspot       | `perf record -g` + flamegraph | call graph profile         |
| Kernel driver timing / call order | `ftrace function_graph`       | function graph tracer      |
| Step through kernel code          | `kgdb` + cross-gdb            | `kgdboc`, `kgdbwait`       |
| Remote userspace stepping         | `gdbserver` + cross-gdb       | `target remote`            |
| Kernel panic post-mortem          | `crash`                       | `bt -a`, `log`             |
| Hardware event counting           | `perf stat`                   | cache-misses, instructions |
