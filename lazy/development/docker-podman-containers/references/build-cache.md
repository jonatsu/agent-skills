# Build Cache

Make rebuilds reuse work. A cache miss on one step rebuilds that step and every step after it, so the layout of
the Dockerfile decides how much each change costs. Written for BuildKit; the last section covers Buildah.

## How a Step Hits or Misses

- `COPY`, `ADD`, and `RUN --mount=type=bind` hit when the content and metadata of every input file match. File
  modification time is ignored, so a fresh checkout alone does not miss.
- Every other `RUN` hits on its command text alone. The builder never looks at what the command would fetch, so
  `RUN apt-get update` stays cached indefinitely and installs the same package versions a week later.
- A changed `ARG` value misses at the first step that uses it, not at its declaration, and every `RUN` after an
  `ARG` uses it implicitly. Declare each `ARG` immediately before the step that needs it, so a changed build
  number or version does not rebuild the stages before it.
- A changed secret value does not miss, because secret contents are not part of the cache key. When a step must
  rerun after a secret rotates, pass a cache-busting `ARG` beside the secret and change both together.
- `SOURCE_DATE_EPOCH` participates in `WORKDIR` cache keys. Set it from a commit timestamp only when
  provenance needs it; a fixed value such as `0` keeps reproducible builds cacheable.

To rerun steps on purpose, rebuild one stage with `--no-cache-filter <stage>` rather than the whole build with
`--no-cache`.

## Layout

Order steps from least to most frequently changing. Copy dependency manifests and lock files, install
dependencies, compile dependencies when the toolchain can do that apart from the application, then copy the
application source. Copy each step's minimum inputs: the configuration files that dependency compilation reads,
not the whole `config/` directory.

Build the operating-system dependencies once in a shared stage, and start the test, production, and development
targets from it, so all of them reuse one cached copy.

Use `COPY --link` for files that do not depend on earlier layers. A linked layer survives changes to the steps
before it, and the image can be rebased onto an updated base image without rerunning the build. A linked copy
cannot read files from the previous state.

Keep the build context small with `.dockerignore`; see `dockerfile-patterns.md`. A broad `COPY . .` makes every
file in the context a cache input, so an unrelated file change rebuilds everything after it.

Mount input that only produces an artifact, rather than copying it: `RUN --mount=type=bind,target=. make`. A bind
mount adds no layer to the cache. It is read-only by default, writes made with `rw` are discarded when the step
ends, and the output must go outside the mount target.

## Cache Mounts

A cache mount is a directory that persists across builds on the same builder, so a step that does miss still
reuses downloads and compiler output: `RUN --mount=type=cache,target=<dir> <command>`. It is the main lever for
package-manager and compiler steps.

- Mount the directory the tool actually uses. Ask the tool rather than guessing: `npm config get cache`,
  `yarn cache dir`, `pip cache dir`, `go env GOCACHE GOMODCACHE`. A mount on the wrong path is an empty
  directory that changes nothing, and it fails silently.
- Use `sharing=locked` for tools that need exclusive access to their data, such as apt; concurrent builds then
  wait for each other. The default `shared` lets writers run at once.
- Give the mount an `id` when several stages or Dockerfiles should share one cache. The `id` defaults to the
  target path.
- Leave the mounted directory intact. Its contents never enter the image layer, so cleaning it saves no image
  space and discards the cache.
- Make the build succeed with an empty cache. Another build may overwrite the files, and garbage collection
  removes cache mounts unused for 48 hours by default.

Cache mounts stay on the builder. `--cache-to` exports layers, not cache mount contents, so on ephemeral CI
runners every mount starts empty. Carrying them between CI runs needs a separate workaround, such as
`reproducible-containers/buildkit-cache-dance` on GitHub Actions.

For Debian and Ubuntu base images, read `apt-cache-mounts.md` before mounting the apt cache: the official image
configuration empties it after every install.

## External Cache

The builder's local cache disappears with the builder. Export it with `--cache-to` and import it with
`--cache-from` when builders are ephemeral, which is the CI case.

| Backend    | Choose it when                                                                              |
| ---------- | ------------------------------------------------------------------------------------------- |
| `registry` | The default choice: cache lives in its own image reference, apart from the output           |
| `inline`   | A single-stage image pushed to a registry; it caches only layers that reach the image       |
| `gha`      | Building in GitHub Actions within its cache size limits                                     |
| `local`    | Testing, or a self-managed shared directory                                                 |
| `s3`       | Check the backend page first: the Docker docs listed it as unreleased when this was written |
| `azblob`   | Check the backend page first: the Docker docs listed it as unreleased when this was written |

- Export with `mode=max` to cache intermediate stages too. The default `min` caches only the layers in the
  final image, which misses most of a multi-stage build.
- Each export overwrites its location. Give each branch its own cache reference, and import both the branch
  cache and the main branch cache.
- For `gha`, set a distinct `scope` per image; the shared default scope keeps only the last build's cache.
- A `local` cache directory grows with every export until one runs with `reset=true`.
- With the default `docker` driver, the `inline`, `registry`, `gha`, and `local` backends need the containerd
  image store, and the others need a different build driver. Check `docker buildx ls` for the active driver.
- Registries without OCI image index support, such as Amazon ECR, need `image-manifest=true`; check whether the
  installed BuildKit already defaults to it.

Trust rules for cache written by untrusted branches are in `ci-cd.md`.

## Garbage Collection

The builder prunes its own cache periodically. The defaults drop cache mounts and local contexts unused for 48
hours, anything unused for 60 days, then whatever exceeds the size limit. When cache keeps disappearing, raise
the limit: `builder.gc.defaultKeepStorage` in `daemon.json` for the default `docker` driver, or the
`reservedSpace`, `maxUsedSpace`, and `minFreeSpace` settings in `buildkitd.toml` for other builders.
`docker builder prune` and `docker buildx prune` delete cache, so they need explicit authority like any other
prune.

## Podman and Buildah

Buildah, which `podman build` uses, supports `RUN --mount=type=cache` with `id` and `sharing`, persists the cache
across builds per user, and clears it with `buildah prune`. It also supports `COPY --link` and `ssh` and
`secret` mounts. Its `--cache-from` and `--cache-to` take only a registry repository, store intermediate images
rather than a BuildKit cache manifest, and are ignored without `--layers`. The BuildKit backends, `mode`, and the
garbage-collection settings above do not apply.

## Validate

The change is done when the cache behaves as designed, observed rather than assumed:

1. Build twice with `--progress=plain`, and confirm that every step reports `CACHED` on the second build.
2. Change one application source file, rebuild, and confirm that only the steps from its `COPY` onward rerun.
3. For a cache mount, force the step to rerun with `--no-cache-filter <stage>`, and confirm that it reuses
   cached packages or build output instead of downloading or compiling them again.
4. For an external cache, build on a fresh builder with only `--cache-from`, and confirm the expected steps hit.
