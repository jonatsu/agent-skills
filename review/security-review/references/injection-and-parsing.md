# Injection and Parsing

Every defect here has the same shape. Untrusted data crosses into an interpreter that cannot tell the
attacker's data from the program's own instructions. The remedy is always to keep the two in separate
channels, never to escape harder.

## Decide Which Interpreter Is Involved

Name the interpreter before you reason about the defect. Each one has its own separated-channel construct, and
the correct question is whether that construct is in use.

| Interpreter                 | Separated-channel construct                            |
| --------------------------- | ------------------------------------------------------ |
| SQL engine                  | Bound parameters, or a query builder that binds        |
| Document or key-value store | Typed values and an operator allowlist                 |
| Operating system            | An argument vector, with no shell                      |
| Directory service           | Encoded filter and DN components                       |
| Template engine             | Data passed as context, never compiled into the source |
| Expression evaluator        | No untrusted input, ever                               |
| Browser DOM                 | Text assignment, or contextual encoding                |
| Path resolver               | Resolve, then check containment                        |
| Serializer                  | A data-only format with a schema                       |

## SQL and Query Languages

Bound parameters are the only complete defense. Escaping functions lag behind the engine's parser and are
routinely defeated by character-set edge cases.

Identifiers cannot be bound. Table names, column names, sort keys, and sort direction must come from a
server-side allowlist that maps a user token to a literal identifier. Building an identifier by quoting user
input is a defect even when the value looks harmless.

Look specifically for:

- string concatenation, formatting, or interpolation reaching a query;
- an ORM's raw-SQL escape hatch, which is where interpolation reappears in codebases that are otherwise safe;
- dynamic `ORDER BY`, `LIMIT`, and pagination built from request values;
- a `LIKE` pattern that passes user wildcards through, which is a denial-of-service and a data-scope issue
  rather than an injection;
- second-order injection, where the value was stored safely and then interpolated on a later read; and
- stored procedures that themselves build dynamic SQL.

For document stores, the injection is usually structural rather than lexical. When a request body deserializes
straight into a query filter, the attacker supplies operators instead of values and turns an equality check
into a comparison or a regular expression. Coerce each field to its expected scalar type before it reaches the
query, and reject operator keys.

## Operating System Commands

Prefer a library call to a subprocess. When a subprocess is genuinely required, pass an argument vector and do
not involve a shell. A shell string built from user input is a critical defect regardless of the escaping
applied.

Argument-vector execution is necessary but not sufficient. Also check:

- an argument that begins with `-`, which the target program reads as an option rather than as data. Insert
  `--` or anchor relative paths with `./`;
- the program itself resolved from a user-influenced value or an inherited `PATH`;
- the inherited environment, since variables such as the loader path and language-specific option variables
  change how the child behaves; and
- a command template read from configuration a tenant can write, which restores the string-building defect
  one level away.

## Path Traversal and File Access

Traversal is not solved by rejecting `..`. Encodings, alternate separators, Unicode normalization, and
symbolic links all reintroduce it.

The reliable sequence is to reject absolute paths and drive letters, join the candidate to the base directory,
resolve the result fully with symlinks followed, and then verify that the resolved path is still inside the
resolved base. Reject anything else. Where the identifier need not be a path at all, prefer an opaque
identifier mapped server-side to a stored location.

For archives, apply the same containment check to every member before extraction, and reject entries that are
absolute, that traverse upward, that are symbolic or hard links, or that expand far beyond their compressed
size.

## Server-Side Request Forgery

A defect exists when the destination of an outbound request is influenced by untrusted input. The reachable
targets are the cloud instance metadata service, internal admin interfaces, unauthenticated services on the
loopback interface, and the container network.

Blocklists of private ranges fail. DNS resolves to a private address after the check, a redirect moves the
request to a new host, and alternate address encodings evade string comparison.

Prefer an allowlist of destination hosts. Where the destination is genuinely open, the request path must
enforce the scheme, resolve the hostname and check every resolved address against private, loopback,
link-local, and metadata ranges, connect to the checked address rather than re-resolving, refuse redirects or
re-run the whole check per hop, set connection and read timeouts, and cap the response size.

Treat any component that fetches a user-supplied URL as an SSRF surface, including document converters,
webhook senders, link previewers, and image processors.

## Deserialization and Parsers

Native object deserialization of untrusted input is a critical defect with no safe configuration. This covers
language-native pickling and object streams, and any format that reconstructs arbitrary classes. The remedy is
a data-only format parsed into a validated schema, not a class allowlist.

For structured text formats, check the parser's configuration rather than the format's reputation:

- YAML loaders that instantiate arbitrary types unless the safe loader is selected;
- XML parsers with external entity resolution or DTD processing enabled, which give file read and SSRF;
- entity and recursion expansion limits, absent which a small document exhausts memory;
- decompression limits, absent which a small archive exhausts disk; and
- schema validation applied after parsing rather than size and depth limits applied during it.

A regular expression applied to untrusted input is a parser too. Catastrophic backtracking turns a short
string into unbounded CPU. Prefer anchored, non-nested patterns, cap the input length, and prefer a
linear-time engine where the platform offers one.

## Template and Expression Evaluation

Server-side template injection follows from compiling a template out of user input rather than from rendering
user input inside a fixed template. The first gives attacker-controlled code in the template engine's own
language, which usually reaches the runtime. Templates must be static assets; user data is context.

The same rule governs every dynamic evaluator: expression languages, query DSLs, spreadsheet formulas,
serialization formats with code hooks, and the language's own `eval`. Untrusted input reaching one of these is
critical.

## Output Encoding

Injection into a browser is the same defect viewed from the other side. The correct encoding depends on where
the value lands, and there are five distinct contexts: HTML element text, attribute values, URL components,
inline script, and inline style. A single escaping function applied everywhere is wrong in at least three of
them.

Frameworks that auto-escape element text still do not protect an attacker-controlled URL used in a link or a
redirect, an attribute name, a full attribute-value injection, or the escape hatches every framework provides
for raw markup. Those escape hatches are the thing to grep for.

Where markup genuinely must come from users, sanitize with a maintained allowlist-based library, on the
server, and serve the result under a content security policy that does not enable inline script.

The same principle covers other sinks that are easy to miss: header values assembled from input, redirect
targets taken from a parameter, spreadsheet cells that begin with a formula character, log lines that carry
untrusted newlines, and filenames echoed into a `Content-Disposition` header.
