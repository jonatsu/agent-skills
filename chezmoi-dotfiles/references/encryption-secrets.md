# Encryption and Secrets

## Encryption: age

Recommended.

```bash
age-keygen -o ~/.config/chezmoi/key.txt        # generate key pair
```

`~/.config/chezmoi/chezmoi.toml`:

```toml
encryption = "age"
[age]
  identity = "~/.config/chezmoi/key.txt"
  recipient = "age1..."                         # public key from keygen output
```

## Encryption: GPG

```toml
encryption = "gpg"
[gpg]
  recipient = "you@example.com"
```

## Add Encrypted Files

```bash
chezmoi add --encrypt ~/.ssh/id_rsa
chezmoi add --encrypt ~/.aws/credentials
# Source gets encrypted_ prefix; decrypted transparently on apply
```

## Fail-Fast Secret Detection

Prevent accidental plaintext secrets in source:

```toml
# ~/.config/chezmoi/chezmoi.toml
[add]
  secrets = "error"
```

When `secrets = "error"`, `chezmoi add` scans for high-entropy strings and refuses to commit detected secrets. Resolution paths:
1. Remove the secret from the file — source it at apply time via template function
2. Encrypt the file: `chezmoi add --encrypt <file>`
3. Use a password manager template function (see below)

Never bypass with `secrets = "warn"` or `secrets = "ignore"` in shared repos.

## Password Manager Integration

Use template functions to avoid committing plaintext secrets.

### 1Password

```toml
# ~/.config/chezmoi/chezmoi.toml
[onepassword]
  command = "op"
```

```
export GITHUB_TOKEN='{{ onepasswordRead "op://Personal/github/token" }}'
```

### Bitwarden

```
export API_KEY='{{ (bitwarden "item" "api-credentials").login.password }}'
```

### pass

```
export SECRET='{{ pass "path/to/secret" }}'
```

### Generic CLI output

```
export TOKEN='{{ output "my-secret-cli" "get" "token" | trim }}'
```
