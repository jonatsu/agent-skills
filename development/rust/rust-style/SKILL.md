---
name: rust-style
description: Write and review idiomatic Rust that fits the crate's edition and minimum Rust version. Use for new Rust code, style or idiom reviews, function signatures and ownership, newtypes and enums, panics and expect, module layout, doc comments, and clippy, rustfmt, or Cargo [lints] setup. Error types, async and tokio, Unix processes and signals, and tests have their own rust-* skills.
license: MIT
compatibility: Rust 1.85 or later (edition 2024).
metadata:
  author: Joonas Onatsu
---

# Rust Style

Everyday Rust defaults for code whose conventions are not already settled. This skill owns the choices that
need judgment in ordinary code and hands each detailed subject to its specialist. Load the specialist when the
task reaches its subject:

| Subject                                                       | Skill                 |
| ------------------------------------------------------------- | --------------------- |
| Error types, `Result` boundaries, thiserror and anyhow        | `rust-error-handling` |
| tokio, tasks, cancellation, shutdown, and async traits        | `rust-async`          |
| Child processes, pseudo-terminals, signals, and exit statuses | `rust-unix-processes` |
| Unit, integration, snapshot, property, and command-line tests | `rust-testing`        |

Current known: Rust 1.99.1, checked on 2026-11-08 against the Rust release notes, the Edition Guide, the Cargo
book, and clippy's own output. Confirm a version fact with `rustc --version` and the release notes at
<https://doc.rust-lang.org/stable/releases.html>.

## Respect Project Conventions

Use these defaults for new crates. In an established crate, follow its declared configuration
(`rustfmt.toml`, `clippy.toml`, `[lints]`) and its consistent local practice, including in new modules.

Recommend a change only for incorrect behavior, a soundness or security problem, a build that breaks for some
user, or concrete maintenance harm. Explain the evidence, the consequence, and the smallest fix. A different
but valid style is not a defect.

## Check the Edition and Minimum Version First

Read `edition` and `rust-version` in `Cargo.toml`, including any `[workspace.package]` values, and any
`rust-toolchain.toml`, before writing code. Use only language features and library items that are stable at
the declared `rust-version`. Your own toolchain is usually newer, so a feature beyond that version compiles for
you and breaks the build for every user on the minimum.

Clippy's default `incompatible_msrv` lint flags standard-library items newer than `rust-version`, but it does
not flag newer language syntax. On Rust 1.99.1 with `rust-version = "1.85"`, an `if let` guard (stable in
1.95) builds without any warning. Only a build with the minimum toolchain catches both, so a crate that declares
a minimum should build with that toolchain in CI.

A new crate uses edition 2024 and declares `rust-version`. Edition 2024 requires `rust-version` 1.85 or later,
and Cargo rejects a lower value. Its default resolver (version 3) prefers dependency versions whose own
`rust-version` fits yours.

Read [references/versions.md](references/versions.md) before using a feature from the last few years, such as
let chains, `if let` guards, `LazyLock`, `#[expect]`, async closures, or `use<..>` bounds, and when moving a
crate to edition 2024 or reviewing code that relies on edition-specific drop order.

## Signatures and Ownership

Borrow what a function only reads, and take ownership of what it keeps. Accept `&str`, `&[T]`, and `&Path`
rather than `&String`, `&Vec<T>`, and `&PathBuf`; clippy's default `ptr_arg` lint flags the owned-reference
forms, because they force callers to own that exact type. Take `String` or `impl Into<String>` when the value is
stored, so a caller who already owns one hands it over without a copy.

Return owned values. Return `Cow<'_, str>` only when the result is sometimes a borrow of the input and sometimes
new. Take `&str` rather than `&Cow<'_, str>` as a parameter, which `ptr_arg` also flags.

Write the elided lifetime in a returned type that borrows from an argument, such as `Ref<'_, T>`. Hiding it
triggers the default `mismatched_lifetime_syntaxes` warning, since Rust 1.89.

A `.clone()` added only to satisfy the borrow checker usually hides a borrow that lasts too long. Shorten the
borrow, borrow struct fields separately, or restructure first. Cloning an `Arc` or `Rc` is cheap and is the
normal way to share ownership.

```rust
use std::path::Path;

pub struct Config {
    name: String,
}

impl Config {
    /// Stores the name, so it takes ownership.
    pub fn new(name: impl Into<String>) -> Self {
        Self { name: name.into() }
    }

    /// Only reads the path, so it borrows the most general form.
    pub fn is_inside(&self, path: &Path) -> bool {
        path.starts_with(&self.name)
    }
}
```

## Types That Carry Invariants

Give an identifier or a validated value its own type, a newtype with a private field. Construct it through
`TryFrom` or `FromStr`, which return an error, so every value of the type is valid.

Model states with an enum, not with combinations of `bool` and `Option` fields that allow impossible states.
Match your own enums without a `_` arm where practical, so that adding a variant shows every place that must
handle it. Mark a public library enum or struct `#[non_exhaustive]` when it is expected to grow; types inside
a binary need no such marker.

Derive `Debug` on every public type. Derive `Clone`, `PartialEq`, `Eq`, and `Hash` when they mean something for
the type, and `Copy` only for small values with no ownership.

```rust,run
use std::fmt;
use std::str::FromStr;

/// A port number that is never zero.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Port(u16);

#[derive(Debug, PartialEq, Eq)]
pub struct InvalidPort(String);

impl fmt::Display for InvalidPort {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "invalid port {:?}: expected 1 to 65535", self.0)
    }
}

impl std::error::Error for InvalidPort {}

impl FromStr for Port {
    type Err = InvalidPort;

    fn from_str(text: &str) -> Result<Self, Self::Err> {
        match text.parse::<u16>() {
            Ok(0) | Err(_) => Err(InvalidPort(text.to_owned())),
            Ok(number) => Ok(Self(number)),
        }
    }
}

fn main() {
    assert_eq!("8080".parse::<Port>(), Ok(Port(8080)));
    assert!("0".parse::<Port>().is_err());
}
```

## Panics

Return a `Result` for anything that can fail because of input, the environment, or another system; the
`rust-error-handling` skill covers the types. Keep panics for broken invariants, where continuing would be a
bug.

Use `expect` with a message that states the invariant, such as `expect("the parser accepted this pattern")`,
rather than `unwrap`, so the panic names what was assumed. `unwrap` is fine in tests and in examples. Use
`get` instead of indexing when an index comes from input.

`Mutex::lock` returns an error only when another thread panicked while holding the lock. Propagate that panic
with `expect("no thread panics while holding this lock")` when the guarded data may now be inconsistent. Recover with
`PoisonError::into_inner` only when every state the data can be in is valid.

Integer overflow panics in debug builds and wraps silently in release builds by default. Use `checked_`,
`saturating_`, or `wrapping_` arithmetic wherever input controls the operands, and pick the one that states
the intended behavior. An `as` cast between integer types also truncates or wraps without a warning, so convert
an input-controlled value with `try_from`, such as `u16::try_from(length)`; the pedantic
`cast_possible_truncation` lint finds the remaining casts.

## Lints and Formatting

Configure lints in the `[lints]` table of `Cargo.toml`, not with crate attributes. In a workspace, put them in
`[workspace.lints]` and add `lints.workspace = true` to each member. Cargo rejects a member that inherits the
workspace lints and also sets its own, so a member that needs an exception uses `#[expect]` in code.

Clippy enables its `correctness` group as errors, and its `suspicious`, `style`, `complexity`, and `perf`
groups as warnings. The `pedantic`, `nursery`, `restriction`, and `cargo` groups are off. Enable `pedantic` as
a group only when the project wants it, and then at priority `-1`, so individual lints can override it. A group
and an override at the same priority trigger the deny-by-default `lint_groups_priority` lint, and clippy
fails. Never enable `restriction` as a group, because its lints contradict each other; clippy itself warns
about it. Pick single restriction lints instead.

```toml,manifest
[lints.rust]
unsafe_code = "forbid"

[lints.clippy]
pedantic = { level = "warn", priority = -1 }
must_use_candidate = "allow"
```

Forbid `unsafe_code` in a crate that needs no unsafe code, so a later change cannot add it unnoticed.

Silence one lint at one site with `#[expect(clippy::lint_name, reason = "why")]`, which warns once the lint no
longer fires, so stale exceptions surface. Use `#[allow]` only where the lint fires on some targets or
configurations but not others.

Deny warnings in CI on the command line, not with `#![deny(warnings)]` in source: a newer compiler adds new
warnings and would break the build for everyone who compiles the crate. Run these in CI:

```text
cargo fmt --check
cargo clippy --all-targets --all-features --locked -- -D warnings
RUSTDOCFLAGS="-D warnings" cargo doc --no-deps --locked
```

Use rustfmt's defaults unless the project has a `rustfmt.toml`. Edition 2024 also selects rustfmt's 2024 style
edition, which sorts imports and other names differently from earlier editions.

## Modules and Visibility

Put a module with children in `src/net.rs` and its children in `src/net/`, the default layout since edition
2018\. A `src/net/mod.rs` layout is also valid: follow whichever the crate uses, and never mix the two. The
restriction lints `mod_module_files` and `self_named_module_files` enforce one layout or the other.

Keep items private by default, use `pub(crate)` for sharing inside the crate, and make `pub` only the intended
API. In a crate with both a library and a binary, keep the logic in `src/lib.rs` and keep `src/main.rs` to
argument parsing and a call into the library, so integration tests can reach the logic.

## Documentation

Document every public item with `///`, starting with a one-line summary. Add an `# Errors` section to a
function returning `Result`, a `# Panics` section when it can panic, and a `# Safety` section to every
`pub unsafe fn`. The default `missing_safety_doc` lint requires the last, and the pedantic `missing_errors_doc`
and `missing_panics_doc` lints check the others.

Code in a doc comment is a doctest that `cargo test` runs. `cargo nextest` does not run doctests, so a project
that uses nextest also runs `cargo test --doc`.
