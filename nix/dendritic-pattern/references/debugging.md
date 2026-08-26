# Debugging Den Configs

Techniques for figuring out why a resolved config doesn't match what an
aspect/policy/entity declaration seems to say — as opposed to authoring new
aspects (see main SKILL.md). Ground truth lives in the *resolved* tree, not in
reading one aspect file in isolation; den's `includes`/`provides`/policy
composition means the value you see at the option path can come from anywhere
in the graph.

## Inspect the Resolved Config

```bash
# Repl helper if the flake defines one, otherwise plain nix repl
just repl
nix repl
:lf .
nixosConfigurations.igloo.config.services.foo.enable
```

This is the actual merged value — check it before assuming which aspect
"should" have won.

## Expose Den Internals Temporarily

```nix
# In a scratch module, NOT committed:
flake.den = den;
```

Lets you inspect `den`'s internal aspect tree from the repl
(`den.aspects.igloo`, etc.) without going through a full host build.

## Resolve One Aspect in Isolation

```nix
den.lib.aspects.resolve "nixos" den.aspects.igloo
```

Expands a single aspect's tree without paying for a full
`nixosConfigurations.<host>.config` build — useful when you know which aspect
is suspect and want its output directly.

## See Which Policies Route to an Entity

```nix
den.lib.policyInspect.inspect { kind = "host"; context = { host = …; }; }
```

Shows which policies den would dispatch for a given entity, cutting through
`includes`/`excludes` composition to answer "why does/doesn't this entity have
that policy's effect."

**Two blind spots.** `inspect` iterates `den.policies` — the registry, not the
activated set — so a policy it lists may never fire in your build. And it wraps
each call in `builtins.tryEval`, so a **throwing policy inspects as "no
effects"** instead of as a failure. If you use throwing policies to enforce
entity invariants (den's only enforcement mechanism), `inspect` is exactly the
wrong tool to verify them with.

## Trace Aspect Includes

```nix
den.lib.capture
```

Captures a trace of aspect resolution (which `includes` pulled in what, from
where). The companion [`denful/den-diagram`](https://github.com/denful/den-diagram)
repo renders these traces visually — optional, reach for it only when a text
trace isn't enough to see the shape of the graph.

## Temporary `builtins.trace`/`builtins.break`

```nix
den.aspects.foo.includes = builtins.trace "foo includes: ${builtins.toJSON (map (a: a.meta.loc) den.aspects.foo.includes)}" [ ... ];
```

Insert directly in the suspect expression (an `includes` list, a `provides`
route, a policy pipe stage), remove before committing.

## Common Symptom Patterns

- **Duplicate values in a resolved list** — a parametric `includes` function
  (e.g. `{ host, user }: [ ... ]`) re-running once per resolution context stage
  rather than once overall. Check whether the function genuinely needs to be
  parametric, or whether a static `includes` list would do.
- **`perHost`/`perUser`/`perHome` shims** are deprecated in favor of plain
  parametric functions (`{ host, ... }: { ... }`) — if an aspect still uses one
  of these shims and behaves oddly around per-entity variation, migrate it
  first before debugging further.
- **Wrong config class evaluated (nixos vs. darwin vs. homeManager)** — check
  the entity's `class` (auto-derived from `system`/platform, or set explicitly)
  before assuming an aspect's logic is broken; a wrong/missing class routes the
  aspect against the wrong module system entirely.
- **A module "does nothing"** — confirm it's actually loaded first:
  underscore-prefixed files/dirs (`_nixos/`, `_foo.nix`) are deliberately
  skipped by `import-tree`, and in a git-backed flake, untracked new files are
  invisible to evaluation regardless of naming. Rule both out before
  suspecting the aspect's logic.
- **`den.ctx` behaving inconsistently** — it's a legacy compatibility shim
  forwarding to `den.aspects`/`den.schema.<kind>.includes`; migrate off it
  rather than debugging its forwarding behavior.

## Validate the Fix

Rebuild/re-eval every entity that transitively includes the aspect/policy that
changed, not just the one originally reported — shared aspects affect entities
that weren't part of the original symptom.
