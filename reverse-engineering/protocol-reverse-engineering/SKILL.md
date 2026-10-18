---
name: protocol-reverse-engineering
description: Recover message formats and conversation states from network captures and implementation evidence. Use when decoding a proprietary protocol, inferring framing or field semantics, documenting exchanges, or building and validating a parser or dissector.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Protocol Reverse Engineering

Recover an evidence-backed description of messages and their stateful exchanges. Keep observed wire behavior,\
implementation evidence, hypotheses, and active experiments distinct.

## Establish Inputs and Execution Boundaries

Record the question, capture or implementation identity, transport, endpoints, direction, scenarios, and known\
versions. Preserve the capture and hash derived exports. Use existing captures for passive work. Live capture, endpoint\
connections, TLS interception, replay, and fuzzing require scope covering the affected systems and effects; an\
offline-analysis request alone does not authorize those operations.

Discover available Wireshark/TShark, packet readers, parser runtime, and optional Lua/dissector support with versions.\
Check selected operations against local help and field/plugin listings. Offline reading ordinarily needs file access,\
not capture privileges. Live capture additionally needs the correct interface, capture backend, permissions, filters,\
and storage budget. Determine missing prerequisites for that route only.

Recommend verified host-appropriate packages or configuration with their purpose. Do not assume sudo or change capture\
permissions, routes, firewall rules, or certificate trust silently. Report what passive work remains possible.

## Infer and Test a Model

1. Inventory conversations and coverage. Separate endpoints, directions, sessions, transport metadata, and application\
   bytes. Check snap length, loss, truncation, retransmissions, and missing handshake data.
2. Read [framing and field inference](references/framing-and-fields.md). Reassemble transport streams before assigning\
   application boundaries; compare multiple messages and controlled scenario differences.
3. Build a field hypothesis table with offset basis, width, encoding, candidate semantics, supporting samples,\
   counterexamples, and confidence. Distinguish observed constraints from assumed protocol limits.
4. Recover conversation states, requests/replies, error paths, timeouts, and identifiers. Preserve unknown transitions.
5. For compressed, encoded, or protected traffic, read [protected traffic](references/protected-traffic.md). Establish\
   access to plaintext or suitable session secrets before promising payload recovery.
6. Read [parser validation and reporting](references/parser-validation.md) before producing a decoder, dissector,\
   specification, or active confirmation plan. Validate held-out captures and malformed inputs.

## Preserve the Result

Deliver transport assumptions, framing rules, field and state evidence, known message examples, parser/dissector usage,\
validation results, unknown variants, and capture limits. Record byte-to-field mappings and reproducible extraction\
settings. Keep sensitive captures and secrets in the user's chosen private location, not in published examples or logs.

Completion means that the requested messages are decoded with explained boundaries and semantics, or the exact missing\
evidence is identified. A parser accepting one sample does not establish a recovered protocol.
