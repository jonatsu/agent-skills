# Packing and Runtime Code Changes

## Distinguish Evidence from a Packer Guess

Collect section/segment sizes and permissions, entry location, import shape, entropy distribution, and signature\
matches. Compression, encrypted data, resources, and generated code can produce similar indicators. Section names and a\
high entropy value are not sufficient identification.

Discover a format-aware detector or unpacker only when needed. Verify supported formats, version, invocation, output\
behavior, and required runtime dependencies. A known unpacker is an option when its recognized format matches the\
bytes; signature edits alone do not repair a damaged or custom container.

## Recover a Useful Stage

Preserve the original and unpack into a new artifact. For dynamic unpacking, identify writes to candidate code regions\
and subsequent execution. Capture after the relevant decoding stage completes and before destructive rewriting or\
cleanup. Record module identity, mapped ranges, permissions, source file offsets where known, relocations, entry\
context, and hashes of the extracted regions.

An original entry point candidate needs evidence: transition from loader/stub behavior to stable application flow,\
coherent calls/data references, and a useful downstream region. A familiar prologue, a tail jump, or a restored stack\
is only a lead. The classic PUSHAD/POPAD stack trick is limited to particular 32-bit stubs; it is not a universal\
unpacking method or a native x86-64 recipe.

For layered packing or per-function decoding, keep a stage map and repeat the capture procedure locally. A single\
snapshot may omit code decoded on other paths. Record encryption keys only where necessary and keep sensitive material\
out of published examples and shared reports.

## Reconstruct Only What the Goal Requires

A memory image may be sufficient for static interpretation without being a valid executable file. Before claiming a\
runnable reconstruction, address virtual-versus-file layout, imports, relocations, entry point, TLS/initialization, and\
any protector-maintained state. Validate in the controlled target environment and preserve failures.

Resolve hidden imports by tracing the resolver, its input and returned address, and module identity. Hash-based\
resolution requires candidate validation with width, case normalization, encoding, rotation, seed, and export\
forwarding behavior. Collisions are possible. An observed API address can depend on runtime load mapping.

Persist recovered names and import/type annotations with address conversions and confidence. Test representative calls\
against actual arguments and return-value uses instead of assigning names solely from a hash match.

## Integrity and Recovery

Before patching decoded code, locate checksums or integrity dependencies. Work with an analysis copy, preserve original\
bytes, and document exactly which assumptions change. A dump that crashes after import repair might lack initialization\
state rather than contain incorrectly decoded instructions. Return to the last validated stage and isolate the missing\
dependency instead of repeatedly widening patches.
