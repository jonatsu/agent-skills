# Platform, Configuration, and Supply Chain

The defects here rarely appear in application code. They live in the files that decide how the application
runs and where its dependencies come from. A review scoped to source files therefore misses them.

## Application Configuration

Configuration defects follow a single pattern. A permissive default is correct for local development, and it
reaches production because nothing distinguishes the two.

Check that debug output, interactive debuggers, verbose error pages, seeded accounts, and development-only
routes cannot be enabled in production. Check that an attacker cannot influence the switch. Check that the
application fails to start on a missing security-critical setting rather than falling back to a default.

For anything served to a browser, review the response headers as a set. A content security policy is the one
that carries weight, and it carries none if it allows inline script or an unrestricted script source. Frame
control, content-type sniffing control, and a restrictive referrer policy are cheap and worth naming. Report a
missing header as low severity unless you can name the attack it would have stopped.

Review CORS against the credential setting. Reflecting the request origin while allowing credentials is
equivalent to trusting every origin, and allowing the null origin is reachable from a sandboxed frame. A
wildcard origin without credentials is usually intentional on a public API and is not a finding. Where the
session rides on a cookie, a permissive origin policy also undoes the CSRF controls in
`identity-and-access.md`.

## Network Exposure and Service Boundaries

Ask what the service listens on and who can reach it. This applies to a management interface, a metrics
endpoint, a debugger port, a database, and a cache. Any of them bound to a routable address, rather than to
loopback or a private network, is a finding. The finding stands whether or not the service has authentication,
because the exposure is the thing you can verify.

Inside a cluster, check whether the network permits any workload to reach any other. Flat networking turns one
compromised container into access to every service.

## Containers and Images

Read the image definition as a security artifact:

- a process running as root when nothing requires it, and a filesystem that is writable when nothing writes;
- a base image pinned by a moving tag rather than by digest, so the content changes without the definition
  changing;
- build arguments and intermediate layers that retain credentials even after a later layer deletes the file;
- a build context that copies the whole tree, including version-control history and local environment files;
- added capabilities, privileged mode, host namespace sharing, and host path mounts, each of which weakens the
  boundary the container exists to provide; and
- secrets supplied as environment variables in the manifest rather than mounted from a secret store.

For orchestrated deployments, extend the same reading to the workload manifest. Check the security context,
the service account and its permissions, missing resource limits, and secrets committed to the manifest.

## Infrastructure as Code

Treat the definition as the deployed state. The recurring findings are storage and network resources open to
the public internet, and permission policies that grant a wildcard action or a wildcard resource. They also
include logging and audit trails disabled and encryption at rest not enabled where the provider offers it. A
state file that holds plaintext secrets and is stored without access control is a finding too.

Trace a permission grant to what actually needs it. A role that carries administrative permissions because
narrowing them was difficult is the finding, and naming the specific actions required is the remediation.

## Continuous Integration

CI has production credentials and executes code, which makes it a high-value target that reviews routinely
skip.

Check for a workflow trigger that runs with repository secrets against code from an untrusted fork. That hands
the secrets to whoever opens a pull request. Check whether untrusted input (a branch name, a pull request
title, an issue body) is interpolated into a shell step. That is command injection with the runner's
credentials. Check that third-party actions and build plugins are pinned to an immutable revision rather than
to a tag. Check that credentials given to a job are scoped to what the job needs. Check that they are not
exposed to every step.

Check whether the pipeline can be made to skip its own security gates. Check whether an artifact can be
published without passing them.

## Dependencies

Run the project's configured audit tool and read its output rather than forwarding it. A reported advisory
matters when the vulnerable code path is reachable from this application, and a critical advisory in a
development-only dependency is usually not urgent. Say which you determined and which you assumed.

Independent of advisories, check that lockfiles exist and are committed, and that installation uses the
lockfile rather than resolving afresh. Check that no dependency is fetched from a mutable reference, such as a
branch or a `latest` tag. Consider the install-time scripts from dependencies.

Check for the naming risks too. Look for a dependency whose name closely resembles a popular package. Look for
an internal package name that a public registry could also serve. Look for a dependency that is unmaintained
or has recently changed ownership.

## Build and Artifact Integrity

Ask whether a consumer can tell that an artifact came from this pipeline. Signed artifacts, recorded
provenance, and reproducible inputs are the controls. Their absence is a real finding for anything
distributed, and usually a low one for an internal service.
