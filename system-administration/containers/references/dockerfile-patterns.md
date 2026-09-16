# Dockerfiles and Builds

Design the image around the target workload and build context. Consult the current Dockerfile and BuildKit references
for syntax and feature support.

## Inspect Before Building

Read the Dockerfile, referenced scripts, ignore file, and relevant lock files. A build executes project-controlled
commands and can access the build context, network, caches, and explicitly mounted secrets. Do not build untrusted input
as a substitute for reviewing it.

Keep sensitive files outside the context where practical. Use `.dockerignore` to exclude repository metadata, local
credentials, environment files, editor state, test artifacts, and dependency directories that the build does not need.

## Separate Build and Runtime Concerns

Use multiple stages when compilers, package managers, source, or development dependencies are unnecessary at runtime.
Copy only the runtime artifacts and required libraries into the final stage. Multi-stage builds are optional for images
that already contain only the required runtime material.

Choose the base image using `base-image-comparison.md`. Pin production bases to a resolved digest and retain enough
version metadata for maintainers to understand and update the image.

## Control Privilege and Files

Create or select a non-root runtime user when the workload permits it. Ensure copied files and writable paths are owned
by that user. Numeric user IDs are useful where no user database exists, but the surrounding platform must grant the
same ID access to mounted data.

Keep credentials out of `ARG`, `ENV`, copied files, and command text. Use BuildKit secret mounts for commands that need
a credential during the build:

```dockerfile
# syntax=docker/dockerfile:1
RUN --mount=type=secret,id=registry_token,required=true \
    command-reading /run/secrets/registry_token
```

Pass the secret through the build tool's supported secret source. Inspect CI logs and cache behavior before treating the
flow as safe.

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
