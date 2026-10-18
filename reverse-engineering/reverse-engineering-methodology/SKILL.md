---
name: reverse-engineering-methodology
description: Plan and conduct evidence-driven reverse engineering of binaries or firmware. Use when starting an investigation, triaging unknown artifacts, choosing static versus dynamic analysis and specialist tools, comparing builds, or deciding the next experiment when an analysis stalls.
license: MIT
compatibility: Triage uses available file-format and binary inspection tools. Decompilers, emulators, debuggers, protocol tools, and solvers are optional routes whose prerequisites must be checked for the selected target.
metadata:
  author: Joonas Onatsu
---

# Reverse-engineering methodology

Turn a bounded question about an unknown program into a sequence of discriminating observations. Select the next\
experiment from evidence, uncertainty, execution feasibility, and the requested result. This skill owns the\
investigation process; specialist skills supply deeper interpretation and tool operation.

## Establish the question and preserve the input

Identify the supplied artifact, existing research, expected output, and operations already authorized. Ask for a\
missing objective only when it changes what behavior must be established. Inventory original binaries/images, extracted\
files, saved tool projects, traces, annotations, and previous failed approaches. Hash inputs and preserve original\
bytes; perform extraction, mutation, or uncertain loading in separate working state. Choose output locations from the\
consuming workspace's conventions rather than imposing a directory tree.

Record the question as an observable claim, such as which input reaches a branch, how a message is parsed, or where a\
field is validated. Identify the evidence that would confirm or contradict it and the first stopping condition. An\
investigation can finish with a bounded explanation or a precise blocker; it need not culminate in exploitation.

## Triage and classify

Discover available tools and inspect their version/help before selecting commands. Recommend missing prerequisites with\
their purpose and host-appropriate installation/configuration guidance. Do not assume privileges or silently install\
dependencies. Optional tools are needed only for the selected route.

Use file headers and mappings to establish format, architecture, bitness, byte order, ABI, symbols, imports, sections,\
relocations, and plausible entry points. For ELF, `file`, `readelf`, `nm`, and `strings` can provide leads; confirm\
tool syntax and select equivalent format-aware tools for PE, Mach-O, or other formats. Keep symbol-table stripping\
separate from dynamic exports or debug information that may survive. Record mitigation indicators separately from\
runtime enforcement; a host's settings do not establish a foreign target's state.

For containers or blobs, inspect headers and boundaries before extraction. Signature hits and entropy changes are\
leads, not proof of a filesystem, compression, or encryption. Use recognized-format validators and inspect extracted\
bytes. Preserve file offsets, virtual addresses, load bases, and runtime addresses as distinct coordinates. For\
firmware engagement stages, consult [firmware investigation stages](references/firmware-investigation-stages.md).

## Choose one evidence-producing route

| Current question or obstacle                                         | First route and specialist depth                                               |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Understand native control/data flow                                  | Instructions and references; `binary-analysis-patterns` for compiled idioms    |
| Query or refine a saved Ghidra program                               | `ghidra-firmware-analysis`, including signatures, types, and manual refinement |
| Inspect functions, compare renderings, match donors, retain r2 state | `radare2-firmware-analysis`                                                    |
| Interpret ARMv7 ARM/Thumb instructions and calling effects           | `arm-assembly`                                                                 |
| Identify and validate a cryptographic construction                   | `crypto-analysis`                                                              |
| Run a target or bounded routine under QEMU and inspect runtime state | `qemu-emulation`                                                               |
| Find inputs/path conditions for a small check                        | `symbolic-execution-tools`, using angr or Triton when justified                |
| Recover a custom interpreter's virtual ISA and program               | `vm-and-bytecode-reverse`                                                      |
| Analysis changes under a debugger/VM, or code is obscured            | `anti-reversing-techniques`                                                    |
| Recover a message format/state from traffic                          | `protocol-reverse-engineering`                                                 |
| Explain artifacts in a process/system memory capture                 | `memory-forensics`                                                             |

A missing specialist does not block basic progress: classify the input, collect focused instructions/references, state\
the unresolved question, and identify the required capability. These routes are depth choices, not required\
dependencies. For static analysis, start at imports, meaningful strings, entry points, symbols, or justified addresses\
and follow both code and data references. Decompilation supplies a hypothesis; inspect instructions when casts, merged\
variables, indirect calls, or boundary effects make that hypothesis uncertain.

Before dynamic execution, establish whether the environment can supply the kernel, libraries, initialized state,\
peripherals, inputs, and isolation the target needs. Distinguish unsupported hardware from missing packages and\
intentional environment detection. Prefer a bounded routine when the whole image cannot run faithfully. Do not\
substitute arbitrary external tool images or assume an MCP wrapper bundles its underlying executables.

## Refine hypotheses through experiments

Read [evidence and experiments](references/evidence-and-experiments.md) when tracking uncertainty, comparing builds,\
resolving tool disagreements, or choosing a next experiment after failure. Maintain competing explanations and choose\
an observation that separates them. Confirm a concrete baseline before changing types, hooks, branch conditions, or\
environment models. Record how each intervention changes the model and which observations still apply to original\
behavior.

For every pass, preserve useful labels/types and update the investigation record with evidence, uncertainty, failed\
approaches, and the next discriminating step. Do not discard an unsuccessful experiment's diagnostics. A clean run,\
attractive pseudocode, similarity hit, or solver witness alone does not establish the research claim.

## Complete and hand off

Deliver the answer with input identity, coordinates, supporting bytes or observations, confidence, alternatives,\
coverage limits, and reproducible commands or saved analysis. State which claims remain inferred or externally\
reported. Verify selected saved annotations and outputs can be reopened or replayed before retiring earlier working\
state. Respect the authorized scope for active network tests, live hardware, acquisition, code execution, and byte\
modifications; reuse existing authorization, and identify any new action that needs a separate decision. Completion\
means the agreed question is answered to its stated evidence bar or the exact missing capability/input is documented.
