# Attributions

## Current Skill

- Skill: `mise-tools`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: original skill with cold-install guidance informed by an external bootstrap example

The skill remains independently authored. The source below prompted coverage of a missing operational branch;
the final semantics, bounds, and cautions were derived from Mise's documentation and runtime interface.

## Reference Source: Slow-Network Bootstrap

Applies to `references/install-and-activation.md`, "Bound a large or slow cold install."

- Upstream author: KevinNitroG
- Upstream project: [KevinNitroG/dotfiles](https://github.com/KevinNitroG/dotfiles)
- Source path: `README.md`
- Source commit: `6bee1ca798e07ef160f48690e15c0d75568d8910`
- Source file:
  <https://github.com/KevinNitroG/dotfiles/blob/6bee1ca798e07ef160f48690e15c0d75568d8910/README.md#4-slow-network>

## Influence Note

The upstream bootstrap example prompted explicit guidance for limiting Mise concurrency and extending network
timeouts during a large cold install. No wording or code was copied. This skill uses shorter timeout defaults,
distinguishes stalled reads from complete downloads, preserves caller overrides, and keeps install-specific
