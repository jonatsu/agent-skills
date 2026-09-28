# Attack Surface, Credentials and Root Filesystem State

What the image contains, who can log into it, and whether its filesystem is writable. Every control here is a
build-time setting (**B**) whose effect must be read back from the image (**R**).

## Where these settings belong

A production posture belongs in a **distro configuration**, not `local.conf`. `local.conf` is a developer's
file: it is not part of the release artefact, it is not reviewed with the layer, and it is parsed before the
machine and distro configs, so a `VAR += …` there loses to a later hard assignment. Placement mechanics are
`yocto-openembedded-development`'s subject; the security consequence is that **a control in `local.conf` is a
control you cannot prove shipped.**

## Feature reduction

```bash
bitbake-getvar DISTRO_FEATURES     # every assignment site and the final value
bitbake-getvar IMAGE_FEATURES
bitbake-getvar MACHINE_FEATURES
```

`DISTRO_FEATURES:remove` in the production distro conf is the blunt instrument — dropping `alsa`, `bluetooth`,
`nfs`, `wifi`, `x11` and similar removes both the daemons and, for many recipes, the code paths compiled in.
Two cautions:

- **Removing a feature does not remove the capability.** A recipe that hard-`RDEPENDS` on a component still
  pulls it; a kernel that still has the driver still has the attack surface. Confirm against the manifest and
  the kernel config, not the feature list.
- **`DISTRO_FEATURES` interacts with hardening in both directions.** `xattr` looks like surface to remove, and
  SELinux, IMA/EVM and any `security.*` labelling need it. Decide against the mechanisms you intend to run.

`IMAGE_FEATURES` alters image assembly *and* how some recipes build; it is not purely an assembly knob.

**Release gate.** An unrecognised `IMAGE_FEATURES` item raises `bb.parse.SkipRecipe`, so BitBake reports that
**nothing provides the image** rather than naming the bad feature at the top of the error. The skip message
does list every valid item, and distinguishes `EXTRA_IMAGE_FEATURES` from `IMAGE_FEATURES`. `validitems` at
scarthgap:

```text
debug-tweaks read-only-rootfs read-only-rootfs-delayed-postinsts stateless-rootfs empty-root-password
allow-empty-password allow-root-login serial-autologin-root post-install-logging overlayfs-etc
```

On master the list is identical **minus `debug-tweaks`**, which was removed at 5.2 Walnascar. It gated exactly
four postcommands, each of which survives as its own feature:

| Removed umbrella | Surviving feature      | Postcommand it drives                |
| ---------------- | ---------------------- | ------------------------------------ |
| `debug-tweaks`   | `empty-root-password`  | suppresses `zap_empty_root_password` |
| `debug-tweaks`   | `allow-empty-password` | `ssh_allow_empty_password`           |
| `debug-tweaks`   | `allow-root-login`     | `ssh_allow_root_login`               |
| `debug-tweaks`   | `post-install-logging` | `postinst_enable_logging`            |

The split is a security improvement: postinst logging no longer costs you a passwordless root login. Upgrading
a 5.0 configuration to 5.2 or later means naming the ones you actually wanted.

## Package removal

`IMAGE_INSTALL:remove` is a metadata edit and misses transitively pulled packages; `PACKAGE_EXCLUDE` and
`BAD_RECOMMENDATIONS` act at install time, after dependency resolution. Mechanism and verification are in
`misleading-controls.md` §6.

Practical order: prefer not pulling the package (a narrower packagegroup, a `PACKAGECONFIG` that omits the
feature) over excluding it. An exclusion that collides with a hard `RDEPENDS` is a build failure you then have
to solve anyway, and an image built by excluding half a packagegroup is hard to review.

**The manifest is the only authority on what shipped:**

```bash
tmp/deploy/images/<machine>/<image>-<machine>.rootfs.manifest   # package name, arch, version per line
oe-pkgdata-util find-path /usr/bin/foo                          # which package ships a path
```

## Credentials

- **`EXTRA_USERS_PARAMS` sets identical credentials on every device.** One extracted image compromises the
  fleet. Treat a baked-in password as a development convenience with a removal date, and generate per-device
  credentials at provisioning time or at first boot.
- **`extrausers.bbclass` accepts seven commands** — `useradd`, `groupadd`, `userdel`, `groupdel`, `usermod`,
  `groupmod`, and **`passwd-expire`**; anything else is `bbfatal "Invalid command in EXTRA_USERS_PARAMS"`.
  `passwd-expire` is present on the scarthgap branch, so a first-login password change does not need a
  hand-rolled `passwd -e` and a first-boot unit. Secondary sources describing it as 6.0-only are describing an
  earlier 5.0 point release; check the branch you have.
- **A password expiry needs somewhere to write.** On a read-only rootfs, `/etc/shadow` must be writable
  (`overlayfs-etc`, or a bind-mounted `/etc`) or the first-login change fails.
- The class hooks `PACKAGE_INSTALL:append` to add `base-passwd shadow` only when `EXTRA_USERS_PARAMS` is
  non-empty, so an image with no users configured does not carry the tools.

**Verify on the rootfs:**

```sh
grep -E '^(root|[a-z]+):' etc/shadow   # locked (*/!), empty (::), or a hash — for every account, not just root
awk -F: '$3 == 0 {print}' etc/passwd   # every uid-0 account, not only "root"
grep -E '^(PermitRootLogin|PermitEmptyPasswords)' etc/ssh/sshd_config etc/ssh/sshd_config_readonly
grep DROPBEAR_EXTRA_ARGS etc/default/dropbear   # -B permits empty passwords; -w disallows root
```

`ssh_allow_empty_password` does more than edit `sshd_config`: it adds `-B` to dropbear's arguments **and**
rewrites `nullok_secure` to `nullok` across `/etc/pam.d/*`. Reverting the feature reverts all three; auditing
only `sshd_config` does not.

## Read-only rootfs and `/etc` overlays

`IMAGE_FEATURES += "read-only-rootfs"` is cheap to enable and easy to over-trust — see
`misleading-controls.md` §3 and §4 for the mechanism, the fstab pattern it matches and the delayed-postinsts
trap.

Configuration that actually holds needs three parts:

1. **The image side** — the feature, plus every writable path moved to a tmpfs or a data partition. Mount
   points for read-write partitions must exist at rootfs-creation time; the rootfs is read-only when the
   system tries to create them.
2. **The boot side** — the kernel command line must not carry `rw`. This is bootloader configuration; route to
   `u-boot-development`.
3. **The state side** — `overlayfs-etc` (an `/etc` overlay backed by a writable device) or `stateless-rootfs`
   (regenerate on every boot, keep nothing). They are different products, not two spellings of one: the
   overlay persists an operator's changes and therefore persists an attacker's, and the stateless image
   discards both.

```bash
bitbake-getvar -r <image> OVERLAYFS_ETC_MOUNT_POINT   # plus _DEVICE, _FSTYPE, _MOUNT_OPTIONS
```

**Verify on a booted first-boot image:**

```sh
findmnt -no OPTIONS /
findmnt /etc                     # overlay, and backed by which device
touch /test-write && echo BAD
grep ' / ' /proc/mounts
cat /proc/cmdline                # a stray rw here beats everything the image did
```

## Service privilege reduction

OE-Core packages upstream defaults, and upstream defaults are not hardened for a product. Public-facing
services are the ones to check by hand; `lighttpd` in OE-Core has shipped running as root, which is the
example worth carrying because it is not an obscure recipe.

The Yocto-shaped work is:

- a `.bbappend` adding a `useradd`/`usermod` via `useradd.bbclass` so the daemon has a non-root account;
- a systemd drop-in packaged by that append, or `SYSTEMD_AUTO_ENABLE` set so an unneeded unit does not start;
- `PACKAGECONFIG` narrowing what the daemon can do at all.

Which systemd directives to set — `ProtectSystem=`, `NoNewPrivileges=`, `PrivateTmp=`, `CapabilityBoundingSet=` —
is general Linux and is not this skill's subject. State the directive, cite `systemd-analyze security <unit>`
as the check, and do not turn this file into a systemd tutorial.

**Verify on target:**

```sh
ps -eo user,pid,comm --sort=user     # who is running as root that need not be
systemd-analyze security             # per-unit exposure, worst first
ss -tulpn                            # what is listening, and as whom
```
