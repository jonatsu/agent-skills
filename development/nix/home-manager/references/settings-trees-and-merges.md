# Settings Trees and Merges

Traps that hit when writing a **nested settings tree** consumed by a generator — `programs.<tool>.settings`,
plasma-manager's `configFile`, cosmic-manager's `configFile`, any freeform submodule rendered to a file.

Trap 1 is a **Nix language** fact and applies to every attrset you write, config tree or not. Traps 2–4 are
module-system and generator behaviour.

Traps 1, 2 and 4 are **invisible to `nix eval`**: the option really does hold what you wrote, and only the
rendered file shows the damage. Trap 3 is the opposite — it throws loudly at eval, and the error names a field
you never touched.

- [Trap 1: `//` is a shallow merge, always](#trap-1--is-a-shallow-merge-always)
- [Trap 2: a nullable submodule parent drags in sibling defaults](#trap-2-a-nullable-submodule-parent-drags-in-sibling-defaults)
- [Trap 3: submodule options without defaults and without `emptyValue`](#trap-3-submodule-options-without-defaults-and-without-emptyvalue)
- [Trap 4: freeform submodules accept typos](#trap-4-freeform-submodules-accept-typos)
- [Verification: build the artefact and read it](#verification-build-the-artefact-and-read-it)

## Trap 1: `//` is a shallow merge, always

Plain Nix, nothing to do with modules or generators: `//` considers only the TOP-LEVEL names of its two
operands. A name present on both sides is REPLACED, never merged, however deep the value goes.

```nix
{ a = { x = 1; }; } // { a = { y = 2; }; }
# => { a = { y = 2; }; }        `x` is gone
```

This is exactly why `lib.recursiveUpdate` exists. Reach for it whenever both sides may share a name:

```nix
lib.recursiveUpdate { a = { x = 1; }; } { a = { y = 2; }; }
# => { a = { x = 1; y = 2; }; } (last wins per LEAF, not per top-level name)
```

Inside ONE attrset literal there is no `//` and no problem — nested attribute paths merge:

```nix
{ a.x = 1; a.y = 2; }         # => { a = { x = 1; y = 2; }; }
```

It bites hardest where a `//` is introduced later, to make part of a literal conditional. `lib.optionalAttrs`
returns an attrset, so it needs a `//` — and the obvious place to put that is the outermost one, which is the
wrong depth:

```nix
# DESTROYS [General]: the right-hand `kdeglobals` replaces the left's outright
{ kdeglobals.General.TerminalService = "kitty.desktop"; }
// lib.optionalAttrs cond { kdeglobals.KScreen.XwaylandClientsScale = true; }

# CORRECT: gate at the deepest name the two sides share
{
  kdeglobals.General.TerminalService = "kitty.desktop";
  kdeglobals.KScreen = lib.optionalAttrs cond { XwaylandClientsScale = true; };
}
```

Pick the tool by what you are merging:

| Situation                                               | Use                                                                        |
| ------------------------------------------------------- | -------------------------------------------------------------------------- |
| Gating one group inside a literal                       | `lib.optionalAttrs` at that group's own name                               |
| The value is an OPTION                                  | `lib.mkIf` / `lib.mkMerge` — the module system merges by the option's type |
| Two plain attrsets that may share names at any depth    | `lib.recursiveUpdate`                                                      |
| Two plain attrsets, guaranteed-disjoint top-level names | `//` is fine                                                               |

NEVER use `//` to combine two trees that share a name unless you intend the right-hand side to win wholesale.
The failure is silent: no error, no warning, and the merged value is exactly what `nix eval` reports.

## Trap 2: a nullable submodule parent drags in sibling defaults

Third-party modules following the nixvim `defaultNullOpts` convention type a group as
`nullOr (submodule { … })` with `default = null`, so nothing is written until you touch it. Setting ANY child
makes the parent non-null — and every sibling child carrying a NON-null default now materialises too.

That is how declaring a keyboard layout under cosmic-manager's `compositor` also wrote
`descale_xwayland = false`, which the compositor reads as "disable XWayland fractional scaling" while its own
default is "fractional". A library's default can lag the program's.

MUST, before setting one field of a typed group, enumerate its siblings and their defaults. Two ways, in order
of reliability:

```bash
# read the option declarations in the module's own source — authoritative
nix eval --raw '<flake>#<module-attr>.outPath'   # then grep the mkOption block

# or dump what the group actually resolves to once you have set your field
nix eval --json '.#nixosConfigurations.<host>.config…<group>'
```

The second is the one that catches this trap: a sibling you never mentioned showing up in that JSON with a
non-null value IS the bug. Then check each against the program's own default, not the module's.

When the generator writes one file per top-level key, writing that key directly (freeform) instead of through
the typed parent avoids the coupling entirely.

## Trap 3: submodule options without defaults and without `emptyValue`

An option declared `mkOption { type = …; }` with no `default` has no value. But whether evaluating that unset
value throws depends on whether its **type carries an `emptyValue`** — nixpkgs' `lib/modules.nix` tests
`type.emptyValue ? value` before it throws.

A generator that walks the submodule with `mapAttrs` + `filterAttrs` (a recursive null-strip) forces every
value. If any declared option has a type WITHOUT an `emptyValue`, the walk fails with:

```
error: The option `foo.b' was accessed but has no value defined. Try setting the option.
```

Reading one field directly, or `builtins.attrNames`, is safe; only forcing a value's evaluation throws.

| Type                                                                                                     | Has `emptyValue`? | Behaviour when unset        |
| -------------------------------------------------------------------------------------------------------- | ----------------- | --------------------------- |
| `str`, `bool`, `int`, `float`, `path`, `package`, `enum`, `either`, `lines`, `commas`, `anything`, `raw` | No                | **throws**                  |
| `nullOr X`, `attrsOf`, `lazyAttrsOf`, `listOf`, `submodule`, `attrs`, `unique` wrapping one of those     | Yes               | silently yields empty value |

Measured on nixpkgs master `af8ad534c6dc23cac562c372e66d81f2bb487b9a` (2026-09-06, `lib/types.nix` +
`lib/modules.nix`); the error string is that rev's wording.

Either supply a `default`, use a type with an `emptyValue`, or declare it as `types.nullOr X`. Declaring
`default = null` on a non-nullable type does not help — it swaps the "no value" error for a type-check
failure.

**On cosmic-manager:** the pattern `cleanNullsExceptOptional` (recursive `filterAttrs` + `mapAttrs`) is in
that repo's source, but the live consumer walks a constructed attrset, not the submodule's config as a whole.
The mechanism is real; the attribution shows where the pattern was read, not an observed failure there.

## Trap 4: freeform submodules accept typos

`freeformType = attrsOf anything` means an unknown key is ACCEPTED, silently, and read back by nobody. A typed
settings submodule therefore gives NO protection against a misspelled setting name — the type only checks
declared keys you already spelled right.

Do NOT justify choosing a typed surface over a freeform write on "type safety" grounds when the submodule is
freeform. Both need the artefact read.

## Verification: build the artefact and read it

`nix eval` proves an option is SET. It does not prove the generator wrote it, that it survived a merge, or
that the tool reads that key or file. For a generator wired through an activation script:

```bash
# 1. the activation entry — note this is usually a WRAPPER SCRIPT, not the
#    generated config; expect to follow it one more hop (see below)
nix eval --raw '.#nixosConfigurations.<host>.config.home-manager.users.<user>.home.activation.<entry>.data'

# 2. realise any store path you land on. It is NOT built yet, so ask for its
#    deriver — which works on an unbuilt path — and build that
nix path-info --derivation /nix/store/<hash>-<name>
nix build --no-link '/nix/store/<hash>-<name>.drv^out'

# 3. read it. If it is a script, the real config is a path INSIDE it —
#    repeat step 2 on that path, then read the result
```

**Expect two hops, not one.** plasma-manager's `configure-plasma` entry points at a `plasma-config` script
whose single line invokes `write_config` against a separate `data.json` — the JSON is the artefact worth
reading, and step 1 never names it. cosmic-manager is the same shape via `configurations.json`. Reading only
the first path shows you a wrapper and tells you nothing.

Do NOT go hunting for the `.drv` by listing the store: `nix path-info --derivation` answers it directly,
unbuilt path or not.

When you have an attribute rather than a path, `nix derivation show <installable>` skips step 2 entirely —
note its output nests under a top-level `derivations` key, so indexing `.[].outputs` fails.

MUST confirm both branches of any gate this way, not just the one you expect to be taken.
