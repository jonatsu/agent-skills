# Writing Techniques for Skills

## Technique 1: The Iron Law

MUST set one unbreakable rule at the top of SKILL.md, right after frontmatter. This prevents the agent from taking shortcuts.

### Examples

```text
IRON LAW: NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.
IRON LAW: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.
IRON LAW: Every migration MUST have a rollback script. No rollback = no execution.
```

### How to Write an Iron Law

Ask: "What is the ONE mistake the agent will most likely make with this skill?"

Then write a rule that prevents it:
- ALL CAPS for emphasis
- Absolute language (`NEVER`, `ALWAYS`, `MUST`)
- No wiggle room

### Red Flag Signals

Pair the Iron Law with red flags that force backtracking:

```markdown
Red Flags (return to Step 1 if any appear):
- "I think the problem might be..." (guessing, not analyzing)
- Making changes without understanding root cause
- Fix works but you cannot explain why
```

## Technique 2: Question-Style Instructions

Give the agent specific questions to answer, not vague directives.

### Examples

```markdown
# Bad - vague directive
Check if the code violates SRP.

# Good - specific question
Ask: How many distinct reasons could this module need to change?
If more than one, it likely violates SRP.
```

```markdown
# Bad
Watch out for race conditions.

# Good
Ask: What happens if two requests hit this code simultaneously?
```

```markdown
# Bad
Handle edge cases properly.

# Good
Ask: What happens if this value is null? Is 0? Is an empty array? Is negative?
```

## Technique 3: Anti-Pattern Documentation

MUST explicitly list what the agent MUST NOT do.

### How to Find Anti-Patterns

Ask: "What would the agent's lazy default look like for this task?" Then MUST explicitly forbid it.

### Examples

```markdown
Anti-Patterns to Avoid:
- Direct SQL string concatenation
- User input inserted into HTML without escaping
- Add unnecessary try-catch blocks with console.log
- Over-abstract one-time operations into utility functions
- Add comments that restate the code
```
MUST keep anti-patterns concrete and specific - not "do not write bad code" but "do not concatenate SQL strings".
