# RTOS Awareness and Stack Checks

A light reference, checked 2026-09-30 against OpenOCD master (`src/rtos/`), FreeRTOS-Kernel 11.3.1, and Zephyr 4.4.2.

## Threads in the Debugger

OpenOCD presents RTOS tasks as GDB threads with `-rtos <name>` on the target, or `-rtos auto`. The names are compared
case-sensitively against the code's list, which differs from the manual in places: `FreeRTOS`, `Zephyr`, `ThreadX`,
`chibios` (lower case), `nuttx`, `RIOT`, `eCos`, `embKernel`, `mqx`, `uCOS-III`, `rtkernel`, `linux`, and
`hwthread`. A wrong name fails with an error listing the valid ones; trust that list. The firmware must keep the
symbols the driver reads.

- **FreeRTOS** needs `uxTopUsedPriority`, which recent kernels no longer provide: link OpenOCD's
  `contrib/rtos-helpers/FreeRTOS-openocd.c` and keep the symbol with `-Wl,--undefined=uxTopUsedPriority`. OpenOCD
  reads task control blocks at fixed offsets and supports only Cortex-M targets, so a configuration that adds fields
  before the task name shows garbled names. `configUSE_TRACE_FACILITY` is not what it needs.
- **Zephyr** needs `CONFIG_DEBUG_THREAD_INFO`, which is unavailable with SMP. OpenOCD looks up
  `_kernel_thread_info_offsets`; the manual's `_kernel_openocd_*` names and an error message's `CONFIG_OPENOCD` are
  out of date.
- probe-rs and the J-Link GDB Server have their own RTOS support; check their documentation for the RTOS in use.

## Stack Overflow

- **FreeRTOS:** `configCHECK_FOR_STACK_OVERFLOW` set to 1 checks the stack pointer against the limit at each context
  switch; 2 also checks that the stack's last words still hold the fill pattern `0xa5`. Both call
  `vApplicationStackOverflowHook(xTask, pcTaskName)`, which the application defines; keep it minimal, since the stack
  is already damaged. Neither catches every overflow. `uxTaskGetStackHighWaterMark()` returns the minimum free stack in
  words, with `INCLUDE_uxTaskGetStackHighWaterMark` set to 1. MPU ports disable these checks and rely on the MPU.
- **Zephyr:** `CONFIG_HW_STACK_PROTECTION` uses the Armv8-M stack-limit registers where the core has them, and an MPU
  guard (`CONFIG_MPU_STACK_GUARD`) otherwise. `CONFIG_STACK_SENTINEL` checks a magic value at the stack's bottom on
  context switches and interrupts, and cannot combine with an MPU guard or userspace. `CONFIG_THREAD_ANALYZER` reports
  each thread's stack use.
- A hardware stack-limit fault (`CFSR.STKOF`) may not stack a valid frame, so its reported PC is unreliable.
