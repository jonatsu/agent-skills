# C, C++, and Embedded Linux: Sources for the Skill Work

Date: 2026-11-23. Prepared for new C and C++ skills and for extending the embedded Linux skills
(`yocto-openembedded-development`, `buildroot-development`, `u-boot-development`, `embedded-linux-bringup`). The code
these skills serve lives in three places, the Linux kernel, U-Boot, and Linux userspace on embedded devices, and must
match each place's own conventions, with improvements added on top.

| File                                                       | What it holds                                                                                                               |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| [c-cpp-practice.md](c-cpp-practice.md)                     | Coding standards, compiler hardening, analysis and sanitizers, userspace patterns, modern C and C++, and per-codebase rules |
| [embedded-linux-practice.md](embedded-linux-practice.md)   | Yocto and OpenEmbedded, Buildroot, expert training material, device robustness, and product security                        |
| [language-standards.md](language-standards.md)             | Compiler defaults per build system and release, the standards projects and SDKs declare, and proposed default standards     |
| [third-party-skills.md](third-party-skills.md)             | About 90 third-party agent skills surveyed, 11 assessed in depth, with licences, pins, and red flags                        |
| [work-session-refinements.md](work-session-refinements.md) | Eight refinements found by applying a draft C rule set to two small tools, with the tool versions used                      |

Four Sonnet research lanes wrote the first four files from primary sources where reachable, and each marks what a
source says apart from its own inference. Each file lists what it could not reach.

## What the Sources Settle

- **Each codebase keeps its own style.** The kernel's documents bind kernel code, and U-Boot says its code "should
  conform to the Linux kernel coding style" with its own deviations. Userspace has no single authority: a project's own
  style comes first, then systemd's `CODING_STYLE.md` as the best maintained written Linux userspace style.
- **The build flags have one reasoned basis.** The OpenSSF Compiler Options Hardening Guide (2026-08-20, CC BY 4.0) is
  the only source with a full flag set and its costs. Yocto's `security_flags.inc` and Buildroot's options carry a
  subset, so a recipe or package must honour `CC`, `CXX`, `CPPFLAGS`, `CFLAGS`, `CXXFLAGS`, and `LDFLAGS` rather than
  rely on the build system to fix a hard-coded Makefile.
- **The rule sets to cite are free to read.** SEI CERT C and C++ are CC BY 4.0. MISRA is paywalled, and BARR-C and the
  C++ Core Guidelines restrict reuse to internal use, so a skill may cite them and state ideas but copy no text.
- **Every userspace pattern has a primary source.** The Linux man-pages (6.17) cover atomic replacement with `fsync`,
  `O_CLOEXEC`, `posix_spawn`, signal safety, `signalfd`, and `explicit_bzero`.
- **Upstream supports more checking than projects use.** The kernel documents `W=1` and `W=2`, sparse, Coccinelle,
  KASAN, UBSAN, KCSAN, and syzkaller. U-Boot's sandbox build supports ASan and libFuzzer upstream.

## Findings That Change the Working Draft

- **GCC 15 compiles C23 by default** (`gnu23`), so a C17 rule must set `-std=gnu17` explicitly.
- **astyle ignores a project `.astylerc` unless told.** It reads one only with `--project` or
  `ARTISTIC_STYLE_PROJECT_OPTIONS`; otherwise the personal default applies. The user's default derives from seL4's
  profile (four spaces, always braces) and rewrote 731 of 865 lines of a kernel file. In kernel and U-Boot trees, run a
  formatter only with the tree's own configuration, and only on changed lines.
- **No formatter reproduces kernel style exactly.** The kernel's own `.clang-format` changed more lines of kernel files
  than astyle in Linux mode, and U-Boot's `.clang-format` has diverged from the kernel's. `checkpatch.pl` is the gate.
- **Kernel style through clang-format needs `DontAlign`** for brackets and operands, or continuation lines mix tabs and
  spaces.
- **AI attribution is per project and per version, so these skills stay silent on it.** At the pinned commits, the
  kernel forbids agents adding `Signed-off-by`, OE-Core and BitBake require an `AI-Generated:` line, and Zephyr keeps
  `Assisted-by:`. The third-party survey reports that mainline Linux dropped its `Assisted-by:` requirement on
  2026-10-14, so older kernel trees still carry it, and some projects forbid every attribution. Whether to attribute
  belongs to the user's commit rules and the repository's own instructions, never to a coding skill.
- **The skills must work across many conventions and versions.** Projects pin old releases for years: a Yocto LTS, a
  vendor kernel, an older U-Boot. A rule that changed between releases belongs in the skill as "read it from the tree
  you are working in", naming the document to read (such as the kernel's `coding-assistants.rst`, a project's
  `AGENTS.md`, or its `.clang-format`), never as one release's answer.

## Where Sources Disagree

These need a decision when the skills are written:

- braces on single statements: required by CERT, MISRA, BARR-C, and the seL4 profile, forbidden by kernel, U-Boot, and
  systemd style;
- `_FORTIFY_SOURCE` level: 3 in OpenSSF and GCC's `-fhardened`, 2 in Yocto, 1 by default in Buildroot;
- the standard to target: `gnu11` in the kernel and U-Boot, `gnu17` in systemd, C23 as GCC 15's default;
- C++ exceptions: favoured by the Core Guidelines, banned by Google style and most embedded projects;
- `-Werror`: development only in OpenSSF, a Kconfig choice in the kernel, selective in Yocto;
- the persistent journal and the writable filesystem on flash, where no source gives a product recommendation.

## Third-Party Skills

No third-party skill covers this space at the quality of the first-party sources. The strongest are
`UtsavBalar1231/kernel-development-skills` and `mohitmishra786/low-level-dev-skills` (both MIT), each with a defect
noted in [third-party-skills.md](third-party-skills.md). No third-party Buildroot, kas, or defensive U-Boot skill
exists. Projects' own agent instruction files (OE-Core, BitBake, Linux, Zephyr) are the most authoritative examples of
"rules agents get wrong".
