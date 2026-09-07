# Compliance, SBOM, and CVE Auditing

License compliance, software bill of materials, CVE auditing, and copyleft source release for a Yocto image. These are
release gates separate from a green build: a build can succeed and still ship an incomplete SBOM, an unaudited CVE, or a
license-metadata gap. Feature names and SBOM formats are release-sensitive — confirm the codename (Iron Law) and read
the version-matched Reference and Security manuals (`official-doc-map.md`).

## Contents

- [The Compliance Gates](#the-compliance-gates)
- [`LIC_FILES_CHKSUM`: the Root of Everything](#lic_files_chksum-the-root-of-everything)
- [License Manifest and On-Target License Text](#license-manifest-and-on-target-license-text)
- [SBOM with `create-spdx` (SPDX)](#sbom-with-create-spdx-spdx)
- [CVE Auditing with `cve-check`](#cve-auditing-with-cve-check)
- [Copyleft Source Release with the `archiver` Class](#copyleft-source-release-with-the-archiver-class)
- [Release Compliance Checklist](#release-compliance-checklist)

## The Compliance Gates

Four independent outputs, each driven by recipe metadata:

| Gate             | Question it answers                                | Driver                         |
| ---------------- | -------------------------------------------------- | ------------------------------ |
| License manifest | what licenses are on the image?                    | `LICENSE` + `LIC_FILES_CHKSUM` |
| SBOM (SPDX)      | what components, versions, and relationships ship? | `create-spdx`                  |
| CVE report       | which known vulnerabilities affect them?           | `cve-check`                    |
| Source archive   | can I hand over copyleft sources?                  | `archiver` class               |

All four read the same declarative recipe metadata, so a wrong or missing `LICENSE`/`CVE_PRODUCT`/`SRC_URI` silently
degrades every downstream artifact. Fix the metadata, not the report.

## `LIC_FILES_CHKSUM`: the Root of Everything

Every recipe except `LICENSE = "CLOSED"` MUST declare `LIC_FILES_CHKSUM`. It pins the exact license text the recipe was
audited against; if upstream changes that text, the checksum mismatch fails `do_populate_lic` and forces a human to
re-review. That failure is a feature — it is the tripwire that keeps a relicensing from slipping through unnoticed.

```bitbake
LICENSE = "GPL-2.0-only & MIT"
LIC_FILES_CHKSUM = "\
    file://COPYING;md5=b234ee4d69f5fce4486a80fdaf4a4263 \
    file://src/util.c;beginline=1;endline=20;md5=ca0d220bc413e1842ecc507690ce416e"
```

- Point at the whole license file, or a header line range when the license lives inside a source file.
- Use SPDX license identifiers in `LICENSE` (`GPL-2.0-only`, not legacy `GPLv2`) — the SBOM and `INCOMPATIBLE_LICENSE`
  filtering depend on them.
- A checksum mismatch means *review the new text*, then update the md5 — never just paste the new hash to make the error
  go away.

## License Manifest and On-Target License Text

The build writes a per-image license manifest listing each package, its version, recipe, and license, under
`${LICENSE_DIRECTORY}/${IMAGE_NAME}/license.manifest`. Review it by hand: it reflects only the declarative metadata, so
any recipe with a weak `LICENSE` or a missing `LIC_FILES_CHKSUM` shows up as a gap.

To ship the license texts on the target itself:

```bitbake
COPY_LIC_DIRS     = "1"      # copy license dirs into the rootfs
COPY_LIC_MANIFEST = "1"      # and the manifest
# or package them so only what you install is included:
LICENSE_CREATE_PACKAGE = "1"
```

## SBOM with `create-spdx` (SPDX)

Yocto generates an SPDX software bill of materials via a class you inherit globally:

```bitbake
# local.conf or distro conf
INHERIT += "create-spdx"
```

The build emits SPDX JSON documents (per recipe and a rolled-up image document) into `tmp/deploy/spdx/` (and a symlink
beside the image). They record components, versions, licenses, files, and dependency relationships — the artifact
downstream tooling ingests for supply-chain and vulnerability analysis.

Release-sensitive: the class name, output layout, and SPDX schema version differ by release (the SPDX 2.x → 3.x
transition is a notable jump). Confirm the codename and check the Reference Manual for that release before asserting the
exact path or schema.

## CVE Auditing with `cve-check`

```bitbake
# local.conf or distro conf
INHERIT += "cve-check"
```

`cve-check` maps built components against the NVD CVE database and writes per-recipe and image-level reports
(`tmp/deploy/cve/`, plus a summary beside the image). The mapping hinges on metadata:

- `CVE_PRODUCT` — the upstream product name(s) as the NVD knows them; the default is the recipe name and is often wrong
  (e.g. `openssl` vs `openssl:openssl`). Set it explicitly when the report is empty or clearly incomplete.
- `CVE_VERSION` — the version to match, when it is not the plain `PV`.
- `CVE_STATUS[<cve-id>]` (release-dependent flag name) — record a triage decision (patched, not-applicable,
  ignored-with-reason) so a known-and-handled CVE stops reappearing as noise.

A CVE is closed either by upgrading, by a patch in `SRC_URI` whose CVE tag the checker recognizes, or by an explicit,
justified status entry — never by deleting the report.

## Copyleft Source Release with the `archiver` Class

To hand over the sources a copyleft license obliges you to provide:

```bitbake
INHERIT += "archiver"
ARCHIVER_MODE[src] = "configured"   # patched (default) | configured | original
```

The class produces per-recipe source tarballs under `tmp/deploy/sources/`. Pick the mode by obligation: `original` for
pristine upstream, `patched` (default) for upstream-plus-your-patches, `configured` when the license requires the exact
configured tree. Pair the archive with `COPYLEFT_LICENSE_INCLUDE`/`_EXCLUDE` to scope which recipes are archived.

## Release Compliance Checklist

- [ ] Every non-`CLOSED` recipe has a `LICENSE` (SPDX identifiers) and a matching `LIC_FILES_CHKSUM`; `do_populate_lic`
  is clean.
- [ ] `INHERIT += "create-spdx"` — SBOM generated and archived with the release.
- [ ] `INHERIT += "cve-check"` — CVE report reviewed; each open CVE upgraded, patched, or given a justified status
  entry.
- [ ] `INHERIT += "archiver"` with the mode your licenses require — source archive captured for the shipped image.
- [ ] License manifest reviewed by hand for metadata gaps.
