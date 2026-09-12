---
name: ast-grep-outline
description: Map a file, directory, or changed file set with `ast-grep outline` before reading source. Use when exploring unfamiliar code, locating a symbol's members, tracing which files import a module, or reviewing the structure a change left behind. Use ast-grep for matching or rewriting a specific code pattern.
license: MIT
compatibility: Requires the ast-grep CLI (`ast-grep`, also installed as `sg`). Documented against 0.45.3.
metadata:
  author: Joonas Onatsu
---

# ast-grep outline

`ast-grep outline` prints a compact structural map with line numbers: top-level items (imports, functions,
classes, structs, interfaces, modules, enums) and their direct members (fields, methods, constructors, enum
variants). It is local and syntax-only, so it is cheap enough to run before any full file read.

Read code in stages: find candidate files by search or by name, outline them, then open only the line range
the outline points at. Defaults adapt to the input — a file shows local structure with member digests, a
directory shows only its exported surface as grouped names.

## Uses

**Before editing a file**, get its table of contents, dependencies and public entry points:

```shell
ast-grep outline <file>
ast-grep outline <file> --items imports
ast-grep outline <file> --items exports
```

**Mapping an unfamiliar directory**, scan the public surface first, then narrow by symbol type:

```shell
ast-grep outline <dir> --items exports
ast-grep outline <dir> --type struct,enum,function
```

**Zooming into a known symbol**, list its members with line numbers instead of reading the body:

```shell
ast-grep outline <file> --match <symbol> --type class --view expanded
```

**Tracing dependency direction**, find which files import a module to decide where a change belongs:

```shell
ast-grep outline <dir> --items imports --view signatures
```

**Reviewing a change**, summarize the resulting structure and public surface:

```shell
ast-grep outline $(git diff --name-only HEAD) --items exports
```

## Arguments

- `--items <KIND>` selects top-level items: `structure` for local declarations (the file default), `exports`
  for the public API (the directory default), `imports` for dependencies, `all` when import and export edges
  matter together.
- `--view <VIEW>` sets detail, least to most: `names` for directory scans, `signatures` for one line per item,
  `digest` for signatures plus member names, `expanded` for one line per member with its line number.
- `--match <REGEX>` filters top-level items by name or signature. Rust regex, case-sensitive. It never matches
  members.
- `--type <TYPE[,TYPE...]>` keeps only some top-level symbol types, such as `--type class,function`. Member
  types like `method` and `field` never match a top-level item, so filtering by one returns nothing.
- `--pub-members` hides private members in views that print members.
- `--lang <LANG>` is required for stdin input, since there is no path to infer the language from.
- `--json=stream` emits one JSON object per file with precise ranges. Use it only to pipe or post-process;
  prefer the text output for navigation.

## Limits

`outline` reports local syntax structure. It does not resolve references, infer types, follow re-export
chains, or build a call graph. Use `ast-grep run`, `rg`, or a compiler-backed tool for those questions, then
outline the files they surface.
