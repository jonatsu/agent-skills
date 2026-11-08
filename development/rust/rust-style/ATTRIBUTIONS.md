# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## First-party Sources

### The Rust Project: release notes, Edition Guide, Cargo book, and clippy

- Source: <https://doc.rust-lang.org/stable/releases.html>, <https://doc.rust-lang.org/edition-guide/>,
  <https://doc.rust-lang.org/cargo/>, <https://rust-lang.github.io/rust-clippy/>
- License: `MIT OR Apache-2.0`
- Version: Rust 1.99.1

The feature versions, the edition 2024 changes, the `[lints]` table rules, and the lint groups and levels come
from this documentation and from clippy's output on that release. No prose or code was copied.

## Third-party Sources

### Apollo Graph, Inc.: `rust-best-practices`

- Source: <https://github.com/apollographql/skills>, `skills/rust-best-practices`
- License: `MIT`
- Version: `9dda1397730370aeb8df4ff8f2015c34c86b5003`

It suggested preferring `#[expect]` with a reason over `#[allow]`, and configuring lints in a workspace
`[lints]` table. Nothing was copied.

### Leonardo Maldonado: `rust-skills`

- Source: <https://github.com/leonardomso/rust-skills>
- License: `MIT`
- Version: `fd2a861ab0406a4ac536a55274d14ea6fd1ca9c9`

It suggested checking features against the declared minimum Rust version, and the edition 2024 unsafe
attribute and `unsafe extern` rules. Nothing was copied.
