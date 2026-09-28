# Attributions

## Current Skill

- Skill: `docker-podman-containers`, named `containers` until 2026-09-28
- Current author: Joonas Onatsu
- Current license: MIT
- Status: original expression informed by an external idea source

## Idea Sources

### github/awesome-copilot

- Source: <https://github.com/github/awesome-copilot>
- Revision: `ce15839f4e82d128f80cc1731e9ee5a4449895fa`
- Path: `instructions/containerization-docker-best-practices.instructions.md`
- License: MIT

This source prompted guidance about immutable container replacement, cache-aware Dockerfile ordering, bounded runtime
logging, and recurring vulnerability evaluation. All expression is original and was checked against current official
Docker documentation; no upstream prose, code, examples, identifiers, data, or assets were copied or adapted.

## Verification Sources

Verification sources establish public facts and are cited near the affected claims. Under this repository's
provenance policy, verification-only use creates no attribution obligation; they are listed here for traceability.

- Fedora Project Wiki, [`Changes/Podman6`](https://fedoraproject.org/wiki/Changes/Podman6) (read 2026-09-28,
  revision `oldid=764440`) — the Podman 6.0 removal of slirp4netns, cgroups v1, and BoltDB, the netavark iptables
  removal, and the `containers.conf`/`storage.conf` rework cited in `references/podman-differences.md`.
