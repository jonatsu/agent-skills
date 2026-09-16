---
name: yocto-security-audit
description: "Audit a Yocto/OpenEmbedded image for security defects, including one you did not build. Use to check what a rootfs actually ships, run and interpret Lynis, OpenSCAP, checksec or kernel-hardening-checker, run testimage and oeqa security suites, read a green suite critically, audit credentials, services, setuid and mounts, and gate an image in CI. Hardening answers how do I set this up; audit answers is it set up, and what is wrong with what I have. Route CVEs and SBOMs to yocto-vulnerability-management."
license: MIT
compatibility: The starting point is an image, a rootfs or a deploy directory; a build tree and layers are optional, unlike this skill's siblings. Host-side checks need only an unpacked rootfs. On-target checks need a bootable target or QEMU plus testimage. Lynis, OpenSCAP, checksec, buck-security and kernel-hardening-checker come from meta-security or meta-openembedded, which must be added to bblayers. checksec-native does not build at 5.0 Scarthgap without a one-line bbappend.
metadata:
  author: Joonas Onatsu
---

# Yocto / OpenEmbedded Security Audit

**IRON LAW: An auditor's own defaults are a claim. You MUST establish what a check could not see before
reporting what it found, and MUST NOT report a clean run, a green suite, or "no findings" without stating the
checks that were disabled, skipped, or never reached.**

This is not caution for its own sake. Every headline claim below was measured on upstream's own security layer
at `scarthgap`:

- `check_security.bbclass` runs `buck-security` with **six check families disabled** and standard output sent
  to `/dev/null`.
- **10 of 29** oeqa test methods assert nothing on the success path — the only assertion sits inside
  `if not match:`.
- Running the suite: **33 passed, 16 failed**. The tests that assert nothing passed; nearly every test that
  asserts a real property failed.
- `checksec-native`, which the host-side lane depends on, **does not build**.

A tool's output is not an audit. Subtracting what the tool could not see is what makes it one.

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

⛔ **BLOCKING. Establish what the artefact is before auditing it.** An audit of the wrong image is worse than
no audit: it produces confident reassurance about something that does not ship.

| Question               | Where the answer is                                        |
| ---------------------- | ---------------------------------------------------------- |
| Which release?         | `DISTRO_VERSION` in `testdata.json`; else package versions |
| Which recipe built it? | **`PN` in `testdata.json` — never the filename**           |
| What is installed?     | the `.manifest` beside the image                           |
| Is this what ships?    | **ask.** Nothing in the artefact answers it                |

The filename really does lie. `meta-security`'s `security-test-image` deploys artefacts named
`security-build-image-*`, because the base recipe it `require`s exports `IMAGE_BASENAME`. Two image recipes
write the same filenames and the second overwrites the first.

## `testdata.json` — read it first

Deployed beside every image and containing a **full dump of the build datastore** (2221 variables in the image
measured here). When it is present, "I have no metadata" is mostly untrue:

```bash
T=<image>-<machine>.rootfs.testdata.json
jq -r '.PN, .IMAGE_BASENAME, .DISTRO_VERSION' "$T"     # provenance and release
jq -r '.DISTRO_FEATURES, .IMAGE_FEATURES' "$T"         # LSMs, pam, seccomp, debug-tweaks
jq -r '.ROOTFS_POSTPROCESS_COMMAND' "$T"               # every credential and rootfs tweak, expanded
```

It is still configuration, not the artefact. It tells you what the build **intended**; the Iron Law applies to
it exactly as to a recipe.

## Workflow

**Audit lane** — "what is wrong with this image":

- [ ] **⛔ BLOCKING — Pass the provenance gate.** Release, recipe, manifest, and whether this artefact ships.
  If the last is unknown, say so; it bounds every severity you assign.
- [ ] **⚠️ REQUIRED — Read the configuration, then confirm on the artefact.** `testdata.json` predicts;
  `/etc/shadow`, `/etc/fstab`, the ELF headers establish. Never report the prediction as the finding.
- [ ] **⚠️ REQUIRED — Before running any auditor, read what it disables by default.** Six families for
  `buck-security`; profiles for OpenSCAP; a distribution model for Lynis.
- [ ] **⚠️ REQUIRED — Subtract the intended state.** The 21 `security_flags.inc` opt-outs, deliberate kernel
  choices, checks inapplicable to a minimal image. What remains is the finding set.
- [ ] **⚠️ REQUIRED — Report lane, coverage, findings, and blind spots.** In that order.

**Gate lane** — "keep it from regressing":

- [ ] **⛔ BLOCKING — Make it fail closed.** A missing report, an unparseable file or a tool that did not run
  must fail. This converts every future rename into a loud failure instead of a silent pass.
- [ ] **⚠️ REQUIRED — Gate on properties you chose and read**, not on a suite's exit status or pass count.
  On the measured run, both of those are available, stable, and wrong.
- [ ] **⚠️ REQUIRED — Baseline what drifts** — manifest, setuid inventory, the security-relevant variables —
  and audit the baseline once absolutely, because drift accepts whatever it started with.
- [ ] **⚠️ REQUIRED — State the gate's own coverage**, so nobody reads green as "audited".

Read-only checks that are already authorized — unpacking a rootfs to a scratch directory, `jq` over
`testdata.json`, `grep` over `/etc`, `checksec`, reading manifests — run in a batch; do not stop to ask after
each.

## Evidence first

```bash
# Provenance
jq -r '.PN, .IMAGE_BASENAME, .DISTRO, .DISTRO_VERSION' <image>.testdata.json
jq -r '.DISTRO_FEATURES, .IMAGE_FEATURES, .ROOTFS_POSTPROCESS_COMMAND' <image>.testdata.json

# What shipped
wc -l <image>-<machine>.rootfs.manifest

# The artefact itself
mkdir rootfs && tar -xjf <image>.rootfs.tar.bz2 -C rootfs
grep '^root:' rootfs/etc/shadow
awk -F: '$3==0 {print $1}' rootfs/etc/passwd
grep -iE '^\s*(PermitRootLogin|PermitEmptyPasswords)' rootfs/etc/ssh/sshd_config
find rootfs -perm -4000 -o -perm -2000
checksec --dir=rootfs/usr/bin
```

Keep every capture bounded — query the artefact, do not paste a rootfs listing.

## Anti-patterns

- MUST NOT report a clean auditor run without naming the checks it disables by default.
- MUST NOT treat a green oeqa suite as a property check. Ten of the layer's cases assert nothing on the success
  path, and `test_checksec_fortify` passes on an image where no fortification claim was checked.
- MUST NOT gate on `do_testimage`'s exit status or its pass count; on the measured image the first blocks for
  unrelated reasons and the second reads 33 green while 16 property tests fail.
- MUST NOT identify an artefact by its filename. Read `PN` from `testdata.json`.
- MUST NOT report a `checksec` sweep as findings before subtracting the 21 `:pn-` opt-outs — and if
  `security_flags.inc` was never required, the finding is one line about the distro, not a table of binaries.
- MUST NOT read a policy directory under `/etc/apparmor.d` or `/etc/selinux` as evidence that a framework is
  enforcing; an image can enable two LSMs while the kernel command line selects one.
- MUST NOT report a host-side service list as "what is exposed" — only a running target answers that.
- MUST NOT assign severity without a stated purpose for the artefact. "Critical if this ships, expected if it
  does not" is a complete answer; a guess is not.
- MUST NOT conclude that an image is secure. An audit finds what it looked for.
- MUST NOT ship an auditor in production; results come from a prod-test image built from prod's package set.
- MUST NOT treat a fetch failure or an environmental failure as a defect in what you are auditing.

## Stated gaps

Naming these is part of the skill's contract; filling them from general knowledge is not.

- **Lynis and OpenSCAP output has not been observed here.** They are packaged upstream and routed to; the
  option names and report formats need confirmation at the packaged version.
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
- **`git.yoctoproject.org/meta-security`** — `classes/check_security.bbclass` and `lib/oeqa/runtime/cases/`
  are short and worth reading before trusting either.
- **`git.openembedded.org/openembedded-core`** — `conf/distro/include/security_flags.inc` for the opt-out
  list that turns a `checksec` sweep into a finding set.
- **The kernel's `Documentation/security/self-protection.rst`**, for that kernel version, over any checker's
  recommendation list.

## Attribution

See `ATTRIBUTIONS.md`. This skill is an independent write-up derived from upstream source and from a build of
`meta-security` performed for it; the CC BY-SA teaching materials that informed subject selection are recorded
there and no material was adapted from them.
