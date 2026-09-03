# Migration & Community

## Migration Guides

- **From traditional flake to Den**: Start by wrapping existing configs in flake-parts modules, then gradually
  consolidate cross-cutting features into single aspect files. Replace `specialArgs` with top-level options.
- **From `den.ctx` to new API**: `den.ctx` forwards to `den.aspects` and `den.schema.<kind>.includes` with
  deprecation warnings. Split into three concerns: `den.aspects` for definitions, `den.policies` for topology,
  `den.schema.<kind>.includes` for activation.
- **Removed outright, no shim** (verified at den `e8e8de1e` on 2026-09-03): `den.stages` hard-throws from an
  `apply` on a hidden option, with a migration message pointing at `den.schema.<kind>.includes`;
  `den.lib.ctxApply` is gone; `meta.adapter` and `oneOfAspects` have no implementation and survive only in a
  docstring and an example template. Use `den.lib.aspects.fx.constraints.{exclude,substitute,filterBy}`.
- **Deprecated but still evaluating** (they warn): `den.ctx.<name>`, `den.lib.perHost`/`perUser`/`perHome`
  (semantics also changed), `den.lib.take.*`, and `den.lib.parametric.*`. Replace the last two with plain
  functions coerced to `{ includes = [ fn ]; }`.
- **From zero to Den**: See `templates/minimal` and `templates/default` in the Denful repo for starter
  templates.

## Real-World Implementations

- <https://github.com/mightyiam/infra> — Shahar "Dawn" Ori (pattern author)
- <https://github.com/vic/vix> — Victor Borja (Den author, primary `denful/den` maintainer)
- <https://github.com/GaetanLepage/nix-config> — Gaëtan Lepage
- <https://github.com/drupool/nixos-x260> — Pol Dellaiera (with blog post)
- <https://github.com/sini/nix-config> — Jason Bowman (den's second-heaviest contributor; also author of several
  standalone flake-parts libraries used by den-based configs — `gen-algebra`, `gen-schema`, `files`,
  `scope-engine`, `hm-wrapper-modules`)

## Community

- GitHub Discussions: <https://github.com/denful/den/discussions>
- Matrix room: `#dendritic:matrix.org`
