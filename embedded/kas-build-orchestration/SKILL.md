---
name: kas-build-orchestration
description: "kas build-orchestration partner for Yocto/OpenEmbedded and other BitBake projects — `.kas.yml`/`.yml` kas config authoring and debugging, `kas build`/`kas checkout`/`kas shell`/`kas dump`/`kas menu`/`kas lock`, layered `header.includes` and `:`-composed configs, multi-repo/multi-layer orchestration, lockfiles and reproducible pins, `kas-container` (Docker/Podman, image/script version match, mounts, credential forwarding), and kas in CI (GitHub Actions/GitLab). Use when a kas build clones the wrong commit, an include override does not take effect, `bblayers.conf`/`local.conf` come out wrong, a lockfile drifts, kas-container fails on UID/ownership or SSH, or you must reason about the effective merged config. kas orchestrates Yocto/OE builds; for recipe/layer/BitBake work use yocto-openembedded-development, and for board/kernel/device-tree debugging use embedded-linux-bringup."
license: MIT
compatibility: Requires kas and Git; native builds need the target project's host dependencies, container builds need Docker or Podman. Menu needs kas UI dependencies. Guidance verified against kas 5.3; check release-matched help on other versions.
metadata:
  author: Joonas Onatsu
---

# kas Build Orchestration

Diagnose the complete input composition, resolved repository pins, actual checkouts, and generated build configuration.
These are related evidence, but they can disagree: a lock overrides a repository selector, the environment overrides a
machine, or kas skips a dirty checkout. One YAML file or a successful command is not sufficient proof of the build state.

Use this file for method; load the relevant section of [the reference](references/kas-tool.md) for command, merge,
lock, container, or cleanup details. The reference is checked against kas 5.3, not a promise about every release.

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
   affected configuration/lock diffs and repeat the check at the failed boundary. Do not turn a diagnostic into an
   unrequested branch update, cleanup, or long build.

## Evidence by Boundary

| Symptom                                    | Collect and compare                                                                                                       |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| Ignored include or setting                 | Exact colon composition, repo-relative include paths, same-key replacements, each fragment's lock, relevant dump sections |
| Wrong commit                               | Base/default selectors, `overrides.repos`, update/force flags, actual HEAD and complete Git status                        |
| Wrong machine, distro, target, task        | File values plus relevant CLI and environment overrides; generated config and downstream variable evaluation              |
| Wrong layers or local.conf                 | Resolved repository paths/layer entries, named header entries, actual files in the configured build directory             |
| UID, mount, credentials, or engine failure | Wrapper versus direct image, effective UID, image/script versions, mount paths/modes and credential file scope            |

Plain `kas dump` shows merged file inputs, retaining an `overrides` section; it does not fold selection variables such
as `KAS_MACHINE` into the dumped machine. `--resolve-refs` resolves managed repository revisions and removes repository
overrides from that output; it does not snapshot dirty work or prove a final BitBake value. See
[configuration and locks](references/kas-tool.md#lockfiles).

Capture only relevant configuration/log sections, with context sufficient to interpret them. Use the actual
`KAS_BUILD_DIR` and configured repository paths rather than assuming every build lives in `./build`.

## Mutation and Authorization

Reuse the user's existing authorization. An explicit request to fix configuration or refresh a lock permits that
bounded change and its necessary verification. A review-only request does not authorize modifying a live workspace.
Ask only when destructive effects, shared paths, credential exposure, or another consequential action exceed the scope.

- **Dump and checkout are resolving operations.** Both can fetch and check out repositories. Checkout also normally
  applies configured patches and writes build configuration. Inspect state first. kas 5.3 skips repositories it detects
  as dirty unless `--force-checkout` is supplied; its Git dirty check is narrower than full status. Never force checkout
  to silence a warning without authority to discard the affected work. Branch checkout can also move local branch refs.
- **Lock changes alter reproducible selection.** `kas lock` creates missing floating-repository pins; use
  `kas lock --update` for a deliberate refresh. They are not snapshots of every current checkout. Existing local and
  external locks affect which file can be updated. Preserve earlier lock edits and inspect all changed pins; do not
  restore from Git as a supposed rollback unless that is the state the user intends to restore.
- **Cleanup needs its actual deletion scope.** Resolve build, work, downloads, sstate, reference-repository, buildtools,
  and managed-repository paths before approval or execution. Shared caches can serve other projects. Use the release's
  dry run before deletion, but disclose that purge's preview can perform repository setup/checkout. See
  [cleanup and purge](references/kas-tool.md#cleanup-and-purge), including `--preserve-repo-refs`.
- **Credential scope is the accessible file/socket set.** Use dedicated SSH/AWS directories when isolation is needed.
  An AWS profile does not hide other files or cached sessions in a mounted directory. An SSH agent can authorize signing
  operations even though its private key files are not mounted. Native AWS setup can fall back to the user's cache if
  the dedicated config directory lacks `sso/cache`; see [credential isolation](references/kas-tool.md#credentials).
  Do not forward unrelated credentials.

Keep normal generated-file ownership clear: kas normally rewrites `local.conf` and `bblayers.conf` during setup. Make
lasting changes in the configuration sources. This does not make every build-directory file disposable, and setup-skip
options change which generation steps run.

## Versions, Trust, and Reproducibility

Check `kas --version`, the actual subcommand's `--help`, and matching upstream documentation before prescribing
version-dependent flags. Check wrapper help separately from native kas help. Prefer matching wrapper/image releases;
5.3 warns on a mismatch, which is a compatibility concern, not proof of a particular failure.

`header.version` declares configuration-format expectations. Use the format changelog to choose a suitable minimum;
do not bump it without a feature need. The installed kas validates against its schema and a supported version range,
not a comprehensive per-key gate keyed to that declaration. Parsing on a new release does not qualify an older release.

Pins constrain repository selection; they do not establish publisher identity. kas 5.3 can enforce configured Git
commit/tag signature verification with `signers`, `signed`, and `allowed_signers` (format 19). Use the version-matched
[security guidance](references/kas-tool.md#security), including its trust-root and dependency requirements.

A lockfile does not capture unmanaged root-repository changes, arbitrary local edits, every recipe source, or the host
kernel. Record those inputs and image identity when release reproduction matters. Containers reduce host dependency
variation; verify artifact reproducibility separately rather than claiming it from a lock or image tag.

## Report the Result

Report the proven cause or remaining hypothesis, the evidence that supports it, the precise edit/command, and the result
of verification. When blocked, name the unavailable evidence and the next discriminating check. State whether you
verified configuration shape, real repository behavior, a build artifact, or only a static walkthrough.

## Sources

- [kas 5.3 manual](https://kas.readthedocs.io/en/5.3/)
- [kas 5.3 implementation](https://github.com/siemens/kas/tree/5.3)
- [Attributions and source influence](ATTRIBUTIONS.md), with the MIT notice and [upstream license](LICENSE.upstream)
