# Control Flow and Compiler Idioms

## Confirm Instruction Boundaries

Use container metadata, relocations, references, unwind information, and observed execution to distinguish code from\
embedded data. Linear decoding can turn constants into plausible instructions. Recursive traversal can miss indirect\
targets. Resolve disagreement at the bytes and incoming edges before forcing a function.

A frame-pointer prologue is evidence, not a definition of a function. Optimized leaf routines may omit it; shared\
epilogues, exception landing pads, tail calls, and split functions complicate boundaries. An unconditional jump with\
ABI-compatible state may be a tail call. A return-like transfer may instead dispatch through a table.

On ARM, establish ARM/Thumb mode and interworking before decoding. On any platform, confirm pointer width and\
instruction set independently of the analyst host. Host `long` size is not target type evidence.

## Recover Branches and Loops

For x86 `cmp a, b`, subsequent signed conditions interpret flags differently from unsigned conditions. For example,\
`jl` and `jb` differ when the high bit is set. Track which instruction last wrote the consumed flags; intervening\
arithmetic can invalidate a superficial comparison reading.

For each loop, record initialization, condition, body, update, exits, and side effects. A backward edge can also be a\
dispatcher, retry, or exception path. A pre-test loop may place its condition after the body in memory. Recover the\
execution graph before choosing a source-level `for` or `while` rendering.

For a switch candidate, establish:

- The index transformation, including subtraction, masks, and signed or unsigned bounds.
- Entry width, table extent, relocation or relative-base rules, and default path.
- Whether targets are blocks, functions, or data selected for a subsequent indirect transfer.
- How multiple indices share targets and whether any target exits the current function.

A large indirect-dispatch loop might be flattening or a bytecode interpreter. Confirm state updates and context\
accesses before assigning that interpretation. Recover simple native edges locally; detailed virtual ISA recovery can\
use `vm-and-bytecode-reverse` when available.

## Interpret Arithmetic at Its Actual Width

Compilers commonly replace multiplication by constants with shifts, additions, or address-generation operations.\
Recover wraparound and truncation, especially when a 32-bit write zero-extends into a wider register.

Unsigned division by a power of two can be a logical shift. Signed division rounds toward zero and may need a bias\
before an arithmetic shift. A mask implementing unsigned remainder does not generally implement signed remainder for\
negative operands. Check zero, maximum values, high-bit values, and negative values where relevant.

Multiplication by a reciprocal constant followed by a shift can implement division. Infer signedness from the multiply\
variant, extension, high-half use, and correction sequence. Validate a candidate formula against boundary values\
instead of naming an algorithm from the constant alone.

Bit scans require attention to zero input and flags. For example, an unguarded `bsr` result is not a universally valid\
count-leading-zeros implementation. Instructions that look redundant may establish flags used later.

## Recognize Copying and Library Idioms

A loop copying bytes through a terminator suggests a string operation; it does not establish buffer capacity. A\
fixed-count copy may be `memcpy`, an inlined assignment, serialization, or a vectorized loop. Check bounds, aliasing,\
alignment, direction, overlap behavior, and error paths before assigning a familiar library name.

Repeated XOR and table lookups are insufficient to identify cryptography. Collect constants, state dimensions, round\
structure, callers, and known input/output pairs. Optimized or inlined library routines can span several recovered\
functions. Preserve a descriptive name when exact identity remains uncertain.

## Validation Worksheet

For each recovered construct, record its start and exits, operand widths, data dependencies, memory effects, and a\
counterexample that could disprove the current interpretation. Compare pseudocode to instructions at the\
counterexample. A convenient high-level rendering is acceptable only while it preserves those semantics.
