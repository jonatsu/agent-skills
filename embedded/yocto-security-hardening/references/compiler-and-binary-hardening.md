# Compiler Hardening, and Proving It Reached the Binaries

The distro flag is the claim. `checksec` over the shipped binaries is the evidence. **The exemption list in
`security_flags.inc` is the reason those two differ**, and it is the strongest worked example of this skill's
Iron Law.

## What `security_flags.inc` sets

`meta/conf/distro/include/security_flags.inc`, read at scarthgap — 71 lines, of which **21 are `:pn-`
opt-outs**.

| Variable                   | Value                                                  |
| -------------------------- | ------------------------------------------------------ |
| `SECURITY_STACK_PROTECTOR` | `-fstack-protector-strong`                             |
| `SECURITY_STRINGFORMAT`    | `-Wformat -Wformat-security -Werror=format-security`   |
| `SECURITY_LDFLAGS`         | `-Wl,-z,relro,-z,now` — full RELRO plus BIND_NOW       |
| `SECURITY_X_LDFLAGS`       | `-Wl,-z,relro` — **partial RELRO only**                |
| `GCCPIE`                   | `--enable-default-pie`                                 |
| `SECURITY_PIE_CFLAGS`      | `-pie -fPIE`, injected **only when `GCCPIE` is empty** |
| `SECURITY_NOPIE_CFLAGS`    | `-no-pie -fno-PIE`, used by the opt-outs               |
| `lcl_maybe_fortify`        | `${OPTLEVEL} -D_FORTIFY_SOURCE=2`                      |

Applied through `TARGET_CC_ARCH:append:class-target`, `TARGET_LDFLAGS:append:class-target` and the
`class-cross-canadian` equivalents — so the flags land on target builds, and SDK/native builds are a separate
question.

The file states its own limits: *"these don't work universally, there are recipes which can't use one, the
other or both … The idea would be over time to reduce this list to nothing."* Believe it.

## The exemptions, by name

| Exempted recipe                                  | What it loses                                       |
| ------------------------------------------------ | --------------------------------------------------- |
| `glibc`, `glibc-testsuite`, `gcc-runtime`        | all `SECURITY_CFLAGS`                               |
| **`grub`, `grub-efi`**, `mkelfimage` (x86)       | all `SECURITY_CFLAGS`                               |
| `libgcc` (powerpc)                               | all `SECURITY_CFLAGS`                               |
| `valgrind`, `sysklogd`                           | PIE (`NOPIE` substitute) and all `SECURITY_LDFLAGS` |
| **`busybox`**, `gcc`                             | `SECURITY_STRINGFORMAT`                             |
| `glibc`, `glibc-testsuite`, `gcc-runtime`, `ltp` | `SECURITY_STACK_PROTECTOR`                          |
| `xserver-xorg`                                   | full RELRO → **partial**                            |
| everything on powerpc                            | PIE                                                 |

So on a typical embedded image, **the primary userspace (`busybox`) builds without
`-Werror=format-security`, and the bootloader (`grub`) builds with no security CFLAGS at all.** "I enabled
`security_flags.inc`, hardening is on" is wrong about specific, nameable, security-relevant binaries.

**`_FORTIFY_SOURCE` vanishes silently at `-O0`.** `OPTLEVEL` is filtered out of `SELECTED_OPTIMIZATION`, and
`lcl_maybe_fortify` is `oe.utils.conditional('OPTLEVEL','-O0','', …)` — a debug-optimised build loses
fortification with no diagnostic, because the flag would otherwise emit a compiler warning.

## `rust_security_flags.inc` is an exemption file, not a second hardening set

Read it before repeating the common instruction to `require` both files "to enable hardening":

```bitbake
SECURITY_CFLAGS:pn-rust-native   = "${SECURITY_NO_PIE_CFLAGS}"
SECURITY_CFLAGS:pn-rust-cross-${TARGET_ARCH} = "${SECURITY_NO_PIE_CFLAGS}"
SECURITY_CFLAGS:pn-rust          = "${SECURITY_NO_PIE_CFLAGS}"
SECURITY_CFLAGS:pn-rust-llvm     = "${SECURITY_NO_PIE_CFLAGS}"
SECURITY_LDFLAGS:pn-rust-cross-arm = " -lssp_nonshared -lssp"
```

Its entire content **removes** PIE from the Rust toolchain recipes because they fail to build with it. It adds
no hardening. Requiring it is still correct — without it those recipes break — but it is not a second set of
protections, and it says nothing about hardening in Rust *code*, which comes from the Rust compiler's own
defaults.

## Release delta: 5.0 opt-in, 6.0 on by default

- **Scarthgap.** `meta/conf/distro/defaultsetup.conf` does **not** require `security_flags.inc`. Hardening is
  opt-in: `require conf/distro/include/security_flags.inc` in your distro conf.
- **master (→6.0).** `defaultsetup.conf` requires `security_flags.inc` (and `no-static-libs.inc`), and
  `bitbake.conf` includes `conf/distro/defaultsetup.conf` for **every** build after the distro conf — so the
  flags apply whatever `DISTRO` is set to, unless a distro conf hard-assigns the `SECURITY_*` variables
  itself. Descriptions of this as a `nodistro`-only default do not match the include chain; read
  `defaultsetup.conf` and `bitbake.conf` at your ref rather than trusting either claim.

The exemption count is 21 on both refs, so the upgrade changes *whether* you get the flags, not *which*
recipes are excluded.

## The baseline is behind a mainstream distro

`lcl_maybe_fortify` writes `-D_FORTIFY_SOURCE=2`. Fedora moved its distribution build flags to
**`-D_FORTIFY_SOURCE=3`** in Fedora 38, and other distributions have followed. So an OE image built with
`security_flags.inc` is not at parity with a current desktop or server distribution, and a customer's security
questionnaire that asks for "level 3 fortification" is asking for something the include does not provide.

Raising it is a one-line distro-conf override, but it is a change to test rather than to assume:

```bitbake
lcl_maybe_fortify = "${@oe.utils.conditional('OPTLEVEL','-O0','','${OPTLEVEL} -D_FORTIFY_SOURCE=3',d)}"
```

`_FORTIFY_SOURCE=3` needs a compiler that supports it and produces build failures in code the weaker level
tolerated, so expect to fix or exempt recipes — which is the same maintenance burden the 21 existing opt-outs
represent.

**Worth checking against whatever distribution you are being compared to**, and not asserted here: several
distributions also enable stack-clash protection and control-flow protection by default. Neither appears
anywhere in `security_flags.inc`. Read your reference distribution's own build-flags documentation before
quoting a gap.

## Verify per binary, host-side

Upstream packages the tool. `meta-security` ships `checksec` 2.6.0 from `slimm609/checksec.sh` at a pinned
`SRCREV`, with `BBCLASSEXTEND = "native"` — so a host-side scan is *meant* to need no target.

⛔ **`checksec-native` does not build at `scarthgap`.** Measured 2026-09-08 by building the layer with its own
`kas/qemux86-64.yml`: the recipe sets `BBCLASSEXTEND = "native"` but leaves `RDEPENDS:${PN}` carrying `procps`,
which has no native variant in OE-Core, so BitBake refuses the target:

```text
ERROR: Nothing RPROVIDES 'procps-native' (but …/checksec_2.6.0.bb RDEPENDS on or otherwise requires it)
```

The target `checksec` builds and packages cleanly; only the native variant is affected. A one-line `.bbappend`
restores the host-side lane, mirroring what the layer's own `buck-security` recipe already does — **verified by
building it**:

```bitbake
# checksec_%.bbappend
RDEPENDS:${PN}:class-native = "bash openssl-bin binutils findutils file"
```

```bash
bitbake checksec-native                       # works with the bbappend above
checksec --dir=tmp/work/<arch>/<recipe>/…/image/usr/bin
checksec --file=tmp/deploy/images/<machine>/…/usr/bin/busybox
```

Without the bbappend, the host-side lane needs another route: run the `checksec` shell script straight from the
recipe's source checkout, or install the target package into a prod-test image and scan on target.

What to read in the output, mapped back to the flags above:

| Column       | Set by                         | Expect                                             |
| ------------ | ------------------------------ | -------------------------------------------------- |
| RELRO        | `SECURITY_LDFLAGS`             | Full; **Partial** on `xserver-xorg` by design      |
| STACK CANARY | `SECURITY_STACK_PROTECTOR`     | Canary found; absent on the exempted recipes       |
| PIE          | `GCCPIE`/`SECURITY_PIE_CFLAGS` | PIE enabled; absent on powerpc                     |
| FORTIFY      | `lcl_maybe_fortify`            | present — **absent means `-O0`, not "no support"** |

**A per-binary result that matches the exemption table is a pass, not a finding.** Compare against the list
above before reporting; the useful finding is a binary that is *not* exempted and *not* hardened.

## The QA checks you already have

`insane.bbclass` runs these at `do_package_qa`. Their severity matters, because a warning does not stop a
release:

| Check                      | Default class  | What it catches                                                     |
| -------------------------- | -------------- | ------------------------------------------------------------------- |
| `ldflags`                  | **`ERROR_QA`** | the recipe dropped `LDFLAGS`, so RELRO/BIND_NOW never applied       |
| `already-stripped`         | **`ERROR_QA`** | the recipe stripped its own binaries, defeating debug packaging     |
| `rpaths`, `useless-rpaths` | **`ERROR_QA`** | build-host paths or redundant search paths burned into ELF headers  |
| `installed-vs-shipped`     | **`ERROR_QA`** | files built and packaged nowhere — they vanish from the image       |
| `textrel`                  | `WARN_QA`      | text relocations — a warning only; promote it if you care           |
| `buildpaths`               | `WARN_QA`      | host paths leaking into the artefact; also a reproducibility signal |

Promote a check by moving it: `ERROR_QA:append = " textrel buildpaths"` in the distro conf. **Never clear a
failure with `INSANE_SKIP` before the named paths are explained** — silencing `installed-vs-shipped` does not
package anything.

## What this file does not cover

Kernel-side hardening symbols are `kernel-hardening.md`. ELF inspection as a *general* Linux practice, and
tools that are not Yocto-integrated, are out of scope for a Yocto skill — the shape to keep here is "which
build setting produced this property, and which recipe is exempt from it".
