---
name: radare2-firmware-analysis
description: Reverse-engineer firmware binaries with radare2. Use to discover functions and references, compare decompilation against instructions or another tool, investigate processor-specific control flow, match stripped functions with donor signatures, or preserve and restore analysis.
license: MIT
compatibility: Requires radare2, installed locally or available through a user-provided container runtime and vetted image. Decompiler plugins are optional.
metadata:
  author: Joonas Onatsu
---

# Radare2 firmware analysis

Use radare2 to recover firmware logic with instruction-correlated function, reference, and control-flow evidence. Start\
from a supplied binary and research question, rather than assuming a processor, repository, or container image.

## Establish the execution environment

Check for `r2` or `radare2`, then inspect its version and `-h` output. Use the available executable name throughout the\
session. If neither exists, identify an available container runtime and a user-provided or reviewed image. Report a\
missing execution mechanism instead of assuming an installed tool or pulling an arbitrary image. Read the host\
distribution/version and query its package catalogue before recommending a package. Explain what the missing executable\
or plugin enables, and present installation as a recommendation. Use existing authorization for setup; do not assume\
administrator access or install tools silently.

For container execution, inspect the image identity and source before running it. Use available Dockerfile lint and\
image scanning tools when vetting a new image; record any missing scan coverage. Mount inputs read-only, disable\
networking, bound resources, and write results to a separate writable directory. On POSIX hosts, map the host UID:GID\
and supply a writable temporary home to avoid root-owned results. Record the exact image identity, runtime options, and\
radare2 version.

Read existing investigation notes and preserve previous analysis before starting a replacement session. Record the\
binary hash, file format, research targets, and a fresh output location using available host tools. Open for static\
analysis without write or debugger options. Use absolute input paths and quote shell arguments; validate addresses or\
symbol expressions before constructing radare2 commands.

## Confirm the loading model

For ELF files, inspect `iIj`, `iSj`, and `isj` for architecture, bitness, byte order, sections, and symbols. Load\
relocations with `-e bin.relocs.apply=true` when examining relocation-dependent references. Executable virtual\
addresses and relocatable module offsets are different coordinates; preserve the loader's section mappings. A runtime\
module address is evidence for a particular loaded instance, not an automatic replacement ELF base.

For raw firmware, establish architecture, bitness, byte order, and load address from headers, boot evidence, or known\
instruction sequences. Use installed help to confirm `-n`, `-a`, `-b`, `-m`, and `cfg.bigendian` before overriding\
them. Keep uncertain load addresses as separate analysis hypotheses and record each mapping. Check decoded instructions\
and branch targets before accepting a mapping. Read [query and interpretation patterns][patterns] for loading and\
function-query commands.

On mixed-mode architectures, verify individual regions instead of forcing one instruction mode over the whole image. An\
ARM Thumb decoder smoke test does not establish discovery of every ARM/Thumb transition.

## Discover and export evidence

Start with exported symbols, entry points, or a justified address. Use `af @ address` for focused function analysis and\
`aa` when expanding symbol and entry-point coverage. Inspect `aflj`, `afij`, instruction bytes, and graph edges to\
verify function boundaries. Follow incoming references and data registrations when tracing callers or function-pointer\
tables. An empty reference list can reflect incomplete analysis; expand coverage before concluding that a function is\
unused.

Export the requested function entry, instruction bytes and disassembly, control-flow graph, references, and any C-like\
rendering. Keep ELF symbols separate from inferred names and preserve the commands used to generate each artifact. Read\
installed help and inspect `LDj` before selecting a decompiler. Native `pdc` provides pseudo-disassembly with limited\
high-level reconstruction. An installed r2dec plugin may provide `pdd`; an installed r2ghidra plugin may provide `pdg`.\
Verify actual command registration instead of assuming that book examples match the installed plugin.

Check the resolved address against the requested function entry after every seek. A failed seek can leave the previous\
function selected, producing plausible output for the wrong target. Check exit status, diagnostics, parseable exports,\
and plugin availability before marking a run complete. Retain failed-run evidence and retry in fresh output state after\
correcting the cause.

## Interpret and preserve results

Compare identical binary hashes, coordinate mappings, and function entries across tools. Resolve disagreements using\
instruction bytes, processor conditions, and control-flow edges. Generated C is an interpretation, not proof of the\
firmware's behavior. r2ghidra shares Ghidra's decompiler engine; its output does not independently corroborate that\
engine. Record each conclusion with its address, supporting evidence, confidence, and unresolved alternatives. When\
predicates disagree, trace the actual flag-setting instruction and every predicated instruction through both outcomes.\
Read [the conditional-return example][patterns] for a generic ARM failure case. Refine inferred names and types from\
callers, accesses, and constants; export before each consequential revision. Check changed interpretation against the\
original instructions and revert a hypothesis that creates contradictions.

Read [matching and persistence][metadata] when building donor signatures, defining types, or restoring annotations.\
Treat signature hits as candidates until instructions and context corroborate their identities. Preserve a reviewed\
session export with the input hash, version, mapping, and plugin identity before closing an annotated session. Replay\
into fresh state and verify required function entries, names, and types before continuing. Use the target workspace's\
documentation conventions for durable findings and source pointers.

Completion means the requested evidence is usable, relevant annotations are preserved, and conclusions state their\
limits. Keep this workflow within authorised static analysis; firmware modifications or live-device operations require\
their own scope.

## References

[metadata]: references/matching-and-persistence.md
[patterns]: references/query-and-interpretation.md
