---
name: nix-packaging
description: "Nix packaging — create derivations for source or binary packages, handle library dependencies, autoPatchelfHook, overlays, and flake outputs. Use when packaging .deb/.rpm/.tar.gz/AppImage, writing mkDerivation, finding missing libraries, or creating overlays. Triggers on: nix package, derivation, mkDerivation, autoPatchelf, buildInputs, nativeBuildInputs, fetchurl, fetchFromGitHub, overlay, FHS, makeWrapper, nix-prefetch."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Nix Packaging

IRON LAW: ALWAYS SOURCE FROM THE ORIGINAL ARCHIVE — NEVER FROM PRE-EXTRACTED DIRECTORIES. PRE-EXTRACTED DIRS
LOSE METADATA, CHECKSUMS, AND REPRODUCIBILITY. THE `src` ATTRIBUTE MUST POINT TO A FETCHED ARCHIVE, NOT A
LOCAL DIRECTORY.

## Workflow

```text
Nix Packaging Progress:

- [ ] Step 1: Identify packaging type (binary vs source) ⚠️ REQUIRED
- [ ] Step 2: Gather source (fetchurl, fetchFromGitHub, etc.)
- [ ] Step 3: Write derivation
- [ ] Step 4: Handle dependencies
- [ ] Step 5: Test the package
- [ ] Step 6: Add to flake outputs / overlay
- [ ] Step 7: Verify ⚠️ REQUIRED
```

## Step 1: Identify Packaging Type ⚠️ REQUIRED

Determine whether the software is distributed as a pre-compiled binary or as source code.

- **Binary packaging**: `.deb`, `.rpm`, `.AppImage`, tarball with pre-built binaries, or a single
  statically-linked binary. Use `autoPatchelfHook` to fix library paths.
- **Source packaging**: Source tarball or git repository. Use the project's build system (meson, cmake, cargo,
  go, etc.).

⛔ BLOCKING: Do NOT proceed without confirming the packaging type. Binary and source derivations have
fundamentally different structures.

## Step 2: Gather Source

Fetch the original archive. NEVER use a pre-extracted directory.

```bash
# For arbitrary URLs
nix-prefetch-url --type sha256 https://example.com/file.deb

# For GitHub archives
nix-prefetch-url --unpack https://github.com/owner/repo/archive/v1.0.0.tar.gz
```

Common fetchers:

- `fetchurl` — any URL. Requires `url` and `hash`.
- `fetchFromGitHub` — GitHub repos. Requires `owner`, `repo`, `rev`, `hash`.
- `fetchzip` — zip archives. Auto-extracts.
- `fetchgit` — raw git repos. Use sparingly; prefer `fetchFromGitHub`.

MUST use `lib.fakeHash` only during initial scaffolding. Replace with the real hash before final delivery.

```nix
# For .zip archives, add unzip to nativeBuildInputs
nativeBuildInputs = [ unzip ];
```

## Step 3: Write Derivation

### Binary Packaging (.deb)

```nix
{ stdenv, lib, autoPatchelfHook, dpkg, fetchurl, gtk3, glib }:

stdenv.mkDerivation (finalAttrs: {
  pname = "example";
  version = "1.0.0";

  src = fetchurl {
    url = "https://example.com/example-${finalAttrs.version}.deb";
    hash = lib.fakeHash;  # replace after first build
  };

  nativeBuildInputs = [ autoPatchelfHook dpkg ];
  buildInputs = [ stdenv.cc.cc.lib gtk3 glib ];

  unpackPhase = ''
    dpkg-deb -x $src .
  '';

  installPhase = ''
    mkdir -p $out
    cp -r usr/* $out/
  '';
})
```

```nix
# Alternative: use ar instead of dpkg-deb
unpackPhase = ''
  ar x $src
  tar xf data.tar.xz
'';
```

### Binary Packaging (.rpm)

```nix
{ stdenv, lib, autoPatchelfHook, rpm, fetchurl, ... }:

stdenv.mkDerivation (finalAttrs: {
  pname = "example";
  version = "1.0.0";

  src = fetchurl {
    url = "https://example.com/example-${finalAttrs.version}.x86_64.rpm";
    hash = lib.fakeHash;
  };

  nativeBuildInputs = [ autoPatchelfHook rpm ];

  unpackPhase = ''
    rpm2cpio $src | cpio -idmv
  '';

  installPhase = ''
    mkdir -p $out
    cp -r usr/* $out/
  '';
})
```

### Simple Binary (no extraction needed)

```nix
stdenv.mkDerivation (finalAttrs: {
  pname = "tool";
  version = "1.0.0";

  src = fetchurl {
    url = "https://example.com/tool-${finalAttrs.version}-linux-amd64";
    hash = lib.fakeHash;
  };

  dontUnpack = true;

  installPhase = ''
    mkdir -p $out/bin
    cp $src $out/bin/tool
    chmod +x $out/bin/tool
  '';
})
```

### Source Packaging

```nix
{ stdenv, lib, fetchFromGitHub, meson, ninja, pkg-config, gtk3 }:

stdenv.mkDerivation (finalAttrs: {
  pname = "example";
  version = "1.0.0";

  src = fetchFromGitHub {
    owner = "owner";
    repo = "example";
    rev = "v${finalAttrs.version}";
    hash = lib.fakeHash;
  };

  nativeBuildInputs = [ meson ninja pkg-config ];
  buildInputs = [ gtk3 ];

  mesonFlags = [ "-Dexample=true" ];
})
```

The `(finalAttrs: { ... })` argument form is `mkDerivation`'s fixpoint: `finalAttrs.version` refers to the
final attribute value, so it stays correct under `overrideAttrs`. Prefer it over `rec`, which binds early and
silently keeps the old value when overridden.

### AppImage Packaging

Use `appimageTools` — the canonical nixpkgs route. `wrapType2` handles extraction and bundles the common
runtime libraries:

```nix
{ lib, appimageTools, fetchurl }:

appimageTools.wrapType2 rec {
  pname = "app";
  version = "1.0.0";

  src = fetchurl {
    url = "https://example.com/app-${version}.AppImage";
    hash = lib.fakeHash;
  };

  # Libraries the app loads at runtime beyond appimageTools' defaults
  extraPkgs = pkgs: [ pkgs.libsecret ];
}
```

Need files from inside the image (`.desktop` entry, icons)? `appimageTools.extract { inherit pname version src; }`
yields the unpacked squashfs tree; copy from it in `extraInstallCommands`.

For a one-off run without packaging: `nix run nixpkgs#appimage-run -- ./app.AppImage`.

Do NOT hand-write an `unpackPhase` that runs `$src --appimage-extract` — files in the Nix store are not
executable, so it fails; let `appimageTools` do the extraction.

### Electron Apps

See [references/electron-dependencies.md](references/electron-dependencies.md) for the complete Electron
runtime dependency list.

## Step 4: Handle Dependencies

### Dependency Categories

| Attribute               | When to use                                                                                                                                      |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `nativeBuildInputs`     | Tools needed at BUILD time only: compilers, code generators, `pkg-config`, `cmake`, `meson`, `makeWrapper`                                       |
| `buildInputs`           | Libraries needed at BUILD and RUN time: `gtk3`, `glib`, `mesa`, `openssl`                                                                        |
| `propagatedBuildInputs` | Libraries needed by consumers of this package at their build time. Use sparingly — only when headers or pkg-config files are required downstream |

See [references/library-mapping.md](references/library-mapping.md) for the complete library→package mapping
and debugging commands.

### makeWrapper Pattern

Use `makeWrapper` to wrap binaries with environment variables or extra PATH entries:

```nix
{ stdenv, lib, makeWrapper, coreutils, gsettings-desktop-schemas, ... }:

stdenv.mkDerivation {
  # ...

  nativeBuildInputs = [ makeWrapper ];

  installPhase = ''
    install -Dm755 $src/bin/app $out/bin/app
    wrapProgram $out/bin/app \
      --prefix PATH : ${lib.makeBinPath [ coreutils ]} \
      --set GSETTINGS_SCHEMA_DIR ${gsettings-desktop-schemas}/share/gsettings-schemas/${gsettings-desktop-schemas.name}
  '';
}
```

## Step 5: Test the Package

```bash
# Build the package
nix build .#package-name

# Quick smoke test in FHS environment (for binary packages)
nix-shell -p steam-run --run "steam-run result/bin/app"

# Check for missing libraries
ldd result/bin/app | grep "not found"

# Run the binary directly
./result/bin/app --help
```

```bash
# Debug autoPatchelf failures — check build log
nix log /nix/store/...-drv
# Or during build:
nix build .#package-name -L  # -L shows full build output
```

## Step 6: Add to Flake Outputs / Overlay

### Flake Parts (perSystem)

```nix
perSystem = { pkgs, ... }: {
  packages.example = pkgs.callPackage ./nix/example.nix { };
  packages.default = pkgs.callPackage ./nix/example.nix { };
};
```

### Overlay

```nix
overlays.default = final: prev: {
  example = final.callPackage ./nix/example.nix { };
};
```

## Binary Overlay Pattern

See [references/binary-overlay-pattern.md](references/binary-overlay-pattern.md) for the full
platform-specific binary overlay pattern with hash conversion.

## Step 7: Verify ⚠️ REQUIRED

⛔ BLOCKING: Do NOT deliver the derivation until ALL checks pass.

```bash
# Build must succeed
nix build .#package-name

# Binary must run without missing library errors
ldd result/bin/* | grep "not found"  # MUST return empty

# Flake check must pass
nix flake check
```

## FHS Escape Hatch (Last Resort)

Use `buildFHSEnv` ONLY when `autoPatchelfHook` cannot resolve dependencies (e.g., binaries that hardcode
`/usr/lib` paths or dlopen libraries at runtime):

```nix
{ buildFHSEnv }:

buildFHSEnv {
  name = "app-fhs";
  targetPkgs = pkgs: [ pkgs.app ];
  runScript = "app";
}
```

NEVER use FHS as the first approach. Always attempt `autoPatchelfHook` first.

## Module-System Wrappers

`makeWrapper`/`symlinkJoin` wrap a single derivation, and the wrapping usually lives inside one NixOS or
home-manager config. When a **configured** executable (baked-in flags, env vars, generated config files) must
stay portable across NixOS, home-manager, nix-darwin, devshells, and plain `nix build`, a module-system
wrapper library such as BirdeeHub's
[nix-wrapper-modules](https://github.com/BirdeeHub/nix-wrapper-modules) is the better fit: it evaluates a
small module system per program and emits an ordinary derivation usable anywhere. Stay with `makeWrapper` for
a one-off env-var or PATH tweak; reach for a wrapper-module library once the wrapping needs generated config
or cross-environment reuse.

| Approach                      | Scope             | Portability                            |
| ----------------------------- | ----------------- | -------------------------------------- |
| `makeWrapper` + `symlinkJoin` | Single derivation | NixOS/HM only                          |
| `nix-wrapper-modules`         | Module system     | NixOS, HM, nix-darwin, devshell, shell |
| `buildFHSEnv`                 | FHS sandbox       | Anywhere (heavy)                       |

## Unfree Packages

```nix
meta = {
  license = lib.licenses.unfree;
};
```

Users MUST enable unfree packages in their configuration to build. Under a flake, that means config passed to
`import nixpkgs`, because pure evaluation ignores `NIXPKGS_ALLOW_UNFREE` and `~/.config/nixpkgs/config.nix`.
See the `nix-flakes` skill for the mechanisms and the evaluation evidence.

## Anti-Patterns

- **Sourcing from pre-extracted directories** instead of original archives. Violates the IRON LAW. Always use
  `fetchurl`/`fetchFromGitHub`.
- **Using `autoPatchelfHook` without putting libraries in `buildInputs`**. `autoPatchelfHook` can only find
  libraries that are in `buildInputs`.
- **Mixing up `nativeBuildInputs` and `buildInputs`**. Build tools go in `nativeBuildInputs`; runtime
  libraries go in `buildInputs`.
- **Using `lib.fakeHash` in final derivation**. Only for initial scaffolding. Replace with real hash before
  delivery.
- **Creating FHS environments when `autoPatchelfHook` would work**. FHS is a heavy escape hatch; try
  `autoPatchelfHook` first.
- **Hardcoding absolute store paths** instead of using package references (e.g., `${gtk3}/lib` not
  `/nix/store/abc-gtk3/lib`).
- **Forgetting to test with `ldd` for missing libraries**. A successful build does not guarantee a runnable
  binary.
- **Using `propagatedBuildInputs` when `buildInputs` suffices**. Only propagate when downstream consumers need
  the library at their build time.
- **Skipping `nix flake check`**. Broken flakes block users.
- **Not pinning `rev` in `fetchFromGitHub`**. Unpinned revisions break reproducibility.
- **Using `xorg.libxkbcommon` instead of `libxkbcommon`** — the correct package is `libxkbcommon`, not
  `xorg.libxkbcommon`.
- **Referencing `version` in `src` from a plain attrset** — it is not in scope and fails to evaluate. Use the
  `(finalAttrs: { ... })` argument to `mkDerivation` and write `finalAttrs.version`; prefer it over `rec`,
  which binds early and keeps stale values under `overrideAttrs`.

## Pre-Delivery Checklist

- [ ] Source fetched from original archive (not pre-extracted directory)
- [ ] Hash is real (not `lib.fakeHash`)
- [ ] Package added to flake outputs or overlay
- [ ] No hardcoded store paths (all references use `${pkg}` interpolation)
- [ ] `meta` block present with at minimum `license` and `description`
- [ ] `meta.platforms` set for multi-platform packages
- [ ] `meta.mainProgram` set if package has multiple binaries (for `nix run`)
