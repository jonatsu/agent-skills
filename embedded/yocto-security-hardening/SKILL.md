---
name: yocto-security-hardening
description: "Yocto/OpenEmbedded security hardening: configure a control, then prove it on the built artefact. Use for IMAGE_FEATURES and distro hardening, root credentials, read-only rootfs, PACKAGE_EXCLUDE, security_flags.inc and checksec, kernel hardening fragments and kernel_configcheck, signed-FIT and dm-verity wiring, sstate and mirror trust, meta-security. Route BitBake mechanics and CVE/SBOM to yocto-openembedded-development, U-Boot verification to u-boot-development, board debugging to embedded-linux-bringup."
license: MIT
compatibility: Requires a BitBake/OE-Core checkout and an initialised build directory. Class names, variables and valid IMAGE_FEATURES items are release-specific; guidance is written for 5.0 Scarthgap with 6.0 deltas named inline. On-target verification needs QEMU or a reachable board plus testimage. checksec, kernel-hardening-checker and Lynis come from meta-security or meta-openembedded, which must be added to bblayers.
metadata:
  author: Joonas Onatsu
---

# Yocto / OpenEmbedded Security Hardening

**IRON LAW: A security setting is a claim, not a control. You MUST verify the property on the built artefact
and MUST NOT report a setting, a variable value, or a feature in `IMAGE_FEATURES` as evidence that the
property holds. A passing security *test* is also a claim — read what it asserts before treating a green suite
as evidence.**

The second half is not rhetorical. Upstream `meta-security`'s own `checksec` oeqa case asserts nothing when
its regex matches, and inspects PID 1 rather than the shipped binaries; it has been that way since 2019. The
first half has an equally concrete basis: `security_flags.inc` carries **21 `:pn-` opt-out lines**, so
"hardening is on" is false for `busybox`, `grub` and a dozen other named recipes on a stock build.

Every answer this skill gives pairs a control with the observation that settles it. A configuration snippet
alone is an incomplete answer.

## Scope

**In:** configuring a security control in a Yocto build, and proving on the artefact that it took effect —
image and distro composition, credentials, root filesystem state, compiler and kernel hardening, the build
side of the boot chain, build and supply-chain trust, and both verification lanes.

**Out:** auditing an artefact you did not build (that starts from an image, not from metadata); CVE and SBOM
work; U-Boot's own verification mechanics; runtime board debugging; MAC policy authoring and disk or network
hardening, which this skill deliberately does not yet cover — see *Stated gaps*.

### Route to a sibling skill

| Task                                                                                             | Skill                              |
| ------------------------------------------------------------------------------------------------ | ---------------------------------- |
| BitBake mechanics, recipes, `.bbappend`, sstate mechanics, licence obligations, `cve-check`/SBOM | **yocto-openembedded-development** |
| U-Boot verified boot, FIT verification, console lockdown, boot scripts                           | **u-boot-development**             |
| Runtime kernel, driver, verity or OTA behaviour on a booted board                                | **embedded-linux-bringup**         |
| `.kas.yml` orchestration                                                                         | **kas-build-orchestration**        |
| Buildroot equivalents                                                                            | **buildroot-development**          |

### Route the task to a reference

| Task or symptom                                                                                       | Reference                                     |
| ----------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| A setting's name does not match its effect; "I set this, why is it not doing that"                    | `references/misleading-controls.md`           |
| Feature and package reduction, root credentials, read-only rootfs, `/etc` overlays, service privilege | `references/image-attack-surface.md`          |
| `security_flags.inc`, FORTIFY/RELRO/PIE/stack protector, `checksec`, packaging QA checks              | `references/compiler-and-binary-hardening.md` |
| Kernel config fragments, `kernel_configcheck` audit levels, `kernel-hardening-checker`, MAC packaging | `references/kernel-hardening.md`              |
| Signed FIT, dm-verity, initramfs bundling, IMA/EVM wiring, key handling                               | `references/chain-of-trust-wiring.md`         |
| sstate and mirror trust, `SRC_URI` checksums, `AUTOREV`, reproducibility, release gates               | `references/build-and-supply-chain-trust.md`  |
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
feature validity all move; that mechanism is `yocto-openembedded-development`'s Iron Law and applies here
unchanged.

Guidance here is release-general with deltas named inline. The deltas that change a security answer:

| Change                                                         | Release                                                                  |
| -------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `debug-tweaks` removed; four standalone features remain        | 5.2 Walnascar                                                            |
| `security_flags.inc` opt-in → required by `defaultsetup.conf`  | opt-in at 5.0; on master `defaultsetup.conf` is included for every build |
| `INIT_MANAGER` default `none` → `systemd`                      | scarthgap → master                                                       |
| `cve-check` present → removed on master, replaced out-of-build | present on every released series including 5.0 and 5.3                   |
| Security chapter moved to `security-manual/`                   | 6.0; the unversioned `dev-manual/vulnerabilities.html` is a 404          |

## Knowledge-refresh gate

⛔ **Where this skill relies on general knowledge rather than stating a fact itself, name the authority and
refresh from it before answering.** Assuming the model already knows a security fact assumes its training data
is current, which for security guidance is unsafe.

| Subject                                  | Refresh from                                                                      |
| ---------------------------------------- | --------------------------------------------------------------------------------- |
| A variable, class or feature's behaviour | the class source at the reader's ref, then the release-matched reference manual   |
| Which kernel symbols to set              | the kernel's `Documentation/security/self-protection.rst` for that kernel version |
| A layer's release coverage or licence    | that layer's `layer.conf` **on the branch in use**, and its own `LICENSE` file    |
| Documentation location                   | `docs.yoctoproject.org/<codename>/…`; the chapter moved between releases          |
| A tool's options or output format        | the version the recipe pins, not the tool's current README                        |

Probe upstream at `git.openembedded.org/openembedded-core` (codename branches) and
`git.openembedded.org/bitbake` (`yocto-5.3`-style tags). **`poky` is being wound down** — its `master` is
retired and its tags stop before 5.3, so probing it returns confident false negatives — and the
`yoctoproject/poky` GitHub mirror is a stub whose recursive tree returns two entries, so code search against it
silently finds nothing. **Always fetch a known-present control file at the same ref**: a missing branch and a
missing file both return 404.

## Workflow

Two lanes. The release gate is shared and blocking.

**Shared entry:**

- [ ] **⛔ BLOCKING — Lock the release and the layer set.** Revision, `MACHINE`, `DISTRO`, and which security
  layers are in `bblayers.conf` with which branch. If it cannot be established, state the assumed release and
  LABEL the assumption.

**Configure lane** — "how do I set up X":

- [ ] **⚠️ REQUIRED — Name the mechanism, not just the variable.** What the setting does, and which layer of
  the build it acts at (metadata, package install, image postprocess, kernel config, deploy).
- [ ] **⚠️ REQUIRED — Place it where it can ship.** A production control belongs in a distro conf or an image
  recipe; `local.conf` is a developer's file and is not part of the release artefact.
- [ ] **⚠️ REQUIRED — Give the verification in the same answer.** The host-side check, the on-target check, or
  both, from `references/verification-workflows.md`. An answer without one is incomplete.
- [ ] **⚠️ REQUIRED — Name what it does not cover.** Every control in this skill has a stated limit; say it.

**Verify lane** — "is X actually in effect":

- [ ] **⛔ BLOCKING — Pick the lane and the image.** Host-side or on-target, and against `prod`, `dev` or
  `prod-test`. A result from the wrong image is not evidence about what ships.
- [ ] **⚠️ REQUIRED — Observe the artefact.** Read the manifest, the rootfs, the ELF headers, the `.config` or
  the running system — never the variable that was meant to produce them.
- [ ] **⚠️ REQUIRED — Prove the negative case where one exists.** An unsigned FIT must be refused, a corrupted
  verity block must fail the read, a bad-key sstate archive must be rejected. A control never observed failing
  has not been shown to work.
- [ ] **⚠️ REQUIRED — Report lane, image, observation, and blind spot.** In that order.

Read-only checks that are already authorized — `bitbake-getvar`, `bitbake -e`, manifest and rootfs
inspection, `checksec` — run in a batch; do not stop to ask after each.

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

## Anti-patterns

- MUST NOT report a variable value, an `IMAGE_FEATURES` entry, or "the setting is in the distro conf" as
  evidence that a security property holds.
- MUST NOT read `bitbake-getvar -r <image> IMAGE_INSTALL` as the shipped package set — it returns
  packagegroups. The manifest is the only authority.
- MUST NOT treat a green oeqa security suite as a property check; upstream's cases are smoke tests and at
  least one asserts nothing at all.
- MUST NOT say "hardening is enabled" after requiring `security_flags.inc`. Name the exempted recipes, or
  check the specific binaries in question.
- MUST NOT read a missing `FORTIFY_SOURCE` as "unsupported" — at `-O0` the flag is dropped silently by design.
- MUST NOT treat a `kernel_configcheck` pass as proof a hardening symbol survived: the default audit level
  filters to boot-affecting options and its findings are warnings.
- MUST NOT ship scanners, auditors or `kernel-hardening-checker` in production; they belong in the prod-test
  image.
- MUST NOT probe `poky` for a current fact, and MUST NOT judge a layer's release coverage from one branch.
- MUST NOT recommend a commercial tool without first establishing that no open-source or free option covers
  the need, and saying so.
- MUST NOT invent a MAC policy, disk-encryption or network-hardening recommendation and present it as this
  skill's guidance — see *Stated gaps*.
- MUST NOT write a private signing key into the build tree, `DL_DIR` or sstate, or leave a key's provenance
  implied.

## Stated gaps

Naming these is part of the skill's contract; filling them from general knowledge is not.

- **Disk and filesystem encryption, network hardening, and MAC policy authoring.** Packaging is covered;
  policy and design are not, and the material to do them properly is not yet in hand.
- **Crypto and FIPS depth.** Pointer only. `meta-wolfssl` is the FIPS-capable route and carries a
  GPL-2.0/commercial split; certificate scope and module boundaries are unverified here.
- **`meta-security` scanner health.** Reports that `buck-security`, `checksec` and `nikto` are broken in the
  layer are **unverified** and must not be repeated as fact.
- **Auditing an image you did not build** — a different starting state, and a different task.

## Reference pointers

Cite the release-matched manual; the codename is in the docs URL path.

- **docs.yoctoproject.org** — Reference Manual (variables, classes, QA checks), Development Tasks Manual
  (*Making Images More Secure*, judged thin by the community that maintains it), the **Security manual**, and
  the Migration Guides, which are where a removed feature or a moved default is actually recorded.
- **`git.openembedded.org/openembedded-core`** and **`/bitbake`** — the authoritative source for any class or
  variable claim, at the reader's ref.
- **`git.yoctoproject.org/meta-security`** — the layer itself; check `layer.conf` on the branch in use.
- **Kernel Self Protection Project** and the kernel's own `Documentation/security/self-protection.rst` — for
  which symbols to set on the reader's kernel version.

## Attribution

See `ATTRIBUTIONS.md`. This skill is an independent write-up derived from upstream source and documentation;
the CC BY-SA teaching materials that informed subject selection are recorded there and no material was adapted
from them.
