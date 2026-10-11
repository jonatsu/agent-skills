# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## First-party Sources

### Arm: Cortex-M documentation

- Source: <https://developer.arm.com/documentation/dui0646/c> (Cortex-M7 Generic User Guide),
  <https://developer.arm.com/documentation/100235/0100> (Cortex-M33 Generic User Guide),
  <https://developer.arm.com/documentation/ddi0439/b> (Cortex-M4 Technical Reference Manual), and
  <https://developer.arm.com/documentation/dui0662/b> (Cortex-M0+ Generic User Guide)
- License: `LicenseRef-Proprietary`
- Version: Cortex-M7 Generic User Guide r1p2 (DUI 0646C), Cortex-M4 TRM r0p0 (DDI 0439B), Cortex-M0+ Generic User Guide
  (DUI 0662B), Cortex-M33 Generic User Guide (100235 0100)

The Arm documents are proprietary, so all rights remain with Arm. They supplied the fault register addresses and bit
layouts, the stacked frame and `EXC_RETURN` values, and the Armv8-M and Armv6-M differences in
`references/cortex-m-faults.md`. Nothing was copied.

### Espressif: ESP-IDF

- Source: <https://github.com/espressif/esp-idf>, `docs/en/api-guides/fatal-errors.rst`,
  `docs/en/api-guides/tools/idf-monitor.rst`, and `docs/en/api-guides/core_dump.rst`
- License: `Apache-2.0`
- Version: `v6.1`

The ESP32 panic output, IDF Monitor, and core-dump guidance in `references/esp32-and-riscv.md` is built on these guides.
Facts are restated in original words; nothing was copied.

### SEGGER: Real Time Transfer

- Source: <https://github.com/SEGGERMicro/RTT>, `RTT/SEGGER_RTT.h` and `RTT/SEGGER_RTT.c`
- License: `BSD-1-Clause`
- Version: `V8.58`

The RTT section of `references/logging-channels.md` is built on the control block layout and buffer behavior in the
source. Nothing was copied.

## Third-party Sources

### royforlinux: openocd-mcu-mcp

- Source: <https://github.com/royforlinux/openocd-mcu-mcp>
- License: `MIT`
- Version: `a930c2a17eff1a8875496f2d876b70bc17cddfb6`

The repository's diagnosis playbooks supplied the idea of organizing fault triage by symptom. Nothing was copied.
