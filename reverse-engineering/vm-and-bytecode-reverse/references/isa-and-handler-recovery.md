# ISA and handler recovery

## Build the instruction contract

Use one row per distinct decoded instruction form. Several handler addresses can implement the same operation, and one\
handler can select different forms using flags or operands.

| Field                | Evidence to retain                                                                      |
| -------------------- | --------------------------------------------------------------------------------------- |
| Opcode/form          | Raw encoding, dispatch lookup, handler addresses                                        |
| Length and operands  | Fetch increments, operand reads, endianness, signedness, variable-length rules          |
| Input state          | Registers/stack/memory read, required flags, validity preconditions                     |
| Output state         | Values written, width/truncation, flags, memory effects                                 |
| Control flow         | Fallthrough, branch origin/unit, target calculation, calls/returns, halt                |
| Exceptional behavior | Stack bounds, division faults, invalid operands, external helper failures               |
| Validation           | Native instruction range, concrete examples, trace comparisons, unresolved alternatives |

Decode reads before naming operands. A fetched byte may be an index, signed displacement, immediate, or part of another\
field. Determine whether an index selects an instruction, register, table element, or memory address from its eventual\
use. Check whether branch offsets are relative to instruction start, operand end, or the already advanced virtual PC.\
Separate byte offsets from instruction indices and account for the virtual address-space width.

For stack instructions, define exactly when SP increments/decrements, which slot contains the top element, and whether\
arguments/results overwrite or allocate storage. For arithmetic, account for intermediate widths, flag changes,\
sign/zero extension, and wraparound. For calls, recover virtual return addresses and frame layout separately from\
native helper calls.

## Use state differences to refine hypotheses

Select inputs that separate competing meanings: zero, one, maximum unsigned value, sign-bit boundary, and asymmetric\
operands. For subtraction, division, and comparisons, operand order matters; equal operands cannot distinguish the\
alternatives. For loads/stores, use distinct values at neighboring addresses and compare access widths and effective\
offsets. For branches, compare taken and fallthrough cases and inspect whether flags survive intervening handlers. A\
handler that looks like ADD might instead update an address, rolling key, or dispatcher state.

Trace native instructions when decompiler variable merging hides state updates. Record the smallest confirmed operation\
first; defer a high-level name whose broader role remains unproved. Repeatedly revisit callers, handler entry setup,\
and shared epilogues when effects seem inconsistent. Some protectors split one virtual instruction across native\
fragments or fuse several instructions into one handler. Do not infer commercial-protector families from opcode count\
or a single entry sequence.
