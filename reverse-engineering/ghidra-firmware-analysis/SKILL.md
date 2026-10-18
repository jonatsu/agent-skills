---
name: ghidra-firmware-analysis
description: Reverse-engineer firmware and native binaries with Ghidra. Use to import images, investigate functions and references, iteratively improve decompilation through names and types, generate or apply function signatures and type metadata, or preserve and resume analysis through GUI/MCP or headless scripting.
license: MIT
compatibility: Requires Ghidra and its supported Java runtime. GUI automation needs a compatible MCP extension and bridge; Python scripting needs compatible PyGhidra and CPython. Java scripts are an alternative. Containers are optional.
metadata:
  author: Joonas Onatsu
---

# Ghidra firmware analysis

Recover behavior from the supplied binary or saved program, guided by a concrete research question. Use the program\
database, instruction listing, and decompiler together; readable C is a model to test.

## Establish the environment and preserve work

Discover the supplied installation, version, supported Java runtime, and available GUI or headless interface. Recommend\
missing packages, runtimes, or extensions with their purpose and verified compatibility. Use the host's package\
metadata and the selected release's documentation; do not assume sudo or install silently. Check PyGhidra and\
compatible Python only for a Python execution path; a GUI bridge may use Python without PyGhidra. Check the bridge's\
own dependencies separately from those of the Ghidra JVM.

Prefer an available native GUI/MCP session for interactive refinement, with LaurieWired/GhidraMCP as the preferred\
integration. Read [GUI and MCP operation](references/gui-and-mcp.md) before using or configuring that route. Use\
[headless execution](references/headless-execution.md) for imports, bulk export, or scripts unavailable over MCP.\
Choose one route that answers the question rather than requiring every optional integration. If a vetted container is\
supplied, mount inputs read-only, separate writable projects/results, bound resources, and map ownership. Discover its\
actual launchers; neither Docker nor a particular host OS is assumed.

Inventory existing programs, names, comments, types, archives, and exports before rebuilding analysis. Record input\
hashes and architecture evidence. Close project sessions before taking a consistent project backup or lossless program\
archive, then verify that the preservation copy opens. A fresh import or exported C file cannot recover unrecorded\
annotations. Use separate project copies for uncertain mappings or metadata trials.

## Establish the loading model

For recognized executables, inspect detected language/compiler IDs, mappings, symbols, and relocations. For raw images,\
justify architecture, bitness, byte order, instruction mode, load address, and mapped ranges. Check instruction\
decoding and branch targets before accepting a mapping; retain competing hypotheses separately. Relocatable module\
offsets and runtime module addresses are different coordinates. Read the loader's actual diagnostics; a saved program\
does not imply clean relocation or completed analysis.

## Navigate evidence before naming

Start from a known import, exported symbol, meaningful string, entry point, or supported address hypothesis. Query\
callers, callees, incoming/outgoing references, initialized data, and pointer-table registrations. A text search\
through exported C misses indirect calls and data relationships. An empty reference result may mean incomplete\
analysis, so inspect instructions and analysis coverage first.

Read [symbol and structure recovery](references/symbol-and-struct-recovery.md) for missing names or layouts. Infer\
roles from argument effects, constants, strings, ownership, and caller/callee relationships. Separate file symbols,\
automated matches, and analyst hypotheses; record address, evidence, confidence, and alternatives. Intuition chooses\
the next hypothesis, not its truth status.

## Enrich metadata and refine the rendering

Read [FunctionID and type metadata](references/functionid-and-typeinfo.md) before generating or applying donors,\
function signatures, header-derived archives, or recovered structures. Function identity, prototype, calling\
convention, and layout are separate claims. Validate architecture/ABI, argument and return storage, widths, alignment,\
and field offsets before propagation. Inventory existing user annotations and the pre-application names/types/failures\
so effects and rollback are visible.

Work from known callee boundaries into callers. Correct one supported type or signature, redecompile, then inspect both\
the intended improvement and unrelated branches for propagation errors. Rename from context as understanding grows, and\
revise names when stronger evidence arrives. Read the\
[manual refinement loop](references/manual-decompilation-review.md) for merged variables, missing operations,\
obfuscation, and runtime corroboration. Reject a pleasing rendering that contradicts instruction effects or a caller's\
argument preparation. Export accepted annotations with their source and target identity; test reopening before treating\
them as durable.

## Export and recover

The bundled [Python exporter](scripts/decompile_all.py) and [Java exporter](scripts/DecompileAll.java) run inside\
Ghidra with a loaded program and one fresh output filename. They do not run as ordinary standalone programs. Both\
attempt every function, use a 60-second per-function timeout, retain failure diagnostics, and report counts. They\
create output exclusively, honor cancellation, and release the decompiler interface. A cancelled export can remain\
partial; preserve it as incomplete evidence and retry to a fresh destination.

Distinguish auto-analysis limits from per-function decompiler limits. Resolve failures through function boundaries,\
unsupported operations, diagnostics, and instruction evidence before raising budgets. Report failed functions\
explicitly; an emitted file alone does not establish successful decompilation. Before editing scripts, consult\
release-matched stubs/API documentation and check the available Python or Java tooling. Trial write-capable scripts\
against disposable projects before retained analysis.

## Completion

Deliver the requested behavior explanation with addresses, supporting instructions/references, accepted metadata,\
uncertain interpretations, and failed functions. Preserve input/tool/metadata identities, mappings, commands,\
diagnostics, annotations, and next questions using the consuming workspace's conventions. Save deliberate edits, reopen\
the program, and verify representative names, signatures, types, and comments. Keep firmware-byte modifications or\
live-device work within their separately authorized scope.
