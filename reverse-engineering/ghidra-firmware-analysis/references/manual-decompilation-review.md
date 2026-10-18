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
2. Retype the variable from the known signature — `FILE *stream`, `const char *path`, `size_t count` — or edit the\
   callee signature where several callers share the wrong type.
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
