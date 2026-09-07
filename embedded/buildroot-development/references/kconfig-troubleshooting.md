# Kconfig / menuconfig Troubleshooting

Why a `BR2_*` symbol will not appear, what "unmet direct dependencies" means and how to clear it, the difference between
`depends on`, `select`, and `imply`, and how to break a recursive-dependency error. Buildroot's configuration is
Kconfig, the same engine the kernel uses, so these rules are general.

For package `Config.in` authoring, see `buildroot-packages.md`. For the release drift that renames or removes symbols,
see the SKILL's *Version awareness*.

## Contents

- [How Visibility Works](#how-visibility-works)
- [Finding a Symbol and Why It Is Hidden](#finding-a-symbol-and-why-it-is-hidden)
- [`depends on` vs `select` vs `imply`](#depends-on-vs-select-vs-imply)
- ["Unmet Direct Dependencies"](#unmet-direct-dependencies)
- [Recursive-Dependency Errors](#recursive-dependency-errors)
- [Symbol Renamed or Removed Across Releases](#symbol-renamed-or-removed-across-releases)
- [Evidence Commands](#evidence-commands)
- [Worked Example: an invisible option and an unguarded select](#worked-example-an-invisible-option-and-an-unguarded-select)

## How Visibility Works

A symbol's prompt is shown only when ALL of its `depends on` conditions are satisfied. Fail one and the option does not
merely default off — it DISAPPEARS from the menu entirely, with no message. "I cannot find the option for X" is almost
always an unmet `depends on`, not a missing package.

A hidden symbol also cannot be set from a defconfig: writing `BR2_PACKAGE_FOO=y` into a defconfig whose dependencies are
unmet is silently dropped when the config is loaded. You MUST satisfy the dependency first.

## Finding a Symbol and Why It Is Hidden

Search inside `make menuconfig`: press `/`, type the symbol or a fragment, and read the result. Kconfig reports the
symbol's prompt, its `Depends on` expression, its `Location` (the menu path), and what selects it. Any `Depends on` term
currently evaluating false is the reason the prompt is hidden.

When menuconfig itself is not handy, grep the release's Config.in files — the symbol's definition shows its dependencies
directly:

```bash
grep -rn "BR2_PACKAGE_FOO\b" package/ */Config.in
```

## `depends on` vs `select` vs `imply`

These three read similarly and behave very differently. Confusing them is the root of most Kconfig grief.

- **`depends on X`** — a visibility and value gate. The option is available only when `X` is true. Non-forcing, and it
  never turns `X` on for you.
- **`select X`** — force-enables `X` and holds it on. Its trap: `select` does NOT evaluate `X`'s own `depends on`. It
  can therefore switch `X` on even when `X`'s dependencies are unmet, which is exactly what produces an "unmet direct
  dependencies" warning. Reserve `select` for leaf symbols with few or no dependencies.
- **`imply X`** — sets `X` to default-on but lets the user turn it back off, and it respects `X`'s visibility. It is the
  polite, non-forcing cousin of `select`.

Rule of thumb: gate with `depends on`, nudge with `imply`, and use `select` only when you are certain the target's
dependencies are already guaranteed.

## "Unmet Direct Dependencies"

The classic warning looks like this:

```
warning: (BR2_PACKAGE_A) selects BR2_PACKAGE_B which has unmet direct dependencies (BR2_PACKAGE_C)
```

Mechanism: `A` does `select B`, but `B` has `depends on C`, and `C` is not enabled. Because `select` skips the
dependency check, Kconfig turns `B` on anyway and warns that `B` is now enabled with a dependency unsatisfied. The build
often fails later in `B` with a missing header or library.

Two ways to fix it, both in the selecting package's `Config.in`:

- Guard the select so it only fires when the dependency holds: `select BR2_PACKAGE_B if BR2_PACKAGE_C`.
- Or mirror the dependency onto `A` so `A` itself cannot be enabled without `C`: add `depends on BR2_PACKAGE_C` to `A`.

Do NOT "fix" it by just enabling `C` blindly in the config — that hides the authoring bug and leaves the next user to
hit it.

## Recursive-Dependency Errors

A cycle of `select`/`depends on` produces a recursive-dependency error at configure time:

```
error: recursive dependency detected!
symbol BR2_PACKAGE_A depends on BR2_PACKAGE_B
symbol BR2_PACKAGE_B is selected by BR2_PACKAGE_A
```

Kconfig prints the exact chain — read it as a loop and cut one edge. The usual culprit is a `select` that closes the
ring; replacing that `select` with a `depends on`, or dropping the redundant back-reference, breaks it. You MUST resolve
the cycle in the `Config.in` graph; there is no config-file workaround.

## Symbol Renamed or Removed Across Releases

A `BR2_*` symbol that existed in an older Buildroot may have been renamed or dropped. Buildroot tracks retired symbols
in `Config.in.legacy`; a legacy option you still have set surfaces under a "Legacy config options" menu and points at
its replacement. Before recommending any symbol, confirm it exists in the target release (menuconfig `/` search, or grep
the tree). See the SKILL's *Version awareness* step.

## Evidence Commands

```bash
# Search + read a symbol's dependencies interactively
make menuconfig            # then press / and type the symbol

# Find the symbol definition and its depends/select in the tree
grep -rn "BR2_PACKAGE_FOO\b" package/ */Config.in

# Effective value of a symbol (wildcards allowed)
make -s printvars VARS=BR2_PACKAGE_FOO

# Is it actually set in the resolved config?
grep "BR2_PACKAGE_FOO" output/.config
```

## Worked Example: an invisible option and an unguarded select

Symptom: a package's option is nowhere in the menu, and after force-setting a related symbol the build warns about unmet
dependencies.

The option requires POSIX threads:

```kconfig
config BR2_PACKAGE_MYAPP
    bool "myapp"
    depends on BR2_TOOLCHAIN_HAS_THREADS
    select BR2_PACKAGE_MYLIB
```

- The prompt is hidden because the configured toolchain has threads disabled, so `depends on BR2_TOOLCHAIN_HAS_THREADS`
  is false. Enable a thread-capable toolchain (a `BR2_TOOLCHAIN_*` with thread support) and the option appears. It is a
  toolchain-feature gate, not a missing package.
- The `select BR2_PACKAGE_MYLIB` is unguarded. If `MYLIB` itself has `depends on BR2_PACKAGE_OPENSSL`, enabling `myapp`
  forces `MYLIB` on even without OpenSSL, yielding
  `... selects BR2_PACKAGE_MYLIB which has unmet direct dependencies (BR2_PACKAGE_OPENSSL)`. Fix in the `Config.in`:
  `select BR2_PACKAGE_MYLIB if BR2_PACKAGE_OPENSSL`, or add `depends on BR2_PACKAGE_OPENSSL` to `BR2_PACKAGE_MYAPP`.

Root cause, evidence, fix, validation — end with `make -s printvars VARS=BR2_PACKAGE_MYAPP` and a `menuconfig` `/`
search to confirm the prompt is visible and the warning is gone.
