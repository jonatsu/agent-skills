# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## First-party Sources

### SEGGER: J-Link / J-Trace User Guide

- Source: <https://kb.segger.com/UM08001_J-Link_/_J-Trace_User_Guide> and its linked knowledge-base pages
- License: `LicenseRef-Proprietary`
- Version: J-Link software 9.80

The knowledge base states no open license, so all rights remain with SEGGER. It supplied the J-Link Base capabilities
and limits, and the order of the "J-Link cannot connect" checks, which `SKILL.md` and `references/jlink-base.md`
restate as a probe-neutral first-contact order. Nothing was copied.

### Raspberry Pi: debugprobe

- Source: <https://github.com/raspberrypi/debugprobe>, `include/board_*_config.h`
- License: `MIT`
- Version: `debugprobe-v2.3.1`

The firmware supplied the three build variants, the pin assignments for the Debug Probe hardware and for a plain Pico,
and the UART bridge behavior in `references/pico-debugprobe.md`. Nothing was copied.
