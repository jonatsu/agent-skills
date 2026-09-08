# Verification Workflows

Two co-equal lanes. **Host-side** runs in CI with no board and sees the artefact as built. **On-target** sees
runtime state — mount options, running users, loaded policy — that no host-side check can observe. Neither is
a substitute for the other, and most controls need one of each.

## Host-side lane

Everything here reads the deploy directory or the datastore. Nothing boots.

| Question                                              | Command                                                                                        |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| What actually shipped?                                | `tmp/deploy/images/<machine>/<image>-<machine>.rootfs.manifest`                                |
| Which kernel modules shipped?                         | `grep '^kernel-module-' <manifest>`                                                            |
| Is a binary hardened?                                 | `checksec --file=<path>` / `--dir=<dir>` — **`checksec-native` needs a one-line bbappend**     |
| Did a kernel symbol survive?                          | `grep CONFIG_… <kernel build dir>/.config`, plus `cfg/mismatch.txt`                            |
| Did the recipe drop `LDFLAGS`, strip, or leak rpaths? | the `ldflags`, `already-stripped`, `rpaths` `ERROR_QA` checks — already run at `do_package_qa` |
| What changed since the last release?                  | `buildhistory` diff                                                                            |
| Is the build reproducible?                            | `oe-selftest -r reproducible.ReproducibleTests.test_reproducible_builds`                       |
| Which postprocess commands ran?                       | `bitbake-getvar -r <image> ROOTFS_POSTPROCESS_COMMAND`                                         |

**The postprocess grep is the cheapest high-value check in this list.** It shows, in one expanded value, every
credential and rootfs tweak the image applied:

```bash
bitbake-getvar -r <image> ROOTFS_POSTPROCESS_COMMAND | \
  grep -oE 'ssh_allow_empty_password|ssh_allow_root_login|postinst_enable_logging|serial_autologin_root|zap_empty_root_password|read_only_rootfs_hook'
```

Read the **absence** of `zap_empty_root_password` as the finding, not its presence — it runs when
`empty-root-password` is *not* set.

You can also inspect the rootfs before it is packed, which is where the credential and configuration checks in
`image-attack-surface.md` belong in CI:

```bash
bitbake-getvar -r <image> IMAGE_ROOTFS      # tmp/work/<machine>/<image>/…/rootfs
```

Treat that path as an inspection target only. Editing under `tmp/work` is not a change to anything that will
be rebuilt.

## On-target lane

`testimage` runs an oeqa suite against a booted image, on QEMU by default or over ssh to a real board:

```bitbake
# local.conf
IMAGE_CLASSES += "testimage"
TEST_SUITES = "ping ssh <your suite>"
TEST_TARGET = "qemu"          # "simpleremote" plus TEST_SERVER_IP/TEST_TARGET_IP for a real board
TESTIMAGE_AUTO = "0"          # "1" runs it after every image build
```

```bash
bitbake <image> -c testimage
```

`ptest` is the other on-target lane — a package's own test suite, run on the target. It answers "does this
component work here", not "is this image hardened", so it belongs in this skill only when a security component
ships one.

## The three-image pattern

Scanners and analysis tools are attacker aids: shipping `checksec`, `kernel-hardening-checker`, Lynis or
OpenSCAP in production hands over a map of the weak spots and drags in dependencies you removed on purpose.
Building a separate hardened image to test also tests the wrong thing.

The pattern that resolves it is three images from one base:

| Image       | Contents                                                       | Used for                                              |
| ----------- | -------------------------------------------------------------- | ----------------------------------------------------- |
| `prod`      | what ships                                                     | the release artefact                                  |
| `dev`       | prod plus developer conveniences                               | development, never released                           |
| `prod-test` | **prod's package set** plus the scanners and oeqa dependencies | running the security suite against production content |

`prod-test` must inherit prod's `IMAGE_INSTALL` and features and add only test tooling — the moment it changes
a security-relevant setting, it stops being evidence about the shipped image. Say which of the three a result
came from whenever you report one.

## Writing an assertion that asserts

Upstream ships the harness, the images and the packaging. **It does not ship assertions that check
properties.** `meta-security`'s `security-test-image` declares a substantial-looking suite —
`ssh ping apparmor clamav samhain sssd checksec smack suricata aide firejail`, plus `parsec tpm2 swtpm ima` —
and the cases are overwhelmingly "the tool is installed and runs":

```python
# lib/oeqa/runtime/cases/aide.py
status, output = self.target.run('aide --help')
self.assertEqual(status, 0, msg = msg)
```

The `checksec` fortify case is the sharpest example, and it is a real defect:

```python
# lib/oeqa/runtime/cases/checksec.py
status, output = self.target.run('checksec --fortify-proc 1')
match = re.search('FORTIFY_SOURCE support:', output)
if not match:
    self.assertEqual(status, 1, msg = msg)
```

**If the regex matches, nothing is asserted.** The test passes whether or not `FORTIFY_SOURCE` is present, and
it has been unchanged since it was introduced in 2019. A second, independent defect: `--fortify-proc 1` and
`--proc=1` inspect **PID 1**, not the shipped binaries — so even repaired, the case could not answer whether
the image was built with fortification.

Hence the Iron Law's second half. When you meet a green security suite, read what it asserts before believing
it.

A property assertion for the same question looks like this — it names the binaries, it fails when the property
is missing, and it encodes the exemptions from `compiler-and-binary-hardening.md` as an explicit allowlist:

```python
from oeqa.runtime.case import OERuntimeTestCase
from oeqa.runtime.decorator.package import OEHasPackage

EXPECT_HARDENED = ['/usr/sbin/sshd', '/usr/bin/<your daemon>']

class FortifyTest(OERuntimeTestCase):
    @OEHasPackage(['checksec'])
    def test_binaries_are_fortified(self):
        for path in EXPECT_HARDENED:
            status, output = self.target.run('checksec --file=%s --format=json' % path)
            self.assertEqual(status, 0, 'checksec failed on %s: %s' % (path, output))
            self.assertIn('"fortify_source":"yes"', output.replace(' ', ''),
                          'FORTIFY_SOURCE missing in %s' % path)
```

Two rules that make the difference between this and the upstream case:

- **Assert in the success path.** An assertion reachable only when parsing failed tests the parser.
- **Name the artefact under test.** A check against PID 1, or against whatever happens to be running, is not a
  statement about the image.

**The key names above are measured, not assumed.** Run against `checksec` 2.6.0 as `meta-security` packages it
at `scarthgap` on 2026-09-08, `--format=json --file=` emits exactly:

```json
{ "/bin/bash": { "relro":"full","canary":"yes","nx":"yes","pie":"yes","rpath":"no","runpath":"no",
                 "symbols":"no","fortify_source":"yes","fortified":"13","fortify-able":"33" } }
```

So `"fortify_source":"yes"` is correct at this version. Two cautions that still apply: the recipe pins a
`SRCREV`, and these names have changed upstream across versions, so re-check when the pin moves; and
`--format=json --fortify-file=` emits **repeated `"function"` keys in one object**, which is not valid JSON and
which `jq` silently reduces to the last occurrence. Parse the `--file` form, not the `--fortify-file` form.

Getting `checksec-native` to build at all needs a one-line bbappend — see `compiler-and-binary-hardening.md`.

## Reporting a result

Say four things, in this order: **which lane** the check ran in, **which image** it ran against, **what was
observed** on the artefact, and **what the check cannot see**. That last clause is what stops a host-side
`checksec` pass being read as "the running system is hardened", and an on-target `findmnt` pass being read as
"every image we ship is read-only".
