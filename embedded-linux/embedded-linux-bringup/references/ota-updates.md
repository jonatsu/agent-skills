# Update and Recovery Diagnostics

This reference covers installation failures, wrong-slot boots, missing confirmation, and failed recovery on an embedded
target. Framework selection, fleet rollout policy, server operation, and partition redesign need their own system
design. Consult [RAUC](https://rauc.readthedocs.io/) or [SWUpdate](https://sbabic.github.io/swupdate/) for those interfaces.
Route packaging to the build-system skill and boot-selection implementation to **u-boot-development**.

## Record the Update Contract

Before diagnosis, identify the framework/version, board compatibility, artifact identity/signature, current slot,
target slot, slot devices, kernel/DTB selection, boot backend, persistent data, and recovery access.
Inspect actual configuration and installation logs rather than inferring layout from `mmcblk0pN` examples.

Separate the stages: artifact retrieval, verification, target selection, writing, activation, reboot, health check,
confirmation, and fallback. A successful installer exit does not establish that the target booted and confirmed the
new image. Reproduce only the necessary stage within the approved scope.

In A/B systems, preserve the currently working slot while writing the selected inactive slot.
In a rescue-based system, prove the independent rescue path remains available before rewriting the production image.

## RAUC: Installation and Boot Confirmation

Find the active `system.conf`: RAUC v1.14 reads the first of `/etc/rauc/`, `/run/rauc/`, and `/usr/lib/rauc/`,
unless `--conf` selects another. Inspect it with the slot relationships, bootnames, backend configuration, and
current status:

```bash
rauc status --detailed
```

Check the bundle's compatible value and signature against the intended keyring before an authorized installation.
Use the installed version's `rauc info`/keyring options to inspect a bundle; do not disable verification to diagnose a
production verification failure. Investigate certificate trust, validity, artifact damage, and configuration instead.

For an authorized update, `rauc install update.raucb` performs installation using the configured slot/backend model.
Review hooks, custom handlers, shared/nonredundant components, and activation policy; do not assume every configuration
has identical side effects. Confirm the selected image set after reboot before marking it healthy.

```bash
# Only after the platform's health check has passed for the booted slot:
rauc status mark-good
```

For RAUC v1.14's U-Boot backend, `BOOT_ORDER` selects priority and `BOOT_<bootname>_LEFT` counts attempts remaining.
Marking a slot good restores its configured positive attempt count; zero attempts is the bad-slot case.
This is different from clearing a failure counter such as U-Boot `bootcount`.
Check [the backend implementation](https://github.com/rauc/rauc/blob/v1.14/src/bootloaders/uboot.c)
and the actual boot script together. Do not mix their counters or manually reset them using the other model's semantics.

When a slot fails, inspect its remaining attempts, priority, boot selection, and the condition that should trigger
another attempt. Exhausting counters requires the actual boot/reboot path to execute; an indefinite hang needs an
effective watchdog or other recovery mechanism. A mark-good service must depend on demonstrated application health,
not merely on reaching an early startup target.

These install behaviours hold for RAUC v1.15.2, checked 2026-10-29 against `src/install.c`, `src/service.c`, and the
[reference](https://rauc.readthedocs.io/en/v1.15.2/reference.html):

- The default handler marks the target slot bad before it writes the first byte, and activates it only after every
  slot is written. Any interrupted or failed install therefore leaves that slot bad. A full custom `handler=` in the
  manifest skips this marking.
- Built with its service, the default, `rauc install` is a D-Bus client. A second install during the first fails with
  `Already processing a different method`; wait for the first to finish.
- `rauc info` and the D-Bus `InspectBundle` method verify the signature by default. For a `crypt` bundle they first
  decrypt the envelope with the device key, so the unauthenticated envelope reaches that key before any signature
  check. Treat inspecting a bundle from untrusted media as handing attacker input to the decryption.
- `events=` in a `[log.<name>]` section is a semicolon-separated list of `install`, `boot`, and `mark`, or `all`.

## SWUpdate: Manifest, Selection, and Handler Failures

Inspect the installed framework configuration and the selected `sw-description` branch, hardware revision, target
devices/volumes, image handlers, scripts, and boot-environment changes.
A hardcoded destination is not automatically the inactive slot. The active slot and selected manifest must agree.

For signed `.swu` archives, verify the signature configuration and manifest-bound payload hashes.
Inspect archive order and required metadata against the selected release; do not execute an archive to inspect it.
Use handler/installer logs to distinguish metadata, signature, target-selection, write, script, and activation failures.
Production verification must remain enabled. The native
[signed-image documentation](https://sbabic.github.io/swupdate/signed_images.html) describes the verification boundary.

Treat boot confirmation as an explicit contract between the health check and the configured boot backend.
SWUpdate's flexible handlers and scripts do not imply RAUC's exact variables or mark-good API.
Keep environment writes and boot script repairs with **u-boot-development**, informed by the updater's observed state.

## Bundle Integrity Versus Running-rootfs Integrity

RAUC `plain`, `verity`, and `crypt` are bundle formats with different verification, streaming, and encryption behavior.
Select and diagnose them using the release's supported format and kernel requirements.
The `verity` bundle format checks the bundle payload during installation; it does not automatically configure
dm-verity for the installed root filesystem. See [rootfs-integrity.md](rootfs-integrity.md) for that separate boot
path.

The `verity` signature covers the manifest and the verity root hash, not the payload bytes, so a damaged payload
passes the signature check. dm-verity then fails the copy with an I/O error, and the kernel log names the corrupted
block. `perform-pre-check=true` reads the whole payload before installing.

## Qualify Recovery Without Promising It from the Layout

A/B can preserve an old image while installation proceeds, but activation normally needs reboot downtime.
Power-loss recovery depends on persistent boot state, shared boot artifacts, storage behavior, watchdog coverage,
and compatibility of persistent data with the fallback image. A rescue partition is useful only if it is protected,
reachable, and capable of completing recovery after the failure being tested.

On a suitable approved bench target, distinguish failures during payload writing, activation-state updates, kernel
startup, service startup, and post-boot health checks. Record which image boots and how confirmation/fallback occurs.
Forced power loss, deliberate image corruption, and fleet updates require authorization for those effects.
Do not weaken signature checks or remove rollback to make an installation appear successful.

### Fault-injection recipes for RAUC

A RAUC bundle ends with its CMS signature, followed by the signature's size as an 8-byte big-endian integer. Damage a
copy of the bundle, never the original, by flipping one bit:

```bash
size=$(stat -c %s update.raucb)
sigsize=$(tail -c 8 update.raucb | od -An -tu8 --endian=big | tr -d ' ')
sigstart=$((size - 8 - sigsize))
flip() { b=$(od -An -tu1 -j "$2" -N1 "$1" | tr -d ' '); printf "$(printf '\\%03o' $((b ^ 1)))" |
  dd of="$1" bs=1 seek="$2" conv=notrunc status=none; }
cp update.raucb bad-sig.raucb && flip bad-sig.raucb $((sigstart + sigsize / 2))   # refusal path
cp update.raucb bad-data.raucb && flip bad-data.raucb $((sigstart / 2))            # verity path
```

The damaged signature must make RAUC refuse the bundle when it opens it, before any slot is written. The damaged
payload passes the signature check of a `verity` bundle and must fail during the copy; with 4096-byte verity data
blocks, the kernel names block offset / 4096. That failure must leave the target slot bad and the booted slot
primary.

- **Reset during an install:** `systemctl reboot --force --force` reboots at once without stopping processes or
  unmounting file systems. It is the nearest shell equivalent of a power cut, but the storage device keeps its power,
  so a real power cut remains the stronger test. Magic SysRq `b` is an alternative where `/proc/sysrq-trigger` exists;
  hardened kernels often omit it.
- **Boot-counter fallback:** in the inactive slot's root filesystem, mask its mark-good unit by linking it to
  `/dev/null` under `/etc/systemd/system/`. RAUC does not ship that unit; the integration does, such as meta-rauc's
  `rauc-mark-good.service`. Activate the slot and reboot repeatedly. Each boot must spend one attempt, the bootloader
  must then fall back, and `rauc status` must then report the slot bad.

Report installer success, selected boot image, health confirmation, and tested recovery separately.
If no hardware recovery test ran, leave recovery qualification unverified.
