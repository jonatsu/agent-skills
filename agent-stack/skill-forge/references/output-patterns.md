# Output Patterns

## Template Pattern

Provide output templates to ensure consistency across runs.

### Strict Templates

When exact format matters:

```markdown
## Output Format

For each issue found, output:

| Field | Format |
|-------|--------|
| severity | P0 / P1 / P2 / P3 |
| location | file:line |
| description | One sentence explaining the problem |
| suggestion | One sentence with the fix |
```

### Flexible Templates

When structure matters but content varies:

```markdown
## Output Structure

1. **Summary** (2-3 sentences)
2. **Details**: most important first
3. **Next Steps**: actionable, prioritized
```

## Example Pattern

Show input/output pairs to demonstrate style and detail level.

```markdown
## Comment Style

Bad: "This function is too long."
Good: "P1: `processOrder()` (142 lines) handles validation, payment, and notification. Split into `validateOrder()`, `processPayment()`, `sendNotification()`."
```

## Pre-Delivery Checklist Pattern

Every checklist item MUST be specific and verifiable - not subjective.

```markdown
# Bad
- [ ] Ensure good quality
- [ ] Make sure it looks nice

# Good
- [ ] No placeholder text remaining (TODO, FIXME, xxx)
- [ ] All generated code runs without errors
- [ ] Color contrast ratio meets WCAG AA (4.5:1 for text)
```
