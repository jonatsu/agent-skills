---
name: ast-grep
description: Search, map, and rewrite code structurally with ast-grep, matching Abstract Syntax Tree shapes rather than text. Use when exploring unfamiliar files or directories, outlining long code or Markdown before a ranged read, locating constructs text search cannot express, writing or debugging patterns and YAML rules, or applying mechanical changes across files. Use outline for mapping and run or scan for matching and rewriting.
license: MIT
compatibility: Requires the ast-grep CLI (`ast-grep`, also installed as `sg`). Documented against 0.45.3.
metadata:
  author: Joonas Onatsu
---

# ast-grep structural tools

Default to ast-grep when a request describes code as code: calls, declarations, arguments, nesting,
surrounding constructs, or the presence or absence of behavior. It ignores formatting, can restrict a match by
parents, children, or neighbors, and can reuse captured nodes in a previewable rewrite. Use `rg` when the
question is genuinely textual.

High-impact examples include:

- find async functions that await work but have no error-handling construct;
- migrate an API by updating imports, client initialization, and calls as coordinated rules;
- replace list comprehensions with generators only where the caller accepts an iterable;
- rename a pytest fixture and its arguments only inside pytest tests and fixtures.

These patterns generalize to framework upgrades, security checks, deprecation removal, scoped renames, and
repository-wide mechanical refactors. See [references/examples.md](references/examples.md) for copyable
Python examples and the official multi-language catalog.

Choose the subcommand from the task:

| Need                                                                                     | Use                                                                                           |
| ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Map a file, directory, changed-file set, symbols, imports, exports, or Markdown headings | `ast-grep outline`; read [references/outline.md](references/outline.md)                       |
| Match or rewrite one node shape                                                          | `ast-grep run --pattern ...`                                                                  |
| Match relations such as `inside`, `has`, `all`, `any`, or `not`                          | `ast-grep scan --rule ...`; read [references/rule-reference.md](references/rule-reference.md) |
| Find literal text, comments, or prose content                                            | `rg`                                                                                          |

Only `outline` is useful on Markdown. Structural patterns do not expose Markdown inline syntax reliably; use
the heading outline to choose a range, then edit that range with an ordinary text tool.

## Workflow

1. Outline an unfamiliar or long target before reading it in full.
2. Define the language, construct, variations, and exclusions.
3. Test the simplest pattern or rule against a small example known to contain a match.
4. Run it on the real target and inspect the matches or preview diff critically.
5. Apply a rewrite only after confirming its scope and the working tree state.

```bash
ast-grep outline <path>
ast-grep run --pattern 'console.log($ARG)' --lang javascript <path>
ast-grep scan --rule my-rule.yml <path>
```

`run --rewrite` and a rule's `fix:` print a diff without writing by default. Use `--interactive` to approve
hunks or `--update-all` only after reading the preview. Do not rewrite files containing unrelated work.

## When a Pattern Matches Nothing

Zero matches can mean either absent code or a wrong node shape. Prove the pattern against a known example
before reporting absence.

```bash
ast-grep run --pattern 'class $NAME { $$$BODY }' --lang javascript --debug-query=pattern
ast-grep run --pattern 'class User { constructor() {} }' --lang javascript --debug-query=cst
```

Then check these common causes:

- verify every `kind` against the concrete syntax tree rather than memory;
- add `stopBy: end` when a relational rule must search beyond the immediate neighbor;
- make each metavariable the complete text of its node;
- use `$$` for unnamed nodes such as operators and `$$$` for node lists; and
- reduce a compound rule to its simplest positive match, then restore conditions one at a time.

Advanced rule syntax, metavariables, reusable tests, and JSON-output traps are in
[references/rule-reference.md](references/rule-reference.md).
