# Licence Compliance and Copyleft Source Release

License compliance and copyleft source release for a Yocto image. These are release gates separate from a green build:
a build can succeed and still ship a license-metadata gap or an incomplete source archive. Feature names are
release-sensitive — confirm the codename (Iron Law) and read the version-matched Reference Manual
(`official-doc-map.md`).

**SBOM generation and CVE auditing are not here.** They read the same recipe metadata but answer a different question
and have their own release discontinuity; they belong to **yocto-vulnerability-management**, which owns `create-spdx`,
`cve-check`, `sbom-cve-check`, `CVE_STATUS` triage and VEX.

## Contents

- [The Compliance Gates](#the-compliance-gates)
- [`LIC_FILES_CHKSUM`: the Root of Everything](#lic_files_chksum-the-root-of-everything)
- [License Manifest and On-Target License Text](#license-manifest-and-on-target-license-text)
- [Copyleft Source Release with the `archiver` Class](#copyleft-source-release-with-the-archiver-class)
- [Release Compliance Checklist](#release-compliance-checklist)

## The Compliance Gates

Two independent outputs here, each driven by recipe metadata:

| Gate             | Question it answers               | Driver                         |
| ---------------- | --------------------------------- | ------------------------------ |
| License manifest | what licenses are on the image?   | `LICENSE` + `LIC_FILES_CHKSUM` |
| Source archive   | can I hand over copyleft sources? | `archiver` class               |

Both read the same declarative recipe metadata as the SBOM and the CVE report, so a wrong or missing
`LICENSE`/`SRC_URI` silently degrades every downstream artifact, here and in vulnerability management alike. Fix the
metadata, not the report.

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

To ship the license texts on the target itself there are two distinct routes, and the second has a step that is easy to
miss.

**Route 1 — copy the texts into the rootfs directly:**

```bitbake
COPY_LIC_MANIFEST = "1"      # place the manifest in the rootfs
COPY_LIC_DIRS     = "1"      # and the per-package license directories (needs the manifest too)
```

**Route 2 — ship them as packages, so only what you install is included:**

```bitbake
LICENSE_CREATE_PACKAGE = "1"          # GENERATES a <pkg>-lic package per recipe
IMAGE_FEATURES:append  = " lic-pkgs"  # INSTALLS those packages into the image
```

**`LICENSE_CREATE_PACKAGE` only creates the packages; it does not install them.** Setting it alone produces
`<pkg>-lic` packages that are built, feedable, and entirely absent from your image — a build that looks like it
satisfied the obligation while shipping nothing. From Honister onward the license packages are no longer pulled in
automatically, and `lic-pkgs` is the image feature that installs them. Confirm the release's mechanism in its
Reference Manual rather than assuming this pair carries across every branch.

Whichever route you take, **verify the delivered rootfs, not the configuration**:

```bash
grep -c . tmp/deploy/images/<machine>/<image>.manifest      # is <pkg>-lic actually in the image?
grep -- '-lic' tmp/deploy/images/<machine>/<image>.manifest
# and look inside the built rootfs for the texts themselves:
find tmp/work/<machine>/<image>/*/rootfs/usr/share/{licenses,common-licenses} -maxdepth 1 2>/dev/null
```

Generating an artifact and delivering it are separate claims. A green build proves neither.

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
- [ ] `INHERIT += "archiver"` with the mode your licenses require — source archive captured for the shipped image.
- [ ] License manifest reviewed by hand for metadata gaps.
- [ ] If license texts must ship on target, the image **manifest and rootfs** inspected to confirm they are actually
  installed — generating `<pkg>-lic` packages is not shipping them.

Each box above is a *generation* check. None of them establishes that your distribution obligations are met: that is a
legal determination about your product, your licenses and how you deliver it. Report what was generated and verified,
and leave the compliance conclusion to whoever owns it.
