# ast-grep outline reference

`ast-grep outline` prints a compact local syntax map with line numbers. A file shows imports, declarations,
and direct members; a directory defaults to grouped exports. Use the result to choose a ranged read rather
than opening an unfamiliar target in full.

## Common Routes

Map a file's table of contents, dependencies, and public entry points:

```bash
ast-grep outline <file>
ast-grep outline <file> --items imports
ast-grep outline <file> --items exports
```

Map a directory's public surface, optionally narrowed by top-level symbol type:

```bash
ast-grep outline <dir> --items exports
ast-grep outline <dir> --type struct,enum,function
```

Zoom into a symbol or trace dependency direction:

```bash
ast-grep outline <file> --match <symbol> --type class --view expanded
ast-grep outline <dir> --items imports --view signatures
```

Summarize the structure left by a change:

```bash
ast-grep outline $(git diff --name-only HEAD) --items exports
```

## Markdown and Other Prose

Markdown headings outline without configuration:

```bash
ast-grep outline <file.md>
ast-grep outline <dir>
ast-grep outline <file.md> --match <heading-regex>
```

`--view` works as it does for code. `--items imports` and `--type` return nothing because prose has neither
imports nor symbol types.

Only navigation transfers to Markdown. `ast-grep run --pattern` does not expose inline constructs such as
links, emphasis, or code spans reliably. Block kinds such as `section` do resolve, so `--kind section` can
provide nested section extents when a start and end line are useful. Edit the range that the outline identifies
with an ordinary text tool.

## Arguments

- `--items <KIND>` selects `structure` (the file default), `exports` (the directory default), `imports`, or
  `all`.
- `--view <VIEW>` selects `names`, `signatures`, `digest`, or `expanded`, from least to most detail.
- `--match <REGEX>` filters top-level names or signatures using a case-sensitive Rust regex. It does not
  match members.
- `--type <TYPE[,TYPE...]>` filters top-level symbol types. Member types such as `method` and `field` return
  nothing at the top level.
- `--pub-members` hides private members in views that print members.
- `--lang <LANG>` is required for stdin because no path exists for language inference.
- `--json=stream` emits one object per file with precise ranges. Prefer text for navigation.

## Limits

`outline` reports local syntax. It does not resolve references, infer types, follow re-export chains, or build
a call graph. Use `ast-grep run`, `rg`, or a compiler-backed tool for those questions, then outline the files
they surface.
