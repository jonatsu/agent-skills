# Daily use

## First choice tools

- `ctx_tree` — compact directory map.
- `ctx_glob` — file discovery.
- `ctx_search` — regex/semantic/symbol search.
- `ctx_read` — compressed or exact file reads.
- `ctx_shell` — command execution with compressed logs.
- `ctx_patch` — anchored/batch file edits.

## Read modes

- `signatures` — API surface; best first look.
- `map` — structure, deps, exports.
- `auto` — let lean-ctx choose.
- `anchored` — edit-ready read for `ctx_patch`.
- `full`/`raw` — exact content when required.
- `lines:N-M` — focused slice.
- `diff` — changed lines after edits.
- `task`/`reference` — intent-focused context.

## Patch workflow

1. `ctx_read(mode="anchored")` for target file.
2. Apply `ctx_patch` with line/hash anchor or batch `ops`.
3. On stale anchor conflict, refresh anchors and retry once.
4. Use create op for new files when supported.

## Shell workflow

Use `ctx_shell` for builds, tests, package managers, git diagnostics, and noisy
commands. Use raw shell only if no lean-ctx shell wrapper exists or exact PTY
interaction is required.
