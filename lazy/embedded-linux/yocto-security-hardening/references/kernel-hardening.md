# Kernel Hardening Through the Build

The kernel is where a hardening setting is most likely to be silently discarded: a fragment that asks for a
symbol the kernel cannot honour produces a **warning**, and by default not even all of those are shown.

## Getting a symbol in

Two mechanisms, and they are not interchangeable:

- **`.cfg` fragments through `SRC_URI`** in a `linux-*.bbappend` — works with any kernel recipe, including a
  vendor one:

  ```bitbake
  FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"
  SRC_URI += "file://hardening.cfg"
  ```

  ```text
  # hardening.cfg
  CONFIG_FORTIFY_SOURCE=y
  CONFIG_STACKPROTECTOR_STRONG=y
  CONFIG_STRICT_KERNEL_RWX=y
  CONFIG_STRICT_MODULE_RWX=y
  CONFIG_HARDENED_USERCOPY=y
  CONFIG_RANDOMIZE_BASE=y
  ```

  **The spacing rule bites here:** a symbol you want off must be written exactly as the kernel writes it,
  `# CONFIG_FOO is not set`. `CONFIG_FOO=n` in a fragment is not the same thing and does not always take.

- **`KERNEL_FEATURES` `.scc` features** — only for `linux-yocto`-derived recipes using the kernel-yocto
  tooling. A vendor kernel that inherits plain `kernel.bbclass` has no `.scc` machinery, and neither does it
  get the configuration audit below.

Which symbols to set is general kernel-hardening knowledge, and it moves: refresh from the kernel's own
`Documentation/security/self-protection.rst` and the Kernel Self Protection Project for the reader's kernel
version before recommending a list.

## The audit is on, quiet, and non-fatal by default

`kernel-yocto.bbclass` at scarthgap:

```bitbake
KCONF_AUDIT_LEVEL ?= "1"
KCONF_BSP_AUDIT_LEVEL ?= "0"
KMETA_AUDIT ?= "yes"
KMETA_AUDIT_WERROR ?= ""
```

`do_kernel_configcheck` runs after `do_configure` and compares what the fragments asked for against the
kernel's final `.config`. Three things follow, and all three are counter-intuitive:

1. **At the default level 1, the check passes `--classify`**, which "streamline[s] the output to only report
   options that could be boot issues, or are otherwise required for proper operation." A dropped *hardening*
   symbol is not a boot issue. **Set `KCONF_AUDIT_LEVEL = "2"` to see the full mismatch list.**

2. **BSP-fragment auditing is off** (`KCONF_BSP_AUDIT_LEVEL ?= "0"`), so invalid elements in a BSP's own
   fragments are not reported at all until you raise it.

3. **Findings are `bb.warn`, not failures**, unless `KMETA_AUDIT_WERROR` is set. In a CI log with thousands of
   lines, a warning is an absence of evidence. Set it:

   ```bitbake
   KCONF_AUDIT_LEVEL = "2"
   KMETA_AUDIT_WERROR = "1"
   ```

The analysis is also written to files under the kernel's meta directory — `cfg/mismatch.txt`,
`cfg/invalid.txt`, `cfg/redefinition.txt` — which is what to read when the warning is truncated.

**The verification that does not depend on any of this** is to read the built configuration:

```bash
bitbake -e virtual/kernel | grep '^B='          # find the kernel build directory
grep -E 'FORTIFY_SOURCE|STACKPROTECTOR|RANDOMIZE_BASE|HARDENED_USERCOPY' <B>/.config
```

and on target, `zcat /proc/config.gz` when `CONFIG_IKCONFIG_PROC=y` — which is itself a small disclosure and a
deliberate choice for a production image.

## `kernel-hardening-checker`

Packaged in `meta-openembedded`, at `meta-oe/recipes-security/kernel-hardening-checker`. It reports which
config symbols and command-line settings could be tightened, against curated recommendation sets.

**Check the branch, not the release number.** At the time of writing, `scarthgap` carries **0.6.17.1** and
`walnascar` carries **0.6.10** — the LTS branch is ahead of a later release branch, because the newer version
was backported there. Secondary sources describing it as "Walnascar and later" understate what the LTS has.

Install it into a **prod-test image, not production** — it is an analysis tool, and shipping it hands an
attacker your own gap list:

```bitbake
IMAGE_INSTALL:append = " kernel-hardening-checker"
```

It also runs host-side against a `.config` file, which is the form that belongs in CI.

## Kernel configuration minimisation

Removing unused subsystems cuts attack surface and boot time together. Yocto helps in one specific way:
because modules are packaged individually, **the module packages in the image manifest are a readable
inventory of the drivers you shipped**, which a monolithic `.config` review is not.

```bash
grep '^kernel-module-' tmp/deploy/images/<machine>/<image>-<machine>.rootfs.manifest
```

A module in that list that no hardware needs is a candidate for removal — and removing it is a config change,
not a package exclusion, or the driver stays built into the kernel.

## `meta-security` and the `security` `DISTRO_FEATURE`

The feature enables nothing by itself; it gates four further conditions (`apparmor`, `smack`, `lkrg`,
`dm-verity-img`). Mechanism and verification: `misleading-controls.md` §5. Layer inventory and release
compatibility: `meta-security-layer-map.md`.

The dm-verity kernel fragment is enabled by `IMAGE_CLASSES` containing `dm-verity-img`, not by a
`DISTRO_FEATURE` — see `chain-of-trust-wiring.md`.

## MAC layers

AppArmor and SMACK come from `meta-security` (`recipes-mac`), SELinux from `meta-selinux`, and all three need
`xattr` in `DISTRO_FEATURES` plus matching kernel symbols and a policy that fits the product.

**This skill does not yet cover MAC policy authoring**: the material to do it properly is not in hand, and a
half-sourced policy recommendation is worse than a routing note. State the packaging, name the gap, and do not
generate a policy from general knowledge without saying that is what you are doing.
