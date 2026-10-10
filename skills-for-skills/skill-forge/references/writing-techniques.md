# Writing Techniques

Choose each piece of guidance by the failure it must prevent. The same wording that fixes one kind of failure
makes another worse.

## Match the Form to the Failure

Name the failure first, from a control run or a recorded failure where one exists, then write it in the form
that prevents it:

| Failure                                                        | Form that prevents it                                                                  |
| -------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| The agent knows a rule and skips it when something pushes back | A prohibition, with the reason it exists and the positive action to take instead       |
| The output exists but has the wrong shape                      | A positive recipe: the parts the output contains, in order                             |
| The output lacks one required element                          | A required slot in the template the agent fills in                                     |
| The right behavior depends on the situation                    | A condition keyed to something the agent can observe, stating what to do when it holds |

A prohibition aimed at a shape problem gives the agent something to negotiate with and tends to produce more of
the unwanted content. A recipe leaves nothing to negotiate, since the output matches it or does not.

Write a recipe without nuance clauses. An appended "unless it matters" reopens every item to judgment; express
a real exception as its own condition. An exemption clause does not scope a rule reliably either, so when part
of the output must escape a rule, restructure so the rule cannot reach it.

## State the Reason Beside the Constraint

Give each constraint the agent must apply to unforeseen cases its reason, in the same sentence or the next.
The reason lets the agent extend the rule to a case the author never listed, and it replaces emphasis such as
capitals, which raises attention without saying why. A mechanical fact, such as a field name or an exit status,
needs no reason.

## Iron Laws

Use an Iron Law when one falsifiable absolute constraint prevents the most consequential likely failure and no
reasonable exception exists.

```text
IRON LAW: Never apply a migration that has no tested rollback path.
```

Where the risk needs contextual judgment, state the decisions and criteria directly instead of a slogan.

## Questions

Use a question when it directs attention to evidence or a boundary more precisely than a general instruction.

```markdown
Ask: Could the state change between this authorization check and the operation it guards?
```

Include the consequence of each possible answer when it is not obvious.

## Anti-Patterns

Name an anti-pattern when the target models commonly choose it and the choice harms the task. Keep it concrete
and place it beside the positive behavior that replaces it.

```markdown
Parameterize user-controlled SQL values. Never concatenate them into a query string because escaping mistakes become SQL injection.
```

Keep anti-patterns to failures with evidence of recurrence. A generic prohibition, an exhaustive catalog, or a
rule drawn from one anecdote adds load without preventing a likely failure.
