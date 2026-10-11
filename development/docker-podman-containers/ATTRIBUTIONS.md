# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## First-party Sources

### Docker: Docker documentation

- Source: <https://docs.docker.com/build/cache/>, <https://docs.docker.com/reference/dockerfile/>, and
  <https://docs.docker.com/build/ci/github-actions/cache/>; content repository <https://github.com/docker/docs>
- License: `Apache-2.0`
- Version: read 2026-10-04

The build-cache and apt cache-mount guidance is built on the cache pages (optimization, invalidation, storage
backends, garbage collection), the Dockerfile reference for cache mounts, `COPY --link`, and `ARG` cache behavior,
and the CI cache page. Facts are restated in original words; nothing was copied.

## Third-party Sources

### GitHub: awesome-copilot

- Source: <https://github.com/github/awesome-copilot>,
  `instructions/containerization-docker-best-practices.instructions.md`
- License: `MIT`
- Version: `ce15839f4e82d128f80cc1731e9ee5a4449895fa`

The instructions supplied the subjects of immutable container replacement, cache-aware Dockerfile ordering, bounded
runtime logging, and recurring vulnerability evaluation. Nothing was copied.

### cogini: phoenix_container_example

- Source: <https://github.com/cogini/phoenix_container_example>, `deploy/debian.Dockerfile`
- License: `LicenseRef-No-License`
- Version: `0d4a50357a2a745b9ac78e8495a3f3554dab151a`

The repository declares no license, so all rights remain with its author. The Dockerfile supplied the ideas behind the
apt cache-mount recipe with snapshot archive pinning in `references/apt-cache-mounts.md`, the shared dependency stage
and `ARG` placement in `references/build-cache.md`, and the `FROM scratch` artifact stage, `COPY --chown`, and SSH
mounts in `references/dockerfile-patterns.md`. Nothing was copied.
