# `meta-security` and Judging a Third-Party Security Layer

**Upstream wins by default.** Reach for a third-party layer only with a stated reason — a capability or a
patch set upstream lacks — and record the reason next to the dependency.

## What upstream actually ships

Read from a `scarthgap` clone of `git.yoctoproject.org/meta-security`. This is more than most secondary
summaries describe:

| Area                | Contents                                                                                                         |
| ------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Sublayers           | `meta-hardening`, `meta-integrity` (IMA/EVM), `meta-tpm`, `meta-parsec`                                          |
| Build-time gate     | `classes/check_security.bbclass`                                                                                 |
| Image integrity     | `classes/dm-verity-img.bbclass`, `recipes-core/images/dm-verity-image-initramfs.bb`, `docs/dm-verity*.txt`       |
| Images              | `security-build-image`, `security-client-image`, `security-server-image`, `security-test-image`                  |
| Packagegroups       | `packagegroup-core-security` and the `-utils`/`-scanners`/`-audit`/`-ids`/`-mac` groups it aggregates            |
| Compliance auditing | **`lynis` 3.1.6**, `openscap` 1.3.9, `scap-security-guide` 0.1.71                                                |
| Scanners            | **`checksec` 2.6.0** (with `BBCLASSEXTEND = "native"`), `buck-security`, `arpwatch`, `clamav`, `chkrootkit`      |
| Intrusion detection | `aide`, `crowdsec`, `ossec`, `samhain`, `suricata`, `tripwire`                                                   |
| MAC                 | AppArmor, SMACK, `ccs-tools`                                                                                     |
| Kernel              | `lkrg`                                                                                                           |
| Runtime tests       | `lib/oeqa/runtime/cases/` — aide, apparmor, checksec, clamav, firejail, samhain, smack, sssd, suricata, tripwire |

Two consequences worth acting on. **Lynis is packaged upstream**, so a third-party layer's Lynis recipe is a
re-implementation rather than the reference. And **`checksec` has a `-native` variant**, which is what makes
the host-side lane in `verification-workflows.md` possible without a board.

## Caveats to state whenever the layer is recommended

- **Release coverage is narrow.** All five sublayers declare `LAYERSERIES_COMPAT = "nanbield scarthgap"`. The
  branch must match the release; this layer does not span series the way `meta-wolfssl` or `meta-timesys` do.
  Check `layer.conf` on the branch you intend to use, not on `master`.

- **`check_security.bbclass` is quieter than it looks.** It runs `buck-security` against `${IMAGE_ROOTFS}` as
  a `ROOTFS_POSTPROCESS_COMMAND`, and:

  ```bitbake
  check_security () {
      ${STAGING_BINDIR_NATIVE}/buck-security -sysroot ${IMAGE_ROOTFS} \
          -log ${T}/log.do_checksecurity.${PID} \
          -disable-checks "checksum,firewall,packages_problematic,services,sshd,usermask" -no-sudo > /dev/null
  }
  ```

  **Six check families are disabled by default and standard output goes to `/dev/null`.** The findings are in
  `${T}/log.do_checksecurity.*` and nowhere else, and the task cannot fail a build on them. Read that log
  before treating a clean build as a clean audit.

- **The oeqa security cases are smoke tests**, and at least one is a genuine defect. See
  `verification-workflows.md`.

- **Scanner health, measured 2026-09-08.** Secondary sources report `buck-security`, `checksec` and `nikto` as
  broken in the layer. **Built at `scarthgap` with the layer's own `kas/qemux86-64.yml`: all three build and
  package cleanly**, exit 0, no errors — `buck-security` 0.7, `checksec` 2.6.0, `nikto` 2.1.6. The blanket
  "broken" claim does not hold, and must not be repeated.

  **One real defect sits underneath it, and it is narrower and worse-placed than the rumour.**
  `checksec-native` is **unbuildable**: the recipe sets `BBCLASSEXTEND = "native"` while `RDEPENDS:${PN}` keeps
  `procps`, which has no native variant, so BitBake reports `Nothing RPROVIDES 'procps-native'`. The layer's own
  `buck-security` recipe solves exactly this with an `RDEPENDS:${PN}:class-native` override; `checksec` simply
  lacks one. That single missing line disables the host-side scanning lane this skill depends on — see
  `compiler-and-binary-hardening.md` for the verified one-line `.bbappend`.

  Building a recipe is not the same as the tool working. These results cover fetch, compile and package only;
  none of the three has been *run* against an image here.

## Judging any security layer

Four criteria, in the order that eliminates candidates fastest:

1. **Does it maintain a branch for your release?** Enumerate the branches — never generalise from `master`'s
   `layer.conf`. A layer whose `master` targets a development codename may still carry a maintained LTS
   branch, and the reverse happens too.
2. **Is the release branch supported, or merely present?** A maintainer who states that only `master` is
   supported, with release branches community-maintained and unverified, puts an LTS user on an unsupported
   branch by construction. That is a statement to quote, not to soften.
3. **What is the licence, and is it resolvable?** Several security layers report `NOASSERTION` or ship no
   licence file at all — the latter meaning unlicensed by default, not merely unrecognised. Resolve it before
   the layer becomes a dependency, and note that a tool and its Yocto layer often carry different licences.
4. **Where does the data go?** A layer that uploads a package manifest to a hosted service discloses the
   product's complete software composition, with versions, to a third party. Legitimate with an agreement;
   never an incidental default.

**Open source only.** A commercial tool may be named to illustrate a category — what a hosted CVE-monitoring
service is — but recommending one requires first establishing that no open-source or free option covers the
need, and saying so explicitly. The burden is on the commercial entry.

Vendor existence is not evidence about licence: a project can be Apache-2.0 or GPL-2.0 open source and still
be published by a company that sells related products. Read the repository's own `LICENSE`.

## Forward pointers

- Post-quantum crypto and FIPS-validated crypto have no upstream answer; both are pointer-depth in this skill.
  `meta-wolfssl` is the FIPS-capable option and carries a GPL-2.0/commercial split whose licence consequences
  belong with `yocto-openembedded-development`'s licence material.
- Static analysis has no upstream answer either.
- CVE monitoring, SBOM production and post-ship re-analysis belong to vulnerability management, not here.
