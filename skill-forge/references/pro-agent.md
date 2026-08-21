# Pro Agent Reference: Three-Layer Architecture

## Layer 1: Directive (The 'What')
Skill instructions and reference files. Goals, process steps, quality gates, edge cases, domain knowledge.

## Layer 2: Orchestration (The 'How')
Agent reasoning and routing. Parse intent, read instructions, plan execution, call tools, handle errors.

## Layer 3: Execution (The 'Do')
Scripts in `scripts/`. Deterministic: same input yields same output. MUST have one responsibility per script. MUST be testable independently.

## When to Use Each Layer

| Task Type | Layer |
|---|---|
| Analysis with judgment | L1 + L2 |
| Parse/extract structured data | L3 (script) |
| Route between workflows | L2 |
| Validate structured input | L3 (script) |
| Generate report with recommendations | L1 + L2 |
| Calculate scores from metrics | L3 if complex |

## Rule of Thumb

MUST use a script when:
- Operation is fragile or exact format is required
- Mathematical computation is involved
- Operation is repeated frequently
- Errors are hard to diagnose

MUST use instructions when:
- Judgment is required
- Output varies by context
- Work is creative or analytical

## Key Insight

LLMs are probabilistic. Business logic is deterministic. 90% accuracy per step cascades to 59% over 5 steps. MUST push deterministic work into scripts.
