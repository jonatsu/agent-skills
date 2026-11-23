# Refinements From Applying the Draft C Rules

Verified by the work session on GCC 15.2, clang-format 23.1.5 and clang-tidy 23.1.4 (ssciwr PyPI wheels), cppcheck
2.19.0 (Ubuntu 26.04 package). Generic; no project facts.

1. Set -std explicitly: GCC 15 defaults to gnu23 (`echo | gcc -dM -E - | grep __STDC_VERSION__` prints 202311L), so a
   "C17" rule without -std=gnu17 compiles as C23. Keep -std in the same shared flag variable as the warnings.
2. clang-format kernel style: UseTab: Always with AlignAfterOpenBracket: Align mixes tabs and spaces on continuation
   lines, failing editorconfig-checker with indent_style = tab. AlignAfterOpenBracket: DontAlign and AlignOperands:
   DontAlign give pure tabs. LLVM-based styles add 4 spaces to a wrapped if-condition; assign the call's result to a
   variable before the if. Set BreakStringLiterals: false so user-visible messages stay greppable.
3. pre-commit/mirrors-clang-format formats JSON, JavaScript, proto and more by default; restrict with
   types_or: [c, c++] when other formatters own those files.
4. clang-tidy bugprone-*, cert-*, clang-analyzer-\* on C: turn off, with a reason in the config,
   bugprone-signed-bitwise (every uint8_t operand via promotion; -Wconversion/-Wsign-conversion cover real cases),
   cert-err33-c (every fprintf to stderr), clang-analyzer-security.insecureAPI.DeprecatedOrUnsafeBufferHandling (Annex K
   \*\_s, absent in glibc). \_GNU_SOURCE trips bugprone-reserved-identifier, cert-dcl37-c, cert-dcl51-cpp: use
   AllowedIdentifiers. Useful finds: bugprone-suspicious-string-compare (`memcmp(...) != 0`),
   bugprone-assignment-in-if-condition, bugprone-implicit-widening-of-multiplication-result (`(size_t)2 * N`).
5. cppcheck checks all #ifdef configurations at once by default: a host-test macro then yields false unusedStructMember;
   run one configuration per invocation with -D/-U. Suppress variableScope (conflicts with top-of-block declarations,
   kernel style) with that reason. main's argv flagged constParameter needs an inline suppression. PyPI "cppcheck" is a
   third-party wheel (msclock), not upstream; prefer the distro package.
6. Sanitizer test runs: ASAN_OPTIONS=exitcode=99 and UBSAN_OPTIONS=halt_on_error=1:exitcode=98, else a sanitizer abort
   exits 1 like an expected refusal and a must-fail case passes on a memory bug.
7. Test-only compile-time macros replace inputs only (fixed keys, alternate /proc/device-tree root), never a check, so the
   host build runs the device build's checks.
8. An explicit cast that silences -Wconversion carries a comment naming the bound that keeps the value in range.
