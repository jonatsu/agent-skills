# Manual decompilation review

## Contents

- Start from the known calls
- The type and rename loop
- When the rendering looks wrong, read the listing
- Read a constant by where it comes from
- Profiling calls hide arguments
- Cut obfuscation before reading
- Confirm at runtime what static reading cannot settle
- Navigate by graph and reference
- Type static data in every section
- Record what you learn

Automated metadata gets a program named and typed; this loop finishes what it cannot, working call site by call site.\
Start from the enriched program — FunctionID names, archive signatures, and the renames replay\
([FunctionID and type metadata][metadata]) — and tighten what remains. This is the core hand-RE workflow; the metadata\
pipeline exists to shorten its first pass, not to replace it.

## Start from the known calls

Read the callee surface before reading any body closely. A dynamic binary names much of it in `.dynsym` and its PLT\
imports (`fopen`, `memcpy`, `pthread_mutex_lock`), and the applied archives add signatures for the rest. Each verified\
callee signature supplies a constraint for its call sites. Check the library version and ABI before treating an\
imported name as a complete declaration. Resolve an unknown callee's identity before typing its use\
([symbol and structure recovery][recovery]); decompiler output supplies usage, never signatures.

## The type and rename loop

A boundary typed by guesswork (`undefined4 *param_2`) misrenders every access inside the function and every caller.\
Correct the boundary at one site and let Ghidra propagate:

1. Take a call to a known function. For example, `fgets(auStack_108, uVar2, piVar1)` calls\
   `char *fgets(char *str, int count, FILE *stream)`, so the first argument is a `char` buffer, `uVar2` an `int`\
   count, and `piVar1` a `FILE *`.
2. Find where the variable's value comes from, then apply the known type (`FILE *stream`, `const char *path`,\
   `size_t count`) at that source. When it is the function's own parameter, change the function signature. When it is\
   the value a previous call returned, change that callee's return type. Retype the variable itself only when it is a\
   true local, such as a stack slot or a callee-saved register. A retype at the wrong level is re-derived on the next\
   decompile and does not hold. For example, an `undefined4` parameter that the function passes straight to a library\
   call's `int` argument is an `int`; change it in the function's signature.
3. The decompiler re-runs and propagates the change to every reference of that value, so the other call sites clean up\
   in the same edit.
4. Rename each variable from the site's context, such as `line`, `line_size`, and `stream` for the `fgets` call; a\
   contextual name is cheap and expected to change, and a later caller with clearer meaning renames it again.
5. Re-read the function: the cleaner rendering exposes the next wrong type (offset arithmetic that was a field access,\
   a callback whose parameters now line up), and the loop repeats.

Work outward from the known calls; each corrected boundary simplifies its callers in turn and pushes the readable\
frontier into new functions. Match the type to the evidence: use character pointers only when byte/string semantics\
support them. Keep unresolved storage generic, and leave a guess with no access pattern behind it uncommitted.

After a type change, reopen the saved program and inspect unrelated branches in the same function as well as the\
intended fields. Ghidra can propagate a struct pointer backward through a merged high variable and mislabel different\
stack storage as that struct. Trace the merge's storage and instruction address; leave a shared pointer generic when\
its branches carry different payloads. Accept the edit only when the intended field names survive and the other branch\
still represents its own value or byte buffer honestly.

Order the work by the call graph: name the leaf functions first and move upward, so each function is read after its\
callees already carry descriptive names. Ghidra's complexity-depth modularisation lists functions in that order.

## When the rendering looks wrong, read the listing

The decompiled C is a lossy rendering, and it drops operations the instructions plainly make: a run of immediate stores\
into a stack array can collapse to its first few entries, and a by-value aggregate argument can render as if nothing\
were passed. When the C looks truncated, contradicts a caller, or omits work the function obviously does, read the\
instruction listing for that range and recover the folded operations from it. Rebuild a table the C under-reports by\
reading the store immediates in order, not the C.

A stack array smaller than a write into it usually means the decompiler split one object. For example,\
`undefined1 auStack_54[4]` cleared by `memset(auStack_54, 0, 0x14)` covers 20 bytes, so the variables that follow it\
in the frame are likely parts of the same object, and the stack variables around it are usually misread as well. Check\
the frame layout in the listing before you treat the write as an overflow. When the frame confirms one object, type the\
full span and re-decompile, which repairs the neighbouring variables together.

Identify the object from how the code fills it. Suppose the code clears those 20 bytes, stores a task pointer at offset\
4, `&autoremove_wake_function` at offset 8, and the object's own address plus 0xc at offsets 0xc and 0x10, then passes\
the object to `prepare_to_wait`. A list head pointing at itself, a well-known callback in a function-pointer field, a\
clear of the exact size, and the calls that receive the object together identify the Linux kernel's `wait_queue_t`:\
`flags`, `private`, `func`, and a `list_head`, 20 bytes on a 32-bit target. Confirm the layout in the header for the\
target's kernel version, apply the type to the whole span, and re-decompile; the fields then render by name.

Record decompiler rendering artifacts, such as an unrecovered jump table that renders as a call through the stack,\
separately from type errors. They need flow repair, such as a jump-table override, rather than a retype;\
[decompiler repairs][repairs] maps each symptom to its repair.

## Read a constant by where it comes from

A literal's meaning comes from the code that produces it and the code that tests it. In Linux kernel code, a small\
negative return value is usually a negated `errno` value: `-5` is `-EIO`, `-4` is `-EINTR`, and `-12` is `-ENOMEM`.\
Check each value before naming the variable that holds it, by tracing every assignment to the call or literal that\
produced it. For example, a driver function's result variable can hold `-5` and `-4` from failed kernel calls and also\
`0x40` and `0x60` that the driver's own polling functions return as hardware status, which its log strings print as a\
status word. Name a variable that mixes the two families as a return code, such as `rc`. Record a confirmed meaning\
as an equate, with Set Equate on the operand, so the listing shows the name instead of the number; a script uses\
`SetEquateCmd`, as the [scripting recipes][recipes] show.

## Profiling calls hide arguments

Code built with `-pg` calls a profiling hook at every function entry, such as `__gnu_mcount_nc` on ARM. The hook\
preserves the argument registers, but Ghidra treats the call as overwriting them. The first argument then renders as\
the hook's return value (`p = __gnu_mcount_nc();`), later ones appear as `extraout_` variables, and every function\
looks like it takes no parameters. Retyping each function by hand leaves the body bound to the hook's result.

Fix it once per program with a call fixup: a specification extension that tells the decompiler what a call to the hook\
does. ARM's `__gnu_mcount_nc` pops the `lr` its caller pushed and returns with `r0`–`r3` intact, which this fixup\
states:

```xml
<callfixup name="gnu_mcount_nc_preserve">
  <target name="__gnu_mcount_nc"/>
  <pcode>
    <body><![CDATA[
      lr = *:4 sp;
      sp = sp + 4;
    ]]></body>
  </pcode>
</callfixup>
```

In the GUI, import the XML file under Edit > Options for the program > Specification Extensions, and apply. Then open\
Edit Function on `__gnu_mcount_nc` and select the fixup as its Call Fixup; set it on both the thunk and the external\
function of that name. A script does the same inside a transaction with\
`SpecExtension(program).addReplaceCompilerSpecExtension(xml, monitor)` and `Function.setCallFixup(name)`. The fixup is\
stored with the program.

Re-decompile to confirm: the hook call disappears, the parameters appear in each signature and body, and a warning\
comment names the injection. A different hook, such as an older `mcount`, has its own stack and register effects; read\
its code and write a fixup body that matches before reusing this one.

## Cut obfuscation before reading

Obfuscated code buries its logic under dead control flow. A common form is the opaque predicate: a branch condition\
built from globals that are never assigned, so it folds to a constant, and the loops and branches it guards are padding\
around the real path. Resolve each such global from its bytes, references, initialization, and possible runtime\
writers. Prove the predicate constant under the stated machine-width and environment assumptions before removing a\
branch. Repeated observation of one outcome alone does not establish that the other branch is unreachable. For a\
heavily obfuscated function, export the decompiled C and simplify it outside the tool, constant-folding the predicates\
and deleting the dead branches until the real control flow is visible, then carry the recovered names back into the\
program.

## Confirm at runtime what static reading cannot settle

Static reading stalls where the decompiler's output is wrong or a call's role is opaque, and a runtime observation\
settles it: breakpoint the call to confirm an argument the C mis-renders or a non-standard ABI, and step it across\
iterations to learn what buffer or structure it builds. Confirm this way only when the target can actually run:\
natively, under emulation where that reaches the behaviour (the `qemu-emulation` skill), or on authorised hardware. A\
target bound to hardware that emulation cannot supply, such as a peripheral or a cartridge bus, may not run at all;\
there, stay with static corroboration against the listing. Treat each runtime observation as evidence for the static\
model, and record the confirmed types and names back to the program.

## Navigate by graph and reference

Search the call graph and reference database; use exported C text to corroborate a graph result. An exported `.c`\
cannot tell a call from a coincidental address, and function-pointer registrations, position-independent references,\
and initialised global tables drop out of it silently. To recover a table's contents, read its bytes in the listing and\
follow its XREFs to the code that fills and reads it; the access width gives the element stride\
([symbol and structure recovery][recovery]).

- The Function Call Graph window follows the listing's current function and shows callers and callees by level; expand\
  a node to keep walking. The Graph Export service writes any displayed graph to a chosen format — JSON among CSV, DOT,\
  GML, GraphML, and others — so the walk becomes a file an agent reads directly.
- Headless, query the call graph and references with the script API from the skill's navigation section, and write the\
  walk to JSON so later passes read it without re-querying.
- Over GhidraMCP, `get_function_calls` returns a function's callers, callees, or both, chosen by its `direction`\
  argument. `get_function_xrefs` and `get_xrefs_to` confirm callers reference by reference; `get_xrefs_from` lists the\
  outward references of one instruction or data address.
- A graph result is a hypothesis as well: an empty result can mean incomplete analysis or an unresolved indirect call,\
  so inspect the underlying instructions before concluding absence.

Answer an ordering question by membership in the callee graph. To decide whether B runs on A's path, collect A's\
callees transitively, down to the depth the question needs. Suppose A's first callees only read a device, poll status,\
and delay, and B never appears among them. Then B does not run inline on that path, and the callee list is the\
evidence. A caller that may run B before calling A is a separate question; walk A's callers to answer it.

Indirect dispatch ends a static walk. When code calls through a function-pointer table, dispatch table, or vtable, the\
call-graph and reference tools resolve the edge only to the table slot or a thunk, often an undefined stub. A function\
reached only that way shows one caller, the slot's address, and no direct reference ties it to its real caller. Treat\
that edge as undecided by the static graph. Resolve it by reading the code that fills the table, or by observing the\
call at runtime as described above. Until then, report the edge as statically undecidable rather than concluding either\
way.

## Type static data in every section

Type static data across every initialised non-executable block, not only sections named `.data` or `.bss`. Read-only\
data, module metadata, parameter tables, and literal pools carry strings and structures as well. When a sweep excludes\
a block, report which one and why. Some families type mechanically, such as parameter-name strings sized by their\
terminating NUL; apply those in bulk and keep per-site judgment for the rest.

Neighbouring statics that code reaches through one base pointer may be one structure or separate globals that the\
linker placed together. Read the symbol table first: when the binary names each member as its own global, keep the\
separate symbols and type the shared access pointer, rather than inventing a structure the source never had.

## Record what you learn

Save accepted types, labels, and names to the program in a transaction, export deliberate renames for replay with the\
input hash, address, prior name, new name, evidence, and confidence, and re-run the metadata application after donor\
updates so the automated pass absorbs the manual one. Readability alone does not prove a declaration; verify argument\
storage and effects against instructions and callers, as [symbol and structure recovery][recovery] requires. A name you\
infer rather than confirm is a hypothesis: keep it distinct from a FunctionID or signature match, and record its basis\
in the function comment so a later pass can review or overturn it.

## References

[metadata]: functionid-and-typeinfo.md
[recipes]: scripting-recipes.md
[recovery]: symbol-and-struct-recovery.md
[repairs]: decompiler-repairs.md
