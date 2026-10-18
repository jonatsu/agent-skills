# Parser Validation and Reporting

## Define a Bounded Parser Contract

State whether input is a complete datagram, a complete reassembled stream, or incremental stream chunks. Return one of\
complete message plus consumed length, need more bytes, or invalid input. A truncated live chunk is not necessarily\
malformed; an incomplete finalized capture must remain marked incomplete.

Check fixed headers before every field read. Validate magic/version where established, declared lengths, arithmetic\
overflow, allowed maximum sizes, nested bounds, and padding. Reject impossible sizes before allocating or requesting\
large buffers. Every loop either advances or returns. Record how unknown tags and message types are preserved.

Keep transport reassembly separate from application parsing. For a TCP Wireshark dissector, use the installed Lua TCP\
PDU/desegmentation API after verifying its signature and behavior. A dissector that returns immediately for a partial\
magic/header may never request the bytes needed to recognize a fragmented message. Test that case explicitly. Require a\
maximum length and diagnostic handling for malformed framing; do not silently desynchronize the stream.

## Validation Matrix

Use captures not used to infer the model, plus synthetic byte-level cases:

| Case                                         | Required outcome                                             |
| -------------------------------------------- | ------------------------------------------------------------ |
| Every header split point and payload split   | Incremental parser requests more bytes without losing state  |
| Multiple complete messages in one chunk      | Consume each message exactly once                            |
| Truncated final header or payload            | Report incomplete with position, not a fabricated message    |
| Zero, boundary and oversized lengths         | Accept only permitted sizes; bound memory and work           |
| Invalid magic, unknown version/type          | Apply documented invalid/unknown handling                    |
| Nested TLV truncation and repeated fields    | Preserve valid unknowns; reject out-of-bounds values         |
| Reassembled gaps or duplicate transport data | Preserve uncertainty or normalize before application parsing |
| Captured error/handshake/reconnect variants  | Decode according to observed state and direction             |

A serializer/parser round trip is useful but can share the same incorrect assumption. Compare serialized output to\
independent capture bytes or implementation evidence. For stateful protocols, validate full exchanges rather than\
independent records alone. Report unobserved edge cases as coverage limits.

## Active Confirmation Is a Separate Operation

Before connecting, replaying, capturing live, or fuzzing, establish target endpoints, permitted message classes, rate,\
test count/time, expected state changes, stop conditions, and recovery. Continue passive work while active scope is\
unresolved. Prefer an isolated fixture service or emulator for malformed-message cases.

Replaying captured TCP packets is not an application-client implementation: sequence numbers, acknowledgments,\
connection state, session identifiers, authentication, and server state can differ. Use a fresh transport connection\
and the recovered application handshake where appropriate. Raw packet replay is a distinct network experiment requiring\
a suitable controlled setup and explicit purpose.

Change one application field at a time. Update dependent lengths, checksums, or authentication only when their\
semantics are understood. Preserve expected replies and inspect state after each bounded test. Blind fuzzing can change\
persistent target state and is not needed to validate an offline parser.

## Specification Shape

Deliver the protocol purpose/version scope, transport and direction, framing rules, field table, state model, worked\
byte examples, error/unknown handling, validated constraints, and unresolved hypotheses. Each field table states offset\
basis, width, endian/encoding, length semantics, and evidence. Keep a synthetic example clearly labeled; never present\
it as captured target traffic.

Include parser/dissector prerequisites, exact installed tool versions used, extraction settings, invocation, validation\
cases and results, and known loss/truncation limits. Preserve scripts and fixtures in the user's chosen workspace, not\
inside an unrelated tool installation.
