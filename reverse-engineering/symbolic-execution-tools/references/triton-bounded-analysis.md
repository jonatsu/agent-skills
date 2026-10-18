# Triton bounded instruction analysis

## Select the correct library and semantics

Use the [Triton dynamic binary analysis library][triton], not the GPU compiler with the same import name. Its Python\
distribution is `triton-library`; verify that the imported module exposes `TritonContext` and the required\
architecture. Inspect the supplied version, build features, solver backend, and examples before choosing API calls.\
Architectural support does not imply coverage of every instruction extension or system operation. Check actual\
processing status at each instruction; stop with its bytes, address, and diagnostics when unsupported.

Triton supplies instruction semantics, symbolic/taint state, and solver interfaces. A harness must supply instruction\
bytes, concrete memory/register state, fetch/control flow, and external behavior. It is not automatically a loader,\
guest OS, peripheral model, or full path explorer. For branch exploration, implement a bounded worklist or use a\
separately vetted exploration layer with a stated contract.

## Build and validate the concrete harness

Start with a short routine whose arguments, ABI, memory effects, and termination are understood. Record code bytes,\
image base, mappings, instruction mode, pointer width, and input hash. Initialize consumed registers, flags, stack,\
globals, pointed-to data, and a return/stop boundary. Advance through actual instruction addresses and update concrete\
state consistently. Capture an independent concrete trace or calculate a small routine by hand, then compare\
intermediate effects. A mismatch at a load often indicates missing memory or the wrong coordinate system rather than a\
solver problem.

If state comes from QEMU or a debugger, define and verify the transfer explicitly: register names/widths, flags,\
address-space layout, data pages, relocated pointers, instruction mode, and snapshot timing must agree. A debugger dump\
is input to a translator, not proof that every needed state element transferred. First validate a synthetic routine\
before attempting a hardware-bound firmware function.

## Symbolize and solve

Symbolize the smallest input byte/register set required by the question; retain names and their input byte locations.\
Keep known surrounding state concrete with its provenance, and mark unknown dependencies instead of inventing zero\
values. Use the selected build's AST and solver APIs to form the branch/output predicate. Preserve the path predicates\
leading to the requested point when asking for a reachable branch. Solving only the final condition can produce an\
assignment incompatible with earlier branches. For branch inversion, retain the required prefix and negate the intended\
branch condition, not unrelated state.

Bound instruction count, loop visits, paths, time, memory, and solver work. Instruction-level taint identifies modeled\
dependencies; lack of taint is not proof of independence when state or instruction semantics are incomplete. Record\
concrete-only instructions and concretization assumptions. Verify solver status with an API that distinguishes\
failure/unknown from unsat; an empty model alone is ambiguous.

## Replay and retain

Apply the assignment to the original input boundary and execute the unmodified check. Confirm the same relevant\
initialized state and the intended branch outcome. If only the modeled trace can replay, describe the result as\
conditional on that trace and initialization. Retain code/state identity, symbol mapping, predicates,\
solver/backend/version, budgets, errors, and concrete observations. Keep remaining unsupported instruction or\
snapshot-transfer work explicit.

[triton]: https://github.com/JonathanSalwan/Triton
