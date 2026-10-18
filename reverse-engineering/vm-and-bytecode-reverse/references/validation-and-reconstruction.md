# Validation and reconstruction

## Validate the decoder before the program

Use safe synthetic byte sequences for known forms, unknown opcodes, truncated operands, and boundary-crossing branches.\
Verify that each decoded instruction accounts for exactly the bytes its handler consumes. Keep undecoded regions\
explicit and preserve their raw offsets. A syntactically valid disassembly is not proof that the chosen opcode table or\
entry boundary is correct. For encrypted/stateful bytecode, reset decoding state at a documented entry boundary and\
test replay consistency.

## Differential execution

Initialize a small target trace and the recovered interpreter from the same virtual state. Compare virtual PC,\
registers, stack, flags, memory writes, and external events after each handler. Stop at the first divergence and\
inspect native semantics, operand decoding, or initial state before patching the output. Use both taken and untaken\
branches, arithmetic edge cases, and input/error paths when those are within the recovered scope. Keep native addresses\
in the trace so a disagreement can be traced back to evidence.

For unavailable execution, manually trace native instructions for small sequences and label this as static\
corroboration. Do not describe it as observed target execution. Missing dependencies, handlers, and device effects are\
named coverage limits, not zero-valued defaults. Independent solver or emulator results can corroborate a model only to\
the extent that their assumptions differ.

## Reconstruct useful behavior

Once relevant instruction semantics are stable, build the bytecode CFG from validated branch targets and instruction\
boundaries. Propagate stack heights or register definitions, recover constants, and follow inputs to outputs and\
checks. Keep exception/external edges and unresolved targets visible. For a small arithmetic check, translate the\
confirmed semantics into fixed-width constraints and replay solved inputs. For a large protected routine, prioritize\
the observable behavior asked about rather than promising source-level recovery.

A recovered CFG contains observed or statically established edges, with their origin recorded. A path trace alone\
cannot establish all possible edges, and unknown handlers can invalidate apparent dead-code conclusions. Simplify only\
under explicit assumptions that preserve the required property. Export recovered names, types, and comments back to\
saved native analysis when useful and verify persistence.

## Optional processor modules

A Ghidra SLEIGH module can support repeated work on a stable virtual ISA. Confirm the installation's processor-module\
build tools and syntax against its documentation before creating a module. Define address spaces, instruction decoding,\
register/state layout, and p-code effects from the validated ISA contract. Test decode and semantic effects on the same\
safe cases used for the standalone decoder. An uncompiled specification sketch is not a working processor or evidence\
that decompilation is correct. Keep temporary lifting, instrumentation, and solver dependencies optional unless the\
selected route needs them.
