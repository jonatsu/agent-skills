---
name: arm-assembly
description: Interpret 32-bit ARMv7 ARM and Thumb disassembly. Use to reconstruct arguments and stack frames, resolve instruction-mode or signedness errors, recover structures and control flow, or trace privileged ARMv7-A firmware code.
license: MIT
compatibility: Requires supplied AArch32 disassembly or an ARM-capable disassembler. Runtime tracing additionally requires a compatible debugger and execution environment.
metadata:
  author: Joonas Onatsu
---

# Reading ARMv7 assembly

Recover behavior from AArch32 instructions and evidence, then improve names, types, and reconstructed logic. This skill\
covers ARMv7 ARM/Thumb, including ARMv7-A system code. AArch64 conventions require different guidance.

## Establish the interpretation

Record the binary hash, relevant addresses, file-to-memory mappings, endianness, processor profile, and available\
symbols. Check file headers, ELF attributes, entry points, and known instruction sequences rather than assuming\
little-endian ARMv7-A. Check the selected disassembler's executable, version, ARM support, and installed help before\
generating output. When a tool is missing, inspect the host distribution and its package catalogue before recommending\
a package. Explain the capability it enables; installation is a recommendation, with no assumed sudo permission.\
Existing disassembly is sufficient for interpretation when its bytes, mode, and coordinate mapping are available.

Distinguish ARM state, with four-byte instructions, from Thumb, with two- and four-byte instructions. For interworking\
branch targets, bit zero encodes Thumb state; the actual instruction address excludes that bit. A plain aligned address\
in a listing does not establish ARM state. Inspect mapping symbols, branch type, and surrounding code. On a bad decode,\
test a separate mode or mapping hypothesis and compare valid branch destinations and literal references.

## Trace one question through a function

1. Identify entry, exits, callers, and the concrete question that the function must answer.
2. Track register definitions, stack deltas, flags, memory accesses, and call effects across each relevant path.
3. Infer candidate argument roles, field offsets, signedness, and return values from these observations.
4. Apply a focused name, prototype, or structure change in the analysis tool when authorized.
5. Recheck instructions and all affected callers after the interpretation changes.

A hypothesis becomes useful when it explains several independent uses without contradicting any observed instruction.\
Name uncertain roles tentatively. Revert a type that hides accesses, changes widths incorrectly, or makes callers\
inconsistent. The [instruction reference](references/instruction-quickref.md) supports flag, addressing, and\
control-flow interpretation. For privileged instructions, exceptions, memory translation, or synchronization, read the\
[system-code interpretation reference](references/armv7a-programmers-guide.md).

## Recover the calling convention

Under base AAPCS32, `r0`–`r3` carry initial argument words and scratch values; `r0` commonly carries the result.\
Alignment, multiword values, aggregates, and hidden result pointers change the allocation. Do not count registers as\
source arguments. An argument may be unused, saved before a call, spilled, or passed on the stack. Inspect callers and\
incoming stack slots before deciding arity. A composite larger than four bytes generally uses caller-provided result\
storage under base PCS. VFP parameter passing and platform-specific conventions need separate confirmation from\
attributes and call sites. A function built with `-pg` calls `__gnu_mcount_nc` before its own code. The hook preserves\
`r0`–`r3`, so registers the body reads after that call still hold the function's arguments, even when a decompiler\
shows them as the hook's result.

Preserve `r4`–`r8`, `r10`, `r11`, and `sp` across conforming calls; `r9` has a platform-defined role. Treat `r12` and\
condition flags as volatile, including across linker veneers. Register `r13` is `sp`, `r14` is `lr`, and `r15` is `pc`.\
Frame-pointer choice is compiler-dependent; `r7` or `r11` may appear, or no frame pointer may exist. Maintain four-byte\
stack alignment and eight-byte alignment at a public interface; verify actual call-boundary alignment. Track saved\
`lr`, local allocation, and outgoing argument space before assigning stack-variable offsets. A push of `lr` is evidence\
about preservation, not a proof that the body contains a normal call.

## Corroborate reconstructed behavior

Follow literal loads and constant construction to actual mapped data before naming a register as a pointer. Infer field\
widths from loads/stores, but distinguish signed extension, packed fields, byte copying, and pointer arithmetic. A\
shift or mask loop alone does not identify cryptography; corroborate constants, data flow, and calling context. Track\
flags from the last instruction that actually writes each flag, including predicated operations and IT blocks. Use\
signed and unsigned boundary inputs to test candidate comparisons.

Where safe runtime access exists, stop at relevant calls or branches and compare predicted registers, flags, and\
memory. Check debugger architecture/mode support and execution prerequisites before relying on a trace. Use synthetic\
instruction examples when runtime coverage is unavailable, and label the result as a static interpretation.

Finish with an annotated trace or reconstructed pseudocode that cites addresses, bytes, mode, ABI assumptions,\
validated names/types, contradictions, and untested paths. Preserve annotations and their original hypothesis before\
closing.
