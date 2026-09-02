# CI/CD for Containers — GitHub Actions

Production-shaped GitHub Actions workflow for containers: SHA-pinned steps, BuildKit, multi-platform, layer
caching, Cosign signing, SBOM attestation, and SARIF upload to the GitHub Security tab.

See also:

- `image-scanning.md` for the standalone scanner usage the CI job wraps
- `dockerfile-patterns.md` for the Dockerfile the CI job builds

---

## 1. Minimum Production Workflow

```yaml
# .github/workflows/container.yml
name: Container Build & Publish

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

permissions:
  contents: read
  packages: write                    # For GHCR push
  id-token: write                    # For Cosign keyless (OIDC)
  security-events: write             # For SARIF upload

jobs:
  build:
    runs-on: ubuntu-24.04
    timeout-minutes: 30

    steps:
      - name: Checkout
        uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683   # v4.2.2

      - name: Set up QEMU
        uses: docker/setup-qemu-action@49b3bc8e6bdd4a60e6116a5414239cba5943d3cf   # v3.2.0

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@c47758b77c9736f4b2ef4073d4d51994fabfe349   # v3.7.1

      - name: Login to GHCR
        uses: docker/login-action@9780b0c442fbb1117ed29e0efdff1e18412f7567   # v3.3.0
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@8e5442c4ef9f78752691e2d8f8d19755c6f78e81   # v5.5.1
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=sha,prefix=sha-,format=short

      - name: Lint Dockerfile
        uses: hadolint/hadolint-action@54c9adbab1582c2ef04b2016b760714a4bfde3cf   # v3.1.0
        with:
          dockerfile: Dockerfile
          failure-threshold: warning

      - name: Build (load into local Docker for scan)
        uses: docker/build-push-action@4f58ea79222b3b9dc2c8bbdd6debcef730109a75   # v6.9.0
        with:
          context: .
          load: true
          tags: local-scan:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Scan image with Trivy
        uses: aquasecurity/trivy-action@6e7b7d1fd3e4fef0c5fa8cce1229c54b2c9bd0d8   # v0.28.0
        with:
          image-ref: local-scan:${{ github.sha }}
          format: sarif
          output: trivy-results.sarif
          severity: HIGH,CRITICAL
          exit-code: '1'
          ignore-unfixed: true

      - name: Upload Trivy SARIF
        if: always()
        uses: github/codeql-action/upload-sarif@4f3212b61783c3c68e8309a0f18a699764811cda   # v3.27.1
        with:
          sarif_file: trivy-results.sarif

      - name: Build and push multi-platform
        id: push
        if: github.event_name != 'pull_request'
        uses: docker/build-push-action@4f58ea79222b3b9dc2c8bbdd6debcef730109a75   # v6.9.0
        with:
          context: .
          push: true
          platforms: linux/amd64,linux/arm64
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          provenance: true                         # SLSA provenance attestation
          sbom: true                               # Attach SBOM attestation

      - name: Install Cosign
        if: github.event_name != 'pull_request'
        uses: sigstore/cosign-installer@dc72c7d5c4d10cd6bcb8cf6e3fd625a9e5e537da   # v3.7.0

      - name: Sign image (keyless via OIDC)
        if: github.event_name != 'pull_request'
        env:
          TAGS: ${{ steps.meta.outputs.tags }}
          DIGEST: ${{ steps.push.outputs.digest }}
        run: |
          echo "$TAGS" | xargs -I {} cosign sign --yes {}@$DIGEST
```

---

## 2. Pinning GitHub Actions

MUST pin all third-party actions to a full commit SHA and record the version in a trailing comment
(Renovate/Dependabot picks up both):

```yaml
uses: docker/build-push-action@4f58ea79222b3b9dc2c8bbdd6debcef730109a75   # v6.9.0
```

NEVER pin only by tag:

```yaml
uses: docker/build-push-action@v6                  # ❌ Mutable
uses: docker/build-push-action@main                # ❌ Extremely mutable
```

First-party `actions/*` steps SHOULD also be SHA-pinned in security-sensitive repos.

---

## 3. Layer Caching Strategies

### GitHub Actions cache (`type=gha`) — simplest

```yaml
cache-from: type=gha
cache-to: type=gha,mode=max
```

Pros: no setup. Cons: 10 GB cache limit per repo; scoped per branch.

### Registry cache — cross-runner, cross-branch

```yaml
cache-from: type=registry,ref=ghcr.io/${{ github.repository }}:buildcache
cache-to: type=registry,ref=ghcr.io/${{ github.repository }}:buildcache,mode=max
```

Pros: no size limit, shared across all runs. Cons: requires registry push access.

### Inline cache — smallest change from an existing workflow

```yaml
cache-from: type=inline
cache-to: type=inline
```

Cache is embedded in the pushed image manifest. Simple, but only reuses across pushes of the same image.

---

## 4. Multi-Platform Builds

```yaml
- uses: docker/setup-qemu-action@...              # For non-native arches
- uses: docker/setup-buildx-action@...
- uses: docker/build-push-action@...
  with:
    platforms: linux/amd64,linux/arm64
    push: true
```

For fastest builds, host a self-hosted `arm64` runner instead of QEMU emulation.

Standalone equivalent (outside CI):

```bash
docker buildx create --name multi --use --bootstrap
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag ghcr.io/org/myapp:latest \
  --push .
```

---

## 5. Cosign Signing & SBOM Attestation

```bash
# Keyless via OIDC (no long-lived keys)
export COSIGN_EXPERIMENTAL=true

# Sign
cosign sign --yes ghcr.io/org/myapp@sha256:<digest>

# Generate SBOM with Syft
syft ghcr.io/org/myapp@sha256:<digest> -o cyclonedx-json > sbom.json

# Attach SBOM as attestation
cosign attest --yes \
  --predicate sbom.json \
  --type cyclonedx \
  ghcr.io/org/myapp@sha256:<digest>

# Verify before deploy
cosign verify \
  --certificate-identity-regexp="https://github.com/org/repo" \
  --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
  ghcr.io/org/myapp@sha256:<digest>

cosign verify-attestation \
  --type cyclonedx \
  --certificate-identity-regexp="https://github.com/org/repo" \
  --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
  ghcr.io/org/myapp@sha256:<digest>
```

The `docker/build-push-action@v6` already supports `provenance: true` and `sbom: true` — use those to get SLSA
provenance + SBOM attached automatically. `cosign sign` still adds the Sigstore signature on top.

---

## 6. Common CI Anti-Patterns

| Anti-pattern                              | Fix                                                                           |
| ----------------------------------------- | ----------------------------------------------------------------------------- |
| Docker Hub credentials as long-lived PATs | Use GHCR + `GITHUB_TOKEN`, or OIDC-based token exchange for other registries  |
| Actions pinned to `@main` or `@v3`        | Pin to full commit SHA with trailing `# vX.Y.Z`                               |
| Building on every push with no cache      | Add `cache-from` / `cache-to` (GHA cache is one line)                         |
| No scan gate before push                  | Trivy `exit-code: 1` on HIGH/CRITICAL                                         |
| No lint before build                      | Add Hadolint step                                                             |
| Building `latest` tag from every branch   | Use `docker/metadata-action` semver / SHA / branch tags                       |
| No SBOM                                   | Add `sbom: true` to build-push-action, plus `cosign attest`                   |
| No signature verification at deploy       | Add `cosign verify` in the deploy step or Kyverno `verifyImages` at admission |
| Pushing on pull_request                   | Guard with `if: github.event_name != 'pull_request'`                          |
| Missing `permissions:` block              | Add explicit least-privilege permissions per job                              |
