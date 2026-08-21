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
