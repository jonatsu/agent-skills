# Attributions

## Current skill

- Skill: `mcu-firmware-debugging`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: original text

## Sources whose reading shaped the skill

No text was copied from these; facts are restated with their source named in each reference.

- Arm: the Cortex-M7 and Cortex-M33 Generic User Guides, the Cortex-M4 Technical Reference Manual, the Cortex-M0+
  Generic User Guide, CMSIS 6's core headers, and the Arm semihosting specification (ARM-software/abi-aa).
- Vendor headers and SDKs: STMicroelectronics' `cmsis_device_f4` and `cmsis_device_h7`, Nordic's nrfx 4.6.0,
  Raspberry Pi's pico-sdk 2.3.1 and RP2350 datasheet, and ESP-IDF 6.1's fatal-errors, IDF Monitor, and core-dump
  guides.
- SEGGER RTT 8.58, OpenOCD master's `src/rtos/` and manual, FreeRTOS-Kernel 11.3.1, Zephyr 4.4.2, defmt 1.1.1,
  probe-rs 0.32.0, and the RISC-V privileged specification.
- [royforlinux/openocd-mcu-mcp](https://github.com/royforlinux/openocd-mcu-mcp): its diagnosis playbooks were read
  as an idea source for organising fault triage by symptom; no text or code was used.

The research notes, with URLs and commits, are in agent-setup's `docs/research/embedded-debugging/`.
