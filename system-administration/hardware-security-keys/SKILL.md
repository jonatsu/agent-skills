---
name: hardware-security-keys
description: Provision and verify hardware security keys such as a YubiKey or Nitrokey, and the identities they carry (OpenPGP card subkeys, resident FIDO2 SSH keys, FIDO2 and PIV age identities, PIV PINs and management keys). Use when setting up, resetting, or re-provisioning a token, backing up its keys to a password manager, registering a token's public keys on GitHub or servers, or making SSH or age prefer it. Not for software-only keys, or for encrypted secrets files such as sops (nix-secrets).
license: MIT
compatibility: Needs the user present with the token; uses gpg, ssh-keygen, script, and per token ykman, nitropy, or an age plugin.
metadata:
  author: Joonas Onatsu
---

# Hardware Security Keys

Hardware-key work splits into two hands. The **operator** (the user) holds the token, the PINs, and every touch; the
agent plans, writes the commands, reads the results, verifies, and records. Most steps are irreversible (a reset, a
`keytocard`, a blocked PIN), so the session runs on four leading ideas:

- **Inventory first:** record what the token holds, read-only, before anything changes it.
- **Backup before destroy:** every secret reaches the password manager, and a read-back proves it, before its local or
  on-card copy goes.
- **Witnessed log:** the operator runs commands inside `script`, and the agent reads the log, so nobody copies output by
  hand and the agent verifies from evidence.
- **Ledger per step:** each finished step lands in the work's plan or record with what was verified.

## The Witnessed Log

Give the operator one copy-pasteable block that opens a recorded shell, runs the step, and closes it. Put the log in
an untracked working folder, such as the task's scratch folder:

```bash
script -q -f -a <work-dir>/<step>.log
<commands>
exit
```

- `-q` hides the start and end banners, `-f` flushes after every write so the log is readable while the operator works,
  and `-a` appends, so one log can collect several runs.

- Prompts with echo off (PINs, passphrases) never reach the log. Anything printed does, so a command inside `script`
  prints only public data: fingerprints, recipients, lengths, `cmp` results, success lines.

- Generate a private key outside `script`, into a file in `$XDG_RUNTIME_DIR` (memory-backed), and `shred -u` it once the
  backup is verified.

- Read the log with terminal escapes stripped:

  ```bash
  sed 's/\x1b\[[0-9;?]*[A-Za-z]//g' LOG | tr -d '\r' | grep -v '^\s*$' | tail -40
  ```

  Filter out any line that could hold a secret before printing it, for example `grep -v 'AGE-SECRET-KEY'`, and check
  afterwards that no secret reached any log with `rg -c` for the secret's prefix.

- When the operator says "done" but a command is missing from the log, run the read-only check yourself rather than
  sending them back.

## Steps

1. **Inventory.** Check with `command -v` that each tool the work needs is installed, and report any that is
   missing. Probe the token read-only and write the result to a tracked record before any change: firmware,
   applets, algorithms and key attributes, PIN and retry counters, resident credentials, free slots, and what each
   public key is registered on. Check public endpoints for registrations (`https://github.com/USER.keys`, `.gpg`,
   `https://api.github.com/users/USER/ssh_signing_keys`). Done when the record holds every parameter a re-creation
   needs. [`references/device-facts.md`](references/device-facts.md) lists the probes per token.
2. **Decide.** Put every open choice to the user with its options and costs (algorithms, expiry, touch and PIN policies,
   where each backup lives, which key is primary, which public keys are published where), and record the decisions in
   the plan before the first irreversible command. Done when no command in the next step depends on an unrecorded
   choice.
3. **Make what a reset destroys.** Revocation certificates, exported public keys, and anything else that only the old
   key can produce come first, backed up and read back.
4. **Run each step as a witnessed log.** One block per step, ending at a natural checkpoint. Name, inside the block's
   instructions, every prompt the operator will see and the answer to give, including "current PIN is the factory
   `123456`" where it applies.
5. **Verify from the log and the stores.** For each secret: read the backup back and compare (`cmp`, fingerprint with
   `ssh-keygen -lf`, an `age` round trip, `gpg --import` in a throwaway keyring). For each public registration: fetch
   the public endpoint. Done when every backup and registration has a check that passed in this session.
6. **Record.** Write the step and what verified it to the work's plan or record, and any surprise to a findings
   note, then commit. Correct an earlier claim the step proved wrong in the same commit and in the
   next reply.
7. **Clean up.** Delete temporary keyrings, key files, and copies once their backups are verified, and archive the plan
   when its steps are done.

## Rules That Held

- Generate a long secret (a PIV management key, a fallback age key) straight into the password manager and pass it by
  command substitution, so nobody types it. A tool that takes a secret only as an argument exposes it briefly in the
  process list; say so and let the user accept it.
- Back up multi-line secrets (key handles, identity files) as file attachments or note bodies. A password field joins
  the lines into one, and the result no longer loads.
- Unplug every other security key during an enrollment: FIDO2 enrollment binds to whichever key the operator touches.
- Test a config's behaviour against the real service before documenting it. `ssh -v` and `ssh -G` show what the config
  does; the config's line order does not.
- Keep the hardware key primary and the password-manager key its fallback by making the choice explicit (see the SSH
  facts), and tell the user what each choice costs in prompts: a `verify-required` key asks for PIN and touch on every
  `git fetch`.
- Treat a commit hook that renders templates as a secret consumer: a template that calls a password-manager function
  must be skipped there, or every commit prompts for authorization.
- When a guard blocks reading a credential-looking path (such as `id_ed25519*`), stop and ask; the operator can run the
  command or lift the guard.

## Device and Tool Facts

[`references/device-facts.md`](references/device-facts.md) holds the per-tool facts this work depends on: GnuPG cards,
FIDO2 SSH keys and `ssh` key selection, `age-plugin-fido2-hmac`, PIV on YubiKey and Nitrokey, password-manager CLIs,
and GitHub key registration. Read the section for each tool before writing its commands.
