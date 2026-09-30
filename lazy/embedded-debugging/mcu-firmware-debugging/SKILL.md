---
name: mcu-firmware-debugging
description: "Find why MCU firmware crashes, hangs, or misbehaves: Cortex-M HardFault and fault-status analysis, stack overflow, watchdog and low-power resets, ESP32 panics and RISC-V exceptions, and logging through RTT, SWO, semihosting, or defmt. Use when firmware faults, resets, locks up, or needs output without a UART, on bare metal, Zephyr, or FreeRTOS. Probe, server, and GDB mechanics belong to debug-hardware, debug-server-tools, and gdb-debugging."
license: MIT
compatibility: Needs the firmware's ELF with debug symbols and, for live analysis, a debug probe and server; the target families covered are Cortex-M, ESP32, and RISC-V MCUs.
metadata:
  author: Joonas Onatsu
---

# MCU Firmware Debugging

Explain a firmware failure from the target's own state: fault registers, the stacked exception frame, reset-cause
flags, and a log. Connecting belongs to `debug-hardware` and `debug-server-tools`, and GDB commands to
`gdb-debugging`; the general method of hypothesis and test is `systematic-debugging`'s.

Reading registers and memory is free. Writing a fault register to clear it, or changing firmware configuration to add
logging, changes the device and the evidence; capture first, then change.

## 1. Classify the Symptom

| Symptom                              | First question                                   | Section |
| ------------------------------------ | ------------------------------------------------ | ------- |
| Stops in a fault handler, or panics  | Which fault, at which instruction?               | 2 or 5  |
| Stops responding, core still running | Where is it looping, and what is it waiting for? | 3       |
| Resets by itself                     | What does the reset-cause register say?          | 3       |
| Runs, but output is wrong or missing | What does a log from the right place say?        | 4       |

Halt the core and read its state before resetting anything: a reset destroys the fault registers, and on RP2350 even a
debugger reset clears the watchdog's reason register.

## 2. Decode a Cortex-M Fault

On Armv7-M and Armv8-M Mainline (Cortex-M3, M4, M7, M33):

1. Read `CFSR` at `0xE000ED28` and `HFSR` at `0xE000ED2C`. `HFSR.FORCED` means a configurable fault escalated, and
   `CFSR` holds the real cause.
2. Read `MMFAR` or `BFAR` only when `CFSR`'s `MMARVALID` or `BFARVALID` bit is set; otherwise the address is stale.
3. Find the stacked frame: bit 2 of the exception's `EXC_RETURN` (in LR on handler entry) picks PSP (1) or MSP (0).
   The frame holds R0 to R3, R12, LR, PC, and xPSR in that order, so the faulting PC is the seventh word.
4. Load the ELF and resolve the stacked PC and LR to source lines, then read the instruction at that PC to see what it
   touched.

An `IMPRECISERR` bus fault has a stacked PC unrelated to the faulting store. On Cortex-M3 and M4 only, setting
`ACTLR.DISDEFWBUF` makes bus faults precise for a debugging session, at a speed cost; M7 and M33 have no such bit.

**Cortex-M0 and M0+ (Armv6-M)** have no `CFSR`, `HFSR`, `MMFAR`, or `BFAR`: every fault is a HardFault, and only the
stacked frame and the instruction at its PC say what happened. Decode that instruction and the registers it used.

The bit meanings, `EXC_RETURN` values, the FPU frame, and Armv8-M stack-limit faults are in
[references/cortex-m-faults.md](references/cortex-m-faults.md).

## 3. Hangs and Resets

- **Reset loops:** read the chip's reset-cause register before anything clears it: STM32 `RCC_CSR` or `RCC_RSR`,
  nRF52 `RESETREAS`, RP2040 `CHIP_RESET` and the watchdog `REASON`, RP2350 `POWMAN.CHIP_RESET`, or ESP-IDF's
  `esp_reset_reason()`. The reference gives addresses and bits. Some keep stale flags from earlier resets until
  cleared, so compare with what the firmware clears at boot.
- **A hang:** halt and read the PC. A loop in a fault handler is section 2. A loop polling a peripheral points at
  clocks, power, or an interrupt that never fires. A core in lockup (a fault inside a fault handler) executes nothing
  until reset or a debugger halt.
- **Stack overflow:** often shows as a fault in unrelated code, or a corrupted return address. On Armv8-M,
  `CFSR.STKOF` reports a stack-limit violation; otherwise use the RTOS's stack checks in
  [references/rtos.md](references/rtos.md), or fill the stack with a pattern and read its high-water mark.
- **Lost debug connection:** the firmware entered low power, disabled the debug pins, or reset; connect under reset
  (`debug-server-tools`).

## 4. Get Output Without a UART

Choose by what the probe and target support:

- **RTT** is the default: it rides on SWD, works with every probe here, and costs little. Keep SEGGER's default
  non-blocking mode; the blocking mode spins forever with no host reading, which looks like a hang.
- **defmt** for Rust: compressed logging decoded on the host from the ELF, usually over RTT with `probe-rs run`.
- **SWO/ITM** needs a J-Link (the Pico probe has no SWO) and a core with ITM; Cortex-M0 and M0+ have none.
- **Semihosting** routes I/O through the debugger, but a semihosting call with no debugger attached faults or
  locks up the core, and with a debugger that has semihosting off it halts. Remove it from firmware that runs
  unattended.

Setup, blocking modes, and the enable sequences are in
[references/logging-channels.md](references/logging-channels.md).

## 5. ESP32 and RISC-V

An ESP32 panic prints a `Guru Meditation Error` line with its cause, a register dump, and a `Backtrace:` of `PC:SP`
pairs; `idf.py monitor` decodes it, as does `addr2line` for the chip's toolchain. A core dump or the panic GDB stub
gives more. A RISC-V exception reports its cause in `mcause` and the instruction in `mepc`; on the RP2350's Hazard3
cores `mtval` is always zero, so the faulting address must be recomputed from the instruction and registers. Both are
in [references/esp32-and-riscv.md](references/esp32-and-riscv.md).

The work is done when the cause is named from evidence: the fault class and instruction, the reset cause, or the log
lines that show the wrong behaviour, captured before any reset or change destroyed them.
