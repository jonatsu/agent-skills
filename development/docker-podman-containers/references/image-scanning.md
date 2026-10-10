# Image Scanning, SBOMs, and Signing

Use scanners and supply-chain tools already selected by the project. Otherwise choose a maintained tool that supports
the artifact, registry, output format, and policy engine in use.

## Scan Against Policy

Scan the exact image digest and target platform that deployment will consume. Select package vulnerabilities,
misconfiguration, secrets, or license checks from the risk being evaluated. A blanket HIGH or CRITICAL threshold can
block on unreachable or unfixed findings while missing project-specific risks.

For each accepted finding, record the identifier, affected component, reason, owner, expiry or review condition, and
upstream tracking location. Keep ignore files narrow and machine-readable when the scanner supports it. Re-run the scan
after base-image or dependency updates.

Re-evaluate retained and deployed digests as vulnerability data changes, even when the image bytes do not. Use
continuous registry analysis or scheduled rescans that cover the artifacts still in use. Record the scanner and database
snapshot, route new actionable findings to an owner, and apply the project's response policy.

Treat a clean result as evidence for that scanner, database snapshot, configuration, image, and platform. It does not
prove that the image is vulnerability-free.

## Produce and Verify Supply-Chain Evidence

Generate an SPDX or CycloneDX SBOM for the pushed digest. Preserve the tool and version that produced it. Sign the
digest, not a mutable tag. Prefer short-lived workload identity when the registry and signing system support it.

Verification must constrain the expected artifact, signer identity, issuer, and repository or workflow identity. Test
the same verification policy used by deployment. Publishing a signature without enforcing an identity policy provides
little deployment assurance.

## Install Tools Safely

Prefer the project's package manager, pinned tool environment, or a release artifact whose checksum and signature can
be verified. Do not pipe a moving installer from the network into a shell. Reading only the first part of a downloaded
script does not verify the script or its dependencies.

Use `official-docs.md` to locate Trivy, Grype, Syft, Cosign, and Hadolint documentation.
