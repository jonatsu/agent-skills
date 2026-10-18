# Symbol and structure recovery

Recover identities and layouts from surviving symbols, constants, strings, call patterns, and memory accesses. Treat\
patterns as hypotheses until instructions and independent context corroborate them.

## Contents

- Ghidra notation and ABI
- Recover a function identity
- Constants and format markers
- Call-pattern fingerprints
- Recover a structure
- Common structure shapes
- Record and verify results

## Ghidra notation and ABI

`FUN_address` is an unnamed function; `DAT_address` is an unnamed data reference. `param_N` is a decompiler parameter,\
and `undefined4` means a four-byte value whose type remains unresolved. Check access width, pointer width, and the\
program's data organisation before interpreting decompiler casts.

Confirm the ABI independently of reconstructed C parameters. For example, ARM AAPCS uses `r0`–`r3` for initial ordinary\
integer arguments, with further arguments on the stack. Return storage, aggregate handling, floating-point variants,\
syscalls, and firmware services need their own ABI checks. Wrong calling conventions or prototypes can hide arguments\
and change apparent return values.

Stripping an ELF's `.symtab` does not necessarily remove `.dynsym` or dynamic imports. Use surviving exports,\
relocations, debug information, and linkage names before attempting manual recovery.

## Recover a function identity

Inspect the function's strings, constants, code shape, access widths, and size. A tiny wrapper has little identifying\
information; its size does not establish that it is `strlen` or `memcpy`. Walk both callers and callees, including data\
registrations and indirect-call tables. Inspect how callers prepare arguments, test results, initialise objects, and\
release resources.

Resolve compiler-generated function-name strings at assertion or error calls. An embedded string can name an enclosing\
function, but verify which argument and call site uses it. Parser errors and protocol field names identify a subsystem\
rather than necessarily naming one function. Combine several features before searching source or comparing known\
implementations. Prefer the target's available library versions and build configuration over an unrelated public build.

FunctionID recognises compiled donor bodies; Version Tracking correlates two programs and propagates accepted\
annotations. BSim searches decompiler-derived similarity signatures and can find near matches across a corpus. Review\
each candidate's evidence and collision risk before accepting names. Use the [metadata reference][metadata] for\
provenance and ABI checks.

## Constants and format markers

Constants can identify an algorithm family but do not prove its mode, key source, purpose, or security consequence.\
Distinguish software implementations from hardware-offload wrappers by following their actual callees and operations.

| Algorithm        | Markers                                      | Interpretation                                     |
| ---------------- | -------------------------------------------- | -------------------------------------------------- |
| MD5              | `67452301 EFCDAB89 98BADCFE 10325476`        | Initial state, also shared with part of SHA-1      |
| MD5              | `D76AA478 E8C7B756 242070DB C1BDCEEE`        | First four round-table values                      |
| SHA-1            | MD5's initial words plus `C3D2E1F0`          | Initial state                                      |
| SHA-1            | `5A827999 6ED9EBA1 8F1BBCDC CA62C1D6`        | Round constants                                    |
| SHA-256          | `6A09E667 BB67AE85 3C6EF372 A54FF53A`        | First four initial-state words                     |
| SHA-256          | `428A2F98 71374491 B5C0FBCF E9B5DBA5`        | First four round constants                         |
| SHA-512          | `6A09E667F3BCC908`                           | First initial-state word; verify 64-bit operations |
| HMAC             | Repeated bytes `36` and `5C`                 | Inner/outer key pads; check hash composition       |
| CRC32            | `EDB88320`                                   | Reversed polynomial                                |
| CRC32-C          | `82F63B78`                                   | Castagnoli polynomial                              |
| AES              | `63 7C 77 7B F2 6B 6F C5`                    | Start of forward S-box                             |
| AES inverse      | `52 09 6A D5 30 36 A5 38`                    | Start of inverse S-box; mode remains unresolved    |
| RC4              | 256-byte state and initialisation/swap loops | Check key scheduling and stream operations         |
| Salsa20/ChaCha20 | `61707865 3320646E 79622D32 6B206574`        | Little-endian words for `expand 32-byte k`         |
| Poly1305         | `0FFFFFFC` and related masks                 | Candidate key-clamping operations                  |

Base64 uses `ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/`; the URL-safe variant uses `-` and `_`.\
Base32 uses `ABCDEFGHIJKLMNOPQRSTUVWXYZ234567`; hexadecimal encoders can expose `0123456789abcdef` or its uppercase\
variant. Check table use before identifying a decoder or encoder.

| Format | Initial bytes or marker                                                    |
| ------ | -------------------------------------------------------------------------- |
| zlib   | `78 01`, `78 9C`, or `78 DA`, subject to header validation                 |
| gzip   | `1F 8B`                                                                    |
| ZIP    | `50 4B 03 04`                                                              |
| bzip2  | `42 5A 68`                                                                 |
| LZMA   | Candidate `5D 00 00` plus dictionary-size fields; validate the full header |
| ELF    | `7F 45 4C 46`                                                              |
| CramFS | `45 3D CD 28` little-endian magic                                          |
| PNG    | `89 50 4E 47 0D 0A 1A 0A`                                                  |
| JPEG   | `FF D8 FF`                                                                 |
| PDF    | `25 50 44 46`                                                              |
| SQLite | `SQLite format 3` followed by NUL                                          |

`DEADBEEF` and `DEADC0DE` can be sentinel or fill values. `CAFEBABE` and `FEEDFACE` can be file-format markers or\
deliberately reused sentinels. Interpret runtime fill patterns against the actual compiler and operating system,\
including Windows-specific patterns when that platform applies.

## Call-pattern fingerprints

| Observed relationship                            | Candidate role  | Verification                               |
| ------------------------------------------------ | --------------- | ------------------------------------------ |
| Size to pointer, later release of that pointer   | Allocation/free | Follow ownership and failure handling      |
| Same object around a critical region             | Lock/unlock     | Verify exclusion behavior and nesting      |
| Path and flags to handle, later handle-only call | Open/close      | Check handle uses and error values         |
| Context creation followed by teardown            | Init/destroy    | Follow the object's lifetime               |
| Increment/decrement, destruction at zero         | Ref/unref       | Confirm shared counter and destructor path |
| Build a request, then parse related output       | Protocol pair   | Verify command discriminator and layouts   |

Memory-operation candidates include `(dst, src, count)` and `(dst, value, count)` patterns. Comparison candidates often\
return zero for equality; confirm both comparison and result tests. Format-string arguments identify formatting\
candidates, and a comparison callback can identify a sorting routine. Return conventions vary by API: POSIX calls\
commonly use `-1`, allocators use NULL, and status APIs may use zero. A NULL comparison alone does not prove pointer\
type; an integer or handle can share that pattern.

## Recover a structure

Identify the object passed to the target and collect every access by offset, width, read/write direction, and observed\
use. Walk callers for allocation, initialisation, lifetime, and post-call reads. Walk callees for additional fields and\
forwarded sub-pointers. When a callee receives `base + 0x20`, translate its local offsets back to the enclosing object\
before merging observations.

The largest observed field end establishes a minimum occupied extent, not the complete structure size. An allocation\
size can bound the object only when it allocates one object, rather than an array or trailing payload. Check padding,\
alignment, flexible arrays, unions, and ownership before assigning a final size. An apparent pointer offset in C can be\
scaled by the inferred pointee type; verify effective byte offsets in instructions.

| Observed use                       | Candidate field                                                      |
| ---------------------------------- | -------------------------------------------------------------------- |
| Called indirectly                  | Function pointer or pointer-table entry                              |
| Passed to string routines          | Character data, requiring pointer versus inline-array discrimination |
| Used as a memory-copy count        | Byte count or size value                                             |
| Incremented across operations      | Counter or index                                                     |
| Decremented to zero before release | Reference count                                                      |
| Compared against a small set       | State or enum                                                        |
| Masked and shifted                 | Flags or packed fields                                               |
| Multiplied with another field      | Dimension or element-count calculation                               |
| Validated at initialisation        | Possible magic/version discriminator                                 |

Access width establishes storage width; alignment only supplies supporting evidence. Four-byte alignment alone does not\
prove an integer, and eight-byte alignment alone does not prove a 64-bit field. Separate inline arrays from pointers by\
observing address computation and pointer loads. Distinguish array-of-structures strides from separate arrays indexed\
together. Mask/shift operations expose bitfields even when the decompiler renders an ordinary integer.

## Common structure shapes

Linked-list nodes have traversal pointers; reference-counted objects have a count and release path. An object with an\
operations table dispatches multiple indirect calls through a common table pointer. A thread-safe resource may pass a\
leading field to lock/unlock calls before accessing its payload. Messages often combine a discriminator, length, and\
payload; validate each independently. Configuration records may contain magic/version/name/flags, but that shape is\
only a hypothesis until accesses establish it. Ring buffers combine backing storage, capacity, and head/tail indices\
with wraparound behavior.

For an illustrative 32-bit target, an observed message might be represented as:

```c
struct candidate_message {
    uint32_t type;       // 0x00: handler discriminator, observed 4-byte access
    uint32_t size;       // 0x04: length candidate, units require confirmation
    uint8_t payload[];   // 0x08: trailing data candidate
};
```

Apply the target ABI's pointer widths and alignment when representing pointer-containing layouts. Never transfer a\
32-bit example's offsets to another target without verifying its accesses.

## Record and verify results

Record the binary hash, address, candidate name, strings/constants, callers/callees, confidence, and alternatives. For\
structures, keep the offset/access table, observed minimum extent, allocation evidence, and uncertain fields beside the\
declaration. Apply confirmed labels and types to preserved analysis state, then inspect decompilation and callers for\
contradictions. An improvement in apparent readability is insufficient evidence of a correct declaration. Export\
annotations and verify reopening before treating the recovered layout as durable.

## References

[metadata]: functionid-and-typeinfo.md
