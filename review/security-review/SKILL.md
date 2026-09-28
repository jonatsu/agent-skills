---
name: security-review
description: Review code, configuration, and infrastructure for exploitable security defects. Use for a security review, vulnerability hunt, threat model, OWASP assessment, or hardening pass over a diff, a component, or a whole repository, and whenever a change touches authentication, authorization, secrets, input parsing, deserialization, file uploads, outbound requests, or agent tool-use surfaces.
license: MIT
compatibility: Requires `rg` and `fd` for discovery. Uses the project's own audit tooling where it is configured, and prefers `betterleaks` over `gitleaks` for secret scanning; both are optional.
metadata:
  author: Joonas Onatsu
---

# Security Review

Report security defects an attacker can actually reach. A pattern match is a lead, not a finding. Trace where
the input comes from and what already constrains it before you write anything down.

## Iron Law

Reviewing is report-only. Do not edit, patch, refactor, or reformat any file while reviewing, however small
and safe the fix looks. Fixing is a separate phase that begins only after the user names which findings to
fix. Never change a file first and mention it afterwards.

## Scope Contract

Two scopes govern the review, and confusing them is the most common failure:

- **Report on** what the user named: the diff, the file, the module, the service.
- **Research** whatever settles a question: callers, configuration, middleware, validation layers, framework
  defaults, deployment manifests.

Reading outside the named scope is required. Reporting outside it is noise. When research outside the scope
uncovers something severe, say so in one clearly separated section rather than folding it into the findings.

## Procedure

### 1. Establish the scope and the deployment context

Use `fd` to discover files and `rg` to search them, throughout the review. Treat truncated or filtered output
as unknown rather than as absence.

Ask what the code is: a production service, a library, a local development tool, a build script, an example.
The same construct carries different risk in each. Determine which parts of the tree are test fixtures,
samples, generated output, or vendored third-party code, and treat them accordingly.

Read the project's own security documentation, threat model, and any `SECURITY.md` before flagging anything.
A project that has documented a deliberate exception has already answered you.

### 2. Map the trust boundaries

List every place untrusted data enters the system: end users, other services, webhooks, message queues,
uploaded files, fetched web or document content, IPC and subprocess output, environment supplied by another
tenant, browser extensions, and model or tool output in an agent system. Name the asset behind each boundary:
credentials, customer data, money, compute, the build pipeline.

The boundary list is the review's spine. Everything after it is depth on one boundary at a time.

### 3. Apply STRIDE to each boundary

Reason through the six categories before you enumerate findings. The value is in the questions you would
otherwise skip, not in the acronym.

| Category               | Question at this boundary                                                       |
| ---------------------- | ------------------------------------------------------------------------------- |
| Spoofing               | Is the identity of the caller or the data source verified, and by what?         |
| Tampering              | Can the data, the code, or the build be modified without detection?             |
| Repudiation            | Can a security-relevant action be traced back to who caused it?                 |
| Information disclosure | Does anything leak secrets, personal data, or internal state past its audience? |
| Denial of service      | Can input exhaust memory, CPU, connections, disk, recursion depth, or spend?    |
| Elevation of privilege | Can input reach a more privileged path than its caller holds?                   |

### 4. Trace the data flow before flagging

For every lead, answer where the value actually comes from. This single question removes most false
positives.

| Attacker-controlled                             | Operator-controlled                           |
| ----------------------------------------------- | --------------------------------------------- |
| Request query, body, form, and path segments    | Environment variables set at deployment       |
| Most request headers, and unsigned cookies      | Configuration files read from the server      |
| Uploaded file content, names, and archive paths | Compile-time constants and enum members       |
| Message-queue and webhook payloads              | Framework settings objects                    |
| Content fetched from a user-supplied URL        | Signed or server-side session state           |
| Records written by another tenant or user       | Internal service addresses from configuration |
| WebSocket frames and streamed chunks            | Values an administrator alone can write       |

Operator-controlled is not the same as safe. It is safe against an external attacker and still relevant if
the threat model includes a malicious operator, a compromised build, or configuration that a tenant supplies.
Say which model you applied.

Then ask two more questions. Does the framework, runtime, or library already neutralize this by default, and
is that default still on? Is there validation, an allowlist, or a sanitizer between the entry point and this
line?

### 5. Sweep the vulnerability classes

Read the reference for every surface the scope contains, and only those, before writing any finding about that
surface. The references carry the exceptions that separate a finding from a false positive, and a review that
never opens one is working from recall.

| Surface in the code                                             | Read                                      |
| --------------------------------------------------------------- | ----------------------------------------- |
| Queries, commands, templates, parsers, paths, outbound requests | `references/injection-and-parsing.md`     |
| Uploads, stored files, archives, and served content             | `references/injection-and-parsing.md`     |
| Login, sessions, tokens, permission checks, tenancy, CSRF       | `references/identity-and-access.md`       |
| Secrets, keys, hashing, randomness, personal data, logs         | `references/secrets-and-crypto.md`        |
| Config, headers, CORS, containers, IaC, CI, dependencies        | `references/platform-and-supply-chain.md` |
| Workflows, state machines, concurrency, quotas, error paths     | `references/logic-and-availability.md`    |
| Prompts, tools, MCP servers, retrieved content, autonomy        | `references/agent-and-llm-surfaces.md`    |

Language and framework specifics stay outside this skill. When a finding depends on one, verify the behavior
against that project's own documentation and cite it in the finding.

### 6. Run the checks the project already configures

Prefer the project's own tooling over improvised greps, and never install anything to review with it. Look
for a lockfile audit (`pip-audit`, `npm audit`, `cargo audit`, `govulncheck`, `bundler-audit`), a configured
secrets scanner, a SAST job in CI, and container or IaC scanning. Run what is configured and present, then
read the output critically rather than pasting it.

For secret scanning, prefer `betterleaks` over `gitleaks` where both are available. Never write a real-looking
credential into the tree to prove that a scanner fires; a scanner that is silent on a planted key has told you
nothing useful, and the planted key outlives the test.

Where you cannot run a configured check, say which one and why under Coverage Limits. Do not present a review
as complete when this step was skipped.

### 7. Gate on confidence, then on severity

| Confidence | Test                                                                  | What to do                         |
| ---------- | --------------------------------------------------------------------- | ---------------------------------- |
| High       | Vulnerable construct plus a traced attacker-controlled input          | Report as a finding                |
| Medium     | Vulnerable construct, but the input source or a mitigation is unclear | List under Needs Verification      |
| Low        | Theoretical, stylistic, or defense in depth with no reachable path    | Leave out, or note once in passing |

Severity describes impact once exploitability is established.

| Severity | Meaning                                                 | Required action     |
| -------- | ------------------------------------------------------- | ------------------- |
| Critical | Direct exploit, severe impact, no authentication needed | Block the merge     |
| High     | Exploitable under realistic conditions, major impact    | Block the merge     |
| Medium   | Needs specific conditions, or bounded impact            | Fix before release  |
| Low      | Defense in depth, minimal direct impact                 | Track, do not block |
| Info     | Observation with no impact claim                        | Record only         |

### 8. Report

Follow the output contract below. Done when every trust boundary from step 2 has been through steps 3 to 5, or
is named under Coverage Limits with the reason it was not.

## Common False Positives

Verify each of these before flagging it:

- Placeholder values in `.env.example`, sample configuration, and documentation.
- Credentials scoped to test fixtures, seeds, and local compose files.
- Keys the vendor intends to be public, such as client-side analytics or publishable API keys. Confirm
  against the vendor's documentation rather than the name of the variable.
- MD5 or SHA-1 over operator-controlled or non-adversarial input, for a cache key or a shard. Over
  attacker-supplied content, where the digest decides deduplication, uniqueness, or integrity, a chosen-prefix
  collision is practical against both and the fast hash is the finding.
- Non-cryptographic randomness used for jitter, sampling, or a UI value.
- Missing TLS, `Secure` cookie flags, and HSTS in code that only ever runs locally or behind a terminating
  proxy. Report the missing production configuration, not the local default. Do not recommend HSTS without
  saying what it locks the domain into.
- Dead code, commented code, and docstrings.
- A construct fed only by a constant or by operator-controlled configuration.
- A path that already requires authentication. Note the requirement instead of claiming an unauthenticated
  exploit.
- A practice the project has deliberately overridden and documented. Where the exception is real but
  undocumented, the finding is the missing documentation.

## Rules

Never propose disabling, weakening, loosening, or deleting a security control as the remedy. Fix the cause,
not the check that caught it. When a control genuinely blocks legitimate work, say so and propose a narrower
control.

Never fabricate a CVE identifier, an exploit chain, or a proof of concept. Label anything you have not
demonstrated as unverified. Do not run an exploit against infrastructure you were not asked to test.

Never copy a discovered secret's value into the report, a commit, or a message. Give its location and its
type, and treat any secret that reached version control as already compromised and needing rotation.

Record the controls that are working. A report that lists only gaps reads as reflexive and gets discounted.

State your coverage limits: what you did not read, which tool you could not run, and which question you could
not settle.

Write the report for a developer who is not a security specialist. Name each vulnerability class in words at
first use, such as server-side request forgery (SSRF), and apply `writing-for-humans` and its reader-ready check
before delivering.

## Output Contract

```markdown
## Security Review: <scope>

### Summary

One paragraph: overall posture, the worst finding, and whether the scope is safe to merge.
Counts by severity. Coverage limits.

### Findings

#### <Vulnerability class> in <component> — <Severity> (SEC-001)

- **Location**: `path/to/file.ext:120`
- **Confidence**: High
- **Issue**: what is wrong
- **Attack path**: entry point, the traced route to this line, and what the attacker gets
- **Evidence**: the smallest quoted snippet that shows the defect
- **Remediation**: the concrete change, and why it closes the path

### Needs Verification

#### <Potential issue> (VER-001)

- **Location**: `path/to/file.ext:88`
- **Open question**: exactly what a maintainer must confirm

### Working Controls

What the code already gets right, relevant to the surfaces reviewed.

### Coverage Limits

What was out of scope, unread, or unresolvable.
```

When nothing qualifies, say "No high-confidence findings" and still deliver the working controls and coverage
limits. Silence is not the same as a clean result.

## Fixing, After Approval

Move to fixes only when the user names the findings to fix. Then:

1. Fix one finding per change. Do not bundle unrelated findings into one commit.
2. Read enough of the surrounding code to know why the insecure form is there. Insecure code usually survives
   because something depends on it.
3. Say what the fix breaks before making it, when it changes an interface, a default, or an operational
   requirement.
4. Follow the repository's own test and commit conventions, and run its checks.
5. Re-verify the specific attack path the finding described. A fix that was not re-traced is unverified.
