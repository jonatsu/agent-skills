# Quirks & Pipes

Quirks solve structured data aggregation between aspects without coupling. Producers emit data on named keys; consumers receive assembled data via function arguments.

## Quick Start: Firewall Ports

```nix
# 1. Declare the quirk
den.quirks.firewall = { description = "Firewall port declarations"; };

# 2. Produce data (any aspect can emit)
den.aspects.nginx = {
  nixos.services.nginx.enable = true;
  firewall = { ports = [ 80 443 ]; };
};
den.aspects.postgres = {
  nixos.services.postgresql.enable = true;
  firewall = { ports = [ 5432 ]; };
};

# 3. Consume data (name the quirk in function args)
den.aspects.networking = {
  nixos = { firewall, lib, ... }: {
    networking.firewall.allowedTCPPorts =
      lib.concatMap (f: f.ports or []) firewall;
  };
};
```

No pipe policy needed — same-scope aggregation works out of the box. If no producers emit data, consumer receives `[]`.

## Quirk Names Shadow Nested Aspects — Silently

**A registered quirk name wins over every other interpretation of that key.** den classifies an aspect's keys in a fixed order: **pipe (quirk) keys first**, then class keys, then nested aspects. Because quirk keys are filtered out of the candidate set before nested-aspect classification runs, a nested aspect whose key collides with a registered `den.quirks` name is read as pipe data and **never registers as an aspect**. No error, no warning.

```nix
den.quirks.firewall = { description = "Firewall port declarations"; };

# Intended as a nested aspect — silently consumed as firewall quirk data instead
den.aspects.edge.firewall = {
  nixos.services.nftables.enable = true;
};
```

Pick quirk names you would never use as an aspect key, and check `den.quirks` before naming a nested aspect. Verified against den `2040b613` (`nix/lib/aspects/fx/key-classification.nix`).

**Related:** sub-aspects are never auto-walked. den's classifier relies on this — nested aspects activate only via an explicit `includes`, which is why depth-1 key detection suffices.

## Pipe Builder API

All pipe stages accessed via `den.lib.policy.pipe`:

| Stage | Purpose |
|-------|---------|
| `pipe.from "quirk-name" [ stages ]` | Start a pipe from a quirk |
| `pipe.filter (e: predicate)` | Remove entries not matching predicate |
| `pipe.transform (e: newShape)` | Map each entry to a new shape |
| `pipe.fold (acc: n: acc + n) initial` | Reduce all entries to a single value |
| `pipe.append { name = "default"; }` | Add a synthetic entry |
| `pipe.for (vals: lib.reverseList vals)` | Replace entire list (max one per pipe per scope) |
| `pipe.expose` | Push child-scope data to parent scope |
| `pipe.collect ({ host, ... }: true)` | Harvest data from sibling scopes (cross-host) |
| `pipe.withProvenance` | Track source scope of collected data |
| `pipe.as "new-quirk-name"` | Rename pipe output (creates derived quirks) |
| `pipe.to [ den.aspects.target ]` | Route pipe data to specific aspects only |

## Cross-Scope Flow

```nix
# Upward: user data reaches host scope
den.policies.expose-prefs = { host, user, ... }:
  let inherit (den.lib.policy) pipe; in
  [ (pipe.from "prefs" [ pipe.expose ]) ];

# Lateral: collect from sibling hosts
den.policies.fleet-backends = { host, ... }:
  let inherit (den.lib.policy) pipe; in
  [ (pipe.from "http-backends" [
      (pipe.collect ({ host, ... }: true))
    ])
  ];
```

## Derived Quirks with `pipe.as`

```nix
den.policies.backends-to-monitoring = { host, ... }:
  let inherit (den.lib.policy) pipe; in
  [ (pipe.from "backends" [
      (pipe.transform (b: "${b.addr}:${toString b.port}"))
      (pipe.as "monitoring-targets")
    ])
  ];
```

Consumers of `monitoring-targets` receive transformed data. Consumers of `backends` are unaffected. `pipe.as` must target a different quirk than its source.

## Config-Dependent Thunks

Quirk values can depend on NixOS `config`:

```nix
den.aspects.my-service = {
  nixos.services.my-service.enable = true;
  firewall = { config, ... }: {
    ports = [ config.services.my-service.port ];
  };
};
```

Include ordering does NOT matter — consumers always see all available data regardless of include order.
