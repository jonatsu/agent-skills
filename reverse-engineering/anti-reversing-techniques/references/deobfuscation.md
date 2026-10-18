# Native-Code Deobfuscation

## Prove the Relevant Simplification

Start with the behavior under investigation and its data dependencies. A value with no visible consumer can still\
affect memory, flags, exceptions, synchronization, or external calls. Follow these effects before removing apparent\
junk. Preserve the original graph and annotate a simplified graph separately.

For an opaque-predicate candidate, record bit width, signedness, overflow, exceptional inputs, and incoming-state\
constraints. Mathematical identities over integers do not automatically hold under machine arithmetic or signed\
comparisons. Seeing one branch on many inputs establishes observed coverage, not constancy.

A proof checks the opposite outcome under the justified incoming constraints. Report whether the contradiction was\
proven, bounded, unproven, or interrupted. Keep solving assumptions with the result. When no solver is available, use\
manual identities and concrete counterexamples, and label the conclusion accordingly.

## Recover Flattened Control Flow

Identify dispatcher candidates through repeated state selection, incoming edges, and shared updates. High graph\
in-degree alone can identify an ordinary loop or error handler. Find state initialization, each state's effects,\
conditional next-state expressions, indirect transitions, and exits.

Create a transition table containing source block, incoming constraints, observable effects, next-state expression, and\
evidence. Keep conditional and unresolved edges. Trace sampling covers executed paths; symbolic exploration covers only\
its model and explored states. Neither automatically yields every original edge.

Construct a simplified graph from justified transitions. Compare return values, memory effects, external calls, and\
exceptions on representative paths before considering a patch. Preserve dispatcher side effects needed by state blocks.\
Saving an annotated graph can answer the question without rewriting executable bytes.

## Decode Strings and Hidden Imports

Locate the decoder's input range, key/state, encoding, allocation lifetime, and caller uses. Capture outputs at a\
stable boundary, or emulate only after modeling required registers, stack, mappings, and dependencies. Validate\
multiple callers and lengths, including empty and embedded-NUL cases where relevant.

Store decoded bytes, encoding hypothesis, source location, decoder identity, and validation evidence. A printable\
result alone is insufficient; verify actual use. Self-modifying code follows the stage and mapping procedure in\
[packing](packing.md). A decoder can mutate shared state, so repeated calls may differ.

For API hashing, recover exact arithmetic and module selection, then compare candidate exports against runtime or\
call-signature evidence. Preserve collisions as alternatives. Rename from verified behavior rather than the first\
matching hash.

## Repair Misleading Disassembly

Inspect executed or referenced byte addresses around overlapping instructions, embedded junk, computed returns, and\
indirect transfers. Re-decode from a justified boundary using the correct instruction mode. Retain other valid entries\
where overlapping paths are actually reachable. Avoid globally converting every confusing region to code.

MOV-heavy transformations may encode operations through memory tables and state cells. Trace data dependencies and\
observable effects; frequency of one instruction is only a recognition lead. Choose a bounded slice and validate\
recovered semantics before attempting whole-program lifting.

## Recognize the VM Boundary

An interpreter candidate has a virtual instruction pointer, decode/dispatch behavior, and virtual state updated by\
handlers. Recover one observed fetch/decode/handler cycle and distinguish context fields from native temporaries.\
Record bytecode range and handler evidence. Detailed virtual ISA recovery can use `vm-and-bytecode-reverse` when\
available. This recognition step remains useful independently and does not require guessing a protector version.

## Preserve the Analysis

Deliver original-to-simplified location mapping, assumptions, proved versus observed edges, decoder outputs, remaining\
unknowns, and a rollback record for any patches. Reopen or export annotations to verify persistence. Completion\
concerns the requested behavior, not an unsupported claim of complete deobfuscation.
