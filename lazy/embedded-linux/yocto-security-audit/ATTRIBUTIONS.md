# Attributions

## Current skill

- Skill: `yocto-security-audit`
- Current author: Joonas Onatsu
- Declared license: MIT
- Status: original material, written 2026-09-08 from upstream source and from a build and test run of
  `meta-security` performed for this skill.

**These records are permanent.** A source entry is not closed by later editing, and it is kept in the past
tense once the material it describes is gone, so a reader who reaches an older revision can establish what the
relationship was.

## Independent write-up, not an adaptation

The research corpus behind this skill set includes conference and training material licensed **CC BY-SA** and
one commercially published book, while this package is declared MIT. The licences are not compatible for a
derivative work, so the skill was written as an **independent write-up**: subjects were selected from the
research, and every mechanism, command and example was derived from primary sources — the classes, recipes and
test cases named below, read at a named ref, and from observations made by running them.

This is the same constraint applied to the sibling skills `yocto-openembedded-development`,
`yocto-security-hardening` and `yocto-vulnerability-management`.

**This skill leans less on the teaching corpus than either sibling.** Most of its content came from building
and running `meta-security` rather than from reading about it, which is recorded here because it is the reason
so few external sources appear below.

## Informed by (subject selection)

- A 2025 conference deck on Yocto security (CC BY-SA) — surfaced the subject: that `meta-security`'s scanners
  were reported broken, and that Lynis and OpenSCAP are the recommended user-space auditors. **Its scanner
  claim was checked by building and does not hold**; see *Corrections*.
- Bootlin embedded-security course slides and the Yocto Project 5.0/6.0 reference manuals (CC BY-SA 3.0/4.0 and
  CC BY-SA 2.0 UK) — background for what an audit is expected to cover.

Local copies live outside this repository. The survey that inventoried them is research material, not part of
this package.

## Primary sources read at a named ref

Verification sources: they establish public facts and are cited near the affected claims. Under this
repository's provenance policy, verification-only use creates no attribution obligation; they are listed for
traceability.

`meta-security` at **`scarthgap`** (`b13f170`) — `classes/check_security.bbclass`,
`recipes-scanners/checksec/checksec_2.6.0.bb`, `recipes-scanners/buck-security/buck-security_0.7.bb`,
`recipes-core/images/security-build-image.bb` and `security-test-image.bb`,
`recipes-compliance/{lynis,openscap,scap-security-guide}`, `conf/layer.conf`, `kas/kas-security-base.yml` and
`kas/qemux86-64.yml`, and every file in `lib/oeqa/runtime/cases/`.

`openembedded-core` at **`scarthgap`** — `conf/distro/include/security_flags.inc` for the opt-out list,
`recipes-extended/procps/procps_4.0.4.bb` and `recipes-extended/net-tools/net-tools_2.10.bb` for their
`BBCLASSEXTEND` state.

`checksec` **2.6.0** as packaged by that layer — `--help` and `--format=json` output, captured by running it.

## Observations made for this skill

Unusually for this repository, a substantial part of this skill rests on measurements rather than reading. They
were produced in a disposable kas-container builder at `scarthgap`/`qemux86-64`, Docker, TCG emulation and
slirp networking, using the layer's **own** `kas/qemux86-64.yml` so that results describe the layer as its
maintainers ship it.

- `bitbake buck-security checksec nikto` — exit 0, all three packaged.
- `bitbake checksec-native` — fails at dependency resolution; fixed with a one-line `RDEPENDS:${PN}:class-native`
  override and rebuilt successfully.
- `bitbake buck-security-native` — succeeds.
- `bitbake security-test-image` — 9890 tasks, exit 0.
- `bitbake security-test-image -c testimage` — 58 results, 33 passed, 16 failed, 9 skipped, recorded per case.
- `checksec --format=json` against a real ELF — the ten key names now quoted in
  `binary-and-kernel-findings.md`.
- The unpacked rootfs — `/etc/shadow`, `/etc/ssh/sshd_config`, and `testdata.json`'s variable set.

The builder is not part of this package and no longer needs to exist; the observations are recorded in the
research corpus and in the text.

## Corrections made against those sources

| Secondary claim                                                          | What building it shows                                                                                    |
| ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| `buck-security`, `checksec` and `nikto` are broken in `meta-security`    | All three build and package cleanly at `scarthgap`. The blanket claim does not hold                       |
| (implied) the `checksec` native path is available for host-side scanning | `checksec-native` is unbuildable: `procps` has no native variant. One line fixes it                       |
| The inverted-assertion defect is one case in `checksec.py`               | It is **10 cases across 5 files**; excluding `smack.py`, 10 of 29 test methods assert nothing on success  |
| (author's own, before testing) `buck-security-native` fails the same way | **Wrong.** It builds. The prediction came from grepping a path that does not exist — recorded as a lesson |

The last row is kept deliberately. An empty result from an unverified path was read as evidence of absence; the
finding it produced was published as a lead and then retracted after a one-command test.

## Scope of this record

Bounded. The decks were compared by subject against this package while it was written; the Yocto manuals were
not compared passage by passage. **The observations cover one release, one architecture and one run
environment**, and building a recipe is not the same as exercising the tool it installs — limits stated in
`SKILL.md` rather than left for a reader to infer. Treat "no correspondence found" as a bounded negative result
rather than proof of independence.
