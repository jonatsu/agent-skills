# OWASP FSTM stage 3: analyzing firmware

Stage 3 turns whatever dump format [stage 2][stage-2] produced into a standardized binary, strips out\
extraction-artifact noise, and locates the sections worth extracting in [stage 4][stage-4]. There is no single formula:\
expect undocumented formats, proprietary containers, and encrypted data, and let what stage 1 already learned about the\
vendor and architecture guide which tool to reach for first. Distilled from [Tarlogic's stage 3 write-up][source] (part\
of the OWASP FSTM series).

## Converting a dump to raw binary

| Format                   | Marker                           | Converts with                         |
| ------------------------ | -------------------------------- | ------------------------------------- |
| Intel HEX                | line starts with `:`             | `Intel_Hex2Bin`, `SRecord`            |
| SREC / Motorola S-record | line starts with `S`             | `SRecord`                             |
| Hexdump / hex string     | address, hex-byte, ASCII columns | `xxd -r`                              |
| Base64                   | printable-only encoding          | a scripting language's base64 library |

## Screening out-of-band and parity data

A chip-off dump of NAND flash carries redundancy data the filesystem never sees: a bad-block index and an\
error-correction parity pool, interleaved per block or page (check the chip's datasheet for the exact split, commonly\
interleaved rather than trailing). Strip it before treating the dump as a clean filesystem image, either with an\
automation attempt (e.g. [Hitsxx/NandTool][nandtool]) or by manual entropy and autocorrelation study, since the exact\
layout is manufacturer-specific.

## Entropy analysis

Entropy, in this context, measures how much a sample's bytes vary rather than true randomness: a file that walks every\
byte value 0-255 in sequence scores the maximum despite being fully predictable. High entropy in a firmware region\
signals compression or encryption; compression tends to score highest, encryption close behind, though this is not\
universal across every algorithm. Running `binwalk -E` over the image and reading its rising/falling entropy edges\
marks section boundaries worth a closer look; on OWASP's `IoTGoat` sample image this located a SquashFS filesystem's\
high-entropy tail before a hex-editor check confirmed the `hsqs5` and `7zXZ` signatures at that address. A genuinely\
encrypted section instead shows uniform high entropy with no signature nearby, which needs more vendor research, a\
leaked key, an earlier unencrypted firmware version, or [stage 6][stage-6]/[stage 7][stage-7] to resolve.

## Signature and magic-number search

`binwalk` (no flags) is the default first tool: it scans for ELF headers, AES S-boxes, compressed data, CRC tables,\
device trees, and filesystem signatures in one pass. Its heuristics produce frequent false positives, especially on 1-2\
byte signatures, so check every hit manually with a hex editor, particularly when a hit contradicts something already\
known about the device. `fdisk -l` complements it by listing any partition table directly, which is both faster than\
`binwalk` on a large image and a quick way to chunk a large firmware image into manageable pieces. `file` runs three\
tests (a `stat` call, a magic-number search restricted to the first bytes, and a language guess); a `file` result of a\
bare partition table or unstructured `data` both mean the interesting content sits past the first bytes and needs the\
deeper tools above. A [file-signature reference list][file-signatures] covers the common formats beyond what's\
tabulated here.

## Sectioning, byte distribution, and string search

Once a section's start address is known, `dd` cuts it out as a standalone file; getting the length right may need\
reading the format's own header (an ELF header's size fields, for example), since `binwalk`'s own automatic extraction\
does not always compute a correct length for every format. A byte-value histogram profiles a section's encoding: an\
ASCII-text-like file peaks near character 32 (space) across a 97-120 and 41-86 range, while a binary or algorithmic\
file shows its own bias depending on its encoding. `strings -n <minlen>` (raising the minimum length past its noisy\
default) surfaces debug messages, license text, version banners, and function names cheaply, often enough on its own to\
identify what software is running and how current the build is.

When entropy or byte distribution flags a section as compressed-or-encrypted with no matching signature, search\
adjacent bytes for known constants instead: hash initialization vectors (MD5, SHA-1, SHA-256), the Rijndael/AES S-box\
table, or a CRC polynomial table. A known integrity-check table nearby narrows which algorithm an\
otherwise-unidentified field is likely to use.

## Manual review

Automated tools rely on heuristics and always need a manual check in a hex editor; investing time in one editor with\
good structure recognition, entropy view, search, and CRC/hash calculators pays off directly, since manual pattern\
recognition catches the small deliberate modification to a known algorithm that automated tools miss.

## References

Distilled from OWASP FSTM / Tarlogic: [OWASP FSTM, stage 3: Analyzing firmware][source].

- [scriptingxss/owasp-fstm][owasp-fstm-repo] — the OWASP FSTM reference project this series is based on.
- [Wikipedia: Intel HEX][wiki-intelhex], [SREC (file format)][wiki-srec], [Hex dump][wiki-hexdump],\
  [Base64][wiki-base64], [Entropy (information theory)][wiki-entropy] — background on the formats and concept above.
- [Intel_Hex2Bin][hex2bin] and [SRecord] — conversion tools for the line-oriented hex formats.
- [Hitsxx/NandTool][nandtool] — attempts to automate out-of-band/parity stripping on a NAND chip-off dump.
- [File Signatures Database][file-signatures] — a broader magic-number reference than the table above.
- [OWASP/IoTGoat][iotgoat] — the deliberately vulnerable firmware image used in the worked examples.

[file-signatures]: https://www.filesignatures.net
[hex2bin]: https://hex2bin.sourceforge.net/
[iotgoat]: https://github.com/OWASP/IoTGoat
[nandtool]: https://github.com/Hitsxx/NandTool
[owasp-fstm-repo]: https://github.com/scriptingxss/owasp-fstm
[source]: https://www.tarlogic.com/blog/owasp-fstm-stage-3-analyzing-firmware/
[srecord]: https://srecord.sourceforge.net/
[stage-2]: 02-obtaining-firmware.md
[stage-4]: 04-extracting-filesystem.md
[stage-6]: 06-firmware-emulation.md
[stage-7]: 07-dynamic-analysis.md
[wiki-base64]: https://en.wikipedia.org/wiki/Base64
[wiki-entropy]: https://en.wikipedia.org/wiki/Entropy_(information_theory)
[wiki-hexdump]: https://en.wikipedia.org/wiki/Hex_dump
[wiki-intelhex]: https://en.wikipedia.org/wiki/Intel_HEX
[wiki-srec]: https://en.wikipedia.org/wiki/SREC_(file_format)
