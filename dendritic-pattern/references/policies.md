# Policies

Policies declare *how entities relate* — the directed edges that connect entity kinds, enrich context, route content, and drive structured data flow.

## What is a Policy?

A policy is a function from context to a list of effects. The pipeline calls it when all required context args are present:

```nix
den.policies.host-to-users = { host, ... }:
  map (user: policy.resolve.to "user" { inherit host user; })
    (lib.attrValues host.users);
```

Policies are **first-class values** — they live in `den.policies` as a registry, and are **activated** by including them in `includes` lists.

## Policy Graph

```text
flake → flake-to-systems → system
system → system-to-os-outputs → host
system → system-to-hm-outputs → home
host → host-to-users → user
host → host-to-hm-users → home-manager users
```

## Writing a Policy

```nix
let inherit (den.lib.policy) resolve; in
den.policies.my-enrichment = { host, ... }:
  [ (resolve { myFlag = true; }) ];
```

## Policy Effects

| Effect | Purpose |
|--------|---------|
| `policy.resolve { bindings }` | Enrich current scope (non-entity keys) or create child scope (entity keys) |
| `policy.resolve.to "user" { inherit host user; }` | Create child entity scope |
| `policy.include den.aspects.monitoring` | Inject aspect through the tree (participates in full resolution) |
| `policy.provide { class = "nixos"; module = { ... }; }` | Deliver raw module directly to class (bypasses tree) |
| `policy.exclude den.policies.foo` | Suppress a policy in subtree |
| `policy.route { fromClass = "user"; intoClass = "nixos"; path = ["users" "users"]; }` | Move class content between scopes |
| `policy.instantiate ...` | Control entity instantiation |
| `policy.spawn ...` | Create detached scope |
| `policy.pipe ...` | Route quirk data (see Quirks section) |
| `policy.deliver { from; to; at; mode; }` | The delivery primitive `route`/`provide` desugar onto |

`route` and `provide` are **PERMANENT user-API sugar**, not migration debt. Both desugar onto one `deliver` edge: `route` maps `fromClass`→`from`, `intoClass`→`to`, `path`/`intoPath`→`at`; `provide` maps `class`→`to`. `mode` is `merge`, `nest`, or `verbatim` — anything else throws. den's own source calls `route` "Tier 1 delivery — replaces `den.batteries.forward` for the common case", so `route` is the general class→class primitive, NOT a flake-parts special case.

## `policy.include` vs `policy.provide`

| | `policy.include` | `policy.provide` |
|---|---|---|
| Path | Walks through the aspect tree | Bypasses the tree entirely |
| Dedup | Subject to include dedup | Deduped by policy/class/path |
| Use when | Injecting aspects for full resolution | Delivering raw modules directly to a class |

## Activation

Declaring a policy only **registers** it. A policy fires only when it appears in an `includes` list:

```nix
# Register
den.policies.my-enrichment = { host, ... }: [ /* effects */ ];

# Activate for all hosts
den.schema.host.includes = [ den.policies.my-enrichment ];

# Activate globally
den.default.includes = [ den.policies.my-enrichment ];

# Activate for specific aspect subtree
den.aspects.igloo.includes = [ den.policies.my-enrichment ];
```

Built-in core policies are always active via `den.schema.*.includes`.

## Deactivation with `excludes`

`excludes` is a first-class key on aspects, symmetric with `includes`. Parent excludes are **authoritative** — child scopes cannot re-enable an excluded policy:

```nix
den.aspects.igloo = {
  includes = [ den.policies.add-marker ];
  excludes = [ den.policies.add-marker ];  # blocks in igloo subtree
};
```

## Conditional Policies

```nix
# Fire only for a specific entity
den.lib.policy.for entity den.policies.igloo-specific

# Fire only when predicate is true
den.lib.policy.when ({ host, ... }: host.wsl.enable) den.policies.wsl-support

# Compose wrappers
den.lib.policy.when (ctx: ctx.flag or false)
  (den.lib.policy.for entity den.policies.my-policy)
```

Wrappers preserve inner policy identity — `excludes` still matches the wrapped policy.

## When a Policy Fires

A policy fires only when the context supplies every **non-defaulted** argument in its pattern (`resolveArgsSatisfied`):

| Pattern | Fires |
|---------|-------|
| `_:` | Always |
| `{ ... }:` | Always |
| `{ host, ... }:` | Only in a host-bearing context |
| `{ host, user, ... }:` | Only where both are bound |

The argument pattern IS the scope selector. There is no separate predicate to configure.

## Enforcing Entity Invariants

**den ships no entity validator and no assertion primitive.** `validators` appears nowhere in den's source at `2040b613`, so a `den.schema.<kind>.validators` key is silently accepted by the freeform schema and never read. A **throwing policy is the only way** to enforce an entity invariant:

```nix
den.policies.require-timezone = { host, ... }:
  if host ? timeZone then [ ] else throw "host ${host.name}: timeZone is required";
```

## `den.lib.policyInspect.inspect`

```nix
den.lib.policyInspect.inspect { kind = "host"; context = { host = …; }; }
# => { <policyName> = { targetKey; targets; from; to; as; routing; }; }
```

**Two blind spots — know them before trusting the output:**

1. It iterates `den.policies`, the **registry**, not the activated set. A policy shown here may never fire in your build.
2. It wraps each policy call in `builtins.tryEval`, so a **throwing policy inspects as "no effects"** rather than as a failure.

Together those defeat using `policyInspect` to verify the enforcement pattern above: the throwing guard that protects your fleet is exactly the policy `inspect` reports as inert.
