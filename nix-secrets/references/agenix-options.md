# agenix Option Reference

## Threat Model

- age encryption provides **confidentiality** but NOT authentication — there is no MAC (message authentication code). A malicious party with write access to the repo could replace encrypted secrets.
- agenix is NOT audited — use at your own risk for sensitive infrastructure.
- Password-protected SSH keys do NOT work with ssh-agent for agenix decryption. Use unprotected keys or age keys directly.
- Rekeying changes ALL encrypted files (age uses random nonces) — every `.age` file gets new ciphertext even if the plaintext is unchanged.

## NixOS Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `age.secrets.<name>.file` | `path` | required | Path to encrypted `.age` file |
| `age.secrets.<name>.path` | `str` | `/run/agenix/<name>` | Decrypted output path (readOnly) |
| `age.secrets.<name>.name` | `str` | `<name>` | Filename after decryption |
| `age.secrets.<name>.mode` | `str` | `0400` | File permissions |
| `age.secrets.<name>.owner` | `str` | `root` | File owner |
| `age.secrets.<name>.group` | `str` | `root` | File group |
| `age.secrets.<name>.symlink` | `bool` | `true` | Symlink vs copy to tmpfs |
| `age.ageBin` | `str` | `age` | Path to age binary |
| `age.secretsMountPoint` | `str` | `/run/agenix.d` | Mount point for secrets |
| `age.secretsDir` | `str` | `/run/agenix` | Directory for decrypted secrets |
| `age.identityPaths` | `listOf path` | `[/etc/ssh/ssh_host_ed25519_key]` | Paths to identity keys |

## home-manager Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `age.secrets.<name>.file` | `path` | required | Path to encrypted `.age` file |
| `age.secrets.<name>.path` | `str` | `$XDG_RUNTIME_DIR/agenix/<name>` | Decrypted output path (readOnly) |
| `age.secrets.<name>.name` | `str` | `<name>` | Filename after decryption |
| `age.secrets.<name>.mode` | `str` | `0400` | File permissions |
| `age.identityPaths` | `listOf path` | required | Paths to identity keys |
| `age.package` | `package` | `pkgs.age` | age package to use |

**CRITICAL: home-manager agenix has NO `owner` or `group` options.** Secrets are owned by the user running home-manager. If a service needs different ownership, use NixOS-level agenix instead.

**HM secretsDir defaults:**
- Linux: `$XDG_RUNTIME_DIR/agenix`
- Darwin: `$(getconf DARWIN_USER_TEMP_DIR)/agenix`
