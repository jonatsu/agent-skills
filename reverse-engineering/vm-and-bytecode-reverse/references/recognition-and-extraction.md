# Recognition and extraction

## Distinguish the interpreter from adjacent structures

An interpreter commonly fetches an opcode from a separate buffer, decodes operands, updates virtual state, and\
dispatches again. Switch, table, threaded, and distributed dispatch are possibilities, not fixed signatures. Follow how\
the next handler and next bytecode position are computed. A control-flow flattener may dispatch on a state variable\
without a separate virtual ISA or bytecode stream. A protocol parser may dispatch on input tags but have no general\
virtual instruction/state model. Resolve that distinction from the producer and consumer of dispatch data.

Find entry/exit transitions and identify which native registers, stack values, and globals initialize the virtual\
context. A native register-save sequence alone is weak evidence; its form depends on architecture, compiler, and\
protector version. Map state reads/writes by offset and width, then use access patterns to propose virtual PC, SP,\
registers, flags, and memory. Do not force a stack-based interpretation when values actually index a virtual register\
file.

## Extract the correct coordinate range

Locate bytecode through references and fetch behavior. Record container offset, mapped native address, virtual PC\
origin, length evidence, and any relocations or runtime transformations. A native virtual address is not a file offset;\
use the executable section mapping when extracting bytes from disk. Validate extracted data against bytes read by the\
interpreter. For multiple bytecode regions, retain each region's mapping and provenance independently.

If decoding depends on a rolling key, handler state, or prior opcode, preserve that context with the bytes. Capture\
runtime-decoded bytes only within the authorized isolated execution environment. Keep encoded input, decoding\
procedure/key provenance, decoded result, and hashes so the extraction can be reproduced. Repeated decryption at fetch\
time may require a stateful decoder rather than one global decrypted dump. Self-modifying bytecode needs versioned\
snapshots or event traces that identify which bytes executed.

## Trace narrowly

Begin with a small input whose expected effects are independently understood. Record native instruction/handler\
addresses, virtual PC, fetched bytes, and state before/after each relevant handler. Bound tracing and minimize\
unrelated program output. Check truncation and dropped events before using a trace as complete. Instrument dispatch and\
handler boundaries rather than assuming a native instruction trace directly exposes the virtual ISA. A trace observes\
one execution; retain unvisited handlers and paths as coverage gaps.
