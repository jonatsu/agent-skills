# nix-wrapper-modules — API Reference

Full option/type/function surface, extracted from <https://birdeehub.github.io/nix-wrapper-modules>
(`lib/*.html`, `modules/default.html`, `md/getting-started.html`, `md/CONTRIBUTING.html`) plus the repo
`flake.nix`. Pre-1.0, no tagged releases — verify against the live docs if an eval disagrees with a shape
here.

## Contents

- [Flake outputs](#flake-outputs)
- [wlib functions](#wlib-functions)
- [Core options](#core-options-libcorenix-always-imported)
- [wlib.types](#wlibtypes)
- [DAG / DAL ordering](#dag--dal-ordering)
- [wlib.modules.makeWrapper internals](#wlibmodulesmakewrapper-internals)
- [constructFiles](#constructfiles)
- [install.\* and flake-parts surface](#install-and-flake-parts-surface)
- [Chaining: .eval / .apply / .wrap / .extendModules](#chaining-eval--apply--wrap--extendmodules)

## Flake outputs

| Output                                             | Contents                                                                                                                               |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `lib`                                              | `wlib` — `evalModule`, `evalModules`, `evalPackage`, `wrapPackage`, `getInstallModule`, `types`, dag helpers, `wrapperModules` (paths) |
| `wrappers`                                         | `mapAttrs (_: v: (evalModule v).config) wrapperModules` — pre-evaluated `.config` per program                                          |
| `wrapperModules`                                   | Raw (unevaluated, importable) module paths per program                                                                                 |
| `flakeModules.wrappers` (= `.default`)             | The flake-parts module (`./parts.nix`)                                                                                                 |
| `nixosModules.<name>`                              | Each wrapper pre-wrapped via `getInstallModule`, importable into NixOS                                                                 |
| `homeModules`, `hjemModules`                       | Aliases of `nixosModules`                                                                                                              |
| `devShells.<system>.default`, `formatter.<system>` | Dev shell / `nixfmt-tree`                                                                                                              |
| `wrappedModules`                                   | **DEPRECATED** alias of `wrappers`; removal scheduled **2026-08-31** (warned in `flake.nix`)                                           |

Templates: `nix flake init -t github:BirdeeHub/nix-wrapper-modules` (default) and `…#flake-parts`.

## wlib functions

| Function                                                            | Behavior                                                                                                                                                                                                                                             |
| ------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `evalModules`                                                       | `lib.evalModules` with the core module pre-imported and `wlib` in `specialArgs`                                                                                                                                                                      |
| `evalModule`                                                        | `module: evalModules { modules = toList module; }` → raw result (`.config`, `.options`)                                                                                                                                                              |
| `evalPackage`                                                       | `module: (evalModules {…}).config.wrapper` — returns the package; requires `pkgs`                                                                                                                                                                    |
| `wrapModule`                                                        | imports `wlib.modules.default`, returns `.config` (so `.wrap` reachable) without needing `pkgs` yet                                                                                                                                                  |
| `wrapPackage`                                                       | `module: evalPackage ([wlib.modules.default] ++ toList module)` — package directly; requires `pkgs`                                                                                                                                                  |
| `getInstallModule`                                                  | `{ name, value, …evalModules-args }` → module importable into another module system; returns `config.install`. Default option location `config.wrappers.${name}`. With flake-parts, prefer importing `config.flake.wrappers.<name>.install` directly |
| `mkOutOfStoreSymlink`                                               | `pkgs -> path -> { out = …; }` (home-manager helper lifted in; `pkgs` first)                                                                                                                                                                         |
| `getPackageOutputsSet`                                              | `Derivation -> { <output> = storePath; }`                                                                                                                                                                                                            |
| `escapeShellArgWithEnv`                                             | double-quote escape so `$VAR`/`${VAR}` still expand — for the `nix` backend only                                                                                                                                                                     |
| `makeCustomizable`                                                  | generalized `makeOverridable`; configurable override attrs + `mergeArgs`                                                                                                                                                                             |
| `sanitizeEnvVarName`                                                | string → valid POSIX env-var name                                                                                                                                                                                                                    |
| `ignoreSpecField`                                                   | placeholder to override only an aux field of a spec-typed value                                                                                                                                                                                      |
| `mapAttrsToList0`, `partitionAttrs`, `genStr`, `repeatStr`, `toKdl` | misc helpers                                                                                                                                                                                                                                         |

## Core options (`lib/core.nix`, always imported)

Build the **derivation** (the wrapper-script logic lives in `wlib.modules.default`).

| Option                                            | Type                                                  | Default                             | Meaning                                                                                                                                                                                                                           |
| ------------------------------------------------- | ----------------------------------------------------- | ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pkgs`                                            | package set                                           | required for `.wrapper`             | Package set used to realize the wrapper                                                                                                                                                                                           |
| `package`                                         | str/path/drv                                          | —                                   | Base package (all `overrides` pre-applied when read)                                                                                                                                                                              |
| `overrides`                                       | `seriesOf` spec (main field `data`)                   | `[]`                                | Ordered `.override`/`.overrideAttrs`/raw-fn transforms. Entry `{ data, type ? null, name ? null, before ? [], after ? [] }`; `type=null` ⇒ `data` is `pkg -> pkg`; `type="override"`/`"overrideAttrs"` ⇒ passed to that attribute |
| `exePath`                                         | null or non-empty line                                | `getExe package` (relative)         | Executable to wrap, e.g. `bin/foo`                                                                                                                                                                                                |
| `binName`                                         | string                                                | package's bin name                  | Output binary file name                                                                                                                                                                                                           |
| `outputName`                                      | non-empty line                                        | `"out"`                             | Output the wrapped binary lands in. NOTE: `nix build` still targets `out` regardless                                                                                                                                              |
| `outputs`                                         | non-empty list of string                              | `[ "out" ]` / `package.outputs`     | Outputs symlinked into the final package (`outputName` first)                                                                                                                                                                     |
| `buildCommand`                                    | attrset of spec (main `data`, `\n`-joined)            | —                                   | DAG of build-script fragments fulfilling the `wrapperPaths` contract; populated for you by the helper modules                                                                                                                     |
| `builderFunction`                                 | function                                              | `{ buildCommand, … }: buildCommand` | How `buildCommand` becomes the derivation. Return a string (into `buildCommand`), a `drvArgs -> finalDrvArgs` fn (full control), or a functor with `mkDerivation` (total control; you handle `passthru`/`sourceStdenv`)           |
| `sourceStdenv`                                    | bool                                                  | —                                   | Run enabled stdenv phases on the wrapper derivation                                                                                                                                                                               |
| `drv`                                             | attrsRecursive                                        | —                                   | Extra raw derivation attrs (not `passthru`/`outputs`/`buildCommand`)                                                                                                                                                              |
| `passthru`                                        | lazyAttrsRecursive                                    | —                                   | Extra `passthru` (lazy — supports `"${config.wrapper}/…"`, not `mkIf`)                                                                                                                                                            |
| `wrapper`                                         | read-only package                                     | —                                   | Final wrapped package (errors without `pkgs`)                                                                                                                                                                                     |
| `apply` / `eval` / `extendModules`                | read-only functions                                   | —                                   | Chaining entry points (see below)                                                                                                                                                                                                 |
| `wrapperPaths.{input,placeholder,relDir,relPath}` | read-only string                                      | —                                   | Contract paths the `buildCommand` must honor                                                                                                                                                                                      |
| `meta.description`                                | string / `{pre?, post?}`                              | —                                   | Doc text                                                                                                                                                                                                                          |
| `meta.maintainers`                                | list of submodule (name/github/githubId/email/matrix) | —                                   | Required on contributed modules                                                                                                                                                                                                   |
| `meta.platforms`                                  | list of `lib.platforms.all` enum                      | `lib.platforms.all`                 | Supported systems                                                                                                                                                                                                                 |

Helper-module options (from `wlib.modules.default` = `makeWrapper` + `symlinkScript` + `constructFiles`):
`env`, `envDefault`, `unsetVar`, `flags`, `addFlag`, `appendFlag`, `flagSeparator`, `prefixVar`, `suffixVar`,
`prefixContent`, `suffixContent`, `chdir`, `runShell`, `runtimePkgs`, `runtimeLibs`, `aliases`,
`filesToExclude`, `filesToPatch`, `wrapperVariants.<name>`, `wrapperImplementation`, `escapingFunction`,
`constructFiles.<name>`.

## wlib.types

| Type                                                                                                          | Purpose                                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `subWrapperModuleWith { modules?, specialArgs?, shorthandOnlyDefinesConfig?, description?, class? }`          | Like `submoduleWith` but pre-imports `wlib.core` and injects `wlib`/`modulesPath`. Value is `.config`; `.optionname.wrapper` is the package |
| `subWrapperModule module`                                                                                     | `subWrapperModuleWith { modules = toList module; }`                                                                                         |
| `specWith { modules, specialArgs?, class?, description?, mainField?, dontConvertFunctions? }` / `spec module` | Normalizes "bare value or `{ <mainField>=value; …aux }`" on merge. `mainField` auto-detected from the single no-default option unless set   |
| `dagOf elemType` / `dalOf elemType`                                                                           | Attrset-DAG / list-DAG of `elemType`; entries `elemType` or `{ data, name?, before?, after? }`                                              |
| `dagWithEsc` / `dalWithEsc`                                                                                   | As above plus an `esc-fn` field (`null` or `string -> string`); used by `makeWrapper`                                                       |
| `seriesOf`                                                                                                    | Like `listOf` but **reverses merge order across imports** — later imports append (used by `overrides`)                                      |
| `withPackagesType`                                                                                            | `withPackages`-style function-from-package-set-to-list                                                                                      |
| `wrapperFlags { length }` / `wrapperFlag`                                                                     | DAL of fixed-length stringable tuples / more flexible flag DAL                                                                              |
| `file { extra }`                                                                                              | Generated-file template (`content`, `path`); pass `pkgs` as `extra` for `writeText`-based defaults                                          |
| `attrsRecursive` / `lazyAttrsRecursive`                                                                       | Like `anything`/`lazyAttrsOf anything` but lists merge                                                                                      |
| `structuredValueWith { typeName, nullable, extraValueTypes }`                                                 | Serializable value (bool/int/float/string/path/attrset/list + extras)                                                                       |
| `stringable`, `linkable`, `nonEmptyLine`, `fixedList { length, elemType }`                                    | value scalars/paths/lines/fixed lists                                                                                                       |

## DAG / DAL ordering

`wlib.dag` builds and resolves ordering across **all** DAG/DAL-typed options in a module (so an `env` entry
can be `after` a `runtimePkgs`-generated one). Key functions: `dagWith`/`dalWith`, `mkDagEntry`, `topoSort` (→
`{ result }` or `{ cycle; loops; }`), `unwrapSort`/`sortAndUnwrap` (throws on cycle), `dagToDal`, plus
ordering constructors `specBetween`/`specAfter`/`specBefore`, `entryBetween`/`entryAnywhere`/`entryAfter`/
`entryBefore` and their `*s*` sequence variants.

Every DAG/DAL entry accepts `{ data, name?, before?, after?, esc-fn? }`; `esc-fn` overrides
`config.escapingFunction` for just that value.

## wlib.modules.makeWrapper internals

`wrapAll`/`wrapMain`/`wrapVariants`/`wrapVariant` emit build-instruction strings. `aggregateSingleOptionSet`
flattens the option categories (`unsetVar`, `env`, `envDefault`, `prefixVar`, `suffixVar`, `prefixContent`,
`suffixContent`, `chdir`, `runShell`, `flags`, `addFlag`, `appendFlag`) into one sorted DAL. `splitDal` →
`{ args; other; }`. `fixArgs { sep?, ifs?, fixPreFlagSort? } argsDAL` resolves `flags`/`addFlag`/`appendFlag`
into concrete `{ addFlag; appendFlag; }` lists, honoring per-entry or global `sep`/`ifs`.

Redefine before import: `import wlib.modules.makeWrapper // { excluded_options.wrapperVariants = true; }`
(also `exclude_wrapper`, `wrapperFunction`, `exclude_meta`, `excluded_options.{top,<opt>}`).

`wrapperVariants.<name>` — extra binaries from one package: each has its own `package`/`exePath`/`binName`
plus the full option set, with `mirror = true` (default) inheriting the top-level values via
`mainConfig`/`mainOpts` special args.

## constructFiles

`constructFiles.<name>` (from `modules/constructFiles`) — generate a config file whose `${placeholder}`
references resolve against the **final** wrapper derivation:

| Field                                                                                                       | Meaning                                                                             |
| ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `content`                                                                                                   | File content (typically `lib.generators.to*` of a `settings` option)                |
| `relPath`                                                                                                   | Path relative to the output                                                         |
| `output`                                                                                                    | Which derivation output it lands in                                                 |
| `builder`                                                                                                   | Custom build command (default `cp "$1" "$2"`)                                       |
| `passAsContent`                                                                                             | Pass content vs. path as `$1`; recommend `true` when `drv.__structuredAttrs = true` |
| `path` (read-only, in-module) / `outPath` (from outside via `passthru.configuration.constructFiles.<name>`) | Resolved locations                                                                  |

Never substitute a bare `pkgs.writeText` — that is the Iron Law failure.

## install.\* and flake-parts surface

`install.modules.<class>` — per-module-system integration modules keyed by module-system `class` (`nixos`,
`homeManager`, …). `install.optionLocation` — where the generated submodule option is placed (auto-set by the
flake-parts module / `getInstallModule`). `install.getWrapperConfig` / `install.mkWrapperExtension` — retrieve
/ extend the wrapper submodule at that location from inside an `install.modules.<class>` module.

flake-parts (`flakeModules.wrappers`): declare `flake.wrappers.<name> = module;`; get `flake.wrapperModules`,
`perSystem.wrappers.packages` and `.control_type` (`"exclude"` default; set `true` to exclude from
`packages.*.*`, `"build"` mode needs explicit `true` opt-in), `perSystem.wrappers.pkgs` override. Derive
`flake.nixosModules`/`homeModules` via `mapAttrs (_: v: v.install) self.wrappers` — no `getInstallModule`
needed.

## Chaining: .eval / .apply / .wrap / .extendModules

Available on both the evaluated module's `config` and (via `passthru`) the resulting package:

- `.eval <module>` — extend with more modules, return the raw `evalModules` result.
- `.apply <module>` — same, auto-grabs `.config`.
- `.wrap <module>` — auto-grabs `.config.wrapper` (needs `pkgs` if not yet supplied).
- `.extendModules { modules?, prefix?, specialArgs? }` — low-level extension.

```nix
initial   = (wrappers.tmux.eval ({ config, pkgs, ... }: { config.clock24 = false; })).config;
extended  = initial.apply { modeKeys = "vi"; };
pkg       = extended.wrap { inherit pkgs; };
more      = pkg.wrap ({ config, pkgs, ... }: { plugins = [ pkgs.tmuxPlugins.fzf-tmux-url ]; });
```

Note the list-merge-order caveat: most list options place a later call's items *before* earlier ones (only
`seriesOf`-typed options preserve call order).
