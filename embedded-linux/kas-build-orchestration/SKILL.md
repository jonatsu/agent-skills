---
name: kas-build-orchestration
description: "Configure and debug kas, the YAML tool that fetches layer repositories and generates Yocto/OpenEmbedded or ISAR build configuration. Use for writing or composing kas configs and includes, a wrong checked-out commit or ignored override, a wrong generated local.conf or bblayers.conf, creating or refreshing kas lockfiles, kas-container ownership, mount, or credential failures, kas in CI, or cleaning a kas workspace. Recipe, layer, and BitBake task failures belong to yocto-openembedded-development."
license: MIT
compatibility: Requires kas and Git; native builds need the target project's host dependencies, container builds need Docker or Podman. Menu needs kas UI dependencies. Guidance verified against kas 5.5; check release-matched help on other versions.
metadata:
  author: Joonas Onatsu
---

# kas Build Orchestration

Diagnose the complete input composition, resolved repository pins, actual checkouts, and generated build configuration.
These are related evidence, but they can disagree: a lock overrides a repository selector, the environment overrides a
machine, or kas skips a dirty checkout. One YAML file or a successful command is not sufficient proof of the build state.

Use this file for method. Load the relevant section of [the reference](references/kas-tool.md) for command, merge,
lock, container, or cleanup details.

## Route the Task

| Boundary                                                                                 | Guidance                           |
| ---------------------------------------------------------------------------------------- | ---------------------------------- |
| kas composition, repository resolution, generated configuration, wrapper/container setup | This skill                         |
| Recipes, layer integration, BitBake task failures, sstate internals, SDKs                | **yocto-openembedded-development** |
| Kernel, device tree, drivers, or board runtime                                           | **embedded-linux-bringup**         |
| Bootloader internals, boot flow, FIT verification                                        | **u-boot-development**             |
| Buildroot configuration or package integration                                           | **buildroot-development**          |

A downstream build failure can expose a wrong kas checkout. Establish the implicated inputs before handing off, without
requiring a new checkout or a full build merely to classify an error.

## Workflow

1. **Establish context.** Record kas version, native/wrapper/direct-image/CI entry point, the exact command and ordered
   config list, relevant `KAS_*` selection/path variables, and the symptom. For containers, record script version,
   engine, image tag/digest, effective user, entrypoint, and mounts as needed. Inspect values narrowly; redact credentials.
2. **Classify the failing boundary.** Is it include/merge, fetch/ref/lock, configuration generation, container setup,
   or downstream BitBake? If dump itself fails, inspect that failure and its inputs. Missing tools or an unavailable
   engine are not reasons to block file inspection or invent a successful resolution.
3. **Inspect existing state before resolving it.** Read the entry files, relevant include chain and adjacent locks;
   resolve repository and cache paths. Inspect managed repositories with `git status --short --untracked-files=all`,
   current HEAD, and relevant branch refs. Preserve local commits and edits before changing checkouts.
4. **Collect evidence appropriate to the boundary.** Use the table below. When repository setup is authorized and its
   effects are understood, run dump with the exact composition to resolve includes. It may fetch, use credentials,
   create repositories, and change checkouts. Use a disposable workspace when existing state must remain untouched;
   record that it cannot reproduce uncommitted local changes automatically.
5. **Validate the most likely cause.** Choose the smallest check that distinguishes it from plausible alternatives.
   Compare intended selectors with actual HEAD/status and generated configuration. A successful checkout can still have
   skipped a dirty repository. Route final BitBake variable expansion to the Yocto skill when assignment precedence matters.
6. **Apply the authorized fix and verify its result.** Correct the owning YAML fragment, pin, or wrapper setting. Review
   affected configuration/lock diffs and repeat the check at the failed boundary. Keep a diagnostic to the checks it
   needs; a branch update, cleanup, or long build needs its own request.

## Evidence by Boundary

| Symptom                                    | Collect and compare                                                                                                       |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| Ignored include or setting                 | Exact colon composition, repo-relative include paths, same-key replacements, each fragment's lock, relevant dump sections |
| Wrong commit                               | Base/default selectors, `overrides.repos`, update/force flags, actual HEAD and complete Git status                        |
| Wrong machine, distro, target, task        | File values plus relevant CLI and environment overrides; generated config and downstream variable evaluation              |
| Wrong layers or local.conf                 | Resolved repository paths/layer entries, named header entries, actual files in the configured build directory             |
| UID, mount, credentials, or engine failure | Wrapper versus direct image, effective UID, image/script versions, mount paths/modes and credential file scope            |

Plain `kas dump` shows merged file inputs only; selection variables, lock resolution, and dirty checkouts need their
own evidence. See [dump and observed build state](references/kas-tool.md#dump-and-observed-build-state).

Capture only relevant configuration/log sections, with context sufficient to interpret them. Use the actual
`KAS_BUILD_DIR` and configured repository paths rather than assuming every build lives in `./build`.

## Mutation and Authorization

Reuse the user's existing authorization. An explicit request to fix configuration or refresh a lock permits that
bounded change and its necessary verification. A review-only request does not authorize modifying a live workspace.
Ask only when destructive effects, shared paths, credential exposure, or another consequential action exceed the scope.

- **Dump and checkout resolve repositories.** Both can fetch and check out, and checkout also applies patches and
  writes build configuration. Inspect HEAD and full `git status` first, because kas skips a repository it detects as
  dirty. Add `--force-checkout` only with authority to discard the affected work. See
  [commands](references/kas-tool.md#installation-and-commands).
- **Lock changes alter reproducible selection.** `kas lock` adds missing pins, and `kas lock --update` refreshes
  floating ones. Review every changed pin. Restore a lock from Git only when HEAD holds the state the user wants back.
  See [lockfiles](references/kas-tool.md#lockfiles).
- **Cleanup deletes whole caches.** Resolve every path it reaches before approval, then preview with `--dry-run`. A
  purge preview still resolves repositories. See [cleanup and purge](references/kas-tool.md#cleanup-and-purge).
- **A build holds its build directory until it exits.** Run one build per `KAS_BUILD_DIR`; a second concurrent run
  can break both and report a misleading cause, such as an OOM-killed bitbake-server. After a task fails, BitBake stops
  starting new tasks but waits for running ones, which can take a long time. Confirm the process has exited before
  you retry.
- **Credential scope is every file and socket the build can reach.** Forward only dedicated directories and files
  that hold the build's own credentials. See [credentials](references/kas-tool.md#credentials).

Make lasting changes in the configuration sources, because kas rewrites `local.conf` and `bblayers.conf` during setup.

## Versions, Trust, and Reproducibility

Check `kas --version`, the actual subcommand's `--help`, and matching upstream documentation before prescribing
version-dependent flags. Check wrapper help separately from native kas help. Prefer matching wrapper/image releases;
5.5 warns on a mismatch, which is a compatibility concern, not proof of a particular failure.

`header.version` declares configuration-format expectations. Raise it only to the lowest format that provides a key
the configuration uses, per the format changelog. The installed kas validates against its schema and a supported
version range, not a comprehensive per-key gate keyed to that declaration. Parsing on a new release does not qualify
an older release.

Pins constrain repository selection; they do not establish publisher identity. Pin every `commit` with its full hash.
kas 5.5 can enforce configured Git commit/tag signature verification with `signers`, `signed`, and `allowed_signers`
(format 19). Read the version-matched [security guidance](references/kas-tool.md#security) before configuring signing
or using `SSH_PRIVATE_KEY` with kas older than 5.4.

A lockfile does not capture unmanaged root-repository changes, arbitrary local edits, every recipe source, or the host
kernel. Record those inputs and image identity when release reproduction matters. Containers reduce host dependency
variation; verify artifact reproducibility separately rather than claiming it from a lock or image tag.

## Report the Result

Report the proven cause or remaining hypothesis, the evidence that supports it, the precise edit/command, and the result
of verification. When blocked, name the unavailable evidence and the next discriminating check. State whether you
verified configuration shape, real repository behavior, a build artifact, or only a static walkthrough.

## Sources

- [kas 5.5 manual](https://kas.readthedocs.io/en/5.5/)
- [kas 5.5 implementation](https://github.com/siemens/kas/tree/5.5)
- [Attributions and source influence](ATTRIBUTIONS.md), with the MIT notice and [upstream license](LICENSE.upstream)
