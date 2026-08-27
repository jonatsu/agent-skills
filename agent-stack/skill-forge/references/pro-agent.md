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

## Solve in the script; never defer to the agent

A script that fails and leaves the agent to work out why has moved the problem, not solved
it. MUST handle the failures you can anticipate — missing file, missing permission, absent
dependency — and MUST emit a message that names what to do next, because that message is
the agent's only input for self-correcting without asking the user.

```python
# Good: the failure is handled, and the message is actionable
except FileNotFoundError:
    print(f"{path} not found; creating it with default contents", file=sys.stderr)

# NEVER: fail bare and let the agent guess
return open(path).read()
```

MUST justify every constant in a comment. `TIMEOUT = 47` tells the agent nothing about
whether 47 is safe to change; if you cannot say why the value is what it is, the agent
cannot either.

## Say whether to execute or to read

Every bundled script MUST state which at its point of use. These are different operations
with different costs, and the distinction is invisible from the filename:

- **Execute** (the default): "Run `analyze_form.py` to extract the fields." Only the
  output enters context.
- **Read as reference** (rare): "See `analyze_form.py` for the extraction algorithm." The
  whole file enters context.

## Key Insight

LLMs are probabilistic. Business logic is deterministic. Error compounds across a chain of steps,
so a long agent-driven sequence is less reliable than its per-step accuracy suggests. MUST push
deterministic work into scripts.

The usual illustration — 90% per step giving 0.9^5 = 59% over five steps — is **arithmetic on
assumed inputs, NEVER a measurement.** It holds only if the steps are independent and each is
exactly 90% accurate, and neither condition has been established for any real agent. Use it to
convey the shape of compounding error; NEVER cite it as evidence, and NEVER derive a threshold
from it.
