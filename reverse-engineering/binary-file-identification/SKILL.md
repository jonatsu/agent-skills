---
name: binary-file-identification
description: Identify the format and container type of an unknown binary file or blob from its magic numbers and byte signatures, with confidence and corroboration. Use when a file has no or a wrong extension, when triaging a firmware dump or carved blob, or when confirming a suspected format with tools such as file, TrID, Siegfried, or DROID. Not for interpreting a binary's compiled code (binary-analysis-patterns) or planning an investigation (reverse-engineering-methodology).
license: MIT
compatibility: Needs a hex viewer, either xxd or hexdump, for by-hand inspection. file (libmagic) gives a fast first guess. Registry-grade identification uses Siegfried or DROID; container detection uses binwalk or unblob; TrID is an optional extension-oriented matcher. The skill checks for each tool and reports what is missing.
metadata:
  author: Joonas Onatsu
---

# Binary File Identification

Decide what an unknown file or blob is from its bytes, then corroborate before asserting the identity.\
Identification names the format and any container; it does not interpret the compiled code or extract the\
contents. Hand those to `binary-analysis-patterns` and to a carving tool once the format is known.

A signature is a byte pattern that marks a format, usually a magic number at the start of the file, sometimes a\
pattern at the end or at a fixed offset. A single match is a hypothesis. Treat it as confirmed only once an\
independent source agrees.

## Establish What You Are Identifying

- Record the file's SHA-256, its size, and where it came from. Work on a copy, never the original.
- Note any claimed type from the extension or the surrounding context as a hypothesis to test, not an answer.\
  A wrong or absent extension is the usual reason this skill is needed.

## Check the Host Tools

Check only the tools the chosen route needs. The minimal route, a hex viewer and `file`, needs no install and\
is present on almost every host, so start there. Confirm each heavier tool with `command -v` and its version\
before relying on it.

Report a missing tool with its purpose and a verified way to obtain it: the package name confirmed against the\
host's package catalogue, or the tool's official container image. Recommending a tool does not authorize\
installing it, running `sudo`, changing packages, or pulling an image. An agent rarely holds those rights, so\
hand the recommendation to the user and continue with the tools already present. Read\
[references/signature-tools-and-registries.md](references/signature-tools-and-registries.md) for per-tool\
package and container options.

## Inspect the Bytes

Read the first bytes with `xxd`, and fall back to `hexdump -C` when `xxd` is absent. Both show hex and ASCII\
side by side.

```bash
xxd -l 64 file        # first 64 bytes; hexdump -C file | head -4 as the fallback
xxd -s -16 file       # last 16 bytes, for a trailer signature
```

Read the trailer as well as the header. Some formats are identified only by a footer, such as the ZIP\
end-of-central-directory record, the PNG `IEND` chunk, or the PDF `%%EOF` marker.

Note the offset of any signature. A magic number at offset 0 identifies the whole file; the same pattern deeper\
in usually marks an embedded or appended file, which the container step below handles.

## Identify With Tools, Then Corroborate

1. Run `file` for a fast first guess. It reads libmagic signatures and names most common formats in one step.
2. Corroborate with a second, independent source before you assert an identity. `file` is fast but often wrong\
   on firmware, raw memory images, and headerless blobs, where it reports `data` or guesses from a coincidental\
   byte match.
3. For an authoritative, versioned identity, resolve a PRONOM persistent identifier (PUID) with Siegfried\
   (`sf`) or DROID. Read [references/signature-tools-and-registries.md](references/signature-tools-and-registries.md)\
   to choose a tool and read its output.
4. When the tools disagree, or none recognizes the format, read the header by hand against known signatures.\
   Read [references/reading-magic-bytes.md](references/reading-magic-bytes.md) for the method, common format\
   families, and the false-match traps.

Report every tool you could not run, with what it would have added, rather than asserting an identity the\
available tools did not support.

## Handle Containers and Nesting

A container such as a ZIP archive, a tar file, a filesystem image, or a firmware image holds other files. When\
the header or a tool reports one, detect its embedded formats and their offsets with `binwalk` or `unblob`,\
then identify each embedded blob at its offset with the steps above.

Detect and identify the parts here; leave carving and extraction to a dedicated tool or skill. High entropy\
across the whole file means compressed or encrypted data rather than a recognizable format; record that\
observation instead of forcing a format name.

## Report the Identification

State the format and, when a container is present, each embedded format with its offset. For each, give the\
signature and its offset, the sources that agreed, and the confidence.

Keep a guess distinct from a confirmed identity. Name the format family when the exact version or variant stays\
unresolved, and say what further evidence would settle it. The identification is complete when the asserted\
format rests on corroborating evidence a later reader can reproduce from the recorded hash, offsets, and tool\
output.

## Attributions

See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for the sources this skill is based on.
