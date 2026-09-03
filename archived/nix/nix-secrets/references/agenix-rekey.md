# agenix-rekey Reference

Extension for agenix that eliminates `secrets.nix`, adds master-key encryption, lazy cached rekeying, and
secret generators.

## Installation

```nix
# flake.nix
inputs.agenix.url = "github:ryantm/agenix";
inputs.agenix-rekey.url = "github:oddlama/agenix-rekey";
inputs.agenix-rekey.inputs.agenix.follows = "agenix";
```

```nix
# NixOS module
{ inputs, ... }: {
  imports = [ inputs.agenix-rekey.nixosModules.default ];
}
```

## Options

### age.rekey (top-level)

| Option                | Type                   | Default                       | Description                                                                |
| --------------------- | ---------------------- | ----------------------------- | -------------------------------------------------------------------------- |
| `masterIdentities`    | `listOf (str \| path)` | `[]`                          | Master key identities (age public key, path to age key, or YubiKey plugin) |
| `hostIdentities`      | `listOf str`           | `[]`                          | Host public SSH/age keys for rekeying                                      |
| `pubkey`              | `str`                  | auto                          | This host's public key (auto from `hostIdentities`)                        |
| `masterKeyPath`       | `path`                 | `~/.config/sops/age/keys.txt` | Path to master key file                                                    |
| `storageMode`         | `str`                  | `"local"`                     | `"local"` (in-repo) or `"derivation"` (Nix store)                          |
| `generatedSecretsDir` | `path`                 | `./secrets/generated`         | Directory for generated secrets                                            |

### age.secrets.\<name> (per-secret)

| Option                | Type    | Default  | Description                                                                       |
| --------------------- | ------- | -------- | --------------------------------------------------------------------------------- |
| `rekeyFile`           | `path`  | `null`   | Path to secret encrypted with master key (replaces `file` when using rekey)       |
| `generator`           | `attrs` | `null`   | Generator definition (see below)                                                  |
| `generator.generator` | `str`   | required | Generator type: `alnum`, `base64`, `hex`, `passphrase`, `dhparams`, `ssh-ed25519` |
| `generator.length`    | `int`   | `32`     | Length for string generators                                                      |
| `generator.name`      | `str`   | `null`   | Name for key-type generators                                                      |
| `generator.cacheDir`  | `path`  | auto     | Cache directory for generated secrets                                             |

## Generators

| Generator     | Output              | Use Case                          |
| ------------- | ------------------- | --------------------------------- |
| `alnum`       | Alphanumeric string | Random passwords                  |
| `base64`      | Base64 string       | API keys, tokens                  |
| `hex`         | Hex string          | Hex-encoded secrets               |
| `passphrase`  | Diceware passphrase | Human-readable passwords          |
| `dhparams`    | DH parameters       | TLS/SSL DH params                 |
| `ssh-ed25519` | SSH keypair         | Host SSH keys                     |
| Custom        | User-defined        | Implement `generator` as function |

## Storage Modes

- **`local`** (default): Secrets stored in-repo under `generatedSecretsDir`. Committed to git.
- **`derivation`**: Secrets stored in Nix store. Not committed. Rebuilt on demand.

## CLI Commands

```bash
agenix edit <name>.age          # Edit secret (encrypts with master key)
agenix view <name>.age          # View decrypted content
agenix rekey -a                 # Rekey all secrets for all hosts
agenix rekey -- <host>          # Rekey for specific host only
agenix generate                 # Generate all generated secrets
agenix generate <name>          # Generate specific secret
```

## Comparison: agenix vs agenix-rekey

| Feature       | agenix                               | agenix-rekey                          |
| ------------- | ------------------------------------ | ------------------------------------- |
| `secrets.nix` | Manual per-secret recipient mapping  | Eliminated — `hostIdentities` on host |
| Master key    | Each secret encrypted per-host       | Single master key, auto-rekey         |
| Generators    | None                                 | Built-in + custom                     |
| Rekeying      | `agenix --rekey` (all files, always) | Lazy, cached, only when changed       |
| Bootstrapping | Need host key first                  | Dummy pubkey, rekey later             |
| YubiKey       | Not supported                        | Supported via `age-plugin-yubikey`    |
