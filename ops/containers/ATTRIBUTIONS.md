# Attributions

## Current skill

- Skill: `containers`
- Current author: Joonas Onatsu
- Current license: GPL-3.0
- Status: merged from two upstream skills and materially modified

This skill was created by merging two upstream skills into a single unified
container skill. The stricter of the two upstream licenses (GPL-3.0) applies to
the combined work.

## Original authors and sources

### 1. `docker` skill (build / compose / CI portions)

- Original author: mte90
- Upstream project: <https://github.com/CodeAtCode/oss-ai-skills>
- Source path (within upstream): `skills/docker/SKILL.md`
- Source commit: `a354eee266635660d6504f71b8b50b8c19c7e86a`
- Upstream license: GPL-3.0

### 2. `container-security-hardening` skill (security / CVE / runtime / K8s portions)

- Original author: community (upstream frontmatter records
  `source: community`; no individual author or upstream URL was recorded in
  the source file frontmatter)
- Upstream project: not recorded in source; content originated as a
  community-authored security hardening skill added to
  `~/.agents/skills/container-security-hardening/` on 2026-05-30
- Source path (within upstream): `SKILL.md` and
  `references/base-image-comparison.md`,
  `references/kubernetes-pod-security.md`,
  `references/seccomp-profile-template.json`
- Source commit: not pinned upstream
- Upstream license: not explicitly declared in source frontmatter; treated as
  community-contributed and folded into the combined GPL-3.0 work

### 3. `compose-systemd.md` reference (systemd deployment for Compose stacks)

- Original author: Joonas Onatsu (internal project documentation)
- Upstream project: `~/src/services/docs/docker-compose-systemd-best-practices.md`
  (local project documentation, no external upstream URL)
- Source path (within upstream): `docker-compose-systemd-best-practices.md`
- Source commit: not pinned (local file, imported 2026-07-14)
- Upstream license: internal project documentation, imported with permission
  and folded into the combined GPL-3.0 work

## Adaptation note

This version merges the two upstream skills listed above into a single
`containers` skill for this repository, and has been materially modified.

Material changes include:

- Merged two separate skills (`docker`, `container-security-hardening`) into
  one unified skill named `containers`.
- Rewrote `SKILL.md` as a lean core (under 500 lines) following
  skill-forge conventions: Iron Law, "When to Use" triggers, decision tree,
  five-layer model summary, minimum bars, common pitfalls, pre-delivery
  checklist, and pointers into `references/`.
- Split extended content into six new reference files:
  `dockerfile-patterns.md`, `docker-compose.md`, `ci-cd.md`,
  `image-scanning.md`, `runtime-security.md`, and (retained/copied)
  `base-image-comparison.md`, `kubernetes-pod-security.md`,
  `seccomp-profile-template.json`.
- Deduplicated overlap between the two upstream skills: base image guidance,
  non-root user setup, multi-stage build patterns, `.dockerignore` guidance,
  and healthcheck advice appeared in both — retained the more detailed
  hardened version (from `container-security-hardening`) and dropped the
  redundant looser variant (from the original `docker` skill).
- Retained all `container-security-hardening` material substance: seccomp
  profile template and workflow, CVE scanning (Trivy / Grype / Hadolint /
  Snyk), SBOM (Syft / CycloneDX), image signing (Cosign keyless via OIDC and
  SBOM attestation), Linux capabilities table, AppArmor, Kubernetes Pod
  Security Admission, NetworkPolicy zero-trust patterns, RBAC least-privilege
  patterns, Kyverno and OPA Gatekeeper policy templates, service account
  hardening including Workload Identity, Falco runtime detection, and
  Kubernetes secrets management options.
- Updated GitHub Actions CI/CD examples to use SHA-pinned action versions,
  BuildKit, buildx multi-platform, layer caching, Cosign signing, SBOM
  attestation, and SARIF upload to the GitHub Security tab.
- Added `references/compose-systemd.md` from internal project documentation
  covering systemd unit design for Docker Compose stacks (Type=oneshot,
  restart policies, graceful shutdown, GPU passthrough, pull policies,
  air-gapped deployments).
  BuildKit, buildx multi-platform, layer caching, Cosign signing, SBOM
  attestation, and SARIF upload to the GitHub Security tab.
- Set skill frontmatter `metadata.author` to `Joonas Onatsu` and
  `metadata.license` to `GPL-3.0` per skill-forge convention that the more
  restrictive upstream license applies to the merged work.

## Upstream license

The upstream `docker` skill is used under GPL-3.0. The upstream
`container-security-hardening` material is folded in under GPL-3.0 as part of
the combined work.

GPL-3.0 requires that derivative works remain under GPL-3.0 and that the
upstream copyright and license notices be preserved. This file provides that
notice.
