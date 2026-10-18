---
name: yocto-security-audit
description: "Audit a built Yocto/OpenEmbedded image, rootfs or deploy directory for security defects, including one built elsewhere with no build tree. Use to find what an image actually ships, to run or interpret Lynis, OpenSCAP, checksec, kernel-hardening-checker or the meta-security testimage suites, to check credentials, SSH, services, setuid files and mounts, or to gate an image in CI. Use yocto-security-hardening to configure a control and yocto-vulnerability-management for CVEs and SBOMs."
license: MIT
compatibility: The starting point is an image, a rootfs or a deploy directory; a build tree and layers are optional, unlike this skill's siblings. Host-side checks need only an unpacked rootfs. On-target checks need a bootable target or QEMU plus testimage. Lynis, OpenSCAP, checksec, buck-security and kernel-hardening-checker come from meta-security or meta-openembedded, which must be added to bblayers. checksec-native does not build at 5.0 Scarthgap without a one-line bbappend.
metadata:
  author: Joonas Onatsu
---

# Yocto / OpenEmbedded Security Audit

An auditor's defaults are a claim about coverage, not coverage. Before reporting what a check found, state what it
could not see: the checks it disabled, skipped, or never reached. Report a clean run, a green suite, or "no
findings" only alongside that list.

The reason is measured, on meta-security's own layer at `scarthgap`. `check_security.bbclass` runs `buck-security`
with six of its thirteen checks disabled and its standard output discarded. Ten of the 29 test methods in
`lib/oeqa/runtime/cases/` (excluding `smack.py`) assert nothing when their expected output appears. In one run of
`security-test-image`, the tests that assert nothing passed, and most tests that assert a real property failed.

## Scope

**In:** auditing a built artefact — an image, rootfs or deploy directory, including one you did not build.
Establishing provenance, running and interpreting auditors and oeqa suites, reading binary, kernel,
credential, service and filesystem state, separating findings from intended state, and gating in CI.

**Out:** configuring controls (**yocto-security-hardening**); CVEs and SBOMs
(**yocto-vulnerability-management**); live intrusion detection, forensics and incident response, which start
from a running compromised system rather than an artefact; and compliance conclusions, which belong to whoever
owns the product.

### Route to a sibling skill

| Task                                                                       | Skill                              |
| -------------------------------------------------------------------------- | ---------------------------------- |
| Configure a control, and prove on the artefact that it took effect         | **yocto-security-hardening**       |
| Which known vulnerabilities affect this image; SBOM; VEX; CVE release gate | **yocto-vulnerability-management** |
| BitBake mechanics, recipes, `.bbappend`, licence obligations               | **yocto-openembedded-development** |
| U-Boot verified boot and FIT verification                                  | **u-boot-development**             |
| Runtime kernel, driver or OTA behaviour on a booted board                  | **embedded-linux-bringup**         |

### Route the task to a reference

| Task or symptom                                                                           | Reference                                  |
| ----------------------------------------------------------------------------------------- | ------------------------------------------ |
| "Audit this image"; no build tree; which release is this; is this what ships              | `references/auditing-without-metadata.md`  |
| Running Lynis, OpenSCAP, `buck-security`, `check_security.bbclass`; what they skip        | `references/running-the-auditors.md`       |
| Running `testimage`; what a green suite means; container obstacles; reading skips         | `references/oeqa-security-suites.md`       |
| `checksec` over a rootfs; kernel hardening symbols; a wall of red that is mostly intended | `references/binary-and-kernel-findings.md` |
| Credentials, SSH exposure, what starts and listens, setuid, mount options, MAC policy     | `references/configuration-findings.md`     |
| Turning findings into a CI gate; baselines and drift; severity; writing the report        | `references/gating-and-reporting.md`       |

## Provenance gate

Establish what the artefact is before auditing it. An audit of the wrong image produces confident reassurance
about something that does not ship.

| Question               | Where the answer is                                        |
| ---------------------- | ---------------------------------------------------------- |
| Which release?         | `DISTRO_VERSION` in `testdata.json`; else package versions |
| Which recipe built it? | `PN` in `testdata.json`, never the filename                |
| What is installed?     | the `.manifest` beside the image                           |
| Is this what ships?    | ask. Nothing in the artefact answers it                    |

The filename really does lie. `meta-security`'s `security-test-image` deploys artefacts named
`security-build-image-*`, because the base recipe it `require`s exports `IMAGE_BASENAME`. Two image recipes
write the same filenames and the second overwrites the first.

## `testdata.json` — read it first

Deployed beside every image and containing a dump of the build datastore's variables (functions and `BB*`
variables excluded); 2221 variables in the image measured here. When it is present, "I have no metadata" is
mostly untrue:

```bash
T=<image>-<machine>.rootfs.testdata.json
jq -r '.PN, .IMAGE_BASENAME, .DISTRO_VERSION' "$T"     # provenance and release
jq -r '.DISTRO_FEATURES, .IMAGE_FEATURES' "$T"         # LSMs, pam, seccomp, debug-tweaks
jq -r '.ROOTFS_POSTPROCESS_COMMAND' "$T"               # every credential and rootfs tweak, expanded
```

It is still configuration, not the artefact. It tells you what the build **intended**; confirm each property on
the artefact, exactly as you would for a recipe.

## Workflow

Audit lane, for "what is wrong with this image":

1. Pass the provenance gate: release, recipe, manifest, and whether this artefact ships. When shipping status is
   unknown, record that, because it bounds every severity.
2. Read the configuration, then confirm each property on the artefact. `testdata.json` predicts; `/etc/shadow`,
   `/etc/fstab`, and the ELF headers establish. Report only the confirmed property as a finding.
3. Before running an auditor, read what it disables by default: six checks for `buck-security`, the selected
   profile for OpenSCAP, a general-purpose distribution model for Lynis.
4. Subtract the intended state: `security_flags.inc` exemptions, deliberate kernel choices, and checks that do not
   apply to a minimal image. What remains is the finding set.
5. Write the report in the order given in `references/gating-and-reporting.md`.

Run auditors in a prod-test image built from prod's package set, never in the shipped image. Classify a fetch or
environment failure as environmental, not as a defect in the artefact.

Gate lane, for "keep it from regressing":

1. Make the gate fail closed: a missing report, an unparseable file, or a tool that did not run fails the gate.
2. Gate on properties you chose and read, never on a suite's exit status or pass count.
3. Baseline what drifts (manifest, setuid inventory, security-relevant variables), and audit the first baseline
   absolutely, because drift accepts whatever it started with.
4. State the gate's own coverage, so a green build reads as "these properties held", not "audited".

Run read-only checks in one batch without pausing between them: unpacking to a scratch directory, `jq` over
`testdata.json`, `grep` over `/etc`, `checksec`, and reading manifests.

## Evidence first

```bash
# What shipped
wc -l <image>-<machine>.rootfs.manifest

# The artefact itself
mkdir rootfs && tar -xpf <image>.rootfs.tar.* -C rootfs   # GNU tar detects the compression; -p keeps setuid bits
grep '^root:' rootfs/etc/shadow
awk -F: '$3==0 {print $1}' rootfs/etc/passwd
grep -iE '^\s*(PermitRootLogin|PermitEmptyPasswords)' rootfs/etc/ssh/sshd_config
find rootfs -perm -4000 -o -perm -2000
checksec --dir=rootfs/usr/bin
```

Keep every capture bounded — query the artefact, do not paste a rootfs listing.

## Stated gaps

Naming these is part of the skill's contract; filling them from general knowledge is not.

- **Lynis and OpenSCAP output has not been observed.** Their command lines are confirmed from source at the
  packaged versions; their report contents on an embedded image are not.
- **`kernel-hardening-checker`'s output has not been observed either.** Its presence and version are verified;
  its report format is not.
- **`check_security.bbclass` has never been run against an image here.** Its contents are read; what
  `buck-security` reports in practice is not known.
- **Everything measured is `scarthgap` on `qemux86-64`, under TCG and slirp.** Another release, architecture or
  environment may differ, and the run environment is not upstream's CI.
- **Auditing a `.wic` or a signed image you cannot unpack** is named, not taught.
- **Intrusion detection, forensics and incident response** are different disciplines with a different starting
  state.

## Reference pointers

Cite the release-matched manual; the codename is in the docs URL path.

- **docs.yoctoproject.org/\<codename>/** — Reference Manual for variables and classes, the Development Tasks
  Manual's *Making Images More Secure*, and the **Security manual** at 6.0.
- **`git.yoctoproject.org/meta-security`** — `classes/check_security.bbclass`, `lib/oeqa/runtime/cases/`, and
  the sublayers' `meta-*/lib/oeqa/runtime/cases/` are short and worth reading before trusting their results.
- **`git.openembedded.org/openembedded-core`** — `conf/distro/include/security_flags.inc` for the exemption
  list that turns a `checksec` sweep into a finding set.
- **The kernel's `Documentation/security/self-protection.rst`**, for that kernel version, over any checker's
  recommendation list.

## Attribution

See `ATTRIBUTIONS.md` for the sources this skill is based on.
