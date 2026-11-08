# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## First-party Sources

### The Rust Project: The Rust Programming Language, chapter 11

- Source: <https://doc.rust-lang.org/book/ch11-03-test-organization.html>
- License: `MIT OR Apache-2.0`
- Version: Rust 1.99.1

The unit and integration test layout and the `tests/common/mod.rs` convention come from this chapter. No prose
or code was copied.

### Test crate documentation: assert_cmd, rstest, proptest, and cargo-nextest

- Source: <https://docs.rs/assert_cmd/2.2.2/assert_cmd/>, <https://docs.rs/rstest/0.28.0/rstest/>,
  <https://docs.rs/proptest/1.12.0/proptest/>, <https://nexte.st/docs/running/>
- License: `MIT OR Apache-2.0`
- Version: assert_cmd 2.2.2, rstest 0.28.0, proptest 1.12.0, cargo-nextest 0.9.151

The binary-testing macros, the case syntax, the regression files, and nextest's handling of ignored tests and
doctests come from this documentation. No prose or code was copied.

### Armin Ronacher: insta documentation

- Source: <https://docs.rs/insta/1.49.0/insta/>
- License: `Apache-2.0`
- Version: 1.49.0

The snapshot update modes and their behavior in CI come from this documentation. No prose or code was copied.

### Tokio Contributors: `#[tokio::test]` documentation

- Source: <https://docs.rs/tokio/1.54.1/tokio/attr.test.html>
- License: `MIT`
- Version: tokio 1.54.1

The default test runtime and the paused-clock requirements come from this documentation. No prose or code was
copied.

## Third-party Sources

### Affaan Mustafa: `rust-testing`

- Source: <https://github.com/affaan-m/ECC>, `skills/rust-testing`
- License: `MIT`
- Version: `d2ef2680594f9a17526a6e1a2e18b3d242c5d17b`

It suggested covering rstest, proptest, and coverage floors with `cargo llvm-cov --fail-under-lines`. Nothing
was copied.

### Apollo Graph, Inc.: `rust-best-practices`

- Source: <https://github.com/apollographql/skills>, `skills/rust-best-practices`
- License: `MIT`
- Version: `9dda1397730370aeb8df4ff8f2015c34c86b5003`

It suggested noting that nextest does not run doctests, and keeping nondeterministic values out of snapshots.
Nothing was copied.
