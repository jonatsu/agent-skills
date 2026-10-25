# Manual decompilation review

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

1. Take a call to a known function whose decompiled argument reads `puVar3`.
2. Find where the variable's value comes from, then apply the known type (`FILE *stream`, `const char *path`,\
   `size_t count`) at that source. When it is the function's own parameter, change the function signature. When it is\
   the value a previous call returned, change that callee's return type. Retype the variable itself only when it is a\
   true local, such as a stack slot or a callee-saved register. A retype at the wrong level is re-derived on the next\
   decompile and does not hold.
3. The decompiler re-runs and propagates the change to every reference of that value, so the other call sites clean up\
   in the same edit.
4. Rename the variable from the site's context; a contextual name is cheap and expected to change, and a later caller\
   with clearer meaning renames it again.
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

A stack array smaller than a write into it is usually one aggregate the decompiler split into pieces. For example,\
`undefined1 auStack_54[4]` cleared by `memset(auStack_54, 0, 0x14)` covers 20 bytes, and the variables that follow it\
in the frame are parts of the same object. Find the type that matches the full span, such as a library structure the\
surrounding calls take. Retype the first slot with it, then re-decompile; the merged variable replaces the fragments,\
and nearby expressions often clear up as well.

Record decompiler rendering artifacts, such as an unrecovered jump table that renders as a call through the stack,\
separately from type errors. They need flow repair, such as a jump-table override, rather than a retype.

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
- A graph result is a hypothesis as well: an empty result can mean incomplete analysis or an unresolved indirect call,\
  so inspect the underlying instructions before concluding absence.

## Type static data in every section

Type static data across every initialised non-executable block, not only sections named `.data` or `.bss`. Read-only\
data, module metadata, parameter tables, and literal pools carry strings and structures as well. When a sweep excludes\
a block, report which one and why. Some families type mechanically, such as parameter-name strings sized by their\
terminating NUL; apply those in bulk and keep per-site judgment for the rest.

## Record what you learn

Save accepted types, labels, and names to the program in a transaction, export deliberate renames for replay with the\
input hash, address, prior name, new name, evidence, and confidence, and re-run the metadata application after donor\
updates so the automated pass absorbs the manual one. Readability alone does not prove a declaration; verify argument\
storage and effects against instructions and callers, as [symbol and structure recovery][recovery] requires. A name you\
infer rather than confirm is a hypothesis: keep it distinct from a FunctionID or signature match, and record its basis\
in the function comment so a later pass can review or overturn it.

## References

[metadata]: functionid-and-typeinfo.md
[recovery]: symbol-and-struct-recovery.md
