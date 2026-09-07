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
Do not overwrite the running production root, sole recovery image, or shared boot state as a diagnostic experiment.

## RAUC: Installation and Boot Confirmation

Inspect `/etc/rauc/system.conf`, slot relationships, bootnames, backend configuration, and current status:

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
dm-verity for the installed root filesystem. See [rootfs-integrity.md](rootfs-integrity.md) for that separate boot path.

## Qualify Recovery Without Promising It from the Layout

A/B can preserve an old image while installation proceeds, but activation normally needs reboot downtime.
Power-loss recovery depends on persistent boot state, shared boot artifacts, storage behavior, watchdog coverage,
and compatibility of persistent data with the fallback image. A rescue partition is useful only if it is protected,
reachable, and capable of completing recovery after the failure being tested.

On a suitable approved bench target, distinguish failures during payload writing, activation-state updates, kernel
startup, service startup, and post-boot health checks. Record which image boots and how confirmation/fallback occurs.
Forced power loss, deliberate image corruption, and fleet updates require authorization for those effects.
Do not weaken signature checks or remove rollback to make an installation appear successful.

Report installer success, selected boot image, health confirmation, and tested recovery separately.
If no hardware recovery test ran, leave recovery qualification unverified.
