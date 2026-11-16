# Conformance and Full Evaluation

## The Five Conformance Requirements

A web page conforms to WCAG 2.2 only when it meets all five:

1. **Level.** It meets every criterion of the claimed level and the levels below it in full, or provides a
   conforming alternate version.
2. **Full pages.** Conformance covers whole pages, including every variation the page shows for different
   screen sizes. Excluding part of a page makes the claim impossible.
3. **Complete processes.** When a page is one step of a process, such as a checkout, every page of the process
   conforms.
4. **Accessibility-supported technologies only.** Content that relies on a technology in a way assistive
   technology does not support must also be available in a way it does.
5. **Non-interference.** Technologies used in a non-conforming way do not block the rest of the page. Four
   criteria apply to all content on the page, relied upon or not: 1.4.2 Audio Control, 2.1.2 No Keyboard Trap,
   2.3.1 Three Flashes or Below Threshold, and 2.2.2 Pause, Stop, Hide.

A criterion that does not apply to the content, such as captions on a page with no video, is satisfied.

## What a Claim Contains

A conformance claim is optional. When one is made, it must state:

- the date of the claim;
- the guidelines' title, version, and address: "Web Content Accessibility Guidelines 2.2 at
  <https://www.w3.org/TR/WCAG22/>";
- the level met;
- the pages it covers, such as a list of addresses, and whether subdomains are included;
- the web content technologies relied upon.

A conformance logo is itself a claim and needs the same parts. A claim may also list extra criteria met and the
browsers and assistive technologies used for testing.

## Partial Conformance

WCAG defines two statements of partial conformance and no others:

- for third-party content the author does not control, such as user comments, stating that the page would
  conform if that content were removed;
- for content in a language that assistive technology does not yet support.

A partial-conformance statement begins "This page does not conform, but would conform to WCAG 2.2 at level X if
…", and identifies the content that does not conform so users can recognise it. Third-party content has a
second route: when the page is monitored and non-conforming content is repaired or removed within two business
days, a conformance claim may rest on that monitoring.

A page that fails a criterion in its own content does not conform. Say that, list the failures, and give the
plan to fix them.

## Accessibility Statements

An accessibility statement is broader than a conformance claim: it may say what does not yet conform, why, and
when it will be fixed. Write it from a full evaluation. When the law requires a statement, as the EU Web
Accessibility Directive does for public sector bodies, follow its required content too.

## Full Evaluation: WCAG-EM 2.0

The W3C's WCAG Evaluation Methodology (WCAG-EM) 2.0, a Group Note of 23 July 2026, applies to websites, apps,
and other digital products. Follow its five steps:

1. **Define the scope:** the product, the conformance target, the browsers and assistive technologies to
   support, and any extra requirements.
2. **Explore the product:** its common views, essential functions, kinds of page, and the technologies it
   relies on.
3. **Select a sample:** a structured sample covering the above, every complete process with its main and
   critical branches, and a random sample of about 10 percent more. Evaluate everything when the product is
   small.
4. **Evaluate the sample** against every criterion at the target level, including each complete process.
   Compare the random sample with the structured one; when it shows new kinds of content or failures, add
   samples.
5. **Report** the outcome of each step, with the evidence for each finding.

The evaluation is done when every sampled page and process has a result for every criterion at the target
level.
