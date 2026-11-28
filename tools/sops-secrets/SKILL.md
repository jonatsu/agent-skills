---
name: sops-secrets
description: Manage a repository's encrypted secrets with SOPS, mostly with age keys. Use to set up .sops.yaml creation rules; to create, edit, read, or run a command with encrypted YAML, JSON, dotenv, INI, or binary files; to add or remove who can decrypt and rotate data keys; and for sops diffs, merge conflicts, and CI. Not for age outside SOPS (age-encryption) or sops-nix modules (nix-secrets).
license: MIT
compatibility: Needs sops 3.9 or later for the subcommands used here. Plugin identities, such as a hardware key, need their age-plugin binary on PATH.
metadata:
  author: Joonas Onatsu
---

# SOPS Secrets

SOPS encrypts each value of a structured file and leaves the key names and structure readable, so an encrypted file
still diffs and reviews as text. Each file has its own data key, wrapped once for every recipient that may decrypt it.
This skill uses age recipients; cloud KMS, PGP, and Vault keys sit in the same `.sops.yaml` slots.

Current known: sops 3.13.3 and age 1.3.2, checked 2026-11-28 with `sops --help` and runs against synthetic keys.

## Keep Plaintext Out of the Transcript

Everything a command prints lands in the transcript, which is not a secret store. Show the user no decrypted value,
and print none unless the user asks for that one value.

- Check access with the output discarded: `sops decrypt secrets/app.yaml >/dev/null && echo ok`.
- Read the file's shape from the encrypted file itself, because key names stay plaintext:
  `jq 'del(.sops) | keys' secrets/app.json`.
- Answer a question about a value with a filter that prints only the answer:
  `sops decrypt secrets/app.yaml | yq '.db | has("password")'`.
- Write a value through stdin, as JSON, so it never appears in a process listing:
  `openssl rand -hex 32 | tr -d '\n' | jq -Rs . | sops set --value-stdin secrets/app.yaml '["db"]["password"]'`.
- Run a consumer with `sops exec-env --pristine secrets/app.env './deploy'`. Without `--pristine` the child inherits
  your whole environment, including `SOPS_AGE_KEY` and `SOPS_AGE_KEY_FILE`. With it, the child gets only the file's
  values, so pass any other variable it needs inline.
- Give a tool a config file with `sops exec-file secrets/app.yaml 'tool --config {}'`. It hands over a named pipe, so
  the plaintext never reaches the disk.

When plaintext must sit on disk, write it outside the repository and delete it afterwards. `--output` overwrites
without asking and creates the file with the umask's mode, usually 0644, so set `umask 077` first. Then check that
`git status` shows no new file.

## Set Up a Repository

1. Give each person, host, and CI job its own age key, and put only the public keys in `.sops.yaml`. Generate a key
   with `age-keygen -o ~/.config/sops/age/keys.txt`, which creates the file mode 0600 and refuses to overwrite one.
   For post-quantum keys, SSH keys, or hardware keys, use the `age-encryption` skill.

2. Write `.sops.yaml` at the repository root, with the most specific rule first:

   ```yaml
   creation_rules:
     - path_regex: ^secrets/prod/
       age: age1ops...,age1ciprod...
     - path_regex: ^secrets/
       age: age1ops...,age1dev...,age1ci...
   ```

   sops finds `.sops.yaml` by searching upward from the working directory, so run it from inside the repository.
   The first rule whose `path_regex` matches wins. The regex is unanchored RE2, matched against the path relative to
   the directory holding `.sops.yaml`, so anchor it with `^` and `$`.

3. Add `encrypted_regex` to a rule whose files have fields that must stay plaintext, such as a Kubernetes Secret:
   `encrypted_regex: ^(data|stringData)$`. A rule takes at most one such selector. Anchor this regex too, because
   it matches any key containing the pattern and encrypts everything below a match.

4. Create each file with `sops edit secrets/app.yaml`, or encrypt an existing one with `sops encrypt -i <file>`.

5. Confirm before committing that every secrets file prints `{"encrypted":true}` from `sops filestatus <file>`.

Setup is done when every secrets file is encrypted and each holder you can test decrypts the files their rule names.

Keep these rules in mind afterwards:

- A file stores its selector settings when it is created. Changing `.sops.yaml` later changes only recipients, and
  only through `updatekeys`.
- A key added later with `sops set` stays plaintext when the file's stored `encrypted_regex` does not match it.
- Leave out `--age` and `SOPS_AGE_RECIPIENTS`. When a rule matches, either one silently replaces that rule's
  recipients. When none matches, sops fails with `no matching creation rules found`.
- Keep every recipient of a file classic or every one post-quantum. sops accepts a mix, and the file is then
  only as strong as its classic recipient.
- Use more than one entry under `key_groups` only when the user asks for Shamir secret sharing, because decryption
  then needs a key from every group.
- Put secrets in values only. Key names, structure, value types, recipients, and the change time stay readable, and
  Git history shows which keys changed.

## Daily Operations

- Edit interactively with `sops edit <file>`. It decrypts to a temporary file only you can read, runs `SOPS_EDITOR` or
  `EDITOR`, and re-encrypts when the editor exits. A GUI editor needs its wait flag, such as `code --wait`.
- Change a file non-interactively with `sops set` and `sops unset` instead of `edit`. After an editor saves text that
  does not parse, `edit` waits for a key press and reopens the editor. The index is a path such as
  `'["db"]["password"]'`, the value is JSON, and `set` works only on a file that is already encrypted.
- Hand one value to a consumer with `sops decrypt --extract '["db"]["password"]' <file>`, which prints a string raw.
- Put every flag after the subcommand. `sops --output out.yaml decrypt f.yaml` ignores `--output`, prints the
  plaintext, and exits 0.
- Keep each file's extension, because sops picks the format from it. Pass `--input-type` for a renamed file, and
  `--filename-override` to encrypt from stdin.
- Leave `--ignore-mac` out of routine use. A `MAC mismatch` (exit 51) means the file was edited by hand or merged as
  text; recover it as [references/git-and-ci.md](references/git-and-ci.md) describes.

## Change Who Can Decrypt

Confirm each recipient change with the user first. Both commands below need a key that decrypts the file now.

- **Add** the public key to the rule in `.sops.yaml`, then run `sops updatekeys -y <file>...`. The data key stays
  the same.

- **Remove** a holder in this order:

  1. Delete their public key from the rule in `.sops.yaml`.
  2. Run `sops updatekeys -y <file>...`.
  3. Run `sops rotate -i <file>` on each file, which replaces the data key and re-encrypts every value.
  4. Commit.
  5. Replace the real passwords, tokens, and keys inside the files, and commit again.

  The removed holder can still decrypt every older version in Git history and any copy they kept, so step 5 is the
  only revocation. Removal is done when no rule names the key, every file is rotated, and every secret they could read
  is replaced or listed for the user to replace.

Keep a backup recipient in every rule, such as an offline key or a second hardware key. A file whose only key is lost
cannot be recovered.

## Git and CI

Read [references/git-and-ci.md](references/git-and-ci.md) before you set up a diff driver, resolve a merge conflict in
an encrypted file, add a hook that rejects plaintext, or give CI a key.
