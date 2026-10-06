---
name: nix-flakes
description: "Create, change, and debug flake-based Nix projects. Use for flake.nix or flake.lock, adding, updating, or pinning inputs, defining outputs, overlays, or devShells, flake-parts, nix build, develop, run, or profile, flake evaluation errors, or a generated flake manifest such as flake-file.nix. For packaging a derivation use nix-packaging; for NixOS hosts use nixos-config."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Nix Flakes

Change `flake.lock` only through `nix flake update` or `nix flake lock`; a hand edit breaks reproducibility and
causes confusing evaluation failures.

`git add` every new or moved file before evaluating a git-backed flake (`.` or `path:.`). Evaluation copies only
files git tracks, dirty edits included; an untracked or ignored file is invisible, and the error is an "attribute
... missing" at whatever references it, not at the file. When a new file or module does not resolve, run
`git status` before debugging the Nix logic.

## Prerequisites

When a command fails with "experimental Nix feature 'flakes' is disabled", enable the features in
`/etc/nix/nix.conf` or `~/.config/nix/nix.conf`:

```text
experimental-features = nix-command flakes
```

Or set via NixOS configuration:

```nix
nix.settings.experimental-features = [ "nix-command" "flakes" ];
```

## Step 1: Identify Flake Context

Determine from the repository whether this is a new flake or an existing one:

- New flake → `nix flake init` (creates template `flake.nix`)
- Existing flake → read `flake.nix` to understand structure
- Check for `flake-parts` → look for `flake-parts.lib.mkFlake` in outputs
- Check for `import-tree` → look for `inputs.import-tree` (dendritic pattern indicator)
- Check the `flake.nix` header and repository documentation for a generator, source module, or a warning not
  to edit the file directly.

When `flake.nix` or an equivalent input manifest is generated, leave its generated region alone. Read
[references/generated-flake-manifests.md](references/generated-flake-manifests.md), change the authoritative
source module, regenerate, and inspect the complete result. Otherwise, edit `flake.nix` normally.

If the project uses a dendritic-pattern framework (e.g. den), `flake.nix` is a minimal dependency manifest and
all logic lives in `modules/`. Look for a dendritic skill in the configuration repository itself before working
there.

## Step 2: Work with Inputs

### Input types

```nix
inputs = {
  # GitHub (fastest, tarball fetch); append /<branch-or-tag> or ?rev=<commit> to pin
  nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

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

  # Git, GitLab, SourceHut, and a subdirectory
  my-repo.url = "git+https://github.com/owner/repo?ref=main&rev=abc123";
  gitlab-pkg.url = "gitlab:owner/repo";
  sourcehut-pkg.url = "sourcehut:~owner/repo";
  sub-pkg.url = "github:owner/repo?dir=subdir";

  # Tarball (direct URL to archive)
  tarball-pkg.url = "https://example.com/package-1.0.0.tar.gz";

  # Path; a relative one starts with ./
  local-pkg.url = "path:./my-pkg";
};
```

### Key rules

- Use `follows` to share one nixpkgs across inputs that bring their own; it prevents version skew.
- List every input you reference in the `outputs` function signature.
- `flake = false` → input is a plain source path, no flake.nix needed
- Start relative paths with `./`; a bare name is a registry lookup.
- Commit `flake.lock` to git for reproducibility.
- Update one input with `nix flake update <input>`; bare `nix flake update` rewrites every input.

### Unfree packages under pure evaluation

Pure evaluation ignores `NIXPKGS_ALLOW_UNFREE` and `~/.config/nixpkgs/config.nix`. It does **not** ignore
config passed to `nixpkgs` inside the flake, which is the fix in almost every case:

```nix
pkgs = import nixpkgs {
  inherit system;
  config.allowUnfree = true;
};
```

To permit named packages instead of every unfree one (`lib` must be in scope):

```nix
config.allowUnfreePredicate = pkg: builtins.elem (lib.getName pkg) [ "vscode" ];
```

Verified against nixpkgs `c043004` with `nix eval .#devShells.<system>.default.drvPath`:

| Setup                                                        | Pure eval                                           |
| ------------------------------------------------------------ | --------------------------------------------------- |
| `config.allowUnfree` passed to `import nixpkgs` in the flake | Succeeds                                            |
| No config                                                    | Fails: "has an unfree license, refused to evaluate" |
| No config, `NIXPKGS_ALLOW_UNFREE=1`                          | Fails; the variable needs `--impure`                |
| No config, `NIXPKGS_ALLOW_UNFREE=1 --impure`                 | Succeeds, identical `.drv` to the first row         |

Rows one and four produce the same derivation path, so the widely repeated claim that in-flake
`config.allowUnfree` does not apply to `nix develop` is wrong. Reach for `--impure` only when you cannot edit
the flake.

When several inputs each evaluate unfree packages,
[numtide/nixpkgs-unfree](https://github.com/numtide/nixpkgs-unfree) publishes a pre-evaluated nixpkgs with
unfree allowed. Point those inputs at it with `follows` instead of threading config through each one:

```nix
nixpkgs-unfree.url = "github:numtide/nixpkgs-unfree/nixos-unstable";
nixpkgs-unfree.inputs.nixpkgs.follows = "nixpkgs";
proprietary-tool.inputs.nixpkgs.follows = "nixpkgs-unfree";
```

This keeps one nixpkgs revision across the tree, so it does not reintroduce the version skew `follows` exists
to prevent.

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

Use the current names: `packages.<sys>.default` replaces the deprecated `defaultPackage`, and `overlays.default`
replaces `overlay`.

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

`nix run .#name` resolves the binary to run via `meta.mainProgram`. Set it on a package with several binaries;
without it, `nix run` uses the package name as the binary name and may run the wrong one or fail.

```nix
meta = {
  mainProgram = "my-app";
};
```

## Step 4: Run Flake Commands

[references/advanced-commands.md](references/advanced-commands.md) lists the build, run, develop, flake
management, and profile commands, with installable resolution, output selection syntax, and the key flags.

## Step 5: Verify

The work is done when every item holds:

- [ ] `nix flake show` lists the expected outputs.
- [ ] `nix flake check` passes.
- [ ] `nix build .#name` produces the expected output.
- [ ] `flake.lock` is committed.
- [ ] `nix flake metadata` shows one nixpkgs, with `follows` set wherever an input brings its own.
- [ ] No deprecated output names or flags remain.
- [ ] A generated manifest was regenerated from its source and its complete diff was reviewed, when applicable.

For live option, package, and binary-cache lookups, use the `mcp-nixos` server:
[references/mcp-nixos.md](references/mcp-nixos.md).
