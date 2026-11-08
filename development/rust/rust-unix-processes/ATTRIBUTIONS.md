# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## First-party Sources

### Tokio Contributors: `tokio::process` and `tokio::signal` documentation

- Source: <https://docs.rs/tokio/1.54.1/tokio/>
- License: `MIT`
- Version: tokio 1.54.1

The signal registration and coalescing rules, child reaping and `kill_on_drop`, and the `stdin` limitation come
from this documentation. No prose or code was copied.

### Jesse Luehrs: pty-process

- Source: <https://git.tozt.net/pty-process>, <https://docs.rs/pty-process/0.5.4/pty_process/>
- License: `MIT`
- Version: 0.5.4

The pseudo-terminal setup, in which the child becomes a session leader with the pseudo-terminal as its
controlling terminal, comes from this crate's documentation. No prose or code was copied.

### The nix project: nix API documentation

- Source: <https://docs.rs/nix/0.31.3/nix/>
- License: `MIT`
- Version: 0.31.3

The signal, process-group, and terminal-settings calls come from this documentation, with the process behavior
confirmed by probes on Linux. No prose or code was copied.

### The rustix project: rustix API documentation

- Source: <https://docs.rs/rustix/1.1.6/rustix/>
- License: `Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT`
- Version: 1.1.6

The process-group and window-size calls named as alternatives come from this documentation. No prose or code
was copied.
