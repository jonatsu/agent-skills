# mcp-nixos

MCP server for real-time NixOS ecosystem queries. Install via `uvx mcp-nixos` or
`nix run github:utensils/mcp-nixos`. No Nix install required for API queries.

Exposes 2 tools:

- `nix(action, query, source, type, channel, limit, system, version)` — actions
  `search`/`info`/`stats`/`browse`/`channels`/`flake-inputs`/`cache`/`store` across sources including NixOS
  packages and options, Home Manager, nix-darwin, FlakeHub, Nixvim, Noogle functions, the NixOS wiki, nix.dev,
  and the binary cache (`system` and `version` apply to `action="cache"` only)
- `nix_versions(package, version, limit)` — package version history with commit hashes

Known limitation: the Home Manager index is often sparse or empty — an empty result there does not prove an
option is absent; cross-check another source.

**Use before writing any flake expression**: verify package names exist, find correct option paths, check
binary cache availability, look up flake inputs, search Nix function signatures. Prevents hallucinated
attribute names.

```python
# Verify a package exists
nix(action="search", query="firefox", source="nixos", type="packages")

# Find correct option path
nix(action="search", query="services.nginx", source="nixos", type="options")

# Check binary cache (avoid 3hr builds)
nix(action="cache", query="firefox", system="x86_64-linux")

# Search Nix functions
nix(action="search", query="mapAttrs", source="noogle")
```
