# Reading Magic Bytes by Hand

Read a signature directly when no tool recognizes the format, when tools disagree, or when the file is a raw\
or headerless blob. This is the fallback the minimal route always supports, because it needs only a hex\
viewer.

## Contents

- [Read the header and the trailer](#read-the-header-and-the-trailer)
- [Where a signature sits: BOF, EOF, and offsets](#where-a-signature-sits-bof-eof-and-offsets)
- [Common format families](#common-format-families)
- [False matches and how to avoid them](#false-matches-and-how-to-avoid-them)
- [Entropy triage](#entropy-triage)

## Read the Header and the Trailer

View the first bytes as hex and ASCII together, then view the last bytes:

```bash
xxd -l 64 file        # header; hexdump -C file | head -4 is the equivalent fallback
xxd -s -16 file       # trailer, read from the end of the file
```

Read both. Many formats are marked at the start, some only at the end, and a few need both to be sure. A\
printable ASCII tag in the first bytes, such as `PK`, `%PDF`, or `ELF`, is the quickest lead; confirm it\
against the full signature rather than trusting the four printable characters alone.

## Where a Signature Sits: BOF, EOF, and Offsets

PRONOM describes a signature by where its bytes sit, and the same vocabulary helps when reading by hand:

- **BOF (beginning of file):** the pattern starts at or near offset 0. Most magic numbers are BOF signatures.
- **EOF (end of file):** the pattern sits at the end, such as the ZIP end-of-central-directory record or the\
  PDF `%%EOF` trailer. Read the trailer to catch these.
- **Absolute offset:** the pattern starts a fixed number of bytes in, such as the `ftyp` box at offset 4 in an\
  MP4, or a filesystem superblock at a fixed sector.
- **Variable offset or wildcards:** the pattern allows a range of positions or accepts any byte in some\
  positions. A signature that is only a few non-specific bytes at a variable offset matches by chance, so it\
  needs stronger corroboration.

Record the offset of every match. A BOF signature identifies the whole file; the same pattern at a deeper\
offset usually marks an embedded or appended file, which the container step handles.

## Common Format Families

A short, high-value set for a first read. Confirm an exact version from the full header or a registry tool;\
these identify the family, not every variant.

| Format or family       | Signature (hex)                | Position | Note                                              |
| ---------------------- | ------------------------------ | -------- | ------------------------------------------------- |
| ELF executable         | `7F 45 4C 46` (`.ELF`)         | BOF      | Offset 4 gives 32- or 64-bit, offset 5 endianness |
| PE / DOS executable    | `4D 5A` (`MZ`)                 | BOF      | `PE\0\0` at the offset stored at `0x3C`           |
| PDF                    | `25 50 44 46` (`%PDF`)         | BOF      | `%%EOF` trailer near the end                      |
| ZIP and ZIP-based      | `50 4B 03 04` (`PK..`)         | BOF      | DOCX, JAR, APK, and ODT are ZIP containers        |
| gzip                   | `1F 8B`                        | BOF      | Often wraps a tar stream                          |
| xz                     | `FD 37 7A 58 5A 00`            | BOF      | —                                                 |
| PNG                    | `89 50 4E 47 0D 0A 1A 0A`      | BOF      | `IEND` chunk marks the end                        |
| JPEG                   | `FF D8 FF`                     | BOF      | Ends with `FF D9`                                 |
| squashfs               | `68 73 71 73` or `73 71 73 68` | BOF      | Endianness flips the magic; common in firmware    |
| Device tree blob (DTB) | `D0 0D FE ED`                  | BOF      | Big-endian magic                                  |
| U-Boot legacy image    | `27 05 19 56`                  | BOF      | 64-byte header precedes the payload               |

## False Matches and How to Avoid Them

- A short magic number occurs by chance in unrelated data. Treat a two- or three-byte match as a lead, and\
  confirm it against the rest of the header and a second source.
- A printable tag can be coincidental. `PK` appears in text that is not a ZIP; require the full `50 4B 03 04`\
  and a plausible local file header.
- `file` reporting a format from one short pattern can be wrong on firmware and raw dumps. Corroborate before\
  asserting.
- A container reuses its members' signatures. Finding a PNG magic inside a firmware image identifies an\
  embedded resource, not the image's own format.
- Endianness changes the bytes. The squashfs magic appears in both orders; match either and record which,\
  because it tells you the image's byte order.

## Entropy Triage

High, uniform entropy across the whole file means the data is compressed or encrypted, so no format signature\
will match the body. Estimate it with a tool such as `binwalk -E`, or by compressing the file and seeing that\
it barely shrinks. Record the observation, and distinguish a known compression header (gzip, xz) from a\
headerless high-entropy blob, which may be encrypted or raw. Do not force a format name onto high-entropy\
data; report it as compressed or encrypted and, where a container tool found one, identify the wrapper instead.
