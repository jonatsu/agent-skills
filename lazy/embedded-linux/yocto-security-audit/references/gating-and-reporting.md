# Gating and Reporting

An audit that nobody can act on is a document. This file is about the two outputs that get acted on: a CI gate
that fails for the right reasons, and a report a reader can use.

## Why the obvious gate does not work

The measured `security-test-image` run at `scarthgap`: **58 results — 33 passed, 16 failed, 9 skipped**, and
`do_testimage` exits non-zero.

- A gate keyed on **exit status** blocks the release, for reasons almost entirely unrelated to the image's
  security posture — an LSM configuration collision, a ClamAV signature download, and a chain of skips.
- A gate keyed on **pass count** sees 33 green and concludes the opposite.

**Neither number is an answer.** Both are stable, both are automatable, and both are wrong. That is the case
against gating on a suite you have not read.

## What to gate on instead

Gate on a small number of properties you chose, each of which fails for exactly one reason:

| Gate on                                                | Not on                                 |
| ------------------------------------------------------ | -------------------------------------- |
| named oeqa cases you have read, or your own assertions | the suite's exit status                |
| a specific `checksec` property on a named binary list  | a whole-rootfs `checksec` sweep        |
| the absence of `root::` in `/etc/shadow`               | "debug-tweaks not in `IMAGE_FEATURES`" |
| a setuid inventory diff against a committed baseline   | the setuid count                       |
| the manifest diff against the previous release         | package count                          |

Two properties make a gate durable:

**It fails closed.** A missing report, an unparseable file or a tool that did not run must fail, not pass. This
is the single highest-value line in any gate — it converts every future rename, relocation or tooling change
from a silent pass into a loud failure.

```bash
test -f "$report" || { echo "audit produced no report — failing"; exit 1; }
```

**It names its own blind spots.** A gate that checks four properties should say so, so nobody reads a green
build as "audited".

## Baselines and drift

Most audit value in CI is not absolute, it is **differential**. The question "is this image secure" has no
mechanical answer; "did anything change" does.

```bash
# commit these per release, diff them per build
tmp/deploy/images/<machine>/<image>-<machine>.rootfs.manifest    # package set and versions
find rootfs -perm -4000 | sort                                   # setuid inventory
jq -S '{DISTRO_FEATURES,IMAGE_FEATURES,ROOTFS_POSTPROCESS_COMMAND}' <image>.testdata.json
```

`buildhistory` does the manifest half of this already and is worth enabling for it alone.

A drift gate has a failure mode worth naming: **it accepts whatever the baseline contained.** If the first
baseline was captured from an image with an empty root password, drift will never complain about it. Baselines
need one absolute audit at the start and a review whenever they are updated.

## Severity is a judgement about intent

A finding is a fact about an artefact. Severity is not, and this is where most audit reports go wrong.

The worked example, from upstream's own image: an empty root password, `PermitRootLogin yes` and
`PermitEmptyPasswords yes` in `security-test-image`. Three genuine findings, **severity nil** — it is a test
image built so a harness can log in. The same three findings in a shipped image are critical.

So the rule: **report the finding always; assign severity only against a stated purpose, and if the purpose is
unknown, say the severity is unknown rather than guessing.** "Critical if this ships; expected if it does not"
is a complete and honest severity for an artefact whose role you were not told.

## False positives, by category

Each has its own shape, and each is covered where the finding is produced:

| Category                                | Usual cause                                                           |
| --------------------------------------- | --------------------------------------------------------------------- |
| `checksec` red cells                    | the 21 `:pn-` opt-outs in `security_flags.inc` — intended state       |
| kernel-hardening-checker "failed" lines | upstream recommendations that cost performance, declined deliberately |
| Lynis warnings on a minimal image       | checks assuming a general-purpose distribution                        |
| oeqa failures                           | configuration collisions and environment, not the image               |
| "package X is ancient"                  | a backported fix — route to **yocto-vulnerability-management**        |

A report that has not subtracted these is a tool's output, not an audit.

## The report

Five things, in this order. Anything less is not actionable:

1. **The artefact.** Which image, which recipe (`PN`, not the filename), which release, and whether it is what
   ships. If you do not know, say so — it bounds everything below.
2. **The lane and the tooling.** Host-side or on-target, which tools at which versions.
3. **Coverage.** What was checked, and — the part that gets skipped — **what was not**, including checks
   disabled by default in the tools you ran.
4. **Findings**, each with the observation that produced it and the artefact path it came from.
5. **Severity against a stated purpose**, or an explicit "purpose unknown".

## What an audit cannot conclude

State these rather than letting a reader infer them:

- **That the image is secure.** An audit finds what it looked for. "No findings" is a statement about the
  checks, not about the artefact.
- **That the artefact is the one that ships.** Nothing in an image establishes this.
- **That configuration equals behaviour.** Kernel command line, initramfs and runtime overlays override what is
  on disk.
- **Anything about the running fleet.** A device in the field has had updates, configuration changes and
  possibly an intrusion. Auditing an image is not auditing a deployment, and intrusion detection, forensics and
  incident response are different disciplines with different starting states.
