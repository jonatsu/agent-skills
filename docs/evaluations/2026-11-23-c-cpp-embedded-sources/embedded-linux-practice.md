# Embedded Linux Practice Sources

Read date: 2026-11-23. Purpose: ground new Yocto, Buildroot and userland C and C++ rules for embedded Linux in
recognised sources.

Conventions in this file:

- "Says" marks what the source states. "Inference" marks my own reading or conclusion.
- "How read" is one of: original (fetched and read the page or file itself), fetch summary (a tool summarised it),
  search snippets only.
- Pins use the release, tag, commit or page date that the source itself shows.
- Where a page shows no licence, the entry says "no licence stated".

## 1. Yocto Project and OpenEmbedded

Current releases on the read date (Says, <https://www.yoctoproject.org/development/releases/>): 6.1 "blacksail", released
September 2026, stable until April 2027; 6.0 "wrynose", released April 2026, LTS until April 2030, at 6.0.4 in
September 2026. Previous LTS: 5.0 "scarthgap". All manual pages below were read at <https://docs.yoctoproject.org/6.1/>
(blacksail) unless stated. The unversioned URL shows "6.1-tip", a moving development snapshot, so cite the versioned
path.

Licence of the Yocto manuals (Says, footer of every manual page, e.g. security manual index): Creative Commons
Attribution-Share Alike 2.0 UK: England and Wales.

### 1.1 Yocto Project Development Tasks Manual, "Writing a New Recipe" (dev-manual/new-recipe)

- URL: <https://docs.yoctoproject.org/6.1/dev-manual/new-recipe.html>
- Version: Yocto 6.1 blacksail docs. Licence: CC BY-SA 2.0 UK (see above). How read: original, fetched as HTML and
  converted to text.
- Recommendations (Says):
  1. Section "Building a Single .c File Package" compiles with `${CC} ${LDFLAGS} helloworld.c -o helloworld`, with
     `S = "${UNPACKDIR}"`, and installs with `install -d ${D}${bindir}` then `install -m 0755`. Inference: this example
     passes LDFLAGS but not CFLAGS, so a recipe that wants the distro security and debug flags should write
     `${CC} ${CFLAGS} ${LDFLAGS}`. The manual does not state that. See 1.7 for why this matters.

  2. Section "Building a Makefile-Based Package": no `do_compile` is needed because BitBake runs `make`. Put extra make
     options in `EXTRA_OEMAKE` or `PACKAGECONFIG_CONFARGS`. A `do_install` is still required, otherwise an empty one
     runs.

  3. Same section: the lz4 example passes the build system flags to the Makefile explicitly, and installs with
     `do_install() { oe_runmake install }`:

     ```text
     EXTRA_OEMAKE = "PREFIX=${prefix} CC='${CC}' CFLAGS='${CFLAGS}' DESTDIR=${D} LIBDIR=${libdir} INCLUDEDIR=${includedir} ..."
     ```

  4. Same section: extra compiler parameters go in the `CFLAGS` variable, for example
     `CFLAGS:prepend = "-I ${S}/include "`.

  5. Section "Installing": for plain Makefiles, `do_install` calls `oe_runmake install` and passes the destination, for
     example `DESTDIR=${D}`. Files go to `${D}` mirroring the target layout.

  6. Section "Enabling System Services": a recipe that ships a systemd unit inherits the `systemd` class. The reference
     manual's `systemd` class entry adds that the class is inert unless `systemd` is in `DISTRO_FEATURES`, that
     `SYSTEMD_SERVICE:${PN}` names the unit, and that services start at boot unless `SYSTEMD_AUTO_ENABLE` is `disable`.

  7. Section "Splitting an Application into Multiple Packages": by default a recipe builds `${PN}`, `${PN}-dbg`,
     `${PN}-dev`. Customise with `PACKAGES` and `FILES`.

  8. The page shows `CFLAGS:append`, `CFLAGS:prepend` and machine-specific overrides such as `CFLAGS:append:sh4`.

### 1.2 Yocto Project Reference Manual, "QA Error and Warning Messages" (ref-manual/qa-checks) and the `insane` class

- URLs: <https://docs.yoctoproject.org/6.1/ref-manual/qa-checks.html> and
  <https://docs.yoctoproject.org/6.1/ref-manual/classes.html> (section insane).
- Version: 6.1 docs. Licence: CC BY-SA 2.0 UK. How read: original. I also read the code that sets the defaults:
  `meta/classes-global/insane.bbclass` on branch `blacksail` of <https://github.com/openembedded/openembedded-core> (file
  blob sha 721088a8f588106809b9a0fe8511001957c6b2fa). GitHub reports no standard licence for that repository
  ("NOASSERTION"); OE-Core states MIT and GPL-2.0-only in its own LICENSE files per the Yocto style guide (1.3).
- Recommendations (Says):
  1. `ldflags`: "File ... doesn't have GNU_HASH (didn't pass LDFLAGS?)". Check that LDFLAGS reach the linker. The
     documented workaround is `TARGET_CC_ARCH += "${LDFLAGS}"` in the recipe.
  2. `already-stripped`: upstream build scripts often strip binaries, which blocks debug symbol extraction into `-dbg`.
     Disable stripping in the upstream build (configure option, or patch out `strip`, `STRIP`, `-s`, `-S`, or `-Wl,-s`).
     The manual adds that the final packaged binaries are still stripped by the build system.
  3. `textrel`: relocations in `.text`. The manual suggests adding `-fPIC` or `-fpic`, for example `CFLAGS:append = " -fPIC"`.
  4. `buildpaths`: TMPDIR must not appear in output files. It leaks build configuration and hurts reproducibility. Fix
     by using relative paths or runtime configuration.
  5. `rpaths`: build system paths in RPATH or RUNPATH are incorrect for the target and a possible security issue.
     Disable rpath in the upstream build.
  6. `staticdev` and `dev-so`: `.a` files go in `-staticdev`, `.so` development symlinks go in `-dev`. Fix with `FILES`
     and `PACKAGES`.
  7. `INSANE_SKIP:${PN} += "dev-so"` skips a check per package. The insane class text says to use `INSANE_SKIP` for
     recipes and `WARN_QA` or `ERROR_QA` globally, and to be careful because the checks detect real problems.
  8. Source of defaults (Says, insane.bbclass at blacksail): `ERROR_QA` defaults to
     `already-stripped arch buildpaths build-deps debug-deps dev-deps dev-elf dev-so empty-dirs file-rdeps`
     `ldflags libdir missing-ptest rpaths staticdev textrel version-going-backwards`
     plus the `usrmerge` check when that distro feature is on. `WARN_QA` defaults to
     `32bit-time native-last pep517-backend`. Inference: `ldflags`, `textrel`, `rpaths`, `buildpaths` and
     `already-stripped` fail the build by default, so a C or C++ recipe has to satisfy them.

### 1.3 Yocto Project Contributor Guide, "Recipe Style Guide" (replaces the OE wiki style guide)

- URL: <https://docs.yoctoproject.org/6.1/contributor-guide/recipe-style-guide.html>
- Version: 6.1 docs. Licence: CC BY-SA 2.0 UK. How read: original.
- Recommendations (Says):
  1. Recipe path is `recipes-category/recipename/recipename_version.bb`; no hyphens in the version.
  2. Variable formatting: spaces around the operator, double quotes, four spaces for indentation, continuation lines
     aligned with the opening quote.
  3. Required variables in every recipe: `SUMMARY`, `DESCRIPTION`, `HOMEPAGE`, `BUGTRACKER`. Recommended order starts
     with SUMMARY, DESCRIPTION, HOMEPAGE, BUGTRACKER, SECTION, LICENSE, LIC_FILES_CHKSUM, DEPENDS, PROVIDES, PV,
     SRC_URI, SRCREV, S, inherit, PACKAGECONFIG, class variables such as EXTRA_OECONF, tasks, PACKAGE_ARCH, PACKAGES,
     FILES, RDEPENDS and the rest.
  4. Define both `LICENSE` and `LIC_FILES_CHKSUM`. Use `License-Update:` in the commit message when they change.
  5. Use `BBCLASSEXTEND` rather than separate `-native` and `-nativesdk` recipes.
  6. Tasks must be idempotent. When editing a file in a task, copy `X` to `X.orig` once, copy it back, then modify it.
  7. Every patch carries an `Upstream-Status:` tag and a description. CVE patches carry a `CVE:` tag (also stated in the
     security manual, 1.5).
  8. Versions: use `~` for pre-releases (`1.5~rc2`), use `PV = "<version>+git"` for untagged git revisions, set `PE`
     when versions stop increasing.
  9. Shell function indentation is consistent within a layer.

### 1.4 Yocto Development Tasks Manual, licence compliance over a product's life (dev-manual/licenses)

- URL: <https://docs.yoctoproject.org/6.1/dev-manual/licenses.html>
- Version: 6.1 docs. Licence: CC BY-SA 2.0 UK. How read: original, searched for the compliance settings.
- Recommendations (Says):
  1. To ship source, enable the `archiver` class: `INHERIT += "archiver"` with, for example,
     `ARCHIVER_MODE[src] = "original"`. Providing all of `DL_DIR` is possible but large.
  2. To ship licence texts: `COPY_LIC_MANIFEST = "1"`, `COPY_LIC_DIRS = "1"`, `LICENSE_CREATE_PACKAGE = "1"`. The page
     explains that the first two copy licences at image build time and do not cover packages installed later, which
     `LICENSE_CREATE_PACKAGE` covers.
  3. Note on static linking: a package pulled in only through a statically linked library recipe may not appear in the
     generated licence manifest (section "Compliance Limitations with Executables Built from Static Libraries").

### 1.5 Yocto Project Security Manual (security-manual)

- URLs: <https://docs.yoctoproject.org/6.1/security-manual/securing-images.html>, `/build-process-security.html`,
  `/vulnerabilities.html`, `/read-only-rootfs.html`, `/sstate-signing.html`. Section 4 (vulnerabilities) also read at
  <https://docs.yoctoproject.org/6.0.4/security-manual/vulnerabilities.html>; the CVE tooling is the same in 6.0.4 and
  6.1.
- Version: 6.1 docs (with 6.0.4 cross-check). Licence: CC BY-SA 2.0 UK. How read: original.
- Recommendations (Says):
  01. Section 3.1 "General Considerations": run static analysis on your own application code; make sure the device can be
      updated; scan for CVEs regularly; update BitBake and layers from stable and LTS branches; remove debugging
      functionality from the final image; run no unneeded network services; remove unneeded software; enable hardware
      secure boot where available.
  02. Section 3.2 "Security Flags": enable `require conf/distro/include/security_flags.inc` in `local.conf` or the distro
      config. The page adds that some flags are enabled or disabled per recipe by default.
  03. Section 3.3: remove `allow-empty-password`, `empty-root-password` and `allow-root-login` from
      `EXTRA_IMAGE_FEATURES` (or the `core/yocto/root-login-with-empty-password` fragment) before production. Use the
      `extrausers` class for passwords. Do not set the same password on every device. Consider a MAC framework (SELinux
      or Smack), see the `meta-selinux` layer.
  04. Section 3.4: hardening tools live in the `meta-security` layer.
  05. Section 4.2 "Vulnerability check at build time": enable with
      `bitbake-config-build enable-fragment core/yocto/sbom-cve-check` or `OE_FRAGMENTS += "core/yocto/sbom-cve-check"`.
      This enables the `sbom-cve-check` class. It writes `<image>-<machine>.rootfs.sbom-cve-check.yocto.json` and an
      enriched `.spdx.json` to `DEPLOY_DIR_IMAGE`. CVE status is Patched, Unpatched or Ignored.
      `SBOM_CVE_CHECK_SHOW_WARNINGS = "1"` prints warnings. `include conf/distro/include/cve-extra-exclusions.inc`
      excludes entries judged not to affect OE-Core.
  06. Section 4.3: fix wrong CVE to recipe mappings with `CVE_PRODUCT` (for example `"flex_project:flex westes:flex"`)
      and `CVE_VERSION`. The manual prefers fixing wrong NVD data at NVD.
  07. Section 4.4: fix by upgrading, by a patch, or by `CVE_STATUS[CVE-xxxx-yyyy] = "reason: text"`. Patches need a
      `CVE: CVE-...` tag and an `Upstream-Status:` tag. Use upstream patches, not other distributions' patches, unless
      they are the only source. Name the patch after the CVE. On stable branches, prefer a backward compatible minor
      upgrade, otherwise backport.
  08. Section 5 "Creating a Read-Only Root Filesystem": add `IMAGE_FEATURES += "read-only-rootfs"`. All `pkg_postinst`
      scripts must succeed at image build time (use `$D` before absolute paths, use native tools or `qemu_run_binary`),
      otherwise the build fails. Applications must write only to writable places such as `/tmp` or `/var/run`.
  09. Section 2 "Build Process Security": `DL_DIR` and sstate are trusted once populated; OE-Core is tested for
      reproducibility but other layers may not be; build environments should be disposable.
  10. Section 6 "Shared State Signing": covers GPG signing of sstate artefacts (read only as an index; not summarised further).
- Release note (Says, release notes 6.0 and 6.1): `sbom-cve-check` and `sbom-cve-check-recipe` classes arrived in 6.0
  and obsolete the `cve-check` class. Any older guidance that tells you to enable `cve-check` is out of date for 6.0 and
  later.

### 1.6 Yocto Project Development Tasks Manual, "Creating a Software Bill of Materials" (dev-manual/sbom)

- URL: <https://docs.yoctoproject.org/6.1/dev-manual/sbom.html>
- Version: 6.1 docs. Licence: CC BY-SA 2.0 UK. How read: original.
- Recommendations (Says):
  1. The `create-spdx` class runs by default through `INHERIT_DISTRO`. Output is `<image>-<machine>.spdx.json` in
     `tmp/deploy/images/<machine>/`. Disable with `INHERIT_DISTRO:remove = "create-spdx"` only if you must.
  2. Generate a recipe-only SBOM with `bitbake <recipe> -c create_recipe_sbom`.
  3. Options named on the page: `SPDX_PRETTY`, `SPDX_INCLUDE_SOURCES`, `SPDX_INCLUDE_COMPILED_SOURCES`,
     `SPDX_INCLUDE_KERNEL_CONFIG`, `SPDX_INCLUDE_PACKAGECONFIG`, `SPDX_FILE_EXCLUDE_PATTERNS`, supplier fields
     (`SPDX_IMAGE_SUPPLIER`, `SPDX_SDK_SUPPLIER`, `SPDX_PACKAGE_SUPPLIER`), package URLs (PURLs) for language
     ecosystems, and build provenance (`SPDX_INVOKED_BY`, `SPDX_ON_BEHALF_OF`).
  4. The page calls the SBOM "the most standard way to provide information about the Software Supply Chain" and ties it
     to licence compliance and vulnerability exposure.

### 1.7 `security_flags.inc` in OpenEmbedded-Core

- URL: <https://github.com/openembedded/openembedded-core/blob/blacksail/meta/conf/distro/include/security_flags.inc>
  (blob sha 824ba2c0e3f1933a39eb62df7fd3eea6e031c89d on `blacksail`; identical on `wrynose` and `master` on the read
  date; `blacksail` branch head commit 5b458838c126051c884c8cb5225c7265d1483ea6, 2026-11-14).
- Licence: no per-file licence stated; OE-Core licence files apply (MIT for most metadata). How read: original, fetched
  through the GitHub API.
- Says:
  1. Default flags:
     `SECURITY_CFLAGS = ${SECURITY_STACK_PROTECTOR} ${SECURITY_PIE_CFLAGS} ${lcl_maybe_fortify} ${SECURITY_STRINGFORMAT}`
     with `-fstack-protector-strong`, `-D_FORTIFY_SOURCE=2` (only when optimisation is not `-O0`),
     `-Wformat -Wformat-security -Werror=format-security`. `SECURITY_LDFLAGS = -Wl,-z,relro,-z,now`. PIE comes from
     GCC's `--enable-default-pie` (`GCCPIE`), with `-pie -fPIE` injected only when GCC lacks it.
  2. The flags are attached to the compiler wrapper variable, not only to CFLAGS:
     `TARGET_CC_ARCH:append:class-target = " ${SECURITY_CFLAGS}"` and
     `TARGET_LDFLAGS:append:class-target = " ${SECURITY_LDFLAGS}"`.
  3. The file opens by saying these flags "don't work universally", that per-recipe overrides exist, and that the goal
     is to shrink that list over time. Examples of opt outs: glibc, gcc-runtime, grub, valgrind, sysklogd.
- Inference: because the flags ride on `TARGET_CC_ARCH`, a recipe that calls `${CC}` gets them even when it ignores
  CFLAGS. A Makefile that hardcodes `gcc` or `cc` gets neither flags nor the cross compiler, and fails earlier. A recipe
  that links with `ld` directly misses `LDFLAGS`, which is the reason for the `ldflags` QA check and the
  `TARGET_CC_ARCH += "${LDFLAGS}"` workaround.

### 1.8 Yocto Project Reference Manual, glossary entries for flags (ref-manual/variables)

- URL: <https://docs.yoctoproject.org/6.1/ref-manual/variables.html> (entries TARGET_CFLAGS, TARGET_CXXFLAGS,
  TARGET_CPPFLAGS, TARGET_LDFLAGS, TARGET_CC_ARCH, DEBUG_BUILD, DEBUG_OPTIMIZATION, DEBUG_PREFIX_MAP, SOURCE_DATE_EPOCH,
  INSANE_SKIP).
- Version: 6.1 docs. Licence: CC BY-SA 2.0 UK. How read: original. SECURITY_CFLAGS has no glossary entry; its only
  documentation is `security_flags.inc` and the security manual (1.5, 1.7).
- Says:
  1. In the target context `CFLAGS`, `CXXFLAGS`, `CPPFLAGS` and `LDFLAGS` are set from the matching `TARGET_*` variable.
     The SDK environment script exports the same values.
  2. `TARGET_CC_ARCH` holds architecture specific compiler flags and is initialised from `TUNE_CCARGS`. The note says
     appending LDFLAGS to it is a common workaround for recipes that ignore exported LDFLAGS.
  3. `DEBUG_PREFIX_MAP` sets `-fdebug-prefix-map`, `-fmacro-prefix-map` and `-ffile-prefix-map` so debug sections hold
     install time paths. The cost is that the debugger needs to be told where the sources are.
  4. `SOURCE_DATE_EPOCH` is computed per recipe from the sources by `meta/lib/oe/reproducible.py`; a recipe can override
     it.
  5. `DEBUG_OPTIMIZATION` defaults to `-Og ${DEBUG_LEVELFLAG}`.
- Note (Says, 6.1 `variables` page, entry for CXXFLAGS and CXX): the manual documents `TARGET_CXXFLAGS`; I did not find
  a separate "CXX" recommendation. Inference: for C++ use `${CXX}` with `${CXXFLAGS}` and `${LDFLAGS}`, mirroring the C
  pattern in 1.1.

### 1.9 Yocto Project Test Manual, "Reproducible Builds" (test-manual/reproducible-builds)

- URL: <https://docs.yoctoproject.org/6.1/test-manual/reproducible-builds.html>
- Version: 6.1 docs. Licence: CC BY-SA 2.0 UK. How read: original.
- Says:
  1. Definition: the same input configuration gives the same binary output regardless of when it is built, the path it
     is built in, or the host distribution.
  2. The project advises making sure the project builds reproducibly before finalising production images, because
     security fixes later should change only the modified components.
  3. Mechanisms: `DEBUG_PREFIX_MAP` mapping, explicit dependencies and `PACKAGECONFIG` so no host dependency is
     auto-detected, per recipe sysroots, images built from a reduced package set, and `HOSTTOOLS` filtering of PATH.
  4. Only BitBake and OE-Core are guaranteed. Adding another layer voids the guarantee (page text).
  5. Test your layers with `oe-selftest -r reproducible.ReproducibleTests.test_reproducible_builds`; limit targets with
     `OEQA_REPRODUCIBLE_TEST_TARGET`.
- Staleness note: the page still says "At the time of writing (release 3.3, hardknott), OE-Core is 100% reproducible...
  apart from the Go language and Ruby documentation packages". Treat that status as old; the live status is at
  <https://www.yoctoproject.org/reproducible-build-results/> (not read).

### 1.10 Yocto Project Development Tasks Manual, other pages used lightly

- `dev-manual/init-manager.html` (6.1): Says that to use systemd-journald as the only logger you set
  `VIRTUAL-RUNTIME_syslog = ""` and `VIRTUAL-RUNTIME_base-utils-syslog = ""` in the distro configuration. Says nothing
  about journald storage settings or flash wear.
- `dev-manual/layers.html` section 3.2 "Following Best Practices When Creating Layers" (6.1): use `.bbappend` rather
  than copying whole recipes; reference includes by path relative to the layer root; scope changes with machine
  overrides such as `DEPENDS:one = "foo"` so one machine's layer does not leak into others.
- Both: original, CC BY-SA 2.0 UK.

## 2. Buildroot

Current releases on the read date (Says, <https://buildroot.org/download.html>): stable 2026.08.x (latest 2026.08.2,
2026-10-22, end of life December 2026); long-term support 2025.02.x (latest 2025.02.20, end of life March 2028); release
candidate 2026.11-rc2 on 2026-11-23. Source repository: <https://github.com/buildroot/buildroot> (tag `2026.08.2`; GitHub
reports no standard licence string, the project ships GPL-2.0 text in `COPYING`).

### 2.1 The Buildroot user manual

- URL: <https://buildroot.org/downloads/manual/manual.html>
- Version: "Buildroot 2026.08 manual generated on 2026-09-04 15:28:27 UTC from git revision d5180309b1" (Says, manual
  footer). Licence: "licensed under the GNU General Public License, version 2" (Says, manual preface).
- How read: original, fetched as HTML and converted to text.
- Recommendations and facts (Says):
  01. Chapter 18 "Adding new packages": a `.mk` file for a hand written Makefile builds with
      `$(MAKE) $(TARGET_CONFIGURE_OPTS) -C $(@D) all`. Action macros may use `$(TARGET_CC)`, `$(TARGET_LD)`,
      `$(TARGET_CROSS)`, `$(STAGING_DIR)`, `$(TARGET_DIR)` and `$(HOST_DIR)`.
  02. Section 18.16 "Meson-based packages": `FOO_CFLAGS`, `FOO_CXXFLAGS` and `FOO_LDFLAGS` default to `TARGET_CFLAGS`,
      `TARGET_CXXFLAGS` and `TARGET_LDFLAGS`. The manual has no dedicated "hardening" chapter; hardening is a set of
      configuration options (2.2).
  03. Chapter 12 "Known issues": extra linker options in `BR2_TARGET_LDFLAGS` cannot contain a `$` sign, for example
      `-Wl,-rpath='$ORIGIN/../lib'` breaks.
  04. Section 8.8 and 8.9: `make show-info` emits JSON with packages, dependencies and licences; `make pkg-stats` writes
      HTML and JSON that flag known CVEs and newer upstream versions; `make show-info | utils/generate-cyclonedx`
      produces a CycloneDX SBOM, which `support/scripts/cve-check --nvd-path dl/buildroot-nvd/` can enrich with NVD data.
  05. Section 13.1 "Complying with open source licenses": `make legal-info` collects, under `output/legal-info/`, a
      README with warnings, `buildroot.config`, source and patches (`sources/`, `host-sources/`), manifests for host and
      target packages, and licence texts. The page warns that the output rests on declarative statements in package
      recipes, that toolchain sources for some external toolchains and Buildroot itself are not produced, and that the
      user or their legal office must check it. `<PKG>_REDISTRIBUTE = NO` keeps a package's source out.
  06. Section 18.4 and chapter 9: hash files (`.hash`) pin download and licence file hashes; licence hashes are checked
      during `make legal-info` so a licence change is caught on a version bump. `BR2_GLOBAL_PATCH_DIR` is the preferred
      way to carry project patches.
  07. Chapter 9 "Project-specific customization": keep customisations outside the Buildroot tree with `BR2_EXTERNAL`, use
      root filesystem overlays and post-build scripts (these do not force a full rebuild, section 8.2), and keep the
      configuration as a defconfig.
  08. Section 8.13 and the Kconfig help for `BR2_PER_PACKAGE_DIRECTORIES`: per-package directories isolate each package
      so it sees only its declared dependencies, and enable top-level parallel build; the option is labelled
      experimental.
  09. Section 11.9 "How does Buildroot support Y2038?": 64-bit architectures have 64-bit `time_t`; musl always has it on
      32-bit; uClibc-ng has it since 1.0.46 (default since 1.0.49); with glibc on 32-bit you must enable
      `BR2_TIME_BITS_64`. The page warns that individual libraries and applications can still misuse the time APIs.
  10. Section on debugging (line about `gdb`): binaries under `output/target` are stripped, so debug from the build
      directory where symbols exist.

### 2.2 Buildroot top level `Config.in` (security hardening and reproducibility options)

- URL: <https://github.com/buildroot/buildroot/blob/2026.08.2/Config.in>
- Version: tag 2026.08.2. Licence: GPL-2.0 per `COPYING` (no per-file licence in this file). How read: original, fetched
  through the GitHub API.
- Says (help texts):
  1. "Security Hardening Options": `BR2_PIC_PIE` (default y where supported, needs shared libraries and a PIE capable
     toolchain); a Stack Smashing Protection choice (`BR2_SSP_NONE`, `BR2_SSP_REGULAR` is `-fstack-protector`,
     `BR2_SSP_STRONG` is `-fstack-protector-strong` and is the default when the toolchain supports it, `BR2_SSP_ALL` is
     `-fstack-protector-all` with a noted performance cost); `BR2_RELRO_NONE`, `BR2_RELRO_PARTIAL`, `BR2_RELRO_FULL`
     (default full when PIE is supported; full also makes the GOT read-only at the cost of start-up time and selects
     PIE); Fortify Source choice `BR2_FORTIFY_SOURCE_1` (default, conservative, compile-time checks only), `_2`
     (aggressive, adds run-time checks), `_3` (extended, needs GCC 12 or newer, extra overhead). Fortify needs glibc and
     an optimisation level above `-O0`.
  2. `BR2_REPRODUCIBLE` ("experimental"): removes known sources of non-reproducibility so that, for a given
     configuration, builds give identical binaries "including on different machines", but only with the same output
     directory (`O=...` path), because absolute paths leak into intermediate files and possibly the target root
     filesystem.
  3. `BR2_TIME_BITS_64` ("Build Y2038-ready code"): passes `-D_TIME_BITS=64`; glibc 2.34 or newer and a 32-bit
     architecture only.
  4. `BR2_ENABLE_DEBUG`, `BR2_STRIP_strip`, `BR2_STRIP_EXCLUDE_FILES` and `BR2_OPTIMIZE_*` control debug info, stripping
     and optimisation.

### 2.3 How Buildroot passes flags: `package/Makefile.in` and `toolchain/toolchain-wrapper.mk`

- URLs: <https://github.com/buildroot/buildroot/blob/2026.08.2/package/Makefile.in> and <https://github.com/buildroot/buildroot/blob/2026.08.2/toolchain/toolchain-wrapper.mk>
- Version: tag 2026.08.2. Licence: GPL-2.0 per `COPYING`. How read: original.
- Says (code):
  1. `TARGET_CFLAGS = $(TARGET_CPPFLAGS) $(TARGET_ABI) $(TARGET_OPTIMIZATION) $(TARGET_DEBUGGING) $(TARGET_HARDENED)`;
     `TARGET_CXXFLAGS = $(TARGET_CFLAGS)`. `TARGET_CPPFLAGS` carries
     `-D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64`, and `-D_TIME_BITS=64` when enabled.
     `TARGET_HARDENED` carries `-D_FORTIFY_SOURCE=1|2|3`.
  2. `TARGET_CONFIGURE_OPTS` exports `CC`, `CXX`, `CPPFLAGS`, `CFLAGS`, `CXXFLAGS` and `LDFLAGS`, so
     `$(MAKE) $(TARGET_CONFIGURE_OPTS)` passes all of them to a hand written Makefile.
  3. Stack protector, PIE and RELRO do not travel in CFLAGS. The toolchain wrapper adds them (`BR2_SSP_OPTION` in
     `TOOLCHAIN_WRAPPER_OPTS`; `-DBR2_PIC_PIE`, `-DBR2_RELRO_PARTIAL` and `-DBR2_RELRO_FULL` as wrapper arguments). With
     `BR2_REPRODUCIBLE` the wrapper adds `-Wl,--build-id=none` and `-ffile-prefix-map=$(BASE_DIR)=buildroot`.
- Inference: Buildroot hardening reaches every compile that goes through the wrapper even when a package ignores CFLAGS,
  but `_FORTIFY_SOURCE` reaches only builds that use `TARGET_CFLAGS` or `TARGET_CPPFLAGS`. This is the opposite split
  from Yocto, where everything rides on `TARGET_CC_ARCH` (1.7). Both split designs mean "use the provided `CC`,
  `CFLAGS`, `CXXFLAGS`, `LDFLAGS` and never hardcode `gcc`" is the rule that serves both.

## 3. Training and conference material, Linux Foundation and OpenSSF guidance

### 3.1 Bootlin training materials (embedded Linux, Yocto, Buildroot, security)

- URL: <https://github.com/bootlin/training-materials> (slides under `slides/<topic>/`, now Typst sources). The rendered
  site <https://bootlin.com/doc/training/> returned "403 Forbidden" to my fetch, so I read the sources, not the PDFs.
- Version: master commit 442a80f0 (2026-11-13). The slides cite Linux 6.19 and Linux 6.18.
- Licence: "Creative Commons Attribution-ShareAlike 3.0 Unported" (Says, `LICENSE` in the repository; the ELCE 2026
  Bootlin slides also state "Creative Commons BY-SA 3.0 license" on the title slide).
- How read: original (raw slide sources through the GitHub API): `sysdev-block-filesystems`, `sysdev-flash-filesystems`,
  `security-ab-updates`, `security-userland`, `security-secure-boot-part-2`, `security-compliance`,
  `sysdev-cross-compiling-user-space`, `yocto-recipe-basics`, `yocto-ota-updates`. Not read: the other 250 or so slide
  folders (for example boot-time, debugging, buildroot-\*, yocto-licensing).
- Recommendations (Says):
  01. Cross compiling hand written Makefiles (`sysdev-cross-compiling-user-space`): use the standard variables `CC`,
      `CXX`, `LD`, `CFLAGS`, `CXXFLAGS`, `LDFLAGS`, `DESTDIR`, `PREFIX`; read the Makefile because there is "no general
      rule". For autotools, `--host` is the target machine and also the cross compiler prefix. Use `pkg-config` with
      `PKG_CONFIG_SYSROOT_DIR` when cross compiling.
  02. Yocto patching slide (`yocto-recipe-basics`): when an upstream Makefile hardcodes `CC` or `CFLAGS`, patching is
      unnecessary; call make with `-e` so environment variables take precedence, by setting `EXTRA_OEMAKE = "-e"`.
      Inference: `make -e` also lets environment values override flags the Makefile needs for itself (include paths,
      defines), so test the result.
  03. Filesystem choice (`sysdev-block-filesystems`): ext2 is "not recommended for embedded systems today"; use a
      journaled filesystem so recovery after power loss is quick; "a good default choice is ext4 for read/write
      partitions" if you have not benchmarked; F2FS is designed for eMMC, SD and SSD and has a 52 MiB minimum partition
      size; SquashFS and EROFS suit read-only root filesystems; Btrfs has a big module size and long initialisation. The
      slide says to benchmark your own workload.
  04. Same slide, "Mixing read-only and read-write filesystems": split storage into a compressed read-only root
      (SquashFS), a read-write journaled partition (ext4) for user and configuration data, and tmpfs for temporary files.
      tmpfs is suggested for "system log files, connection data, temporary files".
  05. Same slide, "Issues with flash-based block storage": for SD and eMMC the flash translation layer is a trade secret,
      so "it is highly recommended to limit the number of writes"; use industrial grade storage.
  06. Raw flash (`sysdev-flash-filesystems`): NAND needs ECC, bad block handling and wear levelling; erase endurance is
      quoted as between 1,000,000 (SLC) and 1,000 (MLC) cycles. UBI/UBIFS is "the de facto standard for medium to large
      capacity NANDs"; JFFS2 still makes sense on small partitions. UBI good practice: give UBI as much of the device as
      possible so wear levelling covers more blocks, use UBI volumes instead of MTD partitions, and do not write to
      `mtdblock` devices because bad blocks are not handled.
  07. A/B updates (`security-ab-updates`): keep two slots; never touch the current slot's boot locations; write to the
      alternate slot; mark it "next"; if boot fails several times the bootloader falls back; if boot succeeds and checks
      pass, mark the slot primary. A watchdog reboots a system that fails to boot. Tools named: SWUpdate, RAUC (with
      hawkBit as rollout back end). With RAUC and U-Boot, protect the U-Boot environment with `CONFIG_ENV_WRITEABLE_LIST`
      when using secure boot. `yocto-ota-updates` repeats this and characterises SWUpdate as "DIY approach, very
      flexible", Mender as "fully integrated, requires systemd", RAUC as "good middleground".
  08. Userland security (`security-userland`): threads should "only hold the capabilities that they absolutely require"
      and make them effective only while needed; use the bounding set to ensure children never gain a capability; systemd
      sandboxing: "A good practice is to enable as much as possible of these options" from `systemd.exec(5)`; options
      listed: `CapabilityBoundingSet=`, `AmbientCapabilities=`, `NoNewPrivileges=`, `SystemCallFilter=` (with groups such
      as `@basic-io`), `PrivateTmp=`, `ProtectSystem=`, `DeviceAllow=`, resource control (`MemoryMax=`, `TasksMax=`,
      `CPUQuota=`).
  09. Secure boot, later stages (`security-secure-boot-part-2`): verify the root filesystem with dm-verity; the root hash
      must be signed or protected, either with the kernel (`CONFIG_DM_VERITY_VERIFY_ROOTHASH_SIG`) or from a signed
      initramfs; if the initramfs sets up verity, the kernel command line becomes security sensitive and must be covered
      by the signature; the slides say the FIT spec has a `cmdline` property that "is not implemented in U-Boot", so use
      a signed U-Boot script that sets `bootargs`.
  10. Compliance (`security-compliance`): CRA dates and the support period (checked against the law in 5.1); SBOM
      standards are CycloneDX (ECMA-424) and SPDX (ISO standard, 2.3 current, 3.0 tooling trailing); no law imposes a
      format; the Linux kernel became a CNA in 2024; NVD and the CVE programme had funding problems in 2025, and the EU
      started EUVD in 2025.

### 3.2 Bootlin, "Yocto BSP layers: Breaking free from complexity" (ELCE 2026, Prague)

- URL: <https://elinux.org/images/7/72/Yocto-bsp-layers-breaking-free-from-complexity.pdf>, listed at <https://www.yoctoproject.org/blog/2026/11/18/yocto-presentations-at-embedded-linux-conference-2026-in-prague/>
- Version: Embedded Linux Conference Europe, October 2026, 39 slides; examples target the wrynose release. Licence:
  "Creative Commons BY-SA 3.0 license" (Says, title slide). How read: original, first 12 slides closely, rest skimmed.
- Says: a BSP layer should hold hardware support only, "No generic software, No DISTRO configuration, No unnecessary
  added constraints". Common vendor layer problems are unrelated recipes, configuration that affects all builds,
  modified core concepts, vendored copies of upstream recipes, and many machines in one layer. The proposed approach is
  "think simple stupid", your own small layers, with `yocto-kiss` (<https://github.com/bootlin/yocto-kiss>) as the
  example.
- Relevance (inference): supports the Yocto layer guidance in 1.10, and a rule that application recipes stay out of BSP
  layers.

### 3.3 OpenSSF, "Compiler Options Hardening Guide for C and C++"

- URL: <https://best.openssf.org/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++> ; source <https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.md>
- Version: page header date 2026-08-20; repository head commit 816cacb7 (2026-11-21) at read time. Licence: "Copyright
  2024, OpenSSF contributors, licensed under CC BY 4.0" (Says, "License" section).
- How read: original (212 KB Markdown, TL;DR, option sections, rpath section, debug info section read; other option
  sections skimmed).
- Recommendations (Says):
  1. Baseline flags "in all cases":

     ```text
     -O2 -Wall -Wformat -Wformat=2 -Wconversion -Wimplicit-fallthrough -Werror=format-security
     -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=3 -D_GLIBCXX_ASSERTIONS
     -D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_FAST -fstrict-flex-arrays=3
     -fstack-clash-protection -fstack-protector-strong -Wl,-z,nodlopen -Wl,-z,noexecstack
     -Wl,-z,relro -Wl,-z,now -Wl,--as-needed -Wl,--no-copy-dt-needed-entries
     ```

  2. Add `-fPIE -pie` for executables, `-fPIC -shared` for shared libraries;
     `-fcf-protection=full -fzero-call-used-regs=used-gpr` on x86_64;
     `-mbranch-protection=standard -fzero-call-used-regs=used-gpr` on aarch64; with GCC add
     `-Wtrampolines -fzero-init-padding-bits=all`.

  3. For production code add
     `-fno-delete-null-pointer-checks -fno-strict-overflow -fno-strict-aliasing -ftrivial-auto-var-init=zero`. For
     multi-threaded C on glibc pthreads add `-fexceptions`. For C, make obsolete constructs errors with
     `-Werror=implicit -Werror=incompatible-pointer-types -Werror=int-conversion`.

  4. Use a blanket `-Werror` during development only. When distributing source, use selective `-Werror=<flag>`, because
     a blanket `-Werror` ties the build to compiler vendors and versions.

  5. Treat a program that cannot build with these options as a bug. Test with both production flags and instrumented
     test builds. Sanitizer sections cover AddressSanitizer, ThreadSanitizer, LeakSanitizer and
     UndefinedBehaviorSanitizer for test builds.

  6. Discouraged: hard coded `-Wl,-rpath` in release binaries, because an attacker who controls the target directory (or
     `$ORIGIN` through hard links) can substitute libraries, and setuid programs are exposed.

  7. Ship stripped binaries and keep separate debug files: `objcopy --only-keep-debug`, `objcopy --strip-unneeded`,
     `objcopy --add-gnu-debuglink`. The guide adds that security must not depend on hiding symbols.

  8. Hardening may be omitted where it costs performance only if the program processes trusted data only; the guide says
     to decide that explicitly.
- Note (Says, "Background"): the guide targets "native (or cross) toolchains", GCC and Clang. Support for individual
  flags differs by compiler, C library and architecture.

### 3.4 OpenSSF, "Concise Guide for Developing More Secure Software" and "CRA Brief Guide for OSS Developers"

- URLs: <https://best.openssf.org/Concise-Guide-for-Developing-More-Secure-Software> and
  <https://best.openssf.org/CRA-Brief-Guide-for-OSS-Developers> ; sources in `docs/` of the same repository (head commit
  816cacb7, 2026-11-21).
- Version: the Concise Guide header is dated 2023-06-14 and the file was current in the repository on the read date; the
  CRA brief guide carries no date. Licence: the files state none; the repository README says documentation is released
  under CC-BY-4.0 (Says, README section "Licenses"). How read: original.
- Recommendations (Says, Concise Guide, 20 numbered items): use package managers; write automated tests including
  negative tests; monitor vulnerabilities in direct and indirect dependencies; apply a roughly 3 day cooldown before
  adopting new dependency releases; do not push secrets; require review; document how to report vulnerabilities; sign
  releases; publish and consume an SBOM (SPDX or CycloneDX); point to the compiler hardening guide for C and C++.
- Says (CRA brief guide): the CRA applies when a product is placed on the market in the course of a commercial activity,
  so a manufacturer who integrates open source components is responsible for them. The guide says it is not legal
  advice.
- Inference: both are generic, not embedded specific. Use them for the process rules, and use 3.3 for the flags.

### 3.5 Embedded Linux Conference Europe 2026 and Open Source Summit talks (read as slide decks)

All are slide PDFs hosted on elinux.org or sched.co. Slide decks usually carry the speaker's licence, so each entry
states what the first slide says. List of all 19 Yocto talks of ELCE 2026:
<https://www.yoctoproject.org/blog/2026/11/18/yocto-presentations-at-embedded-linux-conference-2026-in-prague/> (blog by
Michael Opdenacker, 2026-11-18; I read the list only).

1. "A/B Updates and Secure Boot", Michael Opdenacker (Root Commit), ELCE 2026, 2026-10-08.
   <https://elinux.org/images/d/db/A-b-updates-and-secure-boot.pdf> . Licence: CC BY-SA 4.0 (Says, title slide and last
   slide). How read: original, whole deck.
   - Says: standard A/B implementations can make a system more attackable. Let U-Boot do the bookkeeping:
     `CONFIG_BOOTCOUNT_LIMIT`, `bootlimit`, `altbootcmd` and `upgrade_available` work automatically ("No need to
     implement your own scripts"). Lock the U-Boot environment with `CONFIG_ENV_WRITEABLE_LIST=y` and a list such as
     `bootlimit:dr,bootcmd:sr,altbootcmd:sr,bootcount:dw,bootpart:dw,upgrade_available:dw`; variables are read-only
     unless listed as writable. Do not install `fw_setenv` in the image; use libbootenv from the updater
     (`CONFIG_UPDATE_STATE_BOOTLOADER`) so an attacker has a harder time. Hard code `bootargs` in `bootcmd` and keep
     flexibility with an embedded kernel `bootconfig` (`CONFIG_BOOT_CONFIG_EMBED`). Block the U-Boot shell with
     `CONFIG_DISABLE_CONSOLE=y`, because failing scripts can drop to a shell. A rollback attack through an invalid
     `bootpart` is possible and needs protection. "Design note: watchdog not necessary", because this customer chose to
     rely on the user to reboot; the classic documentation suggests a watchdog.
2. "Secure by Default: Building Locked-Down Embedded Linux Devices With systemd", Mohammad Abdoli (SEGULA Technologies),
   ELCE 2026.
   <https://elinux.org/images/e/e7/Mominux_Secure_by_Default_Building_Locked-Down_Embedded_Linux_Devices_with_systemd.pdf>
   . Licence: "(c) SEGULA Technologies, all rights reserved" (Says, slide footer); treat as not reusable. How read:
   original, most slides.
   - Says: start from each service's real requirements (too strict breaks the service, too loose leaves access); contain
     resources as well as access (`CPUQuota=`, `MemoryMax=`, `TasksMax=`) because a compromised or buggy service can
     exhaust the device (example CVE-2023-5632 in Mosquitto); network access is a privilege (`IPAddressDeny=` and
     `IPAddressAllow=`); portable services with signed dm-verity images; the platform build must provide kernel features
     and fail closed when keys or certificates are missing. Takeaway: "Configured is not enforced is not demonstrated",
     so prove enforcement. Reference build: Yocto scarthgap 5.0.19, systemd 255.21, linux-yocto 6.6.
3. "Complying with CRA SBoM Requirements using the Yocto Project", Joshua Watt (Garmin), Open Source Summit.
   <https://elinux.org/images/b/b2/OSS-NA_Complying_with_CRA_SBoM_Requirements_using_the_Yocto_Project.pdf> . Licence:
   "Creative Commons BY-SA 4.0 International License" (Says, title slide; slide date reads "May 18, 2026" with
   "Copyright 2025", so the date is not reliable). How read: original, selected slides.
   - Says: Yocto SPDX 3.0 output (Yocto 5.1 and later) covers the NTIA minimum elements (10 provided, 4 with
     configuration) and most of the CISA framing and BSI TR-03183 fields. You must set the SBOM creator (`SPDX_AUTHORS`)
     and package supplier (`SPDX_PACKAGE_SUPPLIER`); `SPDX_INCLUDE_TIMESTAMPS = "1"` makes SBOMs non reproducible; PURLs
     are set automatically for recipe types such as cargo, npm, pypi, golang, cpan. Yocto SBOMs list runtime packages
     and their runtime dependencies, which "may be sufficient" for a self contained device, but binaries or code outside
     recipes are not covered. The speaker says the primary CRA text holds the only actual requirements: standard format,
     top level dependencies, use for vulnerability scanning, and "I am not a lawyer".
4. "The Engineer's Guide to the Embedded Linux Galaxy: Navigating Failures and Bricked Devices", Leon Anavi and Piotr
   Bulinski, ELCE 2026. <https://elinux.org/images/4/48/Leon_and_Piotr_ELC_2026_-_Prague.pdf> . Licence: no licence stated
   on the slides I read. How read: skimmed (59 slides, text extraction only).
   - Says (selected): an OTA update with no rollback is a failure mode; tolerate power loss, network interruption and
     corrupted downloads; support rollback to the last known good image; full A/B image is "simple and robust";
     processes and documentation decay unless you can rebuild and operate the system at any time.
5. Not read, found as titles or search snippets only: "Updates on sbom-cve-check" (Bootlin, ELCE 2026), "Securing
   Embedded Linux Buildsystems Against Supply Chain Attacks" (Microsoft), "SELinux in Embedded Linux" (BMW Car IT),
   "Triaging CVEs for the Linux Kernel" (Siemens), "State of Embedded Linux" (Linux Foundation,
   <https://elinux.org/images/4/48/ELC_EU_2026_State_of_Embedded_Linux.pdf>), "The State of SBoMs in Embedded" (OSS NA
   2025, downloaded, not read), "Fighting CVEs in Embedded Linux with the Yocto Project and OTA Updates" (Torizon CRA
   Summit 2025, search snippet), "Debian and Yocto Project based Long-term Maintenance Approaches for Embedded Products"
   (ELCE 2019 PDF, search snippet), "meta-cra-compatible" (OpenEmbedded Workshop 2025, search snippet).

## 4. Device-side robustness for embedded Linux userspace

### 4.1 Writing to flash safely and limiting wear

Sources already above carry most of this: Bootlin flash and block filesystem slides (3.1 items 3 to 6), Yocto read-only
rootfs and `overlayfs-etc` (1.5 item 8). Additional primary sources:

#### 4.1.1 Linux kernel documentation: ext4, F2FS, UBIFS, tmpfs

- URLs: <https://docs.kernel.org/admin-guide/ext4.html> , <https://docs.kernel.org/filesystems/f2fs.html> , <https://docs.kernel.org/filesystems/ubifs.html>
- Version: the rendered pages show no kernel version; read 2026-11-23 from the current documentation tree. The ext4 page
  says `data=journal` is deprecated with removal in January 2028. Licence: no licence stated on the pages (kernel
  documentation ships with the GPL-2.0 kernel sources).
- How read: original, key option passages only.
- Recommendations and facts (Says):
  1. ext4 `commit=nrsec`: default 5 seconds; "if you lose your power, you will lose as much as the latest 5 seconds of
     metadata changes (your filesystem will not be damaged though, thanks to the journaling)". Low values hurt
     performance but help data safety.
  2. ext4 `data=ordered` is the default: data is forced to the main filesystem before its metadata is committed to the journal.
  3. ext4 `auto_da_alloc` (default): the kernel detects the replace-via-rename and replace-via-truncate patterns and
     forces the new file's data blocks out before the rename commits. The page calls applications that rely on this
     "broken" because they do not call `fsync()`. Inference: an application that wants a safe atomic replace on any
     filesystem must still write a temp file, `fsync()` it, `rename()` it, then `fsync()` the directory (see 4.1.2), and
     must not rely on this ext4 mitigation.
  4. F2FS is log structured and checkpoint based. Mount options relevant to robustness:
     `fsync_mode=posix|strict|nobarrier`, `nobarrier` only when the device guarantees its cache is non-volatile,
     `discard`, `checkpoint=disable|enable`, `data_flush`, `fastboot` (reduces mount time at some performance cost).
  5. UBIFS "is tolerant of unclean reboots and power-cuts. It does not need stuff like fsck.ext2", replays its journal,
     and supports write-back (JFFS2 is write-through). Inference: write-back means unsynced data can be lost on power
     loss, so fsync discipline still applies.

#### 4.1.2 Linux man-pages: fsync(2), rename(2)

- URLs: <https://man7.org/linux/man-pages/man2/fsync.2.html> , <https://man7.org/linux/man-pages/man2/rename.2.html>
- Version: Linux man-pages 6.19, page dated 2026-02-08 (Says, page footer; HTML rendered 2026-09-09). Licence: man-pages
  are under mixed free licences; the page shows a COLOPHON but I did not extract a licence line, so "no licence stated"
  in what I read.
- How read: original.
- Says: `fsync()` flushes file data and metadata to the storage device. It "does not necessarily ensure that the entry
  in the directory containing the file has also reached disk. For that an explicit `fsync()` on a file descriptor for
  the directory is also needed." `rename()` replaces `newpath` atomically, so no process sees it missing; the page does
  not claim crash durability of the rename.
- Inference: the safe pattern for configuration is write temp file in the same directory, `fsync(file)`, `rename()`, `fsync(directory)`.

### 4.2 Wall clock without a time server, and monotonic time

#### 4.2.1 clock_gettime(2) and systemd-timesyncd.service(8)

- URLs: <https://man7.org/linux/man-pages/man2/clock_gettime.2.html> (man-pages 6.19) and
  <https://www.freedesktop.org/software/systemd/man/latest/systemd-timesyncd.service.html> (systemd 262, page header
  "systemd 262").
- Licence: man-pages as above. systemd manual sources carry `SPDX-License-Identifier: LGPL-2.1-or-later` in the XML
  source (Says, `man/journald.conf.xml` in <https://github.com/systemd/systemd>; the rendered HTML states none). systemd
  latest release on read date: v262.2 (2026-11-05).
- How read: original.
- Says:
  1. `CLOCK_MONOTONIC` "is not affected by discontinuous jumps in the system time (e.g., if the system administrator
     manually changes the clock), but is affected by frequency adjustments", does not count suspend time, never goes
     backwards. Its start point is unspecified (on Linux, since boot).
  2. systemd-timesyncd "saves the local time to disk every time the clock has been synchronized and uses this to
     possibly advance the system realtime clock on subsequent reboots to ensure it (roughly) monotonically advances even
     if the system lacks a battery-buffered RTC chip". It does this through the mtime of
     `/var/lib/systemd/timesync/clock` (updated on each sync or every `SaveIntervalSec=`). systemd also advances the
     clock to an "epoch" (lowest date assumed correct).
  3. Units ordered after `time-set.target` wait until that time is restored; only `time-sync.target` (via
     `systemd-time-wait-sync.service`) means an accurate reference time.
- Inference for userland C and C++: use `CLOCK_MONOTONIC` for timeouts, intervals and rate limiting; use wall clock only
  for timestamps shown to humans or stored in data; treat wall clock before first sync as untrusted; do not set
  certificate or licence validity from a clock that may not be set (RAUC says the same, 4.4).

#### 4.2.2 Y2038 and 32-bit time

- Buildroot manual 11.9 and `BR2_TIME_BITS_64` (2.1 item 9, 2.2 item 3); Yocto `32bit-time` QA check: Says
  (insane.bbclass at blacksail): for ARM, ARMEB, MIPS o32, PowerPC and x86 targets, the check warns when an ELF file
  uses 32-bit time APIs from glibc; suppress with `INSANE_SKIP = "32bit-time"`. It is in `WARN_QA` by default, not
  `ERROR_QA`.

### 4.3 Watchdogs

#### 4.3.1 systemd: systemd.service(5), systemd-system.conf(5), sd_watchdog_enabled(3)

- URLs: <https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html> , `/systemd-system.conf.html` ,
  `/sd_watchdog_enabled.html`. Version: systemd 262. Licence: see 4.2.1. How read: original.
- Says:
  1. `WatchdogSec=`: the service must call `sd_notify()` with `WATCHDOG=1` within the interval; otherwise it fails and
     is terminated with SIGABRT. Pair it with `Restart=on-failure` (or `on-watchdog`, `always`). The timeout is passed
     in `WATCHDOG_USEC=`.
  2. `sd_watchdog_enabled(3)`: daemons should ping about every half of the returned timeout.
  3. `RuntimeWatchdogSec=` makes PID 1 program and ping the hardware watchdog (`/dev/watchdog0`) and ping at least once
     in half the timeout. Default is off (0). `RebootWatchdogSec=` defaults to 10 minutes and covers a hung shutdown. A
     hardware watchdog device is required.
  4. RAUC documentation recommends `RuntimeWatchdogSec=20` and `ShutdownWatchdogSec=10min` for update systems (see 4.4).

#### 4.3.2 Linux kernel watchdog API

- URL: <https://docs.kernel.org/watchdog/watchdog-api.html> . Version: current docs tree on 2026-11-23, no version shown.
  Licence: no licence stated on page. How read: original, key passages.
- Says: the watchdog starts when `/dev/watchdog` is opened and reboots the system unless pinged within the timeout;
  closing the device disables the watchdog unless the driver supports "Magic Close" (write `V` before closing). Pinging
  by `write()` or `WDIOC_KEEPALIVE`. The page warns that disabling on close is "not always such a good idea" because a
  crashed daemon then leaves the machine unwatched. A smarter daemon can check that services still respond before it
  pings.

### 4.4 A/B updates, RAUC, SWUpdate, Mender

#### 4.4.1 RAUC documentation

- URLs: <https://rauc.readthedocs.io/en/latest/checklist.html> (Design Checklist) and <https://rauc.readthedocs.io/en/latest/integration.html>
- Version: "latest" docs; latest release on the read date is v1.15.2 (2026-03-27, <https://github.com/rauc/rauc>).
  Licence: code LGPL-2.1 (GitHub); the doc pages state no licence.
- How read: original.
- Recommendations (Says):
  1. Checklist: bundles use the `verity` format, and `plain` is disabled in `system.conf`; separate development and
     release keys; test key revocation and rollover; factory image includes all slots; define the bootloader behaviour
     when one slot or all slots fail to boot; identify single points of failure.
  2. Checklist, time: "Systems always have correct time, or validity period is large enough". Inference: a device with
     no battery RTC and no time server can fail certificate validation, so pick validity periods and check time
     handling.
  3. Checklist, watchdog path: never disable the watchdog before the application is ready; the bootloader distinguishes
     watchdog resets from normal boot and enables the watchdog before starting the kernel; the reset reinitialises the
     whole system; all essential services are monitored. Without a hardware watchdog: the bootloader counts failed
     boots, resets the counter on success, and all essential services must work before the boot is confirmed.
  4. Integration page: mark the slot good only after the system is fully started, through a systemd service that runs
     `rauc status mark-good` (the Yocto recipes ship `rauc-mark-good.service`). Configure `RuntimeWatchdogSec=20` and
     `ShutdownWatchdogSec=10min`. Prefer to have the bootloader tell RAUC the booted slot explicitly. barebox
     bootchooser is recommended when the choice is open; U-Boot is natively supported.
  5. Checklist, data migration: keep passwords and SSH keys, and handle shared data across upgrades and downgrades.

#### 4.4.2 SWUpdate documentation

- URL: <https://sbabic.github.io/swupdate/swupdate.html> . Version: latest release 2026.05.2 (2026-11-20,
  <https://github.com/sbabic/swupdate>); docs page itself shows no version. Licence: code GPL-2.0 (GitHub); docs no
  licence stated. How read: original, targeted reads.
- Says: "Power-Off safe" is listed as a feature; SWUpdate runs in a single copy approach from an initramfs, or in a
  double copy approach with software collections; signed images (`sw-description.sig`) are verified before use; a failed
  step stops the update; `--cache-file` allows resuming after a power cut; U-Boot should be built with two environment
  copies so that updating the environment is power-off safe; GRUB has no redundant environment, so environment
  corruption is possible on power loss.

#### 4.4.3 Mender, "How Mender works"

- URL: <https://mender.io/engineers/how-mender-works> . Version: web page, undated; Mender client latest release 5.2.0
  (2026-10-23, <https://github.com/mendersoftware/mender>). Licence: page states "Mender is an open-core Apache
  2.0-licensed solution"; the page itself carries no content licence. How read: original, vendor marketing page, treat
  as a description of intent, not a specification.
- Says: OS updates require a dual A/B rootfs layout; the client writes the inactive partition, sets it to boot, reboots;
  if boot succeeds it commits the partition permanently, otherwise the bootloader returns to the old one; a persistent
  data partition is left unchanged by updates; downtime is the reboot (about 60 seconds).

### 4.5 Logging on flash: systemd journald

- URL: <https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html> . Version: systemd 262 (v262.2,
  2026-11-05). Licence: LGPL-2.1-or-later in the XML source (see 4.2.1). How read: original.
- Says:
  1. `Storage=` is `volatile` (RAM, `/run/log/journal`), `persistent` (`/var/log/journal`, falls back to
     `/run/log/journal` early in boot or if the disk is not writable), `auto` (persistent only if `/var/log/journal`
     exists) or `none`. journald starts volatile and `systemd-journal-flush.service` moves data to persistent storage
     after boot.
  2. Size limits: `SystemMaxUse=`, `SystemKeepFree=`, `SystemMaxFileSize=`, `SystemMaxFiles=` (default 100) apply to
     persistent storage; the `Runtime*` set applies to RAM. `MaxUse` defaults to 10% and `KeepFree` to 15% of the
     respective filesystem, each capped at 4G, and journald honours the smaller resulting limit. Only archived files are
     deleted, so usage can exceed `SystemMaxUse=` after vacuuming. `MaxRetentionSec=` defaults to off. `MaxFileSec=`
     defaults to one month.
  3. `SyncIntervalSec=` default 5 minutes; messages of priority CRIT, ALERT or EMERG are synced immediately. So a power
     cut can lose up to five minutes of lower priority logs.
  4. Rate limiting through `RateLimitIntervalSec=` and `RateLimitBurst=`; compression through `Compress=`.
- The page does not mention flash wear. Inference: on SD, eMMC or NAND, use `Storage=volatile` (and `RuntimeMaxUse=`
  sized for RAM), or `Storage=persistent` with a small `SystemMaxUse=` on a partition you can afford to wear, and
  forward only the logs you need off the device. Yocto's init-manager page only says how to drop syslog (1.10).

## 5. Security for embedded Linux products

### 5.1 EU Cyber Resilience Act (high level)

#### 5.1.1 Regulation (EU) 2024/2847, the law itself

- URL: <https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847> (ELI
  <http://data.europa.eu/eli/reg/2024/2847/oj>). The plain fetch returned a challenge page, so I read it through a stealth
  browser fetch.
- Version: signed 23 October 2024, Official Journal 20 November 2024. Terms: EUR-Lex pages carry the Official Journal
  text; no licence line on the page I read (EU legal texts are reusable under Commission reuse rules, not verified
  here).
- How read: original, whole text.
- Says (articles and annexes named):
  1. Dates (Art. 71): applies from 11 December 2027; Article 14 reporting obligations apply from 11 September 2026;
     Chapter IV on notified bodies from 11 June 2026. Products placed on the market before 11 December 2027 are in scope
     only after a substantial modification, but Article 14 reporting applies to them too (Art. 69).
  2. Scope (Art. 2, 3): products with digital elements with a direct or indirect data connection, in the course of a
     commercial activity. The manufacturer is responsible for the whole product including third party and open source
     components (Art. 13(5), (6)).
  3. Annex I Part I (product properties, "where applicable" after the risk assessment): no known exploitable
     vulnerabilities at placing on the market; secure by default configuration with a way to reset to original state;
     security updates, with automatic updates on by default and an opt-out where applicable; access control;
     confidentiality and integrity of data and of "commands, programs and configuration" with reporting of corruption;
     data minimisation; availability and resilience including against denial of service; limit attack surface including
     external interfaces; exploitation mitigations; security logging with opt-out; secure removal of data and settings.
  4. Annex I Part II (vulnerability handling): identify and document vulnerabilities and components, with an SBOM "in a
     commonly used and machine-readable format covering at the very least the top-level dependencies"; fix without
     delay, separately from feature updates where technically feasible; regular security tests; publish information on
     fixed vulnerabilities; coordinated vulnerability disclosure policy and a contact address; secure distribution of
     updates; updates free of charge with advisories.
  5. Support period (Art. 13(8)): at least five years, unless the product is expected to be used for less time; set by
     expected use time. Security updates must stay available for 10 years or the remaining support period, whichever is
     longer (Art. 13(9)). The end date of support must be stated at the time of purchase (Art. 13(19)).
  6. Reporting (Art. 14): actively exploited vulnerabilities and severe incidents go through ENISA's single reporting
     platform: early warning within 24 hours, notification within 72 hours, final report 14 days after a fix is
     available (vulnerabilities) or within one month (incidents).
  7. Technical documentation and declaration of conformity are kept for 10 years or the support period, whichever is
     longer (Art. 13(13)). Fines: up to EUR 15 million or 2.5 percent of worldwide turnover for failing the essential
     requirements (Art. 64(2)).
  8. Conformity assessment (Art. 32): most products use internal control (module A). "Important" products listed in
     Annex III (class I includes boot managers, operating systems, routers, network interfaces and microcontrollers with
     security functions) need a third party unless harmonised standards, common specifications or a certification scheme
     are applied in full; class II (hypervisors and container runtimes, firewalls, tamper-resistant chips) always needs
     a third party.
- Inference for these skills: the Yocto and Buildroot guidance on SBOM, CVE checking, secure by default images, update
  mechanisms, read-only roots and separation of services maps to Annex I, but the law does not name any tool, flag or
  format.

#### 5.1.2 European Commission, "FAQs on the Cyber Resilience Act"

- URL: <https://digital-strategy.ec.europa.eu/en/library/cyber-resilience-act-implementation-frequently-asked-questions>
  (PDF at <https://ec.europa.eu/newsroom/dae/redirection/document/122331>).
- Version: FAQ version 1.4, 4 September 2026 (Says, version table); first published 3 December 2025. Licence: "(c)
  European Union, 2025" and a note that it is prepared by Commission services and not binding (Says); no further licence
  stated.
- How read: original, table of contents, version table, sections 4.4.2 and 4.5.2.
- Says: the Commission "has also adopted guidance pursuant to Article 26". Due diligence for third party components
  scales with risk and may include checking CE marking, security update history, vulnerability databases, software
  composition analysis, sandboxing high risk components, reviewing the component's SBOM and extra tests such as fuzzing.
  The minimum support period restates Art. 13(8): five years, or the expected life if shorter, and longer for operating
  systems and industrial products.

#### 5.1.3 Other CRA sources used

- Bootlin `security-compliance` slides (3.1 item 10): its date line "adopted on October 10 2024" differs from the law
  (signed 23 October 2024; 10 October is the Council decision date, Says, footnote 2 of the regulation). See the
  disagreements list.
- OpenSSF CRA brief guide (3.4) and Watt talk (3.5 item 3).

### 5.2 Yocto Project Security Manual

See 1.5 for the manual itself (read in full except the sstate signing details). Highlights for product practice: remove
debug features and development logins before release; read-only rootfs; update path; CVE tooling with `sbom-cve-check`;
`security_flags.inc`; MAC with SELinux or Smack; hardening layer `meta-security`.

### 5.3 Secure boot and dm-verity

#### 5.3.1 Linux kernel, dm-verity

- URL: <https://docs.kernel.org/admin-guide/device-mapper/verity.html> . Version: current docs tree on 2026-11-23 (no
  version on page). Licence: no licence stated. How read: original, option section.
- Says: a read-only device-mapper target that verifies blocks against a hash tree. On corruption you can choose
  `ignore_corruption` (log only), `restart_on_corruption` (needs user space support to avoid restart loops),
  `panic_on_corruption`, and the matching `restart_on_error` and `panic_on_error` for I/O errors; forward error
  correction is available through `use_fec_from_device`.

#### 5.3.2 U-Boot documentation, "Verified Boot"

- URL: <https://docs.u-boot.org/en/latest/usage/fit/verified-boot.html> . Version: "latest" docs, no version shown.
  Licence: no licence stated on the page (U-Boot is GPL-2.0-or-later). How read: original, introduction.
- Says: verified boot means verifying all software loaded during boot; it can extend as far as you wish, for example
  U-Boot in read-only memory, then a signed kernel, then the kernel's dm-verity for the root filesystem; with it, field
  upgrade is safe because only correctly signed software runs; the public key is stored in the U-Boot control device
  tree and FIT images carry hashes and signatures; multiple keys and a two level key scheme are supported.

#### 5.3.3 Bootlin and ELCE material

- Bootlin `security-secure-boot-part-2` (3.1 item 9) and Opdenacker's talk (3.5 item 1) cover signed root hash, signed
  initramfs, protected kernel command line, locked U-Boot environment and console. The Yocto security manual (1.5
  item 1) only says "enable hardware support for secure boot".

### 5.4 Least privilege for services: systemd hardening

#### 5.4.1 systemd.exec(5) and systemd-analyze(1)

- URLs: <https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html> and `/systemd-analyze.html` . Version:
  systemd 262. Licence: LGPL-2.1-or-later in source (4.2.1). How read: original, option passages for the options below;
  the rest of the sandboxing section was not read line by line.
- Recommendations and facts (Says):
  1. `NoNewPrivileges=true`: "the simplest and most effective way to ensure that a process and its children can never
     elevate privileges again" (setuid, setgid, file capabilities). It does not affect processes started through IPC
     services.
  2. `DynamicUser=yes` allocates a transient user and group per start (use `StateDirectory=`, `RuntimeDirectory=`,
     `CacheDirectory=`, `LogsDirectory=` for the writable paths it then needs).
  3. `ProtectSystem=strict` mounts the whole filesystem hierarchy read-only except `/dev`, `/proc`, `/sys`; `full` also
     makes `/etc` read-only; `true` covers `/usr` and the boot directories. With `strict` and `PrivateTmp=` on, `/tmp`
     and `/var/tmp` stay writable. `ReadWritePaths=` punches holes.
  4. `PrivateTmp=` gives private `/tmp` and `/var/tmp` removed when the service stops; `disconnected` backs them with a
     new tmpfs. `PrivateDevices=true` leaves only API pseudo devices in `/dev` (no `/dev/sda`, `/dev/mem`).
  5. `CapabilityBoundingSet=` is an allow list; a `~` prefix inverts it. `RestrictAddressFamilies=` allow lists socket
     families such as `AF_UNIX` and `AF_INET`; `none` denies all. `SystemCallFilter=` is an allow list by default; `~`
     makes it a deny list; groups such as `@system-service` exist (group names are not spelled out in the passage I
     read).
  6. `MemoryDenyWriteExecute=true` blocks writable plus executable mappings; the manual warns it is incompatible with
     programs that generate code at run time (JIT).
  7. `systemd-analyze security [UNIT...]` scores a service's sandboxing from 0.0 to 10.0 ("exposure level"); high means
     little sandboxing. The manual warns the score only counts systemd features and is not a verdict on vulnerability.
- Inference: because `ProtectSystem=strict` and `PrivateTmp=` interplay, a C or C++ daemon that wants to run with
  `ProtectSystem=strict` has to take its writable paths from `StateDirectory=` and friends or from `$RUNTIME_DIRECTORY`,
  not hardcode paths. That is a userland rule worth writing into the C and C++ guidance.

#### 5.4.2 Bootlin and ELCE material

- Bootlin `security-userland` (3.1 item 8) and the Segula "Secure by Default" talk (3.5 item 2) give the same option set
  with examples and the "start from the service's real requirements" method.

## Sources I could not reach or read

- <https://bootlin.com/doc/training/> (HTTP 403 from Apache). I used the GitHub source of the slides instead.
- The OE wiki style guide: the Yocto Contributor Guide page (1.3) is its successor, so I did not fetch the wiki.
- Slides of most ELCE 2026 talks (listed in 3.5 item 5), the OpenEmbedded Workshop and Yocto Project Summit 2025 talks,
  and the Yocto "reproducible-build-results" page: titles or snippets only.
- Yocto Security Reference (<https://docs.yoctoproject.org/6.1/security-reference/index.html>): exists, 200 OK, not read.
- Mender's technical docs beyond the overview page, SWUpdate documents beyond the overview page, and any Buildroot
  runtime reproducibility test documentation.
- No source I read gives a flash wear budget or a recommended journald configuration for embedded products; those points
  are marked as inference.

## Practices where sources disagree or differ

01. `_FORTIFY_SOURCE` level. Yocto `security_flags.inc` uses 2 (and drops it at `-O0`). Buildroot defaults to 1
    ("conservative") and offers 2 and 3, with 3 needing GCC 12 or newer. OpenSSF recommends
    `-U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=3`. Level 3 has "additional performance overhead" per Buildroot's help text.
02. Stack clash protection and other newer flags. OpenSSF recommends `-fstack-clash-protection`,
    `-fstrict-flex-arrays=3`, `-fcf-protection=full` or `-mbranch-protection=standard`, `-ftrivial-auto-var-init=zero`
    and others. I found none of them in Yocto's `security_flags.inc` or in Buildroot's `Config.in`, `package/Makefile.in`
    or `toolchain-wrapper.mk` (searched for "clash"). Both build systems expose the common set (stack protector strong,
    PIE, RELRO full, format security); OpenSSF is broader.
03. Where hardening flags travel. Yocto appends them to `TARGET_CC_ARCH` and `TARGET_LDFLAGS` (so `${CC}` carries them,
    but a recipe that does not pass `LDFLAGS` fails the `ldflags` QA check). Buildroot adds SSP, PIE and RELRO in the
    toolchain wrapper but `_FORTIFY_SOURCE` only through `TARGET_CFLAGS`. A rule for C and C++ projects must therefore
    say "honour `CC`, `CXX`, `CFLAGS`, `CXXFLAGS`, `LDFLAGS` and `CPPFLAGS`" and not assume the build system will fix a
    hardcoded Makefile.
04. Workarounds for Makefiles that ignore flags. Yocto QA documentation says `TARGET_CC_ARCH += "${LDFLAGS}"`. Bootlin's
    slide says `EXTRA_OEMAKE = "-e"`. The Yocto "single .c file" example uses `${CC} ${LDFLAGS}` without `${CFLAGS}`,
    while its Makefile example passes `CFLAGS='${CFLAGS}'`. All three are valid in some cases and inconsistent as general
    advice.
05. Definition of reproducible. Yocto: same output for any build path, any host and any time. Buildroot:
    `BR2_REPRODUCIBLE` is "experimental" and only holds for the same output directory (`O=`). Yocto's page also still
    quotes a hardknott era status. A rule that promises reproducibility must say which build system it targets.
06. SBOM format. Yocto emits SPDX (2.x earlier, 3.0 from 5.1, enriched JSON from `sbom-cve-check`); Buildroot emits
    CycloneDX through `utils/generate-cyclonedx` and its own `pkg-stats`. The CRA text names no format, only "commonly
    used and machine-readable" with at least top level dependencies; the Bootlin slide notes SPDX and CycloneDX both
    qualify. The Yocto CVE tool changed in 6.0 (`cve-check` replaced by `sbom-cve-check`), so older guidance is stale.
07. Watchdog with A/B updates. The Bootlin and RAUC material treats a hardware watchdog as one of two valid ways to
    detect failed boots (the other is a boot counter in the bootloader). Opdenacker's ELCE 2026 talk calls the watchdog
    "not necessary" for one customer and relies on a U-Boot boot counter plus a human reboot. RAUC's checklist requires
    the watchdog to be monitored if it is used.
08. Default filesystem for writable data. Bootlin recommends ext4 as the default and says to benchmark; F2FS is flash
    oriented but newer and has a larger minimum size; UBIFS on raw NAND. The kernel ext4 page deprecates `data=journal`.
    No source ranks them for a specific embedded product.
09. CRA dates. Bootlin's slide says the CRA was "adopted on October 10 2024"; the regulation itself is dated 23 October
    2024 (Council decision 10 October 2024, published 20 November 2024). The application dates (11 September 2026
    reporting, 11 December 2027 main obligations) agree across Bootlin, EUR-Lex and OpenSSF.
10. Persistent versus volatile journal. systemd's default is `auto` (persistent if `/var/log/journal` exists); Bootlin
    says tmpfs is right for log files; Yocto's `read-only-rootfs` page says to write to `/tmp` or `/var/run`. No source
    says what to do about logs you must keep across reboots on flash.

## The ten most useful sources overall

01. Yocto Project Security Manual (6.1), <https://docs.yoctoproject.org/6.1/security-manual/> : the one official place that
    ties hardening flags, read-only rootfs and CVE checking together for Yocto.
02. OpenSSF Compiler Options Hardening Guide for C and C++ (2026-08-20): the only source that gives a reasoned full flag
    set for C and C++, with sanitizer and debug info advice.
03. OE-Core `security_flags.inc` (blacksail, blob 824ba2c0) plus `insane.bbclass`: shows exactly what the Yocto build
    enforces and which QA checks are errors.
04. Yocto Reference Manual QA checks and Development Tasks "Writing a New Recipe" (6.1): how a C or C++ recipe must pass
    `LDFLAGS`, avoid stripping and RPATH, and package files.
05. Buildroot manual 2026.08 together with `Config.in`, `package/Makefile.in` and `toolchain-wrapper.mk` (tag 2026.08.2):
    the manual has no hardening chapter, so the code is the real documentation.
06. Regulation (EU) 2024/2847 (EUR-Lex), Annex I and Articles 13, 14 and 71, with the Commission FAQ v1.4: the binding
    text and the official interpretation.
07. systemd 262 manual pages (`systemd.exec`, `journald.conf`, `systemd-timesyncd`, `systemd.service`,
    `systemd-system.conf`, `systemd-analyze`): primary source for hardening, journald, wall clock restore and watchdogs.
08. Bootlin training materials (commit 442a80f0, CC BY-SA 3.0): block and flash filesystem advice, A/B updates,
    capabilities and systemd sandboxing, dm-verity, in a freely reusable licence.
09. RAUC documentation (Design Checklist and Integration, v1.15.2 era): the most concrete checklist for update, watchdog,
    time and key handling.
10. ELCE 2026 talks by Opdenacker (A/B updates and secure boot, CC BY-SA 4.0) and Segula (systemd lock down): current,
    concrete practice, but single speaker opinions.

Close seconds: Yocto Contributor Guide recipe style guide, Joshua Watt's CRA SBOM talk, Linux man-pages for `fsync` and
`clock_gettime`.
