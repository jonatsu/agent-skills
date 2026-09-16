# Attributions

## Current skill

- Skill: `yocto-security-hardening`
- Current author: Joonas Onatsu
- Declared license: MIT
- Status: original material, written 2026-09-08 from upstream source and documentation.

**These records are permanent.** A source entry is not closed by later editing, and it is kept in the past
tense once the material it describes is gone, so a reader who reaches an older revision can establish what the
relationship was.

## Independent write-up, not an adaptation

The research corpus behind this skill includes conference and training material licensed **CC BY-SA** (4.0 and
3.0 decks, 2.0 UK manuals), while this package is declared MIT. The two are not compatible for a derivative
work, so the skill was written as an **independent write-up**: subjects were selected from the research, and
every mechanism, sequence, example and command was derived from primary sources — the classes, configuration
files and recipes named below, read at named refs.

This matters because the sibling skill `yocto-openembedded-development` had a CC BY-SA/MIT conflict found on
2026-09-07 and resolved on 2026-09-08 by independent re-derivation; its `ATTRIBUTIONS.md` carries that record
permanently. This package was written under that constraint from the start rather than repaired into it.

**Rewriting wording is not what makes a work independent.** Selection and arrangement are protectable, so the
test applied here was whether each section's organization comes from a primary source or from a deck. Where a
deck supplied only the *knowledge that a subject mattered*, that influence is recorded below rather than
treated as attribution-free.

## Informed by (subject selection)

Reading these changed which subjects this skill covers. No wording, structure, examples or command sequences
were taken from any of them, and several of their technical claims were corrected against upstream source —
see *Corrections* below.

### Bootlin and conference teaching materials (CC BY-SA)

- Marta Rybczyńska / Bootlin-adjacent conference deck on Yocto security (2025) and a 2026 Yocto reference
  course deck — surfaced the subject list: attack-surface reduction, credentials, read-only rootfs, compiler
  hardening, kernel and bootloader hardening, and the observation that several controls do not do what their
  names say.
- Bootlin embedded-security course slides; Bootlin best-practices decks (Belloni 2020, Dautheribes 2024);
  a 2022 A/B-update deck.
- Notices carried by those sources: © Bootlin and the respective authors, Creative Commons BY-SA 3.0/4.0.
- The Yocto Project 5.0 and 6.0 reference manuals, CC BY-SA 2.0 UK.

Local copies live outside this repository. The survey that inventoried them is research material, not part of
this package.

### `meta-avb` (problem statement only)

The observation that dm-verity's root hash creates a circular dependency between the initramfs and rootfs
tasks — a build-graph problem rather than a generic Linux one — was taken from that project's README as a
*problem statement*. Its approach is described in `references/chain-of-trust-wiring.md` as one of two options,
with its unresolved licence (`NOASSERTION`) stated. No code or configuration was adopted.

### Sources supplied 2026-09-08 for the encryption, network and MAC sections

Three inputs arrived while those sections were being written. What each changed is stated exactly, because
two of them changed less than they appear to.

- **Root Commit, "Yocto Project and OpenEmbedded Training Course"** (Michael Opdenacker), revision dated
  2026-06-13, 282 pages, fetched from the publisher. A newer revision of a deck already in the research
  corpus. Its security chapter carries an explicit *not covered* slide naming firewalls, block-device and
  filesystem encryption, extended file attributes and LSMs — so it **confirmed the three gaps rather than
  filling them**, and no material from it entered those sections. Its own closing slide names the same
  subjects as remaining work. Licence per the publisher's terms; nothing was adapted.
- **An `embedded.com` overview article on securing Yocto-built systems**, supplied by the user. Overview
  depth, no mechanism detail, and no author or date given on the page. It contributed exactly one thing: a
  pointer to a `meta-encrypted-storage` layer for LUKS, which a direct check showed was **last pushed in
  2017**. That correction is in `references/storage-encryption.md`; nothing else was taken.
- **`ni/meta-selinux`** (National Instruments), supplied by the user. Compared against upstream
  `meta-selinux` at scarthgap: same collection name, priority and `LAYERSERIES_COMPAT`, with NI's own branch
  scheme. It supplied the observation that a product distro maintains a downstream SELinux tree, recorded in
  `references/mac-frameworks.md` as a worked example while routing the dependency upstream.

### Two further sources surveyed 2026-09-08, both used for facts only

Both were read after the encryption, network and MAC sections existed, and both changed the skill enough to be
recorded here. Neither supplied wording, structure, section ordering, examples or exercises.

- **Bootlin, Embedded Linux Security course lab manual**, the edition built for an NXP i.MX93 development
  board (43 pages, CC BY-SA). Licence-incompatible with this MIT package, so nothing was adapted; it was read
  for mechanisms and for *verification shapes*, which are this skill's currency. What it changed: the
  observation that a signing key must reach U-Boot's control device tree as well as the FIT recipe; the
  requirement that an unsigned image and a wrong-key image fail distinguishably; the platform-level
  generalisation of ROM-stage verification, including that programming a root-key hash enforces nothing until
  the part's lifecycle state changes; the build-side half of an A/B updater (CA-not-leaf keyring, signing-time
  validation, layout consistency); PKCS#11 as the portable key-custody boundary with on-device key generation;
  and the SELinux relabel and login-mapping facts. **Everything board-specific was deliberately excluded** at
  the user's instruction — the container format, the vendor tooling, the fuse indices, the lifecycle state
  names and the board setup are instantiation, not mechanism, and the skill states the platform prerequisite
  instead.
- **Matt St. Onge, "The Embedded Linux Security Handbook"** (Packt, 2025, 278 pages). Commercially published
  and all rights reserved; read for facts and for gap discovery only, with every finding restated
  independently. It is RHEL/Fedora- and x86/UEFI-shaped rather than a build-system book, so most of it does
  not transfer. What it changed: the named anti-pattern in `references/storage-encryption.md` — its LUKS
  automation stores a key file in cleartext on an unencrypted root filesystem and presents this as an
  improvement, which is the clearest published instance of the failure mode this skill's Iron Law targets; the
  key-recovery paragraph; the non-IP exposure section in `references/network-and-services.md`; and the UEFI
  Secure Boot subsection in `references/chain-of-trust-wiring.md`, kept deliberately thin. Its TPM taxonomy is
  wrong in at least two checkable places, so nothing was taken from it on that subject.

The general-Linux residue of both — seccomp, systemd sandboxing, SELinux operations, PKI practice, firmware
update security — was deliberately **not** written into this skill, per its build-system-shaped scope.

## Primary sources read at named refs

These are verification sources: they establish public facts and are cited near the affected claims. Under this
repository's provenance policy, verification-only use creates no attribution obligation; they are listed for
traceability, and because every corrected claim below depends on one.

`openembedded-core` at **`scarthgap`** and **`master`** — `classes-recipe/rootfs-postcommands.bbclass`,
`classes-recipe/image.bbclass`, `classes-recipe/kernel-yocto.bbclass`, `classes-recipe/kernel-fitimage.bbclass`,
`classes-recipe/testimage.bbclass`, `classes-recipe/overlayfs-etc.bbclass`, `classes/extrausers.bbclass`,
`classes-global/insane.bbclass`, `classes-global/sstate.bbclass`, `conf/bitbake.conf`,
`conf/distro/defaultsetup.conf`, `conf/distro/include/security_flags.inc`,
`conf/distro/include/rust_security_flags.inc`, `lib/oe/rootfs.py`,
`lib/oe/package_manager/ipk/__init__.py`, `lib/oeqa/selftest/cases/reproducible.py`,
`recipes-core/systemd/systemd_255.22.bb` (the `cryptsetup`, `tpm2`, `selinux` and `smack` `PACKAGECONFIG`
entries, the default set, and `FILES:${PN}-crypt`), and `recipes-extended/iptables/iptables_1.8.10.bb` (the
`libnftnl` option and the `xtables-nft-multi` symlinks it gates).

`bitbake` at **`yocto-5.0.12`** — `lib/bb/siggen.py`.

`meta-security` at **`scarthgap`** — `classes/check_security.bbclass`, `classes/dm-verity-img.bbclass`,
`recipes-kernel/linux/linux-yocto_%.bbappend` and `linux-yocto_security.inc`, `recipes-core/images/*`,
`recipes-core/packagegroup/packagegroup-core-security.bb`, `recipes-scanners/checksec/checksec_2.6.0.bb`,
`recipes-compliance/lynis/lynis_3.1.6.bb`, `recipes-mac/AppArmor/apparmor_3.1.3.bb`, the
`recipes-security/` and `meta-tpm/recipes-tpm2/` inventories, `lib/oeqa/runtime/cases/{checksec,aide}.py`,
and every sublayer's `conf/layer.conf`.

`meta-openembedded` at **`scarthgap`**, **`walnascar`** and **`master`** —
`meta-oe/recipes-security/kernel-hardening-checker`, `meta-oe/recipes-crypto/cryptsetup`, and
`meta-networking/recipes-filter` (nftables and the rest of that directory's inventory).

`meta-selinux` at **`scarthgap`** — `conf/layer.conf`, and the root listing that shows the layer carries no
licence file of its own.

U-Boot at **`v2025.10`** — `boot/Kconfig`. systemd at **`v255`** — `meson_options.txt`, for the `apparmor`
option's auto-detected feature type, which is what makes OE-Core's missing `PACKAGECONFIG` consequential.

## Corrections made against those sources

Recorded because the corrected claims circulate widely, and because a reader comparing this skill against the
decks it was informed by should know where they diverge deliberately.

| Secondary claim                                                          | What the source shows                                                                       |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| The `security` `DISTRO_FEATURE` "adds a few kernel fragments"            | It adds **none** by itself; four further conditions gate them, one keyed on `IMAGE_CLASSES` |
| `CVE_CHECK_SKIP_RECIPE` reports skipped recipes as *Patched*             | It returns four empty lists — no annotation at all                                          |
| `security_flags.inc` is default-included "for `nodistro` only" in 6.0    | `bitbake.conf` includes `defaultsetup.conf` for every build, and master's requires it       |
| `extrausers` has six commands; `passwd-expire` is 6.0-only               | Seven, including `passwd-expire`, on the `scarthgap` branch                                 |
| `kernel-hardening-checker` reached `meta-oe` at Walnascar                | Present on `scarthgap` too, at a **newer** version (0.6.17.1) than `walnascar` (0.6.10)     |
| Requiring `rust_security_flags.inc` adds hardening                       | It only removes PIE from the Rust toolchain recipes; it adds none                           |
| `cve-check` was removed in 6.0, so current guidance is wrong for the LTS | Removal is real but confined to `master`; the class is present on every released series     |

## Scope of this record

Bounded. The decks were compared by subject, sequence and command against this package while it was written;
the Yocto manuals were not compared passage by passage; no legal advice was sought or given. Treat "no
correspondence found" as a bounded negative result rather than proof of independence.
