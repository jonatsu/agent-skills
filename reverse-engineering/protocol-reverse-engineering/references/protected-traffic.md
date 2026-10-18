# Protected Traffic

## Distinguish Encoding, Compression, and Encryption

Look for container metadata, negotiated options, implementation calls, repeatability, and known input/output\
relationships. High entropy can result from compression, encryption, or random data. Short samples make entropy\
estimates unstable. Block-aligned lengths and a changing prefix suggest possibilities but do not identify a cipher,\
mode, or IV by themselves.

First locate each transformation boundary: application serialization, compression, encryption/authentication, and outer\
framing. Record which lengths and checks apply at each layer. Preserve original bytes and map each successful decoding\
step to its input and output. Validate a candidate decompressor or decoder against declared lengths and multiple\
samples with strict resource limits.

If implementation evidence is available, trace the actual buffer and length through library or custom calls. A\
cryptographic constant or import establishes a lead, not proof that it protects the target traffic.

## TLS Access Paths

Inspect negotiated version, available handshake coverage, key exchange, and whether the endpoint can supply session\
secrets. A key log is a supported route only when that endpoint/runtime actually emits the needed secrets. Setting\
`SSLKEYLOGFILE` does not make every application produce a key log.

Wireshark's [TLS guide](https://wiki.wireshark.org/TLS/) describes supported key material and configuration. Server\
private keys do not generally decrypt modern forward-secret sessions or TLS 1.3. Require an applicable key-exchange\
case rather than promising private-key decryption universally.

After confirming field availability and the selected key-log path, TShark can read a local capture with that file:

```bash
tshark -r capture.pcapng -o tls.keylog_file:session.keys -Y tls
```

Treat key logs as credentials. Restrict access and avoid copying them into example repositories or general logs. A\
failed decryption can reflect missing secrets, incomplete capture, unsupported versions, or incorrect session\
association; inspect diagnostics before declaring the traffic cryptographically unrecoverable.

## Interception and Endpoint Instrumentation

TLS interception changes endpoint trust and may fail under certificate pinning, mutual authentication, or custom\
transport behavior. A transparent proxy also requires routing and permissions. Do not treat disabling certificate\
validation or changing system trust as an offline-analysis step.

When scope includes a controlled client/server, compare a session-key route, application-level logging, or a scoped\
pre-encryption/post-decryption observation point. Record changed trust, launch, and environment assumptions. Keep\
payloads and credentials limited to the requested analysis. Explain residual coverage when only metadata is visible.

## Evidence and Limits

Record the validated transformation chain, key/source provenance without revealing values, which sessions decode, and\
remaining opaque fields. Use visible timing, sizes, directions, and handshake metadata only for claims those\
observations support. A client fingerprint is not an authenticated application or actor identity.
