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
`lib/oe/package_manager/ipk/__init__.py`, `lib/oeqa/selftest/cases/reproducible.py`.

`bitbake` at **`yocto-5.0.12`** — `lib/bb/siggen.py`.

`meta-security` at **`scarthgap`** — `classes/check_security.bbclass`, `classes/dm-verity-img.bbclass`,
`recipes-kernel/linux/linux-yocto_%.bbappend` and `linux-yocto_security.inc`, `recipes-core/images/*`,
`recipes-core/packagegroup/packagegroup-core-security.bb`, `recipes-scanners/checksec/checksec_2.6.0.bb`,
`recipes-compliance/lynis/lynis_3.1.6.bb`, `lib/oeqa/runtime/cases/{checksec,aide}.py`, and every sublayer's
`conf/layer.conf`.

`meta-openembedded` at **`scarthgap`**, **`walnascar`** and **`master`** —
`meta-oe/recipes-security/kernel-hardening-checker`.

U-Boot at **`v2025.10`** — `boot/Kconfig`.

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
