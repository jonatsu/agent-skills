# U-Boot Security and Provenance

Hardening the boot chain and recording what a build actually is. Two concerns:
locking the SPL → U-Boot → kernel hand-off so only trusted images run, and
stamping every build with the facts (source revision, toolchain, defconfig, output
hashes) needed to answer "what is running on this board?" months later.

Every locking step here removes a degree of freedom from the device. Order matters:
apply the reversible controls first, prove a signed image boots, and treat one-way
fuse operations as the last and most dangerous step. This file EXTENDS the FIT
authoring and signing basics in `uboot-boot-scripts.md` — it makes the signature
*required* rather than merely present, and pushes trust down into the SPL.

## Contents

- [The Boot-Chain Hardening Checklist](#the-boot-chain-hardening-checklist)
- [Lock Autoboot with a Proven Recovery Path](#lock-autoboot-with-a-proven-recovery-path)
- [Disable Unauthenticated Environment Writes](#disable-unauthenticated-environment-writes)
- [Make the FIT Signature Required](#make-the-fit-signature-required)
- [Extend Trust to the SPL](#extend-trust-to-the-spl)
- [SoC Secure Boot and Fusing (HAB / OTP)](#soc-secure-boot-and-fusing-hab--otp)
- [Build-Provenance Logging](#build-provenance-logging)

## The Boot-Chain Hardening Checklist

Work top to bottom. Each step is more expensive and less reversible than the one
above it, so validate before descending. You MUST NOT skip ahead to fusing before
the software-only controls above it are proven on the exact target.

- [ ] **Establish a recovery path FIRST.** Confirm the SoC's ROM download mode
      (UART/USB serial-download) is reachable and documented for this board BEFORE
      changing anything else. Every step below can lock the console; this is the
      floor you fall back to. MUST NOT proceed without it.
- [ ] **Lock autoboot** so the console-interrupt window cannot be used to bypass the
      boot script — but only with the recovery path above proven. Reversible in
      software until fuses are involved.
- [ ] **Make the environment non-authoritative for trust decisions.** Disable or
      write-protect `saveenv` so a runtime env write cannot redirect the boot. The
      env MUST NOT be able to override `bootcmd`, the FIT it loads, or the key.
- [ ] **Require a valid FIT signature.** Move from "signature present" to "unsigned
      or wrongly-signed images are rejected" (`required` property + `CONFIG_FIT_SIGNATURE`).
- [ ] **Extend trust to the SPL.** Have the SPL verify the U-Boot-proper FIT it loads,
      so the chain is unbroken from the first mutable stage.
- [ ] **Prove the signed image boots from the intended key set on the exact target.**
      A signed image MUST be demonstrated to boot before any one-way step.
- [ ] **(One-way) Fuse SoC secure boot.** Blow the ROM's public-key hash and the
      "closed"/secure fuse. IRREVERSIBLE — see the fusing section; MUST get explicit
      user confirmation first.

The dividing line is the last box: everything above it is recoverable in software or
by reflashing; the fuse step is permanent silicon state.

## Lock Autoboot with a Proven Recovery Path

Autoboot normally pauses for a keypress so an operator can drop to the U-Boot shell.
On a hardened device that pause is an attack surface: shell access defeats every
control below it. Close it — but only once you can still recover the board.

You MUST confirm a recovery path exists before applying any of these. Options, in
order of preference: the SoC ROM serial-download mode, a physical boot-mode switch or
strap that forces ROM recovery, or a second (fused) fallback image.

```bash
# Remove the interactive pause. bootdelay=-2 boots immediately with NO key check;
# bootdelay=-1 disables autoboot entirely (stays at the prompt) — the opposite intent.
setenv bootdelay -2

# Gate the interrupt behind a key-hash so a random keypress cannot break in.
# CONFIG_AUTOBOOT_STOP_STR_SHA256 / CONFIG_AUTOBOOT_KEYED enable this at build time.
setenv bootstopkeysha256 <sha256-of-the-secret-key-sequence>

# Password-protect the prompt (CONFIG_AUTOBOOT_ENCRYPT + CONFIG_AUTOBOOT_PASSWORD_...).
```

Reversal / recovery path (keep this ready before you apply the lock):

```bash
# If the env is still writable and you still have console access, undo it:
setenv bootdelay 2
saveenv                       # confirmation-gated; see SKILL.md

# If the console is already locked out: enter the SoC ROM download mode and
# re-flash U-Boot + a clean env with the vendor loader (imx-usb-loader, uuu,
# sunxi-fel, sam-ba, tegrarcm, ...). This is the reason the recovery path is step one.
```

WARNING: setting `bootdelay=-2` together with a write-protected env and no ROM
recovery strap is a common way to permanently brick console access. MUST NOT lock
autoboot on a board whose recovery path you have not personally verified.

## Disable Unauthenticated Environment Writes

The environment is stored on mutable media (eMMC/SD/NAND/SPI-NOR). If `bootcmd`,
`bootargs`, or a key path lives in a writable env, an attacker (or a careless
`fw_setenv`) can redirect the boot without touching the signed image. Harden the env
so it cannot be an unauthenticated trust bypass.

Choose the strongest option the board tolerates:

```text
# 1. No writable env at all — env is compiled in, saveenv has nowhere to go.
CONFIG_ENV_IS_NOWHERE=y          # runtime env is the built-in default only

# 2. Read-only saveenv path — keep the env readable but reject writes.
# CONFIG_ENV_WRITEABLE_LIST restricts which vars saveenv may change (allow-list);
# combine with CONFIG_ENV_ACCESS_IGNORE_FORCE so `env set -f` cannot override it.
CONFIG_ENV_WRITEABLE_LIST=y
CONFIG_ENV_ACCESS_IGNORE_FORCE=y

# 3. Keep security-critical vars out of the env entirely — bake bootcmd/bootargs
# into the .env text (CONFIG_ENV_SOURCE_FILE) or the control FDT so a runtime
# env write cannot reach them.
```

Mark individual variables read-only from within the environment itself, so even a
writable backend refuses to change them:

```bash
# .flags entries: r = read-only, b = boolean, s = string, etc.
# Once bootcmd is 'r', `setenv bootcmd ...` and saveenv cannot alter it.
setenv .flags bootcmd:sr,bootargs:sr,bootdelay:dr
```

Reversal: this is a defconfig / `.flags` change, fully reversible by rebuilding U-Boot
(or, for `.flags`, by an authenticated env reset) — no permanent state is written.
It becomes effectively permanent only after the containing U-Boot is itself signed and
the signature is required. MUST verify the board still boots its normal path after
locking the env, since a mistyped allow-list can strand a needed variable.

You MUST NOT rely on the env for any trust decision that the FIT signature is meant to
enforce. The signature is the trust anchor; the env is convenience state.

## Make the FIT Signature Required

`uboot-boot-scripts.md` covers building and signing a FIT (`mkimage -f ... -k keys
-K u-boot.dtb -r image.itb`) and enabling verification with `CONFIG_FIT_SIGNATURE=y`
/ `CONFIG_RSA=y`. That gets signatures *checked* — but by default an image with **no**
signature can still boot. Hardening means unsigned and wrongly-signed images are
**rejected**.

Two halves must agree: the image must declare that a signature is required, and U-Boot
must be built to enforce it.

Declare the requirement in the `.its` by adding a `required` property to the signature
node. `required = "conf"` binds the signature to the whole configuration (kernel + FDT
+ ramdisk together — the strong choice); `required = "image"` requires each individual
image to be signed.

```dts
configurations {
    default = "conf-1";
    conf-1 {
        description = "Signed kernel + FDT";
        kernel = "kernel";
        fdt = "fdt-1";
        signature {
            algo = "sha256,rsa2048";
            key-name-hint = "dev";
            sign-images = "kernel", "fdt";
            /* This is the hardening line: reject configs lacking a valid signature. */
            required = "conf";
        };
    };
};
```

Build U-Boot to enforce it and to refuse the legacy/unsigned fallbacks:

```text
CONFIG_FIT_SIGNATURE=y            # verify signatures
CONFIG_RSA=y                      # RSA verify algorithm
CONFIG_FIT_SIGNATURE_MAX_SIZE=0x... # bound the FIT the verifier will parse
CONFIG_LEGACY_IMAGE_FORMAT=n      # refuse unsigned legacy uImages
# Do NOT leave a raw booti/bootz path in bootcmd that bypasses FIT verification.
```

With `CONFIG_FIT_SIGNATURE=y`, U-Boot's `bootm` verifies the configuration signature
against the public key in its control FDT before it will relocate and boot the image; a
tampered or unsigned FIT fails with `Bad Data Hash` / `signature check failed` and
`bootm` aborts. Verify high-memory relocation (`fdt_high`, `initrd_high`) does not move
the FDT outside the verified region before enabling this in production.

Sign and inject the key exactly as in `uboot-boot-scripts.md`; the only additions here
are the `required` property and the enforcing defconfig above:

```bash
# Build + sign; -r requires all configs signed, -K injects the pubkey into u-boot.dtb
mkimage -f image.its -k keys -K u-boot.dtb -r image.itb

# Confirm the FIT actually carries the signature and the required flag (read-only)
dumpimage -l image.itb            # shows Sign algo + "Sign value" per config
fdtget u-boot.dtb /signature/key-dev required   # 'conf' once the pubkey is embedded
```

Reversal: rebuild U-Boot with `CONFIG_FIT_SIGNATURE` disabled (or reflash a prior
U-Boot) — reversible until the containing U-Boot is itself verified by a fused SPL.

WARNING: enabling a *required* signature and flashing it as the only U-Boot before a
signed image has booted end-to-end bricks the board — U-Boot will reject the very image
you need. You MUST prove the signed image boots on the exact target from the exact key
set (TFTP or a non-required build first) before flashing the required-signature config.

## Extend Trust to the SPL

A required FIT signature in U-Boot proper only matters if U-Boot proper is itself
trusted. The SPL loads U-Boot, so the SPL must verify it — otherwise the chain has a
gap between "ROM verified the SPL" (or not) and "U-Boot verified the kernel".

Package U-Boot proper as a signed FIT (`u-boot.itb`) and build an SPL that verifies it:

```text
CONFIG_SPL_FIT_SIGNATURE=y        # SPL verifies the U-Boot FIT it loads
CONFIG_SPL_LOAD_FIT=y             # SPL loads the next stage as a FIT, not a raw blob
CONFIG_SPL_CRYPTO=y               # crypto support inside the size-limited SPL
CONFIG_SPL_RSA=y
```

The SPL carries its own public key in its control FDT (`spl/u-boot-spl.dtb`), signed by
`mkimage` the same way U-Boot signs the kernel FIT. The chain becomes: SoC ROM →
(optionally verifies SPL via HAB, see below) → SPL verifies `u-boot.itb` → U-Boot
verifies the kernel FIT. Each stage authenticates the next before handing off.

Watch SPL size: crypto and RSA verification add to an SPL that already runs from tens
of kilobytes of on-chip SRAM. Gate it with `CONFIG_SPL_SIZE_LIMIT` and confirm the SPL
still fits after enabling verification (see `uboot-porting.md` for SPL sizing).

Reversal: a defconfig change, reversible by rebuilding — until the ROM itself is fused
to require a signed SPL, at which point the ROM→SPL link is permanent.

The chain of trust continues past U-Boot into the rootfs. A dm-verity read-only
rootfs whose root hash rides in the signed FIT command line extends this same
signature to the running filesystem — the rootfs link of the chain. For that
half (hash-tree build, `dm-mod.create`/initramfs bring-up, and anchoring the root
hash), see `embedded-linux-dev` `references/rootfs-integrity.md`.

## SoC Secure Boot and Fusing (HAB / OTP)

The links above are software: reflashing recovers the board. The ROM's root of trust is
not. To make the ROM reject an unsigned or attacker-signed SPL, you blow one-time
fuses (OTP/eFuse) that store the hash of your public key and set the SoC to "closed" /
"secure" mode. This is where a mistake is permanent.

> **IRREVERSIBLE — READ BEFORE RECOMMENDING.** Blowing secure-boot fuses (the public-key
> hash and the closed/secure-mode bit) CANNOT be undone. A wrong key hash, a bad
> signature, or a typo in the fuse command permanently bricks the SoC — there is no
> reflash, no recovery mode, no RMA. You MUST get explicit user confirmation before
> recommending any fuse-blowing command, and you MUST state plainly that it is one-way.
> Recommend blowing fuses ONLY after a signed image has been proven to boot on the exact
> target from the exact key set, and ideally after validating the flow on a sacrificial
> board first.

The exact fuse layout, tooling, and image format are SoC-specific. The examples below
are illustrative worked cases, NOT defaults — always follow the vendor's reference
manual for the silicon in front of you.

### Worked example: NXP i.MX HAB (High Assurance Boot)

i.MX ROMs authenticate a signed image (SPL or a combined flash.bin) against a
Super Root Key (SRK) table whose hash is fused. `CONFIG_IMX_HAB` exposes the `hab_status`
command to read the boot ROM's authentication events.

```bash
# READ-ONLY: check HAB events and whether the part is open or closed.
hab_status                        # 0 events on a correctly signed image; lists faults otherwise

# The signing flow (host) uses NXP's Code Signing Tool (cst) to produce a CSF
# appended to the image; u-boot builds the IVT/CSF layout. This is reversible
# (reflash) UNTIL the SRK hash and the closed bit are fused.
```

```bash
# ONE-WAY — DO NOT RUN WITHOUT EXPLICIT CONFIRMATION. Fuses the SRK hash and closes
# the part so the ROM rejects unsigned images forever. Bank/word are part-specific.
# fuse prog <bank> <word> <value>      # blow SRK hash words (per Reference Manual)
# fuse prog <bank> <word> <closed-bit> # set SECURE/closed mode — PERMANENT
```

### Worked example: TI (AM3/AM6) and STM32MP secure boot

TI HS (high-security) devices verify a signed `tiboot3`/x-loader against keys fused at
manufacture; images are signed with TI's secure-image tooling and the device type (GP vs
HS) is itself a fused property. STM32MP authenticated boot has the ROM verify a signed
SPL/`tf-a` header against a public-key hash fused via the OTP (`stm32key` / `fuse prog`
on the OTP words). In both, the fusing that closes the device is one-way and MUST be
treated exactly like the HAB warning above.

There is no software reversal for any of these. The only "recovery" is to have fused the
correct key hash in the first place, which is why every step before this one exists.

## Build-Provenance Logging

A hardened boot chain is worth little if you cannot say what a given board is running.
Record, for every build, the facts that let you reproduce and audit it later: the source
revision (and whether the tree was dirty), the toolchain identity, the defconfig, and the
SHA-256 of the actual SPL and FIT/`u-boot.itb` outputs. Stamp these into a build-info
record next to the artifacts and, where the board allows, expose the revision string in
the U-Boot banner (`u-boot` already embeds `git describe` in
`include/generated/version_autogenerated.h`).

The script below is read-only over the build tree — it computes and records, it does not
mutate sources or media, so it needs no confirmation gate. Run it right after a build.

```bash
#!/usr/bin/env bash
# stamp-uboot-provenance.sh — record the identity of a U-Boot build.
# Read-only: hashes artifacts and captures build facts into a build-info record.
# Usage: stamp-uboot-provenance.sh <defconfig> <artifact> [artifact ...]
#   e.g. stamp-uboot-provenance.sh am335x_evm_defconfig \
#          spl/u-boot-spl.bin u-boot.itb
# Env: CROSS_COMPILE (optional; empty means a native toolchain).
set -Eeuo pipefail

usage() {
  printf 'Usage: %s <defconfig> <artifact> [artifact ...]\n' "${0##*/}" >&2
  exit 2
}

(($# >= 2)) || usage

defconfig="$1"
shift
artifacts=("$@")

# Required external tool.
command -v sha256sum > /dev/null 2>&1 ||
  {
    printf 'error: missing required tool: sha256sum\n' >&2
    exit 1
  }

# Source revision + dirty flag (guard: the build tree may not be a git checkout).
if git -C . rev-parse --git-dir > /dev/null 2>&1; then
  source_rev="$(git describe --always --dirty --tags 2> /dev/null ||
    git rev-parse --short HEAD)"
else
  source_rev="unknown (not a git tree)"
fi

# Toolchain identity. CROSS_COMPILE may be unset/empty for a native build.
cc="${CROSS_COMPILE:-}gcc"
if command -v "$cc" > /dev/null 2>&1; then
  toolchain="$("$cc" --version | head -n1)"
else
  toolchain="unknown (compiler not found: $cc)"
fi

record="build-info.txt"
{
  printf 'u-boot build-info\n'
  printf 'generated:    %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'source_rev:   %s\n' "$source_rev"
  printf 'defconfig:    %s\n' "$defconfig"
  printf 'cross_compile: %s\n' "${CROSS_COMPILE:-<native>}"
  printf 'toolchain:    %s\n' "$toolchain"
  printf 'artifacts (sha256):\n'
  for artifact in "${artifacts[@]}"; do
    if [[ -r "$artifact" ]]; then
      # sha256sum emits "<hash>  <path>"; -- guards paths that start with '-'.
      printf '  %s\n' "$(sha256sum -- "$artifact")"
    else
      printf '  MISSING  %s\n' "$artifact" >&2
      printf '  MISSING  %s\n' "$artifact"
    fi
  done
} > "$record"

printf 'wrote %s\n' "$record"
cat -- "$record"
```

Keep the resulting `build-info.txt` with the release artifacts (or commit its hash to
the release record). To verify a suspect board later, re-run the same defconfig +
toolchain, hash the outputs, and compare: a matching `source_rev` with mismatching
artifact hashes means a reproducibility or toolchain drift, which is itself the finding.
For a reproducible-build guarantee, pin the toolchain (see the toolchain pointers in the
port brief) and keep the build path length stable, since some builds embed it.
