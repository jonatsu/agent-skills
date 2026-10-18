---
name: crypto-analysis
description: Recover and validate cryptographic behavior in binaries and firmware. Use to identify primitives and constructions, trace keys and authenticated data, assess a suspected weakness, or build a decrypt-and-verify or challenge-response proof of concept.
license: MIT
compatibility: Requires supplied binary evidence and test data. Executable proofs require a compatible language runtime and the selected cryptographic, number-theory, or constraint-solving library.
metadata:
  author: Joonas Onatsu
---

# Cryptographic reverse engineering

Recover the implemented construction and its trust boundary before deciding whether a weakness achieves the requested\
outcome. Distinguish confidentiality, integrity, authenticity, freshness, and key possession; success against one does\
not establish another.

## Establish evidence and prerequisites

Read supplied format descriptions, known plaintext/ciphertext, transcripts, and prior analysis before re-deriving their\
contents. Record input hashes, routine addresses, lengths, byte order, candidate parameters, and the question being\
tested. Treat labels and decompiler output as hypotheses until instructions and data flow corroborate them.

Static analysis can proceed from available disassembly and artifacts without a crypto library. For an executable proof,\
check the selected runtime, environment, package version, and API before using it. Choose only dependencies required by\
that proof: PyCryptodome for supported primitives, gmpy2 or SymPy for integer arithmetic, or Z3 for an explicitly\
modeled relation. Check module identity because similarly named packages can expose incompatible APIs. Use an isolated\
environment when setup is authorized; do not assume the author's environment or administrator access. For a missing\
dependency, inspect the host/runtime package catalogue and verify the recommendation against official documentation.\
Explain what it enables, leave installation to existing authorization, and state which work remains possible without\
it.

## Identify a construction

Locate distinctive constants, table accesses, rounds, operand widths, buffer sizes, and imported calls. AES tables or\
SHA initialization values are clues; compiler optimization, alternate implementations, and decoys require\
corroboration. XOR loops, high entropy, and CRC tables alone do not identify encryption or authentication. Trace data\
through initialization, update, finalization, comparison, and error handling.

Recover the whole parameter contract: algorithm, mode, key length and source, IV/nonce length and generation, padding,\
byte order, associated data, tag/signature format, truncation, and exact covered byte ranges. Separate transformations\
such as decompression, key derivation, encryption, MAC, and signature verification. For each stage, identify whether\
output is trusted before validation succeeds.

## Test a suspected weakness conditionally

Read [weakness selection](references/weakness-selection.md) when assessing a candidate failure or choosing arithmetic\
tools. Match the proposed attack to its required observations and capabilities before building it. Record missing\
prerequisites instead of replacing them with assumptions.

For embedded keys, distinguish recoverable bytes, derived per-device secrets, public verification keys, and\
hardware-protected handles. A shared key has impact only within the operations and device population that accept it.\
For nonce or IV reuse, establish reuse under the same key and apply the actual mode's security requirements. Successful\
decryption does not grant signing authority or show that modified content will be accepted.

## Recover challenge-response behavior

Trace challenge creation, freshness, key selection, message serialization, response generation, and verification\
separately. Map every concatenation, length, counter, endian conversion, and truncation using captures and call-site\
buffer accesses. Distinguish a MAC from a checksum or an unkeyed hash. Identify which fields the verifier actually\
authenticates.

Reconstruct a small reference model and compare it against multiple known challenge/response pairs. Use pairs that\
discriminate ordering, lengths, boundary cases, and state/counter behavior. A single matching response can fit an\
incorrect model; retain alternative constructions until discriminating evidence rejects them. If a hardware operation\
cannot be reproduced, isolate its known inputs and outputs rather than inventing a key or algorithm.

## Validate an executable model

Work on supplied copies and synthetic fixtures; preserve the original artifact and exact proof inputs. Check a\
known-answer vector or independently produced result before using the library as an oracle. For decryption, verify\
structure, lengths, padding and authenticated tags/signatures where present, not only printable plaintext. For\
verification, include a known valid case and controlled changes to authenticated bytes, tag, nonce, and excluded\
fields. A negative case should fail for the intended reason; a parser error alone does not prove cryptographic\
rejection.

Model fixed-width arithmetic, shifts, modular operations, and signed comparisons explicitly in constraint proofs.\
Report satisfiable, unsatisfiable, unknown, and incomplete modeling separately. Replay candidate solutions through the\
original routine or a justified concrete oracle; a solver result is conditional on the model. Bound runtime and input\
size for factoring or search. Failure to solve within a bound is not proof of strength.

Completion requires an evidenced construction map and either a reproducible validated model or a precise remaining gap.\
Report the applicable attack conditions, demonstrated effect, acceptance boundary, and untested cases. Preserve source\
pointers, code, test vectors, dependency versions, and outputs without exposing recovered secrets in public reports.
