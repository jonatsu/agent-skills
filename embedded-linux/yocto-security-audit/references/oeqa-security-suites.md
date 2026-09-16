# Running the oeqa Security Suite, and Reading What Comes Back

Upstream ships the harness, the images and the packaging. **It does not ship assertions that check
properties.** Running the suite is easy; knowing what a result means is the whole job.

Hardening's `verification-workflows.md` owns the two-lane model, the three-image pattern and the worked
property assertion. This file owns *running* the suite and *interpreting* it.

## Running it

```bitbake
# in local.conf or the image recipe
IMAGE_CLASSES += "testimage"
TEST_SUITES = "ping ssh <suites>"
TEST_TARGET = "qemu"          # "simpleremote" plus TEST_SERVER_IP/TEST_TARGET_IP for a real board
TESTIMAGE_AUTO = "0"
```

```bash
bitbake <image> -c testimage
```

`TEST_SUITES` names case modules; `meta-security`'s `security-test-image` sets
`ssh ping apparmor clamav samhain sssd checksec smack suricata aide firejail parsec tpm2 swtpm ima`.

### In a container

Measured under kas-container with Docker. Three obstacles, in the order they appear:

| Symptom                                             | Cause and fix                                                                                                                                   |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `TUN control device /dev/net/tun is unavailable`    | pass `--device /dev/net/tun` and `--cap-add NET_ADMIN` to the engine                                                                            |
| `You have no read or write permission on /dev/kvm`  | the entrypoint rebuilds the build user without supplementary groups, so `--group-add` does not reach it. Set `QEMU_USE_KVM = ""` and accept TCG |
| `Setting up tap device failed: sudo … runqemu-ifup` | `TEST_RUNQEMUPARAMS = "slirp"` — user-mode networking, no tap, no sudo                                                                          |

`slirp` plus TCG works with no privilege at all and is the configuration the results below came from. It is
slower and it is not upstream's CI environment, which matters for timing-sensitive or network-topology-sensitive
cases.

## What a green run actually means

**A pass in this suite usually means "the tool is installed and its `--help` exits 0".** That is worth
something — it catches a broken package — and it is not a security property.

Ten of the layer's test methods have a structure where the **only assertion sits inside `if not match:`**, so
when the expected output *is* found, nothing is asserted at all:

```python
# lib/oeqa/runtime/cases/checksec.py
status, output = self.target.run('checksec --fortify-proc 1')
match = re.search('FORTIFY_SOURCE support:', output)
if not match:
    self.assertEqual(status, 1, msg = msg)
```

The pattern appears in `aide.py` (1), `apparmor.py` (3), `checksec.py` (1), `samhain.py` (2) and
`tripwire.py` (3). Excluding `smack.py` — the one genuine suite, 417 of the directory's 799 lines — **10 of 29
test methods assert nothing on the success path.**

`checksec` carries a second, independent defect: `--fortify-proc 1` and `--proc=1` inspect **PID 1**, not the
shipped binaries. Even repaired, the case could not answer whether the image was built with fortification.

## The measured result, and why it is the point

`security-test-image` at `scarthgap`, `qemux86-64`, 2026-09-08. **58 results: 33 passed, 16 failed, 9 skipped.**

| Result  | Cases                                                                                                                            |
| ------- | -------------------------------------------------------------------------------------------------------------------------------- |
| PASSED  | `test_checksec_fortify`, every `--help` smoke test, 9 of 21 SMACK label-manipulation cases                                       |
| FAILED  | 12 of 21 SMACK enforcement cases, `ima.test_ima_enabled`, `apparmor.test_apparmor_aa_complain`, `clamav.test_freshclam_download` |
| SKIPPED | 4 IMA and 4 suricata-update cases behind failed dependencies, `apparmor.test_apparmor_aa_enforce`                                |

**The tests that assert nothing passed. Nearly every test that asserts a real property failed.**

Three readings that follow directly:

1. **`test_checksec_fortify` PASSED on an image where no fortification claim was checked.** Do not read that
   line as evidence about `_FORTIFY_SOURCE`. Use the property assertion in hardening's
   `verification-workflows.md` instead.

2. **`apparmor.test_apparmor_aa_complain` FAILED — through the wrong branch.** All three AppArmor cases grep
   for `apparmor module is loaded.`, which is what `aa-status` prints, not `aa-complain`:

   ```text
   AssertionError: 1 != 0 : aa-complain  failed. Status and output:1 and Traceback…
   ```

   It caught a real failure only via the `if not match:` fallback. Had `aa-complain` exited 0 while doing
   nothing, the test would have passed silently.

3. **The SMACK failures are a configuration collision, not a SMACK defect.** The image enables both `apparmor`
   and `smack` in `DISTRO_FEATURES` while the kernel command line carries `security=apparmor`. Only one major
   LSM is active, so SMACK's enforcement cases cannot pass.

That last point is the one to carry: **upstream ships a security test image that fails its own suite out of the
box.** Any suite result has to be read against the image's configuration before it means anything.

## How to read a result

- [ ] **Check the configuration first.** `DISTRO_FEATURES`, the kernel command line, and which LSM is actually
  active. A failure caused by a configuration collision is not a security finding.
- [ ] **Ask what each passing case asserted.** Read the case source; it is a few dozen lines. A pass whose
  assertion is unreachable is not evidence.
- [ ] **Separate environmental failures.** Downloads, timing and network topology fail for reasons unrelated to
  the image — `clamav.test_freshclam_download` here.
- [ ] **Treat a failing property test as the most valuable result in the run.** It is the only kind that was
  ever going to tell you something.

## Gating on it

Do not gate on `do_testimage`'s exit status alone. On the measured run it fails, for reasons almost entirely
unrelated to the image's security posture — and a gate that counted passes instead would see 33 green and
conclude the opposite. **Neither number is an answer.** See `gating-and-reporting.md`.

Gate on named cases you have read, or on your own property assertions. Everything else is noise with a
changing sign.

## Writing a case that asserts

Covered in hardening's `verification-workflows.md`, which carries the worked example and the two rules that
matter: **assert in the success path**, and **name the artefact under test**. Two additions from running the
suite here:

- **`OETestDepends` chains hide results.** A failed case skips everything behind it — 4 IMA cases and
  `aa-enforce` disappeared that way. A skip in this suite often means an earlier failure, not an inapplicable
  test, so read skips as a chain rather than individually.
- **Put the expected string and the command in one place.** The AppArmor bug is three tests sharing one regex
  that only matches one of them; that is a copy-paste failure a shared constant would have made obvious.
