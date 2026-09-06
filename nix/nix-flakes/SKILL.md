---
name: nix-flakes
description: "Nix Flakes foundational reference for creating, managing, and debugging flake-based Nix configurations. Use when creating a flake, adding inputs, managing flake.lock, using nix build/develop/run/profile, setting up devShells, configuring flake outputs, or troubleshooting flake evaluation. Triggers on: flake.nix, flake.lock, nix build, nix develop, nix flake, flake-parts, inputs, outputs, devShell, nixpkgs, overlays, nix profile."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Nix Flakes

IRON LAW: NEVER edit `flake.lock` by hand. Use `nix flake update` or `nix flake lock`. Manual edits break
reproducibility and cause silent evaluation failures.

IRON LAW 2: New or moved files MUST be `git add`ed (or already tracked) before any flake evaluation can see
them. `nix build`/`nix eval`/`nix flake check` against a git-backed flake (`.`/`path:.`) copy only files git
knows about: tracked files are visible — including unstaged, dirty edits — but untracked and ignored files
are silently invisible. No error at the file itself, just a confusing "attribute ... missing" error at
whatever *references* it. If a brand-new file/module isn't resolving, run `git status` before debugging the
Nix logic.

## Prerequisites

Flakes require experimental features enabled. Add to `/etc/nix/nix.conf` or `~/.config/nix/nix.conf`:

```
experimental-features = nix-command flakes
```

Or set via NixOS configuration:

```nix
nix.settings.experimental-features = [ "nix-command" "flakes" ];
```

Without this, all `nix flake *` and `nix build .#` commands fail with "error: experimental Nix feature
'flakes' is disabled".

## Workflow

```text
Nix Flakes Progress:

- [ ] Step 1: Identify flake context ⚠️ REQUIRED
  - [ ] 1.1 Does a flake.nix already exist?
  - [ ] 1.2 Is this a new flake or modifying existing?
  - [ ] 1.3 Does the project use flake-parts? (check for mkFlake)
- [ ] Step 2: Work with inputs
- [ ] Step 3: Work with outputs
- [ ] Step 4: Run flake commands
- [ ] Step 5: Verify ⚠️ REQUIRED
```

## Step 1: Identify Flake Context ⚠️ REQUIRED

Ask: Is this a new flake or an existing one?

- New flake → `nix flake init` (creates template `flake.nix`)
- Existing flake → read `flake.nix` to understand structure
- Check for `flake-parts` → look for `flake-parts.lib.mkFlake` in outputs
- Check for `import-tree` → look for `inputs.import-tree` (dendritic pattern indicator)

If the project uses a dendritic-pattern framework (e.g. den), `flake.nix` is a minimal dependency manifest and
all logic lives in `modules/`. Look for a dendritic skill in the configuration repository itself before working
there.

## Step 2: Work with Inputs

### Input types

```nix
inputs = {
  # GitHub (fastest, tarball fetch)
  nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  # Specific branch/tag/rev
  flake-parts.url = "github:hercules-ci/flake-parts";

  # Non-flake source (raw source tree)
  some-source = {
    url = "github:owner/repo";
    flake = false;
  };

  # Follow another input's nixpkgs (deduplication)
  home-manager = {
    url = "github:nix-community/home-manager";
    inputs.nixpkgs.follows = "nixpkgs";
  };

  # Git
  my-repo.url = "git+https://github.com/owner/repo?ref=main&rev=abc123";

  # Path (relative MUST start with ./)
  local-pkg.url = "path:./my-pkg";
};
```

### Key rules

- MUST use `follows` to deduplicate nixpkgs across inputs — prevents version skew
- MUST list every input in the `outputs` function signature that you reference
- `flake = false` → input is a plain source path, no flake.nix needed
- Relative paths MUST start with `./` — bare names are registry lookups
- Commit `flake.lock` to git for reproducibility

### Additional flake reference types

```nix
inputs = {
  # SourceHut
  sourcehut-pkg.url = "sourcehut:~owner/repo";

  # GitLab
  gitlab-pkg.url = "gitlab:owner/repo";

  # Tarball (direct URL to archive)
  tarball-pkg.url = "https://example.com/package-1.0.0.tar.gz";

  # Indirect (registry lookup)
  nixpkgs.url = "nixpkgs/nixos-unstable";

  # Path with subpath
  sub-pkg = {
    url = "github:owner/repo?dir=subdir";
  };
};
```

### nixConfig attribute

Set Nix settings scoped to the flake. Any `nix.conf` option may appear here, but application is two-tier
(see below):

```nix
{
  nixConfig = {
    bash-prompt = "\\[\\e[0m\\e[32m\\]nix-develop\\[\\e[0m\\] ";
    extra-substituters = [ "https://cache.example.org" ];
    extra-trusted-public-keys = [ "cache.example.org-1:..." ];
  };
}
```

**Auto-applied keys** (the only ones Nix honors without confirmation, per `src/libflake/config.cc`):
`bash-prompt`, `bash-prompt-prefix`, `bash-prompt-suffix`, `flake-registry`, `commit-lock-file-summary`.

**Every other key** (`substituters`, `extra-trusted-public-keys`, `max-jobs`, ...) is applied only with
`--accept-flake-config`, or after interactive per-value confirmation (accepted values are persisted in
`trusted-settings.json`). In the example above, only `bash-prompt` takes effect without acceptance.

## Step 3: Work with Outputs

### Standard flake outputs

```nix
outputs = { self, nixpkgs, ... }@inputs: {
  # System-keyed outputs
  packages.x86_64-linux.default = ...;
  devShells.x86_64-linux.default = ...;
  apps.x86_64-linux.default = { type = "app"; program = "..."; };

  # Non-system-keyed
  nixosConfigurations.my-host = nixpkgs.lib.nixosSystem { ... };
  homeConfigurations.my-user = ...;
  overlays.default = final: prev: { ... };
  templates.default = { path = ./template; description = "..."; };
  checks.x86_64-linux.test-name = ...;
};
```

### flake-parts outputs

```nix
outputs = inputs@{ flake-parts, ... }:
  flake-parts.lib.mkFlake { inherit inputs; } {
    systems = [ "x86_64-linux" "aarch64-linux" ];

    perSystem = { config, pkgs, ... }: {
      packages.default = pkgs.hello;
      devShells.default = pkgs.mkShell { buildInputs = [ pkgs.git ]; };
    };

    flake = {
      nixosConfigurations.my-host = nixpkgs.lib.nixosSystem { ... };
    };
  };
```

### Output reference table

| Output                        | Used by                  | Structure                          |
| ----------------------------- | ------------------------ | ---------------------------------- |
| `packages.<sys>.<name>`       | `nix build`              | Derivation                         |
| `devShells.<sys>.<name>`      | `nix develop`            | Derivation                         |
| `apps.<sys>.<name>`           | `nix run`                | `{ type, program }`                |
| `nixosConfigurations.<name>`  | `nixos-rebuild`          | `nixosSystem { ... }`              |
| `homeConfigurations.<name>`   | `home-manager`           | `homeManagerConfiguration { ... }` |
| `overlays.default`            | nixpkgs overlay          | `final: prev: { ... }`             |
| `checks.<sys>.<name>`         | `nix flake check`        | Derivation                         |
| `formatter.<sys>`             | `nix fmt`                | Formatter derivation               |
| `templates.<name>`            | `nix flake init`         | `{ path, description }`            |
| `legacyPackages.<sys>`        | `nixpkgs.legacyPackages` | Pre-flake compatibility            |
| `hydraJobs.<sys>`             | Hydra CI                 | Build jobs for Hydra               |
| `nixosModules.<name>`         | NixOS module import      | Reusable NixOS module              |
| `homeManagerModules.<name>`   | home-manager import      | Reusable HM module                 |
| `bundlers.<sys>.<name>`       | `nix bundle`             | Bundle into portable format        |
| `darwinConfigurations.<name>` | nix-darwin               | macOS system config                |
| `darwinModules.<name>`        | nix-darwin module        | Reusable darwin module             |

### meta.mainProgram

`nix run .#name` resolves the binary to run via `meta.mainProgram`. If a package has multiple binaries, set
this to avoid ambiguity:

```nix
meta = {
  mainProgram = "my-app";
};
```

Without `meta.mainProgram`, `nix run .#default` uses the package name as the binary name.

## Step 4: Run Flake Commands

### Build & run

```bash
nix build .#name              # Build specific output
nix build .                   # Build default package
nix run .#name -- args        # Run app with args
nix develop .#name            # Enter named devShell
nix develop -c command args   # Run command in dev env
```

### Flake management

```bash
nix flake init                # Create flake.nix from template
nix flake show                # List all outputs
nix flake check               # Evaluate + run checks
nix flake metadata            # Show lock info
nix flake update              # Update ALL inputs (rewrite lock)
nix flake update nixpkgs      # Update specific input only
nix flake lock                # Create lock, never update existing
```

### Profile management

```bash
nix profile install nixpkgs#hello
nix profile list
nix profile remove hello
nix profile upgrade
nix profile rollback
```

### Key flags

| Flag                        | Effect                           |
| --------------------------- | -------------------------------- |
| `--impure`                  | Allow mutable paths, `$NIX_PATH` |
| `--override-input path url` | Override input at eval time      |
| `--no-write-lock-file`      | Don't write lock                 |
| `--commit-lock-file`        | Auto-commit lock changes         |
| `-L`                        | Show full build output           |

### Advanced Commands

See [references/advanced-commands.md](references/advanced-commands.md) for:
`nix flake prefetch/archive/clone`, `nix profile history/diff-closures/wipe-history`, `nix develop` phase
shortcuts, installable resolution, output selection syntax, and additional key flags.

## Step 5: Verify ⚠️ REQUIRED

- [ ] `nix flake show` lists expected outputs
- [ ] `nix flake check` passes without errors
- [ ] `nix build .#name` produces expected output
- [ ] `flake.lock` committed to git
- [ ] No duplicate nixpkgs versions (check `nix flake metadata`)

## Anti-Patterns

- Editing `flake.lock` by hand — breaks reproducibility
- Omitting `follows` on inputs with their own nixpkgs — causes version skew
- Using bare names instead of `./` for relative paths — treated as registry lookups
- Putting logic in `flake.nix` when using dendritic pattern — all logic belongs in `modules/`
- Using `defaultPackage` (deprecated) instead of `packages.<sys>.default`
- Forgetting to add new inputs to `outputs` function signature
- Running `nix flake update` when you only need one input updated — use `nix flake update <input>`
- **Mixing `nix profile` and `nix-env`** — incompatible internal formats, pick one.
- **Forgetting `experimental-features`** — all flake commands fail without `nix-command flakes` enabled.
- **Using deprecated `--recreate-lock-file` or `--update-input`** — replaced by `nix flake update` and
  `nix flake update <input>`.
- **Not setting `meta.mainProgram` for multi-binary packages** — `nix run` may fail or run the wrong binary.
- **Debugging a "missing attribute" eval error by rewriting Nix logic before checking `git status`** — an
  untracked new file is invisible to flake evaluation and produces exactly this symptom.

## Recommended Tools

### mcp-nixos

MCP server for real-time NixOS ecosystem queries. See [references/mcp-nixos.md](references/mcp-nixos.md) for
installation and usage examples.

## Pre-Delivery Checklist

- [ ] `flake.nix` has valid syntax (`nix flake show` succeeds)
- [ ] All inputs have `follows` where applicable
- [ ] `flake.lock` is committed
- [ ] `nix flake check` passes
- [ ] No deprecated output attributes (`defaultPackage`, `overlay`)
- [ ] `experimental-features` includes `nix-command flakes`
- [ ] `meta.mainProgram` set for packages with multiple binaries
- [ ] No deprecated flags (`--recreate-lock-file`, `--update-input`, `defaultPackage`)
