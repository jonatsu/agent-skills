---
name: containers
description: Build, run, diagnose, and secure Docker and OCI containers. Use for Dockerfiles, Compose applications, container runtime settings, image scanning and publication, or Kubernetes workload hardening. Excludes general Kubernetes cluster administration.
license: MIT
compatibility: Requires the container, registry, scanner, or Kubernetes tools used by the target project.
metadata:
  author: Joonas Onatsu
---

# Containers

Use this skill for container images, Dockerfiles, Compose applications, container runtime settings, image supply chains,
and workload-side Kubernetes controls. Use the `systemd` skill as well when a Compose deployment is managed by systemd.
This skill does not cover general cluster administration, application security, or unrelated CI design.

Treat the target tool's installed help and official documentation as the authority. Container and orchestration features
change across Docker Engine, Docker Compose, containerd, Kubernetes, scanners, registries, and operating systems. Record
the versions that control the requested result before relying on a copied option or manifest field.

## Preserve User Authority

Classify an operation before running it:

- Inspection includes listing objects, reading logs, validating configuration without rendering secret values, and
  scanning local artifacts. These operations are normally read-only.
- Mutation includes building images, pulling from a registry, starting or replacing containers, applying manifests,
  signing images, and changing daemon or host configuration. Reuse authority already supplied by the request.
- Destruction includes removing containers, images, networks, volumes, builders, or Compose orphans. Commands such as
  `docker compose down`, `docker compose up --remove-orphans`, `docker * prune`, and volume removal require explicit
  authority for the resolved target and data impact.

Never add forced cleanup to a recurring job or ordinary start, stop, reload, or validation path. Do not expose values
from container environments, Compose interpolation, registry credentials, build secrets, or Kubernetes Secrets in
command output.

A Dockerfile build executes instructions from the build context. Inspect an untrusted Dockerfile and its referenced
scripts before building it. A remote image pull, registry push, signature publication, or cluster-side dry run uses an
external service; disclose that dependency when it is not already implied by the request.

## Establish the Target

Determine only the facts needed for the active branch:

- artifact and operation: Dockerfile, image, Compose project, running container, registry object, or Kubernetes
  workload;
- environment: development, CI, staging, production, or incident diagnosis;
- runtime and platform: rootful or rootless engine, Linux or Windows containers, target architectures, and orchestrator;
- state and data: current objects, persistent mounts, published ports, credentials, and rollback path; and
- project policy: accepted registries, vulnerability thresholds, signing identity, and deployment authority.

Prefer `docker version`, `docker compose version`, and the relevant command's `--help` over assumed version support.
Use `docker compose config --quiet` for validation when rendered configuration could contain secrets. Inspect effective
runtime settings rather than inferring them from a Dockerfile alone.

## Route the Work

Read the branch reference before making its decisions:

| Branch                                          | Reference                                               |
| ----------------------------------------------- | ------------------------------------------------------- |
| Dockerfile, build context, base image, BuildKit | `references/dockerfile-patterns.md`                     |
| Compose modeling, lifecycle, health, and data   | `references/docker-compose.md`                          |
| Runtime isolation, scanning, SBOMs, and signing | `references/runtime-security.md`                        |
| Container build and publication in CI           | `references/ci-cd.md`                                   |
| Kubernetes workload hardening                   | `references/kubernetes-pod-security.md`                 |
| Compose managed by systemd                      | `references/compose-systemd.md` and the `systemd` skill |
| Current specifications and tool documentation   | `references/official-docs.md`                           |

The remaining references provide additional examples but do not override this workflow or current official
documentation.

## Apply Proportionate Controls

Start from the workload's actual behavior. A typical network service can often run as a non-root user, drop all Linux
capabilities, prevent privilege escalation, use the runtime's default seccomp profile, and make its root filesystem
read-only. Add writable mounts, devices, capabilities, or a different user only when the workload demonstrates the need.
Record each production relaxation with its reason and validation.

Do not impose one base image, multi-stage build, health check, vulnerability threshold, custom seccomp profile, or
resource value on every workload. Choose them from compatibility, threat model, operability, and project policy.
Infrastructure containers, Windows containers, device workloads, and one-shot jobs can require different controls.

Pin production image references to an immutable digest when the deployment workflow can maintain digest updates. Keep a
human-readable tag or release record so operators can identify the version. Never invent a digest; resolve it from the
trusted registry and preserve the intended platform.

## Validate the Requested Outcome

Use checks that observe the changed layer:

- Dockerfile: lint when the project has a linter, build for the target platforms, and exercise the resulting entrypoint.
- Image: inspect configuration and layers, scan against the project's policy, and record any accepted finding with an
  owner, reason, and review condition.
- Compose: run `docker compose ... config --quiet`; use the CLI dry-run facility when supported; verify service health,
  shutdown, mounts, and persistence only when starting the project is authorized.
- Runtime hardening: start an isolated test instance, exercise the real workload, and inspect the effective user,
  capabilities, mounts, security options, and resource limits.
- Kubernetes: validate schemas locally when tooling exists; use `kubectl apply --dry-run=server` only when access to the
  target cluster is authorized; inspect admission results and workload behavior after an authorized apply.
- Supply chain: verify the digest, SBOM format, signature identity, issuer, and registry object that deployment
  consumes.

Report checks that were not run and why. A successful build does not prove runtime health, a clean scan does not prove
the absence of vulnerabilities, and static manifest validation does not prove that the target platform admits or runs
the workload.
