# Dev Containers

## Run a Slim Image as a Dev Container

A Microsoft `devcontainers` base image carries the user, shell, Git, and Python tooling that VS Code expects. A slim
distribution base lacks them. Add them as features in `devcontainer.json` rather than in the Dockerfile, so the
production stages stay free of them:

```json
"features": {
  "ghcr.io/devcontainers/features/common-utils:2": {
    "installZsh": true, "username": "vscode", "userUid": "1000", "userGid": "1000"
  },
  "ghcr.io/devcontainers/features/git:1": {}
}
```

Leave out the `python` feature when the image brings its own interpreter. With `"version": "none"` it installs no
Python, but it still installs pipx and a fixed tool set (flake8, black, mypy, pytest, and others), which can outweigh
`common-utils`. List the tools the team uses in the image's development requirements instead, so they install into the
same environment at pinned versions. The `git` feature adds little after `common-utils`, which already installs Git.

Point `customizations.vscode.settings."python.defaultInterpreterPath"` at the image's virtual environment interpreter.

Under rootful Docker with `"remoteUser": "root"`, Python writes root-owned `__pycache__`, `.pytest_cache`, and
`.mypy_cache` directories into the bind-mounted checkout. `"containerEnv": { "PYTHONDONTWRITEBYTECODE": "1" }` stops
the `__pycache__` part. A non-root `remoteUser` fixes the cause where the workload's device access permits it. Rootless
Podman maps container root to the host user, so it does not have the problem.

## Test With the Dev Containers CLI

`devcontainer up --workspace-folder .`, from the npm package `@devcontainers/cli`, does what VS Code does. It builds
the target, adds the features in a second build, and starts the container. Verify the result inside the container with
`devcontainer exec`: run `uname -m`, `id vscode`, and `command -v zsh git python`, then the application's entry point.

### Podman

- The CLI runs `docker buildx version`. Podman and `podman-docker` answer with buildah's version, so the CLI installs
  features with BuildKit-style bind mounts under `/tmp`. buildah then saves `/tmp` as `0755` instead of `1777`
  ([buildah issue 6503](https://github.com/podman-container-tools/buildah/issues/6503)), and apt in a later feature
  fails with `Couldn't create temporary file /tmp/apt.conf.XXXXXX`. From a terminal, pass
  `--docker-path podman --buildkit never`.
- The CLI passes `build.options` from `devcontainer.json`, such as `--platform`, to the main image build only, not to
  the helper build that packages the features. A foreign-architecture build therefore gets a host-architecture helper
  image, which fails to resolve the short name `dev_container_feature_content_temp`.

A wrapper fixes both. Point `--docker-path`, or VS Code's `dev.containers.dockerPath` setting, at it, and set
`DEVCONTAINER_TEST_PLATFORM=linux/<arch>` for a foreign architecture. This wrapper ran from a terminal with Podman
5.7.0 and Dev Containers CLI 0.91.0, not from VS Code:

```sh
#!/bin/sh
# Fail only `buildx version`, so the CLI installs features without BuildKit.
if [ "${1-}" = "buildx" ] && [ "${2-}" = "version" ]; then
  exit 1
fi
# Give every build the target platform, the feature helper build included.
if [ "${1-}" = "build" ] && [ -n "${DEVCONTAINER_TEST_PLATFORM-}" ]; then
  shift
  exec podman build --platform="${DEVCONTAINER_TEST_PLATFORM}" "$@"
fi
exec podman "$@"
```

### Docker

The CLI needs no workaround and returns once the container starts. For a foreign architecture, run
`DOCKER_DEFAULT_PLATFORM=linux/<arch> devcontainer up --workspace-folder .`, which covers both builds, and add
`"--platform=linux/<arch>"` to `runArgs`.
