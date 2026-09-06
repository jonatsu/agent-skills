---
name: nix-secrets
description: "Nix secrets management with agenix and sops-nix for NixOS and home-manager. Use when setting up secrets, encrypting secret files, configuring agenix or sops-nix, managing age/SSH keys, rekeying, or wiring a secret into a service or user account. Triggers on: agenix, sops-nix, sops, secrets, age encryption, secret file, rekey, age.secrets, sops.secrets, .sops.yaml, hashedPasswordFile, secret management."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Nix Secrets Management

IRON LAW: NEVER use `builtins.readFile` on secret file paths — this copies secret contents into the
world-readable Nix store. ALWAYS reference secrets via `config.age.secrets.<name>.path` or
`config.sops.secrets.<name>.path` so they stay in tmpfs.

> **Using a framework layer on top of flake-parts?** How modules get wired into hosts belongs to that
> framework's own documentation or skills. Secrets are ordinary NixOS/home-manager module options underneath,
> so everything below applies unchanged.

## Workflow

```text
Nix Secrets Progress:

- [ ] Step 1: Choose tool ⚠️ REQUIRED
  - [ ] 1.1 agenix (simpler, SSH keys, one file per secret)?
  - [ ] 1.2 sops-nix (structured files, multiple backends, templates)?
- [ ] Step 2: Generate keys
- [ ] Step 3: Create encrypted secret files
- [ ] Step 4: Wire into config (NixOS and/or home-manager)
- [ ] Step 5: Reference secrets in services
- [ ] Step 6: Verify ⚠️ REQUIRED
```

## Step 1: Choose Tool ⚠️ REQUIRED

### Decision matrix

| Criterion            | agenix                        | sops-nix                               |
| -------------------- | ----------------------------- | -------------------------------------- |
| Simplicity           | Simpler — one file per secret | More complex — structured files        |
| Encryption           | age (SSH keys)                | age, GPG, AWS KMS, GCP KMS, Vault      |
| Secret structure     | One secret per `.age` file    | Multiple secrets per YAML/JSON file    |
| Templates            | No                            | Yes — embed secrets in config files    |
| Eval-time validation | No                            | Yes — checks sops files against config |
| Scalability          | Good for few secrets          | Better for many grouped secrets        |
| Home-manager         | Supported                     | Supported (requires systemd/user)      |

**Recommendation**: Start with agenix. Graduate to sops-nix when one-file-per-secret becomes painful.

**agenix-rekey** (an agenix extension, not a third column): graduate to it when managing many hosts with plain
agenix becomes painful — see [agenix-rekey (When to Graduate)](#agenix-rekey-when-to-graduate).

## Step 2: Generate Keys

### agenix (uses SSH keys)

```bash
# User key — use existing SSH key
cat ~/.ssh/id_ed25519.pub

# Host key — use existing host SSH key
ssh-keyscan <hostname>
# Or fetch from GitHub
curl https://github.com/<username>.keys
```

See [references/agenix-options.md](references/agenix-options.md) for threat model and complete option
reference.

### sops-nix (uses age keys)

```bash
# Generate age keypair
mkdir -p ~/.config/sops/age
age-keygen -o ~/.config/sops/age/keys.txt
age-keygen -y ~/.config/sops/age/keys.txt  # print public key

# Convert existing SSH ed25519 key to age
nix-shell -p ssh-to-age --run "ssh-to-age -private-key -i ~/.ssh/id_ed25519 > ~/.config/sops/age/keys.txt"

# Convert host SSH key to age
nix-shell -p ssh-to-age --run 'ssh-keyscan <hostname> | ssh-to-age'
```

## Step 3: Create Encrypted Secret Files

### agenix

Define recipients in `secrets.nix` (NOT imported into Nix config — just a manifest):

```nix
# secrets.nix
let
  user1 = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI...";
  host1 = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI...";
in
{
  "secret-name.age".publicKeys = [ user1 host1 ];
  "armored-secret.age" = {
    publicKeys = [ user1 host1 ];
    armor = true;  # Base64 PEM for readable diffs
  };
}
```

Create/edit secrets:

```bash
agenix -e secret-name.age       # Opens $EDITOR, encrypts on save
agenix -d secret-name.age       # Decrypt to stdout (for testing/verification)
RULES=custom-secrets.nix agenix -e secret-name.age  # Use custom rules file
```

The `RULES` environment variable overrides the default `secrets.nix` path.

⚠️ REQUIRED: Confirm recipient/key changes before rekeying. `agenix --rekey` rewrites ALL encrypted files (age
uses random nonces — every file gets new ciphertext even if plaintext is unchanged).

```bash
agenix --rekey                  # Re-encrypt all after key changes
```

### sops-nix

Define encryption rules in `.sops.yaml`:

```yaml
keys:
  - &admin_alice age12zlz6lvcdk6eqaewfylg35w0syh58sm7gh53q5vvn7hd7c6nngyseftjxl
  - &host_server age1rgffpespcyjn0d8jglk7km9kfrfhdyev6camd3rck6pn8y47ze4sug23v3

creation_rules:
  - path_regex: secrets/[^/]+\.(yaml|json|env|ini)$
    key_groups:
    - age:
      - *admin_alice
      - *host_server
```

Create/edit secret files:

```bash
nix-shell -p sops --run "sops secrets/example.yaml"
```

⚠️ REQUIRED: Confirm recipient changes before updating keys. `sops updatekeys` re-encrypts the file with all
current recipients from `.sops.yaml`.

```bash
nix-shell -p sops --run "sops updatekeys secrets/example.yaml"
```

Example `secrets/example.yaml`:

```yaml
api-key: <placeholder-replace-with-real-value>
myservice:
  db_password: <placeholder-replace-with-real-value>
```

## agenix-rekey (When to Graduate)

[oddlama/agenix-rekey](https://github.com/oddlama/agenix-rekey) extends agenix for multi-host setups.
Graduate to it when:

- Maintaining `secrets.nix` recipient lists across many hosts becomes painful — agenix-rekey eliminates
  `secrets.nix` by deriving recipients from evaluated host configs. Each secret is encrypted only to master
  identities (`age.secrets.<name>.rekeyFile` replaces `file`); per-host ciphertexts are derived at rekey time,
  lazily and cached.
- You want a hardware-backed (YubiKey/FIDO2 via `age-plugin-yubikey`) or other master age identity in
  `age.rekey.masterIdentities`.
- You need generated secrets — random passwords, SSH keypairs, DH params — declared via
  `age.secrets.<name>.generator.script`.

Verified gotchas before adopting:

- `age.rekey.storageMode` (`"local"` or `"derivation"`) has **no default** — evaluation aborts if unset.
- The per-host key option is `age.rekey.hostPubkey` (singular, set once per host).
- The CLI ships under the `agenix` binary name (`agenix edit|view|rekey|generate`), not `agenix-rekey`.

The option surface shifts between releases; take exact option shapes from the upstream README and module
source, not from cached tables.

## Step 4: Wire into Config

### agenix — NixOS

```nix
# Flake input
inputs.agenix.url = "github:ryantm/agenix";

# In NixOS module
{ config, agenix, ... }: {
  imports = [ agenix.nixosModules.default ];

  age.secrets.secret-name = {
    file = ./secrets/secret-name.age;
    # Optional:
    path = "/custom/path";        # Default: /run/agenix/secret-name
    mode = "0440";
    owner = "serviceuser";
    group = "servicegroup";
    symlink = true;                # false for programs that don't follow symlinks
  };
}
```

### agenix — home-manager

```nix
{ config, agenix, ... }: {
  imports = [ agenix.homeManagerModules.default ];

  age = {
    identityPaths = [ "~/.ssh/id_ed25519" ];
    secrets.example-secret = {
      file = ../secrets/example-secret.age;
    };
  };
}
```

Decryption location: `$XDG_RUNTIME_DIR/agenix`.

See [references/agenix-options.md](references/agenix-options.md) for complete option reference and threat
model.

### sops-nix — NixOS

```nix
# Flake input
inputs.sops-nix.url = "github:Mic92/sops-nix";
inputs.sops-nix.inputs.nixpkgs.follows = "nixpkgs";

# In NixOS module
{ config, sops-nix, ... }: {
  imports = [ sops-nix.nixosModules.sops ];

  sops = {
    defaultSopsFile = ./secrets/example.yaml;
    age.sshKeyPaths = [ "/etc/ssh/ssh_host_ed25519_key" ];
    # OR: age.keyFile = "/var/lib/sops-nix/key.txt";
    # OR: age.generateKey = true;  # Generate if not exists

    secrets.example-key = {};
    secrets."myservice/db_password" = {
      mode = "0440";
      owner = config.users.users.myservice.name;
      restartUnits = [ "myservice.service" ];
      neededForUsers = true;  # Decrypts to /run/secrets-for-users
    };
  };
}
```

### sops-nix — home-manager

```nix
{ config, sops-nix, ... }: {
  imports = [ sops-nix.homeManagerModules.sops ];

  sops = {
    age.keyFile = "${config.home.homeDirectory}/.config/sops/age/keys.txt";
    defaultSopsFile = ./secrets/user.yaml;

    secrets.test = {
      path = "%r/test.txt";  # %r = $XDG_RUNTIME_DIR
    };
  };

  # Services must order after sops-nix.service
  systemd.user.services.mysync.Unit.After = [ "sops-nix.service" ];
}
```

### sops-nix templates (embed secrets in config files)

```nix
{
  sops.secrets.db-password = {};

  sops.templates."myapp.toml" = {
    content = ''
      [database]
      password = "${config.sops.placeholder.db-password}"
    '';
    owner = "myapp";
  };

  systemd.services.myapp = {
    serviceConfig.ExecStart = "${pkgs.myapp}/bin/myapp --config ${config.sops.templates."myapp.toml".path}";
  };
}
```

### sops-nix multiple file formats

```nix
{
  sops.defaultSopsFile = ./secrets.yaml;
  sops.defaultSopsFormat = "yaml";  # or "json", "ini", "dotenv", "binary"

  sops.secrets.github_token = {
    sopsFile = ./other-secrets.json;
    format = "json";
  };
}
```

See [references/sops-nix-options.md](references/sops-nix-options.md) for complete option reference (NixOS,
home-manager, templates).

## Step 5: Reference Secrets in Services

```nix
# CORRECT — reference path, secret stays in tmpfs
services.myservice = {
  enable = true;
  passwordFile = config.age.secrets.secret-name.path;
  # or
  passwordFile = config.sops.secrets.example-key.path;
};

users.users.myuser = {
  isNormalUser = true;
  hashedPasswordFile = config.age.secrets.user-password.path;
};
```

## Step 6: Verify ⚠️ REQUIRED

- [ ] Secrets decrypt at activation (`nixos-rebuild switch` or `home-manager switch` succeeds)
- [ ] Secret files exist at expected paths (`ls /run/agenix/` or `ls /run/secrets/`)
- [ ] No secrets leaked into the Nix store — build the system, then scan its closure:
  `nix build .#nixosConfigurations.<host>.config.system.build.toplevel --print-out-paths --no-link`, then
  `nix path-info -r <that-path> | grep -i secret`
  (matches store path *names* only, not file contents — a clean result is necessary, not sufficient)
- [ ] Services can read secret files (check owner/group/mode)
- [ ] No `builtins.readFile` on secret paths anywhere in config
- [ ] No plaintext secrets in repo
- [ ] Key rotation procedure documented
- [ ] agenix: no password-protected SSH keys in identityPaths
- [ ] sops-nix: `useTmpfs = true` if using impermanence
- [ ] HM agenix: no `owner`/`group` options used (not supported)
- [ ] HM sops-nix: no `restartUnits`/`neededForUsers` used (not supported)

## Anti-Patterns

- Using `builtins.readFile` on secret paths — leaks contents to world-readable Nix store
- Storing plaintext secrets in the repo — always encrypt first
- Forgetting to add host SSH key to recipients — secret won't decrypt on that host
- Using `config.age.secrets.<name>.file` instead of `.path` in service config — `.file` is the encrypted path,
  `.path` is the decrypted path
- Mixing agenix and sops-nix in the same config without clear separation — pick one per module (or per host)
- Forgetting `neededForUsers = true` for user password secrets — they need early decryption
- Putting `.sops.yaml` creation rules with `-` before subsequent key types under `key_groups` — triggers
  Shamir secret sharing
- **Expecting `owner`/`group` on home-manager agenix secrets** — HM agenix has no owner/group options. Secrets
  are owned by the HM user. Use NixOS-level agenix for service-owned secrets.
- **Expecting `restartUnits` on home-manager sops-nix secrets** — HM sops-nix has no restartUnits. Use
  `systemd.user.services.<name>.Unit.After = [ "sops-nix.service" ]` instead.
- **Using password-protected SSH keys with agenix** — ssh-agent cannot decrypt age files with
  password-protected keys. Use unprotected keys or generate age keys directly.
- **Running rekey without confirming recipient changes** — see confirmation gates in Step 3.

## Pre-Delivery Checklist

- [ ] Tool chosen (agenix or sops-nix)
- [ ] Keys generated and distributed to hosts/users
- [ ] Encrypted secret files created and committed
- [ ] Module imported (agenix or sops-nix NixOS/HM module)
- [ ] Secrets referenced via `.path` (not `.file`, not `readFile`)

## Reference Files

- [references/agenix-options.md](references/agenix-options.md) — Complete agenix option reference and threat
  model
- [references/sops-nix-options.md](references/sops-nix-options.md) — Complete sops-nix option reference
  (NixOS, home-manager, templates)
- [references/advanced-patterns.md](references/advanced-patterns.md) — Sharing secrets between services,
  impermanence compatibility, git diff in cleartext
