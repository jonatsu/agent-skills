# Running an Auditor, and Reading What It Disabled

Hardening owns **wiring** an auditor into a prod-test image. This file owns **running** one and interpreting
its output.

**Every auditor here ships with checks turned off by default.** Reporting a clean run without saying which
checks were disabled is the exact failure this skill exists to prevent. Read the defaults before you read the
findings.

## `check_security.bbclass` — the build-time gate, and it is quieter than it looks

`meta-security` ships a class that runs `buck-security` over the rootfs as a `ROOTFS_POSTPROCESS_COMMAND`.
Its entire body:

```bitbake
check_security () {
    ${STAGING_BINDIR_NATIVE}/buck-security -sysroot ${IMAGE_ROOTFS} \
        -log ${T}/log.do_checksecurity.${PID} \
        -disable-checks "checksum,firewall,packages_problematic,services,sshd,usermask" -no-sudo > /dev/null
}
```

Three things to know before treating a clean build as a clean audit:

- **Six of buck-security's thirteen checks are disabled**: `checksum`, `firewall`, `packages_problematic`,
  `services`, `sshd`, and `usermask`. The seven that run are `emptypasswd`, `sgids`, `stickytmp`, `suids`,
  `superusers`, `worldwriteablefiles`, and `worldwriteabledirs`. None looks at SSH configuration, services, or the
  firewall.
- **Standard output goes to `/dev/null`.** The findings exist only in `${T}/log.do_checksecurity.*` in the image's
  work directory. `rm_work` keeps `temp`, so the log survives it.
- **Findings cannot fail the build.** buck-security exits 0 however many warnings it logs; only a startup error,
  such as a missing sysroot, fails the task.

```bash
# Where the output actually is
bitbake-getvar -r <image> T
cat <T>/log.do_checksecurity.*
```

`buck-security-native` **does** build at `scarthgap` — verified — so the class works as written. Its silence is
by design, not by breakage.

## `checksec` — and the one that does not build

Covered in `binary-and-kernel-findings.md` for what its output means. One operational fact belongs here.

`checksec-native` does not build at `scarthgap`: the recipe keeps `procps` in `RDEPENDS` while OE-Core's `procps`
has no native variant. A one-line `.bbappend` restores it:

```bitbake
# checksec_%.bbappend
RDEPENDS:${PN}:class-native = "bash openssl-bin binutils findutils file"
```

Without it, run `checksec` on target in the prod-test image instead.

## Lynis and OpenSCAP

Both are packaged upstream in `meta-security` — `lynis` 3.1.6 and `openscap` 1.3.9 with
`scap-security-guide` 0.1.71 at `scarthgap`. They are the answer to "what user-space auditor should I run", and
they belong in a **prod-test image**, never in production: an auditor on a shipped device is a map of the weak
spots.

```bash
lynis audit system --no-colors --quiet          # on target, in the prod-test image
oscap xccdf eval --results results.xml --report report.html \
    --profile xccdf_org.ssgproject.content_profile_standard \
    /usr/share/xml/scap/ssg/content/ssg-openembedded-ds.xml   # what /usr/share/openscap/run_eval.sh runs
```

**Not run here.** The command lines are confirmed from source at the packaged versions; the output is not
observed. Re-check both when a recipe's pinned release moves, because both tools change their CLI across major
versions.

Two cautions that apply regardless of version:

- **Lynis is written for general-purpose Linux distributions.** A large fraction of its checks assume a package
  manager, a mail transfer agent, a full PAM stack or a desktop. On a minimal embedded image many findings are
  "not installed", which is the intended state, not a gap. Its hardening index is not a number to chase.
- **OpenSCAP evaluates a profile.** The packaged `scap-security-guide` builds only the OpenEmbedded datastream,
  and its one profile, `standard`, describes itself as a documentation sample whose rules "should pass quickly on
  most systems". A passing `standard` run shows that sample held, not that the image meets any benchmark. Name
  the datastream and profile in every result.

## The general rule

Every auditor in this space reports against **its own model of a correct system**, and none of those models is
an embedded Linux image. So:

- [ ] **Name the tool, its version, and its configuration** in the result. "Lynis reports 12 warnings" is not a
  finding until you say which profile and which checks were skipped.
- [ ] **Read the disabled-by-default list first**, then the findings.
- [ ] **Separate "not applicable to an embedded image" from "not checked" from "checked and clean".** All three
  look the same in most output formats, and only the third is evidence.
- [ ] **Never ship the auditor.** Results come from a prod-test image built from prod's package set — see
  the yocto-security-hardening skill's three-image pattern.

## Open source only

A commercial scanner may be named to illustrate a category, never recommended, unless no open-source option
covers the need and that gap is stated explicitly. Where a hosted service is involved, say what leaves the
building: uploading a package manifest discloses the product's complete software composition with versions.
