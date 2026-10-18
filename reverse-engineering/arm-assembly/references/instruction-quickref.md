# AArch32 instruction interpretation

Use the actual encoding and processor features to resolve ambiguous mnemonics. The expressions below use 32-bit\
bitvectors, not unrestricted C arithmetic. Overflow, shifts by the word width, and memory alignment need architectural\
interpretation.

## Conditions and flags

`cmp a,b` sets flags from subtraction without retaining the result. `tst a,b` tests a bitwise conjunction. A\
flag-setting suffix does not mean every flag changes: logical operations typically preserve V; shift carry depends on\
encoding. Track flags individually when reconstructing a predicate.

| Condition           | True when                                    | Typical comparison after `cmp a,b` |
| ------------------- | -------------------------------------------- | ---------------------------------- |
| EQ / NE             | Z / not Z                                    | equal / unequal                    |
| CS or HS / CC or LO | C / not C                                    | unsigned greater-or-equal / less   |
| HI / LS             | C and not Z / not C or Z                     | unsigned greater / less-or-equal   |
| GE / LT             | N equals V / N differs from V                | signed greater-or-equal / less     |
| GT / LE             | not Z and N equals V / Z or N differs from V | signed greater / less-or-equal     |
| MI / PL             | N / not N                                    | negative / nonnegative result      |
| VS / VC             | V / not V                                    | signed overflow / no overflow      |

For subtraction, C represents no borrow. Thus `sbc d,a,b` computes `a - b - (1-C)`. `adc` includes carry; reverse\
subtraction exchanges the operands. `rsb d,a,#0` forms two's-complement negation. The signed and unsigned\
interpretations of the same register bits can choose different branches.

In ARM state many instructions carry a condition suffix. A conditionally executed load or return belongs to that\
predicate. In Thumb, inspect IT state and conditional branches rather than assuming every printed suffix is an\
independent branch. A Thumb instruction may update flags differently inside an IT block; decode the actual encoding.

## Values and bit operations

| Family                            | Interpretation to test                                                                    |
| --------------------------------- | ----------------------------------------------------------------------------------------- |
| MOV / MOVW / MOVT                 | Copy or construct a value; MOVW clears the upper half, MOVT replaces it                   |
| ADD / SUB / ADR                   | Integer arithmetic or address formation, depending on later uses                          |
| AND / ORR / EOR / BIC / MVN / ORN | Intersection, union, XOR, bit clearing, complement, or union with complement              |
| LSL / LSR / ASR                   | Left shift, zero-fill right shift, or sign-fill right shift                               |
| ROR / RRX                         | Rotation within 32 bits or one-bit rotation through carry                                 |
| UBFX / SBFX                       | Extract a field with zero or sign extension                                               |
| BFI / BFC                         | Replace or clear a field while preserving other bits                                      |
| CLZ                               | Count leading zero bits; inspect zero-input behavior before assigning logarithmic meaning |
| MUL / MLA / MLS                   | Low-width product, add-product, or subtract-product                                       |
| UMULL / SMULL                     | Unsigned or signed full-width product into low/high destination registers                 |
| UMLAL / SMLAL                     | Accumulate a full-width product into a register pair                                      |
| UDIV / SDIV                       | Division where the selected core and instruction state implement it                       |

Integer divide is not available on every ARMv7 implementation. Confirm core capabilities rather than inferring them\
from the ISA label. Immediate encodings differ between ARM, Thumb16, and Thumb-2. A mnemonic does not guarantee the\
same constant can be encoded in each. A `movw`/`movt` pair can construct a scalar or a pointer; dereferences and\
relocations discriminate the two.

## Memory and addressing

`ldrb` and `ldrh` zero-extend; `ldrsb` and `ldrsh` sign-extend. Stores retain only their access width. Word accesses\
may carry integers, pointers, packed flags, or copied bytes. `ldrd` can represent one value or adjacent fields.\
Endianness governs byte interpretation and multiword values; a register-pair notation alone does not establish memory\
order.

| Address form             | Effective address and base update                                                             |
| ------------------------ | --------------------------------------------------------------------------------------------- |
| `[base,#offset]`         | Access base plus offset; preserve base                                                        |
| `[base,#offset]!`        | Update base by offset, then access the new base                                               |
| `[base],#offset`         | Access old base, then update base by offset                                                   |
| `[base,index,lsl #k]`    | Access base plus index scaled by a power of two                                               |
| PC-relative literal load | Compute architectural PC, apply encoding-specific alignment and offset, then read the literal |

For common ARM-state reads, PC is the instruction address plus eight; for common Thumb forms it is plus four. Some\
Thumb literal/address forms align that value to four bytes. Use the instruction's rule before calculating its target. A\
literal may be a scalar, relocation, pointer, or inline data, so follow its uses before declaring a string reference.

LDM/STM transfer registers in architectural register order. IA/IB increment; DA/DB decrement; `!` requests writeback.\
Compute the whole register-set transfer before assigning individual addresses. Push/pop commonly encode a descending\
stack. Writeback and loaded base-register interactions require checking the encoding's restrictions.

## Calls, returns, and tables

`bl` records a return address; `blx` has immediate and register forms with different state-selection rules. `bx` uses\
an interworking target, commonly `lr` for return. A plain `b` can be a tail call. Loading `pc` can return or dispatch\
indirectly; derive its destination from the actual source memory.

For `tbb` and `tbh`, decode the table base and unsigned entry width, then form the PC-relative destination with the\
required scaling. Check every recovered destination against an instruction boundary and executable mapping. A jump\
table is data even if linear disassembly produces plausible instructions there.

## A discriminating trace

```asm
cmp r0, #0
moveq r1, #7
bxeq lr
mov r1, #9
bx lr
```

For zero, the first assignment and first return execute. For nonzero, both conditional instructions are skipped. A\
reconstructed inequality on that early return contradicts the instructions. Check the emitted bytes and preceding flag\
writer before blaming a compiler, type, or decompiler. This example is synthetic and does not establish runtime tool\
coverage.
