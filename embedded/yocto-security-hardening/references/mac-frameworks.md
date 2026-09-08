# Mandatory Access Control in a Yocto Image

Light by design: this file covers **choosing one, wiring it into the build, and confirming it is enforcing**.
Policy authoring is a project in its own right and is not attempted here — see *Stated limit*.

## Choose one, and do it early

| Framework    | Packaged in                     | Identifies objects by | Fits                                                   |
| ------------ | ------------------------------- | --------------------- | ------------------------------------------------------ |
| **AppArmor** | `meta-security/recipes-mac`     | **path**              | A few confined daemons on an otherwise ordinary system |
| SELinux      | `meta-selinux` (separate layer) | inode label (xattr)   | Whole-system policy, and the strictest option          |
| SMACK        | `meta-security/recipes-mac`     | label (xattr)         | Simple label schemes, historically Tizen               |

Three facts that decide the choice more often than preference does:

- **AppArmor's path-based matching is a real weakness, not a stylistic difference.** A profile names files by
  path, so a hardlink to a restricted file can fall outside the profile that was meant to cover it. It also
  has on the order of twenty access modes against SELinux's hundreds, and no MLS.
- **Label-based frameworks need `xattr` in `DISTRO_FEATURES`** and filesystem support (`CONFIG_EXT4_FS_SECURITY`
  and friends). An image that strips `xattr` for attack-surface reasons has silently ruled out SELinux, SMACK
  and IMA/EVM together — one of the few places where reducing surface disables a control.
- **Only one LSM stack is worth running**, and the effort is in the policy, not the packaging. Two half-written
  policies are worse than one finished one.

## AppArmor: the wiring

The recipe is `apparmor` (3.1.3 at scarthgap) in `meta-security/recipes-mac/AppArmor`, and it inherits
`features_check` with:

```bitbake
REQUIRED_DISTRO_FEATURES = "apparmor"
```

**Without `apparmor` in `DISTRO_FEATURES` the recipe is skipped**, and a skipped recipe surfaces as BitBake
reporting that nothing provides it — the same confusing failure shape as an invalid `IMAGE_FEATURES` entry.
So the minimum is:

```bitbake
DISTRO_FEATURES:append = " apparmor"
IMAGE_INSTALL:append = " apparmor"
```

The kernel side needs `CONFIG_SECURITY_APPARMOR=y` plus AppArmor being in the active LSM stack at boot —
`lsm=` on the kernel command line on current kernels, or `security=apparmor` / `apparmor=1` on older ones.
`meta-security`'s `linux-yocto_security.inc` adds the AppArmor kernel feature, but only when **both**
`security` and `apparmor` are in `DISTRO_FEATURES`; see `misleading-controls.md` §5 for why the `security`
feature alone changes nothing. A vendor kernel gets none of this and needs the symbol set by a fragment —
`kernel-hardening.md`.

**A gap worth knowing before you rely on unit-level confinement:** OE-Core's systemd recipe has **no
`apparmor` `PACKAGECONFIG` at all** (it has `selinux` and `smack`), and upstream systemd's `apparmor` meson
option is an auto-detected feature. So whether `AppArmorProfile=` in a unit does anything depends on whether
`libapparmor` happened to be in the sysroot when systemd was built — it is not declared by the metadata.
Check the built artefact rather than assuming either answer:

```sh
systemd --version        # look for +APPARMOR or -APPARMOR in the feature flags
```

If it comes out `-APPARMOR`, confine with profiles and `apparmor_parser` rather than through unit directives.

Profiles are ordinary packaged content: the recipe builds and installs the upstream profile set, and your own
profiles belong in the recipe that owns the daemon they confine, installed under `/etc/apparmor.d/`. Ship them
as release content, not as something applied on a running device.

## SELinux: the wiring

The layer is upstream at `git.yoctoproject.org/meta-selinux`. Four facts from its `conf/layer.conf` at
scarthgap that decide whether it drops into an existing build:

- **`LAYERDEPENDS_selinux = "core meta-python"`** — `meta-python` is a non-obvious second dependency, so
  adding `meta-selinux` alone fails the layer-dependency check.
- **`LAYERSERIES_COMPAT_selinux = "scarthgap"`** — a single release, narrower even than `meta-security`. The
  branch must match exactly.
- **`PREFERRED_PROVIDER_virtual/refpolicy ??= "refpolicy-targeted"`** — the reference policy ships in
  variants (targeted, minimum, mls, standard); which one you build is the biggest single decision, because it
  sets how much policy you inherit versus write.
- **The layer carries no root `LICENSE` or `COPYING` file** on that branch. Recipes declare their own
  licences; the layer does not. Resolve that before it becomes a product dependency.

`selinux` is a `DISTRO_FEATURE`, not an `IMAGE_FEATURES` entry — OE-Core's systemd recipe, for instance,
derives its `selinux` `PACKAGECONFIG` by filtering `DISTRO_FEATURES`. Labelling also needs `xattr` and
filesystem security support, and a relabel at image creation time.

`ni/meta-selinux` (National Instruments, 7★, pushed 2026-06) is a **maintained downstream copy**, not a fork
of record: same `selinux` collection name and priority, same `LAYERSERIES_COMPAT`, with NI's own
`nilrt/master/<codename>` branch scheme reaching back to `sumo`. Useful as a worked example of a product
distro that actually ships SELinux; **depend on the upstream layer**, per upstream-wins-by-default, and note
that its branch has no root licence file either.

## Verify that it is enforcing

Configuration says nothing here; three of the four checks below have failed silently on real images.

```sh
cat /sys/kernel/security/lsm          # is apparmor in the active stack at all?
aa-status                             # profiles loaded, and how many are in enforce vs complain mode
cat /proc/self/attr/current           # the confinement of the shell you are in
cat /proc/<pid>/attr/current          # and of the daemon you meant to confine
```

**`complain` mode is the trap.** A profile in complain mode logs and permits, so `aa-status` reporting
profiles loaded is compatible with nothing being enforced. Count the enforce-mode profiles, and check that
your daemon's PID is confined by the profile you expect rather than by `unconfined`.

Then prove the negative case: make the confined process attempt something the profile forbids and confirm it
is **denied**, with the denial visible in `dmesg` or the audit log. A policy never observed denying anything
has not been shown to work.

SELinux's equivalents are `sestatus`, `getenforce` (`Enforcing`, not `Permissive`) and `ps -eZ`; SMACK's are
under `/sys/fs/smackfs`. The same trap exists in both — permissive modes make a broken policy look installed.

## Stated limit

**This skill does not author MAC policy.** Writing an AppArmor profile or an SELinux policy module for a real
daemon needs the daemon's actual file, capability and network behaviour, and the honest workflow is to start
in complain or permissive mode, collect denials, and turn them into rules — not to generate a profile from a
model's expectations. If a policy is needed, say that this is the workflow and that the material to teach it
properly is not in this skill yet.
