# Base Image Decisions

Choose the runtime image from compatibility and maintenance requirements. Size and vulnerability counts change with
every published image, so inspect candidate manifests and scan their current digests instead of relying on a stored
comparison table.

## Decision Order

1. Identify the operating system, architecture, libc, certificates, timezone data, native libraries, and runtime files
   the application needs.
2. Prefer an image maintained by the runtime vendor or another source the project trusts.
3. Remove build tools and package-manager caches from the runtime image. Use a separate build stage when it makes that
   boundary clearer or smaller.
4. Confirm that the chosen image supports the required user, filesystem paths, diagnostics, and patch process.
5. Resolve and scan the exact target-platform digest before deployment.

`scratch` fits a genuinely static binary after required certificates and data files are supplied. Distroless images can
reduce runtime contents but change debugging and user-management workflows. Alpine uses musl, which can be incompatible
with glibc-linked binaries or native extensions. Debian or Ubuntu slim variants often suit workloads that need glibc or
limited runtime diagnostics.

Do not select an image from size alone. A slightly larger image with a reliable update path and compatible libraries can
carry less operational risk than a smaller image that forces untracked additions or cannot be diagnosed.

## Verification

Resolve the supported platforms and immutable references with the registry tooling available to the project. Build and
run the application for every target architecture. Scan the exact digest and compare findings by reachability, available
fix, and project policy rather than raw count alone.
