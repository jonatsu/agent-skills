# Container Delivery in CI

Keep the pipeline specific to the target registry and CI platform. Consult current official action or task
documentation before choosing inputs or pinned revisions.

## Pipeline Order

1. Lint the Dockerfile and validate metadata.
2. Build once for testing, using a deterministic context and the project lock files.
3. Exercise the image entrypoint and application behavior.
4. Scan the tested image under the project's vulnerability and secret policy.
5. Push only from authorized events and identities.
6. Address the pushed image by its returned digest.
7. Generate or attach an SBOM and provenance for that digest.
8. Sign the digest with the approved identity, then verify it with the same identity and issuer constraints used by
   deployment.

Grant each job only the permissions its steps need. Pull requests from untrusted forks must not receive publishing
credentials. Keep build secrets in the CI platform's secret facility and pass them through BuildKit secret mounts rather
than build arguments or environment persisted in image layers.

Pin third-party CI extensions to immutable revisions when the platform supports it. Let an update tool maintain those
pins, and review the upstream release before merging an automated update. Never enable automatic merging merely because
an image or action has a new digest.

Cache package downloads and build layers without placing credentials or generated secrets in the cache. Treat cache
content from untrusted branches as untrusted input.

The pipeline succeeds only when deployment can identify the exact tested digest and verify the required attestations.
A tag alone does not establish that identity.
