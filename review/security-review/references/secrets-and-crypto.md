# Secrets, Cryptography, and Data Protection

## Secrets in the Tree

A credential committed to version control is compromised, because history keeps it after the file changes.
The finding is always two things: remove the credential from the running system, and rotate it. A change that
only deletes the line is not a fix.

Report the location and the credential type. Never copy the value into a report, a commit message, a test, or
a chat message.

Look beyond source files. Credentials collect in lockfiles and dependency URLs, container image layers and
build arguments, CI configuration and workflow files, editor and tool configuration, test fixtures and
recorded HTTP interactions, notebooks, and infrastructure state files. A state file that a provisioning tool
writes commonly holds every secret the deployment uses in plaintext.

Distinguish a real credential from a placeholder before flagging. Sample environment files, documentation, and
obvious dummy values are not findings. Vendor keys intended to be public are not findings either; confirm that
against the vendor's documentation rather than against the variable name, because a publishable key and a
secret key often differ by one word.

Where a secrets scanner is configured, run it. Prefer `betterleaks` over `gitleaks` where both are available.
Never plant a real-looking credential in the tree to prove that a scanner fires. The test tells you nothing
when the scanner is silent, and the planted value outlives the test.

## Secret Handling at Runtime

Configuration supplied by the environment or by a secret manager is the baseline. Beyond that, check that
secrets are not passed as command-line arguments where the process table exposes them, not written to logs or
crash reports, not embedded in URLs where proxies and history retain them, and not returned by a diagnostic or
health endpoint.

Ask whether the system can rotate a credential without redeployment, and whether anything caches a secret past
its rotation.

## Algorithm and Construction Choices

Judge cryptography by what the code is trying to achieve. The common error is a construct that is correct for
one goal used for another.

| Goal                         | Correct construct                                     |
| ---------------------------- | ----------------------------------------------------- |
| Store a password             | A memory-hard password hash with a per-user salt      |
| Verify a message came intact | A keyed MAC, or an authenticated encryption mode      |
| Encrypt data                 | Authenticated encryption with a unique nonce per key  |
| Derive a key from a secret   | A key derivation function, not a plain hash           |
| Generate a token or an ID    | The platform's cryptographically secure random source |
| Fingerprint a file           | Any collision-resistant hash, and a fast one is fine  |

Flag the mismatches, not the algorithm names in isolation. A fast hash over a file is correct. The same hash
over a password is a defect. A non-cryptographic random source in a sampling decision is correct; the same
source generating a reset token is a defect.

Specific constructions worth checking:

- an unauthenticated encryption mode, which permits an attacker to alter plaintext undetected;
- a nonce or initialization vector that is fixed, counted from zero on restart, or reused across messages;
- encryption applied without any integrity check, then decrypted and parsed;
- a signature verification whose failure path continues rather than rejects;
- a comparison of a MAC or a token that is not constant-time;
- key material generated or stored alongside the data it protects, so a single read compromises both; and
- certificate or hostname verification disabled, which is usually a development workaround that shipped.

Do not write a cryptographic primitive by hand, and treat any hand-rolled construction in review as a finding
in its own right regardless of whether you can break it.

## Transport and Storage

Report a missing transport control against the environment that actually runs it. Production traffic between
services and to users needs TLS with verification enabled. Local development, tests, and traffic terminated by
a proxy outside the scope do not. State which you assumed.

Be deliberate about HSTS. It is correct for a production domain the operator controls, and it commits every
subdomain for the duration of the max-age. Recommend it only with that consequence stated.

For data at rest, ask what the encryption defends against. Full-disk encryption defends against a stolen
device and does nothing against an application-level read. Field-level encryption of the sensitive columns is
what limits a database compromise, and it costs queryability.

## Personal Data and Logging

Identify what the system stores about people, then check three things: whether it needs to store it, how long
it keeps it, and who can read it.

In logs and telemetry, check that authentication material, tokens, session identifiers, full payment data,
government identifiers, and request bodies that carry any of these are redacted before they are written.
Redaction has to happen at the logging boundary. A rule that depends on every call site remembering will be
wrong somewhere.

Errors are the other leak. A stack trace, a database error, or an internal hostname returned to a client hands
an attacker the system's shape. Return a generic message with a correlation identifier, and keep the detail
server-side.

Also check what the system sends outward: crash reporters, analytics, error trackers, and support tooling all
receive whatever the request context carried unless something strips it.
