# Tool Prompt Authoring

Load when the target is a tool or function description the model reads to decide
whether to call it. Skip it for system prompts, agent definitions, API prompts
and global rule files.

Tool prompts are not API docs. They teach the model **when to reach for the tool,
what shape its inputs take, and which failure modes are the caller's
responsibility**. Everything else — engine internals, recovery heuristics,
fallback chains, performance tuning — stays in code.

---

### Describe surface, not machinery

The model picks tools from prose, not source. Tell it WHEN and WHY, NEVER HOW the
tool works internally. If the model's behavior would not change based on a
detail, the detail does NOT belong in the prompt.

A read tool enumerates every source it covers — file, directory, archive,
database, PDF, URL — so the model stops reaching for shell equivalents. It does
NOT mention the chunker, the binary sniffer, or the cache layer.

### Anatomy

1. **One-line purpose**, in the model's vocabulary. Not "wraps libfoo" but
   "compact, line-anchored edit format".
2. **Input grammar.** Operators, parameters, selectors — the concrete syntax the
   model will emit verbatim.
3. **Worked examples**, 3–8, covering the common shapes. Each example IS the
   explanation; do NOT narrate it twice.
4. **Failure shapes the caller owns** — those it can fix by changing its input.
   Skip failures the engine recovers from silently.
5. **Anti-patterns**, as WRONG/RIGHT pairs, drawn from real failures rather than
   imagined ones.
6. **A short recap** of the load-bearing rules, for the case where the body is
   skimmed.

### What stays out

Implementation file and function names. Recovery, retry, normalization, caching.
Performance characteristics, unless they change the calling strategy. Telemetry
and debug flags the model cannot set. Version history and deprecated parameters.
Cross-tool plumbing, unless the model must coordinate the two.

### Examples carry the contract

Tool prompts lean on examples harder than agent prompts do: syntax is mechanical,
and one correct example beats three paragraphs of grammar. Put the canonical
shape last — the most recent example is the strongest anchor for output
formatting.

Examples MUST be runnable shape, never pseudo-code. If the tool takes JSON, the
example is JSON. If it takes a custom grammar, the example uses real anchors and
real payloads.
