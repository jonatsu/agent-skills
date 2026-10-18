# Binary and Kernel Findings

Two checks that produce a great deal of output and, read naively, a great deal of noise. The skill in both
cases is knowing which red cells are findings and which are the intended state.

## `checksec` over a rootfs

```bash
checksec --dir=rootfs/usr/bin
checksec --file=rootfs/usr/bin/<binary>
checksec --format=json --file=rootfs/bin/busybox
```

**`checksec-native` does not build at `scarthgap`** without the one-line `.bbappend` in
`running-the-auditors.md`. Without it, run the target package inside a prod-test image, or run the
`checksec` shell script directly from its source checkout — it is a shell script, not a compiled tool.

### The JSON output, measured

At `checksec` 2.6.0, the version `meta-security` packages, `--format=json --file=` emits exactly ten keys:

```json
{ "/bin/bash": { "relro":"full","canary":"yes","nx":"yes","pie":"yes","rpath":"no","runpath":"no",
                 "symbols":"no","fortify_source":"yes","fortified":"13","fortify-able":"33" } }
```

Two traps:

- **The recipe pins a `SRCREV`, and these key names have changed upstream across versions.** Re-check when the
  pin moves.
- **`--format=json --fortify-file=` emits repeated `"function"` keys inside one object**, which is not valid
  JSON. `jq` accepts it and silently keeps only the last occurrence — 33 entries reduce to 1. **Parse the
  `--file` form.**

### Reading the result

Map each column back to what sets it, and compare against the exemptions before reporting:

| Column       | Set by                         | Expect                                                                                                                      |
| ------------ | ------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| RELRO        | `SECURITY_LDFLAGS`             | Full; **Partial** on `xserver-xorg` by design                                                                               |
| STACK CANARY | `SECURITY_STACK_PROTECTOR`     | Canary found; absent on the exempted recipes                                                                                |
| PIE          | `GCCPIE`/`SECURITY_PIE_CFLAGS` | PIE enabled; absent on powerpc                                                                                              |
| FORTIFY      | `lcl_maybe_fortify`            | "yes" when any `*_chk` symbol is imported; "no" also covers `-O0`, exempted recipes, and binaries with no fortifiable calls |

The `fortified` and `fortify-able` counts compare against the host's libc, not the target's. Read them as
approximate on a cross-built rootfs, and on a musl target treat them as meaningless.

A per-binary result that matches an exemption is the intended state, not a finding. OE-Core's
`security_flags.inc` at `scarthgap` exempts 13 recipes. Eleven show in `checksec`: `glibc`, `glibc-testsuite`,
`gcc-runtime`, `grub`, `grub-efi`, `valgrind`, and `sysklogd` lose most flags; `libgcc` on powerpc and `mkelfimage`
on x86 lose them on that architecture only; `ltp` loses the stack canary; `xserver-xorg` gets partial RELRO. `busybox`
and `gcc` lose only format-string warnings, which `checksec` cannot see, so a hardening gap in `busybox` is a
finding. Read the file at the image's release; the list changes between releases.

The useful finding is **a binary that is not exempted and not hardened** — usually the product's own
application, built by a recipe that dropped `LDFLAGS` or set its own `CFLAGS`.

Also worth knowing before reporting: if `security_flags.inc` was never required at all, *nothing* is hardened
and the correct finding is one line about the distro configuration, not a table of several hundred binaries.
Check `testdata.json` for the `SECURITY_*` variables before generating a per-binary report.

## Kernel configuration

The question is which hardening symbols survived into the shipped kernel, and the artefact is the `.config`:

```bash
# on target, if CONFIG_IKCONFIG_PROC=y — which is itself a small disclosure
zcat /proc/config.gz | grep -E 'FORTIFY_SOURCE|STACKPROTECTOR|RANDOMIZE_BASE|HARDENED_USERCOPY'

# host-side, from a deployed kernel image built with CONFIG_IKCONFIG=y (script from that kernel's source tree)
scripts/extract-ikconfig <deployed kernel image> | grep -E 'FORTIFY_SOURCE|STACKPROTECTOR|RANDOMIZE_BASE|HARDENED_USERCOPY'
```

`kernel-hardening-checker` (in `meta-oe`, 0.6.17.1 at `scarthgap`) compares a `.config` against a recommended
set and reports the gaps. **Its output has not been observed here**; treat the option names and report format
as needing confirmation at the packaged version.

Three cautions specific to reading its output:

- **It reports against upstream recommendations, not your threat model.** A "failed" line is a recommendation
  not followed, which may be a deliberate and correct choice for an embedded target — several of its checks
  cost real performance or break legitimate workloads.
- **Kernel version matters more than the tool version.** The authority for which symbols exist and what they do
  is the kernel's own `Documentation/security/self-protection.rst` **for that kernel version**, not the
  checker's list.
- **A `kernel_configcheck` pass is not this check.** Its default audit level filters to boot-affecting options
  and its findings are warnings unless `KMETA_AUDIT_WERROR` is set — see the yocto-security-hardening skill.

## Reporting either of these

Both produce output that looks like a report and is not one. Convert it:

- [ ] **State the tool, its version, and the artefact** — which image, which lane.
- [ ] **Subtract the intended state.** Exempted recipes, deliberate kernel choices, architecture limits.
- [ ] **Report the residue, with the recipe or config that owns each item.** A finding a reader cannot act on
  is a statistic.
- [ ] **Say what the check could not see.** Host-side `checksec` says nothing about what is running;
  `/proc/config.gz` says nothing about modules that were never loaded.
