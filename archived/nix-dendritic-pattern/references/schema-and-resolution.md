# Schema & Resolution

## Schema: Shared Options Across Entity Kinds

`den.schema` defines options that apply to every entity of a given kind:

```nix
{
  # All hosts
  den.schema.host.home-manager.enable = true;

  # All users
  den.schema.user = { user, lib, ... }: {
    options.groupName = lib.mkOption { default = user.userName; };
  };

  # Shared across ALL entity kinds
  den.schema.conf = {
    options.copyright = lib.mkOption { default = "Copy-Left"; };
  };
}
```

## Entity Options Reference

### Host options

| Option        | Default          | Description                                               |
| ------------- | ---------------- | --------------------------------------------------------- |
| `name`        | attrset key      | Configuration name                                        |
| `hostName`    | `name`           | Network hostname                                          |
| `system`      | parent key       | `x86_64-linux`, `aarch64-darwin`, etc.                    |
| `class`       | auto from system | `"nixos"` or `"darwin"`                                   |
| `aspect`      | `name`           | Primary aspect name                                       |
| `instantiate` | class-dependent  | `lib.nixosSystem`, `darwinSystem`, etc.                   |
| `intoAttr`    | class-dependent  | Flake output path                                         |
| `users`       | `{}`             | User account definitions                                  |
| `*`           | freeform         | Custom attributes accessible via `host.<attr>` in aspects |

### User options

| Option     | Default      | Description                                    |
| ---------- | ------------ | ---------------------------------------------- |
| `name`     | attrset key  | User configuration name                        |
| `userName` | `name`       | System account name                            |
| `aspect`   | `name`       | Primary aspect name                            |
| `classes`  | `[ "user" ]` | Nix classes this user participates in          |
| `*`        | freeform     | Custom attributes accessible via `user.<attr>` |

### Home options

| Option        | Default                                   | Description                                     |
| ------------- | ----------------------------------------- | ----------------------------------------------- |
| `name`        | attrset key                               | Home configuration name                         |
| `userName`    | `name`                                    | User account name                               |
| `hostName`    | —                                         | Host binding, set by the `"user@host"` key form |
| `system`      | parent key                                | Platform system                                 |
| `class`       | `"homeManager"`                           | Home class                                      |
| `aspect`      | `name`                                    | Primary aspect name                             |
| `pkgs`        | `inputs.nixpkgs.legacyPackages.${system}` | nixpkgs instance                                |
| `instantiate` | `homeManagerConfiguration`                | Builder function                                |
| `*`           | freeform                                  | Custom attributes                               |

## Freeform Attributes

Host, user, and home types all use `freeformType` — attach arbitrary data without declaring options:

```nix
den.hosts.x86_64-linux.igloo = {
  gpu = "nvidia";
  datacenter = "eu-west";
};
```

Access in aspects via context:

```nix
den.aspects.igloo.includes = [
  ({ host, ... }: lib.optionalAttrs (host ? gpu) {
    nixos.hardware.nvidia.enable = true;
  })
];
```

## Strict Mode

**Entities are freeform by default (`strict = false`).** An undeclared attribute is accepted SILENTLY and
reads back absent — a typo is not an error, it is a value you will never see again. Strict checking is opt-in,
two ways:

```nix
# Whole flake
imports = [ inputs.den.flakeModules.strict ];

# Per entity kind
den.schema.host = den.lib.strict;
```

The flake module is just the per-kind form applied to `host`, `user`, `aspect`, `home`, and `flake`.

## Entity Registries

**den declares exactly two instance registries: `den.hosts` and `den.homes`.** Declaring `den.schema.<kind>`
does NOT mint a `den.<kind>s` registry — custom entity kinds are supported, but the registry for one has to be
hand-declared.

`den.schema.<kind>.parent` drives the entity ancestor DAG that den walks to classify every entity-kind
argument. It is never dead code: get it wrong and arguments that should bind become "misplaced", which is
silently inert.

## Eval-Time Fetches

den calls `builtins.fetchTarball` for `gen-schema` (`nix/lib/schema.nix`) and `nix-effects` (`nix/lib/fx.nix`)
during evaluation unless the consuming flake supplies those inputs. Dropping the input does not remove the
dependency; it hands the pin to den's CI lock instead of yours.

## Resolution Pipeline

When Den evaluates a host, it runs a resolution pipeline driven by policies:

1. **Host resolution** — For each `den.hosts.<system>.<name>`, create a `host` scope. Resolve host aspect via
   `den.schema.host.includes`.

2. **Core policy fan-out** — `host-to-users` policy fans out one `{ host, user }` pair per user declared on
   the host. `den.default` is injected as a schema include for host, user, and home — no separate
   `*-to-default` policies.

3. **Battery policies forward user environments** — Home-environment batteries (homeManager, hjem, maid) share
   a factory. Fan-out policy fires when battery is enabled, host OS is supported, and host has users of the
   battery's class. Each matching user is forwarded into the target namespace (e.g.,
   `home-manager.users.<name>`).

4. **Deduplication** — Pipeline tracks seen include keys, keyed by `"${scope}/${identityKey}"`. First
   inclusion resolves full aspect; subsequent includes of same aspect in same scope are skipped. Different
   scopes each get their own copy.

5. **Home configurations** — Standalone `den.homes` entries follow a separate path via flake policies. Home
   scopes have no `host` in context, so policies requiring `{ host }` are not activated.

6. **Output** — Flake-level policies drive final assembly. `flake-to-systems` fans out per system.
   `system-to-os-outputs` resolves hosts, `system-to-hm-outputs` resolves homes. Each entity is instantiated
   and placed at its `intoAttr` path.
