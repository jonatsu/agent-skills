# Attributions

## Current Skill

- Skill: `docker-podman-containers`, named `containers` until 2026-09-28
- Current author: Joonas Onatsu
- Current license: MIT
- Status: original expression informed by external idea sources

## Idea Sources

### github/awesome-copilot

- Source: <https://github.com/github/awesome-copilot>
- Revision: `ce15839f4e82d128f80cc1731e9ee5a4449895fa`
- Path: `instructions/containerization-docker-best-practices.instructions.md`
- License: MIT

This source prompted guidance about immutable container replacement, cache-aware Dockerfile ordering, bounded runtime
logging, and recurring vulnerability evaluation. All expression is original and was checked against current official
Docker documentation; no upstream prose, code, examples, identifiers, data, or assets were copied or adapted.

### cogini/phoenix_container_example

- Source: <https://github.com/cogini/phoenix_container_example>
- Revision: `0d4a50357a2a745b9ac78e8495a3f3554dab151a`
- Path: `deploy/debian.Dockerfile`
- Author: the `cogini` GitHub organization
- License: none found; the repository carries no license file at this revision

This source prompted the apt cache-mount recipe in `references/apt-cache-mounts.md`, together with its snapshot
archive pinning. It also prompted the shared operating-system dependency stage, minimum-input copies, and `ARG`
placement in `references/build-cache.md`. In `references/dockerfile-patterns.md` it prompted the `FROM scratch`
artifact stage, `WORKDIR` before `USER`, `COPY --chown` in place of a later `chown`, and SSH mounts for private
dependencies. Because the source has no license, only ideas were taken. All
expression and every example are original, and no upstream code, comments, or identifiers were copied.

## Verification Sources

Verification sources establish public facts and are cited near the affected claims. Under this repository's
provenance policy, verification-only use creates no attribution obligation; they are listed here for traceability.

- Fedora Project Wiki, [`Changes/Podman6`](https://fedoraproject.org/wiki/Changes/Podman6) (read 2026-09-28,
  revision `oldid=764440`) — the Podman 6.0 removal of slirp4netns, cgroups v1, and BoltDB, the netavark iptables
  removal, and the `containers.conf`/`storage.conf` rework cited in `references/podman-differences.md`.
- Docker documentation (read 2026-10-04): the
  [build cache pages](https://docs.docker.com/build/cache/) (optimize, invalidation, backends and their
  subpages, garbage collection), the [Dockerfile reference](https://docs.docker.com/reference/dockerfile/) for
  cache mounts, `COPY --link`, and `ARG` cache behavior, and the
  [GitHub Actions cache page](https://docs.docker.com/build/ci/github-actions/cache/) on cache mounts in CI.
  These are cited in `references/build-cache.md` and `references/apt-cache-mounts.md`.
- Buildah man pages `buildah-run(1)`, `buildah-build(1)`, `buildah-copy(1)`, and `buildah-prune(1)`, and the
  [Buildah release notes](https://buildah.io/releases/) (read 2026-10-04), for the Buildah cache support stated in
  `references/build-cache.md`.
- debuerreotype
  [`debuerreotype-minimizing-config`](https://github.com/debuerreotype/debuerreotype/blob/master/scripts/debuerreotype-minimizing-config)
  for the `docker-clean` behavior, and [apt(8)](https://manpages.debian.org/unstable/apt/apt.8.en.html) on
  script use (read 2026-10-04).
