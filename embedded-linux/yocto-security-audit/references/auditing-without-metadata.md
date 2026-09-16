# Auditing an Artefact You Did Not Build

The starting state that defines this skill: an image, a rootfs tarball, maybe a `.wic`, and no build tree. Every
first move the sibling skills teach — `bitbake-getvar`, `bitbake -e`, reading the recipe — is unavailable.

The good news is that a Yocto deploy directory carries far more evidence than people expect, and most audits
that "need the build" do not.

## Establish provenance before anything else

⛔ **An audit of the wrong artefact is worse than no audit**, because it produces confident reassurance about
something that does not ship. Answer these four before running a single check:

| Question                    | Where the answer is                                                 |
| --------------------------- | ------------------------------------------------------------------- |
| Which release?              | `DISTRO_VERSION` in `testdata.json`; failing that, package versions |
| Which recipe built it?      | **`PN` in `testdata.json` — not the filename.** See the trap below  |
| What is actually installed? | the `.manifest` beside the image                                    |
| Is this what ships?         | ask. Nothing in the artefact answers it                             |

That last one has no technical answer and is the one that matters most. Prod, dev and prod-test images look
alike and differ in exactly the ways an audit cares about; hardening's `verification-workflows.md` describes
the three-image pattern. **Always report which image a result came from.**

### The filename does not identify the recipe

Measured on `meta-security` at `scarthgap`: building `security-test-image` deploys artefacts named
`security-build-image-*`, because `security-build-image.bb` contains
`export IMAGE_BASENAME = "security-build-image"` and the test image `require`s it. Two image recipes write the
same filenames, and the second silently overwrites the first.

```bash
jq -r '.PN, .IMAGE_BASENAME' <image>.testdata.json
# security-test-image      <- the recipe that built it
# security-build-image     <- what the files are called
```

This is not a corner case someone contrived; it is upstream's own security layer. **Read `PN`, never the
filename.**

## `testdata.json` is the audit's best friend

Deployed beside every image, and it is a **complete dump of the build datastore** — 2221 variables in the image
measured here. If it is present, "no metadata" is largely untrue:

```bash
T=<image>-<machine>.rootfs.testdata.json

jq -r '.DISTRO, .DISTRO_VERSION' "$T"              # release, exactly
jq -r '.DISTRO_FEATURES' "$T"                      # LSMs, pam, seccomp, tpm…
jq -r '.IMAGE_FEATURES' "$T"                       # debug-tweaks and friends
jq -r '.ROOTFS_POSTPROCESS_COMMAND' "$T"           # every credential and rootfs tweak, expanded
jq -r '.PN, .IMAGE_BASENAME' "$T"                  # provenance
jq -r 'keys[] | select(startswith("SECURITY_"))' "$T"   # what hardening flags were in scope
```

`ROOTFS_POSTPROCESS_COMMAND` is the highest-value single line: it names, in expanded form, every credential and
filesystem tweak the image applied. Read the **absence** of `zap_empty_root_password` as a finding, not its
presence — it runs when `empty-root-password` is *not* set.

**But `testdata.json` is still configuration, not the artefact.** It tells you what the build intended. The
Iron Law applies to it exactly as it applies to a recipe: confirm the property on the rootfs.

### When it is absent

It ships as part of the deploy directory, so a customer handed only an image file will not have it. Then you
are down to the artefact itself, and the table below is what remains.

## What the artefact alone still tells you

| Question                           | How, with no build tree                                                                     |
| ---------------------------------- | ------------------------------------------------------------------------------------------- |
| What is installed, at what version | the `.manifest`; failing that, `/var/lib/opkg/status`, `/var/lib/dpkg/status` or the rpm db |
| Release, approximately             | `/etc/os-release`, and the versions of `bash`, `glibc`, `busybox` against release history   |
| Root credentials                   | `/etc/shadow`, `/etc/passwd`                                                                |
| What starts at boot                | `/etc/systemd/system/`, `/lib/systemd/system/*.wants/`, or `/etc/init.d` and `rc*.d`        |
| Service exposure                   | unit files' `ExecStart`, `User=`, and any config the daemon reads                           |
| Binary hardening                   | `checksec --dir=` over the unpacked tree                                                    |
| Kernel configuration               | `/proc/config.gz` on target, or the shipped `.config`/`bzImage` if deployed                 |
| MAC policy present                 | `/etc/apparmor.d/`, `/etc/selinux/`, `/etc/smack/`                                          |
| SBOM, if generated                 | `.spdx.tar.zst` at 5.0, `.spdx.json` at 6.0 — route to **yocto-vulnerability-management**   |

Unpacking without root is the usual practical obstacle. A `.tar.bz2` rootfs needs nothing special:

```bash
mkdir rootfs && tar -xjf <image>.rootfs.tar.bz2 -C rootfs ./etc/shadow ./etc/ssh/sshd_config
```

An `.ext4` needs a loop mount and therefore privilege, or a userspace reader such as `debugfs -R`. A `.wic` is
a partition image: `wic ls` if you have the tooling, otherwise offsets from the `.wks` or a partition table
read.

## What is simply unknowable from the artefact

Say these plainly rather than inferring them:

- **Which layers and revisions produced it**, unless `testdata.json` or an SBOM is present. Package versions
  narrow the release; they do not identify a layer set or local patches.
- **Whether a binary's hardening reflects policy or accident.** `checksec` shows the result, not the intent.
- **Whether the configuration on disk is what runs.** Kernel command line, initramfs and runtime overlays can
  all override it — `read-only-rootfs` edits `/etc/fstab`, but the kernel command line decides.
- **Whether this is the image that ships.** Ask.

## Worked example — auditing upstream's own security image

Run against `meta-security`'s `security-test-image` at `scarthgap`, 2026-09-08. Configuration first:

```bash
jq -r '.IMAGE_FEATURES, .ROOTFS_POSTPROCESS_COMMAND' <image>.testdata.json
# debug-tweaks ssh-server-openssh
#   ssh_allow_empty_password  ssh_allow_root_login  postinst_enable_logging …
```

Then the artefact, because configuration is a claim:

```bash
grep '^root:' rootfs/etc/shadow
# root::15069:0:99999:7:::

grep -iE '^\s*(PermitRootLogin|PermitEmptyPasswords)' rootfs/etc/ssh/sshd_config
# PermitRootLogin yes
# PermitEmptyPasswords yes
```

**An empty root password, root SSH login and empty SSH passwords, in an image whose name is
`security-test-image`.** Three findings, confirmed on the artefact rather than inferred from `debug-tweaks`.

And then the judgement that makes it an audit rather than a scan: **this is fine.** It is a test image whose
whole purpose is to let a harness ssh in and run cases. The finding is real, the severity is nil *for this
artefact's purpose*, and it would be critical if the same image shipped.

That is the shape of every audit finding — see `gating-and-reporting.md`. A finding is a fact about an
artefact; severity is a judgement about intent, and you usually have to ask for the intent.
