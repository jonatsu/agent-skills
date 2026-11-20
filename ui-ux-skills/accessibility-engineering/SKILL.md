---
name: accessibility-engineering
description: Design, evaluate, review, and fix interfaces for accessibility against WCAG 2.2, by default at Level AA, for web content and native apps, with EN 301 549 for non-web software, documents, and hardware such as kiosks. Use when checking whether a page, app, component, or device meets WCAG or accessibility requirements, fixing barriers for keyboard or screen reader users, preparing an accessibility statement, or planning accessibility testing. Use usability-engineering for general ease of use and cli-ui-ux for command-line tools.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Accessibility Engineering

Make interfaces usable by disabled people, and judge them against the requirements that define that. Judge web
content and native apps against the Web Content Accessibility Guidelines (WCAG) 2.2. Judge other software,
documents, and hardware against EN 301 549. The default target is WCAG 2.2 Level AA, which means every Level A
and AA success criterion. Use Level AAA only when the user names it, because W3C does not recommend AAA as a
general policy.

## Which Guidance Applies

When a skill exists for the medium, load it as well, because its conventions are more specific. For a
command-line tool, load `cli-ui-ux`. Its conventions include colour that never carries meaning alone, output
that works without a terminal, and no animation in a pipe. General ease of use belongs to `usability-engineering`.

When the user names a law or a contract, check which WCAG version and level it cites before you judge.
[references/standards.md](references/standards.md) holds the versions the main regulations cite, and how EN
301 549 applies WCAG beyond the web.

## Fit the Evaluation to the Request

An evaluation takes one of two depths. Design, review, and fix work keep to their own scope, set in
[Modes](#modes).

- **Quick check.** The user asks for a brief look, such as a quick or rough check, or names one component.
  Report the barriers you find and the test that would confirm them, in under 300 words. A quick check never
  supports a conformance claim, so say so.
- **Full evaluation.** Every other evaluation request. Cover every criterion at the target level for the pages,
  screens, or processes in scope. Use the full report shape.

## Rules for Every Mode

### Claim Conformance Only From a Full Evaluation

Conformance belongs to full pages and complete processes, never to a component or a code reading. A page
conforms only when it meets all five WCAG conformance requirements. A checkout or sign-up flow conforms only
when every page in it does. For a document or software, the unit is the whole document or the whole program.
Reading the source, or a clean automated scan, cannot show conformance, because many criteria need human
judgement and testing with assistive technology.

- When you find a failure, state that the page does not conform at the target level. List the failures.
- When you find none, say what you checked and what still needs checking. Never write "conforms" or
  "compliant" on that evidence.
- WCAG allows a statement of partial conformance only for third-party content the author does not control,
  or for languages without accessibility support. A page with its own failures does not partially conform; it
  does not conform.

[references/conformance.md](references/conformance.md) holds the five requirements, what a claim must contain,
and the method for a full evaluation.

### Read Each Criterion Exactly

Judge a finding by the criterion's normative text, at its stated level. The Understanding and Techniques
documents are informative: a technique is one way to pass, and a failure example is not an automatic fail.
Cite each finding by number, name, and level, such as "1.4.3 Contrast (Minimum), AA". Where a case is
borderline, say so and give both readings. Check thresholds and new criteria in
[references/wcag-22.md](references/wcag-22.md) before you cite them, because several are commonly misquoted.

### Fix With Native Elements First

Use the native element with the needed role and keyboard behaviour, such as `button`, `a href`, `input`,
`select`, or `details`. Add ARIA only where no native element exists, and then supply every behaviour the role
promises. An ARIA role changes what assistive technology announces, not how the control works. A link goes
somewhere and a button does something, so an action such as signing out is a button. Keep every focusable
element exposed to assistive technology: never put `aria-hidden="true"` or `role="presentation"` on one. Site
navigation is a disclosure, a button that shows a list of links, not an ARIA `menu`.

### Name the Tests That Confirm It

Reading code and running scanners predicts barriers; testing confirms them. Every report, including a quick
check and a fix, ends by naming the tests still needed:

- keyboard only, with focus visible at every step;
- a screen reader with its usual browser, such as NVDA or JAWS with Chrome, and VoiceOver with Safari;
- zoom to 200 percent, and reflow at 320 CSS pixels wide;
- testing with disabled users, for any interface the public uses.

Name only the tests that apply to the medium. [references/testing.md](references/testing.md) holds the manual
checks, what automated tools can and cannot find, and how to involve users.

## Modes

- **Design**: before the interface exists. List the users' ways of perceiving and operating it: sight,
  hearing, touch, speech, a keyboard, a switch, or a screen reader. For each, decide how the design meets the
  criteria at the target level. End with the test plan.
- **Evaluate**: an existing page, app, document, or device. Check every criterion at the target level within
  the scope, and report in the shape below.
- **Review**: a proposed or recent change. Check what changed and what it touches, at the target level, and
  that no barrier came back. Report the findings in the five parts below, then the tests.
- **Fix**: change the code by the rules above. Report what you changed, with the criterion each change
  meets, the barriers that remain, and the tests.

## Rate Severity by Consequence

Rate each finding by who it blocks and how badly, and state that consequence in words:

| Severity | Meaning                                                     |
| -------- | ----------------------------------------------------------- |
| Blocker  | Some users cannot complete the task at all                  |
| Major    | The task is possible only with great effort or outside help |
| Minor    | The task works, with avoidable difficulty                   |

The criterion's level states the requirement, and the severity states its consequence; report both. Use words,
not a score, a grade, or a percentage of criteria met, because those claim a measurement nobody made.

## Report Shape

An evaluation reports in four parts:

1. **Answer.** Whether it meets the target, and what to fix first. One failure makes the answer "does not
   conform".
2. **Scope and method.** The target version and level, what you examined, and how: source reading, a scan, or
   testing.
3. **Findings.** Give each one, worst first, with five parts:
   - where it occurs;
   - who it blocks, and how;
   - the criterion by number, name, and level;
   - the severity, with its consequence;
   - a concrete fix.
4. **Tests still needed.** The tests from [Name the Tests That Confirm It](#name-the-tests-that-confirm-it).

## Attributions

See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for the sources this skill is based on.
