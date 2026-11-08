---
name: rust-testing
description: Write, organize, and run tests for Rust crates. Use for unit and integration test layout, testing a binary's exit codes and output with assert_cmd, async tests with #[tokio::test] and paused time, parameterized tests with rstest, property tests with proptest, snapshots with insta, keeping slow tests that need real systems opt-in, and running tests with cargo nextest. Test strategy across languages belongs to test-engineer; test-first workflow to test-driven-development.
license: MIT
compatibility: Rust 1.85 or later (edition 2024).
metadata:
  author: Joonas Onatsu
---

# Rust Testing

How to lay out, write, and run tests in a Rust crate, with the crates that make each kind of test short. This
skill covers the Rust mechanics; deciding what to test belongs to `test-engineer`, and working test-first to
`test-driven-development`. The Rust skills cover their own subjects:

| Subject                                                  | Skill                 |
| -------------------------------------------------------- | --------------------- |
| Everyday style, lints, and moving logic into the library | `rust-style`          |
| Error types, and which variant a test should expect      | `rust-error-handling` |
| Tasks, cancellation, and shutdown under test             | `rust-async`          |
| Child processes and signals under test                   | `rust-unix-processes` |

Current known: assert_cmd 2.2.2, insta 1.49.0, rstest 0.28.0, proptest 1.12.0, tokio 1.54.1, and
cargo-nextest 0.9.151, checked on 2026-11-08 against their documentation and by running the examples on
Rust 1.99.1. proptest 1.12 needs Rust 1.88; on an older `rust-version`, Cargo's default resolver picks an older
proptest.

## Where Tests Live

- **Unit tests** sit in the file they test, in `#[cfg(test)] mod tests { use super::*; ... }`, and may test
  private items.
- **Integration tests** are files under `tests/`. Cargo builds each file as its own crate, which sees only the
  library's public API.
- **Shared helpers** for integration tests go in `tests/common/mod.rs`, imported with `mod common;`. A
  `tests/common.rs` file would itself become a test crate and show up in every run.
- **A binary's logic** belongs in `src/lib.rs`, because integration tests cannot import a binary crate. Test
  the binary itself as a program, as the next section shows.
- **Test-only code in the library**, marked `#[cfg(test)]`, is invisible to integration tests, which link the
  library built without `cfg(test)`. Put helpers that integration tests share in `tests/common/mod.rs`, or
  behind a non-default `test-support` feature.
- **Test-only crates** go in `[dev-dependencies]`, so they never reach the built program.

Return `Result` from a test to use `?`, such as `fn parses() -> Result<(), Box<dyn std::error::Error>>`. Use
`#[should_panic(expected = "...")]` only for a function whose contract is to panic; a returned error is tested
by matching it, for example with `assert!(matches!(error, ConfigError::UnknownKey { .. }))`.

Never call `std::env::set_var` in a test. It is `unsafe` in edition 2024, and `cargo test` runs tests on
parallel threads that share one environment. Pass configuration into the code under test, or set the variable
on a child process with `Command::env`.

## Testing a Binary's Contract

A command-line tool's exit statuses, its stdout and stderr, and its behavior without a terminal are its
contract. Test them by running the built binary from an integration test with `assert_cmd`. In a file under
`tests/`, `assert_cmd::cargo::cargo_bin_cmd!("tool-name")` gives a command for the crate's binary; cargo builds
the binary first and passes its path to the test.

Give each run a clean environment and a temporary directory, so the test does not read the developer's real
configuration: call `env_clear()`, set `HOME` and the `XDG_*` directories to a `tempfile::TempDir`, and add
back only what the binary needs, such as `PATH`. Bind the `TempDir` to a variable that lives for the whole
test, because dropping it deletes the directory; `TempDir::new()?.path()` is gone by the next statement.
Assert stdout and stderr separately, because a message on the wrong stream is a contract break.

```rust,run
#[cfg(test)]
mod tests {
    use assert_cmd::Command;
    use predicates::prelude::predicate;

    // In an integration test, use `assert_cmd::cargo::cargo_bin_cmd!("tool-name")`;
    // `sh` stands in for the binary here.
    fn tool() -> Command {
        let mut command = Command::new("sh");
        command.env_clear().env("PATH", "/usr/bin:/bin");
        command
    }

    #[test]
    fn usage_error_goes_to_stderr_with_status_2() {
        tool()
            .args(["-c", "echo 'error: unknown flag --frob' >&2; exit 2"])
            .assert()
            .code(2)
            .stdout(predicate::str::is_empty())
            .stderr(predicate::str::starts_with("error: unknown flag"));
    }

    #[test]
    fn result_goes_to_stdout() {
        tool().args(["-c", "echo ready"]).assert().success().stdout("ready\n");
    }
}
```

Test signal handling with a real process:

1. Spawn the binary with `std::process::Command::new(assert_cmd::cargo::cargo_bin!("tool-name"))`, with
   stdout piped.
2. Wait until the binary reports that it is ready, by reading a readiness line from its stdout. A `sleep`
   instead races with the binary's startup and fails on a slow machine.
3. Send SIGTERM with `nix::sys::signal::kill`.
4. Wait for the exit with a deadline by polling `try_wait`, since std has no timed wait, and kill the child if
   the deadline passes. Assert how it ended: a wrapper that exits 143 has `code() == Some(143)`, and a process
   that dies from the signal has `signal() == Some(15)` instead. Then assert the cleanup.

The `rust-unix-processes` skill covers the statuses a wrapper must return.

## Async Tests

`#[tokio::test]` runs each test on its own current-thread runtime, so spawned tasks interleave on one thread.
Use `#[tokio::test(flavor = "multi_thread")]` when the test needs real parallelism; it needs tokio's
`rt-multi-thread` feature.

`#[tokio::test(start_paused = true)]` starts the clock paused, and the runtime then jumps time forward
whenever it has no work to do, so a test of a 30-second timeout finishes at once. It needs tokio's `test-util`
feature in `[dev-dependencies]` and works only with the current-thread runtime.

Waiting on real I/O, such as a child process or a socket, also leaves the runtime with no work, so time jumps
forward and a timeout around that wait fires at once. Use paused time only for code that waits on tokio's
timers and channels. Test real processes and connections on a running clock, with generous timeouts.

```rust,run
use std::time::Duration;

pub async fn wait_or_give_up(work: impl Future<Output = u32>) -> Option<u32> {
    tokio::time::timeout(Duration::from_secs(30), work).await.ok()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test(start_paused = true)]
    async fn gives_up_after_thirty_seconds() {
        let started = tokio::time::Instant::now();
        assert_eq!(wait_or_give_up(std::future::pending()).await, None);
        assert_eq!(started.elapsed(), Duration::from_secs(30));
    }
}
```

## Parameterized, Property, and Snapshot Tests

Use `rstest` cases when one behavior is checked against several inputs, so each case reports on its own:

```rust,run
pub fn exit_status_for_signal(signal: i32) -> i32 {
    128 + signal
}

#[cfg(test)]
mod tests {
    use rstest::rstest;

    use super::*;

    #[rstest]
    #[case::interrupt(2, 130)]
    #[case::terminate(15, 143)]
    #[case::kill(9, 137)]
    fn adds_128_to_the_signal(#[case] signal: i32, #[case] status: i32) {
        assert_eq!(exit_status_for_signal(signal), status);
    }
}
```

Use `proptest` for a property that must hold for every input, such as a parser that round-trips. When a case
fails, proptest shrinks it to a small input and records its seed. For a test under `src/`, the seed goes to
`proptest-regressions/<path>.txt`; for an integration test, to `tests/<name>.proptest-regressions` beside it.
Commit both, so the failing case runs again on every later test run.

```rust,run
pub fn escape(text: &str) -> String {
    text.replace('\\', "\\\\").replace(',', "\\,")
}

pub fn unescape(text: &str) -> String {
    let mut output = String::new();
    let mut characters = text.chars();
    while let Some(character) = characters.next() {
        if character == '\\' {
            output.extend(characters.next());
        } else {
            output.push(character);
        }
    }
    output
}

#[cfg(test)]
mod tests {
    use proptest::prelude::*;

    use super::*;

    proptest! {
        #[test]
        fn unescape_reverses_escape(text in ".*") {
            prop_assert_eq!(unescape(&escape(&text)), text);
        }
    }
}
```

Use `insta` snapshots for output that is long or structured, such as help text or a JSON report. Review a
changed snapshot with `cargo insta review`, from the separately installed `cargo-insta` tool, before accepting
it. In CI, insta writes no snapshot files and fails on any difference. Snapshot only output that is
deterministic: replace timestamps, temporary paths, and process IDs first. Insta's `filters` feature does this
for text such as help output, and its `redactions` feature for serialized values; enable each in `Cargo.toml`.

```rust,run
pub fn usage() -> String {
    ["Usage: tool <command>", "", "Commands:", "  run   Start a sandbox", "  list  List sandboxes"].join("\n")
}

#[cfg(test)]
mod tests {
    #[test]
    fn usage_lists_every_command() {
        insta::assert_snapshot!(super::usage(), @r"
        Usage: tool <command>

        Commands:
          run   Start a sandbox
          list  List sandboxes
        ");
    }
}
```

Prefer a small hand-written fake that implements the trait over a mocking framework such as `mockall`. A fake
keeps working when the call order changes, and it reads like the real implementation. For code that talks
HTTP, such as a proxy, run a real local server with `wiremock` and point the code under test at its address.

Show readable diffs for failed comparisons of long values with `pretty_assertions::assert_eq`. Mark tests that
share process state, such as the working directory, with `serial_test`'s `#[serial]`, so they do not run at the
same time; nextest already runs each test in its own process.

## Slow Tests That Need Real Systems

Keep the default test run fast and runnable anywhere. Mark a test that needs a real system, such as KVM,
Podman, or the network, with `#[ignore = "needs /dev/kvm"]`. The reason shows in the test output, and the test
runs only when asked:

```text
cargo test -- --ignored                     # only the ignored tests
cargo test -- --include-ignored             # everything
cargo nextest run --run-ignored only        # the same with nextest
cargo nextest run --run-ignored all         # everything
```

Run the slow tests in a CI job on a machine that has those systems, so they still run on every change.

## Running Tests

`cargo nextest run` runs each test in its own process and in parallel, which isolates crashes and global state
and reports slow tests. It does not run doctests, so a project that uses nextest also runs `cargo test --doc`.
Configure timeouts, retries, and test groups in `.config/nextest.toml`. `cargo test` hides a passing test's
output; pass `-- --no-capture` to see it.

Measure line coverage with `cargo llvm-cov`, and fail CI under a floor with `--fail-under-lines`. Coverage
shows which lines no test runs, not whether the tests check the right results.
