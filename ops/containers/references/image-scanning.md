# Image Scanning, SBOM, and Signing

Trivy, Grype, Hadolint, Syft, and Cosign — the standard OSS toolchain for finding CVEs, generating SBOMs, and
signing container images. Includes CI integration, ignore files, and admission control policies.

See also:

- `ci-cd.md` for the full GitHub Actions workflow that wires these together
- `dockerfile-patterns.md` for the Dockerfile that produces the image being scanned

---

## 1. Trivy — CVE + Secret + Misconfig Scanner (Recommended)

### Install

```bash
# macOS
brew install trivy

# Debian / Ubuntu
apt install trivy

# Linux / official installer (verified script)
tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh \
  -o "$tmpdir/trivy-install.sh"
sed -n '1,160p' "$tmpdir/trivy-install.sh"                # Read before running
sh "$tmpdir/trivy-install.sh"
```

### Common commands

```bash
# Scan an image for CVEs
trivy image myapp:latest

# Fail CI on HIGH/CRITICAL
trivy image --exit-code 1 --severity HIGH,CRITICAL myapp:latest

# Ignore CVEs already fixed downstream but not marked so
trivy image --ignore-unfixed myapp:latest

# Scan Dockerfile / IaC for misconfiguration
trivy config ./Dockerfile
trivy config ./k8s/

# Scan whole repo (vulnerabilities + secrets + misconfigs)
trivy fs --scanners vuln,secret,misconfig .

# Secret scan on an image
trivy image --scanners secret myapp:latest

# Generate SBOM
trivy image --format cyclonedx --output sbom.json    myapp:latest
trivy image --format spdx-json  --output sbom.spdx.json myapp:latest

# SARIF for GitHub Security tab
trivy image --format sarif --output trivy.sarif --severity HIGH,CRITICAL myapp:latest

# Apply an ignore file
trivy image --ignorefile .trivyignore myapp:latest
```

### `.trivyignore`

MUST include justification for every entry:

```
# CVE-2023-1234 — only exploitable via feature X we don't use.
#                 Tracked in issue #42. Recheck after upstream fix.
CVE-2023-1234

# CVE-2023-5678 — no upstream fix; risk accepted by security review 2026-04-01.
CVE-2023-5678
```

### `.trivyignore.yaml` (v0.53+)

Structured form with expiry dates — preferred for production:

```yaml
vulnerabilities:
  - id: CVE-2023-1234
    paths: ["usr/lib/x86_64-linux-gnu/libcrypto.so.3"]
    statement: "Not reachable in our config; feature X disabled."
    expired_at: 2026-12-31
```

---

## 2. Grype — Anchore Alternative

Fast and produces SBOMs alongside Syft. Good if you're already in the Anchore ecosystem.

```bash
# Install (verified script)
tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh \
  -o "$tmpdir/grype-install.sh"
sed -n '1,160p' "$tmpdir/grype-install.sh"
sh "$tmpdir/grype-install.sh"

# Scan
grype myapp:latest

# Fail on critical
grype myapp:latest --fail-on critical

# SARIF
grype myapp:latest -o sarif > grype.sarif

# Pair with Syft — scan an SBOM instead of the image
syft myapp:latest -o cyclonedx-json > sbom.json
grype sbom:sbom.json
```

---

## 3. Hadolint — Dockerfile Linter

Catches Dockerfile anti-patterns and best-practice violations statically.

```bash
# Run directly
docker run --rm -i hadolint/hadolint < Dockerfile

# With config
hadolint --config .hadolint.yaml --failure-threshold warning Dockerfile
```

`.hadolint.yaml`:

```yaml
failure-threshold: warning
ignored:
  - DL3008    # apt-get: pin versions (allow floating for base image)
trustedRegistries:
  - gcr.io
  - ghcr.io
  - public.ecr.aws
```

Full rule reference: <https://github.com/hadolint/hadolint#rules>.

---

## 4. Syft — SBOM Generation

```bash
# Install
brew install syft

# CycloneDX (recommended for cosign attestation)
syft myapp:latest -o cyclonedx-json > sbom.json

# SPDX
syft myapp:latest -o spdx-json > sbom.spdx.json

# Human-readable table
syft myapp:latest
```

---

## 5. Secret Scanning

```bash
# Trivy handles secrets too
trivy image --scanners secret myapp:latest

# Dedicated: TruffleHog
trufflehog docker --image myapp:latest

# Pre-commit: git-secrets (prevent committing secrets in the first place)
git secrets --scan
```

---

## 6. Cosign — Sign and Verify Images

### Install

```bash
brew install cosign
# or download from https://github.com/sigstore/cosign/releases
```

### Sign (keyless via OIDC — recommended)

```bash
# In GitHub Actions with permissions: id-token: write
export COSIGN_EXPERIMENTAL=true
cosign sign --yes ghcr.io/org/myapp@sha256:<digest>
```

No long-lived keys. Sigstore's public transparency log (Rekor) records the signature.

### Sign with a key (only if OIDC is unavailable)

```bash
cosign generate-key-pair                # Creates cosign.key + cosign.pub
cosign sign --key cosign.key ghcr.io/org/myapp@sha256:<digest>
```

MUST store `cosign.key` in a secret manager, not in Git.

### Attach SBOM as attestation

```bash
cosign attest --yes \
  --predicate sbom.json \
  --type cyclonedx \
  ghcr.io/org/myapp@sha256:<digest>
```

### Verify before deploy

```bash
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

---

## 7. Registry Scanning Comparison

| Registry                         | Built-in Scanning                     | Notes                    |
| -------------------------------- | ------------------------------------- | ------------------------ |
| GHCR (GitHub Container Registry) | No — run Trivy in CI                  | Best for OSS, OIDC auth  |
| AWS ECR                          | Yes (enhanced scanning via Inspector) | Enable per-repo          |
| GCP Artifact Registry            | Yes (Container Analysis)              | Enabled by default       |
| Azure ACR                        | Yes (Defender for Containers)         | Premium tier             |
| Docker Hub                       | Yes (limited on free tier)            | Avoid for private images |
| Harbor                           | Yes (via Trivy/Clair)                 | Self-hosted              |

Enable ECR enhanced scanning:

```bash
aws ecr put-registry-scanning-configuration \
  --scan-type ENHANCED \
  --rules '[{"repositoryFilters":[{"filter":"*","filterType":"WILDCARD"}],"scanFrequency":"CONTINUOUS_SCAN"}]'
```

---

## 8. Admission Control — Block Unsigned / Unscanned Images

### Kyverno — verify Cosign signature at admission

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-signed-images
spec:
  validationFailureAction: Enforce
  rules:
    - name: verify-signature
      match:
        resources:
          kinds: [Pod]
      verifyImages:
        - imageReferences:
            - "ghcr.io/org/*"
          attestors:
            - entries:
                - keyless:
                    subject: "https://github.com/org/repo/.github/workflows/*"
                    issuer: "https://token.actions.githubusercontent.com"
```

### Kyverno — require SBOM attestation

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-sbom-attestation
spec:
  validationFailureAction: Enforce
  rules:
    - name: verify-sbom
      match:
        resources:
          kinds: [Pod]
      verifyImages:
        - imageReferences: ["ghcr.io/org/*"]
          attestations:
            - type: cyclonedx
              attestors:
                - entries:
                    - keyless:
                        subject: "https://github.com/org/repo/.github/workflows/*"
                        issuer: "https://token.actions.githubusercontent.com"
```

---

## 9. Scanner Selection Guide

| Use case                                                         | Recommended tool                         |
| ---------------------------------------------------------------- | ---------------------------------------- |
| One tool that does most things (CVE + secret + misconfig + SBOM) | Trivy                                    |
| Deep supply chain integration with SBOM-first workflow           | Syft + Grype                             |
| Dockerfile static analysis before build                          | Hadolint                                 |
| Filesystem / IaC / K8s manifest scanning                         | Trivy `config`, `fs`                     |
| Runtime container behaviour anomalies                            | Falco (see `kubernetes-pod-security.md`) |
| Commercial support & policy management                           | Snyk, Prisma Cloud, Aqua                 |
