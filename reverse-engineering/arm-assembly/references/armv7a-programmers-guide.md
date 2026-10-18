# Interpreting ARMv7-A system code

Use this reference to organize investigation of privileged instructions and boot code. Recover the processor's\
implemented features and runtime state before interpreting implementation-defined fields. ARMv7-M uses a different\
exception model; this reference does not substitute for its documentation.

## Establish privilege and register state

Identify User, System, exception, Monitor, or Hyp mode from a saved CPSR or instructions that change mode. Availability\
of security and virtualization extensions depends on the core and configuration. An exception can switch register\
banks; track the active bank when following `sp`, `lr`, and saved status. FIQ has additional banked registers, but that\
does not remove the need to inspect the handler's preservation obligations.

Use CPSR flags for predicates, T for instruction state, interrupt masks for delivery, and mode bits for bank selection.\
IT state can survive into a status snapshot. Separate APSR-visible arithmetic state from privileged control fields.\
Secure/Non-secure state is a separate dimension from processor mode.

## Decode control-register accesses

For each `mrc`/`mcr`, retain the complete coprocessor, opcode, CRn, CRm, and opcode2 tuple. A CRn value alone cannot\
identify a register. Compare the tuple with documentation for the actual core and extensions. An `mrc` destination of\
`pc` has special effects; inspect the architectural rule instead of treating it as an ordinary load.

| Evidence sought                          | Register families to resolve                                  |
| ---------------------------------------- | ------------------------------------------------------------- |
| Core and optional features               | MIDR, feature identification registers, MPIDR                 |
| MMU, caches, alignment, vector selection | SCTLR and implementation-defined auxiliary controls           |
| Floating-point access                    | CPACR and applicable security controls                        |
| Translation bases and format             | TTBR0, TTBR1, TTBCR                                           |
| Short-descriptor domain checks           | DACR                                                          |
| Abort diagnosis                          | DFSR, IFSR, DFAR, IFAR and extension-specific state           |
| Cache or TLB synchronization             | Maintenance operation encodings, barriers, shareability scope |
| Exception dispatch                       | VBAR and security/virtualization variants                     |
| Address-space or thread identity         | CONTEXTIDR and thread identification registers                |

Do not assume that Cortex-A implementation-defined controls describe another vendor's ARMv7-A core. Record raw values\
before assigning bitfield names so a later interpretation can be corrected.

## Reconstruct a translation

First determine whether translation is enabled and which security/virtualization translation stages apply. For the\
relevant stage, identify short versus long descriptors from control state; address width alone is insufficient.\
Determine the TTBR selection, base masking/alignment, and applicable address-space identifier before reading a table.

For a conventional short-descriptor, full-address-space first-level table, index by VA bits 31:20. A section mapping\
resolves at that level; a coarse table points to a second level indexed by VA bits 19:12. Small pages preserve the low\
twelve offset bits. Supersections, large pages, and reduced first-level tables need their own rules. Classify\
descriptor type before extracting an address; fault entries are not physical pointers.

Inspect access permissions together with control bits, domain mode where applicable, execute-never bits, and memory\
attributes. A permissive domain setting can change the interpretation of AP bits. Long descriptors have different\
layouts and controls. Walk a known mapped address first and compare its result with code/data placement or a runtime\
memory read. Keep virtual, intermediate, physical, and file offsets labelled distinctly.

A control-register write alone does not prove later execution observes the change. Trace required barriers and\
TLB/cache maintenance, including other cores and address spaces where relevant. Avoid inferring a race-free update\
sequence from one instruction in isolation.

## Interpret ordering and cache maintenance

DMB orders specified memory accesses within its scope. DSB additionally waits for completion required by its\
domain/type. ISB synchronizes subsequent instruction execution with context changes; it does not replace data-cache\
maintenance. Resolve the instruction's barrier option, memory type, shareability, and core rules before explaining a\
sequence. Inner Shareable, Outer Shareable, Non-shareable, and full-system scopes are distinct.

For DMA, identify who owns the buffer, which accesses are coherent, and where maintenance reaches. Cache clean,\
invalidate, and clean-and-invalidate are different operations. Discarding dirty data can lose writes. An\
instruction-cache synchronization sequence does not establish that a device sees a DMA buffer. For unknown maintenance\
tuples, preserve their encoding and defer the semantic claim until the core manual resolves it.

## Recover exceptions and interrupts

Look for vector-slot branches, a loaded vector base, status-register saves, bank switches, and exception-return\
instructions. Determine low/high/programmed vectors from control state; a table-shaped byte sequence alone is only a\
candidate. The common ARMv7-A vector offsets are reset 0x00, undefined 0x04, SVC 0x08, prefetch abort 0x0c, data abort\
0x10, reserved or extension-specific 0x14, IRQ 0x18, and FIQ 0x1c. Monitor/Hyp entry and return rules require their\
extension-specific treatment.

Separate exception entry's automatic status/link updates from the handler's software register saves. A return that\
restores status can change mode and instruction state; it is not an ordinary function return. Interpret LR adjustments\
according to exception type and instruction state before assigning the resumed instruction. For an abort, decode fault\
status and determine whether the reported fault address is valid. External/imprecise faults can make the immediately\
preceding instruction an unreliable cause.

Identify the interrupt controller from the platform memory map and driver accesses. Do not assume a universal\
controller base, GIC generation, vector setup, or interrupt-ID assignment.

## Complete the reconstruction

Produce a state transition or address walk with input state, decoded tuples, descriptor bytes, control assumptions,\
resulting addresses or handler destinations, corroborating observations, and unresolved implementation details. Mark a\
speculative configuration explicitly when register snapshots or core documentation are unavailable.
