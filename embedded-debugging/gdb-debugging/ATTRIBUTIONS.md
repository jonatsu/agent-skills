# Attributions

- Author: Joonas Onatsu
- License: `MIT`

The package adapts material from low-level-dev-skills, whose MIT license requires its notice to travel with the
material; keep `LICENSE.upstream` with the skill.

## First-party Sources

### The GDB developers: GDB

- Source: <https://sourceware.org/git/binutils-gdb.git>, `gdb/doc/gdb.texinfo` and the `gdb/` sources
- License: `GPL-3.0-or-later AND GFDL-1.3-or-later`
- Version: `gdb-18.1-release`

The guidance in `SKILL.md` is built on the manual and the source: connecting and loading, hardware breakpoint and
watchpoint limits and their error messages, reading optimized code, batch runs, and core dumps. Facts are restated in
original words; nothing was copied.

### The LLVM Project: LLDB

- Source: <https://github.com/llvm/llvm-project>, `lldb/docs/` and `lldb/source/`
- License: `Apache-2.0 WITH LLVM-exception`
- Version: `llvmorg-23.1.2`

`references/lldb.md` takes every row of its GDB-to-LLDB command table from LLDB's official command map or its source.
Nothing was copied.

## Third-party Sources

### mohitmishra786: low-level-dev-skills

- Source: <https://github.com/mohitmishra786/low-level-dev-skills>, `skills/debuggers/gdb/` and
  `skills/debuggers/lldb/`
- License: `MIT`
- Version: `bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608`

Adapted for remote embedded targets: the `gdb` skill's batch-mode invocation, its `gdbserver` and `--attach` pattern,
and its breakpoint `commands ... silent ... continue` logging pattern. The `lldb` skill supplied the idea of a
GDB-to-LLDB command table.
