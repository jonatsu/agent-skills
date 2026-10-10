# kas — Command and Configuration Reference

Checked against **kas 5.3** documentation and implementation. Use release-matched help for other versions; native kas,
`kas-container`, and a project's custom wrapper can own different commands and flags. This reference supports the
workflow in `SKILL.md`; read only the branch needed for the task.

## Contents

- [Installation and commands](#installation-and-commands)
- [Dump and observed build state](#dump-and-observed-build-state)
- [Configuration and composition](#configuration-and-composition)
- [Lockfiles](#lockfiles)
- [Selection and path variables](#selection-and-path-variables)
- [Containers](#containers)
- [Credentials](#credentials)
- [Cleanup and purge](#cleanup-and-purge)
- [CI and ISAR](#ci-and-isar)
- [Security](#security)
- [Reproduction evidence](#reproduction-evidence)

## Installation and Commands

Use the project's supported kas version and existing installation method. An isolated native install can use
`pipx install 'kas==5.3'`; distro packages may provide another release. Native builds still need the dependencies of
the selected Yocto/OE release. Menu requires both kconfiglib (supplied by `kas[tui]`) and newt's Python bindings
for its terminal UI. Consult the
[installation guide](https://kas.readthedocs.io/en/5.3/userguide/getting-started.html) for the host environment.

Before these commands, inspect paths and repository state and establish authorization for their effects. Dump, diff,
lock, shell, and build can resolve repositories; their names do not imply passive inspection.

| Operation                              | kas 5.3 command                                               | Relevant effect                                                                    |
| -------------------------------------- | ------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Set up and build                       | `kas build kas-project.yml`                                   | Fetch/checkout, patches, generated config, BitBake build                           |
| Set up without building                | `kas checkout kas-project.yml`                                | Fetch/checkout, patches and generated config                                       |
| Flatten inputs                         | `kas dump kas-project.yml`                                    | Resolve repositories, emit configuration; skip patches and build config generation |
| Run a command in the build environment | `kas shell kas-project.yml -c 'bitbake -c devshell myrecipe'` | Normally performs setup before the command                                         |
| Configure a menu                       | `kas menu Kconfig`                                            | Read Kconfig, write `.config.yaml`; can trigger a selected build                   |
| Create missing pins                    | `kas lock kas-project.yml`                                    | Resolve floating managed repos and write applicable local locks                    |
| Refresh pins                           | `kas lock --update kas-project.yml`                           | Update floating refs and applicable local locks                                    |
| Compare configurations                 | `kas diff old.yml new.yml`                                    | Resolve two configurations; not a one-argument checkout-versus-lock comparison     |
| Select a target/task                   | `kas build kas-project.yml --target myrecipe --task compile`  | Run the selected BitBake task after setup                                          |

`kas menu` consumes **Kconfig**, not a kas YAML file. Its `.config.yaml` records menu selections and generated kas
settings; commands with an omitted config can use that file in `KAS_WORK_DIR`. Do not accidentally replace another
project's saved selections. `kas diff` accepts `--content-only` to omit repository log details; this does not make
repository resolution read-only.

[Plugin documentation and help](https://kas.readthedocs.io/en/5.3/userguide/plugins.html) owns the full option inventory.
`--force-checkout` can discard local work; never add it merely to make a setup warning disappear. Without it, kas skips
repositories it detects as dirty, so verify actual HEAD/status even after success. For Git, kas 5.3's dirty test uses
`git diff --stat`, which does not cover every staged or untracked change. Inspect full status and relevant branch refs.

## Dump and Observed Build State

Dump can fetch/clone/check out repositories, including repositories supplying includes. In 5.3 it skips patch application,
build-environment setup, and generated BitBake configuration. Therefore it is useful for input resolution, but cannot
prove that existing files under the build directory correspond to that input. Do not use it as the first action when
preserving a live checkout is part of the task; inspect files first or resolve in an authorized disposable workspace.

```bash
kas dump kas-base.yml:board.yml:debug-image.yml
kas dump --format json kas-project.yml
kas dump --resolve-refs kas-project.yml
```

Plain dump retains the `overrides` mapping. Read `overrides.repos.<name>` alongside base/default repository selectors.
`--resolve-refs` replaces managed repository refs with resolved revisions and removes those overrides from the output.
Resolution happens before configured patches; neither form captures arbitrary dirty files. `--resolve-local` can add
root-repository tracking information, but warnings about unversioned or dirty sources still require investigation.

Selection overrides such as `KAS_MACHINE` are not substituted into plain dump's `machine` field. Capture the relevant
CLI/environment selection separately, then inspect actual `local.conf`, `bblayers.conf`, and repository state. A strong
assignment in a `local_conf_header` can outrank kas's generated `MACHINE ??=`; use the Yocto/OE skill for final BitBake
variable evaluation. Avoid logging environment variables or configuration values containing credentials.

`kas dump --lock` emits locking-shaped output. The old write combination `--lock --inplace` is deprecated in 5.3 and
routes to the lock plugin; use the lock commands below for writes. Do not equate an invocation containing `--update`
with one that omits it.

## Configuration and Composition

A header with a supported `version` is sufficient for schema validity; a useful build also needs suitable repositories,
layers, and target selections. In 5.3, omitted machine/distro/target select `qemux86-64`, `nodistro`, and
`core-image-minimal`. Specify them when a silent default would select the wrong product.

The following illustrates the configuration shape using historical documentation pins, not a qualified release matrix.
Replace repository revisions and machine/layer choices with the project's verified compatible set.

```yaml
header:
  version: 14
machine: raspberrypi4-64
distro: poky
repos:
  meta-custom:
  poky:
    url: https://git.yoctoproject.org/git/poky
    commit: 89e6c98d92887913cadf06b2adb97f26cde4849b
    layers:
      meta:
      meta-poky:
      meta-yocto-bsp:
local_conf_header:
  product: |
    BB_NUMBER_THREADS = "8"
    PARALLEL_MAKE = "-j8"
    IMAGE_INSTALL:append = " strace gdbserver"
```

A repository with neither URL nor path refers to the repository containing the configuration. Its layer paths are
relative to that repository's root. An explicit relative repository `path` is relative to `KAS_WORK_DIR`; an absolute
path can put managed data outside it. No URL disables VCS operations for that entry. An absent `layers` mapping selects
the repository root as a layer; explicitly exclude non-layer repositories such as a standalone BitBake checkout.

### Include Order, Paths, and Replacement

```yaml
header:
  version: 14
  includes:
    - kas/base.yml
    - kas/boards/board.yml
    - kas/features/debug.yml
```

For files under Git, these string paths are relative to the **repository root**, not the including file's directory.
Outside version control, the root is the first configuration's directory. A deprecated file-relative fallback exists
in 5.3; do not rely on it for a new configuration. Cross-repository includes use `repo` and `file`, with `file` relative
to that repository's root. Includes must stay inside the referenced repository.

```yaml
header:
  version: 14
  includes:
    - repo: bsp
      file: kas/board.yml
repos:
  bsp:
    url: https://www.example.com/git/meta-bsp
    branch: release
    layers:
      meta-board:
```

The cross-repository example requires a real project URL and an approved branch/pin. kas may need several checkout/merge
iterations to discover transitive includes. An included file must not change the revision of the repository from which
it is being loaded; that creates an unsupported circular repository dependency.

Includes merge depth-first and top-to-bottom, then the containing file's values merge last. Dictionaries merge
recursively; non-map values, including strings and lists, replace earlier values. Dictionary insertion order is
preserved, and the merged header version is the maximum used version. For example:

| Earlier fragment                                  | Later fragment                      | Result                                    |
| ------------------------------------------------- | ----------------------------------- | ----------------------------------------- |
| `target: [image-a, image-b]`                      | `target: [image-c]`                 | Only `image-c`                            |
| `local_conf_header: {product: old, common: keep}` | `local_conf_header: {product: new}` | `product` becomes `new`; `common` remains |
| `local_conf_header: {product: old}`               | `local_conf_header: {debug: extra}` | Both named entries, in insertion order    |

For append-like header behavior, use another named entry. Reusing a key replaces its complete text, not part of the
BitBake statement inside it.

**Merge order and emission order are different, and the second one decides which assignment wins.** Merging preserves
insertion order, as above. But kas writes the header entries **sorted by key**: `_get_conf_header` iterates
`sorted(...)` over the mapping, so `local.conf` receives them alphabetically regardless of which fragment supplied
them ([config.py](https://github.com/siemens/kas/blob/5.3/kas/config.py)). `bblayers_conf_header` is emitted the same
way.

That is the supported lever for overriding a vendored fragment's setting without editing it: add a named entry whose
key sorts after the one being overridden, and use a plain `=` so the later line wins in BitBake.

```yaml
local_conf_header:
  base: |          # from the upstream fragment
    BB_NUMBER_THREADS = "24"
  host-tuning: |   # sorts after "base", so this is written later and wins
    BB_NUMBER_THREADS = "8"
```

Confirm the result in the generated `local.conf` rather than trusting the ordering; a key chosen for its alphabetical
position is a fragile intent to express, so comment why the name was chosen.

Map merging also means omitted layer entries remain; explicitly exclude unwanted layers:

```yaml
repos:
  poky:
    layers:
      meta-yocto-bsp: excluded
```

Command-line composition applies the same ordered merging:

```bash
kas dump kas/base.yml:kas/boards/board.yml:kas/features/debug.yml
```

All colon-composed files must belong to the same repository or all be outside version control. Use a cross-repository
include for files from different repositories. Configs on the command line **and included fragments** can each have
adjacent lockfiles. A new containing file can add its own lock, so include/composition equivalence assumes the same
relevant inputs and locks. See the
[configuration guide](https://kas.readthedocs.io/en/5.3/userguide/project-configuration.html) and
[include implementation](https://github.com/siemens/kas/blob/5.3/kas/includehandler.py).

### Format Version Versus Tool Version

Use the [format changelog](https://kas.readthedocs.io/en/5.3/format-changelog.html) to select an appropriate declaration:
`commit`/`branch` and repository overrides arrived with format 14, `tag` with 15, and signing configuration with 19.
This history is not a complete runtime gate on each key: 5.3 validates with its installed schema and separately checks
the declared version range. A successful parse on 5.3 does not prove the file works with an older kas executable.
Keep version declarations honest and test every release for which compatibility is claimed.

## Lockfiles

For `kas-project.yml`, the adjacent lock is `kas-project.lock.yml`. kas loads locks for each processed config, including
transitive includes and colon-composed fragments. A lock's repository entries normally live in `overrides.repos`, which
are interpreted separately from the base `repos` entries. Read both when a pin appears unexpected.

```yaml
header:
  version: 14
overrides:
  repos:
    poky:
      commit: 89e6c98d92887913cadf06b2adb97f26cde4849b
```

For kas 5.3:

- `kas lock kas-project.yml` resolves repositories with existing locks in effect. It creates missing pins for floating
  managed repositories; it is not the operation for deliberately advancing an existing locked branch.
- `kas lock --update kas-project.yml` ignores locks during resolution and updates floating refs. Explicit commits still
  constrain their repositories. Revision resolution is before patches, not an arbitrary snapshot of working trees.
- The lock plugin updates existing local lockfiles that own the relevant pin. If a repository is locked only in an
  external included repository, it does not rewrite that external lock. A corresponding local lock can be updated.
  Remaining unpinned floating repositories are added to the top lock, adjacent to the first command-line config.
- Inspect every affected lockfile, checkout, and warning. External locks retained on disk can still determine the next
  normal build, even after an update resolution observed a newer revision. Validate the subsequent locked selection.
- A root repository without VCS operations, arbitrary dirty files, and repositories already pinned by explicit commits
  do not all become new lock entries. Preserve the configuration repository's revision and changes separately.

A lock refresh is a deliberate input change. Reuse authorization for that change, preserve prior lock edits, and review
the complete pin diff. Restoring a file from HEAD is safe only if HEAD is the intended previous state. See
[Lock implementation](https://github.com/siemens/kas/blob/5.3/kas/plugins/lock.py).

## Selection and Path Variables

| Variable                    | Native kas 5.3 meaning                                                      |
| --------------------------- | --------------------------------------------------------------------------- |
| `KAS_WORK_DIR`              | Existing workspace directory; default current directory                     |
| `KAS_BUILD_DIR`             | Build directory; default `KAS_WORK_DIR/build`; configured parent must exist |
| `KAS_MACHINE`, `KAS_DISTRO` | Override corresponding configuration selections                             |
| `KAS_TARGET`, `KAS_TASK`    | Override target/task; target supports space-separated values                |
| `DL_DIR`, `SSTATE_DIR`      | Download and shared-state caches passed into the build environment          |
| `KAS_REPO_REF_DIR`          | Reference repositories used for fetching/cloning; can be populated by kas   |
| `KAS_BUILDTOOLS_DIR`        | Explicit location for downloaded/installed buildtools                       |

For target/task, a supplied build CLI option wins over environment, then configuration, then the default. Do not infer
selection from YAML alone. Paths must be accessible and must not overlap, except that the data directories may be
inside `KAS_WORK_DIR`. See the release's
[environment reference](https://kas.readthedocs.io/en/5.3/command-line.html#environment-variables).

## Containers

The wrapper sets up mounts and runs kas in an OCI image; direct image and CI invocations can bypass parts of that setup.
Record the actual entry point before diagnosing. Prefer a wrapper from the same release as the image; kas 5.3 emits a
warning on a mismatch. Matching versions is a useful compatibility default, not a diagnosis by itself.

```bash
# Inspect a project-vendored wrapper's version before use
./kas-container --version
KAS_IMAGE_VERSION=5.3 ./kas-container build kas-project.yml
KAS_CONTAINER_ENGINE=podman ./kas-container build kas-project.yml
```

The default image is `ghcr.io/siemens/kas/kas:<script-version>`. `KAS_CONTAINER_IMAGE` supplies a custom full image
reference, including a digest when exact content identity matters. Since 5.0, `KAS_CONTAINER_IMAGE_DISTRO` can select
an available base such as `debian-bookworm`, yielding a `<version>-<distro>` tag. Check the release's actual image set.
Docker is preferred during engine auto-detection; `KAS_CONTAINER_ENGINE` selects Docker or Podman explicitly.
The 5.3 wrapper adds `--userns=keep-id` for Podman.

### Mounts and Ownership

| Host input             | Container path when forwarded |
| ---------------------- | ----------------------------- |
| Source repository root | `/repo`                       |
| `KAS_WORK_DIR`         | `/work`                       |
| `KAS_BUILD_DIR`        | `/build`                      |
| `DL_DIR`               | `/downloads`                  |
| `SSTATE_DIR`           | `/sstate`                     |
| `KAS_REPO_REF_DIR`     | `/repo-ref`                   |
| `KAS_BUILDTOOLS_DIR`   | `/buildtools`                 |

Paths inside `KAS_WORK_DIR` are rewritten under `/work` instead of mounted again at the fixed paths above. Unset optional
variables can leave data at kas's in-container defaults; inspect actual arguments before inferring a host path from this
table.

**A mounted cache can still be bypassed by the configuration.** kas passes `SSTATE_DIR`, `SSTATE_MIRRORS`, `DL_DIR` and
`TMPDIR` into BitBake through `BB_ENV_PASSTHROUGH_ADDITIONS` ([libkas.py](https://github.com/siemens/kas/blob/5.3/kas/libkas.py)),
so they arrive as environment. A hard `=` assignment in a `local_conf_header` outranks that, and a configuration
carrying someone else's absolute paths — a vendored fragment with CI paths is the common case — silently redirects both
caches to directories that are not mounted. Nothing errors; the build simply re-downloads and rebuilds every run and the
mounted directories stay empty.

```bash
# The only reliable check: read the generated file, not the wrapper's arguments.
rg -n 'DL_DIR|SSTATE_DIR|BB_NUMBER_THREADS' "$KAS_BUILD_DIR/conf/local.conf"
```

Override with a later-sorting `local_conf_header` entry pointing at the container-side mount paths, per the emission
order documented above. The wrapper finds the source repository root from the config file. Its default source mount
is read-only for build/checkout and writable for shell/lock; `--repo-ro` and `--repo-rw` select explicit modes.
If work and source are the same host directory, the writable `/work` mount also exposes the source through that path;
a read-only `/repo` mount alone does not isolate it from writes. Use separate directories when that distinction matters.

Represent an in-tree layer through its source repository so Git metadata remains reachable under `/repo`:

```yaml
repos:
  my-project:
    layers:
      subdir/meta-my-layer:
```

**A layer path that escapes the repository root resolves differently native versus containerised**, and the failure is
silent at checkout time. Under native kas the root repository sits inside `KAS_WORK_DIR`, so `..` reaches the workspace;
under the wrapper the root repo is mounted at `/repo`, so `..` is `/`. A configuration written for the native layout
therefore generates a `bblayers.conf` naming a directory that does not exist:

```yaml
repos:
  meta-example:
    layers:
      ../meta-example:     # resolves under native kas; becomes /meta-example in the container
```

```text
ERROR: The following layer directories do not exist:
ERROR:    /work/build/../../meta-example
```

`kas checkout` reports **success** — generating a `bblayers.conf` is not validating one — and the error surfaces later
from BitBake. Prefer paths that stay inside the repository. To repair a vendored configuration without editing it,
exclude the escaping entry and name the repository root:

```yaml
repos:
  meta-example:
    layers:
      ../meta-example: disabled    # 5.3 also accepts the deprecated spelling "excluded"
      .:
```

The entrypoint remaps `builder` and uses `gosu builder` when a nonzero `USER_ID` is supplied, as the wrapper normally
does. It skips that remapping path when `USER_ID` is absent or zero. Therefore a direct image or CI job needs its own
UID/entrypoint check; do not promise host ownership merely because the image name contains kas.

Rootless Docker requires a read-only source repository. Use a separate `KAS_WORK_DIR`; kas temporarily changes managed
directory ownership, and the host must not write managed files while kas is operating. Entrypoint cleanup restores
ownership of top-level managed directories, not a blanket recursive restoration of all content. In this mode the
wrapper defaults the source mount to read-only even for shell/lock and rejects an explicit writable source request.
Lock writes under `/repo` therefore need a different supported execution arrangement, such as an authorized native
refresh. Do not resolve that limitation by blindly changing owners or making the source writable. See
[container guidance](https://kas.readthedocs.io/en/5.3/userguide/kas-container.html) and the
[entrypoint](https://github.com/siemens/kas/blob/5.3/container-entrypoint).

Extra runtime options can be passed with `--runtime-args "--memory=8g --cpus=4"`. Inspect existing options and resource
limits; do not add privilege or host mounts as a generic fix for permission errors.

## Credentials

These are kas-container 5.3 wrapper options, placed before its subcommand:

```bash
./kas-container --ssh-agent build kas-project.yml
./kas-container --ssh-dir ~/.ssh/kas-only build kas-project.yml
./kas-container --git-credential-store /path/to/scoped-credentials build kas-project.yml
./kas-container --aws-dir /path/to/scoped-aws build kas-project.yml
./kas-container --no-proxy-from-env build kas-project.yml
```

Use dedicated directories/files that contain only credentials intended for the build. An AWS profile does not narrow
which files a supplied directory exposes: the whole SSO cache can be copied, including unrelated active sessions.
For isolation, use a dedicated directory or separate account; logging out unrelated sessions helps only if no other
sensitive material remains accessible. Do not copy actual secrets into logs or saved diagnostic output.

For native kas 5.3, when the directory beside `AWS_CONFIG_FILE` lacks `sso/cache`, credential setup can fall back to
the invoking user's `~/.aws/sso/cache`. A dedicated config file alone is therefore insufficient. Supply a dedicated
cache directory (empty if SSO is not used) or use an account without unrelated cached sessions. Verify which cache path
is selected; do not inspect or copy real credential contents merely to diagnose it.

SSH-agent forwarding exposes agent operations, even without exposing the private key files. Use it only for the intended
build's trust boundary. A credential-store file also grants its contents to the build. There is no
`--git-credential-socket` wrapper option in 5.3; do not prescribe one from another wrapper's documentation.

[Credential handling](https://kas.readthedocs.io/en/5.3/userguide/credentials.html) describes the release's supported
file/environment mechanisms. Forwarding and limiting credential authority are separate decisions.

## Cleanup and Purge

Inspect the actual resolved paths and preserve local work before authorizing deletion. kas workspace cleanup commands
are different from `bitbake -c clean/cleansstate/cleanall <recipe>`; kas's operations can affect whole caches.

| kas 5.3 operation | Removal scope                                                                                                                                          |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `clean`           | Build `tmp*` directories; ISAR layout may require privileged removal                                                                                   |
| `cleansstate`     | Clean artifacts plus contents of the environment-selected or default sstate cache                                                                      |
| `cleanall`        | Above plus contents of the environment-selected or default download cache                                                                              |
| `purge`           | Above plus build-directory contents, managed repositories and other managed paths; matching reference repos unless preserved; explicit buildtools path |

Native cleanup selects cache paths from process `SSTATE_DIR`/`DL_DIR` or defaults under the build directory. Do not
assume it evaluates arbitrary BitBake assignments in `local.conf` to discover caches. Repository `path` settings can
point outside the workspace. Explicit cache directories themselves may survive while their contents are deleted.

Preview the exact release/entry point and environment you intend to use:

```bash
kas cleanall --dry-run kas-project.yml
kas purge --dry-run --preserve-repo-refs kas-project.yml
# Through the wrapper, if that is the actual build environment:
./kas-container purge --dry-run --preserve-repo-refs kas-project.yml
```

Purge must resolve repositories to discover its targets, including on `--dry-run`; the preview suppresses deletion,
not all setup, checkout, or network activity. A fresh workspace is not guaranteed to stay empty after preview.
`--preserve-repo-refs` protects matching reference repositories only, not downloads or sstate. Establish authorization
for every shared or external path, not just `KAS_WORK_DIR`. Remove `--dry-run` only when the listed effects match the
approved deletion scope. Keep the same other flags and environment.

For rootless Docker, use the supported wrapper purge path for ownership cleanup rather than ad hoc recursive chown/rm.
If preview fails, report the unresolved targets; do not treat partial output as a complete deletion inventory.
[Cleanup implementation](https://github.com/siemens/kas/blob/5.3/kas/plugins/clean.py) owns version-specific details.

## CI and ISAR

CI may use the image directly or invoke the wrapper. Verify which entrypoint runs, its effective user, work/source
mounts, cache locations, environment, and config composition. The entrypoint's GitLab safe-directory handling requires
`CI_PROJECT_DIR` and absent `USER_ID`; setting a variable cannot help if the runner bypasses the entrypoint. Respect
runner-provided project paths instead of inventing a replacement. Use the same kas release and intended inputs locally.

Use the GitHub operations guidance for runner/workflow behavior and the shell guidance for command quoting. Keep CI
credentials scoped, use explicit minimal permissions, disable checkout credential persistence unless needed, and pin
remote actions to verified commits. Record image digests when reproducibility requires immutable image content.
This skill does not supply an unqualified copy-and-run CI template across different runner contracts.

For ISAR, `./kas-container --isar build kas-isar-project.yml` selects the `kas-isar` image. ISAR requires privileged,
rootful container execution; the wrapper can invoke a privileged executor. Confirm that this authority and the target
environment are already within the task before running it. Do not silently add privileged mode to an ordinary OE build.

## Security

Repository pins select content; they do not authenticate its publisher. kas 5.3 supports explicit Git signature
verification: define trusted keys using `signers`, enable `signed` on the repository, and set nonempty `allowed_signers`.
These keys were introduced with format 19. Depending on the scheme, dependencies include GPG/python-gnupg or Git's SSH
signature tools. Check the release's [schema and signing fields](https://kas.readthedocs.io/en/5.3/userguide/project-configuration.html).

Trust roots must come from an already trusted source, not solely from the repository being authenticated. kas checks
configured signatures before checkout, including repositories supplying includes; verification is not enabled for all
repositories by default. Wrong-signer and unsigned cases must reject under the intended policy. Tags are mutable: use
appropriate commit constraints as well as authentication. A valid signature identifies an authorized signer; it does
not make build recipes safe to execute with unrelated credentials or privileges.

## Reproduction Evidence

Record the exact config composition, its source repository revision and local changes, applicable locks, explicit pins,
patches, kas version, image digest/base, relevant environment, and downstream recipe source inputs. A lockfile alone
does not capture all of these. OCI images reduce host package variation but share kernel/runtime constraints and
purposefully receive mounts, user settings, and credentials.

Normal kas setup rewrites `local.conf` and `bblayers.conf`; make durable changes in the owning YAML. Setup-skip options
can preserve existing config. Neither behavior means every build-directory file is recoverable output: inspect local
work before cleanup. Verify release artifact reproduction separately, using the Yocto/OE skill for build-system inputs.
