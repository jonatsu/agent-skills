# Controls Whose Names Misdescribe Their Effect

Eight settings whose names imply a security property while the mechanism permits, defers, hides or excludes.
Each entry states the mechanism, the second-order trap, and the observation that settles it on the artefact.

Every mechanism below was read from upstream source at a named ref. Where a release changes the mechanism, the
delta is named inline. **Re-read the class at the reader's ref before quoting a line number**; the reasoning
survives a refactor, the line does not.

## 1. `empty-root-password` permits, it does not clear

`rootfs-postcommands.bbclass`, scarthgap:

```bitbake
ROOTFS_POSTPROCESS_COMMAND += '${@bb.utils.contains_any("IMAGE_FEATURES",
    [ 'debug-tweaks', 'empty-root-password' ], "", "zap_empty_root_password ", d)}'
```

The postcommand runs when the feature is **absent**. Adding the feature suppresses the step that would lock a
passwordless root account. On master the `debug-tweaks` half of the condition is gone and the test is a plain
`bb.utils.contains`, but the inversion is unchanged.

**Second-order trap.** `zap_empty_root_password` runs `sed 's%^root::%root:*:%'` over `/etc/shadow` and
`/etc/passwd`. A root account carrying a real hash — from a vendor layer, an `EXTRA_USERS_PARAMS` line, or a
postinst — passes untouched. **The feature's absence therefore does not mean root is secure**, only that root
has no *empty* password.

Master adds `add_empty_root_password_note`, which appends a line to `/etc/issue` when root's hash field is
empty. It is a banner, not a control, and its presence is a useful smell when reading someone else's image.

**Verify on the rootfs, never on `IMAGE_FEATURES`:**

```sh
grep '^root:' etc/shadow    # root:*: or root:!: is locked; root:: is passwordless;
                            # root:$y$... ships a real hash from somewhere — find out where
```

## 2. `serial-autologin-root` does nothing on its own

Same class, and the gate is `bb.utils.contains` over a **list**, which requires *every* listed feature:

```bitbake
ROOTFS_POSTPROCESS_COMMAND += '${@bb.utils.contains("IMAGE_FEATURES",
    [ 'empty-root-password', 'serial-autologin-root' ], "serial_autologin_root ", "", d)}'
```

So `serial-autologin-root` alone is inert, and the pair is what patches `--autologin root` into
`serial-getty@.service` (systemd) or `start_getty` (sysvinit). Read this in both directions: a reviewer who
sees only `serial-autologin-root` in a config has not found an autologin, and one who sees only
`empty-root-password` has not ruled one out.

`bb.utils.contains` requires all values; `bb.utils.contains_any` requires one. That distinction decides the
meaning of most feature gates in this class — check which one a gate uses before reading it.

## 3. `read-only-rootfs-delayed-postinsts` disables a safety check

`meta/lib/oe/rootfs.py`, scarthgap:

```python
if bb.utils.contains("IMAGE_FEATURES", "read-only-rootfs", True, False, self.d) and \
   not bb.utils.contains("IMAGE_FEATURES", "read-only-rootfs-delayed-postinsts", True, False, self.d):
    delayed_postinsts = self._get_delayed_postinsts()
    if delayed_postinsts is not None:
        bb.fatal("The following packages could not be configured offline and rootfs is read-only: %s" % ...)
```

With `read-only-rootfs` alone, a package that cannot be configured offline **fails the build**. Adding the
delayed-postinsts feature removes that check and defers those postinsts to first boot — which needs a writable
rootfs at first boot, on a product that claims to be read-only.

**Verify a fresh first boot, not a second boot:** an image whose deferred postinsts already ran looks clean
afterwards.

```sh
findmnt -no OPTIONS /            # expect ro
touch /test-write                # must fail
journalctl -b | grep -i postinst # nothing deferred should be running
```

## 4. `read-only-rootfs` edits configuration; the kernel decides the mount

`read_only_rootfs_hook` does four things: rewrites the `/etc/fstab` line **matching `/dev/root`** to `ro`,
flips busybox `inittab`'s `remount,rw /` to `remount,ro /`, sets `ROOTFS_READ_ONLY=yes` in `/etc/default/rcS`
under sysvinit, and relocates ssh host keys to `/var/run/ssh` when none are pre-generated. It creates
`/etc/machine-id` under systemd.

Two consequences the name hides:

- **A BSP fstab naming a real device** (`/dev/mmcblk0p2 / ext4 defaults …`) does not match the `/dev/root`
  pattern and is left writable. The feature ran; the property does not hold.
- **The kernel command line wins.** `rootflags=rw`, or a bootloader that appends `rw`, mounts the rootfs
  writable regardless of anything the image did. That half belongs to `u-boot-development`.

Under `overlayfs-etc` the ssh-key relocation is deliberately skipped, because `/etc` is writable again —
`stateless-rootfs` re-enables it. So `read-only-rootfs` plus `overlayfs-etc` is a *different* configuration
from `read-only-rootfs` alone, not a strictly stronger one.

## 5. The `security` `DISTRO_FEATURE` is a gate that enables other gates

`meta-security` at scarthgap. `recipes-kernel/linux/linux-yocto_%.bbappend` is one line:

```bitbake
require ${@bb.utils.contains('DISTRO_FEATURES', 'security', '${BPN}_security.inc', '', d)}
```

and `linux-yocto_security.inc` is four lines, each conditional on a *further* feature — `apparmor`, `smack`,
`lkrg` in `DISTRO_FEATURES`, and `dm-verity-img` in `IMAGE_CLASSES`. **`security` on its own adds no kernel
configuration at all.** Note that the verity fragment keys on `IMAGE_CLASSES`, a different mechanism from the
other three, and that eCryptfs is not in this file at scarthgap despite appearing in secondary summaries.

The layer warns at parse time when it is included without the feature, and that warning is silenceable with
`SKIP_META_SECURITY_SANITY_CHECK = 1` — which is how the misreading survives.

```bash
bitbake-getvar -r linux-yocto KERNEL_FEATURES   # every assignment site plus the final value
bitbake-getvar DISTRO_FEATURES                  # is apparmor/smack/lkrg actually present?
bitbake-getvar IMAGE_CLASSES                    # dm-verity-img is the verity trigger
```

`KERNEL_FEATURES` gaining nothing after enabling `security` is the expected result, not a bug.

## 6. `IMAGE_INSTALL:remove` edits metadata; `PACKAGE_EXCLUDE` edits the install

`IMAGE_INSTALL:remove` removes a name from a **list**. A package pulled in transitively — through a
packagegroup's `RDEPENDS`, or another package's — was never in `IMAGE_INSTALL`, so removing it there is a
no-op against the thing you are trying to drop.

`PACKAGE_EXCLUDE` is enforced by the package manager after dependency resolution.
`meta/lib/oe/package_manager/ipk/__init__.py`:

```python
for exclude in (self.d.getVar("PACKAGE_EXCLUDE") or "").split():
    cmd += " --add-exclude %s" % exclude
for bad_recommendation in (self.d.getVar("BAD_RECOMMENDATIONS") or "").split():
    cmd += " --add-ignore-recommends %s" % bad_recommendation
```

with equivalents for rpm and deb. `BAD_RECOMMENDATIONS` sits at the same layer for the weaker `Recommends`
relationship. **Not verified:** the behaviour when an excluded package is a hard dependency of something else
in the image. Expect a build failure rather than a silent drop, and confirm before asserting it.

**Verify against the manifest**, not the variable — `bitbake-getvar -r <image> IMAGE_INSTALL` returns
packagegroups, not the resolved set:

```bash
grep -c '^<pkg> ' tmp/deploy/images/<machine>/<image>-<machine>.rootfs.manifest
```

## 7. `BB_SIGNATURE_HANDLER` is a checksum handler, not a signer

`bitbake/lib/bb/siggen.py` at `yocto-5.0.12` selects a `SignatureGenerator` subclass by name, defaulting to
`noop`. The class's whole state is hashing state — `basehash`, `taskhash`, `unihash`, `runtaskdeps`,
`file_checksum_values`. A grep of all 1295 lines for `gpg|openssl|rsa|x509|hmac|verify_signature` returns
nothing. "Signature" in BitBake means *task input hash* throughout, and `OEEquivHash` is hash equivalence, not
signing.

**Second trap:** an unrecognised handler name logs an error and falls back to `noop` rather than failing, so a
typo silently disables hash equivalence.

Signing sstate is a different set of variables entirely — see `build-and-supply-chain-trust.md`.

## 8. `CONFIG_FIT_SIGNATURE` enables verification; it does not require it

U-Boot `boot/Kconfig` at `v2025.10`. `FIT_SIGNATURE` gives U-Boot the capability to verify a FIT; making a
signature **mandatory** is the `required` property in the key node, which `mkimage -r` writes into U-Boot's
control dtb. Its one automatic side effect is on another symbol: `LEGACY_IMAGE_FORMAT` gains
`default y if !FIT_SIGNATURE && !TI_SECURE_DEVICE`, a default a board can override, and one that says nothing
about unsigned *FIT* images.

**The Yocto side is better than the raw trap suggests, and only when it is switched on.**
`kernel-fitimage.bbclass` signs with:

```bash
${UBOOT_MKIMAGE_SIGN} -F -k "${UBOOT_SIGN_KEYDIR}" -r ${KERNEL_OUTPUT_DIR}/$2 ${UBOOT_MKIMAGE_SIGN_ARGS}
```

— `-r` is there, so OE marks the key required, but the whole block is inside
`if [ "x${UBOOT_SIGN_ENABLE}" = "x1" ]`. With `UBOOT_SIGN_ENABLE = "0"` the FIT is assembled and never signed,
and `FIT_GENERATE_KEYS = "1"` in that state only produces a warning that the keys will not be used.

Which dtb the board actually boots is U-Boot's question — route the verification mechanics to
**u-boot-development**, and see `chain-of-trust-wiring.md` for what the build owns.

## Why this list shapes the skill

Every entry has the same shape: **a setting whose name implies a property, whose mechanism permits, defers,
hides or excludes.** Hence the Iron Law, and hence a verification beside every control rather than a
configuration snippet alone.

| Verification shape          | Worked example here                                                          |
| --------------------------- | ---------------------------------------------------------------------------- |
| Inspect the built rootfs    | `grep '^root:' etc/shadow` rather than trusting `IMAGE_FEATURES`             |
| Boot the *first-boot* state | deferred postinsts are invisible on a second boot                            |
| Read the gate, not the name | `contains` needs every feature; `contains_any` needs one                     |
| Check the resolved set      | the image manifest, never `bitbake-getvar -r <image> IMAGE_INSTALL`          |
| Prove the negative case     | an unsigned FIT must fail to boot; a bad-key sstate archive must be rejected |

The last shape generalises: **a control that has never been observed failing has not been shown to work.**
