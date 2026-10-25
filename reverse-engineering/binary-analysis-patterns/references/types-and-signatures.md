# Signatures and Data Recovery

## Recover an Interface from Both Sides

Establish the target ABI, compiler conventions, and possible custom convention. Common integer argument registers\
include RDI, RSI, RDX, RCX, R8, R9 for System V AMD64; RCX, RDX, R8, R9 for Microsoft x64; X0-X7 for AArch64; and R0-R3\
for common AAPCS32 calls. Floating-point, aggregate, variadic, and hidden return-pointer rules require the actual ABI.\
These integer summaries are not complete function declarations.

Inspect several callers and the callee. Distinguish incoming arguments from register residue, scratch space, stack\
spills, and values initialized before use. Recover stack alignment, return storage, callee-saved registers, and whether\
the function actually returns. A mistaken `noreturn` annotation can erase real flow downstream.

Separate three claims: function identity, declaration, and data layout. A recognizable implementation or similarity\
match does not prove its prototype. A header from another ABI does not prove the target layout. Track provenance and\
confidence independently for each claim.

## Build Types from Accesses

For each pointer candidate, collect offset, access width, read/write role, and every function using that offset.\
Repeated fixed offsets suggest a structure; scaled indexing suggests an array; pointer chasing suggests a linked\
object. Distinguish a structure pointer from an interior pointer by following its derivation.

Use neutral fields such as `field_08` until operations justify roles. Allocate explicit gaps rather than inventing\
members to fill unknown bytes. Confirm alignment, packing, unions, flexible arrays, embedded objects, and target\
pointer width. An 8-byte load can be a pointer, integer, two packed fields, or bit representation.

Recover signedness from extension and comparisons, not width alone. Byte access can represent a flag, character, packed\
integer, or buffer element. Floating-point operations provide stronger evidence than a 4-byte memory read.

For an indirect call, trace the object pointer and table index. Confirm whether the table is a vtable, callback array,\
switch table, or import structure. Multiple inheritance or interface adjustment may shift the apparent object base.\
Record verified slot behavior before assigning a class hierarchy.

## Refine Decompilation Without Concealing Evidence

1. Save the original inferred declaration and the evidence for the proposed change.
2. Establish where the variable's value comes from. A parameter takes its type from the function's declaration, and a\
   call result takes it from the callee's return type. Change the type at that source; most decompilers re-derive a\
   type changed elsewhere.
3. Change the narrowest justified component, such as one parameter type or one field offset.
4. Redecompile the function and inspect all affected callers and writes.
5. Check pointer scaling, casts, stack balance, hidden arguments, and return-value uses.
6. Preserve the change only if it explains the observations without introducing contradictions.

A newly elegant decompilation is a diagnostic signal, not proof. Forced casts, extensive invented padding, or\
unexplained argument disappearance suggest a wrong type, boundary, or ABI. A local array smaller than a write into it\
usually marks one aggregate split into several variables; type the full span and re-decompile. Split an incorrect\
merged variable where supported, and preserve the raw instruction evidence for tool limitations.

Use known headers, symbols, type archives, donor libraries, or debug information only after matching architecture, ABI,\
version, and relevant build options. Review similarity candidates manually using unique constants, call shape, and\
control/data flow. Common wrappers and short routines generate misleading matches.

## Persist a Recoverable Result

Record address-space and image identity with each annotation. Export the reviewed changes when the tool supports it and\
verify representative names and structures after reopening. Preserve rationale for tentative fields, donor pins, and\
rejected interpretations separately from confirmed facts. Never copy runtime absolute addresses into a rebased database\
without converting through the recorded mapping.
