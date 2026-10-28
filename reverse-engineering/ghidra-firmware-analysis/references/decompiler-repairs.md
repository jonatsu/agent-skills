# Decompiler repairs

## Contents

- Find the fact the decompiler trusts
- Signatures and calls
- Control flow
- Operations the decompiler cannot see through
- Data mutability and register values

The decompiler renders what the program database tells it: saved signatures, flow types, data settings, and register\
values. When the C is structurally wrong, find the fact it trusts falsely and correct that fact at its source; editing\
the rendering does not hold. Menu, analyzer, and script names below match Ghidra 12.1.4 and 12.2. Check the installed\
release's help when a name differs.

## Find the fact the decompiler trusts

| Symptom in the C                                              | Usual cause                                                                      |
| ------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `in_<reg>` or `unaff_<reg>` variables                         | a wrong signature, a register holding a global, or a callee's side effect        |
| `extraout_<reg>` variables                                    | a value assumed to survive a call that kills it, or a callee's wrong return type |
| a return or argument narrower than the register the code uses | a wrong return type or calling convention on the function or a callee            |
| a constant that is an address inside the same function        | broken stack analysis, often a callee that moves `sp` against its convention     |
| junk code or error bookmarks after a call                     | a callee that never returns but is not marked so                                 |
| `(*UNRECOVERED_JUMPTABLE)()` with a jump-table warning        | an unbounded switch, or a return the decompiler reads as an indirect jump        |
| pcode operations such as `ZEXT`, `SUB`, or `CONCAT`           | widths that the declared types do not explain                                    |

Correct the signature, data-type size, or function attribute the symptom points to, then re-decompile the function and\
its callers. Three bundled scripts find candidates across a program. `FindPotentialDecompilerProblems` lists problems\
in a navigable table. `CompareFunctionSizesScript` flags functions whose decompilation is far smaller than their\
instruction count, which often means a wrong return type. `DecompilerStackProblemsFinderScript` reports locals assigned\
addresses inside their own function. To see what the decompiler removed, clear "Eliminate unreachable code" in the\
decompiler's analysis options, then restore it after diagnosis.

## Signatures and calls

The decompiler uses a saved signature as it stands and otherwise infers one per call site, so its view can differ from\
the listing's. Save an inferred signature with Commit Params/Return; a manual signature edit commits at once. Commit\
Local Names saves local names but not their types.

The Decompiler Parameter ID analyzer commits a signature for every function it touches. Run it only after library\
signatures are applied, because an early run spreads guessed types across the program.

- Variadic or indirect call: right-click the call and choose Override Signature, matching the format string or the\
  target's real prototype. The Variadic Function Signature Override analyzer derives these from format strings; it is\
  off by default and runs as a one-shot analyzer.
- Non-standard convention: in Edit Function Signature, select Use Custom Storage and set each parameter's and the\
  return's storage. One value can span several locations, such as a result returned in a register pair.
- Helper that breaks its convention: for a helper that moves `sp` or clobbers registers outside its convention,\
  mark it In Line so callers decompile its body. Otherwise give it a call fixup; the `-pg` hook repair in\
  [manual decompilation review](manual-decompilation-review.md) shows one. A program's specification extensions hold\
  custom call fixups, callother fixups, and calling conventions in `.cspec` syntax.
- Function that never returns: in Edit Function Signature, check No Return; a script calls\
  `Function.setNoReturn(true)`. Run `FixupNoReturnFunctionsScript` to list further candidates and repair the code that\
  analysis disassembled after their calls. Lowering the evidence threshold of the Non-Returning Functions - Discovered\
  analyzer finds more of them automatically.

## Control flow

- Unbounded switch: define the table in the listing as an array of pointers. Add a `COMPUTED_JUMP` reference from\
  the indirect jump to each target, re-create the function, and run `SwitchOverride` with the jump selected.\
  `FindUnrecoveredSwitchesScript` finds such sites.
- Conditional return through `lr` on ARM: a `bx<cond> lr`, such as `bxne lr` after an APCS-frame epilogue,\
  decompiles as `(*UNRECOVERED_JUMPTABLE)()` with a jump-table warning. Set a Return flow override on that\
  instruction; a script calls `instruction.setFlowOverride(FlowOverride.RETURN)` in a transaction, and the phantom call\
  becomes `return`. In compiler-generated code, a conditional `bx lr` is always a return, so sweep the whole program for\
  them rather than fixing one site. Check any hand-written assembly before applying the sweep there.
- Shared tail call: when several callers end with a jump to the same function, the Shared Return Calls analyzer\
  marks each jump `CALL_RETURN`. Set one it missed with Modify Instruction Flow.
- Opaque predicate: after proving the condition constant, as the manual review describes, patch the branch to an\
  unconditional one, or add a `JUMP_OVERRIDE_UNCONDITIONAL` reference to the taken target.
- Jump into an instruction's middle: the listing shows a disassembly error while the decompiler is correct. Shorten\
  the jumping instruction with Modify Instruction Length (`setLengthOverride`), then re-create the function.\
  `FixOffcutInstructionScript` handles some recurring patterns.

## Operations the decompiler cannot see through

An instruction the processor specification cannot model exactly becomes a user-defined pcode operation, shown as\
`CALLOTHER` in the pcode listing. The decompiler treats it as a black box with inputs and outputs and no other effect.

System calls are the common case: x64 `syscall` and ARM `svc` both render as a pseudo-call with no visible arguments.\
To give a syscall its name, signature, and references, follow these steps:

1. In the Memory Map, add an overlay block in the `OTHER` space, marked Overlay and Artificial.
2. Create a body-less function in that block for each syscall, with the syscall calling convention and signature.
3. Add a `CALLOTHER_OVERRIDE_CALL` reference from the trap instruction to that function.

The bundled `ResolveX86orX64LinuxSyscallsScript` automates these steps for x86 and x64 Linux. It recovers the number\
register with the symbolic propagator. Another architecture needs an adapted script and a supplied number-to-name\
table. Leave this override off any `CALLOTHER` operation that has an output.

A core-specific instruction with no model renders as a generic operation, such as `coprocessor_movefromRt(...)` for a\
vendor hardware divide on ARM. Identify the operation from vendor documentation, the toolchain's CPU option, or the\
operands and their later use. Then annotate each site, for example reading the result as the quotient of the nearby\
dividend and divisor.

## Data mutability and register values

Each defined data item and memory block has a mutability setting: normal, constant, volatile, or writable. Set it on\
data with Data > Settings, or for a whole block in the Memory Map. Mark data constant when the decompiler should show\
its value instead of a pointer to it. Mark a hardware register or shared flag volatile to keep reads that the\
decompiler would otherwise fold away.

Set Register Values at a function's entry tells the decompiler what a register holds there. Use it to correct the ARM\
`TMode` context when a range decodes in the wrong instruction set. Use it also when a register holds a global's\
address across functions; with that value set, accesses through the register render as the global.
