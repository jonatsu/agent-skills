# LLDB for Embedded and Remote Targets

Checked 2026-09-30 against LLDB's command map (<https://lldb.llvm.org/use/map.html>) and source at LLVM 23.1.2. Rows
the official map lacks are marked "from source" and were read from LLDB's option definitions; confirm them with
`help <command>` in the installed LLDB.

## What LLDB Cannot Do Here

LLDB has no flash `load`. `target modules load --load` writes a file's sections into target memory, which works for
RAM but not flash, and `process load` loads a shared library into a running process. Flash through the debug server
or its own programmer (see `debug-server-tools`), then attach LLDB.

## Connecting

- A debug server's GDB port: `gdb-remote 3333`, or `gdb-remote host:port`. It is shorthand for
  `process connect --plugin gdb-remote connect://host:port`, with the host defaulting to `localhost`.
- A bare-metal ELF: `target create build/firmware.elf`, then `gdb-remote <port>`.
- Server commands: `process plugin packet monitor <command>` sends what GDB's `monitor` sends.
- Embedded Linux, one process: on the target run `lldb-server gdbserver :1234 /usr/bin/app`, then on the host
  `gdb-remote <board-ip>:1234`.
- Embedded Linux, a remote platform: on the target `lldb-server platform --listen "*:1234" --server`; on the host
  `platform select --sysroot <sdk-sysroot> remote-linux`, then `platform connect connect://<board-ip>:1234`. The
  `--sysroot` option is LLDB's nearest match to GDB's `set sysroot`.
- A core file: `target create --core <core> <elf>`.
- Path mapping: `settings set target.source-map <build-prefix> <local-prefix>` does what GDB's
  `set substitute-path` does; `target.exec-search-paths` and `target.debug-file-search-paths` find binaries and
  separate debug info.

## Command Map

| GDB                          | LLDB                                                                        |
| ---------------------------- | --------------------------------------------------------------------------- |
| `break main`                 | `breakpoint set --name main`, short `b main`                                |
| `break file.c:12`            | `breakpoint set --file file.c --line 12`, short `b file.c:12`               |
| `hbreak main`                | `breakpoint set --hardware --name main` (from source)                       |
| `tbreak main`                | `tbreak main`; `breakpoint modify --one-shot true <id>` for an existing one |
| `watch var`                  | `watchpoint set variable var`                                               |
| `watch -location expr`       | `watchpoint set expression -- expr`, with `-s <bytes>` for the size         |
| `rwatch var` / `awatch var`  | `watchpoint set variable -w read var` / `-w read_write var` (from source)   |
| `run`                        | `process launch`, short `run`                                               |
| `continue`                   | `process continue`, short `c`                                               |
| `step` / `next`              | `thread step-in` / `thread step-over`, short `s` / `n`                      |
| `stepi` / `nexti`            | `thread step-inst` / `thread step-inst-over`, short `si` / `ni`             |
| `finish`                     | `thread step-out`, short `finish`                                           |
| `bt`                         | `thread backtrace`, short `bt`; `bt all` for every thread                   |
| `bt full`                    | no single command: `bt`, then `frame variable` in each frame of interest    |
| `info registers`             | `register read`                                                             |
| `x/4xw addr`                 | `memory read --size 4 --format x --count 4 addr`, or `x/4xw addr`           |
| `info frame`                 | `frame info`                                                                |
| `info args` + `info locals`  | `frame variable`, short `fr v`                                              |
| `info locals`                | `frame variable --no-args`, short `fr v -a`                                 |
| `info sharedlibrary`         | `image list`                                                                |
| `target remote host:port`    | `gdb-remote host:port`                                                      |
| `monitor cmd`                | `process plugin packet monitor cmd` (from source)                           |
| `set scheduler-locking step` | per step only: `thread step-in -m this-thread` (from source)                |

LLDB accepts GDB's `x/<count><format><size>` shorthand as long as no space follows `x`. It has no persistent
equivalent of `set scheduler-locking`; the `--run-mode` (`-m`) option on `thread step-in`, `step-over`, and `until`
takes `this-thread`, `all-threads`, or `while-stepping` (the default) for one step at a time.
