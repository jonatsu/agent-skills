# U-Boot Security and Build Provenance

Define what an attacker can change before choosing controls: console input, persistent environment, removable media,
network payloads, update state or later DT fixups. Identify the trusted verifier and key at each handoff. A signature is
evidence checked by that verifier, not itself a trust anchor.

## Contents

- [Recovery and shell access](#recovery-and-shell-access)
- [Environment controls](#environment-controls)
- [FIT enforcement](#fit-enforcement)
- [Final kernel inputs](#final-kernel-inputs)
- [SoC lifecycle and provisioning](#soc-lifecycle-and-provisioning)
- [Build provenance helper](#build-provenance-helper)

## Recovery and shell access

Before deploying a restrictive configuration, qualify a recovery method allowed by the board's current and intended
security lifecycle. ROM download mode, a recovery image, or alternate media may be unavailable or may require a correctly
signed payload. Do not promise universal reflashing or universal irrecoverability.

`bootdelay=0` removes the delay but retains interruption checking; `-2` disables the abort check, while `-1` suppresses
autoboot. Keyed or encrypted autoboot options govern interruption. They do not authenticate every command prompt entry.
In [main_loop](https://github.com/u-boot/u-boot/blob/v2025.10/common/main.c), a returning boot command can reach the CLI.
A prompt can redirect execution even if the environment cannot be saved.

Define the intended outcome for failed loads, rejected FITs, missing media, returning scripts and abort attempts. Inspect
CLI availability, boot-command failure handling, alternate methods and recovery commands in the actual build. Test each
path under the enforcing configuration. A successful uninterrupted boot does not prove shell lockdown. Recovering a
previous configuration must also remain permitted by the trust policy then in force.

## Environment controls

Compiled `.env` or C defaults populate mutable RAM state. `CONFIG_ENV_IS_NOWHERE` removes persistence, not RAM mutation.
Neither places boot decisions beyond shell or import influence.

`CONFIG_ENV_WRITEABLE_LIST` restricts creation, mutation and import to explicitly writable variables. It is not a
`saveenv`-only allow-list and does not authenticate arbitrary backend bytes. `CONFIG_ENV_ACCESS_IGNORE_FORCE` controls
force behavior in applicable paths. Check their resolved configuration and the
[environment Kconfig contract](https://github.com/u-boot/u-boot/blob/v2025.10/env/Kconfig).

Runtime `.flags` can alter variable access policy. Protect the policy itself and its static definitions; setting a
read-only flag through an attacker-writable `.flags` variable is insufficient. Test critical-variable mutation, `.flags`
changes, force/default/import operations, and modified persistent state. Define expected rejection for each attacker
capability rather than assuming one console test covers raw-media replacement. See the
[flags callback](https://github.com/u-boot/u-boot/blob/v2025.10/env/flags.c).

Keep trust decisions in authenticated code/data, then constrain all untrusted inputs that can redirect them. Compiling a
string into initial environment defaults does not accomplish this by itself.

## FIT enforcement

Use the actual configuration-signature declaration and host command in
[signed FIT construction](uboot-boot-scripts.md#signed-fit-construction). Enforcing required configuration signatures
reads keys and `required = "conf"` from the **verifier's trusted control DT**. The untrusted FIT cannot impose this
policy on its own verifier. See
[required-key verification](https://github.com/u-boot/u-boot/blob/v2025.10/boot/image-fit-sig.c).

Check the verifier's resolved FIT/signature/algorithm options and any parser size limits. `CONFIG_FIT_SIGNATURE=y`
alone is insufficient: verify the required key node, package that exact DT, and account for raw `booti`/`bootz`, legacy
images, scripts, EFI, network and recovery paths that might bypass this policy. Disable or enforce unsupported paths
according to the required threat boundary; a configured preferred boot path does not eliminate alternatives.

For SPL, independently establish its next-stage format, FIT loading/signature/algorithm options, required keys, control
DT provider and final packaged image. Injecting a public key with `mkimage -K spl/u-boot-spl.dtb` does **not** sign that
DT. Its authenticity depends on how ROM or a preceding trusted stage authenticates the SPL image containing it.
Likewise, U-Boot proper's required kernel key must reside in its authenticated verifier artifact.

A qualification matrix must include valid, unsigned, wrong-key, altered signature, tampered kernel/DT/ramdisk and
alternate boot paths. Run acceptance/rejection with the exact enforcing build and packaged control DT. Host signature
tools can check a FIT/control-DT pair, but cannot prove that ROM authenticates that verifier or that the board has no
bypass. `dumpimage -l` is metadata inspection only.

For key rotation, coordinate which keys the verifier trusts/requires with which images remain bootable at every update
step. Exercise recovery and rollback policy with those combinations. Do not recommend disabling verification as recovery
unless that change itself is permitted and explicitly authorized by the actual trust policy.

## Final kernel inputs

Trace the authenticated root hash, root-device selection and command line to the values Linux actually consumes.
A signed DT's `/chosen/bootargs` may be replaced by environment-derived `bootargs` in
[fdt_chosen](https://github.com/u-boot/u-boot/blob/v2025.10/boot/fdt_support.c). Other board fixups and alternate loaders
can also introduce inputs after verification. Moving a verified blob is different from modifying its contents; safe
memory placement alone does not authenticate a later change.

For each source of bootargs, root hash, DT fixups and slot selection, change it independently in a disposable test.
Untrusted values must be rejected or have no effect on authenticated inputs. Inspect the final kernel command line and
verity setup. Use **embedded-linux-bringup**, `references/rootfs-integrity.md`, for dm-verity and rootfs validation;
retain its requirement that the consumed root hash be authenticated through the complete handoff.

## SoC lifecycle and provisioning

OTP/eFuse writes cannot be reversed. An image rejected after provisioning is a different event: some systems permit
authenticated recovery, others restrict it. Before proposing provisioning, resolve the silicon revision, ROM scheme,
lifecycle, customer-key state, revocation/rollback rules, image format and vendor recovery policy.

| Example family/scheme | Distinction to establish                                                                                         |
| --------------------- | ---------------------------------------------------------------------------------------------------------------- |
| NXP HAB               | Match HAB version and silicon; HABv3 evidence is not an i.MX6/8 HABv4 procedure, and AHAB uses a different chain |
| TI K3                 | Distinguish GP, HS-FS and HS-SE; do not infer factory customer-key enforcement from “HS” alone                   |
| STM32MP               | Match chip revision, ROM/authentication format and provisioning state; SPL/TF-A responsibilities vary            |

The [v2025.10 K3 guide](https://github.com/u-boot/u-boot/blob/v2025.10/doc/board/ti/k3.rst) documents HS-FS/HS-SE
roles. NXP AN4547 Rev. 0 (10/2012), section 2.2, describes HABv3 authenticated serial-download recovery as a bounded
counterexample to “any bad signature permanently bricks every SoC.” It supplies no provisioning recipe for another HAB
generation. Consult the exact vendor manual for any intended target.

Prepare a matrix of present/intended lifecycle, accepted/rejected images, allowed recovery entry points, required keys,
revocation effects and tested outcomes. Open-state successful boot does not prove closed-state enforcement. Require
explicit authorization for the exact irreversible transition and values. This skill supplies no generic fuse bank/word
commands. Software fixture tests cannot qualify physical provisioning, power-loss behavior or recoverability.

## Build provenance helper

The bundled [stamp-uboot-provenance.sh](../scripts/stamp-uboot-provenance.sh) writes a **new host record**; it is not a
read-only command. It reads required files and Git state, then publishes only after validation succeeds. It never writes
boot media. Requirements: Bash 4+, Git and GNU coreutils on Linux, a quiescent successful build, an explicit Git source
root and absolute paths. Sources without Git need a separately documented archive-identity workflow.

```bash
bash <skill-root>/scripts/stamp-uboot-provenance.sh \
  /absolute/source /absolute/build /absolute/release/build-info.txt \
  /absolute/build/build-identity.txt /absolute/build/spl/u-boot-spl.bin /absolute/build/u-boot.itb
```

Create `build-identity.txt` as part of the actual build, recording the invocation and environment, selected defconfig,
compiler path/version and wrappers, toolchain/container digest, external firmware/dependency pins and source patch
identity. Preserve its source records with the release. Do not generate a compiler identity from today's PATH and label
it as the compiler that produced an old image. Select the required artifacts for the board; a build without SPL need not
invent one.

The helper records the supplied identity file and its digest, source HEAD and current tracked/untracked status, effective
`build/.config` digest, and each required artifact digest. Paths/status are Bash-escaped for unambiguous display; do not
source the record as shell code. Missing, directory, unreadable, empty identity/config, hash failure or an existing
output causes nonzero exit. A temporary file is created beside the output and published with a no-replacement hard link;
this requires an output filesystem supporting hard links. It preserves existing files, directories and symlinks.

The caller owns the relationship between source, build-time evidence and artifacts. Quiesce concurrent writers before
capture; the script does not lock the source/build or certify historical provenance. Preserve dirty patches and untracked
inputs separately; a dirty status is not their content. The record is unsigned and is not an attestation. Matching
revision or build-path length alone does not prove reproducibility; rebuild using preserved inputs and compare outputs,
then investigate any mismatch rather than inferring a single cause.
