# Attributions

## Current skill

- Skill: `debug-hardware`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: original text

## Sources whose reading shaped the skill

No text was copied from any of these; facts are restated with their source named where the skill uses them.

- **SEGGER knowledge base** (<https://kb.segger.com/UM08001_J-Link_/_J-Trace_User_Guide> and linked pages, read
  2026-09-30): the J-Link Base facts, and the order of the "J-Link cannot connect" checks, which section 5 of
  `SKILL.md` and `references/jlink-base.md` adapt into a probe-neutral first-contact order.
- **raspberrypi/debugprobe** (MIT, tag `debugprobe-v2.3.1`) and Raspberry Pi's Debug Probe documentation: the
  firmware variants, pin assignments, and connector specification in `references/pico-debugprobe.md`.
- **Vendor documentation** for `references/target-connections.md`: the RP2040 and RP2350 datasheets, an ST
  Community article on STM32 readout protection, the nRF Connect SDK's AP-Protect documentation, ESP-IDF's JTAG
  debugging guide, Raspberry Pi's `config.txt` documentation, and probe.rs's Raspberry Pi page.

The research notes behind these, with URLs and commits, are in agent-setup's
`docs/research/embedded-debugging/`.
