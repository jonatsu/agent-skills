---
name: nix-wrapper-modules
description: "Create portable wrapped executables with BirdeeHub's nix-wrapper-modules — express a program's flags, env, prefix/suffix, and generated config as a nixpkgs module instead of makeWrapper/symlinkJoin/writeShellScriptBin, then install the resulting derivation across NixOS, home-manager, nix-darwin, flake-parts, devshells, or bare shells. Use when wrapping a tool with baked-in config/flags/env, generating a program's config file from Nix, exposing multiple wrapped binaries, or building a reusable configured-binary module. Triggers on: nix-wrapper-modules, wrappers.wrap, wlib, wrapPackage, evalPackage, evalModule, wrapped executable, configured binary, wrap a program, makeWrapper alternative, symlinkJoin wrapper, subWrapperModuleWith, constructFiles, wrapper backend, wrapperImplementation."
license: MIT
metadata:
  author: Joonas Onatsu
---

# nix-wrapper-modules

IRON LAW: Drive the wrapper THROUGH the module system — `settings` → `constructFiles` → `env`/`flags`. NEVER
hand-roll a `makeWrapper`/`symlinkJoin`/`writeShellScriptBin` bypass for "just one flag" (it throws away the
module's compose/override/desktop-file correctness), and NEVER render a generated config file with a bare
`pkgs.writeText`: use `constructFiles.<name>`, or `${placeholder "out"}`-style paths resolve against the wrong
derivation and silently break at runtime.

Upstream: <https://github.com/BirdeeHub/nix-wrapper-modules> · docs
<https://birdeehub.github.io/nix-wrapper-modules>. Pre-1.0, no tagged releases — pin by commit and treat
recalled option shapes as untrusted (verify against the docs or `references/api-reference.md`).

## When this is the right tool

A "wrapped executable" here is a derivation that re-exposes a package's **full** output (man pages, desktop
files, `/share`, sibling binaries) and rewraps its binary with flags/env/config expressed as a NixOS-style
module (`options`/`config`).

| Situation                                                                                    | Use                                                                            |
| -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Bake flags/env/config into a tool AND keep composability, `.override`, correct desktop files | **nix-wrapper-modules**                                                        |
| Add one env var / PATH entry to a single binary, no config generation                        | `makeWrapper` + `symlinkJoin` (lighter — see the `nix-packaging` skill)        |
| Change how the package itself builds (patch, version bump, deps)                             | nixpkgs `overrideAttrs`/`.override` (the `nix-packaging` skill), not a wrapper |
| Need an FHS sandbox for an unpatched binary                                                  | `buildFHSEnv` / `nix-ld` (the `nixos-config` skill)                            |

Why not the hand-rolled forms: `writeShellScriptBin` drops the rest of the package; `symlinkJoin` +
`postBuild wrapProgram` gets the package back but gives no `.override` passthrough, no principled cross-import
override, and often a wrong `Exec=`/`Icon=` in the desktop file. The module approach fixes all three and
composes across every module system.

## Workflow

```text
nix-wrapper-modules Progress:

- [ ] Step 1: Confirm a module-wrapper is the right tool (table above) ⚠️ REQUIRED
- [ ] Step 2: Add the flake input and know the outputs map
- [ ] Step 3: Author the wrapper (pick one of three modes)
  - [ ] 3a: settings → constructFiles → env/flags (no writeText bypass) ⛔ IRON LAW
- [ ] Step 4: Install it for the target environment(s)
- [ ] Step 5: Build the derivation and run it ⛔ BLOCKING
```

## Step 1: Confirm the tool ⚠️ REQUIRED

Check the table above. If the task is a plain package override or a one-env-var wrapper, STOP and use the
`nix-packaging` skill instead — a module wrapper is overkill and adds an input.

## Step 2: Flake input and outputs

```nix
inputs.nix-wrapper-modules.url = "github:BirdeeHub/nix-wrapper-modules";
inputs.nix-wrapper-modules.inputs.nixpkgs.follows = "nixpkgs";  # optional: reuse your nixpkgs
```

The flake needs only `nixpkgs` itself; `flake-parts` is optional (needed only for `flakeModules.wrappers`).
Outputs you consume (full list in `references/api-reference.md`):

| Output                                                | What it gives you                                                                        |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `wrappers.<name>`                                     | Pre-evaluated `.config` per bundled program — `.wrap`/`.apply`/`.eval` directly callable |
| `wrapperModules.<name>`                               | Raw importable module path per program                                                   |
| `lib` (`wlib`)                                        | `evalModule`, `evalPackage`, `wrapPackage`, `getInstallModule`, `types`, dag helpers     |
| `flakeModules.wrappers` (= `.default`)                | The flake-parts module                                                                   |
| `nixosModules.<name>` / `homeModules` / `hjemModules` | Per-wrapper pre-built install modules                                                    |

MUST use `wrappers`, NOT `wrappedModules` — the latter is a deprecated alias scheduled for **removal
2026-08-31**.

## Step 3: Author the wrapper — pick one mode

### Mode A — configure a bundled program

```nix
inputs.nix-wrapper-modules.wrappers.alacritty.wrap {
  inherit pkgs;
  settings.terminal.shell.program = "${pkgs.zsh}/bin/zsh";
  settings.terminal.shell.args = [ "-l" ];
}
```

### Mode B — ad-hoc wrap of any package

```nix
inputs.nix-wrapper-modules.lib.wrapPackage ({ config, wlib, lib, pkgs, ... }: {
  inherit pkgs;
  package = pkgs.curl;
  runtimePkgs = [ pkgs.jq ];
  env.CURL_CA_BUNDLE = "${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt";
  flags = { "--silent" = true; "--connect-timeout" = "30"; };
  flagSeparator = "=";
})
```

`wrapPackage` returns the derivation directly. It requires `pkgs` — see the "no pkgs yet" gotcha below if you
need to share a wrapper before `pkgs` is known.

### Mode C — reusable module with its own options (⛔ IRON LAW lives here)

Declare a typed `settings` option, render it with a `lib.generators.to*` function into
`constructFiles.<name>.content`, and point the program at `constructFiles.<name>.path`:

```nix
{ config, lib, wlib, pkgs, ... }: {
  imports = [ wlib.modules.default ];
  options.settings = lib.mkOption {
    inherit (pkgs.formats.gitIni { }) type;   # or a plain attrsOf type for key=value programs
    default = { };
  };
  config = {
    package = lib.mkDefault pkgs.git;
    env.GIT_CONFIG_GLOBAL = config.configFile.path;
    constructFiles.gitconfig = {
      relPath = "${config.binName}config";
      content = lib.generators.toGitINI config.settings;
    };
    meta.maintainers = [ wlib.maintainers.birdee ];
  };
}
```

Evaluate with `inputs.nix-wrapper-modules.lib.evalModule <module>`; the package is `.config.wrapper`. Use
`constructFiles`, never `pkgs.writeText`, so `${placeholder "out"}` resolves against the final wrapper.
`wlib.modules.default` supplies `env`, `flags`, `addFlag`/`appendFlag`, `runShell`, `chdir`,
`prefixVar`/`suffixVar`/`prefixContent`/`suffixContent`, `runtimePkgs`/`runtimeLibs`, `unsetVar`, `aliases`,
`wrapperVariants`, `constructFiles` — see `references/api-reference.md`.

## Step 4: Install per environment

| Target                                | How                                                                                                                                                                                                  |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Bare shell / devshell / flake package | The `.wrap`/`evalPackage` result is a plain derivation — `nix build`, `nix run`, `mkShell` `packages`, `home.packages`, etc.                                                                         |
| NixOS / home-manager / nix-darwin     | `imports = [ (lib.getInstallModule { name = "tmux"; value = wrapperModules.tmux; }) ];` then set `wrappers.tmux = { enable = true; settings = { … }; };`. `enable = true` auto-installs the package. |
| flake-parts                           | Import `flakeModules.wrappers`; declare `flake.wrappers.<name> = <module>;`; import `config.flake.wrappers.<name>.install` into a host/home module (no `getInstallModule` needed).                   |

Only NixOS/HM/darwin get an auto-install default; a bare `.wrap` result you install like any package.

## Step 5: Build and run ⛔ BLOCKING

MUST build the derivation and execute it — a clean eval does not prove the wrapper runs:

```bash
nix build .#<attr>      # or nix-instantiate/eval the .config.wrapper
./result/bin/<binName> --help
```

## Backends (`wrapperImplementation`)

| Value             | Engine                   | Notes                                                                                                |
| ----------------- | ------------------------ | ---------------------------------------------------------------------------------------------------- |
| `"nix"` (default) | custom                   | Runtime `$VAR` expansion; most flexible; escape values with `wlib.escapeShellArgWithEnv`             |
| `"shell"`         | `pkgs.makeWrapper`       | Build-time expansion; do NOT use `escapeShellArgWithEnv` here                                        |
| `"binary"`        | `pkgs.makeBinaryWrapper` | Needed for macOS shebang invocation; **silently drops `runShell`, `prefixContent`, `suffixContent`** |

## Anti-Patterns

- **`makeWrapper`/`symlinkJoin`/`writeShellScriptBin` bypass** for one flag after adopting a module wrapper —
  defeats compose/override/desktop-file correctness (Iron Law).
- **`pkgs.writeText` for generated config** instead of `constructFiles` — breaks `${placeholder}` path
  resolution silently (Iron Law).
- **Using deprecated `wrappedModules`** — use `wrappers` (old alias removed 2026-08-31).
- **Assuming list options keep call order** — most list options (`lib.types.listOf`) put a later
  `.wrap`/`.apply` call's items *before* earlier ones; only `seriesOf`-typed options (e.g. `overrides`)
  preserve call order. Check the option's type before relying on ordering.
- **`wrapperImplementation = "binary"` while using `runShell`/`prefixContent`/`suffixContent`** — those are
  ignored.
- **Sharing a wrapper before `pkgs` is known via `.wrapper`/`wrapPackage`** — those error without `pkgs`; use
  `.eval`/`.apply`/`wrapModule` to pass the config along, and supply `pkgs` at the install site.
- **Reading `constructFiles` from outside via `config`** — from outside the module use
  `<pkg>.configuration.constructFiles.<name>.outPath`, not the in-module `config.…path`.

## Pre-Delivery Checklist

- [ ] A module wrapper is genuinely the right tool (not a plain override or one-env-var wrapper)
- [ ] Uses `wrappers`, not deprecated `wrappedModules`
- [ ] Generated config goes through `constructFiles`, never bare `pkgs.writeText`
- [ ] No `makeWrapper`/`symlinkJoin` bypass sneaking around the module
- [ ] Backend choice is deliberate; no `runShell`/`prefixContent`/`suffixContent` under the `binary` backend
- [ ] The wrapped derivation builds AND the binary runs with the intended flags/env/config
- [ ] Full API/option/type detail consulted in `references/api-reference.md` when needed

## Reference

`references/api-reference.md` — full `wlib` function list, core options, `wlib.types`, DAG/DAL ordering,
`wlib.modules.makeWrapper` internals, `constructFiles`, and the `install.*`/flake-parts surface.
