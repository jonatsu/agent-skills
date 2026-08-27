# Skill Workflow Patterns

## Patterns

### 1. Sequential Workflow
Steps execute in order; each step's output feeds the next.
```
Step A → Step B → Step C
```
Use when: output of step N is required input for step N+1.

### 2. Command Routing
A main skill dispatches to sub-skills via a routing table.
```
Routing Table: intent → sub-skill
"install"  → install-skill
"configure" → config-skill
"validate"  → validation-skill
```
Use when: one skill MUST support multiple distinct operations.

### 3. Parallel Delegation
Spawn independent subagents, collect results.
```
Subagent A ─┐
Subagent B ─┤→ Aggregate → Final
Subagent C ─┘
```
Use when: tasks are independent and can execute concurrently.
MUST aggregate results before returning.

### 4. Iterative Refinement
Generate → Evaluate → Improve loop, repeating until criteria met.
```
Draft → Score → Revise → Score → ... → Final
```
Use when: quality improves with cycles and evaluation exists.

### 5. Context Detection
Detect the type of input or environment, apply type-specific handling.
```
Input → Detector → [Type A path | Type B path | Type C path]
```
Use when: behavior MUST vary based on context characteristics.

### 6. Scoring & Reporting
Compute weighted scores across categories, report at priority levels.
```
Categories × Weights → Aggregate Score → [Critical | Warning | OK]
```
Use when: a multi-dimensional quality or health signal is required.

### 7. Template Selection
Match context to a template, fill fields, return result.
```
Context → Selector → [Template A | Template B] → Filled
```
Use when: output structure is predictable from input type.

### 8. Graceful Degradation
Detect unavailable tools or agents, substitute alternatives.
```
Try Primary → [Success → Return] [Failure → Try Fallback → ...]
```
Use when: tools or agents may be missing at runtime.
MUST NOT assume all dependencies are present.

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| The Monolith | Everything in one skill doc | Split into focused references |
| Vague Directive | "Analyze and provide insights" | Specific steps, criteria, output format |
| Over-Engineered | Unnecessary sub-skills for simple tasks | Start simple; add complexity only when required |
| Silent Failure | No error handling or fallback paths | Add "If X fails, then Y" branches explicitly |
| Tool Assumption | Assumes required tools are always available | Check availability at runtime; provide fallbacks |
