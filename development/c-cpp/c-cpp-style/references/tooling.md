# Tooling for C and C++

Configuration and pitfalls for the formatters and linters that the `c-cpp-style` skill names. Each tool changes its
output between releases, so read "Version Pinning" before the first run in a tree.

## Contents

- clang-format
- astyle
- pre-commit
- clang-tidy
- cppcheck
- Version Pinning

## clang-format

Run clang-format only when the tree carries its own `.clang-format`. The tool searches the file's parent directories
for it. Without one, clang-format falls back to `--fallback-style`, which defaults to LLVM, so match the surrounding
code by hand instead.

### Changed Lines Only

Format the lines you changed, not whole files. `git clang-format` runs clang-format on the lines that differ from
`HEAD` and writes the result to the working tree or the index.

```sh
git clang-format            # lines that differ from HEAD
git clang-format HEAD~1     # also the last commit
git clang-format main       # the whole branch
git clang-format --diff     # print the diff; confirm the preview behaviour with git clang-format -h
```

Review the resulting diff before you stage it. `git clang-format` handles only files with its default extension list,
which covers `c`, `h`, `cc`, `cpp`, and `hpp`. Its git-config keys are `clangFormat.binary`, `clangFormat.commit`,
`clangFormat.extensions`, and `clangFormat.style`.

When a whole file must change, put the formatting in a separate commit that holds nothing else (U-Boot's coding
style document asks for this). Run `clang-format -i` only on a clean working directory, so the diff shows exactly what
the tool did. Fence a hand-aligned table with `// clang-format off` and `// clang-format on` in U-Boot. In kernel
sources avoid the fences, because other people run other clang-format versions.

### Kernel Style With Pure Tabs

Kernel style indents with tabs. `UseTab: Always` combined with `AlignAfterOpenBracket: Align` mixes tabs and spaces on
continuation lines, which fails `editorconfig-checker` under `indent_style = tab`. Set these options together:

```yaml
UseTab: Always
AlignAfterOpenBracket: DontAlign
AlignOperands: DontAlign
ContinuationIndentWidth: 8
BreakStringLiterals: false
```

An LLVM base sets `ContinuationIndentWidth` to 4, so without it a wrapped argument or a wrapped `if` condition gets one
tab plus four spaces. With it, clang-format 21 and 23 indent both with tabs only.

`BreakStringLiterals: false` keeps a user-visible message on one line, so `rg` finds it by its text.

A wrapped `if` condition then starts at the same indent as the body, so the two run together. Assign the call's
result to a variable before the `if` to keep the condition on one line:

```text
/* The continuation lines up with the body. */
if (parse_header(buf, len, &hdr) < 0 ||
    hdr.version != EXPECTED_VERSION) {

/* Stays on one line. */
ret = parse_header(buf, len, &hdr);
if (ret < 0) {
```

### Kernel and U-Boot Trees

Neither the kernel's own `.clang-format` nor astyle reproduces kernel style. Measured on a few already conforming
kernel files, both tools changed lines: the kernel's file changed 23 to 304, and astyle in Linux mode 20 to 202. The
kernel's documentation says its file only approximates the common style, and a subsystem may add its own
`.clang-format` in a subdirectory. Use `checkpatch.pl` as the gate in a kernel tree, and review every clang-format hunk.

U-Boot's `.clang-format` began as a copy of the kernel's and has diverged since, so never copy one tree's file into
the other. The kernel's header says "Intended for clang-format >= 11" and sets no upper version, so output can differ
between major releases (inference).

## astyle

astyle reads a project `.astylerc` only when asked: with `--project`, `--project=<name>`, or the environment variable
`ARTISTIC_STYLE_PROJECT_OPTIONS`. Otherwise a personal default applies, taken from `--options=<path>`, then
`ARTISTIC_STYLE_OPTIONS`, then `~/.astylerc`. A personal default can rewrite most of a file in another style.

Precedence, measured on astyle 3.6.20:

- Command-line options win over every file.
- The project file wins over the default file.
- `--options=none` disables the default file only. The project file stays ignored, and astyle uses its built-in
  four-space defaults.
- `--project=none` disables the project file.
- `ARTISTIC_STYLE_OPTIONS` naming a missing file stops astyle with "Cannot open default option file".

A repository that a personal default must not reformat needs both flags, `astyle --options=none --project`, or an
explicit `--options=<repo file>` (inference from the measurements). Put that invocation in the repository's recipe so
nobody retypes it.

Linux mode (`--style=linux --indent=force-tab=8`) falls short of kernel style in measured cases: it re-indents macro
bodies, it re-spaces casts so that `(long long)-tmp` becomes `(long long) - tmp`, it re-aligns wrapped arguments, and
it indented top-level declarations inside an `#if !CONFIG_IS_ENABLED(...)` block in a U-Boot file.

## pre-commit

The `pre-commit/mirrors-clang-format` hook formats JSON, JavaScript, protocol buffers, and more by default. Restrict it
to C and C++ with `types_or` when other formatters own the remaining files:

```yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-clang-format
    rev: v23.1.5
    hooks:
      - id: clang-format
        types_or: [c, c++]
```

The `check-metaschema` hook of `check-jsonschema` checks YAML and JSON files as schemas. `.clang-format` and
`.clang-tidy` are YAML but not schemas, so the hook fails on them. Exclude them from that hook:

```yaml
    hooks:
      - id: check-metaschema
        exclude: ^\.clang-(format|tidy)$
```

## clang-tidy

Enable check families by an explicit list, not `*`, because the set of checks changes every release. In C, many
`modernize-*` and `cppcoreguidelines-*` checks make no sense.

### Checks to Turn Off in C

Turn these off in `.clang-tidy`, with the reason beside each so a later reader can judge it:

```yaml
Checks: >-
  bugprone-*,cert-*,clang-analyzer-*,
  -bugprone-signed-bitwise,
  -hicpp-signed-bitwise,
  -cert-err33-c,
  -clang-analyzer-security.insecureAPI.DeprecatedOrUnsafeBufferHandling
# bugprone-signed-bitwise, named hicpp-signed-bitwise before clang-tidy 23: flags every uint8_t operand
#   through integer promotion. -Wconversion and -Wsign-conversion cover the real cases. Negate both names,
#   because bugprone-* enables the new one and an unknown name is ignored.
# cert-err33-c: flags every fprintf to stderr. Review still covers calls whose result matters.
# clang-analyzer-security.insecureAPI.DeprecatedOrUnsafeBufferHandling: asks for the Annex K *_s functions,
#   which glibc does not provide.
```

`_GNU_SOURCE` trips `bugprone-reserved-identifier`, `cert-dcl37-c`, and `cert-dcl51-cpp`. Set the `AllowedIdentifiers`
option of each of the three to list it, instead of removing the checks:

```yaml
CheckOptions:
  bugprone-reserved-identifier.AllowedIdentifiers: _GNU_SOURCE
  cert-dcl37-c.AllowedIdentifiers: _GNU_SOURCE
  cert-dcl51-cpp.AllowedIdentifiers: _GNU_SOURCE
```

Confirm an option key on the installed release with `clang-tidy --dump-config`.

### Checks That Found Real Defects

- `bugprone-suspicious-string-compare` flags `memcmp(...) != 0` used as a string compare.
- `bugprone-assignment-in-if-condition` flags an assignment inside an `if` condition. Some check lists give it
  another name; confirm the name with `clang-tidy --list-checks`.
- `bugprone-implicit-widening-of-multiplication-result` flags a multiplication done in `int` and then widened, which
  `(size_t)2 * N` avoids.
- The check list also names `bugprone-unsafe-functions`, `bugprone-signal-handler`, `bugprone-sizeof-expression`,
  `bugprone-not-null-terminated-result`, `bugprone-narrowing-conversions`, and `cert-err34-c` for unchecked
  string-to-number conversions.
- A negated check name that the installed release does not know is accepted silently, so confirm every name in
  `Checks` with `clang-tidy --list-checks`.
- `linuxkernel-must-check-errs` is the one kernel-specific check.

For the `clang-analyzer-*` checks, which clangd skips, read [clangd.md](clangd.md#clang-tidy-and-the-analyzer).

## cppcheck

cppcheck checks every `#ifdef` configuration at once. A host-test macro then produces false `unusedStructMember`
reports. Run one configuration per invocation with `-D` or `-U`:

```sh
cppcheck -DHOST_TEST=1 --project=compile_commands.json
cppcheck -UHOST_TEST src/
```

Suppress these two findings, and keep the reason where the suppression lives:

- `variableScope` conflicts with declarations at the top of a block, which kernel style requires. Pass
  `--suppress=variableScope` in the check script or task recipe, and write the reason in a comment beside it.
- `constParameter` flags the `argv` parameter of `main` as pointer to const, while `main` keeps its standard
  signature. Put `// cppcheck-suppress constParameter` on the line above, with a comment giving the reason.
  cppcheck reads inline suppressions only with `--inline-suppr`, so add that flag to the check script or task recipe.

A struct that mirrors a firmware or hardware layout has members that no code reads, such as reserved fields or end
tags. `unusedStructMember` is then correct but irrelevant in every configuration, so suppress it inline on the member,
with the reason.

Feed cppcheck the compilation database with `--project=compile_commands.json`, and pass `--platform` or a platform XML
that matches the target when char width or pointer size differs from the host. The project's `misra.py` addon checks
MISRA C:2012 and ships without the rule texts.

## Version Pinning

clang-format, clang-tidy, and cppcheck change their output between releases, so pin each tool in the tree and in CI.

- clang-format through pre-commit: set `rev` of `mirrors-clang-format` to a tag. The tag equals the clang-format
  version, so `rev: v23.1.5` is clang-format 23.1.5. The README leaves `rev` empty for you to fill.
- clang-format through `cpp-linter-hooks`: its `rev` pins the hook, not the tool. Pass `--version=<major.minor.patch>`,
  because without it two machines can install different versions.
- clang-tidy: run it through `uvx --from clang-tidy==<version> clang-tidy`, with the exact version from the tree's
  CI. The wheel ships `run-clang-tidy.py` and `clang-tidy-diff.py` beside the binary.
- cppcheck: install it from the distribution package or run a container whose tag fixes the version. The PyPI
  `cppcheck` package is a third-party wheel, not upstream's build.
