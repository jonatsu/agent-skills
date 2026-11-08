---
name: rust-unix-processes
description: Spawn, supervise, and wrap child processes from Rust on Linux and other Unix systems. Use for std or tokio Command, passing a child's exit status through, forwarding signals to a process group, SIGTERM and SIGINT handling, pseudo-terminals and raw terminal mode, window resizing, zombies, and pipe deadlocks, with nix, rustix, or pty-process. General async patterns belong to rust-async.
license: MIT
compatibility: Linux or another Unix; Rust 1.85 or later (edition 2024).
metadata:
  author: Joonas Onatsu
---

# Rust Unix Processes

Run and supervise other programs from Rust: start them, pass their terminal and signals through, and report
how they ended. Each step has a failure that compiles and looks fine until a user presses Ctrl-C, resizes a
window, or runs the tool from a script. Other subjects have their own skills:

| Subject                                               | Skill                 |
| ----------------------------------------------------- | --------------------- |
| Tasks, `select!`, cancellation, and shutdown on tokio | `rust-async`          |
| Error types and messages at the binary's edge         | `rust-error-handling` |
| Testing exit codes, streams, and signals of a command | `rust-testing`        |
| Everyday style, lints, and `unsafe_code = "forbid"`   | `rust-style`          |

Current known: nix 0.31.3, rustix 1.1.6, pty-process 0.5.4, and tokio 1.54.1, checked on 2026-11-08 against
their API documentation and probes on Linux. nix and rustix change their APIs between minor versions, so
confirm a signature on docs.rs for the version in `Cargo.lock`.

## Starting a Child

Build the command from a program and an argument list, never a shell string, so arguments reach the child
exactly as given. Set the child's environment with `Command::env`, `env_remove`, and `env_clear`. Never call
`std::env::set_var` for a child's benefit: it is `unsafe` in edition 2024, because it races with every other
thread that reads the environment.

The standard library opens every file descriptor with close-on-exec, so a child inherits only standard input,
output, and error, plus anything passed through `Stdio`. A Rust program ignores `SIGPIPE` from startup, and
`Command` restores the default handling in the child, so the child sees a normal broken pipe.

Map a spawn failure to the exit status shells use, so callers can tell the wrapper's failure from the
child's:

| Spawn error                                                         | Exit status |
| ------------------------------------------------------------------- | ----------- |
| `io::ErrorKind::NotFound` for the program itself                    | 127         |
| `io::ErrorKind::PermissionDenied`, or `raw_os_error()` is `ENOEXEC` | 126         |
| Any other failure before the child runs                             | 125         |

`NotFound` also covers a missing script interpreter (`#!/nonexistent/sh`) and a missing working directory.
Check that the program exists before spawning when the status must tell these apart, and report the missing
interpreter or directory as 126 or 125.

A child started through `pre_exec`, as pty-process does, never fails with `ENOEXEC`: the C library then retries
the file with `/bin/sh`, so a file without a shebang runs as a shell script, and a corrupt binary exits 127
through the shell. pty-process also wraps the error as `pty_process::Error::Io`, so read the `io::Error` from
that variant before classifying it.

## Waiting and Output

Every child must be waited for. An exited child that nobody waits for stays a zombie and holds a process slot.
Dropping a std `Child` neither kills nor waits for it, and leaves a zombie. tokio reaps a dropped child on a
best-effort basis, at some later time. `kill_on_drop(true)` on a tokio `Command` sends SIGKILL to the child's
own process ID when the handle is dropped, not to its children; stop the whole process group as the Signals
section describes.

Never wait for a child before draining its piped output. A child that fills the pipe buffer blocks on its next
write, and the parent blocks in `wait`, so both hang. Use `output()` or `wait_with_output()`, or read stdout and
stderr concurrently with the wait. Give the child `Stdio::null()` for any stream you do not read.

```rust,run
use std::process::Stdio;
use tokio::io::AsyncReadExt;
use tokio::process::Command;

#[tokio::main]
async fn main() -> std::io::Result<()> {
    let mut child = Command::new("sh")
        .args(["-c", "head -c 200000 /dev/zero; echo done >&2"])
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()?;
    let mut stdout = child.stdout.take().expect("stdout is piped");
    let mut stderr = child.stderr.take().expect("stderr is piped");
    let (mut out, mut err) = (Vec::new(), Vec::new());
    let (read_out, read_err, status) = tokio::join!(
        stdout.read_to_end(&mut out),
        stderr.read_to_end(&mut err),
        child.wait(),
    );
    read_out?;
    read_err?;
    assert!(status?.success());
    assert_eq!(out.len(), 200_000);
    assert_eq!(err, b"done\n");
    Ok(())
}
```

## Passing the Exit Status Through

A wrapper exits with its child's status, so callers see the child's result. `ExitStatus::code()` is `None`
when a signal killed the child; read the signal with `std::os::unix::process::ExitStatusExt::signal` and exit
with 128 plus its number, which is what shells report.

Return the status from `main` as `std::process::ExitCode` rather than calling `std::process::exit`.
`process::exit` skips every destructor, so a guard that restores the terminal or removes a temporary file
never runs.

```rust,run
use std::os::unix::process::ExitStatusExt;
use std::process::{Command, ExitCode, ExitStatus};

/// The status a wrapper exits with after its child ends.
fn passthrough_code(status: ExitStatus) -> u8 {
    if let Some(code) = status.code() {
        return u8::try_from(code).unwrap_or(1);
    }
    let signal = status.signal().expect("a child without an exit code was killed by a signal");
    u8::try_from(128 + signal).unwrap_or(1)
}

fn main() -> ExitCode {
    let killed = Command::new("sh").args(["-c", "kill -TERM $$"]).status();
    let killed = killed.expect("sh runs");
    assert_eq!(passthrough_code(killed), 143);

    let failed = Command::new("sh").args(["-c", "exit 3"]).status().expect("sh runs");
    assert_eq!(passthrough_code(failed), 3);
    ExitCode::SUCCESS
}
```

Dying by the same signal, instead of exiting with 128 plus its number, means resetting the signal's
disposition and raising it. For a signal the wrapper has registered a handler for, resetting needs an
`unsafe` call such as `nix::sys::signal::signal`, so a crate that forbids `unsafe` code exits with 128 plus the
number.

## Signals

Listen with `tokio::signal::unix::signal(SignalKind::terminate())` or `tokio::signal::ctrl_c()`. Registering
a signal replaces its default action for the rest of the process, even after the stream is dropped: a program
that listens for SIGINT or SIGTERM no longer dies from it, so it must stop and exit on its own. Several
deliveries of one signal may arrive as a single notification.

Register every signal you handle before you change any state that needs cleanup: before spawning the child
and before putting the terminal in raw mode. A signal that arrives before registration takes its default
action and kills the wrapper, leaving the child running and the terminal raw.

Choose where the child runs by how it uses the terminal:

- **The child never opens a terminal** (its stdin is null or piped, and it does not open `/dev/tty` itself,
  as ssh, sudo, and password prompts do): start it in its own process group with
  `Command::process_group(0)` and forward SIGINT, SIGTERM, SIGHUP, and SIGQUIT to that group.
- **The child gets its own pseudo-terminal**, as in the next section: it leads a new session and process
  group, so forward the same four signals to its group.
- **The child shares the caller's terminal**: keep it in the wrapper's process group. A process in another
  group on that terminal is a background job, and the kernel stops it as soon as it reads the terminal or
  changes its settings, so the wrapper would wait forever. The terminal already sends SIGINT and SIGQUIT for
  `Ctrl-C` and `Ctrl-\` to the whole foreground group, so forwarding them would deliver them twice. Still
  register SIGINT and SIGQUIT and discard them, or the first `Ctrl-C` kills the wrapper while the child keeps
  the terminal. Forward only SIGTERM and SIGHUP, to the child's process ID with `nix::sys::signal::kill`.

Send a signal to a group with `nix::sys::signal::killpg` or `rustix::process::kill_process_group`, so the
child's own children receive it too. The child's children can outlive it, and the group lives as long as any
member does, so after the child exits, stop what is left of its group: SIGTERM, a bounded wait, then SIGKILL.
`ESRCH` means the group is empty. For full containment of everything the child starts, also make the wrapper a
subreaper with `rustix::process::set_child_subreaper`, or run the child in a PID namespace. A subreaper inherits
the orphaned grandchildren, and tokio reaps only the children it spawned, so the wrapper must reap the group's
zombies itself: a group of zombies still exists, and `killpg` never reports `ESRCH` for it. The example's
`reap_group` does that.

```rust
use std::process::ExitStatus;
use std::time::Duration;

use nix::errno::Errno;
use nix::sys::signal::{Signal, killpg};
use nix::sys::wait::{WaitPidFlag, WaitStatus, waitpid};
use nix::unistd::Pid;
use tokio::signal::unix::{self as unix_signal, SignalKind};

/// Signal streams, registered before the child starts so that no early signal takes its default action.
pub struct Forwarded {
    interrupt: unix_signal::Signal,
    terminate: unix_signal::Signal,
    hangup: unix_signal::Signal,
    quit: unix_signal::Signal,
}

impl Forwarded {
    /// Registers the signals a wrapper forwards.
    ///
    /// # Errors
    ///
    /// Returns an error when a signal handler cannot be registered.
    pub fn register() -> std::io::Result<Self> {
        Ok(Self {
            interrupt: unix_signal::signal(SignalKind::interrupt())?,
            terminate: unix_signal::signal(SignalKind::terminate())?,
            hangup: unix_signal::signal(SignalKind::hangup())?,
            quit: unix_signal::signal(SignalKind::quit())?,
        })
    }
}

/// Forwards signals to a child that leads its own process group, then stops whatever the child left behind.
///
/// # Errors
///
/// Returns an error when waiting for the child fails.
pub async fn supervise(mut child: tokio::process::Child, signals: &mut Forwarded) -> std::io::Result<ExitStatus> {
    let id = child.id().expect("the child has not been waited for yet");
    let group = Pid::from_raw(i32::try_from(id).expect("process IDs fit in i32"));
    let status = loop {
        let forwarded = tokio::select! {
            status = child.wait() => break status?,
            _ = signals.interrupt.recv() => Signal::SIGINT,
            _ = signals.terminate.recv() => Signal::SIGTERM,
            _ = signals.hangup.recv() => Signal::SIGHUP,
            _ = signals.quit.recv() => Signal::SIGQUIT,
        };
        if let Err(error) = killpg(group, forwarded) {
            eprintln!("could not forward {forwarded}: {error}");
        }
    };
    stop_group(group).await;
    Ok(status)
}

/// Stops the rest of a process group: SIGTERM, up to five seconds of waiting, then SIGKILL.
async fn stop_group(group: Pid) {
    if killpg(group, Signal::SIGTERM) == Err(Errno::ESRCH) {
        return;
    }
    for _ in 0..50 {
        tokio::time::sleep(Duration::from_millis(100)).await;
        reap_group(group);
        if killpg(group, None) == Err(Errno::ESRCH) {
            return;
        }
    }
    if let Err(error) = killpg(group, Signal::SIGKILL) {
        eprintln!("could not stop process group {group}: {error}");
    }
}

/// Reaps exited members of the group that the wrapper inherited as a subreaper; tokio reaps only its own.
fn reap_group(group: Pid) {
    let members = Pid::from_raw(-group.as_raw());
    while let Ok(status) = waitpid(members, Some(WaitPidFlag::WNOHANG)) {
        if status == WaitStatus::StillAlive {
            break;
        }
    }
}
```

The child's process ID names its group only when it was started with `process_group(0)` or leads its own
session, as a child of pty-process does.

## Pseudo-Terminals

A child that expects a terminal, such as a shell or an editor, needs a pseudo-terminal whose secondary side is
its controlling terminal. That requires `setsid` and the `TIOCSCTTY` ioctl in the child between fork and exec,
which only `CommandExt::pre_exec` can run. `pre_exec` is `unsafe`, and its closure may call only
async-signal-safe functions: no allocation, no locks, no logging. In a crate that forbids `unsafe` code, use
the `pty-process` crate with its `async` feature, which does this setup and returns an ordinary
`tokio::process::Child`.

```rust,run
use tokio::io::AsyncReadExt;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let (mut pty, pts) = pty_process::open()?;
    pty.resize(pty_process::Size::new(24, 80))?;
    let mut child = pty_process::Command::new("sh")
        .args(["-c", "test -t 0 && echo on-a-terminal"])
        .spawn(pts)?;

    let mut output = Vec::new();
    let mut buffer = [0_u8; 1024];
    loop {
        match pty.read(&mut buffer).await {
            Ok(0) => break,
            Ok(read) => output.extend_from_slice(&buffer[..read]),
            // Linux reports EIO, not end of file, once the child side has closed.
            Err(error) if error.raw_os_error() == Some(nix::libc::EIO) => break,
            Err(error) => return Err(error.into()),
        }
    }
    assert!(child.wait().await?.success());
    assert!(String::from_utf8_lossy(&output).contains("on-a-terminal"));
    Ok(())
}
```

Passing a terminal through also needs these, each with its own failure when left out:

- **End of output.** Reading the primary side returns `EIO` on Linux after the child exits, as in the example.
  Treat it as the end of the stream. That happens only once every copy of the secondary side is closed:
  `spawn` consumes the `Pts`, but with `spawn_borrowed`, drop the `Pts` after spawning, or the read never
  ends. A grandchild that inherited the terminal also keeps it open after the child exits, so race the read
  loop against `child.wait()` rather than waiting for `EIO` alone.
- **Raw mode.** Put the caller's terminal in raw mode, so keystrokes such as `Ctrl-C` reach the child as
  bytes. Do it only when standard input is a terminal and the wrapper is its foreground process group, because
  changing the settings of a terminal from a background job, as in `launcher &`, stops the wrapper. Restore the
  saved settings in a `Drop` guard, and keep every exit path inside that guard's scope, because a terminal left
  in raw mode is unusable. The guard does not run under `panic = "abort"`, on SIGKILL, or on a signal the
  wrapper did not register, so register signals first. After SIGCONT, the shell may have restored its own
  settings, so apply raw mode again.
- **Window size.** Copy the caller's size to the pseudo-terminal at start and on every SIGWINCH: read it with
  `rustix::termios::tcgetwinsize` on standard input, and apply it with `Pty::resize`.
- **Reading the caller's input.** `tokio::io::stdin()` reads on a blocking thread that cannot be cancelled, so
  runtime shutdown can hang until the user presses Enter. Read interactive input on a dedicated
  `std::thread` and send it to the copy task over a channel.

```rust
use std::io::{self, IsTerminal};
use std::os::fd::AsFd;

use nix::errno::Errno;
use nix::sys::termios::{self, SetArg, Termios};
use nix::unistd;

/// Holds the caller's terminal in raw mode and restores it when dropped.
pub struct RawMode {
    saved: Termios,
}

impl RawMode {
    /// Enters raw mode, or returns `None` when standard input is not a terminal in the foreground.
    ///
    /// # Errors
    ///
    /// Returns an error when the terminal settings cannot be read or changed.
    pub fn enter() -> nix::Result<Option<Self>> {
        let stdin = io::stdin();
        if !stdin.is_terminal() {
            return Ok(None);
        }
        // ENOTTY: a terminal, but not this process's controlling terminal.
        match unistd::tcgetpgrp(stdin.as_fd()) {
            Ok(foreground) if foreground == unistd::getpgrp() => {}
            Ok(_) | Err(Errno::ENOTTY) => return Ok(None),
            Err(error) => return Err(error),
        }
        let saved = termios::tcgetattr(stdin.as_fd())?;
        let mut raw = saved.clone();
        termios::cfmakeraw(&mut raw);
        termios::tcsetattr(stdin.as_fd(), SetArg::TCSANOW, &raw)?;
        Ok(Some(Self { saved }))
    }
}

impl Drop for RawMode {
    fn drop(&mut self) {
        // Nothing useful can be done if restoring fails while dropping.
        let _ = termios::tcsetattr(io::stdin().as_fd(), SetArg::TCSANOW, &self.saved);
    }
}
```
