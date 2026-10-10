# Attributions

## Current skill

- Skill: `debug-server-tools`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: original text; one component adapted from upstream

## Adapted component

- Upstream: [mohitmishra786/low-level-dev-skills](https://github.com/mohitmishra786/low-level-dev-skills), skill
  `skills/embedded/openocd-jtag/`, revision `bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608`, read 2026-09-30.
- Upstream license: MIT, Copyright (c) 2026 chessMan; the full text is in [LICENSE.upstream](LICENSE.upstream).
- Adapted into `references/openocd.md`: the script-mode `program ... verify reset exit` pattern with an address for
  raw binaries, the distinction between `reset run`, `reset halt`, and `reset init`, and the shape of an
  error-message section. The upstream's error table was not carried over, because several of its messages are not
  ones OpenOCD prints; the messages here come from OpenOCD's sources and documentation.

## Sources whose reading shaped the skill

No text was copied from these; facts are restated with their source named in each reference.

- OpenOCD's `doc/openocd.texi` and `tcl/` (master `21f88d78` and release 0.12.0), pyOCD 0.45.1's subcommands and
  `docs/`, probe-rs 0.32.0's `probe-rs-tools` and <https://probe.rs/docs/>, Espressif's ESP-IDF JTAG guide and
  `openocd-esp32`, and SEGGER's J-Link GDB Server knowledge-base page.
- [a5c-ai/babysitter](https://github.com/a5c-ai/babysitter), skill `jtag-swd-debug` (MIT, revision
  `feb68abe397acc14f32b34984975c48fedba2b33`): read as a reference; it lists capabilities without procedures, and
  nothing from it was used.

The research notes, with URLs and commits, are in agent-setup's `docs/research/embedded-debugging/`.
