# mcp-nixos

MCP server for real-time NixOS ecosystem queries. Install via `uvx mcp-nixos` or
`nix run github:utensils/mcp-nixos`. No Nix install required for API queries.

Exposes 2 tools with ~1,030 tokens context cost:

- `nix(action, query, source, type, channel, limit)` — search/info/stats/cache/flake-inputs across 10 sources
  (NixOS packages 130K+, options 23K+, Home Manager 5K+, nix-darwin, FlakeHub, Nixvim, Noogle functions, wiki,
  nix.dev, binary cache)
- `nix_versions(package, version, limit)` — package version history with commit hashes

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
