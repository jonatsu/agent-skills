# Versions and Edition 2024

Use this file to check a feature against the crate's `rust-version`, and to work with edition 2024's changes.
Every version below comes from the Rust release notes (<https://doc.rust-lang.org/stable/releases.html>), and
every edition change from the Edition Guide (<https://doc.rust-lang.org/edition-guide/rust-2024/>), as of Rust
1.99.1.

## Contents

- Feature versions
- Edition 2024 changes
- Moving a crate to edition 2024

## Feature Versions

A feature is usable when the crate's `rust-version` is at least the version listed. Clippy's
`incompatible_msrv` lint flags the library functions and types in this table, but not the language features
and not the `cfg_select!` macro, so check those here before using them.

| Feature                                                         | Kind     | Stable in           |
| --------------------------------------------------------------- | -------- | ------------------- |
| `let ... else`                                                  | Language | 1.65                |
| `std::hint::black_box`                                          | Library  | 1.66                |
| `std::sync::OnceLock`                                           | Library  | 1.70                |
| `async fn` and return-position `impl Trait` in traits           | Language | 1.75                |
| `Result::inspect_err`, `Option::inspect`                        | Library  | 1.76                |
| `std::sync::LazyLock`, `std::cell::LazyCell`, `Option::take_if` | Library  | 1.80                |
| `#[expect(lint, reason = "...")]`                               | Language | 1.81                |
| `core::error::Error`                                            | Library  | 1.81                |
| `use<..>` precise-capturing bounds on `impl Trait`              | Language | 1.82 (traits: 1.87) |
| `&raw const` and `&raw mut`                                     | Language | 1.82                |
| `Option::is_none_or`, `std::iter::repeat_n`                     | Library  | 1.82                |
| Edition 2024, async closures, `AsyncFn` traits in every prelude | Language | 1.85                |
| Trait object upcasting to a supertrait                          | Language | 1.86                |
| `Vec::pop_if`, slice and `HashMap` `get_disjoint_mut`           | Library  | 1.86                |
| `Vec::extract_if`, `std::io::pipe`                              | Library  | 1.87                |
| Let chains (`if let A = a && let B = b`), edition 2024 only     | Language | 1.88                |
| `mismatched_lifetime_syntaxes` warning                          | Lint     | 1.89                |
| `if let` guards on match arms                                   | Language | 1.95                |
| `cfg_select!`                                                   | Macro    | 1.95                |

For anything not listed, search the release notes for the item's name; the first version that lists it is the
one it became stable in.

## Edition 2024 Changes

These are the edition 2024 changes most likely to alter what existing code means or whether it compiles. Each
line names the change and what to do about it.

- **Let chains.** `&&` may join `let` conditions in `if` and `while`. They need edition 2024 as well as Rust 1.88.
- **`if let` scrutinee temporaries** drop before the `else` branch runs. A lock guard taken in the condition no
  longer lives into `else`, which removes a classic deadlock.
- **Tail-expression temporaries** drop before the block's local variables. Code that returned
  `cell.borrow().len()` from a block now compiles. A temporary whose lifetime the old rule extended may now need
  its own `let`.
- **Return-position `impl Trait` captures** every in-scope generic parameter, including lifetimes. Write
  `+ use<'a, T>` to capture fewer, for example when the returned value must not borrow an argument.
- **`unsafe extern` blocks.** An `extern` block must be written `unsafe extern`, and each item in it may be
  marked `safe` or `unsafe`.
- **Unsafe attributes.** `no_mangle`, `export_name`, and `link_section` must be written
  `#[unsafe(no_mangle)]`.
- **Newly unsafe functions.** `std::env::set_var` and `std::env::remove_var` need an `unsafe` block, because
  they are unsound while any other thread runs. Set a child's environment with `Command::env` instead, and pass
  settings in as values rather than through the environment.
- **`unsafe_op_in_unsafe_fn` warns.** An unsafe operation inside an `unsafe fn` needs its own `unsafe` block.
- **`static_mut_refs` is deny-by-default.** A reference to a `static mut` is an error. Use an atomic, a
  `Mutex`, `OnceLock`, or `&raw const` instead.
- **Never-type fallback.** An expression of type `!` that must become some type now becomes `!` rather than
  `()`.
- **Match ergonomics.** `mut`, `ref`, and `ref mut` on a binding, and `&` patterns, are errors where the default
  binding mode is not move. Write the pattern fully explicitly, or drop the modifier.
- **Prelude.** `Future` and `IntoFuture` are in the prelude, which can make a call to a trait method of the
  same name ambiguous.
- **Boxed slices.** `boxed_slice.into_iter()` yields owned items rather than references.
- **`gen` is reserved.** Rename an identifier called `gen`, or write it as `r#gen`, which is what
  `cargo fix --edition` does.
- **Macro fragments.** The `expr` fragment also matches `const` blocks and `_`. Use `expr_2021` where a macro
  depends on the old matching.
- **Cargo manifest names.** The duplicate spellings `[project]`, `default_features`, `crate_type`,
  `proc_macro`, `dev_dependencies`, and `build_dependencies` are removed; use `[package]` and the dashed forms.
  A dependency inherited from the workspace can no longer set `default-features = false` unless the workspace
  entry does too.
- **Cargo resolver 3** is the default. It prefers dependency versions whose `rust-version` fits the crate's own.
- **Doctests** are combined into one binary per crate, which makes them faster. A doctest that depends on
  being compiled as its own crate, for example because it relies on its line numbers or uses `$crate`, opts
  out with the `standalone_crate` code-block tag.
- **rustfmt style edition 2024** sorts names by version-aware rules, so the first `cargo fmt` after the move
  reorders imports.

## Moving a Crate to Edition 2024

1. Commit or stash other work, so the migration is one reviewable change.
2. Run `cargo fix --edition --all-targets --all-features`. It applies the mechanical fixes while the crate is
   still on its old edition.
3. Set `edition = "2024"` and a `rust-version` of at least 1.85 in `Cargo.toml`.
4. Review every `unsafe` block that `cargo fix` added around `set_var` or `remove_var`. Replace the call where
   possible, because the added block only silences the error and does not make the call sound.
5. Run `cargo fmt`, then the full build, clippy, and tests.

The step is done when the crate builds, passes clippy with warnings denied, and passes its tests on edition
2024, and every added `unsafe` block has a reason.
