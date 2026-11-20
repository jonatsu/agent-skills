---
name: usability
description: Design, evaluate, and review the usability of any interface people operate, from GUIs, web and mobile apps to voice interfaces, device panels, and other human-machine interfaces, using established principles and methods such as heuristic evaluation and cognitive walkthroughs. Use when judging whether an interface is easy to learn and use, finding usability problems in a design or change, or planning a usability evaluation. Use cli-ui-ux for command-line tools and accessibility for WCAG and accessibility audits.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Usability

Judge and shape how easily people learn and use an interface to reach their goals. The interface may be a
screen, a web or mobile app, a voice dialogue, a device panel, or any other human-machine interface. ISO
9241-11:2018 defines usability as an outcome of use. It is how effectively, efficiently, and satisfactorily
specified users reach specified goals in a specified context. Every judgement therefore starts from users, tasks,
and context.

## Which Guidance Applies

When a skill exists for the medium, load it and follow it, because its conventions are more specific. For a
command-line tool or a project's task commands, that is `cli-ui-ux`. Use this skill only for what such a skill
leaves open, and say which skill your report follows.

A usability review does not cover accessibility conformance, such as WCAG. Where the interface has public or
diverse users, recommend an accessibility review, which the `accessibility` skill carries out.

A safety-critical interface follows its own domain's standards and process, which this skill does not replace.
Examples are control rooms (ISO 11064), process-automation human-machine interfaces (ANSI/ISA-101), indicator
and actuator coding (IEC 60073), and medical devices (IEC 62366-1). Name a standard in your report only when you
can verify that it applies.

## Fit the Effort to the Job

Choose the depth before you start, from what the request or the project states. A guess about the audience is
not a statement of it.

- **Quick check.** The user asks for a brief look, such as a quick or rough check. The same holds when the
  user states that only a few known people use the interface. Leave `references/` unread, and write only this:

  1. The answer first: usable enough or not, and what to fix first.
  2. One sentence of assumptions.
  3. The few findings that matter most, each with the problem, its severity and consequence, and the fix.
  4. One sentence naming the test that would confirm them.

  Keep the report short enough to read at a glance, without headings. It still names the medium's skill and the
  domain standard, each when one applies.

- **Full evaluation.** Every other request. Use the method the mode below selects and the full report shape.

An explicit request for a walkthrough always uses the walkthrough, even when it says "quick".

## The Principles

Eight principles summarize where the established sets agree: Nielsen's heuristics, Shneiderman's golden rules,
Norman's design principles, and ISO 9241-110.

1. **Visible status and feedback.** People can see what state the system is in and what their action did.
2. **Match the user's world and conventions.** Words, order, and mappings follow what users already know.
3. **Prevent errors.** The design makes the wrong action hard, and the right one obvious.
4. **Help users recover.** Errors say what went wrong and how to fix it, and work is never lost.
5. **User control.** People can cancel, undo, or leave, and nothing changes without them.
6. **Recognition over recall.** Options, rules, and state are shown, not memorized.
7. **Learnable and efficient.** A first-time user succeeds, and a frequent one has shortcuts.
8. **Minimal.** Each screen, prompt, or display carries only what the current task needs.

Translate each principle into the medium through its interaction dimensions: words, visuals, physical objects
or space, time, and behaviour. Each medium carries a principle in the dimensions it has. A voice interface has no
visuals, so its status lives in words and timing. A washing machine dial carries its state in position and
markings.

Propose fixes that the medium can build. Flag any fix that needs a change to the hardware or platform.
[references/principles.md](references/principles.md) holds each principle's questions per dimension and the
sources behind them.

When users get something wrong, look for the design cause first: a missing signifier, a misleading mapping, or
absent feedback. A door that people push when it must be pulled has a design fault, not a user fault.

## Modes

- **Design**: before the interface exists. Write the design in this order:
  1. The users, their tasks, and the context of use.
  2. The conventions of the medium and platform that the users already know.
  3. For each principle, how each dimension of the medium meets it, using the questions in
     [references/principles.md](references/principles.md).
  4. The open decisions, each with a recommendation.
  5. The evaluation plan from [Confirm With Users](#confirm-with-users).
- **Evaluate**: an existing interface, prototype, or specification. Choose the method by the question:
  - "Is it usable?" or "what should we fix?": a heuristic audit, by
    [references/heuristic-audit.md](references/heuristic-audit.md).
  - "Walk through how a new user would do X" or "where would they get stuck?": a cognitive walkthrough, by
    [references/cognitive-walkthrough.md](references/cognitive-walkthrough.md). Follow its per-action recipe;
    a list of findings ordered by severity is not a walkthrough.
  - "Is this a good experience overall?", beyond ease of use: a holistic review, by
    [references/holistic-review.md](references/holistic-review.md).
- **Review**: a proposed or recent change. Judge what changed and what it touches, with the questions in
  [references/principles.md](references/principles.md). Check that it keeps the interface's existing
  conventions, and that every principle the old version met still holds. Report in the full report shape, with
  findings only about the change.

When a finding rests on a quantitative law, such as Fitts's law or the response-time limits, read
[references/laws.md](references/laws.md) first. Several such laws are commonly misquoted.

## Rate Severity by Consequence

Rate each finding on Nielsen's scale, from what the problem costs the user:

| Rating | Meaning                         |
| ------ | ------------------------------- |
| 0      | Not a usability problem         |
| 1      | Cosmetic; fix if time allows    |
| 2      | Minor; low priority             |
| 3      | Major; high priority            |
| 4      | Catastrophe; fix before release |

Judge three factors: frequency, impact, and persistence. Frequency is how often it occurs, impact is how badly it
hurts when it does, and persistence is whether users overcome it once they know.

State that consequence in words beside the rating. An example: "every caller who asks for an agent is sent back
to the main menu". Order findings by rating, worst first.

Report severity only in this form. A total score, a grade, or a percentage of principles met claims a
measurement nobody made, so leave them out. The same holds for predicted success rates and task times.

## Report Shape

A full evaluation writes the report in this order; a quick check uses its own shape above.

1. **Answer.** One or two sentences: is it usable enough for its users, and what to fix first.
2. **Scope and assumptions.** The users, tasks, and context you assumed, what you examined, and the method.
3. **Findings.** Give each one, worst first, with five parts:
   - where it occurs;
   - what the user experiences;
   - the principle it breaks;
   - the severity, with its consequence;
   - a concrete fix that fits the medium.
4. **Confirm with users.** Which users to test with, which tasks, and what would show each top finding. This
   slot is required in every report, including a quick check, where one sentence fills it.

## Confirm With Users

An expert review predicts problems; only people using the interface confirm them. Say so in every report, and
name the test that would settle the top findings. Different evaluators also find different problems, so one
review is one evaluator's view. For a costly decision, recommend several independent evaluators or a test.

Plan a test this way:

- Recruit people who match the real users: about five per round for one group of users. With two distinct
  groups, test three or four from each; with more groups, three from each (Nielsen, 2000).
- Give them realistic tasks with no hints, and ask them to think aloud.
- Watch where they hesitate, fail, or recover. Record task success, errors, and comments.
- Test again after fixing, because a second round finds what the first fix exposed.
- For a satisfaction measure, use the System Usability Scale (SUS). Its wording may need adapting for a
  device or a voice interface. Read a score against a comparison point, such as the previous version, not as a
  pass mark.

For hardware, test a paper, cardboard, or breadboard prototype before the design is frozen. Changing it
afterwards costs most.

## Attributions

See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for the sources this skill is based on.
