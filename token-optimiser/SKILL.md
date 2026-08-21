---
name: token-optimiser
description: "Agent operational patterns for minimizing token consumption during sessions. Covers selective reading, tool efficiency, context isolation, output economy, and anti-patterns. Platform-agnostic, no tool-specific references. Complements semantic-compression (text content) and system-prompts (prompt authoring)."
metadata:
  author: Joonas Onatsu
  license: MIT
---

## Scope

Operational behavior patterns that reduce token burn during agent sessions. This skill does NOT cover:
- Text compression rules (see `semantic-compression`)
- Prompt authoring density (see `system-prompts`)

Techniques below name capabilities (LSP, AST search, vision tools, parallel
calls, subagents, checkpoint/rewind) that not every runtime has. Apply each only
where the current harness supports it; NEVER invent a tool or fake a result to
satisfy a rule.

## Cardinal rule

**Correctness over brevity.** Token optimization MUST NOT drop meaning, context, or precision. Every technique below reduces *waste* (narration, redundant reads, unnecessary verbosity). None may sacrifice:
- Accuracy of technical claims or code
- Completeness of required deliverables
- Critical context the reader or downstream tool needs to act correctly
- Error details, edge cases, or caveats that affect behavior

When brevity and correctness conflict, correctness wins. Always.

## Input economy

 - SHOULD read line ranges over whole files; read a whole file only when it is small or you genuinely need all of it. Prefer structural summaries first, then expand the ranges you need.
 - SHOULD locate targets with grep/glob before reading, unless the exact path and scope are already known. AVOID opening a file just hoping to find something.
 - AVOID re-reading unchanged content; re-read only when the file may have changed since your last read.
 - When code intelligence is available (LSP: definition, references, hover), SHOULD prefer it over reading entire files to understand symbols.
 - When available, SHOULD prefer AST search over regex where structure matters; fewer false positives, less noise.
 - When vision/inspect tools are available and relevant, SHOULD use them instead of reading raw bytes into context.

## Output economy

 - MUST NOT narrate intent: skip "Now I'll...", "Let me check...", "I'm going to...".
 - AVOID preamble before results and filler summaries after. Economy trims narration, not substance — still deliver the required results and report what you validated.
 - In status notes and internal reasoning, MAY drop articles and use `[subject] [verb] [reason].` fragments. Keep user-facing prose clear and well-formed.
 - AVOID restating what was just done; move to the next step.
 - Exception: security warnings, irreversible operations, and ambiguous sequences get full prose.

## Tool efficiency

 - When the runtime supports parallel calls, SHOULD parallelize independent tool calls rather than serializing reads/searches that have no dependency.
 - SHOULD batch related searches into one call where the tool supports multiple patterns or paths.
 - SHOULD use targeted selectors — line ranges, column offsets, query filters — where the tool supports them. Broad queries waste context on irrelevant matches.
 - One failing lookup is not "blocked." SHOULD retry with a different strategy (different pattern, path, or tool) before concluding absence — but after a few tries, report the gap rather than retrying indefinitely.

## Context isolation

 - Before an exploratory branch, note the goal and scope; afterward keep only the findings and discard the intermediate steps. Where the runtime provides checkpoint/rewind, use it for exactly this.
 - When subagents are available and the task is broad, SHOULD delegate isolated investigative slices — their context is isolated, so only the final report enters yours.
 - When delegation is available, SHOULD dispatch independent slices in parallel rather than reading everything yourself.
 - Read a delegated artifact only when you need specific content from it.

## Anti-patterns

| Pattern | Cost | Fix |
|---|---|---|
| Reading whole files to find one function | Entire file in context | Grep for the symbol, read the range |
| Re-reading unchanged files | Duplicate context | Trust prior reads; re-read only on change |
| Serial tool calls with no dependency | Wasted round-trips | Parallelize where supported |
| Narrating each step | ~20-50 tokens per narration | Delete narration entirely |
| Reading a file "to see what's there" | Unbounded | Glob/grep first, read targeted ranges |
| Dumping full command output | Unbounded | Use filtered/summary output modes |
| Re-importing/re-declaring in eval cells | Redundant setup tokens | State persists; reuse prior definitions |
| Asking the user what tools can answer | Round-trip + user effort | Use tools first |

## Decision heuristic

Before each tool call, ask:
1. Do I already have this information in context? Skip if yes.
2. Can I narrow the query (line range, pattern, selector)? Always narrow.
3. Are there other calls I need that don't depend on this result? Parallelize them where supported.
4. Will this produce more context than I need? Use a filtering/summary mode.
5. Is this exploratory? Note the goal and scope first, keep only the findings.
