# kas — Command and Configuration Reference

kas is a setup tool for Yocto/OpenEmbedded and other BitBake-based projects. It replaces the manual "clone these layers,
hand-edit `bblayers.conf`, tweak `local.conf`" workflow with a single versioned YAML configuration file, then optionally
drives the build. This reference is the full command and schema detail behind `SKILL.md`; pull the section you need on
demand.

## Contents

- [What kas does](#what-kas-does)
- [Installation](#installation)
- [Core commands](#core-commands)
- [`kas dump` — the flattened config](#kas-dump--the-flattened-config)
- [Configuration file structure](#configuration-file-structure)
- [Configuration composition (includes)](#configuration-composition-includes)
- [Lockfiles](#lockfiles)
- [Excluding layers](#excluding-layers)
- [Environment variables](#environment-variables)
- [Container builds (`kas-container`)](#container-builds-kas-container)
  - [Script and image version match](#script-and-image-version-match)
  - [Container image selection](#container-image-selection)
  - [Container engine](#container-engine)
  - [Directory mounts](#directory-mounts)
  - [Credential forwarding](#credential-forwarding)
  - [Additional runtime arguments](#additional-runtime-arguments)
  - [What `container-entrypoint` does](#what-container-entrypoint-does)
  - [Cleanup and purge](#cleanup-and-purge)
- [CI usage](#ci-usage)
- [ISAR builds](#isar-builds)
- [kas vs manual setup](#kas-vs-manual-setup)
- [Security](#security)

## What kas does

1. Clones every BitBake layer and checks each out at the commit the config pins.
2. Generates `bblayers.conf` and `local.conf` from that config.
3. Launches a minimal, controlled build environment, which limits host contamination.
4. Optionally invokes BitBake to run the build.

Everything kas produces in the build directory is regenerated from the config on the next run. Treat the YAML as the
source of truth and the build dir as disposable output.

## Installation

```bash
# Recommended: isolated install via pipx
pipx install kas

# Debian/Ubuntu system package (may lag upstream)
sudo apt install kas
```

## Core commands

```bash
# Clone all layers, set up the environment, and build the default target
kas build kas-project.yml

# Clone and set up only — no build. Inspect the checkout before committing to one.
kas checkout kas-project.yml

# Print the fully merged, includes-resolved config (ground truth for debugging)
kas dump kas-project.yml

# Drop into the BitBake shell environment to run arbitrary bitbake commands
kas shell kas-project.yml -c 'bitbake core-image-minimal'
kas shell kas-project.yml -c 'bitbake -c devshell myrecipe'

# Interactive, menuconfig-style configuration
kas menu kas-project.yml

# Pin every repo to its current commit (write/refresh a lockfile)
kas lock kas-project.yml

# Show differences between the current and the locked state
kas diff kas-project.yml

# Build a specific target
kas build kas-project.yml --target core-image-minimal

# Run a specific BitBake task
kas build kas-project.yml --target myrecipe --cmd compile

# Compose configs on the command line (same effect as includes in the file)
kas build kas-base.yml:debug-image.yml:board.yml

# Clean build artifacts (see Cleanup and purge for the destructive variants)
kas clean kas-project.yml
kas cleansstate kas-project.yml   # also empties the sstate cache
kas cleanall kas-project.yml      # also removes downloads
```

## `kas dump` — the flattened config

`kas dump` resolves every include, applies the merge order, folds in any auto-loaded lockfile, and prints the single
effective config that kas will actually build from. It is read-only. Reach for it first whenever an override, pin,
machine, or distro value is not behaving as the file in front of you suggests.

```bash
# Human-readable YAML of the merged config
kas dump kas-project.yml

# Dump the exact command-line composition you build
kas dump kas-base.yml:board.yml:debug-image.yml

# Machine-readable, for scripting or diffing
kas dump --format json kas-project.yml

# Replace floating branch/tag refs with the exact commit hashes they resolve to
kas dump --resolve-refs kas-project.yml

# Write/refresh a lockfile from the resolved refs
kas dump --lock --update --inplace kas-project.yml
```

- `--format {yaml,json}` selects the output format (`yaml` by default).
- `--resolve-refs` pins each floating ref to its concrete commit in the output.
- `--lock` emits lockfile-shaped output; combine with `--update` to advance refs to their latest commit and `--inplace`
  to overwrite the `.lock` file next to the config.

When the dump disagrees with the config you were handed, the include/override chain or an auto-loaded lockfile is the
real story. Trust the dump.

## Configuration file structure

kas configs are YAML (JSON also works). The minimal fields are `header`, `machine`, `distro`, and `repos`.

```yaml
# kas-project.yml
header:
  version: 14          # config format version — always required
machine: raspberrypi4-64
distro: poky

repos:
  # The repo this config lives in — include it in bblayers with an empty entry
  meta-custom:

  # External layer — cloned and checked out at the pinned commit
  poky:
    url: "https://git.yoctoproject.org/git/poky"
    commit: 89e6c98d92887913cadf06b2adb97f26cde4849b
    layers:
      meta:
      meta-poky:
      meta-yocto-bsp:

  meta-openembedded:
    url: "https://git.openembedded.org/meta-openembedded"
    commit: d1a58c8c71ef3e8f327ed5a5671af6cc3f9cde00
    layers:
      meta-oe:
      meta-python:

# Additions to local.conf. Named keys let includes override or append per key.
local_conf_header:
  meta-custom: |
    BB_NUMBER_THREADS = "8"
    PARALLEL_MAKE = "-j8"
    IMAGE_INSTALL:append = " strace gdbserver"

# Additions to bblayers.conf (rarely needed)
bblayers_conf_header:
  meta-custom: |
    POKY_BBLAYERS_CONF_VERSION = "2"
```

`header.version` is the schema format number, an integer. Key semantics are gated on it, so do not use a key the
declared version predates, and do not bump it casually.

## Configuration composition (includes)

Split a build into composable fragments — base, BSP, product, image — and compose them.

```yaml
# kas-product-a.yml
header:
  version: 14
  includes:
    - kas-base.yml          # poky + common layers + local_conf_header
    - kas-bsp-myboard.yml   # BSP layer + MACHINE setting
    - kas-debug-image.yml   # debug packages added to IMAGE_INSTALL
```

Or compose on the command line without writing a combined file. The two forms are equivalent:

```bash
kas build kas-base.yml:kas-bsp-myboard.yml:kas-debug-image.yml
```

Pull an include from another repository:

```yaml
header:
  version: 14
  includes:
    - repo: meta-bsp-collection
      file: hw1/kas-hw-bsp1.yml
repos:
  meta-bsp-collection:
    url: "https://www.example.com/git/meta-bsp-collection"
    commit: 3f786850e387550fdab836ed7e6dc881de23001b
```

**Merge order is the mechanism, not a detail.** Includes merge top-to-bottom; a later entry overrides an earlier one,
and the current file's own values override every include. Debugging an override without knowing the order is guessing —
dump the config and read the result.

## Lockfiles

A lockfile pins every repo to an exact commit for a fully reproducible build. kas auto-loads `<config>.lock.<ext>`
whenever it sits next to the config, so a checkout at an "unexpected" commit is usually the lockfile doing its job, not
a bug.

```yaml
# kas-project.lock.yml — auto-loaded when kas-project.yml is used
header:
  version: 14
overrides:
  repos:
    poky:
      commit: 89e6c98d92887913cadf06b2adb97f26cde4849b
    meta-openembedded:
      commit: d1a58c8c71ef3e8f327ed5a5671af6cc3f9cde00
```

Generate or refresh a lockfile from the current checkouts:

```bash
kas lock kas-project.yml
# or, equivalently, via dump:
kas dump --lock --update --inplace kas-project.yml
```

To move to newer commits, update the lockfile deliberately rather than editing around it.

## Excluding layers

Mark a layer excluded to drop it from a combined configuration:

```yaml
repos:
  poky:
    url: "https://git.yoctoproject.org/git/poky"
    commit: abc123
    layers:
      meta-yocto-bsp: excluded   # do not add to bblayers.conf
```

## Environment variables

| Variable        | Description                                            |
| --------------- | ------------------------------------------------------ |
| `KAS_WORK_DIR`  | Working directory for kas (default: current directory) |
| `KAS_BUILD_DIR` | Build directory (default: `KAS_WORK_DIR/build`)        |
| `KAS_MACHINE`   | Overrides `machine` from the config                    |
| `KAS_DISTRO`    | Overrides `distro` from the config                     |
| `KAS_TARGET`    | Overrides `target`; space-separated for several        |
| `KAS_TASK`      | Overrides `task`                                       |

Precedence for the selection variables is CLI flag (`kas build --target`), then environment, then the config value, then
the schema default. The defaults are `qemux86-64` / `nodistro` / `core-image-minimal`, so a config that omits `machine`,
`distro` or `target` builds something plausible-looking rather than failing.

`kas dump` renders the merged **config files** and does not apply these overrides, so it cannot show which variant an
environment-selected build will actually produce. Where `dump` must stay truthful, keep the selection in files and
compose them (`base.yml:variant/debug.yml`) instead.

Container builds honour several more; see [Directory mounts](#directory-mounts).

## Container builds (`kas-container`)

`kas-container` is a shell-script wrapper that runs `kas` inside an OCI container. It is the recommended way to build,
because:

- The build environment is fully decoupled from the host.
- All build dependencies are pinned inside the image.
- Developers on different hosts get identical environments.
- CI and local builds share one image.

### Script and image version match

The `kas-container` script version MUST match the `kas` version inside the image. Download the script from the same
release tag as the image you intend to use; a mismatch causes subtle mount and entrypoint failures.

```bash
# Download the kas-container script pinned to a release
curl -fsSL https://raw.githubusercontent.com/siemens/kas/5.3/kas-container \
    -o kas-container
chmod +x kas-container

# Confirm the version
./kas-container --version
```

Vendoring the script into your own repo and updating it alongside `KAS_IMAGE_VERSION` keeps the two in lockstep.

### Container image selection

By default `kas-container` uses `ghcr.io/siemens/kas/kas:<version>`.

```bash
# Default: image auto-resolved to the script version
./kas-container build kas-project.yml

# Pin an explicit image version
KAS_IMAGE_VERSION=5.3 ./kas-container build kas-project.yml

# Distribution-specific image (kas >= 5.0): debian-bookworm, debian-trixie
KAS_CONTAINER_IMAGE_DISTRO=debian-bookworm \
    ./kas-container build kas-project.yml
# Resolves to ghcr.io/siemens/kas/kas:5.3-debian-bookworm

# A fully custom image
KAS_CONTAINER_IMAGE=myregistry/my-kas:latest \
    ./kas-container build kas-project.yml
```

### Container engine

`kas-container` auto-detects Docker or Podman. Force one explicitly:

```bash
KAS_CONTAINER_ENGINE=podman ./kas-container build kas-project.yml
KAS_CONTAINER_ENGINE=docker ./kas-container build kas-project.yml
```

For Podman it adds `--userns=keep-id` automatically so the container runs with your UID and file ownership on mounts
stays consistent.

### Directory mounts

`kas-container` mounts host directories into the container at fixed paths. Set these variables to control where data
lands on the host:

| Host variable                 | Container path | Notes                                       |
| ----------------------------- | -------------- | ------------------------------------------- |
| `KAS_WORK_DIR` (default: CWD) | `/work`        | Working dir; kas-managed repos land here    |
| `KAS_BUILD_DIR`               | `/build`       | BitBake build directory; created if absent  |
| `DL_DIR`                      | `/downloads`   | Download cache; created if absent           |
| `SSTATE_DIR`                  | `/sstate`      | Shared state cache; created if absent       |
| `KAS_REPO_REF_DIR`            | `/repo-ref`    | Git reference repo for faster cloning       |
| `KAS_BUILDTOOLS_DIR`          | `/buildtools`  | Yocto buildtools archive; created if absent |

Share `DL_DIR` and `SSTATE_DIR` across projects to skip re-downloading and re-building:

```bash
export DL_DIR=/mnt/yocto-cache/downloads
export SSTATE_DIR=/mnt/yocto-cache/sstate
export KAS_WORK_DIR=$HOME/kas-builds/my-project
./kas-container build kas-project.yml
```

The source repo is mounted at `/repo` — read-only for `build` and `checkout`, read-write for `shell` and `lock`.
Override with `--repo-ro` or `--repo-rw`. kas-container finds it by running `git rev-parse --show-toplevel` on the
config file's directory, so `/repo` is the repository root even when the config sits in a subdirectory.

That distinction matters for in-tree layers. A layer reached through `/work` has no `.git` above it when the work dir is
a subdirectory of the repository, so `image-buildinfo` records `<unknown>` for it while every fetched layer reports a
revision. Declaring the layer through its own repository puts it under `/repo`, where git works:

```yaml
repos:
  # No url and no path: the repository containing this config file.
  # `layers:` paths are relative to that repository's root.
  my-project:
    layers:
      subdir/meta-my-layer:
```

### Credential forwarding

```bash
# Forward the SSH agent (private layer repos)
./kas-container --ssh-agent build kas-project.yml

# Mount a specific SSH config dir — avoid $HOME/.ssh, which exposes every key
./kas-container --ssh-dir ~/.ssh/kas-only build kas-project.yml

# Git credential store
./kas-container --git-credential-store ~/.git-credentials build kas-project.yml

# Git credential cache socket
./kas-container --git-credential-socket /tmp/git-credential.socket build kas-project.yml

# AWS CLI config (private S3 sstate mirrors)
./kas-container --aws-dir ~/.aws build kas-project.yml

# Block host proxy settings from being inherited
./kas-container --no-proxy-from-env build kas-project.yml
```

Forwarding `--ssh-dir ~/.ssh` or `--aws-dir ~/.aws` wholesale exposes every key and active SSO session to the build.
`--aws-dir ~/.aws` copies the whole `~/.aws/sso/cache` into the workspace. Use a dedicated directory (`~/.ssh/kas-only`)
or a scoped AWS profile, and log out of unrelated profiles first.

### Additional runtime arguments

Pass extra arguments straight to the container engine:

```bash
./kas-container --runtime-args "--memory=8g --cpus=4" build kas-project.yml
```

### What `container-entrypoint` does

`container-entrypoint` is the entrypoint baked into the image. You never invoke it directly; its key behaviours are
worth knowing when a container build fails on ownership or credentials:

- Reads `USER_ID`/`GROUP_ID` (set by `kas-container` from `id -u`/`id -g`) and remaps the internal `builder` user to
  your host UID/GID, so files written to mounts are owned by your host user.
- Copies SSH config from `/var/kas/userdata/.ssh` into the builder's home.
- Syncs the container timezone to the host (`KAS_HOST_TZ`).
- Runs `kas` via `gosu builder`, so the build has your UID rather than root.
- Under rootless Docker (which cannot use `--userns=keep-id`), restores directory ownership after the build.
- On GitLab CI, marks `CI_PROJECT_DIR` as a safe git directory to work around runner ownership mismatches.

### Cleanup and purge

```bash
# Build artifacts only (keep sstate and downloads)
./kas-container clean kas-project.yml

# Build artifacts and the sstate cache
./kas-container cleansstate kas-project.yml

# Build artifacts, sstate, and downloads
./kas-container cleanall kas-project.yml

# ALL kas-managed data (build dir + managed repos), and restore directory
# ownership so the host can delete the tree
./kas-container purge kas-project.yml

# Preview what purge would remove — run this first
./kas-container purge --dry-run kas-project.yml
```

`purge` is the correct way to fully remove a kas workspace, especially under rootless Docker where directory ownership
must be restored before the host can delete the directories. It also removes the managed repos, so any uncommitted work
in a managed layer is lost — preview with `--dry-run` and confirm the work dir first.

## CI usage

Reference the image directly in CI configuration:

```yaml
# GitHub Actions
jobs:
  build:
    runs-on: ubuntu-latest
    container:
      image: ghcr.io/siemens/kas/kas:5.3
    steps:
      - uses: actions/checkout@v4
      - run: kas build kas-project.yml
```

```yaml
# GitLab CI
build:
  image: ghcr.io/siemens/kas/kas:5.3
  script:
    - kas build kas-project.yml
```

On GitLab CI, set `CI_PROJECT_DIR`; `container-entrypoint` uses it to configure `safe.directory` automatically.

## ISAR builds

For ISAR (Debian-based embedded) images, use the `kas-isar` image:

```bash
./kas-container --isar build kas-isar-project.yml
# Uses ghcr.io/siemens/kas/kas-isar:<version>
```

ISAR requires privileged container execution and does not work under rootless Docker.

## kas vs manual setup

| Situation                                            | Recommendation                                          |
| ---------------------------------------------------- | ------------------------------------------------------- |
| New project, multiple developers                     | kas — reproducible environment in one file              |
| Existing project with an established README workflow | Either; kas is a drop-in for `source oe-init-build-env` |
| CI/CD with a layer-pinning requirement               | kas — lockfiles and container support built in          |
| Quick single-layer experiment                        | Manual setup may be simpler for a one-off               |

## Security

kas does not validate the integrity of fetched repositories. Pull only from trusted sources, pin commits, use lockfiles,
and consider GPG signing for supply-chain security in production builds.
