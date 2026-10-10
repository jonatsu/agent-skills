# Binary Overlay Pattern

For a platform-specific pre-built binary, key the source table on the system, expose per-system `packages`,
and add an overlay that reuses them. A complete, self-contained `flake.nix`:

```nix
{
  description = "Platform-specific binary package";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      version = "1.0.0";

      # Replace each hash after the first build attempt reports the real one
      sources = {
        "x86_64-linux" = {
          url = "https://example.com/tool-linux-amd64-v${version}";
          hash = nixpkgs.lib.fakeHash;
        };
        "aarch64-linux" = {
          url = "https://example.com/tool-linux-arm64-v${version}";
          hash = nixpkgs.lib.fakeHash;
        };
        "x86_64-darwin" = {
          url = "https://example.com/tool-darwin-amd64-v${version}";
          hash = nixpkgs.lib.fakeHash;
        };
        "aarch64-darwin" = {
          url = "https://example.com/tool-darwin-arm64-v${version}";
          hash = nixpkgs.lib.fakeHash;
        };
      };

      # Supported systems are exactly the systems we have a binary for
      forAllSystems = nixpkgs.lib.genAttrs (builtins.attrNames sources);

      toolFor = system:
        let pkgs = nixpkgs.legacyPackages.${system};
        in pkgs.stdenv.mkDerivation {
          pname = "tool";
          inherit version;

          src = pkgs.fetchurl { inherit (sources.${system}) url hash; };
          dontUnpack = true;

          installPhase = ''
            install -Dm755 $src $out/bin/tool
          '';

          meta = {
            description = "Tool description";
            homepage = "https://example.com";
            license = nixpkgs.lib.licenses.unfree;
            platforms = builtins.attrNames sources;
            mainProgram = "tool";
          };
        };
    in {
      packages = forAllSystems (system: rec {
        tool = toolFor system;
        default = tool;
      });

      overlays.default = final: prev: {
        tool = self.packages.${final.stdenv.hostPlatform.system}.tool;
      };
    };
}
```

Notes:

- The overlay looks the package up by the host platform's system (`final.stdenv.hostPlatform.system`); there
  is no `prev.system` attribute.
- `sources.${system}` throws a clear "attribute missing" error on unsupported systems, and
  `meta.platforms` keeps `nix flake check` honest about what is supported.

## Hash Conversion

```bash
# Get hash in base32, convert to SRI format (what the `hash` attribute expects)
nix-prefetch-url --type sha256 https://example.com/file
nix hash to-sri --type sha256 <base32-hash>

# Or fetch and print the SRI hash in one step
nix store prefetch-file https://example.com/file
```
