# Agent and Model Surfaces

A system that gives a language model tools has a trust boundary that conventional review misses. The model's
context window is an input channel, and everything placed into it is untrusted once any part of it came from
outside.

Review these surfaces the same way as any other: name the boundary, name the asset behind it, and trace what
an attacker who controls the input can reach.

## The Core Defect

A model does not separate instructions from data. Text retrieved from a document, a web page, a code comment,
an issue, an email, a filename, or another tool's output is read as part of the same stream as the system
prompt. Instructions embedded in that text are therefore executed with whatever authority the agent holds.

There is no reliable filter for this. Detection heuristics, delimiters, and instructions to ignore embedded
commands all reduce the rate and none of them close the boundary. Review accordingly: the control that matters
is what the agent is permitted to do, not how well the prompt is worded.

## Trace the Injection Path

For each system, answer three questions in order.

**What untrusted content reaches the context?** Fetched pages, retrieved documents, repository contents, ticket
and pull-request text, user uploads, database records written by other users, tool and API responses, and
subagent output all qualify. So does a filename, and so does an error message that echoes input.

**What can the agent do once influenced?** Enumerate the tools by consequence, not by name. Which write files,
run commands, make outbound requests, spend money, send messages, or change permissions? That list is the
blast radius of every injection path above.

**What can leave?** Exfiltration needs an outbound channel, and the channels are easy to overlook: a fetch to
an attacker-controlled URL, an image or link rendered in the response, a written file the user later publishes,
a commit, a message sent to a third party, and a search query. A read-only agent that can render a remote image
can still exfiltrate everything it has read.

## Controls Worth Requiring

Scope authority to the task. An agent authorized for more than the current task needs is the finding, whether
or not you can demonstrate the injection. This is the single highest-value control, and it is usually the
missing one.

Require confirmation at the consequential action rather than at the start of the session. Approval granted
once for a session is not approval for what an injected instruction does later in it.

Keep the privileged path away from untrusted content. Where a design permits it, separate the component that
reads untrusted content from the component that holds credentials and tools, and pass structured results
between them rather than free text.

Treat every model output that reaches an interpreter as untrusted input. Generated SQL, shell commands, code,
file paths, URLs, and markup need the same validation as data from a user, because that is what they are.
Model output rendered into a page needs the same output encoding as user content.

Bound the loop. Cap iterations, tool calls, recursion depth, token spend, and wall-clock time, and make the
cap a hard stop rather than a warning. An agent without these can be driven into unbounded cost by input that
never triggers any other control.

Log the decisions, not only the results: which tool was called, with what arguments, on whose behalf, and
what content was in context. An agent incident is unreconstructable without this.

## Configuration and Integration Review

For a tool or server the agent connects to, check what the definition actually grants. A tool description is
part of the prompt, so a server can influence the agent through its own metadata; a server added from an
untrusted source is a supply-chain risk with prompt-level reach.

Check how the server is authenticated and what credentials it holds, whether its permissions are per-user or
shared, and whether a tool that reads and a tool that writes are gated the same way. Check that credentials
for downstream services are not passed through the model, since anything in the context can be emitted.

For hosted deployments, check tenant isolation in conversation storage, in vector stores, and in caches. A
retrieval index built across tenants leaks by design, and the retrieval step is often the only place the
tenant filter is missing.

## Reporting These Findings

Severity follows the reachable consequence, exactly as elsewhere. An injection path into an agent that can
only read public data is low. The same path into an agent that can commit, deploy, or send mail is critical.

State the path explicitly: the content source, how it reaches the context, the tool it drives, and what the
attacker gets. An assertion that prompt injection is possible, without that chain, is not a finding.
