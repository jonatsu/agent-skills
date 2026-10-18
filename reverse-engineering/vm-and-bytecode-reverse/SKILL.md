---
name: vm-and-bytecode-reverse
description: Recover custom virtual-machine instruction sets and bytecode behavior from interpreters or protected binaries. Use to identify dispatchers, reconstruct virtual state and opcode semantics, extract encoded bytecode, build a disassembler or interpreter, or validate devirtualized logic against execution traces.
license: MIT
compatibility: Requires a disassembler or decompiler for the native interpreter. Dynamic tracing, emulation, SMT solvers, and Ghidra processor modules are optional branches with their own architecture and runtime requirements.
metadata:
  author: Joonas Onatsu
---

# VM and bytecode reverse engineering

Recover the interpreter's virtual instruction semantics before treating its bytecode as a program. This job concerns\
custom bytecode machines, not detecting whether native software runs under a hypervisor. Start from an input image or\
saved analysis, the behavior to explain, and any authorized traces.

## Establish evidence and the analysis route

Record binary/bytecode hashes, extraction ranges, native architecture, address mappings, and the research question.\
Discover available native-code analysis tools, versions, scripting support, and saved projects. Check optional\
trace/emulation engines against the native architecture and required system behavior. Recommend missing tools or\
configuration for the actual host; do not assume sudo or silently install dependencies. Use a static route when\
execution is unavailable, with explicit limits on unresolved runtime decoding or state.

A repeated switch or indirect jump can be an ordinary parser, state machine, or flattened native control flow. Confirm\
a stream of virtual instructions, virtual state, and a repeated fetch/decode/execute relationship. Follow dispatcher\
inputs, table entries, and state updates rather than identifying a VM from visual complexity alone. Read\
[recognition and extraction](references/recognition-and-extraction.md) for competing interpretations and encoded\
streams.

## Recover the virtual machine

Identify the virtual PC, registers or operand stack, flags, memory, call stack, and native-to-virtual entry/exit\
boundary. Keep native and virtual addresses separate in notes and exports. For each reached handler, record opcode\
selection, consumed bytes, operand encoding, state preconditions, data effects, control-flow effects, external\
interactions, and uncertainty. Handler addresses need not map one-to-one to opcodes. Use\
[ISA and handler recovery](references/isa-and-handler-recovery.md) to derive and refine the instruction contract.

Trace a small known input or manually execute a short bytecode sequence before naming the entire handler set.\
Distinguish VM stack traffic from the native stack and distinguish virtual flags from host flags. Test arithmetic\
widths, sign extension, byte order, stack direction, branch origin, and operand-dependent instruction length. Treat\
handler names as hypotheses until native instructions and state effects agree. Unknown handlers remain unknown; do not\
invent familiar instruction semantics from one mnemonic-like pattern.

## Build a decoder and behavioral model

Implement a task-specific decoder from the recovered ISA table, beginning with the bytecode needed for the question.\
Validate lengths, operand bounds, branch targets, unknown opcodes, and truncation before interpreting a stream. Stop or\
mark an uncertain region rather than silently stepping one byte and presenting the remainder as valid code. Preserve\
raw bytes and native handler locations beside each decoded instruction.

For behavior recovery, add an interpreter or lifted representation whose state updates match the observed machine. Make\
external effects explicit and keep native helper semantics separate from virtual operations. Read\
[validation and reconstruction](references/validation-and-reconstruction.md) for differential testing and output\
criteria. Optional symbolic analysis needs its own supported semantics and state; it does not automatically solve\
nested or encrypted VMs. A formal processor module is useful for repeated analysis only after a decoder and instruction\
semantics are established.

## Refine and finish

Compare model and target effects at instruction boundaries. Use the first divergence to revise the ISA or\
initialization, then rerun earlier cases to detect regressions. Retain alternate handler interpretations until evidence\
discriminates them. For nested machines, recover each layer's input/output contract and verify extraction before\
recursing into another layer.

Deliver the virtual state layout, ISA table, bytecode extraction map, decoder/model, relevant control/data flow,\
validation observations, unresolved handlers, and coverage limits. Preserve evidence and research state using the\
consuming workspace's conventions; the installed skill package is not an output directory. Completion means the\
requested bytecode behavior is supported by handler semantics and validation, or its exact blockers are stated. A\
single observed execution does not establish complete path coverage or equivalence of a reconstructed program.
