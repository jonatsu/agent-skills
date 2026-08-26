# Code intelligence

## Use cases

- Find symbols and declarations before broad reads.
- Trace call paths and dependencies.
- Estimate blast radius before edits.
- Inspect architecture, routes, smells, and quality debt.

## Common tool families

- Symbol tools: symbol lookup, references, declarations.
- Graph tools: callgraph, dependency graph, impact.
- Architecture tools: routes, modules, ownership hints.
- Quality tools: smells, complexity, navigability, token tax.

## Guidance

Prefer code-intelligence tools for semantic questions. Use `ctx_search` for
literal patterns and `ctx_read` only after narrowing target files. If another
LSP or graph server is more precise for the language, use it for symbol-safe
refactors and keep lean-ctx for compression/search/shell.

## What is LSP-backed and what only approximates it

`ctx_refactor` is the only tool here backed by a real language server. Its
headless path spawns an external server, covers a handful of languages, and
requires that server's binary to already be on `PATH` — lean-ctx never downloads
or manages one. Headless diagnostics do not exist, and the safe two-phase rename
and safe-delete operations need a running IDE backend, reporting a
backend-required error otherwise.

Everything else — symbol lookup, callgraph, dependency graph, impact — is
tree-sitter and graph approximation. Matches are name-based, NOT reference-exact,
so an "all usages" answer from those tools is a candidate list rather than a
complete one. When a rename must be correct rather than plausible, use a genuine
LSP client and keep these for orientation.
