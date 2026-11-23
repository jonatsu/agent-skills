---
name: hardware-security-keys
description: Explain and set up hardware security keys such as a YubiKey, Nitrokey, or OnlyKey, covering what their FIDO2, U2F, OpenPGP, PIV, OTP, and hmac-secret functions are for and how to provision, reset, back up, and verify the keys they hold. Use when someone asks what a hardware key can do or which function to use for something, wants a token set up for web sign-in, SSH, Git signing, encryption, disk unlock, or sudo, or is resetting, re-provisioning, backing up, or registering a token's keys. Not for software-only keys, or for encrypted secrets files such as sops (nix-secrets).
license: MIT
compatibility: Linux. Needs the user present with the token; uses gpg, ssh-keygen, script, and the token's vendor CLI.
metadata:
  author: Joonas Onatsu
---

# Hardware Security Keys

Most hardware security keys expose the same functions: FIDO2 and U2F, an OpenPGP card, PIV, OATH codes, keyboard
slots, and `hmac-secret`. This skill explains what each is for, recommends uses, and runs the setup with the user at
the keyboard. Commands and paths are for Linux.

## Choose the Branch

- **Explain and advise** when the person asks what their key can do, what a function is for, or how to use it for
  something. Follow [Explain and Advise](#explain-and-advise).
- **Set up and maintain** when they want a function configured, a token reset or re-provisioned, a backup made, or
  public keys registered. Follow [Set Up and Maintain](#set-up-and-maintain).

An advice session often ends in a setup. Switch branches only when the person approves the plan.

## Know the Token

Read the token's device file before saying what it can do, because tokens differ in which functions they have and in
what form. Each file answers the same questions in the same order: capabilities, inventory, PINs and resets, firmware,
backup, and Linux specifics.

- YubiKey: [references/yubikey.md](references/yubikey.md)
- Nitrokey 3: [references/nitrokey-3.md](references/nitrokey-3.md)
- OnlyKey: [references/onlykey.md](references/onlykey.md)

For a token with no file, read its vendor's documentation and tool help before offering any step, and tell the person
which facts are unverified until the inventory confirms them. Host-side facts that hold for every token (GnuPG, `ssh`
key selection, age, password-manager CLIs, GitHub registration) are in [references/tools.md](references/tools.md).

## Explain and Advise

1. Find out which token or tokens the person has, and read their device files.
2. Explain each function they ask about in plain words: what it does, what it protects against, and what it costs in
   storage, prompts, and recovery. [references/use-cases.md](references/use-cases.md) has the explanation and the uses
   of each function.
3. Ask what they actually do: web accounts, SSH servers, a Git host, encrypted mail or files, disk encryption, `sudo`.
4. Recommend a setup from the default in `use-cases.md`, adjusted to their answers and to what their token supports.
   Give each recommendation its gain and its trap, and say plainly when a function is not worth setting up for them.

Done when every function they asked about is explained, and each recommendation names the token function it uses and
the recovery path if the token is lost.

## Set Up and Maintain

Hardware-key work splits into two hands. The **operator** (the user) holds the token, the PINs, and every touch; the
agent plans, writes the commands, reads the results, verifies, and records. Most steps are irreversible (a reset, a
`keytocard`, a blocked PIN), so the work runs on four leading ideas:

- **Inventory first:** record what the token holds, read-only, before anything changes it.
- **Backup before destroy:** every secret reaches the password manager, and a read-back proves it, before its local or
  on-card copy goes.
- **Witnessed log:** the operator runs commands inside `script`, and the agent reads the log, so nobody copies output by
  hand and the agent verifies from evidence.
- **Ledger per step:** each finished step lands in the work's plan or record with what was verified.

### The Witnessed Log

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

- Write every file a retry may rewrite with `>|`. Many shells set `noclobber`, and then a rerun after a cancelled
  prompt fails with "cannot overwrite existing file" and keeps the old file.

- When the operator says "done" but a command is missing from the log, run the read-only check yourself rather than
  sending them back.

### Steps

1. **Inventory.** Check with `command -v` that each tool the work needs is installed, and report any that is
   missing. Probe the token read-only with the commands in its device file, and write the result to a tracked record
   before any change: firmware, functions, algorithms and key attributes, PIN and retry counters, resident
   credentials, free slots, and what each public key is registered on. Check registrations at the public endpoints
   listed in `tools.md`. Done when the record holds every parameter a re-creation needs.
2. **Decide.** Put every open choice to the user with its options and costs (algorithms, expiry, touch and PIN policies,
   where each backup lives, which key is primary, which public keys are published where), and record the decisions in
   the plan before the first irreversible command. Done when no command in the next step depends on an unrecorded
   choice.
3. **Make what a reset destroys.** Revocation certificates, exported public keys, and anything else that only the old
   key can produce come first, backed up and read back.
4. **Run each step as a witnessed log.** One block per step, ending at a natural checkpoint. Name, inside the block's
   instructions, every prompt the operator will see and the answer to give, including "current PIN is the factory
   `123456`" where it applies. For a token that types its output, name the window to focus. Give every step as a
   command, never as a comment the operator must act on, and check its effect in the next block. For an OpenPGP card,
   follow [references/openpgp-card.md](references/openpgp-card.md).
5. **Verify from the log and the stores.** For each secret: read the backup back and compare (`cmp`, fingerprint with
   `ssh-keygen -lf`, an `age` round trip, `gpg --import` in a throwaway keyring). For each public registration: fetch
   the public endpoint. List each password-manager item's field names and compare them with what the record says it
   holds. Done when every backup and registration has a check that passed in this session.
6. **Record.** Write the step and what verified it to the work's plan or record, and any surprise to a findings
   note, then commit. Correct an earlier claim the step proved wrong in the same commit and in the next reply.
7. **Clean up.** Delete temporary keyrings, key files, and copies once their backups are verified, and archive the plan
   when its steps are done.

### Traps That Change a Setup

Each of these holds on every token that has the function; the device file adds the token's own.

- **No export.** FIDO2 credentials, OATH secrets, and keys generated on a card or in a PIV slot cannot be copied off.
  Their backup is a second token enrolled separately, or a key generated off the token and kept in the password manager
  before it is moved on.
- **A FIDO reset destroys more than credentials.** It replaces the token's secret, which ends every passkey, every SSH
  key, and every `hmac-secret` identity (age, disk unlock). Re-enroll or recover each one before resetting.
- **Separate PINs.** FIDO2, OpenPGP, PIV, and the device itself (where one exists) each keep their own PIN and retry
  counter. Say which PIN each prompt wants.
- **Choices fixed at creation.** PIV PIN and touch policies, `verify-required` on an SSH key, and the PIN answer for an
  `hmac-secret` identity cannot change later without a new key.
- **Two tokens.** Recommend a second token for anything the person cannot afford to lose, and enroll both in the same
  session.

### Rules That Held

- Generate a long secret (a PIV management key, a fallback age key) straight into the password manager and pass it by
  command substitution, so nobody types it. A tool that takes a secret only as an argument exposes it briefly in the
  process list; say so and let the user accept it.
- Back up multi-line secrets (key handles, identity files, typed backups) as file attachments or note bodies. A
  password field joins the lines into one, and the result no longer loads.
- Unplug every other security key during an enrollment: FIDO2 enrollment binds to whichever key the operator touches.
- Test a config's behaviour against the real service before documenting it. `ssh -v` and `ssh -G` show what the config
  does; the config's line order does not.
- Keep the hardware key primary and the password-manager key its fallback by making the choice explicit (see
  `tools.md`), and tell the user what each choice costs in prompts: a `verify-required` key asks for PIN and touch on
  every `git fetch`.
- Treat a commit hook that renders templates as a secret consumer: a template that calls a password-manager function
  must be skipped there, or every commit prompts for authorization.
- When a guard blocks reading a credential-looking path (such as `id_ed25519*`), stop and ask; the operator can run the
  command or lift the guard.
