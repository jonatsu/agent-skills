# Cognitive Walkthrough

Step through one task as a first-time user would, action by action, and predict where they fail. The method
targets learnability for people who use an interface without training. Wharton, Rieman, Lewis, and Polson
described it in their 1994 practitioner's guide.

## Inputs

State these before walking:

- **The user:** who they are, what they know about this kind of interface, and what they know about the task.
- **The task:** the goal in the user's own words, such as "send this invoice to my accountant".
- **The correct action sequence:** every action the design requires, from the starting state to the goal,
  including taps, holds, typing, and waits.

## The Walk

For each action in the sequence, ask four questions. They paraphrase Wharton and colleagues:

1. **Goal:** will the user try to achieve the right effect at this point?
2. **Notice:** will the user see that the correct control or action is available?
3. **Associate:** will the user connect that control with what they want to achieve?
4. **Progress:** after acting, will the user see that they moved toward the goal?

Answer each question with a short, credible story of why the user would succeed. Where no credible success
story exists, record a failure at that action. Then continue the walk as if the user found the way. That way the
walk also finds the failures at later steps.

## Report

The walkthrough report goes through the task in order. Use this shape in place of the general findings list:

```text
Step N: <the action the design requires>
  Goal:      yes / no, and why
  Notice:    yes / no, and why
  Associate: yes / no, and why
  Progress:  yes / no, and why
  Stuck here: <what the user does instead, and the consequence>
  Severity:  0 to 4, with the consequence in words
  Fix:       <a concrete change>
```

After the steps, list the failures worst first, each naming the step where it stops the user. Close with the
confirmation slot: a test with first-time users on this task.

The walk is done when every action in the correct sequence has all four answers, and every "no" has a
consequence and a fix.

## Faster Variant

For a quick pass, Spencer's streamlined walkthrough (2000) asks two questions per action:

1. Will the user know what to do at this step?
2. If the user does the right thing, will they know that it was right, and that they are making progress?

Use it when the user wants speed over depth, and say that you used it.

## Limits

The walkthrough covers learnability for first-time users only. It says little about efficiency for experts,
and it predicts rather than measures. Different evaluators reach different conclusions, so recommend a test with
first-time users on the same task. Give consequences in words, and leave out any predicted success rate or task
time, because the walkthrough cannot measure either.
