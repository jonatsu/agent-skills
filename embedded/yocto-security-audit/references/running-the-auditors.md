# Running an Auditor, and Reading What It Disabled

Hardening owns **wiring** an auditor into a prod-test image. This file owns **running** one and interpreting
its output.

⛔ **Every auditor here ships with checks turned off by default.** Reporting a clean run without saying which
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

- **Six check families are disabled by default**: `checksum`, `firewall`, `packages_problematic`, `services`,
  `sshd`, `usermask`. Between them that is most of what an auditor would say about a network-facing image.
- **Standard output goes to `/dev/null`.** The findings exist only in `${T}/log.do_checksecurity.*`, which is
  under `tmp/work` and is deleted by `rm_work`.
- **The task cannot fail the build.** It is a postprocess command with no assertion; a finding is a line in a
  log nobody reads.

```bash
# Where the output actually is
bitbake-getvar -r <image> T
cat <T>/log.do_checksecurity.*
```

`buck-security-native` **does** build at `scarthgap` — verified — so the class works as written. Its silence is
by design, not by breakage.

## `checksec` — and the one that does not build

Covered in `binary-and-kernel-findings.md` for what its output means. One operational fact belongs here:
**`checksec-native` does not build at `scarthgap`** without a one-line `.bbappend`, because the recipe keeps
`procps` in `RDEPENDS` while `procps` has no native variant. Hardening's
`compiler-and-binary-hardening.md` carries the verified fix. Without it, the host-side scanning lane is simply
unavailable and you are pushed to the on-target lane.

## Lynis and OpenSCAP

Both are packaged upstream in `meta-security` — `lynis` 3.1.6 and `openscap` 1.3.9 with
`scap-security-guide` 0.1.71 at `scarthgap`. They are the answer to "what user-space auditor should I run", and
they belong in a **prod-test image**, never in production: an auditor on a shipped device is a map of the weak
spots.

```bash
lynis audit system --no-colors --quiet          # on target, in the prod-test image
oscap xccdf eval --profile <profile> /usr/share/xml/scap/ssg/content/<datastream>.xml
```

**Not run here.** Everything in this section is read from the recipes and the tools' own documentation, not
observed. Confirm option names and output format against the packaged version — the recipes pin specific
releases and both tools change their CLI across major versions.

Two cautions that apply regardless of version:

- **Lynis is written for general-purpose Linux distributions.** A large fraction of its checks assume a package
  manager, a mail transfer agent, a full PAM stack or a desktop. On a minimal embedded image many findings are
  "not installed", which is the intended state, not a gap. Its hardening index is not a number to chase.
- **OpenSCAP evaluates a profile.** The result is meaningless without naming which datastream and which
  profile, and the shipped SSG profiles target enterprise distributions rather than embedded images. Read the
  profile before reporting the score.

## The general rule

Every auditor in this space reports against **its own model of a correct system**, and none of those models is
an embedded Linux image. So:

- [ ] **Name the tool, its version, and its configuration** in the result. "Lynis reports 12 warnings" is not a
  finding until you say which profile and which checks were skipped.
- [ ] **Read the disabled-by-default list first**, then the findings.
- [ ] **Separate "not applicable to an embedded image" from "not checked" from "checked and clean".** All three
  look the same in most output formats, and only the third is evidence.
- [ ] **Never ship the auditor.** Results come from a prod-test image built from prod's package set — see
  hardening's `verification-workflows.md`.

## Open source only

A commercial scanner may be named to illustrate a category, never recommended, unless no open-source option
covers the need and that gap is stated explicitly. Where a hosted service is involved, say what leaves the
building: uploading a package manifest discloses the product's complete software composition with versions.
