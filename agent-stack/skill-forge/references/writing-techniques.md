# Conditional Writing Techniques

These techniques address specific failure modes. Apply one when its condition exists; omit it otherwise.

## Dominant Failure and Iron Laws

Identify the most consequential likely failure. Use an Iron Law when one falsifiable absolute constraint prevents it and
reasonable exceptions do not exist.

```text
IRON LAW: Never apply a migration that has no tested rollback path.
```

Do not manufacture a slogan for a skill whose risks require contextual judgment. State those decisions and criteria
directly.

## Questions

Use a question when it directs attention to evidence or a boundary more precisely than a general instruction.

```markdown
Ask: Could the state change between this authorization check and the operation it guards?
```

Include the consequence of each possible answer when it is not obvious.

## Anti-Patterns

Name an anti-pattern when the target models commonly choose it and the choice harms the task. Keep it concrete and place
it beside the positive behavior that should replace it.

```markdown
Parameterize user-controlled SQL values. Never concatenate them into a query string because escaping mistakes become SQL injection.
```

Avoid generic prohibitions, exhaustive catalogs, and rules derived from a single anecdote without evidence that the
failure is likely to recur.
