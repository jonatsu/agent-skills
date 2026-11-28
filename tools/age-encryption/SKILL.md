---
name: age-encryption
description: Encrypt and decrypt files with age or rage. Use to generate an age key, including a post-quantum one; to encrypt a file, archive, or backup to someone's age, SSH, or GitHub keys or to a passphrase; to decrypt an .age file; or to use a YubiKey, Nitrokey, or other hardware key as an age identity. Not for SOPS-managed secrets files (sops-secrets), signing files, or provisioning the token itself (hardware-security-keys).
license: MIT
compatibility: Post-quantum keys and tagged hardware recipients need age 1.3 or later; rage 0.12 has no post-quantum keys. A hardware identity needs its age-plugin binary on PATH.
metadata:
  author: Joonas Onatsu
---

# age Encryption

age encrypts one file or stream to one or more recipients (public keys), or to one passphrase. Whoever holds a
matching identity (private key) decrypts it. age has no configuration, keyring, or default key path, so every command
names its keys. rage is a compatible implementation with the same flags.

Current known: age 1.3.2, checked 2026-11-28 by runs; rage 0.12.1 from its README.

## Choose a Key

- **Native post-quantum key**, upstream's recommendation for most uses: `age-keygen -pq -o key.txt`. Its recipient
  starts `age1pq1` and is about 1960 characters long.
- **Native classic key**, for a file that must also open with rage, an older age, or a hardware key:
  `age-keygen -o key.txt`. Its recipient starts `age1` and is 62 characters long.
- **An SSH key**, only when the recipient has no age key: `ssh-ed25519`, or `ssh-rsa` of at least 2048 bits. A file
  encrypted to one names a short tag of that key, and `ssh-agent`, ECDSA keys, and SSH keys held on a token do not
  work.
- **A hardware key**: read [references/hardware-keys.md](references/hardware-keys.md) before generating its identity.
- **A passphrase**, with `-p`: interactive only, and it cannot share a file with recipients.

A file's recipients are either all post-quantum or all classic; age refuses a mix. `age-keygen -o` creates the file
mode 0600 and never overwrites one. Print a key's recipient with `age-keygen -y key.txt`.

## Encrypt and Decrypt

```bash
age -r age1... -r age1... -o report.pdf.age report.pdf  # each recipient decrypts on their own
age -R recipients.txt -o backup.tar.age backup.tar     # one recipient per line, # starts a comment
tar cz data/ | age -R recipients.txt -o data.tgz.age   # a directory, as one stream
curl -fsS https://github.com/USER.keys | age -R - -o f.age f  # a GitHub user's SSH keys
age -e -i key.txt -o notes.txt.age notes.txt           # to your own identity's recipient
age -d -i key.txt -o report.pdf report.pdf.age
```

- Put every flag before the one INPUT. When `-R -` or `-i -` reads stdin, INPUT must be a file.
- A recipients file skips SSH key types age cannot use, with a warning, and fails with `no recipients found` when
  none is left. A GitHub user with only ECDSA or security-key SSH keys needs an age key instead.
- Write plaintext with `-o` to a file, never to the transcript, unless the user asks to see it. `-o` overwrites
  without asking and uses the umask's mode, so set `umask 077` before decrypting.
- Delete the output when `age -d` exits nonzero. A truncated file can still leave its first authenticated chunks
  behind.
- `-a` armors the output for a text channel. It changes the encoding only.
- Encrypt to two recipients from the start: the working key and a backup key kept offline. A file whose only identity
  is lost cannot be recovered. Before deleting the plaintext, decrypt once with each identity you hold.

For a run nobody attends, `-p` fails, because it reads the passphrase from the terminal, so use an identity file
instead. A passphrase-protected identity file, `age-keygen | age -p > key.age`, still prompts once on each use. Stream a
key from a secret store without writing it to disk, through any command that prints it:
`age -d -i <(<command that prints the key>) FILE`.

## Know What age Does Not Do

- **It does not authenticate the sender.** Anyone with a recipient can create a file for it, and any recipient of a
  shared file can create a new one the others accept. When the reader must know who sent a file, sign it as well, for
  example with `ssh-keygen -Y sign` or signify. Upstream documents no safe way to combine the two.
- **It cannot revoke.** A stolen identity decrypts every file ever encrypted to it, so replace the key and re-encrypt
  the files that still matter.
- **It hides less than the content.** Ciphertext length shows the plaintext length, the header shows the recipient
  types, and SSH and tagged hardware recipients identify their key.

## Plugins

For a recipient `age1NAME1...` or an identity `AGE-PLUGIN-NAME-1...`, age runs `age-plugin-NAME` from PATH. `-j NAME`
selects a plugin that needs no identity file. A plugin runs with your privileges, so install only plugins the user
trusts. Plugin identities usually cover hardware keys, which
[references/hardware-keys.md](references/hardware-keys.md) describes.
