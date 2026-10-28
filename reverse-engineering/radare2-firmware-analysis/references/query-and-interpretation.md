# Query and interpretation patterns

Verify installed help before extending a command sequence; core and plugin dispatch syntax can differ by version. The\
commands below operate on analysis state, while the input remains open without write mode.

## Load a binary

Resolve `binary_path` to an absolute supplied filename before running these shell commands. Use the available\
executable name if it is `radare2` rather than `r2`.

```sh
r2 -N -e bin.relocs.apply=true "$binary_path"
```

`-N` skips user settings and scripts, making configuration easier to reproduce. Record explicit settings and installed\
plugins because this option does not remove all environmental differences. Inspect `iIj`, `iSj`, and `isj` before\
changing architecture or loading settings.

For a raw little-endian ARM32 image whose evidence establishes load address `0x8000`:

```sh
r2 -N -n -a arm -b 32 -m 0x8000 -e cfg.bigendian=false "$binary_path"
```

These architecture and address values are an example, not defaults for arbitrary firmware. `-n` bypasses binary-format\
information; `-m` maps the file at the selected address. Keep ELF loader mappings for executables and relocatable\
modules unless evidence requires a separate loading hypothesis. For an ARM function confirmed to be Thumb, inspect\
`afB?` and set `afB 16` at that function. Verify the resulting instruction boundaries and branch destinations.

## Navigate analysis

```text
iIj                    binary architecture, bitness, base address, ABI
iSj                    sections and address mappings
isj                    file-derived symbols
af @ 0x8000            analyze a justified entry and discovered callees
aa                     analyze symbols, imports, and entry points
aflj                   discovered functions as JSON
afij @ 0x8000          function entry, size, and analysis details
pdfj @ 0x8000          bytes and disassembly
agfj @ 0x8000          basic blocks and graph edges
axtj @ 0x8000          known incoming references
axfj @ 0x8000          references from this address
agcj @ 0x8000          call graph rooted at this function
agCj                   global call graph
pdc @ 0x8000           native pseudo-disassembly
LDj                    installed decompiler command names
La                     installed architecture plugins
Lc                     installed core plugins
```

Replace `0x8000` with a verified function entry in the current mapping. Prefer literal hexadecimal addresses after\
resolving symbols so command construction cannot execute symbol-supplied syntax. Use `?v $$` after seeking and compare\
the result with `afij` and the requested entry. Follow references and pointer-table registrations before searching\
exported C text. Expand analysis when callers are missing, then distinguish absent evidence from proven absence.

Build the call graph before claiming a flow across functions, such as one call running before another. Use `agcj` to\
walk one function's callees and `axtj` to walk its callers. Export `agCj` when you need the shape of a large subsystem\
at once; a graph format such as `d` (Graphviz DOT) renders it for a person. A static graph stops at indirect dispatch:\
an edge through a function-pointer or dispatch table resolves only to the table slot. Report such an edge as\
undecided until the code that fills the table, or a runtime observation, settles it.

## Retain evidence

Inside an interactive session, choose a fresh output directory with a simple path that radare2 can parse unambiguously.\
The following `exports` directory must already exist; use a separate directory for each run.

```text
?V > exports/version.txt
iIj > exports/binary.json
iSj > exports/sections.json
isj > exports/symbols.json
aflj > exports/functions.json
afij @ 0x8000 > exports/function.info.json
pdfj @ 0x8000 > exports/function.instructions.json
agfj @ 0x8000 > exports/function.graph.json
axtj @ 0x8000 > exports/function.xrefs.json
pdc @ 0x8000 > exports/function.c
PS exports/session.r2
```

Check redirection syntax against the installed version and inspect each file after export. Record the original hash,\
mapping, plugin identities, command sequence, diagnostics, and manual changes alongside these files. Require\
instruction and graph evidence even when a plugin emits readable C. At conditional returns, check the processor's\
predicate, register effects, and branch destination against each competing interpretation.

## Conditional-return disagreement

Consider this synthetic ARM sequence, where `r4` points at a record:

```asm
cmp r0, #0
ldmibeq r4, {r0, r1}
bxeq lr
mov r0, #1
bx lr
```

On equality, both the load and early return execute. Otherwise both are skipped. A decompiler rendering\
`if (r0 != 0) return ...` for that early return reverses the predicate. Trace Z from `cmp`, identify intervening flag\
writes, and compare both paths before assigning C meaning. Record affected tool/plugin versions and bytes; a successful\
export does not establish correct C. The example is an interpretation check, not a claim that every version has this\
defect.
