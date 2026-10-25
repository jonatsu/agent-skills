# OWASP FSTM stage 8: runtime analysis

Stage 8 goes past what static analysis can show by reaching a running process's memory and execution flow directly, on\
real hardware with administrator or debug access, or in a purpose-built virtual environment. Without either, a\
chroot-based environment carrying every needed tool, file, and library can substitute, at the cost of being slower to\
build and more error-prone. Distilled from [Tarlogic's stage 8 write-up][source] (part of the OWASP FSTM series).

Three technique families cover this stage: **instrumentation and debugging** (inspecting memory and controlling flow\
via breakpoints, sometimes by injecting extra code the target does not itself run), **tracing** (logging the system\
calls and events a process makes), and **logging** (reading whatever the executable already writes out, the least\
informative of the three but sometimes the only one available).

## Hardware debuggers

JTAG (IEEE 1149) is the most common hardware debug interface; a compliant device exposes `TCK` (clock), `TMS`\
(debug-port state), `TDI`/`TDO` (instruction and data in/out), and, when the debug port's post-startup state is\
undetermined, `TRST*` (reset it to resynchronize). Common options, cheapest and most open-source-friendly last:

| Debugger                 | Targets                              | Software                          |
| ------------------------ | ------------------------------------ | --------------------------------- |
| Segger J-Link            | ARM v7/v8, mainly Cortex-M           | Proprietary, widely IDE-supported |
| Microchip ICP (PICkit)   | 8/16/32-bit PIC, DSP                 | Proprietary                       |
| TI TMDSEMU110-U (XDS110) | ARM v7/v8/v9, Cortex-A/R/M           | Proprietary                       |
| ST-Link                  | ARM v6/v7/v8 Cortex-M/R (ST parts)   | Open or closed; J-Link or OpenOCD |
| FTDI FT2232HX            | Reconfigurable JTAG/USART/I2C/SPI    | Open-source OpenOCD               |
| Bus Pirate               | USART/JTAG/SPI/I2C, ARM v7/PIC/Atmel | Open-source OCSP                  |

## Software debuggers

A hardware debugger pairs two independent pieces of software: the adapter's own driver (converting raw hardware packets\
into frames) and a separate debugger front-end, most often GDB, consuming those frames; configure each separately. GDB\
supports real-time instrumentation of nearly any target, standalone firmware or a process inside a running OS, and has\
GUI/TUI front-ends for most editors and IDEs (Eclipse CDT, CLion, KDevelop, Qt Creator, Emacs, and others). [PEDA]\
extends GDB specifically for binary analysis and exploit development: memory coloring and disassembly display, plus\
commands such as `patch` (write to memory), `pattern` (generate or search a cyclic pattern), `ropgadget`/`ropsearch`,\
and `searchmem`/`find`.

Worked example: an STM32F3xx-based (ARM Cortex-M4) device was studied via a NUCLEO-F303RE development board carrying\
the same core, driven by the open-source OpenOCD debugger with GDB attached.

```
$ openocd -f interface/stlink.cfg -f board/st_nucleo_f3.cfg   # OpenOCD defaults to port 3333
$ gdb-multiarch
(gdb) target remote :3333
```

With the manufacturer's datasheet confirming RAM starts at `0x20000000`, that region can be inspected directly. Without\
symbols, the basic commands (`step`, `next`, `continue`, `disas`, `nexti`, `break`, `stepi`) still support real-time\
tracing, though it takes more practice than working with symbol information.

## Frida and Qiling

[Frida] injects JavaScript or a native library into a running application on Windows, macOS, Linux, iOS, Android, or\
QNX; common uses are function tracing, spying on cryptographic API calls, and tracing application logic without source,\
which suits black-box analysis particularly well. Qiling (introduced in [stage 6][stage-6]) doubles as an\
instrumentation platform in this stage: its scripted API sets the emulation parameters (target binary, argv, root\
filesystem, verbosity) declaratively, then drives execution, optionally attaching an external debugger or invoking AFL\
from the same script.

## Tracing and logging

`strace` (via the kernel's `ptrace` facility) is the default tool for a process's system calls:\
`strace -o out.txt <command>` reveals, for example, a lookup against `/etc/passwd` and a write to stdout, without any\
deeper debugging session. `ftrace`, reached through `trace-cmd` or `KernelShark`, extends the same idea to kernel\
events, interrupts, and MMIO tracing. Enabling kernel core dumps captures a crashed executable's state for later\
inspection with `gdb <executable> <core dump>`.

Choosing which executables and processes to spend this stage's (costly) analysis on should draw directly on\
[stages 3-7][stage-3]'s findings, prioritizing whatever they already flagged as most likely to hold a complex bug that\
static analysis alone could not surface.

## References

Distilled from OWASP FSTM / Tarlogic: [OWASP FSTM, step 8: Runtime analysis][source].

- [Frida] — the dynamic instrumentation toolkit.
- [longld/peda][peda] — Python Exploit Development Assistance for GDB.
- Qiling, ["Instrumenting IoT firmware"][qiling-intro] — Qiling's own introduction to using it as an instrumentation\
  platform.
- [trace-cmd] and [KernelShark] — userspace front ends for the kernel's `ftrace` facility.
- Microsoft Learn, ["Tracing and Instrumenting Applications"][ms-tracing] — background on the\
  instrumentation/tracing/logging distinction used above.

[frida]: https://frida.re/
[kernelshark]: https://kernelshark.org/
[ms-tracing]: https://learn.microsoft.com/dotnet/framework/debug-trace-profile/tracing-and-instrumenting-applications
[peda]: https://github.com/longld/peda
[qiling-intro]: https://qiling.io/2022/08/10/intro/
[source]: https://www.tarlogic.com/blog/owasp-fstm-runtime-analysis/
[stage-3]: 03-analyzing-firmware.md
[stage-6]: 06-firmware-emulation.md
[trace-cmd]: https://www.trace-cmd.org/
