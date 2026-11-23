# C and C++ Practice Sources

Read date for everything below: 2026-11-23. Pins are repository commits (short SHA with commit date), version strings
printed in the source, or the read date where the source carries none.

Conventions in this file:

- `[S]` marks what the source says. `[I]` marks my own inference. Unmarked text is a description of the source.
- "Read how" values: `original` (full text fetched with curl or `gh api` and read in the parts named),
  `fetch summary` (WebFetch model summary), `snippets` (search result snippets only), `measured` (I ran the tool).
- "Suits" values: LU = Linux userspace, ELU = embedded Linux userspace, BM = bare metal, firmware, bootloader,
  kernel-side code.

## Findings That Correct Earlier Assumptions

1. **astyle project files are not picked up automatically.** The astyle docs and my test (astyle 3.6.20) agree: a
   project `.astylerc` is used only with `--project`, `--project=<name>`, or the environment variable
   `ARTISTIC_STYLE_PROJECT_OPTIONS`. Without one of those, only the default file applies (`--options=`, then
   `ARTISTIC_STYLE_OPTIONS`, then `$HOME/.astylerc`). So a personal `~/.astylerc` with 1TBS and four spaces would
   silently reformat kernel or U-Boot code unless the command line says `--project` or `--options=none`. Details in the
   "Formatters" section.
2. **U-Boot's `.clang-format` is no longer a copy of the kernel's.** The U-Boot style document says it was "copied
   directly from the Linux kernel". At the pinned commits the two files differ in 62 diff lines, including a
   "U-Boot specific" block of `ForEachMacros`.
3. **The kernel's own `.clang-format` does not reproduce the kernel's own files.** On four kernel files it changed more
   lines than astyle did (measured, small sample). Neither tool is a drop-in checker for kernel style.
4. **KSPP wiki at kernsec.org has an expired TLS certificate.** I did not bypass it. The same content is at
   `kspp.github.io` (read) and the kernel tree ships `kernel/configs/hardening.config` (read).

---

## Topic 1. Coding standards and guidelines

### 1.1 SEI CERT C Coding Standard

- URL: <https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/> (the old wiki.sei.cmu.edu URL now
  redirects there). Source repo: <https://github.com/cmu-sei/secure-coding-standards>
- Pin: repo commit `73ee7a0dbe77` (2026-11-19). Targets C11 `[S]` (`front-matter/introduction/scope.md`: developed for
  C11, applicable to C99). The site itself calls the content "a work in progress".
- Licence: standards CC BY 4.0, code examples MIT (repo `LICENSE`).
- Read how: original (index, scope, rules vs recommendations, tool selection, the full rules index with 122 rule
  titles). I did not read individual rule bodies.
- Suits: LU, ELU, partly BM (the POSIX rules are LU/ELU only).
- Recommendations (rule titles are quoted from the rules index):
  1. INT30-C "Ensure that unsigned integer operations do not wrap", INT32-C (signed overflow), INT31-C (lossy
     conversions), INT33-C (divide by zero).
  2. ARR30-C and ARR38-C: do not form out-of-bounds pointers; guarantee that library functions do not form invalid
     pointers. STR31-C: guarantee storage for the string plus the null terminator.
  3. ERR33-C "Detect and handle standard library errors" and ERR34-C "Detect errors when converting a string to a
     number". POS54-C does the same for POSIX calls.
  4. ENV33-C "Do not call system()". POS34-C "Do not call putenv() with a pointer to an automatic variable".
  5. SIG30-C "Call only asynchronous-safe functions within signal handlers", SIG31-C, SIG34-C, SIG35-C.
  6. POS36-C and POS37-C: observe revocation order when dropping privileges, and check that the drop succeeded.
  7. FIO45-C "Avoid TOCTOU race conditions while accessing files", POS35-C (symlink races), POS38-C (fork and file
     descriptors).
  8. MEM30-C to MEM36-C (use after free, leaks, sizing, flexible array members), EXP33-C (uninitialised reads),
     EXP34-C (null dereference), MSC30-C (do not use `rand()`), MSC41-C (never hard code sensitive information).
- Where it says so: `rules/01.index.md` lists every ID and title. `rules-versus-recommendations.md`: a rule must be
  automatable and its violation likely to cause a defect; recommendations are weaker `[S]`.
- `[S]` The standard recommends static analysis and a TS 17961 conforming analyser, and says it cannot endorse a tool
  (`tool-selection-and-validation.md`).
- `[I]` Cite rule IDs in skills, because clang-tidy `cert-*`, Cppcheck and GCC `-fanalyzer` map to them.

### 1.2 SEI CERT C++ Coding Standard

- URL: <https://cmu-sei.github.io/secure-coding-standards/sei-cert-cpp-coding-standard/>
- Pin: same repo commit `73ee7a0dbe77`. Targets **C++14** `[S]` (`scope.md`). No recommendations are published
  (`1.index.md`: "does not currently expose any recommendations"). 169 files in its content tree.
- Licence: CC BY 4.0 and MIT, as above.
- Read how: original (index and scope only).
- Suits: LU, ELU. Little use for BM.
- Recommendations: I did not read individual rules. `[I]` The standard predates C++17, C++20 and C++23, so it
  cannot be the only C++ source. Use it for the resource, container-invalidation and concurrency rules, and use the
  C++ Core Guidelines for modern language use.

### 1.3 MISRA C and MISRA C++

- URLs: <https://misra.org.uk/product/misra-c2025/> and <https://misra.org.uk/product/misra-cpp2023/>
- Pin: MISRA C:2025 "updated in March 2025", supersedes 2023, 2019, 2012, 2004, 1998 `[S]`. MISRA C++:2023
  published October 2023, targets C++17, replaces MISRA C++:2008 and AUTOSAR C++14 (search snippets; the product
  page lists "TC1:2026").
- Licence: paid, single-user licence for a named person, "not printable", may not be shared or transferred `[S]`
  (product page via fetch summary).
- Read how: fetch summary of the C:2025 product page and the publications page; snippets for C++:2023 and the free
  documents. **I could not read the rule texts. They are not free.**
- What is free `[S, snippets only]`: the "MISRA C:2012 Permits" and "MISRA Compliance:2020" documents were announced
  as free downloads on the MISRA forum (thread dated 2021-03-01); the MISRA GitLab hosts a public "Example Suite"
  (<https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite>). The publications page (fetch summary) did not
  say which items are free.
- Free proxy that I did read: the **Zephyr coding guidelines** (section 1.9) list a 131 item MISRA C:2012 subset with
  paraphrased rule text, MISRA ID and CERT C cross reference, and the Cppcheck manual says `misra.py` "does not
  provide rule texts".
- Suits: BM and safety work. LU and ELU only when a customer demands it.
- Recommendations I can support from free text only:
  1. Rule 15.6 (braces on every `if`, loop body) is in Zephyr's subset and cross-referenced to CERT EXP19-C
     (`zephyr-cg.rst`, the rule 15.6 entry).
  2. Use deviation records, not silent suppression. Name MISRA Compliance:2020 as the process document `[S, snippet]`.
  3. `[I]` Pick a documented subset, as Zephyr does, rather than claiming full MISRA compliance.

### 1.4 C++ Core Guidelines

- URL: <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines> ; source
  <https://github.com/isocpp/CppCoreGuidelines>
- Pin: file header date "Jun 14, 2026", repo commit `5baf9fe252d0` (2026-11-02). The file says "release 0.8" if it were
  code.
- Licence: MIT-style grant "for your personal or internal business use only" plus a contributor licence (`LICENSE`).
  **This is narrower than a normal MIT licence.** Quote and link, do not copy rule text into a public skill.
- Read how: original (header, and these sections: F.15 to F.46, R.1 to R.22, ES.20 to ES.78, E.1 to E.31, CPL.1 to
  CPL.3, SL.con, SL.str, SL.C.1, NR.3).
- Suits: LU, ELU. BM only with a subset (see disagreements).
- Recommendations:
  1. R.1 manage resources with RAII; R.3 a raw pointer is non-owning; R.10 avoid `malloc` and `free`; R.11 avoid
     explicit `new` and `delete`.
  2. ES.20 always initialise an object; ES.22 do not declare a variable until you can initialise it; ES.25 use
     `const` or `constexpr`; ES.46 avoid narrowing conversions; ES.47 use `nullptr`; ES.48 to ES.50 avoid casts, use
     named casts, do not cast away `const`.
  3. ES.76 avoid `goto`; ES.78 do not rely on implicit fallthrough.
  4. F.20 prefer return values to output parameters; F.43 never return a pointer or reference to a local.
  5. E.25 "If you can't throw exceptions, simulate RAII" and its note that signalling errors "in a way that cannot be
     ignored requires exceptions". NR.3 says some hard real time systems cannot use exceptions `[S]`.
  6. CPL.2 "If you must use C, use the common subset of C and C++, and compile the C code as C++" `[S]`. This
     collides with kernel and systemd style (see disagreements).
  7. SL.C.1 do not use `setjmp` and `longjmp`.
- `[S]` The document admits its rules "have not been completely checked for completeness, consistency, or
  enforceability" (header "Problems").

### 1.5 Linux kernel coding style (and deprecated.rst)

- URLs: <https://docs.kernel.org/process/coding-style.html> and
  <https://docs.kernel.org/process/deprecated.html> ; source `Documentation/process/coding-style.rst`,
  `Documentation/process/deprecated.rst`, `Documentation/process/programming-language.rst`.
- Pin: `torvalds/linux` commit `b6a9fa34ce41` (2026-11-22).
- Licence: `deprecated.rst` carries `SPDX GPL-2.0`. `coding-style.rst` carries no SPDX tag; the tree is GPL-2.0
  (GitHub reports NOASSERTION for the repo).
- Read how: original. coding-style chapters 1, 2, 6, 7, 14, 15, 16, 17, 22 read in full; deprecated.rst sections
  strcpy, strncpy, strlcpy, VLAs, allocator arithmetic read.
- Suits: BM (kernel and U-Boot code). Not for userspace.
- Recommendations:
  1. Tabs are 8 characters; the limit is 80 columns; never break user visible strings (chapters 1 and 2).
  2. Single exit with `goto out_free_buffer:` style labels; "Avoid GW-BASIC names like err1 and err2" (chapter 7).
  3. Functions "do just one thing", under 5 to 10 local variables (chapter 6).
  4. Use `p = kmalloc_obj(*p, ...)` and `kmalloc_objs()` style allocators, never cast the return of an allocator
     (chapter 14; the `_obj` forms are new in this tree). `[S]` Both forms check for multiplication overflow.
  5. Naming of return values: an action name returns 0 or `-Exxx`; a predicate returns a boolean (chapter 16).
  6. Do not add `BUG()` or `BUG_ON()`; use `WARN_ON_ONCE()` with recovery; `BUILD_BUG_ON()` is encouraged
     (chapter 22).
  7. Do not use `inline` for functions over about three lines (chapter 15).
  8. `deprecated.rst`: replace `strcpy()`, `strncpy()` (removed from the kernel), `strlcpy()` with `strscpy()` and
     its variants; no VLAs; no open coded `count * size` in allocator arguments, use `kmalloc_array()`,
     `array_size()`, `struct_size()`, `check_mul_overflow()`; replace `simple_strtol()` with `kstrtol()`.
  9. `programming-language.rst`: the kernel builds with `-std=gnu11` and also supports Rust under `CONFIG_RUST`. It
     names no C++ `[S]`.

### 1.6 systemd coding style

- URL: <https://github.com/systemd/systemd/blob/main/docs/CODING_STYLE.md>
- Pin: `systemd/systemd` commit `e691c3d7c145` (2026-11-23). The build uses `c_std=gnu17` (`meson.build`).
- Licence: LGPL-2.1-or-later (SPDX tag in the file).
- Read how: original; Formatting, Memory Allocation, Error Handling, Types, File Descriptors, Functions to Avoid,
  Runtime Behaviour, Threading read.
- Suits: LU, ELU.
- Recommendations:
  1. 8 space indent, no tabs; about 109 columns; asymmetric braces; no braces around a single statement.
  2. Return negative `-Exxx` from every function that can fail for more than one reason; "Always check OOM".
  3. Every `open()`, `socket()`, `recvmsg()`, `fopen()` sets close on exec from the start (`O_CLOEXEC`,
     `SOCK_CLOEXEC`, `MSG_CMSG_CLOEXEC`, `F_DUPFD_CLOEXEC`, mode `e`).
  4. Never use `atoi()` or `strtol()` directly (checked wrappers instead); never `dup()`; never `exit()` in library
     style code; do not use `fgets()`, `basename()`, `dirname()`, `FILENAME_MAX`.
  5. Avoid fixed size string buffers (`char buf[256]` is "likely doing something wrong"); use `_cleanup_free_`
     scope based cleanup; no `alloca()` without the checked wrapper.
  6. Avoid threads; prefer worker processes; use `posix_spawn()` where `fork()` plus `exec` would do.
  7. Use `off_t` never; fixed width types; `unsigned` for values that cannot be negative.
- `[I]` systemd's wrappers (`safe_atoi`, `xopenat`) are project specific. A skill should state the underlying rule
  (use `strtol` with `endptr` and `errno` checks, always pass `O_CLOEXEC`) and not name the wrapper.

### 1.7 GNU Coding Standards

- URL: <https://www.gnu.org/prep/standards/standards.html>
- Pin: "last updated April 27, 2026" `[S]`.
- Licence: GNU Free Documentation License 1.3 or later, no invariant sections.
- Read how: original text; sections 3.4, 4.2, 5.1, 5.7 read.
- Suits: LU (GNU style packages).
- Recommendations:
  1. Lines of 79 characters or fewer; function open brace in column one (5.1).
  2. "Avoid arbitrary limits on the length or number of any data structure" (4.2).
  3. "Check every system call for an error return" and include `strerror` text in the message (4.2).
  4. "Check every call to malloc or realloc to see if it returned NULL" (4.2).
  5. Prefer `sigaction` over `signal` (4.2).
  6. ISO C99 is fine to use; never use trigraphs (3.4). GNU C supports almost all of C23 (5.7).
  7. Use `getopt_long`; use Gnulib for portability (4.2, 5.7).

### 1.8 Barr Group Embedded C Coding Standard (BARR-C:2018)

- URL: <https://barrgroup.com/embedded-c-coding-standard> (PDF <https://barrgroup.com/sites/default/files/barr_c_coding_standard_2018.pdf>)
- Pin: BARR-C:2018 (copyright 2018). Fixed edition.
- Licence: **"for your own internal use and for the use of your internal staff ... only."** Copyright Barr Group, no
  redistribution of the document or derived works. Do not copy its text into a public skill; cite and paraphrase
  the idea.
- Read how: original (PDF text; rules 1.1, 1.3, 1.7, 1.8, 5.2, 5.3, 5.6, 6.5, 8.5 read).
- Suits: BM and firmware. `[I]` Mostly irrelevant to kernel code.
- Recommendations:
  1. Comply with C99; restrict C++ compilers to the chosen C version (1.1).
  2. Braces always surround blocks, including single statements; left brace on its own line (1.3). **This conflicts
     with kernel and systemd style.**
  3. Do not use `auto` or `register`; avoid `goto` and `continue`, but "occasional use of goto to handle an
     exceptional circumstance is acceptable" (1.7).
  4. Use `static` for module-private items, `const` where appropriate, `volatile` for ISR shared data and
     memory-mapped registers (1.8).
  5. Use fixed width integers; do not use `short` and `long`; no bitwise operators on signed data; do not mix signed
     and unsigned in comparisons (5.2, 5.3).
  6. ISR rules: mark with the compiler's ISR keyword, name ending `_isr`, `static`, install a stub handler for every
     unhandled vector (6.5).
  7. Do not use `abort()`, `exit()`, `setjmp()`, `longjmp()` (8.5).

### 1.9 Zephyr coding guidelines (a free MISRA subset)

- URL: <https://docs.zephyrproject.org/latest/contribute/coding_guidelines/index.html>
- Pin: `zephyrproject-rtos/zephyr` commit `23b642c12704` (2026-11-23). Apache-2.0.
- Read how: original (`doc/contribute/coding_guidelines/index.rst`, preamble and table structure; rule 15.6 entry).
- Suits: BM, RTOS firmware.
- Recommendations: `[S]` "The coding guideline rules are based on MISRA-C 2012 and are a subset" and "all required
  for Zephyr and all new code should comply"; each row links MISRA rule, MISRA example file and CERT C cross
  reference. `[I]` This is the best free example of how to adopt a MISRA subset with CERT cross references.

### 1.10 The Power of Ten (Holzmann, NASA/JPL)

- URL: <https://spinroot.com/gerard/pdf/P10.pdf>
- Pin: the PDF carries no date. `[I]` From memory it is IEEE Computer, June 2006; verify before citing a date.
- Licence: no licence stated (author's PDF).
- Read how: original, rules 1 to 8 and the closing remarks.
- Suits: BM, safety critical firmware.
- Recommendations: 1. no `goto`, `setjmp`, `longjmp`, recursion. 2. every loop has a fixed upper bound. 3. no dynamic
  memory allocation after initialisation. 4. functions fit on one printed page. 5. assertion density of at least two
  per function, side effect free. 6. smallest possible scope for data. 7. check every non-void return value and every
  parameter (`(void)` cast marks a deliberate ignore). 8. limit the preprocessor to includes and simple macros.
- `[S]` The paper argues that guidelines need to be small enough to be checked by tools.

### 1.11 U-Boot coding style

Covered in "Per-codebase conventions".

---

## Topic 2. Compiler hardening and warnings

### 2.1 OpenSSF Compiler Options Hardening Guide for C and C++

- URL: <https://best.openssf.org/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.html> ; source
  <https://github.com/ossf/wg-best-practices-os-developers> (`docs/Compiler-Hardening-Guides/`)
- Pin: document dated 2026-08-20; repo commit `816cacb72970` (2026-11-21).
- Licence: CC BY 4.0 (document footer). Repo code Apache-2.0.
- Read how: original, nearly all of the TL;DR, tables 1 to 4, the `_FORTIFY_SOURCE`, stack protector and sanitizer
  sections.
- Suits: LU and ELU primarily. `[S]` The tables say they are "primarily applicable to compiling user space code in
  GNU/Linux". For embedded the guide only notes size costs (for example `-ftrivial-auto-var-init`). Kernel and
  firmware have their own flag sets.
- Recommendations (TL;DR block, exact):
  1. `-O2 -Wall -Wformat -Wformat=2 -Wconversion -Wimplicit-fallthrough -Werror=format-security`.
  2. `-U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=3 -D_GLIBCXX_ASSERTIONS -D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_FAST -fstrict-flex-arrays=3`.
  3. `-fstack-clash-protection -fstack-protector-strong`, linker
     `-Wl,-z,nodlopen -Wl,-z,noexecstack -Wl,-z,relro -Wl,-z,now -Wl,--as-needed -Wl,--no-copy-dt-needed-entries`.
  4. Add `-fPIE -pie` for executables, `-fPIC -shared` for libraries, `-fcf-protection=full` on x86_64,
     `-mbranch-protection=standard` on aarch64, `-fzero-call-used-regs=used-gpr`.
  5. For production code add `-fno-delete-null-pointer-checks -fno-strict-overflow -fno-strict-aliasing -ftrivial-auto-var-init=zero`.
  6. Promote obsolete C constructs to errors: `-Werror=implicit -Werror=incompatible-pointer-types -Werror=int-conversion`.
  7. Blanket `-Werror` only during development, never in distributed source, because it ties the build to compiler
     versions; use selective `-Werror=<flag>` instead.
  8. Sanitizers: not for production, and never on set-user-ID binaries; exception is UBSan with
     `-fsanitize-minimal-runtime` (Clang) or `-fsanitize-trap=undefined` (GCC). `_FORTIFY_SOURCE` is incompatible with
     ASan, so disable it in sanitizer builds.
  9. Avoid hard coded `-Wl,-rpath` (the only "discouraged" option).
- `[S]` "We recommend explicitly enabling desired compiler flags in your build scripts ... rather than relying on the
  toolchain defaults." Defaults vary by distribution.

### 2.2 GCC manual: warning options, `-fanalyzer`, instrumentation options

- URLs: <https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html> ,
  <https://gcc.gnu.org/onlinedocs/gcc/Static-Analyzer-Options.html> ,
  <https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html>
- Pin: the "current" manual. The GCC front page lists releases 16.2, 16.1, 15.3, 14.4, 13.5. Copyright 1988 to 2026
  FSF. `[I]` The page text does not print the exact release, so I cannot say 16.2 with certainty.
- Licence: GFDL (FSF copyright notice on the page; I did not read the licence text).
- Read how: original (HTML converted to text); searched for specific options.
- Suits: LU, ELU, BM (GCC based toolchains).
- Recommendations:
  1. `-fanalyzer` "is neither sound nor complete ... a bug-finding tool" and "is only suitable for use on C code in
     this release" `[S]`; much more expensive than other warnings. It models `malloc`/`free`, file descriptors,
     tainted input (`-Wanalyzer-tainted-*`) and `mktemp` misuse `[S]`.
  2. `-fhardened` turns on `-D_FORTIFY_SOURCE=3`, `-D_GLIBCXX_ASSERTIONS`, `-ftrivial-auto-var-init=zero`, PIE with
     `-z relro -z now`, `-fstack-protector-strong`, `-fstack-clash-protection`, and `-fcf-protection=full` on x86 GNU
     Linux. It only sets an option you did not already set `[S]`. The flag list may change between major releases.
  3. Warnings that are not in `-Wall`: `-Wshadow`, `-Wconversion`, `-Wvla`, `-Wnull-dereference`, `-Wcast-align`,
     `-Wdouble-promotion`, `-Wmissing-prototypes`, `-Wstrict-prototypes`, `-Walloca`, `-Wstack-usage=`,
     `-Wundef`, `-Wlogical-op`, `-Wduplicated-cond`. All appear in the manual; I did not verify per option which
     group enables it.
  4. `-fstack-protector` guards functions with `alloca` or buffers of 8 bytes or more `[S]`.
  5. GCC 15 defaults to C23 (`gnu23`) `[S]` (C status page); older code that uses `bool`, `nullptr`, `true` or `()`
     as an identifier or old style declarations can break.

### 2.3 Clang user manual (diagnostics) and thread safety analysis

- URLs: <https://clang.llvm.org/docs/UsersManual.html> , <https://clang.llvm.org/docs/ThreadSafetyAnalysis.html>
- Pin: tip of tree docs, read 2026-11-23. PyPI `clang-format` wheel is 23.1.5 and `clang-tidy` 23.1.4 that day.
- Licence: no licence stated on the pages (LLVM project is Apache-2.0 with LLVM exceptions per its repo; not re-read).
- Read how: original, "Enabling All Diagnostics" and the Thread Safety section.
- Suits: LU, ELU, BM.
- Recommendations:
  1. `-Weverything` "we generally don't recommend using it. `-Wall -Wextra` are a better choice for most projects"
     `[S]`.
  2. `-Wthread-safety` with `GUARDED_BY`, `REQUIRES` annotations checks lock discipline at compile time `[S]`
     (`[I]` works for C with the attribute macros, including pthread mutexes).
  3. The docs list a `-fbounds-safety` extension for C. `[I]` Not portable to GCC, so not a baseline.

### 2.4 glibc manual: Source Fortification, and Red Hat `_FORTIFY_SOURCE=3` article

- URLs: <https://www.gnu.org/software/libc/manual/html_node/Source-Fortification.html> and
  <https://developers.redhat.com/articles/2023/02/06/how-improve-application-security-using-fortifysource3>
- Pin: glibc manual page, read date. Red Hat article dated 2023-02-06 (date taken from the OpenSSF guide's citation).
- Licence: glibc manual GFDL (not re-read); Red Hat article terms not read.
- Read how: glibc page fetched and read (short); Red Hat article NOT fetched. `[S]` per OpenSSF, which cites it.
- Suits: LU, ELU on glibc. `[I]` Not for musl or newlib: check libc support before adding the macro.
- Recommendations: the glibc page lists the fortified functions (memcpy, strcpy, sprintf, snprintf, gets and so
  on). OpenSSF says level 3 needs `-O1` or higher and a compiler that can derive the destination size.

### 2.5 Yocto and Buildroot hardening defaults (embedded Linux evidence)

- URLs: Yocto `meta/conf/distro/include/security_flags.inc` in openembedded-core; Buildroot `Config.in`
  ("Security Hardening Options").
- Pins: openembedded-core `40bb14c83632` (2026-11-19); buildroot `cd21c00a15fa` (2026-11-23).
- Licence: openembedded-core file carries no SPDX in the part read; Buildroot repo reports NOASSERTION (GPL-2.0 or
  later in practice; not verified).
- Read how: original files (Debian and Fedora pages not read; they are cited by OpenSSF only).
- Suits: ELU.
- Recommendations `[S]`:
  1. Poky default flags: `-fstack-protector-strong`, PIE (`--enable-default-pie`), `-D_FORTIFY_SOURCE=2` (not at
     `-O0`), `-Wformat -Wformat-security -Werror=format-security`, linker `-Wl,-z,relro,-z,now`.
  2. Poky keeps a per recipe override list and says the "idea would be over time to reduce this list to nothing".
  3. Buildroot offers `BR2_PIC_PIE`, `BR2_SSP_{REGULAR,STRONG,ALL}`, `BR2_RELRO_*`, `BR2_FORTIFY_SOURCE_{1,2,3}` as
     options; the `_2` help text warns "some conforming programs might fail".
  4. `[I]` Embedded Linux projects already inherit hardening from the build system; a skill for application code
     should not hard code these flags in the application Makefile if the BSP injects them.

### 2.6 Linux kernel build flags and hardening (Kconfig, KSPP)

See "Per-codebase conventions: kernel" for `W=1`, `CONFIG_WERROR`, `hardening.config` and KSPP.

---

## Topic 3. Static analysis, sanitizers, fuzzing

### 3.1 clang-tidy checks

- URL: <https://clang.llvm.org/extra/clang-tidy/checks/list.html>
- Pin: tip of tree docs read 2026-11-23; wheels `clang-tidy` 23.1.4 on PyPI the same day.
- Licence: no licence stated on page.
- Read how: original (full list). Family counts from the list: bugprone 249, clang-analyzer 225, readability 134,
  modernize 110, cppcoreguidelines 86, cert 84, misc 73, performance 52, google 40, concurrency 5, linuxkernel 2.
- Suits: LU and ELU (C and C++). BM when a compile database exists. `[I]` Many `modernize-*` and
  `cppcoreguidelines-*` checks make no sense for C.
- Recommendations:
  1. `bugprone-*` is the main bug family; examples: `bugprone-unsafe-functions`, `bugprone-signal-handler`,
     `bugprone-sizeof-expression`, `bugprone-not-null-terminated-result`, `bugprone-narrowing-conversions`,
     `bugprone-implicit-widening-of-multiplication-result`, `bugprone-unchecked-string-to-number-conversion`,
     `bugprone-assignment-in-selection-statement`.
  2. `cert-*` maps to CERT rules (for example `cert-err33-c`).
  3. `clang-analyzer-*` includes `clang-analyzer-security.insecureAPI.*` and
     `clang-analyzer-security.insecureAPI.DeprecatedOrUnsafeBufferHandling`.
  4. `linuxkernel-must-check-errs` is the one kernel specific check.
  5. `[I]` Enable families by explicit allow list, not `*`, and pin the clang-tidy major version, because the set
     changes every release.

### 3.2 Cppcheck

- URL: <https://cppcheck.sourceforge.io/manual.html> ; source manual `man/manual.md` in the cppcheck repo.
- Pin: repo commit `21459e9c4fb9` (2026-11-22); latest release 2.22.0. GPL-3.0.
- Licence: GPL-3.0 (repo). The manual file carries no separate licence.
- Read how: original manual (introduction, severities, project import, platform, suppressions, baseline).
- Suits: LU, ELU, BM.
- Recommendations:
  1. Feed it `compile_commands.json` (`--project=compile_commands.json`); `bear` can generate it from a Makefile.
  2. Use `--platform` or a custom platform XML that matches the target (char bits, pointer size) `[S]`.
  3. Suppress with an id and a file, an inline `// cppcheck-suppress`, or a hash based XML suppression that survives
     line moves `[S]`. A baseline workflow records existing findings so only new ones fail `[S]`.
  4. `[S]` "Static analysis should be used as a complement ... does not replace careful design, testing, dynamic
     analysis, fuzzing."
  5. `[S]` `misra.py` addon checks MISRA C:2012 but ships without rule texts.
  6. The open source edition lacks the Premium checkers; the Premium manual exists. I did not read it.

### 3.3 Coverity Scan

- URL: <https://scan.coverity.com/faq>
- Pin: read 2026-11-23; no version.
- Terms: free only for registered open source projects that meet an OSI style definition `[S]`; the project must accept
  the Scan User Agreement.
- Read how: original FAQ text.
- Suits: LU, ELU, BM (any C or C++ project that builds on Linux).
- Recommendations: `[S]` build submission caps per week by size: up to 28 builds per week and 4 per day under 100K
  lines; 21 and 3 for 100K to 500K; 14 and 2 for 500K to 1M; 7 and 1 above 1M. `[I]` Run it on a schedule (weekly or
  nightly), not per commit.

### 3.4 Sanitizers (ASan, UBSan, TSan, MSan, KASAN)

- URLs: <https://clang.llvm.org/docs/AddressSanitizer.html> , `UndefinedBehaviorSanitizer.html`,
  `ThreadSanitizer.html`, `MemorySanitizer.html`; kernel `Documentation/dev-tools/kasan.rst`, `ubsan.rst`.
- Pin: tip of tree Clang docs read 2026-11-23; kernel commit `b6a9fa34ce41`.
- Licence: Clang pages no licence stated; kernel docs GPL-2.0.
- Read how: original.
- Suits: LU and ELU for the Clang ones. KASAN is kernel only. U-Boot sandbox supports ASan (see U-Boot section).
- Recommendations `[S]`:
  1. ASan: build with `-O1 -g -fsanitize=address -fno-omit-frame-pointer`; typical slowdown 2x.
  2. TSan: typical slowdown 5x to 15x, Linux x86_64 and aarch64 among others; forces PIE behaviour.
  3. MSan: typical slowdown 3x; requires that all code, including libraries, is instrumented.
  4. UBSan: `-fsanitize=undefined`; select checks with `-fsanitize=` names (`bounds`, `signed-integer-overflow`);
     `-fsanitize-trap=` and `-fno-sanitize-recover=` change what a failure does. `unsigned-integer-overflow` and
     `implicit-conversion` are separate opt in checks, not part of `undefined`.
  5. Kernel KASAN has three modes: Generic (debugging, like ASan), SW_TAGS (debug and dogfood), HW_TAGS (cheap
     enough for production, needs hardware tagging).
  6. Run the test suite under ASan plus UBSan in CI; add TSan as a separate job (ASan and TSan cannot combine `[S]`
     OpenSSF).

### 3.5 libFuzzer, AFL++, OSS-Fuzz, syzkaller

- URLs: <https://llvm.org/docs/LibFuzzer.html> ; <https://github.com/AFLplusplus/AFLplusplus>
  (`docs/fuzzing_in_depth.md`); <https://google.github.io/oss-fuzz/> ; <https://github.com/google/syzkaller>
- Pins: libFuzzer page "Last updated on 2026-11-23". AFL++ branch `stable` commit `d798677805de` (2026-11-15), latest
  release v5.03c. OSS-Fuzz commit `e8139aeb3f12` (2026-11-23), Apache-2.0. syzkaller commit `e9bfbe3ad949`
  (2026-11-23), Apache-2.0.
- Licences: libFuzzer docs no licence stated (LLVM). **AFL++ is AGPL-3.0-or-later for `afl-fuzz`, with parts under
  Apache-2.0** (its README). Instrumentation runtimes linked into the target are Apache-2.0 `[S]`; re-check before
  shipping instrumented binaries.
- Read how: original (libFuzzer and AFL++ parts; OSS-Fuzz new project guide and "ideal integration" page;
  syzkaller `docs/linux/kernel_configs.md`).
- Suits: LU, ELU (libFuzzer, AFL++, OSS-Fuzz). BM via host builds only. U-Boot sandbox for U-Boot. syzkaller for the
  kernel.
- Recommendations `[S]`:
  1. libFuzzer target: `int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size)`; "must not exit()", should be
     deterministic and "ideally ... not modify any global state".
  2. Build with `-fsanitize=fuzzer,address` (or `fuzzer,signed-integer-overflow`, `fuzzer,memory`); use
     `-fsanitize=fuzzer-no-link` for the library objects.
  3. Seed the corpus with varied small valid inputs; shrink with `-merge=1`; keep a dictionary for token formats.
  4. AFL++: use `afl-clang-lto` when Clang 11 or later exists, else `afl-clang-fast`; persistent mode and CMPLOG
     (`AFL_LLVM_CMPLOG=1`) improve speed and depth; run on tmpfs when possible.
  5. OSS-Fuzz needs `project.yaml`, `Dockerfile`, `build.sh`; default sanitizers are address and undefined; MSan is
     "supported and recommended" but off by default because of uninstrumented dependencies.
  6. An ideal fuzz target "is fast and has no OOMs", has a seed corpus and dictionary, and runs on the seed corpus
     in CI.
  7. syzkaller needs `CONFIG_KCOV=y`, `CONFIG_KCOV_INSTRUMENT_ALL=y`, `CONFIG_KCOV_ENABLE_COMPARISONS=y`,
     `CONFIG_DEBUG_FS=y`; kmemleak optional.
- `[I]` For a skill: write a fuzz harness for every parser that touches untrusted bytes and keep it in the repo; run
  the corpus as a regression test in CI.

### 3.6 Formatters and pinning (clang-format, astyle) and how projects pin tool versions

- URLs: <https://clang.llvm.org/docs/ClangFormat.html> ; <https://astyle.sourceforge.net/astyle.html> ;
  <https://pypi.org/project/clang-format/> ; <https://pypi.org/project/clang-tidy/> ;
  <https://github.com/pre-commit/mirrors-clang-format> ; <https://github.com/cpp-linter/cpp-linter-hooks>
- Pins:
  - `clang-format` PyPI 23.1.5 and `clang-tidy` PyPI 23.1.4 (Apache-2.0), wheels from
    `ssciwr/clang-format-wheel` and `ssciwr/clang-tidy-wheel`.
  - `pre-commit/mirrors-clang-format` commit `ce4bd7270237`, latest tag `v23.1.5`, MIT, "mirror of
    ssciwr/clang-format-wheel".
  - `cpp-linter/cpp-linter-hooks` commit `5812ce5fdcbf`, release 1.9.0, MIT.
  - astyle docs page (read 2026-11-23, no version printed); local binary Artistic Style 3.6.20; PyPI `astyle` wheel
    3.6.18 by a third party (`Freed-Wu/astyle-wheel`, licence field GPL-3.0-or-later). The astyle docs page states
    no licence.
- Read how: original (astyle page in full for option files and the styles; READMEs of the hooks), measured
  (astyle runs and clang-format runs).
- Suits: all.
- How projects pin `[S]`:
  1. `mirrors-clang-format`: set `rev:` to a tag; the tag equals the clang-format version, so the pin is exact
     (`rev: v23.1.5` is clang-format 23.1.5). The README leaves `rev: ''` for you to fill.
  2. `cpp-linter-hooks`: the `rev` is the version of the hooks, not of the tool. Without `--version` the hook installs
     the newest wheel, "so two machines can end up with different versions", and the README says teams and CI
     "should set `--version`". `--version=21` takes the newest 21.x; `--version=21.1.8` pins exactly. clang-format
     wheels cover LLVM 6 to 23, clang-tidy wheels 13 to 23. For offline use, pin through pre-commit's
     `additional_dependencies`.
  3. `clang-tidy-wheel` publishes one package per major and minor release and ships `run-clang-tidy.py` and
     `clang-tidy-diff.py`.
  4. The kernel's `.clang-format` says "Intended for clang-format >= 11" and gives no upper pin. `[I]` So formatting
     output can drift between clang-format majors.
- Astyle option file lookup `[S]` (astyle docs "Option Files"; confirmed by my test):
  1. Command line options always win.
  2. The **project file** is used only when asked: `--project` (looks for `.astylerc` or `_astylerc` in the source
     path and its parents), `--project=<name>`, or `ARTISTIC_STYLE_PROJECT_OPTIONS=<name>`. `--project=none` disables
     it. The project file beats the default file.
  3. The **default file**: `--options=<path>`, else `ARTISTIC_STYLE_OPTIONS`, else `$HOME/.astylerc`, else
     `%APPDATA%\astylerc`. `--options=none` disables it.
  4. Measured with astyle 3.6.20 (`HOME` set to a directory holding a 1TBS, four space `.astylerc`, and a project
     directory holding a `style=linux, force-tab=8` `.astylerc`):
     - no flag: the HOME file applied (four spaces). The project file was ignored.
     - `--options=none` only: four spaces came out. The project file was still ignored, and astyle fell back to its
       built in defaults (four space indent, no brace rewriting).
     - `--project`: tabs and Linux braces (project file applied and it overrode HOME).
     - `--options=none --project`: tabs (project file only).
     - `ARTISTIC_STYLE_PROJECT_OPTIONS=.astylerc`: tabs.
     - `ARTISTIC_STYLE_OPTIONS=/nonexistent`: astyle stops with "Cannot open default option file".
  5. `[I]` For a repository that must not be reformatted by a user's personal defaults, the safe invocation is
     `astyle --options=none --project ...` (or an explicit `--options=<repo file>`), plus a wrapper script or just
     recipe that always passes it.

Findings about astyle versus clang-format are in "Per-codebase conventions".

---

## Topic 4. Secure and robust Linux userspace patterns

All man pages below are from the installed Linux man-pages 6.17 (page footer date 2026-02-08), read with `man`. The
canonical copies are at <https://man7.org/linux/man-pages/> . Licence: the man-pages project ships each page under
its own licence, stated in the page's COLOPHON or header; I did not read those. Treat as "licence stated per page,
not checked".

### 4.1 Atomic file replacement with durability: rename(2), fsync(2), open(2) `O_TMPFILE`; LWN

- URLs: man7 `rename.2`, `fsync.2`, `open.2`; <https://lwn.net/Articles/322823/> (Corbet, "ext4 and data loss", 2009-03-11);
  <https://lwn.net/Articles/457667/> (Moyer, "Ensuring data reaches disk", 2011-09-07).
- Licence: LWN articles are copyright Eklektix, Inc. (article footer); no reuse licence stated, link do not copy.
- Read how: original (man pages: the relevant paragraphs; LWN: fetched and read the key passages).
- Suits: LU, ELU.
- Recommendations:
  1. `[S]` `rename()` atomically replaces the target: "there is no point at which another process attempting to access
     newpath will find it missing", and if the call fails the old target stays (rename(2)).
  2. `[S]` `fsync()` flushes file data and metadata, but "does not necessarily ensure that the entry in the directory
     containing the file has also reached disk. For that an explicit fsync() on a file descriptor for the directory is
     also needed" (fsync(2)).
  3. `[S]` POSIX never promised data survival without `fsync`; ext3 ordering was "almost an accident", and ext4 delayed
     allocation exposed it (LWN 2009: "The real solution ... is to fix the applications").
  4. `[S]` A newly created file may need `fsync` of both the file and its directory (LWN 2011, "When Should You
     Fsync?").
  5. `[I]` Pattern: create the temp file in the same directory (same filesystem), write, check every write error,
     `fsync(fd)`, `close`, `rename`, then `fsync` the directory. `[I]` Add `fchmod` or create with the final mode
     first. Check the return value of `close()` too.
  6. `[S]` open(2) also has `O_TMPFILE`; `renameat2(RENAME_NOREPLACE)` avoids overwriting (renameat2(2); I read only
     the headline description).

### 4.2 Close on exec, descriptor hygiene: open(2), close_range(2), systemd style

- URLs: man7 `open.2`, `close_range.2`; systemd CODING_STYLE (File Descriptors); CERT POS38-C.
- Pin: man-pages 6.17; systemd `e691c3d7c145`.
- Read how: original.
- Suits: LU, ELU.
- Recommendations:
  1. `[S]` "The use of this flag [O_CLOEXEC] is essential in some multithreaded programs, because using a separate
     fcntl(2) F_SETFD operation ... does not suffice to avoid race conditions" (open(2)).
  2. `[S]` Use `SOCK_CLOEXEC`, `F_DUPFD_CLOEXEC`, `SFD_CLOEXEC` and the fopen `e` mode (systemd style; signalfd(2) names
     `SFD_CLOEXEC`).
  3. `[S]` `close_range(first, last, CLOSE_RANGE_CLOEXEC)` sets close on exec on a range, and `CLOSE_RANGE_UNSHARE`
     avoids races with other threads sharing the table (close_range(2), since Linux 5.11).
  4. `[S]` Open untrusted paths with `O_NONBLOCK` (systemd) so a FIFO or device cannot hang the open. `[I]` Combine
     with `fstat` after open, not `stat` before.

### 4.3 Spawning processes: posix_spawn(3), system(3), fork(2)

- URLs: man7 `posix_spawn.3`, `system.3`, `fork.2`; Baumann, Appavoo, Krieger, "A fork() in the road", HotOS 2019
  (<https://www.microsoft.com/en-us/research/uploads/prod/2019/04/fork-hotos19.pdf>).
- Licence: man pages per page; paper copyright of the authors/ACM, no reuse licence stated in the text I read.
- Read how: original.
- Suits: LU, ELU (also MMU-less ELU: `[S]` posix_spawn(3) says these functions were specified "for machines that lack
  ... fork(2)", "generally small, embedded systems lacking MMU support").
- Recommendations:
  1. `[S]` system(3): "Do not use system() from a privileged program (set-user-ID, set-group-ID, or with
     capabilities) because strange values for some environment variables might be used to subvert system integrity";
     use `exec` family but not `execlp` or `execvp`.
  2. `[S]` system(3): any user input that reaches the command "should be carefully sanitized".
  3. `[S]` `posix_spawn` supports `POSIX_SPAWN_SETSIGMASK`, `POSIX_SPAWN_SETSIGDEF` and file actions in the child
     before `exec`; descriptors with `FD_CLOEXEC` are closed (posix_spawn(3)).
  4. `[S]` After `fork()` in a multithreaded program the child "can safely call only async-signal-safe" functions
     (fork(2)).
  5. `[S]` The paper recommends `posix_spawn`-like APIs and argues fork "should be removed as a first-class
     primitive" for new designs; `[I]` treat as opinion, not Linux policy.
  6. `[S]` systemd: threads plus `clone` or `fork` can deadlock on the malloc lock; prefer worker processes with
     `execve`; `posix_spawn` avoids the copy on write trap.

### 4.4 Signals: signal-safety(7), sigaction(2), signalfd(2), signal(7)

- URLs: man7 `signal-safety.7`, `sigaction.2`, `signalfd.2`, `signal.7`; CERT SIG30-C.
- Read how: original.
- Suits: LU, ELU.
- Recommendations:
  1. `[S]` Handler options are (a) call only async-signal-safe functions and keep the handler reentrant, or (b) block
     signals around unsafe calls; "Generally, the second choice is difficult in programs of any complexity, so the
     first choice is taken" (signal-safety(7)).
  2. `[S]` The set of async-signal-safe functions is a fixed table (signal-safety(7)); `printf`, `malloc` are not in it.
  3. `[S]` `signalfd()` turns signals into a descriptor you `read`; the signals "should be blocked using
     sigprocmask(2)" first; `SIGKILL` and `SIGSTOP` cannot be received this way (signalfd(2)).
  4. `[S]` Use `sigaction`, not `signal` (GNU Coding Standards 4.2; sigaction(2) says `signal()` is less portable
     for establishing handlers); set `SA_RESTART` (systemd).
  5. `[I]` Recommended order: signalfd or `sigwaitinfo` in an event loop, else self pipe, else a handler that only sets
     a `volatile sig_atomic_t` flag.

### 4.5 Safe parsing of untrusted input

- URLs: CERT C rules (INT30-C, INT31-C, ARR38-C, STR31-C, ERR34-C, FIO47-C); man7 `strtol.3`; kernel `deprecated.rst`;
  Sassaman, Patterson, Bratus, Shubina, "The Halting Problems of Network Stack Insecurity",
  ;login: December 2011 (<https://www.usenix.org/system/files/login/articles/105516-Sassaman.pdf>); Wheeler,
  "Secure Programming HOWTO" v3.72, 2015-09-19 (<https://dwheeler.com/secure-programs/>).
- Licence: CERT as above. Kernel GPL-2.0. LangSec paper copyright of USENIX/authors, no reuse licence read. Wheeler's
  book offers the GNU FDL (its table of contents lists "The GNU Free Documentation License" as appendix D).
- Read how: CERT titles original; strtol(3) original; LangSec paper original (two column text, read in part); Wheeler
  only the table of contents page (about 22 KB), **not the chapters**. `langsec.org` itself failed the TLS
  certificate check, so I did not read the site.
- Suits: LU, ELU, BM parsers.
- Recommendations:
  1. `[S]` strtol(3): set `errno = 0` first, check `ERANGE`, and compare `endptr` to detect "no digits"; the function
     "does not modify errno on success".
  2. `[S]` Kernel: replace `simple_strtol()` family with `kstrtol()` family (deprecated.rst).
  3. `[S]` Kernel: never compute `count * size` in an allocator argument; use `kmalloc_array`, `array_size`,
     `struct_size`, `check_mul_overflow()` and friends.
  4. `[S]` LangSec: treat the input as a language; the input handling code is a recogniser; avoid input languages
     whose parser equivalence is undecidable; prefer parsers generated from a grammar and keep the accepted language
     small (paper, "Principle 1 and 2" passages; two column layout, so I paraphrase).
  5. `[I]` Parse into a validated typed structure once, at the boundary; carry lengths with pointers; reject, do
     not repair.

### 4.6 Integer overflow checks

- URLs: <https://gcc.gnu.org/onlinedocs/gcc/Integer-Overflow-Builtins.html> ; C23 `<stdckdint.h>`; CERT INT30-C and
  INT32-C; kernel `include/linux/overflow.h` behaviour via `deprecated.rst`.
- Read how: original (GCC page and the CERT and kernel texts above). I did not read the C23 clause text for
  `ckd_add`; the local man page for `ckd_add(3)` is empty.
- Recommendations:
  1. `[S]` `__builtin_add_overflow(a, b, &res)` and the `sub` and `mul` forms compute in "infinite precision", return
     true when the stored result differs, and "have fully defined behavior for all argument values" (GCC manual).
  2. `[S]` GCC C status: `<stdckdint.h>` is supported since GCC 14 (C23's `ckd_add`, `ckd_sub`, `ckd_mul`).
  3. `[S]` Compile with `-fno-strict-overflow` for production (OpenSSF) so signed overflow is not optimised away;
     this does not replace explicit checks.
  4. `[I]` Use the checked builtins before every size computation that feeds `malloc`, `memcpy` or an array index.

### 4.7 Zeroing secrets: explicit_bzero(3), `memset_explicit`

- URLs: man7 `explicit_bzero.3`; glibc 2.43 announcement
  <https://sourceware.org/pipermail/libc-announce/2026/000052.html>
- Read how: man page original; glibc 2.43: search snippets from two sources (the announcement list and a news site)
  quoting the NEWS line, plus a fetch of the announcement that did not show the NEWS text. Treat the C23 claim as
  `[S, snippets]`.
- Recommendations:
  1. `[S]` `explicit_bzero()` "guarantees that compiler optimizations will not remove the erase operation"; it is a
     nonstandard extension (glibc 2.25, also BSDs); other names are `memset_explicit()` and `memset_s()` (explicit_bzero(3)).
  2. `[S, snippets]` glibc 2.43 added the C23 `memset_explicit`.
  3. `[I]` Zeroing a buffer does not clear registers, spilled copies, swap or core dumps. Combine with `mlock`,
     `MADV_DONTDUMP` and short lifetimes where secrets matter. This is my inference, not read in these sources.

### 4.8 Privilege separation and sandboxing

- URLs: Provos, Friedl, Honeyman, "Preventing Privilege Escalation", USENIX Security 2003
  (<https://www.usenix.org/legacy/events/sec03/tech/full_papers/provos_et_al/provos_et_al.pdf>); man7
  `capabilities.7`, `seccomp.2`, `credentials.7`; kernel `Documentation/userspace-api/no_new_privs.rst`; systemd
  `systemd.exec(5)` (<https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html>, page header
  "systemd 262").
- Licence: paper: noncommercial reproduction for educational or research purposes, notice must be kept (page 1).
  systemd docs LGPL-2.1-or-later (project). Kernel docs GPL-2.0.
- Read how: paper original (design section read); man pages original (grep level); systemd.exec original
  (directive descriptions grep level); `no_new_privs` original.
- Suits: LU, ELU. Not BM.
- Recommendations:
  1. `[S]` OpenSSH privilege separation: a privileged monitor and unprivileged slaves; "A slave must ask the monitor
     to perform any operation that requires privileges", and the monitor validates each request.
  2. `[S]` `no_new_privs` is inherited across fork, clone and execve and cannot be unset; with it, `setuid` bits and file
     capabilities no longer add privilege (no_new_privs.rst). An unprivileged seccomp filter requires it (seccomp(2)).
  3. `[S]` Drop capabilities from the bounding set with `PR_CAPBSET_DROP` (capabilities(7)).
  4. `[S]` systemd units can apply the same ideas declaratively: `NoNewPrivileges=`, `ProtectSystem=`, `ProtectHome=`,
     `PrivateTmp=`, `PrivateDevices=`, `CapabilityBoundingSet=`, `RestrictAddressFamilies=`, `SystemCallFilter=`,
     `MemoryDenyWriteExecute=`, `RestrictNamespaces=`, `DynamicUser=`, `LockPersonality=`, `RestrictSUIDSGID=`.
  5. `[S]` CERT POS36-C and POS37-C: drop supplementary groups, then gid, then uid, and verify the drop worked.
  6. `[I]` For embedded targets, prefer a unit file or init script with these settings over linking a sandbox library.

### 4.9 Other primary sources worth knowing

- CERT ENV33-C, FIO45-C (TOCTOU), POS35-C (symlinks), MSC41-C. Covered under 1.1.
- Kernel `Documentation/process/deprecated.rst` also applies to userspace in spirit (VLAs, `strlcpy`).

---

## Topic 5. Modern C and modern C++

### 5.1 ISO C23 (ISO/IEC 9899:2024) via draft N3220, and compiler support pages

- URLs: <https://open-std.org/jtc1/sc22/wg14/www/docs/n3220.pdf> (title block: "ISO/IEC 9899:2024 (en) N3220 working
  draft"); <https://gcc.gnu.org/projects/c-status.html> ; <https://clang.llvm.org/c_status.html>
- Pin: N3220 file served with last modified date 2024-02-21; GCC and Clang status pages read 2026-11-23.
- Licence: N3220 is a WG14 working draft with the ISO copyright cover sheet; no reuse licence stated. GCC page no
  licence stated (FSF copyright footer).
- Read how: N3220 title page only (4 MB PDF, not read). GCC C status page original.
- Suits: LU, ELU, partly BM (depends on the toolchain).
- What the GCC page `[S]` says about C23:
  1. "C23 mode is the default since GCC 15"; select with `-std=c23` or `-std=gnu23`.
  2. Features listed with GCC versions: `<stdckdint.h>` (14), `nullptr`, `constexpr` for objects, `typeof` and
     `typeof_unqual`, empty initialiser `{}`, `bool` `true` `false` `static_assert` as keywords, `[[nodiscard]]`,
     `[[maybe_unused]]`, `[[fallthrough]]`, `[[deprecated]]`, `unreachable()`, `#embed`, `_BitInt`, digit separators,
     enums with a fixed underlying type, `#elifdef`, `#warning`, `__VA_OPT__`.
  3. Removals: `gets`, trigraphs, implicit `int`, implicit function declarations, K&R style definitions and `()`
     now means `(void)`.
  4. Clang supports `-std=c23` and `-std=c2y` (Clang 19 or later) but says C11 and C23 status is "under
     investigation" for the table.
- `[I]` What to adopt: `nullptr`, `[[nodiscard]]`, `[[fallthrough]]`, `<stdckdint.h>` (where the compiler is GCC 14 or
  later), `memset_explicit` (glibc 2.43 or later), fixed underlying enum types, `constexpr` objects. What to avoid or
  gate: `#embed` and `_BitInt` for portability, anything for a firmware toolchain that only supports C11 or C17.
  Gate by `__STDC_VERSION__` and feature test macros.
- Baseline evidence `[S]`: the kernel builds `-std=gnu11` (`Makefile`, `programming-language.rst`); U-Boot `-std=gnu11`
  (`Makefile` line 538); systemd `c_std=gnu17`; Barr requires C99; GNU Coding Standards say C99 is fine and mention
  nothing newer as required.

### 5.2 C++ language and library: GCC C++ status, libstdc++ and libc++ hardening, Google style

- URLs: <https://gcc.gnu.org/projects/cxx-status.html> ;
  <https://gcc.gnu.org/onlinedocs/libstdc++/manual/using_macros.html> ;
  <https://libcxx.llvm.org/Hardening.html> ; <https://google.github.io/styleguide/cppguide.html>
- Pins: GCC and libc++ pages read 2026-11-23. Google style guide repo `google/styleguide` commit `8bdadbb0732b`
  (2026-11-19), licence CC BY 3.0 (README).
- Read how: original (relevant sections only; I fetched cppreference compiler support pages but did not read them).
- Suits: LU, ELU. BM only for freestanding subsets.
- Recommendations:
  1. `[S]` C++23 features are available in GCC since version 11 and the page calls support "experimental" for the
     latest revision; C++26 since GCC 14.
  2. `[S]` libc++ hardening modes: none, fast, extensive, debug. "Fast mode ... intended to be used in production. We
     recommend most projects adopt this." Hardening "has no impact on the ABI".
  3. `[S]` libstdc++: `_GLIBCXX_ASSERTIONS` is on by default only without optimisation; `_GLIBCXX_DEBUG` is the heavier
     debug mode. OpenSSF recommends `_GLIBCXX_ASSERTIONS` for production.
  4. `[S]` Google style: "We do not use C++ exceptions", "Avoid using run-time type information (RTTI)", targets C++20
     and bans C++23 features at the time of reading ("code should target C++20, i.e., should not use C++23
     features").
  5. `[S]` C++ Core Guidelines E.25 and NR.3 acknowledge that some systems cannot use exceptions.
  6. `[I]` Adopt: `std::span`, `std::string_view` (careful with lifetime), `constexpr`, `std::array`, `enum class`,
     `[[nodiscard]]`, RAII, `std::unique_ptr`, `std::optional`; `std::expected` (C++23) where the toolchain has it.
     Avoid on constrained targets: iostreams, exceptions, RTTI, dynamic allocation after start up, `std::regex`.
     This list is mine; the Core Guidelines support the first group (R, ES, F sections).

### 5.3 `-fno-exceptions` and `-fno-rtti` on embedded C++

No authoritative source on this fetched beyond Core Guidelines E.25 and NR.3, and Google style. `[I]` The guideline
conflict is real (see "Where sources disagree"). A skill should say: the choice is a project level decision, pick one,
enforce it in the build flags, and keep libraries that share headers consistent.

---

## Per-codebase conventions

Authority order for each place: the place's own documents first, then generic advice only where the place is silent.

### Linux kernel (drivers and modules)

Authoritative sources and pins (`torvalds/linux` commit `b6a9fa34ce41`, 2026-11-22):

- `Documentation/process/coding-style.rst`, `deprecated.rst`, `programming-language.rst`, `submitting-patches.rst`
  (all read), `4.Coding.rst` (read), `scripts/checkpatch.pl` with `Documentation/dev-tools/checkpatch.rst` (read),
  `sparse.rst`, `coccinelle.rst`, `kasan.rst`, `ubsan.rst`, `kcov.rst`, `kcsan.rst`, `testing-overview.rst`
  (read in part), `kernel/configs/hardening.config` (read), `Documentation/security/self-protection.rst` (headings
  read), `scripts/Makefile.warn` (read), `Documentation/process/coding-assistants.rst` (read).
- KSPP: <https://kspp.github.io/Recommended_Settings.html> (site repo `KSPP/kspp.github.io` commit `04b2a2c36113`,
  2026-05-14, GPL-2.0 per GitHub; read in part: CONFIG list). The kernsec.org wiki copy was unreachable (expired TLS
  certificate).
- Licence: kernel docs GPL-2.0; Makefile and config files GPL-2.0.

Enforcement tooling `[S]`:

- `scripts/checkpatch.pl` reports ERROR, WARNING, CHECK; "should be viewed as a guide, not as a replacement for human
  judgment" (`submitting-patches.rst`). `--strict` and `--subjective` add checks (`checkpatch.rst`).
- Sparse: `make C=1` (recompiled files) or `C=2` (all files); annotations `__bitwise`, `__user`, `__force`
  (`sparse.rst`).
- Coccinelle: `make coccicheck MODE=report|patch` (`coccinelle.rst`).
- Compiler warnings: `scripts/Makefile.warn` has four groups, `W=1`, `W=2`, `W=3`, `W=e`, combinable (`W=12`);
  `W=1` adds for example `-Wmissing-format-attribute`, `-Wunused-const-variable`; `W=2` adds `-Wshadow`,
  `-Wunused-macros`. `CONFIG_WERROR` defaults to `COMPILE_TEST` and has "If in doubt, say Y"
  (`init/Kconfig`). `4.Coding.rst` says submitted code "should, as a rule, not produce any compiler warnings".
- Runtime: lockdep, KASAN, UBSAN, KCSAN, KFENCE, kmemleak, KCOV (`4.Coding.rst`, `dev-tools/`).
- Formatting aid: `.clang-format` in the tree root (see below).
- The kernel sets its own flags in the top `Makefile`: `-std=gnu11`, `-fno-strict-aliasing`,
  `-fno-delete-null-pointer-checks`, `-fno-strict-overflow`, `-ftrivial-auto-var-init=zero` or `pattern` depending on
  config (lines 473 to 1174).

Where it differs from generic advice `[S]` unless marked:

- No blanket `-Werror` assumption in a patch: whether the tree builds with `-Werror` is a Kconfig choice
  (`CONFIG_WERROR`); the rule is "no warnings", with the flag a switch. Do not add `-Werror` to a driver Makefile.
- Kernel types and helpers replace libc: `u8`, `u32`, `kmalloc`, `kzalloc`, `kmalloc_array`, `kstrtol`, `strscpy`,
  `memcpy` via kernel headers; libc is not available. `printk` and `dev_err` or `pr_*` for messages.
- `goto` based unwinding is the norm, with named labels (chapter 7).
- No `BUG()`; use `WARN_ON_ONCE()` with recovery (chapter 22).
- No VLAs, no `strncpy()`, no `strlcpy()`, no open coded allocator arithmetic (`deprecated.rst`).
- Tabs, 80 columns, no braces around single statements, function brace on its own line, other braces attached.
- No C++ in the tree `[S]` for what `programming-language.rst` names (C `gnu11` and Rust); `[I]` I read no statement
  that forbids C++ explicitly.
- Checkpatch is the acceptance gate; reviewers apply `Signed-off-by` rules. `coding-assistants.rst` says AI agents
  "MUST NOT add Signed-off-by tags" and must read the process documents before fixing bugs. **A skill for the kernel
  should say so.**

Improvements an upstream reviewer would accept `[I]` unless a source is named:

- Run `make W=1` on your own driver and fix what it says; clean `W=1` output is commonly expected for new code. The
  tree documents the levels `[S]`; the "expected for new code" part is my inference from the "no warnings" rule.
- Run sparse (`C=1`) and `make coccicheck`; run `checkpatch.pl --strict` before posting `[S]` that checkpatch exists
  and has `--strict`.
- Build and test with KASAN, UBSAN, lockdep, KCSAN, kmemleak enabled (`[S]` recommended in `4.Coding.rst` and
  `dev-tools/`). `hardening.config` contains `CONFIG_UBSAN_BOUNDS`, `CONFIG_FORTIFY_SOURCE`, `CONFIG_KFENCE`,
  `CONFIG_INIT_STACK_ALL_ZERO`, `CONFIG_LIST_HARDENED` and more `[S]`.
- KUnit and kselftest for tests (`testing-overview.rst`).
- Fuzz with syzkaller (needs `CONFIG_KCOV`, see 3.5). Bugs found are posted with a reproducer. `coding-assistants.rst`
  says unverified bug reports "may cause the report to be ignored" `[S]`.
- KSPP recommended settings and `hardening.config` apply to the kernel configuration of a product, not to a driver
  patch.

Out of tree only `[I]`: extra `-W` flags beyond `W=3` in a vendor driver tree; clang-tidy with a compile database
(only two kernel specific checks exist: `linuxkernel-*`); `-fanalyzer` on kernel code (the GCC manual says
it is for C and does not claim kernel support; I did not test it). Upstream would not take a cleanup patch whose only
purpose is to silence an out of tree tool unless it also fixes a real bug.

### U-Boot

Authoritative sources and pins (`u-boot/u-boot` commit `e578056c766d`, 2026-11-21):

- `doc/develop/codingstyle.rst` (read), `process.rst`, `sending_patches.rst` (read), `checkpatch.rst` (read),
  `testing.rst` (read), `designprinciples.rst`, `security.rst` (read head), top level `Makefile` (read flags),
  `.clang-format`.
- Licence: docs are GPL-2.0+ or GPL-2.0-only (SPDX tags in the files).

What U-Boot says about kernel style `[S]`: "All contributions to U-Boot should conform to the Linux kernel coding
style" and ship `.clang-format`; the net comment exception is Linux only; run `scripts/checkpatch.pl` directly or via
`b4 prep --check` (`codingstyle.rst`). Patch flow: `b4` is "the preferred tool" and U-Boot ships a `.b4-config`;
`patman` "now lives outside the U-Boot tree" (`sending_patches.rst`).

U-Boot specific rules `[S]` (`codingstyle.rst`):

- Use a C structure to map I/O register regions, and check layout with `check_member()`.
- Do not use `#if` in `.c` files where a header stub works; use `IS_ENABLED(CONFIG_X)`; prefer compiling out whole
  functions; mark possibly unused definitions `__maybe_unused`.
- Put a blank line before the final `return`.
- Driver model, logging and Kconfig rules are separate pages.

Tooling `[S]` (Makefile and `scripts/`): `scripts/checkpatch.pl`, `scripts/coccicheck`, Sparse via `C=1`
(Makefile lines 239 to 250), `make W=1|2|3` through `scripts/Makefile.extrawarn`, `buildman` and `binman` in `tools/`,
a pytest suite run on the `sandbox` build (`testing.rst`).

Build flags `[S]` (Makefile lines 535 to 538, 971, 1333):
`-Wall -Werror=strict-prototypes -Werror=implicit-function-declaration -Werror=implicit-int`,
`-fno-strict-aliasing -fno-common -std=gnu11 -ffreestanding -fno-builtin`,
`-Wno-format-security`, `-fstack-protector-strong` where the board enables it, `-fno-strict-overflow`. The Makefile
carries the comment "-Wundef Enable it and fix warnings".

How far U-Boot follows kernel style: nearly all rules (tabs, 80 columns, checkpatch). Differences `[S]`: its own
`.clang-format` has diverged (62 differing lines, with a "U-Boot specific" `ForEachMacros` block), the net comment
exception does not apply, `log_*()` and driver model APIs replace `dev_*()` and `printk`, `CONFIG_IS_ENABLED()`
macros handle SPL and TPL variants, and `-Wno-format-security` is set.

Where it differs from generic advice: same as the kernel for libc: no hosted libc (`-ffreestanding`), U-Boot's own
`printf` and string helpers, constrained stack and malloc heap early in boot (`[I]` from the freestanding flags and the
Holzmann rules; U-Boot docs I read do not state the sizes), no C++.

Improvements likely to be accepted `[I]` except where tagged:

- Sandbox ASan: U-Boot's `arch/sandbox/config.mk` adds `-fsanitize=address` when `CONFIG_ASAN` is set and
  `-fsanitize=fuzzer` when `CONFIG_FUZZ` is set `[S]`; `drivers/fuzz/sandbox_fuzzing_engine.c` is an upstream fuzzing
  engine driver (Google, 2022) `[S]`. So sanitizers and libFuzzer harnesses on the sandbox are upstream supported.
- `scripts/Makefile.kcov` exists upstream `[S]`.
- Run `make W=1` and `checkpatch --strict` on a patch before posting; run the sandbox pytest suite `[S]` (testing.rst).
- Extra static analysis (Cppcheck, clang-tidy, Coverity) on the sandbox build. `[I]` The sandbox build is a hosted
  Linux program, so all userspace tools work. Results on target specific code are not covered.
- Out of tree only: board specific hardening flags without a Kconfig option; a repo wide `-Werror`.

### Linux userspace (and embedded Linux userspace)

There is no single authority. Order of sources:

1. The project's own style, if it has one (systemd, GNU, Busybox, and so on).
2. systemd `CODING_STYLE.md` as the best maintained written userspace style that targets modern Linux APIs (read,
   pin `e691c3d7c145`).
3. GNU Coding Standards (read, last updated April 27, 2026) for GNU style projects.
4. Barr Group BARR-C:2018 and Zephyr guidelines (read) for firmware-adjacent userspace on small targets.
5. OpenSSF compiler guide (read) for flags, CERT C (read titles) for rules.

Enforcement tooling in userspace projects: `.clang-format` and `.editorconfig` (systemd has both; `.clang-format`
SHA `55d98e79` at the pinned commit), clang-tidy (systemd's style says clang-tidy reports direct `open()` calls `[S]`),
Cppcheck, sanitizers in CI, OSS-Fuzz.

Where userspace differs from the kernel `[S]`: libc is available and error returns use `errno` with `-1`, `<stdint.h>`
types not `u32` (systemd: "Do not use kernel types like `u32`"), `-std=gnu17` (systemd), threads are allowed but
systemd avoids them.

Is the seL4 astylerc a reasonable default for Linux userspace C? Facts and judgment:

- The file (`seL4/seL4_tools` `misc/astylerc`, commit `6493e0c6fab3`, 2026-10-26, BSD-2-Clause per its header;
  GitHub reports NOASSERTION): `style=otbs`, `indent=spaces=4`, `pad-header`, `attach-closing-while`, `pad-oper`,
  `pad-comma`, `unpad-paren`, `align-pointer=name`, `add-braces`, `attach-return-type`, `convert-tabs`,
  `min-conditional-indent=0`, `max-code-length=120`, `max-continuation-indent=120` `[S]`.
- It matches BARR-C only in "always use braces" (1.3a). It differs from BARR-C on brace placement.
- It contradicts the kernel and U-Boot (tabs, 80 columns, no braces on single statements) and systemd (8 spaces,
  no braces on single statements, `const char* foo(...)` return type spelling, `(const char*) s` casts) `[S]`.
- Measured: running it on a 865 line kernel file changed 731 lines (k_string.c, `--options=<file>` only); on a
  72 line kernel file it changed 76 lines; on a U-Boot file of 344 lines it changed 400. Counts are `<` plus `>` lines
  from `diff`.
- `[I]` Judgment. It is a sensible default for a **new, self-contained** C project that is allowed to pick its style,
  particularly one that wants always-braces (MISRA 15.6, CERT EXP19-C, BARR-C 1.3a). It is a poor default for a
  tree that follows another style. For userspace C that must fit an existing ecosystem, follow that ecosystem. For a
  greenfield userspace project, systemd's style is the closest Linux native written standard; its rules differ on
  single statement braces (systemd forbids them for single lines, seL4's profile adds them), so the two cannot both be
  adopted. A skill should say "use the repository's own style files first; use the personal default only when the
  repository has none".

### Formatter findings: astyle versus clang-format on kernel style

Evidence, mostly measured. Sample size is small (four kernel files, three U-Boot files, tip of tree on 2026-11-23).
Treat as indicative.

Usage evidence (which formatter do embedded and kernel adjacent projects use). Checked with the GitHub contents API
for `.clang-format` and `.astylerc` at repo root, 2026-11-23:

- `.clang-format` present: Linux kernel, U-Boot, Zephyr, systemd, RIOT, RT-Thread, OpenSBI, coreboot, OP-TEE OS.
- `.astylerc` at the root: Arm Mbed OS (archived upstream status unclear; last push 2024-10-08). PX4 keeps
  `Tools/astyle/astylerc` and check scripts; ArduPilot keeps `Tools/CodeStyle/astylerc` and `ardupilot-astyle.sh`.
  A code search for filename `.astylerc` also returned arkime, tinc, newsboat, igraph, syslog-ng and others.
- No formatter config at the root of the repos I checked: FreeRTOS-Kernel, esp-idf, micropython, NuttX, pico-sdk,
  edk2, openwrt, seL4 (seL4 keeps its astylerc in `seL4_tools`).
- `[I]` Result: clang-format is the norm in kernel, U-Boot and RTOS trees. astyle is used by a minority, mainly
  flight control and a few userspace projects. This is a sample of 24 repos I chose, not a census.

Can astyle reproduce kernel style `[S]` plus measured `[M]`:

- `[S]` `--style=linux` (`-A8`): "Opening braces are broken from namespace, class, and function definitions. The
  braces are attached to everything else", "frequently used with an indent of 8 spaces"; the docs call it Kernel
  Normal Form. `--indent=force-tab=8` (`-T8`) indents with tabs counted as 8.
- `[M]` Command: `astyle --options=none --style=linux --indent=force-tab=8 --suffix=none <file>`. Lines changed on
  files that already follow kernel style: `lib/kstrtox.c` 52 of 541, `lib/list_debug.c` 36 of 72, `lib/string.c` 20
  of 865, `drivers/char/random.c` 202 of 1712 (counts are `<` plus `>` diff lines).
- `[M]` Falls short:
  1. It re-indents macro bodies (`#define kstrto_from_user(...)` was rewritten and re-aligned).
  2. It re-spaces casts: `(long long)-tmp` became `(long long) - tmp`, which changes how the code reads.
  3. It re-aligns wrapped function arguments differently from kernel practice (`lib/list_debug.c`).
  4. On U-Boot `drivers/serial/serial_pl01x.c` it **indented top level declarations by a tab** inside an
     `#if !CONFIG_IS_ENABLED(DM_SERIAL)` block, a clear misparse of conditional compilation.
  5. It splits `c1 = 0; c2 = 0;` style multi statement lines (U-Boot `lib/string.c`), which kernel style tolerates.
- `[M]` The kernel's own `.clang-format` (clang-format 23.1.5, `--style=file:.clang-format`) also does not leave kernel
  files unchanged: `kstrtox.c` 99, `list_debug.c` 69, `string.c` 23, `random.c` 304 changed lines. The kernel docs say
  the file "tr[ies] to approximate the most common kernel coding style" and "not all the kernel follows the same
  style" `[S]` (`Documentation/dev-tools/clang-format.rst`). On the U-Boot files with U-Boot's own
  `.clang-format`: `cli.c` 27, `serial_pl01x.c` 55, `echo.c` 9 changed lines. (astyle: `cli.c` 20, `serial_pl01x.c` 40,
  `echo.c` 0.) Lines changed is not a quality measure; many are alignment details.
- `[I]` Neither tool is exact. Use `checkpatch.pl` as the kernel and U-Boot gate and use a formatter only on new
  code you wrote, or only on changed lines (`git clang-format`), and review the diff.

The kernel `.clang-format` `[S]`: header "Intended for clang-format >= 11" (`.clang-format` line 3), `UseTab: Always`,
`TabWidth: 8`, `IndentWidth: 8`, `ColumnLimit: 80`, 807 lines in the tree at the pinned commit, a long `ForEachMacros`
list; `clang-format.rst` says tweaks per subsystem go in a subdirectory `.clang-format`. U-Boot ships its own, which
now differs from the kernel's (62 diff lines).

Option lookup protects the kernel from a personal default only if the command says so: see 3.6, items 2 to 5 of the
astyle option file lookup.

---

## Where sources disagree

01. **Braces on single statements.** BARR-C 1.3, MISRA 15.6 (via Zephyr), CERT EXP19-C and the seL4 astylerc require braces.
    Kernel style, systemd and U-Boot forbid them on single statements.
02. **Brace placement.** BARR-C wants every left brace on its own line. Kernel and systemd put function braces differently
    (kernel: own line; systemd: same line, "try to write `void foo() {`"). GNU puts the function brace in column one.
03. **Line length.** Kernel 80, GNU 79, systemd about 109, seL4 profile 120.
04. **Indent.** Kernel and U-Boot tabs of 8; systemd 8 spaces; seL4 profile 4 spaces; BARR-C its own rule (not read in
    detail).
05. **`goto`.** Kernel mandates it for cleanup. BARR-C says avoid it but allows it for exceptional cases. Power of Ten and
    Core Guidelines ES.76 say avoid; MISRA subset keeps the rule on label placement (Rule 15.3).
06. **`-Werror`.** OpenSSF: only during development. Kernel: Kconfig choice, default only for `COMPILE_TEST`.
    Poky: `-Werror=format-security` always on. `[I]` These agree once "blanket" versus "selective" is the dividing line.
07. **Exceptions in C++.** Core Guidelines E.25 and NR.3 favour them but accept limits. Google style bans them. Embedded
    projects usually ban them. CERT C++ assumes them.
08. **C and C++ boundary.** Core Guidelines CPL.2 says compile C as C++; kernel, systemd and BARR-C 1.1b keep C as C. These
    cannot both be followed.
09. **Types.** systemd: do not use kernel `u32`; kernel: use them. BARR-C: no `short` or `long`, systemd: no `short` types.
10. **`_FORTIFY_SOURCE` level.** OpenSSF says 3; Poky uses 2; Buildroot offers 1 to 3; GCC `-fhardened` uses 3.
    The tradeoff is breakage of code that uses flexible array extensions or `malloc_usable_size` `[S]` (OpenSSF).
11. **Standard to target.** Kernel and U-Boot gnu11, systemd gnu17, BARR-C C99, GCC 15 default gnu23, Google style C++20,
    CERT C++ C++14, MISRA C++:2023 C++17.
12. **`-fanalyzer` readiness.** GCC says C only and not sound or complete; some projects rely on it anyway. I found no
    kernel statement either way.
13. **Fork versus spawn.** The HotOS paper says deprecate fork; systemd uses `posix_spawn` and `fork` plus `exec` as the
    situation needs; man pages describe both.

## Gaps and things I did not reach

- MISRA C:2025 and MISRA C++:2023 rule text: paywalled. Free items were identified only from search snippets.
- kernsec.org wiki: expired TLS certificate; I did not bypass it. KSPP content read from `kspp.github.io` instead.
- langsec.org: TLS certificate error; the primary paper was read from usenix.org.
- Red Hat `_FORTIFY_SOURCE=3` article, Debian and Fedora hardening pages: not fetched (cited through OpenSSF only).
- N3220 body, C++ standard text, cppreference pages: not read. C23 facts come from GCC and Clang status pages.
- Wheeler's HOWTO chapters and the SEI CERT rule bodies: not read.
- Barr Group text read was the 2018 PDF; I did not read its naming and comment chapters.
- Kernel documentation licensing: file level SPDX tags only; `COPYING` not re-read.
- The tool counts for astyle versus clang-format are from a single run on seven files.

---

## Ranked list: ten most useful sources overall

01. **OpenSSF Compiler Options Hardening Guide for C and C++** (2026-08-20): one flag set with rationale and costs; the
    best single basis for build rules.
02. **Linux kernel `coding-style.rst`, `deprecated.rst`, `4.Coding.rst` and `checkpatch` docs**: the authority for
    anything that lands in the kernel or U-Boot, and a rich list of banned patterns.
03. **SEI CERT C Coding Standard** (repo `73ee7a0dbe77`): numbered, tool mapped rules with CC BY 4.0, usable in citations.
04. **systemd `CODING_STYLE.md`**: the most concrete, current written style for modern Linux userspace C (fd hygiene,
    error codes, allocation, `posix_spawn`).
05. **Linux man-pages 6.17** (`open`, `rename`, `fsync`, `posix_spawn`, `system`, `signal-safety`, `signalfd`,
    `explicit_bzero`): primary text for every pattern in topic 4.
06. **C++ Core Guidelines** (2026-06-14): the broadest modern C++ rule set, with the licence limit noted.
07. **U-Boot `codingstyle.rst`, `sending_patches.rst`, `Makefile` and sandbox sanitizer support**: shows exactly where
    U-Boot follows the kernel and where it does not, and which tools upstream accepts.
08. **Clang and LLVM sanitizer, libFuzzer and clang-tidy documentation**: authoritative on cost, flags and check families
    for the analysis stack.
09. **GCC manual (warnings, `-fanalyzer`, `-fhardened`, integer overflow builtins) and the GCC C and C++ status pages**:
    the ground truth for what each GCC release does, including that GCC 15 defaults to C23.
10. **BARR-C:2018 with the Zephyr MISRA subset and the Power of Ten**: the best readable embedded rule sources. The Barr
    PDF has a strict internal use licence; the other two are freer.
