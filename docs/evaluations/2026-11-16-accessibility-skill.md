# Evaluation: the `accessibility` Skill

Date: 2026-11-16. The question was how to give agents an accessibility skill that judges interfaces against
WCAG 2.2 and EN 301 549, beside `usability`, which leaves conformance out. It led to
`ui-ux-skills/accessibility`. The source survey behind it is
[2026-11-16-accessibility-sources.md](2026-11-16-accessibility-sources.md).

## Verdict

`ready with risks`. Without the skill, Sonnet and Opus already find most planted failures, cite criteria, and
give no score. They miss three things: they do not name the screen-reader, keyboard, and user tests that would
confirm their findings, they ask only for "a manual pass" before a conformance claim, and Sonnet advised a
statement of partial conformance for a page with its own failures, which WCAG does not allow. With the skill,
every outcome passed in all ten runs of the final round. The risks are one repetition per cell, one client
(Claude Code), and no case yet for design mode, review mode, the quick check, an AAA target, a document or
native app, or a clean page.

## Decisions Settled With the User

| Decision       | Chosen                                                                                         | Reason                                                        |
| -------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Scope          | Web content and native apps on WCAG 2.2, with EN 301 549 for documents, software, hardware     | WCAG is the shared base; EN 301 549 applies it beyond the web |
| Default target | WCAG 2.2 Level AA; AAA only when the user names it                                             | W3C does not recommend AAA as a general policy                |
| Reuse          | Modes, quick check versus full evaluation, report shape, severity by consequence, eval harness | The `usability` design held up in its own evaluation          |
| Conformance    | No claim from reading code or a scan; partial conformance only where WCAG allows it            | The gaps the control runs showed                              |
| Tests          | Every report ends with the keyboard, screen-reader, zoom, and user tests still needed          | Reading code predicts barriers; testing confirms them         |
| Fixes          | Native elements before ARIA; site navigation as a disclosure, not an ARIA `menu`               | The ARIA Authoring Practices and the rules of ARIA use        |

## Cases

`ui-ux-skills/accessibility/evals/behavior.json` holds five cases with planted problems:

- **a1:** the `usability` u1 sign-up form, plus blocked zoom, a logo with no `alt`, and low-contrast errors.
- **a2:** an account menu built from a `div` with `role="button"`, clickable `li` items, a list hidden with
  `aria-hidden`, and a removed focus outline. The request is to fix it.
- **a3:** an article page with a clean axe scan, whose owner wants a conformance statement. It plants an
  informative chart with `alt="image"` and a required field marked only by colour. Its "click here" links pass
  2.4.4 through their sentences, a trap for over-reporting.
- **a4:** a parking ticket machine specification: touch-only, no speech, a screen centred at 1.6 m, and a
  20-second payment timeout.
- **a5:** a command-line tool that shows status only by colour, which should defer to `cli-ui-ux`. It runs
  only with the skill.

`evals/grade.py` checks the scripted outcomes: no score or count of criteria met for a1 and a3, the fixed
menu's elements and state for a2, and the tool's piped output for a5. It was proven both ways on synthetic
right and wrong answers. The rest were graded from each report and trace.

## Control Runs Without the Skill

Claude Code `general-purpose` subagents ran each case once per model, in its own copy of the fixture, and were
told not to read the accessibility or usability skills.

| Case          | Sonnet                                                                    | Opus                             |
| ------------- | ------------------------------------------------------------------------- | -------------------------------- |
| a1 sign-up    | A4 fails: no screen-reader, keyboard, or user test recommended            | A4 fails: the same               |
| a2 menu fix   | B5 partial: no screen-reader check named for the fix                      | all pass                         |
| a3 clean scan | C3 partial: only "a manual pass"; advises a partial-conformance statement | C3 partial: only "a manual pass" |
| a4 machine    | all pass                                                                  | all pass                         |

## Evaluation With the Skill

The brief gave each run the skill's path, without its `evals/` folder, and the same task. Two rounds ran.
Between them, an independent review on Sonnet checked the skill against its primary sources.

| Case            | Failed without the skill | Sonnet with the skill                               | Opus with the skill                         |
| --------------- | ------------------------ | --------------------------------------------------- | ------------------------------------------- |
| a1 sign-up      | A4 (both)                | all pass; names NVDA, VoiceOver, and disabled users | all pass; the same                          |
| a2 menu fix     | B5 (Sonnet)              | all pass; sign out becomes a button                 | all pass                                    |
| a3 clean scan   | C3 (both)                | all pass; no partial-conformance statement          | all pass; "click here" judged to pass 2.4.4 |
| a4 machine      | none                     | all pass; cites the clause 8.3 limits               | all pass                                    |
| a5 command line | not run                  | all pass; loads `cli-ui-ux`                         | all pass; loads `cli-ui-ux`                 |

The review changed the skill in five ways. The quick-check and full-evaluation split now applies only to an
evaluation, because it had told a fix to audit every criterion. EN 301 549 gained its clause 9.7 on user
preferences, which WCAG lacks, the closed-functionality sub-clauses, and the measured limits for stationary
ICT; in the first round both models had guessed those numbers. WCAG2ICT's unit of evaluation, a whole document
or program, now covers non-web conformance. The 3.3.8 exceptions and the third-party conformance route were
corrected. The grader stopped flagging percentages such as "200 percent zoom" and a disclaimer such as "no
overall score", and started requiring a script that changes `aria-expanded`.

## Remaining Risks

- The a3 step-order item is borderline under 1.3.2, so it is neither required nor penalised.
- Full reports run long, from about 560 to 2,200 words; the cases set no limit outside the quick check.
- The description has no trigger for contrast, alt text, ARIA, or a procurement conformance report.
