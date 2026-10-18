---
name: binary-analysis-patterns
description: Interpret compiled binaries and recover control flow, function signatures, data structures, and compiler idioms. Use when explaining disassembly or decompiler output, resolving conflicting type hypotheses, or identifying binary mitigations and their runtime effects.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Binary Analysis Patterns

Recover a defensible model of compiled behavior. Treat pseudocode, symbol matches, and familiar instruction sequences\
as hypotheses until instructions and surrounding uses corroborate them.

## Establish the Analysis Contract

Record the binary hash, format, architecture, endianness, address width, load assumptions, and the requested behavior.\
For raw images, keep candidate load maps separate until references, entry behavior, and data accesses support one.\
Preserve the original and work in a separate analysis database.

Discover the selected disassembler or decompiler, supported architectures, version, and available scripting or MCP\
operations. Static interpretation needs no target execution. Dynamic confirmation additionally needs an appropriate\
debugger or emulator and a controlled target environment. Check only the selected route.

Report missing tools, loaders, architecture modules, or debug/type inputs with their purpose. Verify host-specific\
package names against the host package catalog or official installation documentation before recommending them.\
Recommend installation or configuration; assume neither administrative access nor permission to change the host.\
Continue byte-level interpretation where tooling gaps allow it.

## Recover Behavior Iteratively

1. Map entry points, exports, imports, strings, cross-references, executable regions, and likely data boundaries. Keep\
   locations as file offsets, analysis addresses, or runtime addresses with the mapping stated.
2. Select a function that answers the requested question. Check its boundaries, incoming edges, instruction mode, and\
   calling convention before trusting its pseudocode.
3. Read [control flow and compiler idioms](references/control-flow.md) for branches, loops, arithmetic, indirect\
   dispatch, tail calls, or ambiguous code/data boundaries. Reconstruct conditions using actual operand widths.
4. Read [signatures and data recovery](references/types-and-signatures.md) before assigning prototypes, naming fields,\
   or replacing decompiler variables. Collect caller, callee, and memory-access evidence first.
5. Apply one focused annotation or type change. Redecompile and inspect callers, changed expressions, and newly exposed\
   contradictions. Revise or revert a hypothesis that makes other uses less coherent.
6. Validate decisive behavior with independent cross-references, instruction semantics, or bounded concrete tests in an\
   authorized environment. Mark unexecuted paths and assumptions explicitly.

For protection indicators or runtime address/permission differences, read\
[mitigation interpretation](references/mitigations.md). Identification explains analysis constraints; it does not\
establish exploitability or require weakening host safeguards.

## Preserve and Deliver the Model

Save names, signatures, layouts, comments, and their confidence in the analysis database. Export annotations or record\
a reproducible application procedure when the tool permits it. Verify saved state by reopening or checking an\
independent export before declaring persistence complete.

Report the requested behavior, evidence locations, recovered interfaces and layouts, validation performed,\
contradictions, and unresolved paths. Distinguish neutral role names such as `candidate_decoder` from verified\
identities. Completion means that each consequential claim has supporting evidence or an explicit uncertainty, and\
another analyst can find and reproduce the model.

Tool-specific project operations can use `ghidra-firmware-analysis` or `radare2-firmware-analysis` when available. This\
package supplies the interpretation loop independently; their installation is not required to use it.
