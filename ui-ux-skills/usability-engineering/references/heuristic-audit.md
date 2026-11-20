# Heuristic Audit

Inspect an interface against the principles and report each violation with its consequence. Nielsen and
Molich introduced the method in 1990. It finds likely problems quickly, and it cannot say whether real users
succeed.

## Steps

1. **State the inputs.** Name the users, their main tasks, and the context of use. The context covers the
   device, the environment, how often they use it, and what a failure costs them. Take the inputs from the
   request and the project's files. Where one is missing, choose a plausible value and list it as an assumption.
2. **Narrow the scope.** Choose the screens, states, or tasks to inspect. A whole product in one pass yields a
   shallow list.
3. **Pass one: learn the flow.** Go through each main task once as the user would. Note the states, modes,
   and messages you meet, including the error and empty states.
4. **Pass two: check each principle.** For every element and state in scope, ask the questions in
   [principles.md](principles.md) for the dimensions the medium has. Record each violation as it appears.
5. **Merge and rate.** Merge duplicates that share one cause. Rate each finding on the severity scale in
   `SKILL.md`, from its frequency, impact, and persistence. A violation that does no harm in this context is a
   0: say why and drop it.
6. **Write the fix.** Give each finding a concrete fix that the medium can build. Where a fix trades against
   another principle, name the trade-off.
7. **Report.** Write the report in the shape `SKILL.md` gives.

The audit is done when three things hold. Every in-scope task has been walked once. Every principle has been
asked of every element in scope. Every finding has a rating, a consequence, and a fix.

## Recording a Finding

Record each finding with these parts, so findings can be merged and ranked:

```text
Where:       the screen, state, control, or step
Problem:     what the user experiences, in their terms
Principle:   the principle it breaks
Severity:    0 to 4, and the consequence in words
Fix:         a concrete change the medium can build
```

## Limits

- One evaluator finds only part of the problems, about a third on average in Nielsen's projects, and Nielsen
  recommends three to five evaluators. Present a single audit as one view. For a costly decision, recommend
  more evaluators or a user test.
- A heuristic violation is not automatically a problem. A convention may break a principle for a good reason,
  so judge it by its consequence for these users.
- One evaluator's severity rating is unreliable, and Nielsen found the mean of three ratings satisfactory. Mark
  a lone rating as provisional.
- The audit predicts. The report's confirmation slot names the test that would confirm the top findings.
