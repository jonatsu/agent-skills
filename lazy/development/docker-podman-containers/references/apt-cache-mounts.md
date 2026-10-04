# Apt Cache Mounts on Debian and Ubuntu Images

Read `build-cache.md` first; this covers only what apt adds to its cache-mount rules.

## The Image Empties the Cache

The official Debian image ships `/etc/apt/apt.conf.d/docker-clean`. It deletes downloaded `.deb` files after
every `dpkg` run and every `apt-get update`, and it disables apt's binary package caches. With that file in
place, a cache mount on `/var/cache/apt` is emptied at the end of every install and saves nothing. This common
pattern looks cached and is not:

```dockerfile
RUN --mount=type=cache,target=/var/cache/apt \
    apt update && apt install -y gcc
```

Inspect the base image before relying on a cache mount, because derived and Ubuntu images vary:

```bash
docker run --rm <base-image> ls /etc/apt/apt.conf.d
```

## Recipe

```dockerfile
# syntax=docker/dockerfile:1
FROM debian:<release>-slim AS os-deps

RUN rm -f /etc/apt/apt.conf.d/docker-clean \
 && echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' \
      > /etc/apt/apt.conf.d/keep-cache

RUN --mount=type=cache,id=apt-cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,id=apt-lists,target=/var/lib/apt,sharing=locked \
    apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      build-essential ca-certificates
```

Each part prevents a specific failure:

- Removing `docker-clean` and setting `Keep-Downloaded-Packages` in their own earlier step keeps downloaded
  packages in the mount. Repeat this step in every stage that starts from a fresh base image.
- Mounting both `/var/cache/apt` (packages) and `/var/lib/apt` (package lists) caches the download and the index.
- `sharing=locked` makes concurrent builds wait for each other, because apt needs exclusive access to its data
  and the default `shared` mode lets parallel builds use the same files at once.
- Reusing the same `id` values in every stage and Dockerfile lets all of them share one cache.
- `apt-get` keeps a stable command line for scripts, where `apt` may change behavior between versions.
- `DEBIAN_FRONTEND=noninteractive` on the command, rather than as an `ENV`, keeps it out of the final image.
- `--no-install-recommends` skips recommended packages, so the image gets only the named packages and their
  required dependencies.
- Keep `apt-get update` in the same `RUN` as the install. The cached lists only make the refresh cheaper; without
  it, the install can request package versions the mirror no longer serves.

Leave out `apt-get clean` and `rm -rf /var/lib/apt/lists/*` in a cache-mounted step. Both directories are mounts,
so their contents never reach the image, and deleting them discards the cache. Keep that cleanup only in steps
that run without the mounts.

## Repeatable Package Versions

The cache key of an apt step is its command text, so a rebuild on a new builder installs whatever the mirror
serves that day while a cached builder keeps the old versions. To make Debian builds install the same versions
everywhere, point the sources at a dated `snapshot.debian.org` archive and pass the date as an `ARG` declared
just before that step. Snapshot archives need `[check-valid-until=no]`, because their release files expire.
Changing the date then becomes the explicit way to take package updates.
