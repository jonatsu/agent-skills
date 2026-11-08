# Evaluation: Rust Skills and the Design of the Rust Set

Date: 2026-11-08. The question was whether popular published Rust skills could serve a coming Rust project, or
whether to write our own. That project is a Linux command-line tool that launches sandboxed coding agents. It
uses tokio, two hyper and rustls proxies, clap, serde with TOML, and pseudo-terminal, signal and process-group
handling through nix or rustix. It needs no `unsafe` code of its own.

## Verdict

Adopt none of the six candidates, and write an independent set of five skills. Every candidate taught material
that is wrong for current Rust, and the errors cluster in the topics the project depends on: async cancellation
and shutdown, `Send` bounds, clippy and `[lints]` configuration, and test setup. No candidate covers Unix
processes, pseudo-terminals or signals. Each one contributes a few ideas, listed below, to be rewritten and
checked against official documentation rather than copied.

## Candidates

All six are MIT-licensed. Each was reviewed with `skill-forge` review mode at review-lite depth, without model
runs. Five reviews compiled a sample of the examples with Rust 1.99.1 and edition 2024; the apollographql
review checked by reading against official documentation only.

| Skill                                                                | Commit    | Verdict                       | Use        |
| -------------------------------------------------------------------- | --------- | ----------------------------- | ---------- |
| `rust-best-practices` from <https://github.com/apollographql/skills> | `9dda139` | not ready                     | ideas only |
| `rust-patterns` from <https://github.com/affaan-m/ECC>               | `d2ef268` | invalid as shipped, not ready | ideas only |
| `rust-testing` from <https://github.com/affaan-m/ECC>                | `d2ef268` | invalid as shipped, not ready | ideas only |
| `rust-async-patterns` from <https://github.com/wshobson/agents>      | `4bde316` | invalid as shipped, not ready | ideas only |
| `memory-safety-patterns` from <https://github.com/wshobson/agents>   | `4bde316` | invalid as shipped, not ready | reject     |
| `rust-skills` from <https://github.com/leonardomso/rust-skills>      | `fd2a861` | not ready                     | ideas only |

"Invalid as shipped" means the package fails this repository's policy validator, because it lacks the author
and license fields. The apollographql and leonardomso descriptions are folded YAML scalars, which this
repository's description check rejects.

### `apollographql/skills` `rust-best-practices`

A 94-line index over about 2,400 lines of chapter references, copyright Apollo Graph, Inc.

- Its thread-safety table states the bounds wrongly: `&T: Send` needs `T: Sync`, `Arc<T>: Send` needs
  `T: Send + Sync`, and `&mut T` can be sent across scoped threads
  (<https://doc.rust-lang.org/std/marker/trait.Send.html>).
- It recommends `&String` and read-only `Cow<str>` parameters, which clippy's default `ptr_arg` lint flags.
- About ten examples do not compile, including let-else blocks without their closing `;`.
- It declares Rust 1.70 but teaches `LazyLock` (1.80), `#[expect]` (1.81) and `assert_matches!` (1.96).
- It names nursery lints as key lints under a `-D warnings` run that never enables them, and its `[lints]`
  example inverts Cargo's priority order.

Worth adapting: duplication against the wrong abstraction, `#[expect]` with a reason over `#[allow]`, a
workspace `[lints]` table with correct priorities, the fact that `nextest` does not run doctests, what not to
snapshot with `insta`, and the index-plus-chapters layout.

### `affaan-m/ECC` `rust-patterns` and `rust-testing`

Two single files of about 500 lines each, copyright Affaan Mustafa. About 70% is idiom a current model already
writes.

- An `unsafe` example states an incomplete safety contract, leaving out that the memory must stay valid and
  unaliased, and it presents `get_unchecked` as acceptable.
- It uses the deprecated `criterion::black_box` instead of `std::hint::black_box`.
- It recommends `tokio::time::pause` without its `test-util` feature and current-thread runtime requirements.
- It advises a `#[must_use]` that clippy's `double_must_use` flags, teaches the older `mod.rs` layout, and
  compares floats with `f64::EPSILON`, which is wrong for values far from 1.
- `rust-testing` forces test-driven development on every testing request, which conflicts with this
  repository's `test-driven-development` and `test-engineer` skills.

Worth adapting: the split between thiserror for libraries and anyhow for applications, enums for states, the
`tests/common/mod.rs` layout, `matches!` for asserting error variants, rstest, proptest and mockall usage, and
coverage gates with `cargo llvm-cov --fail-under-lines`.

### `wshobson/agents` `rust-async-patterns` and `memory-safety-patterns`

Copyright Seth Hobson.

- The async skill omits cancellation safety in `select!`, `spawn_blocking`, `Pin` and `TaskTracker`.
- Two of its examples do not compile (E0521 and E0277), and its channel and shutdown examples hang or panic.
- Its lock advice contradicts the tokio documentation, and it recommends `async-trait` without mentioning
  native `async fn` in traits (Rust 1.75).
- The memory-safety skill mixes Rust, C++ and C without a shared job. Its C++ example races, its Rust `RwLock`
  example deadlocks, and its C cleanup example fails to compile under GCC 15. It has no `unsafe` or FFI content.

Worth adapting from the async skill: its list of patterns, as an outline to rewrite.

### `leonardomso/rust-skills`

One skill of 265 rule files in 26 categories, about 33,600 lines, copyright Leonardo Maldonado. Its version
gating is the strongest of the six: every release number checked against the Rust release notes was correct.

- It says `#[tokio::test]` uses the multi-thread runtime; it uses the current-thread runtime
  (<https://docs.rs/tokio/latest/tokio/attr.test.html>).
- Its `select!` loop never exits after the channel closes, because an always-enabled cancellation branch keeps
  the `else` arm from running.
- It says dropped futures stop at their next `.await`; a dropped future is never polled again
  (<https://docs.rs/tokio/latest/tokio/macro.select.html>).
- Two of its rules about `Send` on spawned tasks are false, and it claims `trait-variant` gives a
  dyn-compatible trait, which fails with E0038.
- Its shutdown guidance omits `TaskTracker` and aborts tasks immediately after cancelling them.
- Three of its `[lints]` and `clippy.toml` setups fail under current cargo and clippy, including group lints at
  the same priority as their overrides, which the deny-by-default `lint_groups_priority` lint rejects.
- It teaches the deprecated `criterion::black_box`, and its mockall example returns the wrong values.
- Its own example checker runs `cargo check` only, never clippy and never the code, and accepts 124 known
  failures.

Worth adapting: the cancel-safety table, bounded and `watch` channels, declaring a minimum Rust version,
`check-cfg`, `#[instrument]` spans, serde `deny_unknown_fields` and `flatten`, error source chains, let-else and
if-let chains, `const` blocks, and snapshot testing.

## The Rust Set

Five skills, one per concern, in the shape of the Python set:

| Skill                 | Covers                                                                                            |
| --------------------- | ------------------------------------------------------------------------------------------------- |
| `rust-style`          | Idioms, edition and minimum-version awareness, clippy and the `[lints]` table                     |
| `rust-error-handling` | thiserror and anyhow, error types, source chains                                                  |
| `rust-async`          | tokio, cancellation safety, `spawn_blocking`, `Send` and `'static` bounds, shutdown, async traits |
| `rust-testing`        | nextest, insta, rstest, proptest, command-line contract tests, slow tests kept opt-in             |
| `rust-unix-processes` | Pseudo-terminals, process groups, signal forwarding, exit-status pass-through with nix or rustix  |

An `unsafe` and FFI skill is deferred, because the project writes no `unsafe` code of its own. A scoped Rust
rule in the installing configuration points agents at the set.

## Proving the Examples

A wrong Rust claim reads as plausibly as a right one, as all six candidates show, so every skill proves its
examples mechanically before it lands:

- The repository pins Rust 1.99.1 with clippy and rustfmt in `mise.toml`, because clippy's lints and their
  levels change between releases.
- A check in `just check` builds every Rust code block in the Rust skills and runs clippy with warnings
  denied. A block's label can also require that it runs and exits 0, that it fails with a named compiler
  error, or that a `Cargo.toml` fragment is accepted by cargo and clippy. Running matters because several
  defects above compile cleanly and behave wrongly.
- The check stays permanent, because edits are where an unnoticed broken example lands. It skips blocks whose
  content has not changed, and CI runs it only when a Rust skill changes.
- Claims that can change between versions cite official documentation and the Rust version they were checked
  on, and each skill gets an independent review before it lands. Compiling proves an example is valid Rust, not
  that its advice is sound; the review covers that.
