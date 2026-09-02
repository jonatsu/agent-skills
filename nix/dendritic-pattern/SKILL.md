---
name: dendritic-pattern
description: "Denful dendritic pattern for Nix Flakes — aspect-oriented, context-driven configuration composition. Use when setting up Denful, writing aspects, declaring hosts/users/homes, using policies, quirks, namespaces, custom classes, migrating from traditional Nix layout, or debugging why an aspect/policy/entity isn't resolving as expected. Triggers on: denful, den, dendritic, aspect, den.aspects, den.hosts, den.homes, den.batteries, import-tree, flake-parts module, provides, includes, context dispatch, debug den, resolve aspect, policyInspect, den.lib."
metadata:
  author: Joonas Onatsu
  license: MIT
---

# Denful Dendritic Pattern

IRON LAW: Every `.nix` file in `modules/` is a top-level flake-parts module contributing to `den.aspects.*`.
NEVER create host-specific monolith files. One feature = one aspect, spanning all config classes (nixos,
darwin, homeManager) it touches.

## Revision Pinning ⚠️ REQUIRED

Every den API claim in this skill was read from den's source at **`2040b613`** (2026-08-10). **den is pre-1.0
— minor bumps carry breaking API changes**, and the consuming repo pins its own revision.

**First, check the gap.** `nix flake metadata --json | jq -r '.locks.nodes.den.locked.rev'` gives the repo's
pin. If it differs from `2040b613`, treat the four dated claim sets below as unverified until re-checked, and
verify anything you are about to write by reading the declaration in the pinned den — never by reading den's
docs, which were found materially wrong at this revision (`batteries.mdx` omits `flake-scope`; the example
template references `oneOfAspects` and `nix/lib/aspects/adapters.nix`, neither of which exists).

**Re-check after any `nix flake update den`:**

| Claim set                                                    | Where                                                | Verify by reading                                                                             |
| ------------------------------------------------------------ | ---------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| The 15 `den.batteries.*` and the auto-activated integrations | Built-in Batteries                                   | `modules/aspects/batteries/` — grep for `den.batteries.` definition sites                     |
| Removed vs deprecated APIs                                   | Anti-Patterns, references/migration.md               | `modules/removed-stages.nix`, `modules/compat/`, `nix/lib/take.nix`, `nix/lib/parametric.nix` |
| Silent-failure rules                                         | Silent Failures                                      | `nix/lib/aspects/fx/arg-class.nix`, `nix/lib/synthesize-policies.nix`                         |
| `forward` / `route` / `deliver` signatures                   | references/custom-classes.md, references/policies.md | `nix/lib/forward.nix`, `nix/lib/policy-effects.nix`                                           |

Read a remote den with `ctx_git_read` against `github.com/denful/den` at the pinned rev. Do NOT clone it
locally and do NOT point a subagent at a local clone.

## Workflow

```text
Dendritic Pattern Progress:

- [ ] Step 1: Identify the feature ⚠️ REQUIRED
  - [ ] 1.1 What feature is being added or modified?
  - [ ] 1.2 Which config classes does it touch? (nixos, darwin, homeManager)
  - [ ] 1.3 Is it a host, user, or shared aspect?
- [ ] Step 2: Choose aspect shape
- [ ] Step 3: Write the aspect module
- [ ] Step 4: Wire into entity (host/user/home)
- [ ] Step 5: Verify ⚠️ REQUIRED
```

## Core Concepts

### What is Denful?

Denful (`den`) is a Nix framework that inverts traditional host-first configuration into **feature-first
(aspect-oriented)** composition. Instead of "host → services", it's "feature → [nixos, homeManager, darwin]
contexts".

- **Aspect** = a feature written once, applied across all config classes it touches
- **Context-driven dispatch** = function parameters determine when an aspect runs
- **No `enable` flags** = importing a module = enabling the feature
- **No `specialArgs`** = top-level options accessible everywhere, no forwarding chains

### Entry point (flake.nix)

```nix
{
  outputs = inputs: inputs.flake-parts.lib.mkFlake
    { inherit inputs; }
    (inputs.import-tree ./modules);

  inputs = {
    den.url = "github:denful/den";
    flake-parts.url = "github:hercules-ci/flake-parts";
    import-tree.url = "github:vic/import-tree";
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    home-manager = {
      url = "github:nix-community/home-manager";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
}
```

`flake.nix` is a dependency manifest. ALL logic lives in `modules/`. Entry point rarely changes after initial
setup.

### Framework import (modules/dendritic.nix)

```nix
{ inputs, ... }: {
  imports = [ inputs.den.flakeModule ];
}
```

This enables all `den.*` option namespaces.

### The `__functor` Pattern

Every aspect in Den has a default `__functor` that inspects context parameters to decide what to produce. Bare
attrsets and functions work directly — no wrapper required:

```nix
# Bare attrset — runs everywhere
{ nixos.firewall.enable = true; }

# Parametric function — runs only when context matches argument shape
{ host, user }: { nixos.networking.hostName = host.name; }
```

Den introspects function arguments at evaluation time. A function requiring `{ host, user }` is silently
skipped in contexts that only have `{ host }`. No conditionals, no `mkIf`, no `enable` — the context shape
**is** the condition.

### Context Arguments

Context arguments are pipeline parameters — NOT NixOS module arguments (`config`, `pkgs`, `lib`). Context is
evaluated *before* module evaluation, which is why it cannot cause infinite recursion.

| Context                   | When Available           | Example                                                             |
| ------------------------- | ------------------------ | ------------------------------------------------------------------- |
| `{}` (none)               | Always                   | `{ nixos.firewall.enable = true; }`                                 |
| `{ host }`                | Host scope               | `{ host }: { nixos.networking.hostName = host.name; }`              |
| `{ host, user }`          | User scope (within host) | `{ host, user }: { nixos.users.users.${user.userName} = { ... }; }` |
| `{ home }`                | Standalone home scope    | `{ home }: { homeManager.home.username = home.userName; }`          |
| `{ class, aspect-chain }` | Static aspect leaf       | `{ class }: { ${class}.foo = true; }`                               |

**Flat form** — context args and module-system args can be mixed in a single function:

```nix
# Flat form — host from context, config/pkgs from module system
den.aspects.my-aspect = {
  nixos = { host, config, pkgs, ... }: {
    networking.hostName = host.name;
    environment.systemPackages = [ pkgs.git ];
  };
};
```

**MUST include `...`** in flat-form class modules — the module system passes extra args that cause eval errors
without it. Exception: if ALL args are context args (e.g., `{ host }:` with no `...`), the function is called
directly by Den and never reaches the module system.

## Advanced Topics (in references/)

Load one ONLY when its trigger fires. **Do NOT load any of these to write an ordinary aspect** — the body
above covers aspect shapes, entity wiring, batteries, and silent failures. Loading references speculatively is
the most common way this skill wastes its own context budget.

| Reference                                                       | Load when                                                                                       |
| --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| [policies.md](references/policies.md)                           | Writing or debugging a policy, enforcing an entity invariant, or reading `policyInspect` output |
| [quirks-and-pipes.md](references/quirks-and-pipes.md)           | Aggregating data across aspects (`den.quirks`, `pipe.*`)                                        |
| [namespaces.md](references/namespaces.md)                       | Publishing or consuming a `den.ful.<name>` aspect library                                       |
| [custom-classes.md](references/custom-classes.md)               | Declaring a new class, or calling `den.batteries.forward` / `policy.route`                      |
| [schema-and-resolution.md](references/schema-and-resolution.md) | Entity options, freeform vs strict, custom entity kinds, or tracing the resolution pipeline     |
| [migration.md](references/migration.md)                         | Porting an existing config, or hitting a removed/deprecated API                                 |
| [debugging.md](references/debugging.md)                         | A resolved config does not match what the declarations say                                      |

## Step 1: Identify the Feature ⚠️ REQUIRED

Ask:

- What is the feature? (bluetooth, gaming, dev-tools, ssh, desktop)
- Which config classes does it touch? (nixos, darwin, homeManager)
- Is it tied to a specific host/user, or shared across all?

**Aspect types:**

- **Host aspect** — named after a host (e.g., `den.aspects.igloo`)
- **User aspect** — named after a user (e.g., `den.aspects.tux`)
- **Shared aspect** — named after a feature (e.g., `den.aspects.bluetooth`)

## Step 2: Choose Aspect Shape

### Static (plain attrset)

```nix
den.aspects.bluetooth = {
  nixos.hardware.bluetooth.enable = true;
  homeManager.services.blueman-applet.enable = true;
};
```

### Parametric (context-driven)

```nix
den.aspects.my-feature = { host, user, ... }: {
  nixos = lib.optionalAttrs (host ? gpu) {
    hardware.nvidia.enable = true;
  };
  homeManager.programs.some-tool.enable = true;
};
```

**Context shape IS the condition.** No `mkIf`, no `enable` flags.

- `{ ... }` → runs everywhere
- `{ host }: ...` → runs only when host context exists
- `{ host, user }: ...` → runs only when both contexts exist

### Bare function (no wrapper needed)

```nix
den.aspects.simple = { nixos.networking.firewall.enable = true; };
```

### Additional Aspect Keys

| Key                           | Purpose                                                                                 |
| ----------------------------- | --------------------------------------------------------------------------------------- |
| `includes`                    | DAG edges — list of aspects/policies to compose                                         |
| `excludes`                    | Suppress policies from firing in this subtree (authoritative over child includes)       |
| `provides`                    | Named sub-aspects + cross-entity routing                                                |
| `meta`                        | Metadata submodule (name, loc, file, self + custom)                                     |
| `classes`                     | Class schemas declared by this aspect                                                   |
| `policies`                    | Inline policy definitions on the aspect                                                 |
| `name`, `description`, `into` | Also structural — the pipeline handles them, they are never class or nested-aspect keys |

**Key classification order is pipe → class → nested aspect.** Every other key is tested in that order, and the
first match wins:

1. Structural keys above (extend the set with `den.reservedKeys`)
2. Registered `den.quirks` names — see references/quirks-and-pipes.md, a collision here silently swallows a
   nested aspect
3. Registered `den.classes` names, but only when the value looks like module content — a flat scalar attrset
   such as `{ name = "x"; }` under a class-named key is NOT treated as class content
4. Anything left carrying aspect structure becomes a nested aspect

## Step 3: Write the Aspect Module

### File placement

```
modules/
├── dendritic.nix       # framework import
├── hosts.nix           # entity declarations
├── defaults.nix        # global settings
├── aspects/            # shared aspects (optional split)
│   ├── bluetooth.nix
│   ├── gaming.nix
│   └── dev-tools.nix
├── igloo.nix           # host aspect
├── tux.nix             # user aspect
└── _nixos/             # _ prefix = ignored by import-tree (raw NixOS modules)
```

Any `.nix` file in `modules/` is auto-loaded by `import-tree`. Multiple files can contribute to the same
aspect (incremental features).

### Aspect with includes (DAG composition)

```nix
den.aspects.workstation = {
  includes = [
    den.aspects.dev-tools
    den.batteries.primary-user
    { nixos.programs.vim.enable = true; }          # inline static
    ({ host }: { nixos.time.timeZone = "UTC"; })    # inline parametric
  ];
  nixos.services.xserver.enable = true;
};
```

### Aspect with provides (sub-aspects + cross-entity routing)

```nix
den.aspects.igloo = {
  # Sub-aspect (conditional within this aspect)
  provides.gpu = { host, ... }:
    lib.optionalAttrs (host ? gpu) {
      nixos.hardware.nvidia.enable = true;
    };

  # Deliver to ALL users on this host
  provides.to-users.homeManager.programs.helix.enable = true;

  # Deliver to specific user
  provides.alice.homeManager.programs.vim.enable = true;
};

den.aspects.tux = {
  # Deliver to ALL hosts this user is on
  provides.to-hosts.nixos.programs.nh.enable = true;

  # Deliver to specific host
  provides.igloo.nixos.programs.emacs.enable = true;
};
```

## Step 4: Wire into Entity

### Declare hosts

```nix
# modules/hosts.nix
{
  den.hosts.x86_64-linux.igloo.users.tux = { };
  den.hosts.aarch64-darwin.mac.users.alice = { };
}
```

This single line:

- Creates host `igloo` with system `x86_64-linux`
- Auto-derives `class = "nixos"` from platform
- Creates user `tux` within host
- Auto-creates `den.aspects.igloo` (empty nixos class)
- Auto-creates `den.aspects.tux` (empty, context = `{host, user}`)
- Produces `nixosConfigurations.igloo` output

**Flat form also works** — declare the host directly and give it a `system`:

```nix
den.hosts.igloo = { system = "x86_64-linux"; };
```

den splits `den.hosts.*` keys into system groups and direct hosts by testing each key against
`lib.systems.flakeExposed`. A key that is not a known system is read as a host NAME, and such a host MUST
carry `system` or evaluation throws.

### Enable home-manager per user

```nix
# Per-user
den.hosts.x86_64-linux.igloo.users.tux.classes = [ "homeManager" ];

# Or globally (recommended)
den.schema.user.classes = lib.mkDefault [ "homeManager" ];
```

### Standalone homes (no root)

```nix
den.homes.x86_64-linux.tux = { };
# Produces homeConfigurations.tux

den.homes.x86_64-linux."tux@igloo" = { };
# Bound to host, home-manager CLI auto-selects by user@hostname
```

### Global defaults

```nix
# modules/defaults.nix
{ lib, ... }: {
  den.schema.user.classes = lib.mkDefault [ "homeManager" ];
  den.default = {
    nixos.system.stateVersion = "25.11";
    homeManager.home.stateVersion = "25.11";
    includes = [
      den.batteries.define-user
      den.batteries.inputs'
    ];
  };
}
```

`den.default` applies to ALL entities.

## Step 5: Verify ⚠️ REQUIRED

- [ ] `nix flake show` lists expected `nixosConfigurations` / `homeConfigurations`
- [ ] `nix flake check` passes
- [ ] `nix build .#nixosConfigurations.<host>.config.system.build.toplevel` succeeds
- [ ] No `specialArgs` pass-through chains
- [ ] No `enable` flags on aspects (import = enable)
- [ ] Raw NixOS modules prefixed with `_` if in `modules/`

## Built-in Batteries

Verified against den `2040b613` (2026-08-10). den is pre-1.0 and minor bumps carry breaking API changes —
re-check this table if your `flake.lock` pins a different revision.

**Exactly 15 attributes exist under `den.batteries.*`.** All are opt-in: a battery does nothing until it
appears in an `includes` list.

| Battery                                 | Purpose                                                                     |
| --------------------------------------- | --------------------------------------------------------------------------- |
| `den.batteries.define-user`             | Creates OS + home user accounts                                             |
| `den.batteries.flake-scope`             | Exposes flake scope to aspects                                              |
| `den.batteries.forward { each = …; … }` | Create custom Nix classes — `each` is REQUIRED                              |
| `den.batteries.host-aspects`            | Includes a user's host aspects into the user scope                          |
| `den.batteries.hostname`                | Sets hostname cross-platform                                                |
| `den.batteries.import-tree ./path`      | Auto-load .nix files per class; `.provides.{host,user,home}` variants exist |
| `den.batteries.inputs'`                 | flake-parts `inputs'` as module arg                                         |
| `den.batteries.insecure [ "pkg" ]`      | Allowlist insecure packages                                                 |
| `den.batteries.mutual-provider`         | Inert compatibility shim (see below)                                        |
| `den.batteries.primary-user`            | wheel group, primary user setup                                             |
| `den.batteries.self'`                   | flake-parts `self'` as module arg                                           |
| `den.batteries.tty-autologin "user"`    | TTY1 autologin                                                              |
| `den.batteries.unfree [ "pkg" ]`        | Allowlist unfree packages                                                   |
| `den.batteries.user-shell "fish"`       | Sets login shell OS + HM                                                    |
| `den.batteries.vm-autologin`            | TTY1 autologin for NixOS VMs                                                |

**`inputs'` and `self'` contain apostrophes.** Both are valid Nix identifiers. Omitting the apostrophe is the
most common "undefined argument" error, and it gets misread as a den limitation.

### Auto-activated integrations — NOT batteries

`os-class`, `os-user`, `wsl`, `home-manager`, `hjem`, and `maid` are real, live integrations, but
**`den.batteries.os-class` and friends do not exist**. They ship as built-in policies and class declarations
that activate on their own conditions (e.g. `os-class` declares `den.classes.os` and adds
`den.policies.os-to-host` to `den.default.includes`). Writing `includes = [ den.batteries.os-class ]` is an
error, not a no-op.

| Integration                      | Activates when                                                    |
| -------------------------------- | ----------------------------------------------------------------- |
| `os-class`                       | Always — routes `os` class into the host's `nixos`/`darwin` class |
| `os-user`                        | Always — routes `user` class into `users.users.<name>`            |
| `home-manager` / `hjem` / `maid` | Users carry the corresponding class                               |
| `wsl`                            | WSL support conditions are met                                    |

**`mutual-provider` is inert** — `provides.to-users` and `provides.to-hosts` are built-in.
`den.batteries.mutual-provider` still resolves so old configs keep evaluating, but it produces no effects.

## Aspect Meta-Data

Aspects have a `meta` submodule for attaching metadata:

```nix
den.aspects.igloo = {
  meta.description = "Primary laptop";
  meta.priority = "high";
  nixos.networking.hostName = "igloo";
};
```

Default `meta.*` attributes:

| Attribute | Description                                       |
| --------- | ------------------------------------------------- |
| `name`    | Submodule name (e.g., `"igloo"`)                  |
| `loc`     | Location path (e.g., `["den" "aspects" "igloo"]`) |
| `file`    | Last file where this aspect was defined           |
| `self`    | Reference to the aspect module `config`           |

Access meta from other aspects:

```nix
den.aspects.igloo.meta.name
```

Aspects are fixed-point — they can reference themselves via `config`:

```nix
den.aspects.igloo = { config, ... }: {
  meta.default-key = "Hello World!";
  homeManager.programs.gpg.settings.default-key = config.meta.default-key;
};
```

## Silent Failures

These produce NO error, NO warning, and NO output. Each one gets misread as "den cannot do this." Verified
against den `2040b613`.

- **A misplaced entity argument makes the aspect inert.** den classifies each entity-kind arg against the
  schema entity DAG: bindable from the current context, a descendant (fan-out), or **misplaced — and misplaced
  is silently inert**. At root scope there is no scope kind, so EVERY entity arg there is misplaced. An aspect
  written as `{ host, ... }:` at root scope simply never runs.
- **A policy only fires when the context supplies every non-defaulted argument.** `resolveArgsSatisfied` reads
  the function's argument pattern: `_:` and `{ ... }:` always fire; `{ host, ... }:` fires only in a
  host-bearing context. The argument pattern IS the scope selector — there is no separate predicate to check.
- **A class module requiring an absent den schema-kind arg is DROPPED**, and den's `lib.warn` rides on the
  discarded module, so the warning never prints. Scope: every `den.schema` key EXCEPT `conf` and `aspect`.
- **That rule does NOT extend to module-system args.** home-manager sets
  `_module.args.osConfig = lib.mkDefault null`, so on a standalone home `osConfig` is bound and **null**, not
  absent. Guard against null, not against absence.
- **Undeclared entity attributes are accepted silently and read back absent**, because entities are freeform
  by default. A typo'd key is not an error; it is a value you will never see again. Opt into strict checking
  (see references/schema-and-resolution.md).

## Anti-Patterns

- Using `specialArgs` to pass values between config classes — use let-bindings or `den.*` options
- Adding `enable` options to aspects — importing a module = enabling the feature
- Creating host-specific monolith files — one feature = one aspect
- Putting logic in `flake.nix` — all logic belongs in `modules/`
- Forgetting `_` prefix on raw NixOS modules in `modules/` — import-tree will try to load them
- **`lib.optionalAttrs` merged at the wrong depth** — a plain-Nix hazard, not a den one: `//` is a shallow
  merge, so gating an outer level replaces the shared name and drops its siblings. Gate the deepest shared
  name, or use `lib.recursiveUpdate`. See the `home-manager` skill's references/settings-trees-and-merges.md
- Using string references in `includes` — use real aspect references (`den.aspects.foo`)
- Mixing traditional `nixosConfigurations` with `den.hosts` — let Den manage entity declarations
- Creating separate files per config class (nixos.nix, homeManager.nix) — one aspect spans all classes
- **Using `den.ctx` instead of `den.aspects`/`den.schema`/`den.policies`** — `den.ctx.<name>` still evaluates
  but warns ("use `den.schema.<name>.includes`"). Migrate to the three-way split.
- **Writing `den.stages`** — REMOVED, and it hard-throws on any use. Replacement:
  `den.schema.<kind>.includes`.
- **Writing `den.lib.take.*` or `den.lib.parametric.*`** — both fully deprecated and warn. Use plain functions
  coerced to `{ includes = [ fn ]; }`.
- **Writing `meta.adapter`, `den.lib.ctxApply`, or `oneOfAspects`** — removed with no shim, or never existed.
  den's own example template still references `oneOfAspects` and `nix/lib/aspects/adapters.nix`; neither
  exists. The real API is `den.lib.aspects.fx.constraints.{exclude,substitute,filterBy}`.
- **Forgetting `...` in flat-form class modules** — the module system passes extra args that cause eval errors
  without it.
- **Using `pipe.as` with the same quirk name as source** — throws an error. Must target a different quirk.
- **Declaring a policy without activating it** — registering in `den.policies` only adds to the registry. Must
  appear in an `includes` list to fire.
- **Expecting child `includes` to override parent `excludes`** — parent excludes are authoritative.
- **Confusing `class` (nixos/darwin/homeManager — module evaluation domain) with entity kind (host/user/home —
  Den data type)** — classes determine which module system evaluates; entity kinds determine how policies
  dispatch.

## Pre-Delivery Checklist

- [ ] `flake.nix` is minimal (dependency manifest only)
- [ ] `modules/dendritic.nix` imports `inputs.den.flakeModule`
- [ ] All aspects use `den.aspects.*` namespace
- [ ] Entities declared via `den.hosts` / `den.homes`
- [ ] `den.default` sets `stateVersion` for nixos and homeManager
- [ ] `nix flake check` passes
- [ ] No `specialArgs` pass-through chains
- [ ] No `enable` flags on aspects
- [ ] No `den.ctx` usage (migrate to `den.aspects`/`den.schema`/`den.policies`)
- [ ] Flat-form class modules include `...` (unless all args are context args)
- [ ] Custom policies activated via `includes` (not just registered)
- [ ] No `pipe.as` targeting same quirk as source
- [ ] `meta` used for aspect metadata (not ad-hoc top-level keys)
