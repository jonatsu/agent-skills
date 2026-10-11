---
name: apt-fetch-emulation
description: Download, list, and verify .deb packages from a Debian or Ubuntu APT repository without adding it to the host's sources, checking the repository signature and checksums over plain HTTP. Use to fetch packages for offline installation or inspection, including on a non-Debian host or for another architecture, to see what a repository publishes, or to diagnose why one answers 403 or lacks indexes. Not for managing the host's own APT sources or installing packages.
license: MIT
compatibility: Requires a POSIX shell, curl, awk, and sha256sum or shasum; gpgv to verify signatures; xz, gzip, or bzip2 for the index compression a repository publishes. The dependency-resolving route requires apt-get.
metadata:
  author: Joonas Onatsu
---

# APT Fetch Emulation

Fetch what APT would fetch from a repository, without registering the repository on the host or running its
package manager against the host's state. The bundled `scripts/apt-fetch.sh` follows APT's own sequence over
HTTP GET: it reads the signed Release metadata, the Packages index that Release lists, and then each selected
`.deb`, and it checks every file against the hash its parent lists.

## Choose the Route

Use the script by default. It runs on any host with a POSIX shell and `curl`, it lists what a repository
offers, and it downloads exactly the packages named. It does not resolve dependencies.

When the user needs a package together with its dependency closure, and the host has `apt-get`, use a
[private APT tree](#private-apt-tree) instead, so APT itself resolves and verifies the set.

When a repository answers 403, returns empty indexes, or otherwise refuses requests, read
[references/access-failures.md](references/access-failures.md) before retrying.

## Settle Trust Before Fetching

Get the repository's signing key from its publisher's install instructions: the key they place in
`/etc/apt/keyrings/` or name in `signed-by=`. Fetch it over HTTPS from the publisher's own domain, and compare
its fingerprint with the published one when the publisher gives one (`gpg --show-keys key.asc`). `gpgv` reads
binary keyrings, so convert an armored key, one starting with `-----BEGIN PGP PUBLIC KEY BLOCK-----`, with
`gpg --dearmor < key.asc > key.gpg`.

Pass the key with `-k`. Use `-U` only when no key exists or the user accepts an unauthenticated download. The
checksums then detect corruption but not tampering, and the report must say so.

## Run the Script

Map a `sources.list` line to the arguments: `deb [arch=arm64 signed-by=key.gpg] URI SUITE COMPONENT` becomes
`-k key.gpg -c COMPONENT URI SUITE arm64`. A suite ending in `/` names a flat repository with no `dists/` tree,
so pass it unchanged, such as `./`. A deb822 `.sources` file carries the same values as `URIs:`, `Suites:`,
`Components:`, and `Signed-By:`; when `Signed-By:` holds the key block itself, save it to a file and dearmor it.

```sh
# List what the index offers, as tab-separated name, version, architecture.
scripts/apt-fetch.sh -k debian.gpg -l https://deb.debian.org/debian bookworm arm64

# Download named packages; pin a version when the index carries several.
scripts/apt-fetch.sh -k vendor.gpg -o ./debs https://example.com/apt stable amd64 tool=2.1.0-1 tool-data
```

The script names each verified `.deb` on stdout and reports progress and failures on stderr. It exits 0 when
every selected package verified, 1 when any fetch or check failed, and 2 on a usage error. A package whose hash
does not match is never written to the output directory.

Name the packages, or list first and then name them. `-a` downloads the entire index, which for a distribution
archive means tens of thousands of packages, so reserve it for a small vendor repository the user wants
mirrored. Pin `name=VERSION` when the script reports several versions; it refuses to guess which one APT would
pick. When the requested architecture has no index, check the `Architectures:` and `Components:` lines of the
repository's Release file.

The script sends the headers of APT 3.2.0, captured from a live `apt-get update`. Set `APT_FETCH_USER_AGENT`
when a repository expects another client string.

The script reads binary `Packages` indexes only. It does not fetch source packages, use authenticated
repositories, or follow `by-hash` paths, and it trusts packages only through their SHA256.

## Private APT Tree

APT run against a throwaway directory resolves dependencies and verifies signatures without touching the host's
sources, lists, or package state. It needs `apt-get`, but it does not need root. List the distribution's own
archive alongside a vendor repository, because the closure usually reaches into the distribution.

```sh
root=$(mktemp -d)
mkdir -p "$root/etc/apt/apt.conf.d" "$root/etc/apt/preferences.d" "$root/etc/apt/sources.list.d" \
  "$root/var/lib/apt/lists/partial" "$root/var/cache/apt/archives/partial" "$root/var/lib/dpkg"
: >"$root/var/lib/dpkg/status"
cat >"$root/etc/apt/sources.list" <<EOF
deb [arch=arm64 signed-by=$PWD/vendor.gpg] https://example.com/apt stable main
deb [arch=arm64 signed-by=$PWD/debian.gpg] https://deb.debian.org/debian bookworm main
EOF
set -- -o "Dir=$root" -o "Dir::State::status=$root/var/lib/dpkg/status" -o APT::Architecture=arm64
apt-get "$@" update
apt-get "$@" install --download-only --yes tool   # the closure lands in $root/var/cache/apt/archives
apt-get "$@" download tool                        # or the package alone, into the current directory
```

The empty status file makes APT treat nothing as installed, so the closure also holds dependencies a real target
already has, such as `libc6`. Remove the tree when the download is copied out.

## Report

Report each downloaded path, whether the Release signature was verified and with which key, and every package
that failed or was skipped. State that dependencies were not resolved when the script did the download.
