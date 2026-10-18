# Signature Tools and Registries

Choose a tool by the question. A fast first guess, an authoritative versioned identity, an extension-oriented\
match, or a container breakdown each have a different best tool. Corroborate across at least two before\
asserting an identity, because each tool has a characteristic blind spot.

## Contents

- [file (libmagic)](#file-libmagic): the fast first guess
- [Siegfried and DROID (PRONOM)](#siegfried-and-droid-pronom): authoritative versioned identity
- [TrID](#trid): extension-oriented statistical match
- [binwalk and unblob](#binwalk-and-unblob): containers and embedded formats
- [Installing or containerizing the tools](#installing-or-containerizing-the-tools)
- [Authoring a signature when none exists](#authoring-a-signature-when-none-exists)

## What You Always Have

The minimal path needs no special install. A hex viewer (`xxd` or `hexdump`) and `file` ship on almost every\
Linux and macOS host, and together they identify most common formats and support all the by-hand reading in\
[reading-magic-bytes.md](reading-magic-bytes.md). Reach for the tools below to raise confidence or to break\
down a container, not because the minimal path failed to run.

## file (libmagic)

`file <path>` reports a format from the libmagic signature database. It is installed almost everywhere and\
answers in one step, so it is the default first guess.

Its limits decide when to corroborate. libmagic matches short patterns, so it reports a plausible format from a\
coincidental byte match, and it falls back to `data` on firmware, raw images, and headerless blobs it does not\
recognize. Confirm its answer against a second source before asserting it. Useful options:

```bash
file -k <path>        # keep going after the first match; shows competing matches
file -z <path>        # look inside compressed files
file --mime-type <path>
```

## Siegfried and DROID (PRONOM)

PRONOM is The National Archives registry of file formats. Each format has a persistent identifier (a PUID such\
as `fmt/19` for a PDF version) and a published byte signature. A PUID is an authoritative, versioned identity,\
which is what a `file` string cannot give.

Siegfried (`sf <path>`) matches a file against the PRONOM signatures and reports the PUID, the format name and\
version, and the basis for the match. DROID is the registry's own Java tool and matches against the same\
signatures with a batch and reporting workflow. Prefer Siegfried for a command-line check; reach for DROID when\
a project already standardizes on it or needs its reports.

```bash
sf <path>             # YAML with the PUID, format, version, and matching basis
sf -json <path>
```

Resolve a PUID at <https://www.nationalarchives.gov.uk/PRONOM/> to read the format's full signature and\
history. The registry route is the one to trust when the exact version or variant matters.

## TrID

TrID matches a file against a database of patterns weighted by how often each appears per extension, and\
reports ranked candidates with percentages. It is useful as a third opinion when `file` and the PRONOM tools\
disagree, and for common desktop formats. Read its ranking as relative likelihood, not proof; the top\
candidate can still be wrong on an unusual or headerless file.

## binwalk and unblob

A container holds other files, and these tools find the embedded formats and their offsets rather than naming\
the outer file.

`binwalk <path>` scans for known signatures throughout the file and lists each with its offset, which is how\
you find an appended or embedded blob. `unblob <path>` identifies and recursively unpacks many container and\
filesystem formats. Use either to map a firmware image or archive, then identify each embedded blob at its\
offset with the main steps.

Keep the boundary: these detect and locate the parts. Carving and extracting their contents is a separate\
task, handed to a dedicated extraction tool or skill.

## Installing or Containerizing the Tools

Check each tool with `command -v` and its version before relying on it. When one is missing, recommend a way to\
obtain it and leave the install to the user; an agent rarely holds `sudo` or permission to change the host or\
pull images. Verify a package name against the host's own catalogue before naming it, because names differ per\
distribution. On Debian-family hosts, `apt-cache policy <package>` confirms availability and\
`dpkg -S /absolute/path` identifies an installed provider; other distributions use their own equivalents.

Portability differs by tool:

- `xxd`, `hexdump`, and `file` are present on almost every host, so the minimal route rarely needs anything.
- Siegfried is a single Go binary (`sf`), installable per user with no root through `go install`, Homebrew, or\
  the maintainer's apt repository, then `sf -update` to fetch signatures. It publishes no official container\
  image, and needs none.
- unblob pulls in many extractors, so its official image `ghcr.io/onekey-sec/unblob:latest` is the clean\
  portable option when host installation is blocked. Run the file through it read-only, mounting the input\
  directory. Without the image, `pip install --user unblob` plus the extractors it lists under\
  `unblob --show-external-dependencies` is the host route.
- DROID needs a Java runtime; binwalk offers community container images. Treat both as optional third opinions.

A container is an alternative to a host install, not a required workflow. Do not pull an image or enable a\
service as part of checking what is available; recommend it, and let the user run it.

## Authoring a Signature When None Exists

When no tool recognizes a format, the format can be described as a PRONOM signature and tested before it is\
submitted. The signature syntax, with its beginning-of-file and end-of-file anchors and offsets, is covered in\
[reading-magic-bytes.md](reading-magic-bytes.md). The ffdev.info utility bundles Roy and Siegfried in the\
browser to test a draft signature against sample files; a passing signature can then be contributed to PRONOM.\
This is the last resort, reached only after the inspection and tool steps leave the format unidentified.
