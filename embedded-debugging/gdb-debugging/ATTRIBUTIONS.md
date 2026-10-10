# Attributions

## Current skill

- Skill: `gdb-debugging`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: original text; two components adapted from upstream

## Adapted components

- Upstream: [mohitmishra786/low-level-dev-skills](https://github.com/mohitmishra786/low-level-dev-skills), skills
  `skills/debuggers/gdb/` and `skills/debuggers/lldb/`, revision `bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608`, read
  2026-09-30.
- Upstream license: MIT, Copyright (c) 2026 chessMan; the full text is in [LICENSE.upstream](LICENSE.upstream).
- From the `gdb` skill: the batch-mode invocation, the `gdbserver` and `--attach` pattern, and the breakpoint
  `commands ... silent ... continue` logging pattern, all reworked for remote embedded targets.
- From the `lldb` skill: the idea of a GDB-to-LLDB command table. Its rows were not carried over, because several
  were wrong (`bt full`, `fr v -a`, `set scheduler-locking`); every row here comes from LLDB's official map or its
  source at LLVM 23.1.2.

## Sources whose reading shaped the skill

No text was copied from these; facts are restated with their source named in the references.

- The GDB manual and source at `gdb-18.1-release`, LLDB's documentation and source at `llvmorg-23.1.2`, Debian's
  `gdb-multiarch` build rules, Rust's `src/etc/rust-gdb` at 1.98.1, and the Arm Cortex-M0, M0+, M3, M4, M7, and M33
  Technical Reference Manuals for the breakpoint and watchpoint counts.

The research notes, with URLs and commits, are in agent-setup's `docs/research/embedded-debugging/`.
