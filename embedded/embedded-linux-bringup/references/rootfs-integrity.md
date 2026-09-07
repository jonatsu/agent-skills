# Verified-rootfs Bring-up with dm-verity

Diagnose three separate boundaries: the data/hash layout, the kernel mapping, and the authenticity of the parameters
that reach that mapping. A self-consistent hash tree does not establish that its root hash came from a trusted source.

## What Failure Means

dm-verity verifies covered blocks as they are read through a read-only mapping.
Unread corrupt data may not prevent boot. Without recovery by configured error correction, Linux v6.12 behaves as follows:

| Selected policy         | Result when corrupt data is detected                                           |
| ----------------------- | ------------------------------------------------------------------------------ |
| Default                 | Fail the affected I/O; do not return the corrupt data as successfully verified |
| `ignore_corruption`     | Log and permit the read; weakens integrity enforcement                         |
| `restart_on_corruption` | Restart; needs a recovery policy that avoids an endless restart loop           |
| `panic_on_corruption`   | Panic; needs a usable recovery path                                            |

I/O errors and integrity mismatches have distinct policy controls. Check the installed kernel's options and defaults.
`ignore_zero_blocks` returns zeroes for blocks expected to be zero rather than accepting arbitrary on-media contents.
See the [kernel verity documentation](https://docs.kernel.org/admin-guide/device-mapper/verity.html).
Do not switch to `ignore_corruption` to hide a failing production verification step.

## Verify the Build Artifacts First

Use cryptsetup's `veritysetup` on immutable build artifacts or disposable copies, not a mounted writable production root.
`format` writes the hash device/file; select that destination explicitly and preserve any existing valuable content.

```bash
# Build host: rootfs.img is the finished data image; rootfs.hash is a new output file.
veritysetup format --hash=sha256 --data-block-size=4096 --hash-block-size=4096 rootfs.img rootfs.hash
```

Record the output root hash, salt, covered data blocks, format version, block sizes, hash offset, algorithm,
and whether a verity superblock exists. Keep this record with the exact data/hash artifact hashes.
The image must contain complete data blocks; do not silently leave a trailing payload outside coverage.
If either image changes after formatting, regenerate the tree and update the authenticated parameter set together.

```bash
# Substitute the root hash from the format result; this userspace check creates no DM mapping.
veritysetup verify rootfs.img rootfs.hash ROOT_HASH
```

Check the exit status. A userspace verify proves consistency against the supplied hash, not its authenticity or a
working boot configuration. With nondefault/no-superblock layouts, supply the parameters required by that layout.
For appended hashes, establish a nonoverlapping offset and explicit data extent before formatting.
Use the [cryptsetup manuals](https://gitlab.com/cryptsetup/cryptsetup/-/tree/v2.7.0/man) for the chosen release.

## Bring Up the Mapping

An initramfs can create the mapping after storage discovery with `veritysetup open`, then mount the mapped device as
the final root. It needs the tool, its dependencies, crypto support, and appropriate DM/storage drivers available at
that stage. Check each failure's command, status, and kernel diagnostic before changing the root hash.

Without an initramfs, the kernel's `dm-mod.create=` interface needs built-in DM initialization, verity, required crypto,
storage, and filesystem support. A module on the inaccessible final root cannot provide those prerequisites.
Use the [DM early-init table grammar](https://docs.kernel.org/admin-guide/device-mapper/dm-init.html).

Derive the table from the actual formatted layout: the mapping length is in sectors, block counts use their specified
block sizes, and the hash-tree start must account for any header/superblock and offset.
Do not copy the userspace byte offset directly into a field measured in hash blocks.
Check backing-device discovery/wait settings separately from waiting for the final mapped root.

Distinguish these failures:

- Missing backing device or mapping: discovery, built-in support, device naming, table syntax, or setup order.
- Mapping exists but reads fail: data/hash mismatch, wrong extent/offset/algorithm/salt, storage errors, or tampering.
- Userspace verify succeeds but boot fails: deployed artifact selection, kernel parameters, mapping setup, or trust path.

## Trace the Root Hash to the Kernel

Identify who supplies the root hash and all paths that can replace it or bypass the mapping.
A signed FIT is not by itself a guarantee that Linux receives authenticated bootargs.
U-Boot can modify the working FDT after image verification, including taking `bootargs` from the environment;
see [v2025.10 fdt_chosen](https://github.com/u-boot/u-boot/blob/v2025.10/boot/fdt_support.c#L301).

Possible designs include parameters in an authenticated DT or initramfs with later overrides constrained, or a
kernel-verified root-hash signature with enforced trusted-key policy.
For any design, verify the actual final kernel inputs, key trust, signature enforcement, and alternate boot paths.
An optional signature feature is not enforcement if an unsigned alternative can still be selected.
Route FIT authoring, environment restrictions, required signatures, and the earlier secure-boot chain to
**u-boot-development**. Do not prescribe a generic `.its` bootargs property as a complete trust solution.

Within an approved test environment, alter the root hash and unauthenticated bootargs independently.
Those changes must be rejected or unable to change the authenticated root path.
Also test attempted bypass through another `root=` or boot path; a valid verity mapping is ineffective if unused.
Do not claim this trust chain verified from a successful `veritysetup verify` alone.

## Writable State and A/B Updates

Keep writes outside the verified mapping. A separate writable data partition or overlay upper layer can support
application state, but that content is not authenticated by the lower rootfs's dm-verity tree.
An overlay can shadow verified executables/configuration; preserving lower-layer integrity does not authenticate the
combined filesystem view. Define which mutable paths the security design permits.
Encryption by itself, including ordinary dm-crypt, does not automatically authenticate mutable data.

Each updated slot needs matching data, hash tree, and authenticated parameters activated as one bootable set.
Preserve the old set and test recovery when an accessed block fails verification.
RAUC's verity bundle format protects the installation artifact; it does not establish this running-rootfs mapping.
See [update diagnostics](ota-updates.md) for installation and boot confirmation.

Report image consistency, mapping behavior, authenticated boot selection, and corruption recovery as separate results.
Name untested hardware, power-loss, and release conditions explicitly.
