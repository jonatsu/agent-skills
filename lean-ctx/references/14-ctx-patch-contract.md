# ctx_patch contract

Field names and behaviors verified against lean-ctx 3.9.18.

**The runtime error message is the contract.** The published MCP schema is a
flat, all-optional bag — `allOf`/`oneOf` are stripped before publication — and
upstream docs disclaim per-op schemas, deferring to the server source. NEVER
"correct" this file from the published schema or from upstream prose. If a call
is rejected for a missing or unknown field, follow the error, then fix this file.

## Contents

- Operations and their fields
- Why an exact-match op misses
- replace_all rewrites the file mode
- Batching and atomicity
- dry_run does not validate anchors
- line is advisory; the hash carries identity
- Gates that reject a write before any anchor is checked
- Stale-anchor protocol

## Operations and their fields

`path` is top-level. Each op carries `op` plus its own fields.

| Op | Fields | Anchored read first |
|---|---|---|
| `set_line` | `line`, `hash`, `new_text` | yes |
| `insert_after` | `line`, `hash`, `new_text` | yes |
| `delete` (single) | `line`, `hash`, `new_text=""` | yes |
| `replace_lines` | `start_line`, `start_hash`, `end_line`, `end_hash`, `new_text` | yes |
| `delete` (range) | `start_line`, `start_hash`, `end_line`, `end_hash`, `new_text=""` | yes |
| `replace_symbol` | `name`, `new_text` | no |
| `replace_unique` | `old_text`, `new_text` | no |
| `replace_all` | `find`, `replace` | no |
| `create` | `new_text` | no |

Traps inside that table:

- The replacement field is `new_text` for every op EXCEPT `replace_all`, which
  names it `replace` and rejects `new_text`/`old_text`/`old_string`/`new_string`
  outright. `replace` MUST be passed explicitly; there is no default.
- `replace_symbol` takes `new_text`, never `new_body`, and `new_text` is the FULL
  replacement declaration — the whole function or class block, not just a body.
- `replace_symbol`'s `name` resolves against the WHOLE repository index, and the
  top-level `path` does NOT scope it. A common name returns
  `AMBIGUOUS_SYMBOL: 'x' matches N symbols; qualify it:` listing candidates from
  every language in the repo, shell scripts included — `name=main` with `path` set
  to a single file returned 10 candidates across 7 other files. The error prints
  qualified `path:symbol` forms. For any name that is not repo-unique, use
  `replace_unique` on the declaration line instead.
- `replace_unique` requires a non-empty `old_text` (`old_string`/`new_string` are
  accepted aliases); `find`/`replace` are rejected there.
- On `delete`, the mere presence of `start_line` or `end_line` selects the range
  shape and then demands all four anchor fields.
- `replace_lines` tolerates missing hashes, which silently disables conflict
  detection. Always pass them.
- `insert_after` with `line=0` inserts at the top of the file, and its `new_text`
  MUST be non-empty.
- An anchored read returns `N:hash|`. Split it into the named `line` and `hash`
  fields — never pass a combined `"N:hash"` string.
- `new_text` on a single-line op is the replacement content only, never the old
  line repeated back.

SHOULD prefer `replace_unique` for renames and path sweeps: no anchored read, no
hash to go stale, and a non-unique match fails loudly instead of editing the wrong
line. `replace_all` covers every occurrence in one call but rewrites the file mode
— see below before reaching for it.

## Why an exact-match op misses

`replace_unique` and `replace_all` match bytes, so the miss is almost always
invisible whitespace rather than a wrong string.

The most common trigger is a **formatted markdown table**: a formatter pads cells,
so a row's trailing `|` sits behind a run of spaces and an `old_text` ending in
`… |` never matches. End the match before the padding.

## replace_all rewrites the file mode

**`replace_all` destroys the file's mode; the other ops do not.** It rewrites the
file at `0600`, so a patched script keeps `100755` in the index while the working
copy loses `+x`, and the next invocation dies with `Permission denied`.

The edit reports success, and `git status` stays silent because the index is
unchanged — the drift shows only as `ls -l` disagreeing with `git ls-files -s`. On
a 755 probe file, `replace_unique` and anchored `set_line` both preserved 755 while
`replace_all` reset it to `0600`.

After ANY `replace_all` on an executable, `chmod` it back and verify. Prefer
`replace_unique`, which is the better tool for a rename sweep regardless.

## Batching and atomicity

- Batch independent edits with `ops:[...]`.
- NEVER send a top-level `op` and `ops:[...]` in the same call. For
  `replace_unique` and `replace_all` the top-level op wins and the whole batch is
  discarded with no error.
- `create` and `replace_all` CANNOT be batched; each MUST be its own top-level
  call.
- Atomicity is narrower than "batch-atomic" suggests. A run of anchored ops on
  ONE file is atomic: one stale anchor aborts it with zero writes. A cross-file
  batch is NOT — file 1 is written before file 2 is read, and file 2's CONFLICT
  comes back as ordinary text in an otherwise successful-looking response.
- A batch containing `replace_unique` or `replace_symbol` applies sequentially,
  so earlier ops are already on disk when a later one fails.
- **Partial application runs in BOTH directions.** A failed op does not stop later
  ops in the same batch, so op 1 can fail while ops 2 and 3 land. The aggregate
  response then reads as success: each applied op prints its own `✓` and the error
  is one block among them. After any multi-op batch, confirm each intended change
  actually landed rather than scanning for an overall failure.

## dry_run does not validate anchors

On anchored ops, `dry_run` short-circuits before the file is even opened. A
fabricated hash — or a missing file, or a malformed op — returns
`DRY RUN: would apply`. Only the real call returns CONFLICT. NEVER use it to
check an anchor.

It does earn its keep elsewhere: it validates fields on
`replace_unique`/`replace_symbol` and reports a true match count on
`replace_all`.

`dry_run` MUST be a JSON boolean. The string `"true"` reads as false and the edit
APPLIES.

## line is advisory; the hash carries identity

If the hash does not match at `line`, `ctx_patch` searches the whole file for a
unique line carrying that hash and edits THERE instead — silently, with no notice
in the output. A stale line number with a good hash therefore succeeds, and the
edit can land somewhere other than the line named. Only 0 or 2+ matches fall back
to CONFLICT. The 4-hex hash carries the identity; the number does not.

## Gates that reject a write before any anchor is checked

- A tree-sitter **syntax** gate blocks an edit that would turn a clean file
  broken. Override per call with `validate_syntax=false`.
- A **code-health** complexity gate warns, and blocks only where configured to.
  Config-only; there is no per-call override.
- A no-op edit is an error, not a success.

A rejected write is therefore not always an anchor problem. Read the error before
re-reading the file.

## Stale-anchor protocol

1. A hash mismatch means the file changed since the read.
2. The CONFLICT error returns fresh anchors inline for every miss — retry from
   those. They are omitted only when the miss is past EOF (the file shrank);
   then re-read with `mode="anchored"`.
3. Recompute anchors and retry exactly once.
4. Still failing: STOP. Do not loop, and do not guess hashes.

**Distinct symptom:** if a refreshed anchored read returns the file with no
`N:hh|` anchors at all — not a hash mismatch — that is environmental, not stale.
Do not retry-loop. Make all of that file's edits in one batch from the last good
anchored read, and check whether the running server predates a `lean-ctx update`:
the MCP process holds the old binary until the host restarts it.
