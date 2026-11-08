---
name: rust-error-handling
description: Design how Rust code fails and reports errors. Use when defining error types with thiserror, choosing between thiserror and anyhow, adding context to ? propagation, writing error messages, validating configuration or input at a boundary with serde, or turning errors into a binary's exit codes and stderr report. Panics and expect belong to rust-style; errors inside async tasks also touch rust-async.
license: MIT
compatibility: Rust 1.85 or later (edition 2024), with thiserror 2 and anyhow 1.
metadata:
  author: Joonas Onatsu
---

# Rust Error Handling

How Rust code reports failure: the error types a module returns, the context each layer adds, and the
message and exit status a person or script finally sees. Other subjects have their own skills:

| Subject                                   | Skill                 |
| ----------------------------------------- | --------------------- |
| Panics, `expect`, and everyday style      | `rust-style`          |
| `JoinError` and failures in spawned tasks | `rust-async`          |
| A wrapped child's exit status and signals | `rust-unix-processes` |
| Testing error variants and error output   | `rust-testing`        |

Current known: thiserror 2.0.21 and anyhow 1.0.104, checked on 2026-11-08 against their documentation and
probes on Rust 1.99.1.

## Choose the Error Type by Its Caller

Ask what the caller does with the error. When callers act differently depending on what failed, give them an
enum they can match: define it with `thiserror`, one variant per distinct action, and keep the variants'
fields to what the caller needs. When every caller only reports the error, use `anyhow::Error` and add
context instead.

So a library crate, or a module whose callers branch on the failure, returns its own `thiserror` enum. A
binary's command handlers and `main`, which only report, use `anyhow::Result`. Never return `anyhow::Error`
or `Box<dyn Error>` from a library's public API, because the caller can no longer match on the cause.

## Write Each Message Once

Every error in a chain contributes one message, and a reporter prints them in order, outermost first. Each
message describes only its own layer: "reading config /etc/app.toml", not "reading config: permission
denied". Write messages as lowercase phrases without trailing punctuation, as the `std::error::Error`
documentation recommends, so they join cleanly with `: `.

In `thiserror`, `#[from]` makes a field the error's `source`. Interpolating that same field in the `#[error]`
message prints the cause twice, once in your message and once as the next link in the chain:

```rust,run
use std::io;

#[derive(Debug, thiserror::Error)]
enum Doubled {
    #[error("reading config: {0}")]
    Read(#[from] io::Error),
}

#[derive(Debug, thiserror::Error)]
enum Once {
    #[error("reading config")]
    Read(#[from] io::Error),
}

fn main() {
    let doubled = anyhow::Error::from(Doubled::from(io::Error::other("disk gone")));
    assert_eq!(format!("{doubled:#}"), "reading config: disk gone: disk gone");

    let once = anyhow::Error::from(Once::from(io::Error::other("disk gone")));
    assert_eq!(format!("{once:#}"), "reading config: disk gone");
}
```

Use `#[error(transparent)]` for a variant that forwards another error unchanged, adding no message of its own.

## Add the Context the Cause Lacks

A low-level error rarely says what was being done. `std::io::Error` carries no path, so "No such file or
directory" alone does not say which file. Add the missing facts where they are known:

- With anyhow, call `.with_context(|| format!("reading {}", path.display()))` on the `Result`. The closure runs
  only on failure; use `.context("...")` for a fixed message.
- With thiserror, give the variant the facts as fields and the cause as a `#[source]` field, such as
  `#[error("reading {path}")] Read { path: PathBuf, #[source] source: io::Error }`. Use `#[from]` only when
  the conversion needs no extra facts, because a `From` conversion cannot supply them.

Add context once per layer that knows something new. Repeating the same fact at every `?` makes the chain
repeat itself.

## Validate at the Boundary

Turn untrusted input into checked types where it enters the program, so the code behind the boundary handles
only valid values. For configuration read with serde:

- Put `#[serde(deny_unknown_fields)]` on every configuration struct, so a misspelled key is an error rather
  than a silently ignored setting. toml reports the key's line and column, and the expected names.
- Deserialize a constrained value straight into its checked type with `#[serde(try_from = "String")]` and a
  `TryFrom<String>` implementation, so an invalid value fails during parsing with your message.

```rust,run
use serde::Deserialize;

#[derive(Debug, Deserialize)]
#[serde(try_from = "String")]
struct Name(String);

impl TryFrom<String> for Name {
    type Error = String;

    fn try_from(text: String) -> Result<Self, Self::Error> {
        if text.is_empty() || text.contains('/') {
            return Err(format!("invalid name {text:?}: expected a non-empty name without '/'"));
        }
        Ok(Self(text))
    }
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
struct Config {
    name: Name,
}

fn main() {
    let config: Config = toml::from_str("name = \"work\"").expect("the config is valid");
    assert_eq!(config.name.0, "work");

    let typo = toml::from_str::<Config>("nmae = \"work\"").unwrap_err();
    assert!(typo.to_string().contains("unknown field `nmae`, expected `name`"));

    let invalid = toml::from_str::<Config>("name = \"a/b\"").unwrap_err();
    assert!(invalid.to_string().contains("invalid name \"a/b\""));
}
```

## Report at the Edge

A binary turns its error into two things: a message on stderr and an exit status. Returning `Err` from
`fn main() -> anyhow::Result<()>` prints `Error: ` with the `Debug` form and a "Caused by" list, then exits
with status 1. It adds a backtrace when `RUST_BACKTRACE=1` or `RUST_LIB_BACKTRACE=1` is set, and
`RUST_LIB_BACKTRACE=0` keeps error backtraces off. That suits a quick tool, but not a command-line tool with
documented exit statuses.

For such a tool, keep `main` small: run the program, and on error print `error: {error:#}` to stderr, which
joins the chain with `: `, and return the `ExitCode` that the error maps to. Some links, such as a toml parse
error, span several lines, which reads fine on a terminal. Map errors to statuses in one function, so every
failure path uses the same table, and use the tool's documented status as the fallback: 125 for a wrapper, as
`rust-unix-processes` describes.

Find what failed without losing it on the way:

- `error.downcast_ref::<YourError>()` finds your error through any number of anyhow `.context()` layers.
- It does not find a cause stored as another error's `#[source]` field. Reach that cause through the outer
  variant, as the example does, or search the whole chain with
  `error.chain().find_map(|cause| cause.downcast_ref::<io::Error>())`. A chain search matches any `io::Error`,
  such as a missing configuration file, so classify a spawn failure by its own variant.
- `#[error(transparent)]` hides the inner type from both, so match the outer enum.
- Attach a cause with `.context()` or a `#[source]` field. Formatting it into `anyhow!("...: {cause}")` turns
  it into text, and no downcast finds it again.

```rust,run
use std::io;
use std::process::{Command, ExitCode};

use anyhow::Context;

#[derive(Debug, thiserror::Error)]
enum LaunchError {
    #[error("unknown sandbox {0:?}")]
    UnknownSandbox(String),
    #[error("starting {program}")]
    Spawn {
        program: String,
        #[source]
        source: io::Error,
    },
}

fn launch(name: &str, program: &str) -> anyhow::Result<()> {
    if name != "default" {
        return Err(LaunchError::UnknownSandbox(name.to_owned()).into());
    }
    Command::new(program)
        .status()
        .map_err(|source| LaunchError::Spawn { program: program.to_owned(), source })
        .with_context(|| format!("launching sandbox {name}"))?;
    Ok(())
}

/// The documented exit status of each failure; a spawn failure is classified by its own cause only.
fn exit_code(error: &anyhow::Error) -> ExitCode {
    match error.downcast_ref::<LaunchError>() {
        Some(LaunchError::UnknownSandbox(_)) => ExitCode::from(2),
        Some(LaunchError::Spawn { source, .. }) => match source.kind() {
            io::ErrorKind::NotFound => ExitCode::from(127),
            io::ErrorKind::PermissionDenied => ExitCode::from(126),
            _ if source.raw_os_error() == Some(nix::libc::ENOEXEC) => ExitCode::from(126),
            _ => ExitCode::from(125),
        },
        None => ExitCode::from(125),
    }
}

fn report(result: anyhow::Result<()>) -> (String, ExitCode) {
    match result {
        Ok(()) => (String::new(), ExitCode::SUCCESS),
        Err(error) => (format!("error: {error:#}"), exit_code(&error)),
    }
}

fn main() {
    let (message, code) = report(launch("other", "true"));
    assert_eq!(message, "error: unknown sandbox \"other\"");
    assert_eq!(code, ExitCode::from(2));

    let (message, code) = report(launch("default", "/nonexistent/tool"));
    assert!(message.starts_with("error: launching sandbox default: starting /nonexistent/tool: "));
    assert_eq!(code, ExitCode::from(127));
}
```

A real `main` prints the message with `eprintln!` and returns the code.

With clap, a parse error is not always a usage error: `--help` and `--version` also arrive as `Err` from
`try_parse`. Call `error.exit()` on a clap error, which prints it and exits 0 for help and version and 2 for
misuse, before any guard that must run on exit exists, because it calls `process::exit`. Otherwise call
`error.print()` and return `error.exit_code()`, rather than mapping every clap error to 2.

Keep secrets out of error values. An error variant that carries a token, a password, or a whole configuration
value prints it through `Display` or `Debug` into logs and terminals.

## Errors Across Tasks and Threads

An error that crosses a thread or a `tokio::spawn` must be `Send + Sync + 'static`. `anyhow::Error` already
is, and a `thiserror` enum is when its fields are. Awaiting a task's handle yields
`Result<Result<T, E>, JoinError>`; `handle.await??` propagates both, since `JoinError` converts into
`anyhow::Error`. After `??`, a panic in the task is an ordinary `anyhow::Error`; tell it apart with
`error.downcast_ref::<JoinError>()` and `is_panic`, or handle the `JoinError` before converting it, as
`rust-async` describes.

A `Box<dyn Error + Send + Sync>` does not convert into `anyhow::Error` with `?`. Convert it with
`.map_err(anyhow::Error::from_boxed)`.
