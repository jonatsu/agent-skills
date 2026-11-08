# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## First-party Sources

### Tokio Contributors: tokio and tokio-util API documentation

- Source: <https://docs.rs/tokio/1.54.1/tokio/>, <https://docs.rs/tokio-util/0.7.20/tokio_util/>
- License: `MIT`
- Version: tokio 1.54.1, tokio-util 0.7.20

The runtime shutdown behavior, the blocking-work guidance, the cancellation-safety lists, the `select!` branch
rules, the mutex choice, and the `TaskTracker` and `JoinSet` comparison come from this documentation. No prose
or code was copied.

## Third-party Sources

### Seth Hobson: `rust-async-patterns`

- Source: <https://github.com/wshobson/agents>, `plugins/systems-programming/skills/rust-async-patterns`
- License: `MIT`
- Version: `4bde3168b43c0655c4d00ea2726e631719908a6d`

Its list of async patterns served as an outline of topics to cover. Nothing was copied.

### Leonardo Maldonado: `rust-skills`

- Source: <https://github.com/leonardomso/rust-skills>
- License: `MIT`
- Version: `fd2a861ab0406a4ac536a55274d14ea6fd1ca9c9`

Its cancellation-safety table and its failing `select!` loop and shutdown examples showed which cases the skill
must state correctly. Nothing was copied.
