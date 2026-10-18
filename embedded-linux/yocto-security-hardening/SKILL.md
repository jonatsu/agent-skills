---
name: yocto-security-hardening
description: "Harden a Yocto/OpenEmbedded image you build and prove each control on the built artefact. Use for root login and IMAGE_FEATURES, read-only rootfs, compiler and kernel hardening, signed FIT and dm-verity, LUKS, fscrypt or TPM2-sealed keys, firewalls, AppArmor or SELinux wiring, sstate trust, security layers, or a security setting that has no effect. Route audits of an existing image to yocto-security-audit, CVEs and SBOMs to yocto-vulnerability-management, U-Boot verification to u-boot-development."
license: MIT
compatibility: Requires a BitBake/OE-Core checkout and an initialised build directory. Class names, variables and valid IMAGE_FEATURES items are release-specific; guidance is written for 5.0 Scarthgap with 5.1 to 6.0 Wrynose deltas named inline. On-target verification needs QEMU or a reachable board plus testimage. checksec, kernel-hardening-checker and Lynis come from meta-security or meta-openembedded, which must be added to bblayers.
metadata:
  author: Joonas Onatsu
---

# Yocto / OpenEmbedded Security Hardening

## Evidence rule

A security setting is a claim, and the built artefact is the evidence. Report a property as holding only after
you observe it on the artefact: the manifest, the rootfs, the ELF headers, the kernel `.config`, or the running
system. Treat a passing security test the same way, and read what it asserts before you cite it.

Two upstream examples show why. `security_flags.inc` carries 18 per-recipe opt-outs, so `busybox`, `grub` and
others build without parts of the hardening set. `meta-security`'s oeqa `checksec` fortify case passes because
`checksec` rejects the test's own command line.

Pair every control you configure with the observation that settles it.

## Scope

**In:** configuring a security control in a Yocto build, and proving on the artefact that it took effect —
image and distro composition, credentials, root filesystem state, compiler and kernel hardening, the build
side of the boot chain, data-at-rest encryption, network exposure, MAC framework wiring, build and
supply-chain trust, and both verification lanes.

**Out:** auditing an image you did not build, CVE and SBOM work, U-Boot's own verification, and runtime board
debugging; the table below names the owner of each. MAC policy authoring is a stated gap.

### Route to a sibling skill

| Task                                                                                        | Skill                              |
| ------------------------------------------------------------------------------------------- | ---------------------------------- |
| Auditing a built image, running an auditor or an oeqa suite, reading a result, gating in CI | **yocto-security-audit**           |
| CVEs affecting an image, SBOM generation, VEX, a CVE release gate                           | **yocto-vulnerability-management** |
| BitBake mechanics, recipes, `.bbappend`, sstate mechanics, licence obligations              | **yocto-openembedded-development** |
| U-Boot verified boot, FIT verification, console lockdown, boot scripts                      | **u-boot-development**             |
| Runtime kernel, driver, verity or OTA behaviour on a booted board                           | **embedded-linux-bringup**         |
| `.kas.yml` orchestration                                                                    | **kas-build-orchestration**        |
| Buildroot equivalents                                                                       | **buildroot-development**          |

### Route the task to a reference

| Task or symptom                                                                                       | Reference                                     |
| ----------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| A setting's name does not match its effect; "I set this, why is it not doing that"                    | `references/misleading-controls.md`           |
| Feature and package reduction, root credentials, read-only rootfs, `/etc` overlays, service privilege | `references/image-attack-surface.md`          |
| `security_flags.inc`, FORTIFY/RELRO/PIE/stack protector, `checksec`, packaging QA checks              | `references/compiler-and-binary-hardening.md` |
| Kernel config fragments, `kernel_configcheck` audit levels, `kernel-hardening-checker`, MAC packaging | `references/kernel-hardening.md`              |
| Signed FIT, dm-verity, initramfs bundling, IMA/EVM wiring, key handling                               | `references/chain-of-trust-wiring.md`         |
| sstate and mirror trust, `SRC_URI` checksums, `AUTOREV`, reproducibility, release gates               | `references/build-and-supply-chain-trust.md`  |
| LUKS/dm-crypt, fscrypt, TPM2 key sealing, and which threat a design actually covers                   | `references/storage-encryption.md`            |
| What is listening, firewalling it, the legacy-vs-nft split, ssh exposure                              | `references/network-and-services.md`          |
| Choosing and wiring AppArmor, SELinux or SMACK, and confirming one is enforcing                       | `references/mac-frameworks.md`                |
| How to check something host-side or on target; writing an oeqa assertion; the three-image pattern     | `references/verification-workflows.md`        |
| What `meta-security` provides; judging a third-party security layer                                   | `references/meta-security-layer-map.md`       |

## Controls whose names misdescribe their effect

Know these exist before reading any configuration. Full mechanism and verification in
`references/misleading-controls.md`.

| Setting                              | What it actually does                                                                   |
| ------------------------------------ | --------------------------------------------------------------------------------------- |
| `empty-root-password`                | **Permits**; the zap step runs when the feature is *absent*, and only rewrites `root::` |
| `serial-autologin-root`              | Inert alone — the gate needs `empty-root-password` **as well**                          |
| `read-only-rootfs-delayed-postinsts` | **Disables** the check that would fail the build; defers writes to first boot           |
| `read-only-rootfs`                   | Edits `/etc/fstab` lines matching `/dev/root`; the kernel command line still decides    |
| the `security` `DISTRO_FEATURE`      | Adds **nothing** alone; gates four further feature conditions                           |
| `IMAGE_INSTALL:remove`               | Metadata edit — a no-op against transitively pulled packages; use `PACKAGE_EXCLUDE`     |
| `BB_SIGNATURE_HANDLER`               | A task-hash handler, not a signer; falls back to `noop` on a typo                       |
| `CONFIG_FIT_SIGNATURE`               | Enables verification; *requiring* it is `mkimage -r` plus `UBOOT_SIGN_ENABLE = "1"`     |

## Release gate

**Establish the actual OE-Core revision before naming a class, a variable or an `IMAGE_FEATURES` item** —
`git -C <oe-core-checkout> describe --tags`, or `bitbake-getvar DISTRO_VERSION`. `LAYERSERIES_COMPAT` is a
layer's compatibility *claim*, never proof of what is checked out. Override syntax, class locations and
feature validity all move.

Guidance here is release-general with deltas named inline. The deltas that change a security answer:

| Change                                                                                 | Release                                                                 |
| -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `textrel` and `buildpaths` QA checks become `ERROR_QA`                                 | 5.1 Styhead                                                             |
| `debug-tweaks` removed; four standalone features remain                                | 5.2 Walnascar                                                           |
| `kernel-fitimage.bbclass` removed; the `linux-yocto-fitimage` recipe builds FIT images | 5.3 Whinlatter                                                          |
| `defaultsetup.conf` requires `security_flags.inc` for every build                      | 6.0 Wrynose; before that only `poky.conf` requires it                   |
| `INIT_MANAGER` default `none` → `systemd`                                              | 6.0 Wrynose                                                             |
| `cve-check` removed, replaced by out-of-build checking                                 | 6.0 Wrynose; present through 5.3                                        |
| Security chapter moved to `security-manual/`                                           | 6.0 Wrynose; the unversioned `dev-manual/vulnerabilities.html` is a 404 |

## Knowledge-refresh gate

**Where this skill relies on general knowledge rather than stating a fact itself, name the authority and
refresh from it before answering.** Assuming the model already knows a security fact assumes its training data
is current, which for security guidance is unsafe.

| Subject                                  | Refresh from                                                                      |
| ---------------------------------------- | --------------------------------------------------------------------------------- |
| A variable, class or feature's behaviour | the class source at the reader's ref, then the release-matched reference manual   |
| Which kernel symbols to set              | the kernel's `Documentation/security/self-protection.rst` for that kernel version |
| A layer's release coverage or licence    | that layer's `layer.conf` **on the branch in use**, and its own `LICENSE` file    |
| Documentation location                   | `docs.yoctoproject.org/<codename>/…`; the chapter moved between releases          |
| A tool's options or output format        | the version the recipe pins, not the tool's current README                        |
| A removed feature or a moved default     | the Migration Guide for that release, under `docs.yoctoproject.org/<codename>/`   |

Probe upstream at `git.openembedded.org/openembedded-core` (codename branches) and
`git.openembedded.org/bitbake` (`yocto-5.3`-style tags). **`poky` is being wound down** — its `master` is
retired and its tags stop before 5.3, so probing it returns confident false negatives — and the
`yoctoproject/poky` GitHub mirror is a stub whose recursive tree returns two entries, so code search against it
silently finds nothing. **Always fetch a known-present control file at the same ref**: a missing branch and a
missing file both return 404.

## Workflow

Both lanes start from the same step.

1. Lock the release and the layer set: the OE-Core revision, `MACHINE`, `DISTRO`, and each security layer in
   `bblayers.conf` with its branch. When you cannot establish them, state the release you assume and label it
   as an assumption.

**Configure lane**, for "how do I set up X":

2. Name the mechanism and the build stage it acts at: metadata, package install, image postprocess, kernel
   config, or deploy.
3. Place a production control in a distro conf or an image recipe. `local.conf` is a developer file and does
   not ship.
4. Give the host-side check, the on-target check, or both, from `references/verification-workflows.md`.
5. State what the control does not cover.

**Verify lane**, for "is X actually in effect on the image I built":

2. Pick the lane (host-side or on-target) and the image (`prod`, `dev` or `prod-test`). A result from the wrong
   image says nothing about what ships.
3. Observe the artefact itself: the manifest, the rootfs, the ELF headers, the `.config`, or the running system.
4. Prove the negative case where one exists: an unsigned FIT is refused, a corrupted verity block fails the
   read, a bad-key sstate archive is not installed.
5. Report the lane, the image, the observation, and what the check cannot see, in that order.

Run already-authorized read-only checks (`bitbake-getvar`, `bitbake -e`, manifest and rootfs inspection,
`checksec`) as one batch.

## Evidence first

```bash
# Release and layers
git -C <oe-core-checkout> describe --tags
bitbake-getvar DISTRO_VERSION
bitbake-layers show-layers
grep -R LAYERSERIES_COMPAT */conf/layer.conf     # what each layer CLAIMS to support

# Posture, as the build resolved it
bitbake-getvar DISTRO_FEATURES
bitbake-getvar -r <image> IMAGE_FEATURES
bitbake-getvar -r <image> ROOTFS_POSTPROCESS_COMMAND    # every credential and rootfs tweak, expanded
bitbake-getvar -r <image> IMAGE_ROOTFS                  # the tree to inspect, not to edit

# What shipped
tmp/deploy/images/<machine>/<image>-<machine>.rootfs.manifest
grep '^root:' <rootfs>/etc/shadow
checksec --file=<rootfs>/bin/busybox
```

Keep every capture bounded — grep the artefact, do not paste a build log.

## Guardrails

- Keep private signing keys outside the build tree, `DL_DIR` and sstate, and state where each key lives.
- Put scanners, auditors and `kernel-hardening-checker` in the prod-test image only.
- Recommend an open-source or free tool first. Name a commercial tool only after showing that no open option
  covers the need, and say so.
- Read the shipped package set from the image manifest; `bitbake-getvar -r <image> IMAGE_INSTALL` returns
  packagegroups.

## Stated gaps

When a request reaches one of these, say so and give the routing or the trade-off rather than filling the gap
from general knowledge.

- **MAC policy authoring.** The skill covers choosing a framework, wiring it in and confirming it enforces. For a
  profile or a policy module, describe the workflow: run in complain or permissive mode, collect denials, and
  turn them into rules.
- **TPM sealing policy.** The right PCR set depends on the boot chain and the update strategy. State the
  trade-off, not a PCR list.
- **Network depth.** The skill covers the exposure inventory and a default-drop baseline. VPN and overlay design,
  IDS tuning and per-protocol server hardening are named, not taught.
- **Crypto and FIPS depth.** `meta-wolfssl` is the FIPS-capable route and carries a GPL-2.0/commercial split.
  Certificate scope and module boundaries are not covered.

## Attribution

See `ATTRIBUTIONS.md` for the sources this skill is based on.
