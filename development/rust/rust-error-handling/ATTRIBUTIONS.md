# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## First-party Sources

### David Tolnay: thiserror and anyhow documentation

- Source: <https://docs.rs/thiserror/2.0.21/thiserror/>, <https://docs.rs/anyhow/1.0.104/anyhow/>
- License: `MIT OR Apache-2.0`
- Version: thiserror 2.0.21, anyhow 1.0.104

The `#[from]`, `#[source]`, and `transparent` rules, the alternate `{:#}` chain format, and the backtrace
variables come from this documentation. No prose or code was copied.

## Third-party Sources

### Affaan Mustafa: `rust-patterns`

- Source: <https://github.com/affaan-m/ECC>, `skills/rust-patterns`
- License: `MIT`
- Version: `d2ef2680594f9a17526a6e1a2e18b3d242c5d17b`

It suggested the split between thiserror for libraries and anyhow for applications. Nothing was copied.

### Apollo Graph, Inc.: `rust-best-practices`

- Source: <https://github.com/apollographql/skills>, `skills/rust-best-practices`
- License: `MIT`
- Version: `9dda1397730370aeb8df4ff8f2015c34c86b5003`

Its error type that both interpolates and wraps its cause showed the doubled-message failure the skill
demonstrates. Nothing was copied.
