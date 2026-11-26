# Dockerfiles and Builds

Design the image around the target workload and build context.

## Inspect Before Building

Read the Dockerfile, referenced scripts, ignore file, and relevant lock files. A build executes project-controlled
commands and can access the build context, network, caches, and explicitly mounted secrets. Do not build untrusted input
as a substitute for reviewing it.

Keep sensitive files outside the context where practical. Use `.dockerignore` to exclude repository metadata, local
credentials, environment files, editor state, test artifacts, and dependency directories that the build does not need.

## Order for Cache Reuse

Read `build-cache.md` for step ordering, cache mounts, and external cache. Without a cache mount, keep a
package-index refresh, package installation, and cache cleanup in the same `RUN` instruction, because a later
deletion leaves the removed bytes in an earlier layer. With a cache mount, leave the cleanup out, because it
discards the cache and saves no image space. Keep unrelated commands separate when combining them would obscure
failures or waste cache reuse; layer count alone is not an optimization target.

## Separate Build and Runtime Concerns

Use multiple stages when compilers, package managers, source, or development dependencies are unnecessary at runtime.
Copy only the runtime artifacts and required libraries into the final stage. Multi-stage builds are optional for images
that already contain only the required runtime material.

When the deliverable is a file rather than an image, such as a release archive or a binary, end with a
`FROM scratch` stage that copies in only those files, and build it with `--output type=local,dest=<dir>`. The
files land in that directory on the host, and no image is created.

Choose the base image using `base-image-comparison.md`. Pin production bases to a resolved digest and retain enough
version metadata for maintainers to understand and update the image.

## Slim an Image

Find where the size comes from before changing anything; `image-probing.md` has a probe for each source:

- **A heavy base image**, such as a full development image, carries tooling before the Dockerfile adds anything.
  Start from a slim distribution base, and add development tooling only in a development stage or as dev container
  features (`dev-containers.md`).
- **Build tools in the final stage**, such as compilers, headers, CMake, and Git. Build native libraries and every
  Python wheel in a builder stage. `COPY` the installed tree, such as a `DESTDIR` staging of `/usr/local`, into the
  runtime stage, and install the wheels from a `RUN --mount=type=bind,from=builder` so they never form a layer.
- **Hard dependencies on a GUI or toolkit** that the workload never loads, which `--no-install-recommends` cannot
  drop. Where the distribution splits the compiled libraries into their own packages, install only the libraries the
  workload uses. Take pure-Python modules from the full package with `apt-get download` and `dpkg-deb -x`; dpkg then
  records no owner for the copied files. A library's own hard dependency can still pull a few toolkit libraries.
- **Recommended packages**, which can also carry required plugins; check them before dropping them.

Pick the base release by the binary interface its packages share with pip. A distribution Python extension built
against an older major version of a library that pip pins, such as numpy 1.x under numpy 2.x, risks a binary
mismatch. Compare versions on `packages.debian.org` or `packages.ubuntu.com` with
`search?keywords=<pkg>&searchon=names&exact=1&suite=all&section=all`. Prefer the release whose Python version has
prebuilt wheels for the target architecture, because a missing wheel means a source build, which is slow under
emulation.

Run one Python. Mixing a base image's own Python with the distribution's packages through `PYTHONPATH` makes every
distribution package shadow its pip copy, because `PYTHONPATH` precedes `site-packages`. It also breaks tools that
install user packages, such as the dev container `python` feature. Use the distribution's interpreter with
`python3 -m venv --system-site-packages /opt/venv`: the distribution's bindings stay importable, the virtual
environment's pins win, and PEP 668 stays intact. Check which copy wins with
`python -c 'import <mod>; print(<mod>.__version__, <mod>.__file__)'`.

When a library built into `/usr/local/lib` shares a soname with a distribution package, pin the search order and fail
the build on the wrong copy, as `image-probing.md` shows.

## Control Privilege and Files

Create or select a non-root runtime user when the workload permits it. Keep application code and its directory owned
by root and readable by that user, so a compromised process cannot rewrite its own code, and give the user ownership
only of the paths it writes. `WORKDIR` creates a missing directory owned by the current `USER`, so set `WORKDIR`
before `USER` to keep the application directory root-owned. Numeric user IDs are useful where no user database exists,
but the surrounding platform must grant the same ID access to mounted data.

Give a copied file to the runtime user with `COPY --chown=<user>:<group>` only when the process writes to it. A later
`RUN chown -R` copies every affected file into a new layer, so the image carries them twice.

Keep credentials out of `ARG`, `ENV`, copied files, and command text. Use BuildKit secret mounts for commands that need
a credential during the build:

```dockerfile
# syntax=docker/dockerfile:1
RUN --mount=type=secret,id=registry_token,required=true \
    command-reading /run/secrets/registry_token
```

Pass the secret through the build tool's supported secret source. Inspect CI logs and cache behavior before treating the
flow as safe.

Fetch dependencies from a private Git host with `RUN --mount=type=ssh`, forwarding the caller's agent with
`--ssh default`, so no key enters the context or a layer. Copy a committed `known_hosts` entry for that host into the
build rather than running `ssh-keyscan` during it, because a scan trusts whatever key the network returns.

## Define Process Behavior

Use exec-form `ENTRYPOINT` or `CMD` when the workload should receive signals directly. Add a small init only when the
process tree needs signal forwarding or child reaping. Set the working directory explicitly.

Add a Dockerfile health check only when the image can perform a meaningful check across its intended deployments.
Otherwise define the health or readiness check at the deployment layer. Do not add `curl` or a shell solely to satisfy
a generic health-check rule.

## Validate

Use the project's configured Dockerfile linter when present. Build the required platforms and exercise the resulting
image with representative configuration. Inspect the final image configuration, layers, user, entrypoint, environment,
and labels. Confirm that build-only files and secrets are absent from both the filesystem and build history.
