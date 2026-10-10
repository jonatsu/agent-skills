# Encrypting Data at Rest

Two threats, and they need different designs. **A stolen device** is defeated by any key the running system
cannot be asked for while powered off. **A compromised root on a running device** is defeated only if the key
never becomes readable to userspace — which means a hardware key store and a policy that binds release to the
system's measured state.

A passphrase-less key file sitting in a read-only rootfs defeats the first threat and none of the second. Say
which threat a design covers; most embedded designs quietly cover only the first.

**The common failure is worse than that, and it is published advice.** A 2025 professional handbook on
embedded Linux security walks through automating LUKS unlock by writing a key file to the root filesystem,
restricting its permissions, and referencing it from `crypttab` — on a machine whose own `lsblk` output shows
that root filesystem is **not encrypted** — and presents it as an unambiguous improvement in security posture,
with no threat model stated. A key stored in cleartext next to the thing it unlocks defeats neither threat:
whoever steals the device gets both halves. Recognise this pattern when reviewing an existing design, and when
reading guidance about one.

## What the platform decides

**Portable rule: LUKS with a hardware-bound key needs kernel Trusted Keys backed by a real key store.** Where
the SoC's security block exposes no Trusted Keys backend, you get "naked" cryptsetup — a key that exists in
plaintext somewhere at unlock time — and the compromised-root threat is not addressed however the rest is
configured. Establish which of the following the target has before designing:

| Key store                                             | Trusted Keys backend                | Consequence                                                           |
| ----------------------------------------------------- | ----------------------------------- | --------------------------------------------------------------------- |
| Discrete or firmware TPM 2.0                          | `trusted` (TPM 2.0)                 | Sealing to PCRs is available; the reference case                      |
| OP-TEE / TEE-backed                                   | `trusted` (CAAM/TEE, SoC-dependent) | Check the vendor's kernel; support varies by part                     |
| SoC security block, no NVM or no Trusted Keys support | none                                | Naked cryptsetup only — state the limit rather than working around it |
| None                                                  | none                                | Encryption is a compliance gesture; do not present it as a control    |

Check on the target, not in the datasheet:

```sh
ls /dev/tpm0 /dev/tpmrm0
grep -E 'CONFIG_TRUSTED_KEYS|CONFIG_TCG_TPM|CONFIG_ENCRYPTED_KEYS' /proc/config.gz   # if IKCONFIG is on
keyctl add trusted testkey "new 32" @u                                               # does the backend answer?
```

## The Yocto wiring

Everything below is metadata, and each piece has a way of being missing without an error.

- **`cryptsetup` is not in OE-Core.** It is `meta-openembedded/meta-oe/recipes-crypto/cryptsetup` (2.7.5 at
  scarthgap), so `meta-oe` must be in `bblayers.conf`.

- **systemd's cryptsetup and TPM2 support are off by default.** At scarthgap the recipe's default
  `PACKAGECONFIG` contains neither, and both exist:

  ```bitbake
  PACKAGECONFIG[cryptsetup] = "-Dlibcryptsetup=true,-Dlibcryptsetup=false,cryptsetup,,cryptsetup"
  PACKAGECONFIG[tpm2] = "-Dtpm2=true,-Dtpm2=false,tpm2-tss,tpm2-tss libtss2 libtss2-tcti-device"
  ```

  Enable them explicitly, in the distro conf:

  ```bitbake
  PACKAGECONFIG:append:pn-systemd = " cryptsetup tpm2"
  ```

- **`systemd-cryptenroll` is packaged separately** — `FILES:${PN}-crypt` covers it and `${libdir}/cryptsetup`,
  with only an `RRECOMMENDS` from the main package. On an image built with `NO_RECOMMENDATIONS` or a curated
  package list, it is simply absent.

- **TPM tooling comes from `meta-security/meta-tpm`** — `tpm2-tools`, `tpm2-tss`, `tpm2-abrmd`,
  `tpm2-openssl`, `tpm2-pkcs11`. That layer declares `LAYERSERIES_COMPAT = "nanbield scarthgap"`, so the
  branch must match the release.

- **`clevis` is not packaged in `meta-security`** (checked at scarthgap). A clevis-based unlock needs another
  layer or your own recipe; do not write it into a design as if it were available.

- **`meta-encrypted-storage` is dead, and secondary write-ups still recommend it.** The only repository of
  that name was last pushed in 2017 and has five stars. Treat any guidance routing LUKS through it as stale,
  and build on `meta-oe`'s `cryptsetup` plus `meta-tpm` instead.

- **Filesystem-level alternatives**: `fscrypt` and `fscryptctl` (per-directory encryption, no separate block
  device) are in `meta-security/recipes-security`, and `ecryptfs-utils` and `cryptmount` are there too. Prefer
  fscrypt when the requirement is "encrypt this data directory" rather than "encrypt this partition" — it
  avoids a second block device and the initramfs unlock entirely.

## Design shapes that hold

1. **Encrypted data partition, key sealed to the TPM, rootfs read-only and verity-protected.** The rootfs
   carries no secret, so `dm-verity` covers integrity and LUKS covers the data. Enrolment binds the key to a
   measured state, and the unlock then happens through an `/etc/crypttab` entry:

   ```sh
   systemd-cryptenroll --tpm2-device=auto --tpm2-pcrs=<policy> /dev/<part>
   ```

2. **Encrypted rootfs, unlocked from an initramfs.** Needed when the rootfs itself is confidential. The
   initramfs then holds the unlock logic and must be part of the signed boot chain — see
   `chain-of-trust-wiring.md`, because an unsigned initramfs makes the whole design decorative.

3. **fscrypt on a directory tree.** Cheapest to integrate; protects file contents and names, not metadata or
   the directory structure above the protected tree.

**Design the recovery path with the enrolment.** A device whose only key slot is a TPM-sealed one is
unrecoverable the moment the sealing policy stops matching — a firmware update, a board repair, a TPM
failure. LUKS supports multiple key slots precisely so a second, differently-held credential can exist:
an escrow passphrase kept by whoever supports the fleet, or a recovery key generated per device and stored
off it. Enrol it at manufacture, not after the first field failure, and treat it as a secret with its own
custody story rather than a shared password.

**Which PCRs to seal against is the decision that decides whether this survives an update.** Sealing to
firmware and bootloader measurements means every legitimate firmware update invalidates the policy and needs a
re-enrolment path; sealing to too little means an attacker who can boot a modified kernel gets the key. Design
the re-enrolment path at the same time as the sealing policy, not afterwards.

## Verification

Host-side, the build only proves the pieces are present:

```bash
grep -E 'cryptsetup|tpm2-tools|libtss2' tmp/deploy/images/<machine>/<image>-<machine>.rootfs.manifest
bitbake -e systemd | grep '^PACKAGECONFIG='          # cryptsetup and tpm2 actually enabled?
```

On target, systemd's own feature string settles what it was built with, which is faster than inferring it
from the metadata:

```sh
systemd --version        # expect +TPM2 and +LIBCRYPTSETUP; a minus sign means the PACKAGECONFIG never landed
```

On target, the property:

```sh
cryptsetup luksDump /dev/<part>          # LUKS2, key slots, and which tokens are enrolled
systemd-cryptenroll --tpm2-device=list
lsblk -o NAME,TYPE,FSTYPE                # the mapper device, and what sits under it
cat /etc/crypttab
```

**Then prove the negative case, which is the only part that tests the design rather than the configuration:**

- Read the raw partition and confirm it is not plaintext — `head -c 4096 /dev/<part> | strings` finding your
  data is a complete failure.
- Change the measured state the key is sealed to (boot a different kernel, or extend a PCR) and confirm the
  unlock **fails**. A key that survives that was never bound to anything.
- For the compromised-root threat specifically: confirm root cannot extract the key material —
  `keyctl show`/`keyctl print` on a trusted key must return the wrapped blob, not the key.

An encryption setup never observed refusing to unlock has not been shown to protect anything.

## Stated limits

- **Sealing policy detail** — which PCR set suits a given update strategy — is not settled here. It depends on
  the boot chain, and getting it wrong is a field-bricking mistake, so the skill states the trade-off rather
  than a recommended PCR list.
- **Vendor security blocks other than TPM 2.0** vary too much to generalise; read the part's own reference
  manual for whether Trusted Keys are supported at all.
- **Nothing here has been run.** The commands are read from upstream documentation and recipe metadata, not
  executed against a board.
