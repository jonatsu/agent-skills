# Accessibility skill: source survey

Date: 2026-11-16. Prepared for the accessibility skill (WCAG 2.2 on web and native apps, Level AA default, plus a short
non-web section based on EN 301 549). This file is the research notes and the survey in one. It is not part of the
skill.

## 0. How to read this file

Three facts that changed in 2026 were rechecked against the originals: WCAG-EM 2.0 (the W3C Note page of 23 July
2026), EN 301 549 V4.1.1 (the ETSI deliverable directory, dated 2 September 2026), and the ADA Title II extension
(91 FR 20902, published 20 April 2026).

Reading routes. "Original" means I read the standard, regulation or report itself. "Via summary" means a fetch tool
summarised the original page with a small model, so figures and wording are paraphrases I could not check character by
character. "Secondary" means a source that cites the original.

| Source                                                                                            | How I read it                                                                                                                                                                               |
| ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| WCAG 2.2 success criteria, conformance text                                                       | Original: raw W3C source files at tag `WCAG22-20241212` (commit `1dfe1647bd`), the same date as the Recommendation. Names and levels cross-checked against the EN 301 549 V4.1.1 AAA table. |
| WCAG 2.2, WCAG 3, WCAG-EM 2.0, WCAG2ICT, WCAG2Mobile, Using ARIA, ARIA in HTML, W3C history pages | Via summary (`WebFetch`). W3C pages block `docs-mcp` and `crawl4ai`.                                                                                                                        |
| EN 301 549 V4.1.1                                                                                 | Original: ETSI PDF, pages 1 to 12, 61 to 62, 69 to 71, 78 to 79, 86 to 87, 95.                                                                                                              |
| WebAIM Million 2026, WebAIM Screen Reader Survey 11                                               | Original (full page text).                                                                                                                                                                  |
| GDS tool audit (blog and audit page)                                                              | Original (full page text).                                                                                                                                                                  |
| Deque coverage report                                                                             | Via summary, and it is vendor marketing.                                                                                                                                                    |
| Vigo et al. 2013                                                                                  | Via summary of the repository abstract. The paper itself was not read.                                                                                                                      |
| eCFR (28 CFR 35.200, 36 CFR 1194 App. A, 45 CFR 84.84), Federal Register API                      | Original text.                                                                                                                                                                              |
| EUR-Lex (Directive 2019/882, Directive 2016/2102, Decision 2021/1339)                             | Original text via a stealth browser; `crawl4ai`, `docs-mcp` and `WebFetch` returned empty pages.                                                                                            |
| ISO page for ISO/IEC 40500                                                                        | Not read (HTTP 403). Facts come from ETSI, W3C and search snippets.                                                                                                                         |
| Apple accessibility pages                                                                         | Not readable (JavaScript-rendered, empty). Named as pointers only.                                                                                                                          |
| Third-party skills                                                                                | Repository trees and the first part of key files, at the commit named in section 7.                                                                                                         |

Important: the date of this survey is late 2026, and several facts changed during 2025 and 2026. EN 301 549 has a new
version, WCAG-EM has a new version, and "Using ARIA" has been discontinued. Do not use older memory of these.

## 1. WCAG 2.2

### 1.1 Version and status

- WCAG 2.2 is a W3C Recommendation dated 12 December 2024. First published 5 October 2023, republished 12 December 2024.
  Errata exist at `https://www.w3.org/WAI/WCAG22/errata/`. Latest version URL: `https://www.w3.org/TR/WCAG22/`. Editors:
  Alastair Campbell, Chuck Adams, Rachael Bradley Montgomery, Michael Cooper, Andrew Kirkpatrick. (via summary; the date
  also matches the source tag and `publishDate: 2024-12-12` in the source build configuration, original.)
- WCAG 2.2 has 86 success criteria: 31 at Level A, 24 at AA, 31 at AAA. I counted these from the source files; the AAA
  count (31) equals the table in EN 301 549 V4.1.1, clause 9.5.
- The 13 guidelines and 4 principles are unchanged from WCAG 2.1.
- WCAG 2.2 keeps backward compatibility. The Recommendation says pages that conform to 2.2 are at least as accessible as
  pages that conform to 2.1, and that sites conforming to 2.2 "also conform to WCAG 2.0 and WCAG 2.1". It adds one
  caveat: authors required by policy to meet 2.0 or 2.1 "may need to continue to test and report 4.1.1".
- The Working Group "recommends that sites adopt WCAG 2.2 as their new conformance target, even if formal obligations
  mention previous versions".
- New success criteria were appended to the end of each guideline, so criteria within a guideline are not ordered by
  level. The order says nothing about the level. Only the A, AA or AAA marker does.

### 1.2 Success criteria by guideline

Names are as the Recommendation states them. "New" marks the nine criteria added in 2.2.

#### Principle 1: Perceivable

1.1 Text Alternatives

- 1.1.1 Non-text Content (A)

1.2 Time-based Media

- 1.2.1 Audio-only and Video-only (Prerecorded) (A)
- 1.2.2 Captions (Prerecorded) (A)
- 1.2.3 Audio Description or Media Alternative (Prerecorded) (A)
- 1.2.4 Captions (Live) (AA)
- 1.2.5 Audio Description (Prerecorded) (AA)
- 1.2.6 Sign Language (Prerecorded) (AAA)
- 1.2.7 Extended Audio Description (Prerecorded) (AAA)
- 1.2.8 Media Alternative (Prerecorded) (AAA)
- 1.2.9 Audio-only (Live) (AAA)

1.3 Adaptable

- 1.3.1 Info and Relationships (A)
- 1.3.2 Meaningful Sequence (A)
- 1.3.3 Sensory Characteristics (A)
- 1.3.4 Orientation (AA)
- 1.3.5 Identify Input Purpose (AA)
- 1.3.6 Identify Purpose (AAA)

1.4 Distinguishable

- 1.4.1 Use of Color (A)
- 1.4.2 Audio Control (A)
- 1.4.3 Contrast (Minimum) (AA)
- 1.4.4 Resize Text (AA)
- 1.4.5 Images of Text (AA)
- 1.4.6 Contrast (Enhanced) (AAA)
- 1.4.7 Low or No Background Audio (AAA)
- 1.4.8 Visual Presentation (AAA)
- 1.4.9 Images of Text (No Exception) (AAA)
- 1.4.10 Reflow (AA)
- 1.4.11 Non-text Contrast (AA)
- 1.4.12 Text Spacing (AA)
- 1.4.13 Content on Hover or Focus (AA)

#### Principle 2: Operable

2.1 Keyboard Accessible

- 2.1.1 Keyboard (A)
- 2.1.2 No Keyboard Trap (A)
- 2.1.3 Keyboard (No Exception) (AAA)
- 2.1.4 Character Key Shortcuts (A)

2.2 Enough Time

- 2.2.1 Timing Adjustable (A)
- 2.2.2 Pause, Stop, Hide (A)
- 2.2.3 No Timing (AAA)
- 2.2.4 Interruptions (AAA)
- 2.2.5 Re-authenticating (AAA)
- 2.2.6 Timeouts (AAA)

2.3 Seizures and Physical Reactions

- 2.3.1 Three Flashes or Below Threshold (A)
- 2.3.2 Three Flashes (AAA)
- 2.3.3 Animation from Interactions (AAA)

2.4 Navigable

- 2.4.1 Bypass Blocks (A)
- 2.4.2 Page Titled (A)
- 2.4.3 Focus Order (A)
- 2.4.4 Link Purpose (In Context) (A)
- 2.4.5 Multiple Ways (AA)
- 2.4.6 Headings and Labels (AA)
- 2.4.7 Focus Visible (AA)
- 2.4.8 Location (AAA)
- 2.4.9 Link Purpose (Link Only) (AAA)
- 2.4.10 Section Headings (AAA)
- 2.4.11 Focus Not Obscured (Minimum) (AA), new
- 2.4.12 Focus Not Obscured (Enhanced) (AAA), new
- 2.4.13 Focus Appearance (AAA), new

2.5 Input Modalities

- 2.5.1 Pointer Gestures (A)
- 2.5.2 Pointer Cancellation (A)
- 2.5.3 Label in Name (A)
- 2.5.4 Motion Actuation (A)
- 2.5.5 Target Size (Enhanced) (AAA)
- 2.5.6 Concurrent Input Mechanisms (AAA)
- 2.5.7 Dragging Movements (AA), new
- 2.5.8 Target Size (Minimum) (AA), new

#### Principle 3: Understandable

3.1 Readable

- 3.1.1 Language of Page (A)
- 3.1.2 Language of Parts (AA)
- 3.1.3 Unusual Words (AAA)
- 3.1.4 Abbreviations (AAA)
- 3.1.5 Reading Level (AAA)
- 3.1.6 Pronunciation (AAA)

3.2 Predictable

- 3.2.1 On Focus (A)
- 3.2.2 On Input (A)
- 3.2.3 Consistent Navigation (AA)
- 3.2.4 Consistent Identification (AA)
- 3.2.5 Change on Request (AAA)
- 3.2.6 Consistent Help (A), new

3.3 Input Assistance

- 3.3.1 Error Identification (A)
- 3.3.2 Labels or Instructions (A)
- 3.3.3 Error Suggestion (AA)
- 3.3.4 Error Prevention (Legal, Financial, Data) (AA)
- 3.3.5 Help (AAA)
- 3.3.6 Error Prevention (All) (AAA)
- 3.3.7 Redundant Entry (A), new
- 3.3.8 Accessible Authentication (Minimum) (AA), new
- 3.3.9 Accessible Authentication (Enhanced) (AAA), new

#### Principle 4: Robust

4.1 Compatible

- 4.1.1 Parsing (Obsolete and removed). Listed in the table of contents but no longer a requirement.
- 4.1.2 Name, Role, Value (A)
- 4.1.3 Status Messages (AA)

New in 2.2 at A or AA (six): 2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8. New at AAA (three): 2.4.12, 2.4.13, 3.3.9.
Removed: 4.1.1. The Recommendation gives the reason: assistive technology "no longer has any need to directly parse
HTML".

### 1.3 Normative thresholds the skill will want to get right

Read from the success-criterion source files at the tag above (original). These are normative wording, shortened.

- 1.4.3: text contrast at least 4.5:1; large-scale text at least 3:1. No requirement for incidental text (inactive
  components, pure decoration, invisible text) or logotypes.
- 1.4.4: text can be resized without assistive technology up to 200 percent without loss of content or function.
- 1.4.10: no two-dimensional scrolling at 320 CSS pixels wide (vertical-scrolling content) or 256 CSS pixels high
  (horizontal-scrolling content). The criterion says 320 CSS pixels equals a 1280 pixel viewport at 400 percent zoom.
  Exceptions: content that needs a two-dimensional layout (maps, diagrams, video, games, data tables, toolbars kept in
  view).
- 1.4.11: user interface components, their states, and graphical objects need at least 3:1 against adjacent colors.
- 1.4.12: no loss when line height is at least 1.5, paragraph spacing at least 2, letter spacing at least 0.12 and word
  spacing at least 0.16 times the font size. The content does not have to use these values.
- 2.4.11: a focused component is not entirely hidden by author-created content.
- 2.4.13 (AAA): focus indicator area at least a 2 CSS pixel thick perimeter, with 3:1 contrast between focused and
  unfocused pixels.
- 2.5.8: pointer targets at least 24 by 24 CSS pixels, with five exceptions (spacing, equivalent control, inline, user
  agent control, essential). The Enhanced criterion 2.5.5 is AAA.
- 2.5.7: anything that needs dragging can also be done with a single pointer without dragging.
- 3.2.6: help mechanisms repeated across a set of pages appear in the same relative order.
- 3.3.7: information the user already entered in the same process is auto-populated or selectable, with exceptions
  (essential, security, no longer valid).
- 3.3.8: no cognitive function test (such as remembering a password or solving a puzzle) in authentication unless an
  alternative, an assisting mechanism, object recognition or personal content is available.
- 4.1.2: standard HTML controls already meet this criterion when used according to specification.

### 1.4 Conformance

Original: conformance section of the Recommendation, source at the tag above.

A web page conforms only when all five requirements are met.

1. Conformance level. One level is met in full: A, AA or AAA. Level AA means all A and AA criteria are satisfied, or a
   Level AA conforming alternate version is provided. Authors are encouraged to report progress beyond their level. The
   text says "It is not recommended that Level AAA conformance be required as a general policy for entire sites because
   it is not possible to satisfy all Level AAA success criteria for some content."
2. Full pages. Conformance is for full pages only and cannot be reached if part of a page is excluded. Alternatives
   obtainable directly from the page count as part of it. Every variation a page automatically presents for different
   screen sizes must conform.
3. Complete processes. When a page is one of a series of pages in a process, all pages in the process conform at the
   stated level or better. The example is checkout in an online store.
4. Only accessibility-supported ways of using technologies. Content that is not provided in an accessibility-supported
   way must also be available in a way that is.
5. Non-interference. Technologies used in a non-conforming way must not block access to the rest of the page. The page
   must still conform with any non-relied-upon technology turned on or off. Four criteria apply to all content on the
   page whether or not it is relied upon: 1.4.2 Audio Control, 2.1.2 No Keyboard Trap, 2.3.1 Three Flashes or Below
   Threshold, 2.2.2 Pause, Stop, Hide.

Conformance claims are optional. A claim must contain: the date; the guidelines title, version and URI ("Web Content
Accessibility Guidelines 2.2 at <https://www.w3.org/TR/WCAG22/>"); the level; a concise description of the pages covered
(such as a list of URIs, and whether subdomains are included); and a list of the web content technologies relied upon. A
conformance logo is itself a claim and needs these components. Optional components include extra criteria met,
technologies used but not relied upon, and the user agents and assistive technologies used for testing.

Two partial-conformance statements exist: one for third-party content the author does not control (and a
monitoring-and-repair option within two business days), and one for language accessibility support.

Conformance is defined only for web pages. For software, documents and apps, the W3C Note WCAG2ICT (section 4.1) and EN
301 549 translate the rules. See section 4.

### 1.5 Understanding and Techniques

- The Recommendation text says material marked non-normative, examples, notes and introductions are informative. The
  "WCAG 2.2 Supporting Documents" paragraph lists How to Meet WCAG 2.2 (quick reference), Understanding WCAG 2.2,
  Techniques for WCAG 2.2 and What's New in 2.2 as documents "based on" the Recommendation, built so they can be updated
  when technologies change. (Original.)
- Understanding WCAG 2.2 calls itself "Informative explanations, not required to meet WCAG" and "not part of the
  'normative' WCAG standard". Page dated 11 February 2026. (Via summary.)
- Techniques for WCAG 2.2: "not required to meet WCAG". Content can satisfy the criteria without using any documented
  technique. A failure technique shows an example of failing a criterion; content may still pass if equivalent
  alternative content meets the normative text. Page dated 11 May 2026. (Via summary.)
- Result: only the Recommendation text is normative. Understanding and Techniques are advisory. A technique is not a
  requirement, and a failure example is not an automatic fail.

### 1.6 WCAG 3

- W3C Accessibility Guidelines (WCAG) 3.0 is a W3C Working Draft dated 10 September 2026
  (`https://www.w3.org/TR/2026/WD-wcag-3.0-20260910/`). The history page lists ten drafts since the First Public Working
  Draft of 21 January 2021; the previous ones were 3 March 2026, 4 September 2025, 12 December 2024. (Via summary, two
  W3C pages agree.)
- The document says "WCAG 3 does not replace WCAG 2", that it is a successor to WCAG 2.2 without deprecating WCAG 2,
  that it "still has several years of work", and that it is "inappropriate to cite this document as other than a work in
  progress".
- Consequence for the skill: target WCAG 2.2. Mention WCAG 3 only as a draft that cannot be used for conformance.

## 2. Evaluation method

### 2.1 WCAG-EM

- Status changed in 2026. WCAG Evaluation Methodology (WCAG-EM) 2.0 is a W3C Group Note dated 23 July 2026
  (`https://www.w3.org/TR/2026/NOTE-wcag-em-2-20260723/`; editors Hidde de Vries, Jeroen Hulscher, Steve Faulkner). It
  builds on WCAG-EM 1.0 (2014), applies to apps and other digital products as well as websites, and does not change WCAG
  requirements. The WAI page (updated 12 August 2026) keeps 1.0 available but does not say 2.0 supersedes it. A Group
  Note is not endorsed by W3C as a whole. (Via summary; the TR page, the W3C history page and the WAI page agree.)
- Steps and sub-steps, as the Note titles them:
  - Step 1 Define the evaluation scope: 1.1 scope of the digital product; 1.2 conformance target; 1.3 an accessibility
    support baseline; 1.4 additional requirements (optional).
  - Step 2 Explore the target digital product: 2.1 common views; 2.2 essential functionality; 2.3 variety of sample
    types; 2.4 technologies relied upon; 2.5 other relevant samples.
  - Step 3 Select a representative sample set: 3.1 structured sample set; 3.2 randomly selected sample set; 3.3 complete
    processes.
  - Step 4 Evaluate the selected sample set: 4.1 check all initial samples; 4.2 check all complete processes; 4.3
    compare structured and random sample sets.
  - Step 5 Report the evaluation findings: 5.1 document the outcomes of each step; 5.2 record evaluation specifics; 5.3
    evaluation statement; 5.4 aggregated score; 5.5 machine-readable reports. Only 5.1 is required.
- Sampling: a structured sample covers common views, essential functionality, sample types and technologies. A random
  sample of 10 percent of the structured set is added on top (80 structured plus 8 random gives 88). Random samples must
  be unique and not already in the structured set. The selection method is recorded. Each complete process is included
  with its start, default sequence and critical branch sequences. If the random sample reveals new content types or
  findings, return to step 3 and add samples. Sampling can be skipped when the whole product is small or can be
  evaluated in full. Sample size depends on size, age, complexity, consistency, development process, needed confidence
  and earlier findings.
- WCAG-EM 1.0 (2014) is the earlier method; I did not read it. Its step list is not needed because 2.0 replaces it in
  practice, but this is an inference.

### 2.2 What automated tools can and cannot detect

Four measured or published sources. They use different definitions of "detect", so the figures do not compare directly.

| Source                                                                                                             | Method                                                                                                                                                             | Figure                                                                                                                                                                                                                                                                                                                                                                                                | Caveats                                                                                                                                                                                                                |
| ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GDS (UK Government Digital Service) tool audit, blog 24 Feb 2017, audit page last updated 13 April 2018. Original. | The team built a test page with deliberate failures (142 on the audit page; 143 in the 2017 blog) and ran 13 tools (10 in the blog).                               | Pass or fail detection: best tool 40 percent, worst 13 percent. Counting items a tool flagged for manual check: best 50 percent. In the 2017 blog, 42 of 143 barriers (29 percent) were missed by all 10 tools; Tenon found 37 percent, Asqatasun 41 percent counting manual prompts, Google Accessibility Developer Tools 17 percent. The blog also says 71 percent were found by at least one tool. | Synthetic page, not real sites. Tools are 2018 versions (axe was tested before axe 3.0). Commenters (Wilco Fiers, Steve Green) argued the page misses complex widgets, so results may overstate real-world detection.  |
| Vigo, Brown and Conway, W4A 2013 (peer reviewed). Via summary of the repository abstract.                          | Six automated tools tested against WCAG 2.0.                                                                                                                       | Coverage: at most 50 percent of success criteria. Completeness: 14 to 38 percent. Correctness: 66 to 71 percent for the tools with the higher completeness, because catching more also produces more false positives.                                                                                                                                                                                 | Old tool versions. I did not read the paper.                                                                                                                                                                           |
| Deque Automated Accessibility Coverage Report (2021). Via summary. **Vendor marketing**, by the maker of axe.      | Anonymised first audits from the vendor's customers, HTML only, WCAG 2.0 and 2.1 A and AA. Counted issues the axe-core rules reported with no manual verification. | 57.38 percent of issues by volume (169,242 of 294,958). Sample "13,000+ pages/page states", "nearly 300,000 issues". By criterion count the report states automation found issues for 16 of the 50 WCAG 2.1 AA criteria and says that supports the older "20 to 30 percent" figure.                                                                                                                   | Study period not stated; the page also cites "over 2,000 audits" without reconciling the counts. The vendor sells the tool. Counting by issue volume favours frequent, easy-to-detect issues such as missing alt text. |
| WebAIM Million 2026 (Feb 2026 data). Original.                                                                     | WAVE automated scan of 1,000,000 home pages.                                                                                                                       | 95.9 percent of pages had at least one detected WCAG 2 failure. Average 56.1 detected errors per page. 96 percent of errors fall into six categories.                                                                                                                                                                                                                                                 | The report states that "absence of detected errors does not indicate that a page is accessible or conformant." It is a measure of what is found, not of detection coverage.                                            |

One third-party skill README (zivtech, section 7) says "axe-core finds roughly 30 to 40 percent of WCAG issue types". It
gives no source. I did not use it as evidence.

Safe statement for the skill, supported by the first three sources: automated tools find a minority to a modest majority
of issues depending on how you count, they do not replace manual and assistive-technology testing, and a clean automated
run proves nothing. Never give one number without its method.

### 2.3 Manual and assistive-technology testing

- Keyboard-only: W3C "Easy Checks" (updated 21 March 2024, via summary) lists Visible Keyboard Focus among eight common
  checks (Image Alternative Text, Page Title, Headings, Color Contrast, Skip Link, Visible Keyboard Focus, Language of
  Page, Zoom) plus captions, transcripts, audio description, labels and required fields. It says the checks are
  "designed to be quick and easy, rather than exhaustive". The criteria involved are 2.1.1, 2.1.2, 2.4.3, 2.4.7, 2.4.11
  and 2.1.4.
- Zoom and reflow: criteria 1.4.4 (200 percent), 1.4.10 (320 by 256 CSS pixels) and 1.4.12 (text spacing), with the
  numbers in section 1.3.
- GOV.UK Service Manual, "Testing for accessibility" (last updated 29 October 2024, original): meet WCAG 2.2 AA as a
  minimum; use automated and manual testing, because "you'll miss some issues if you only do automated testing"; test
  with the most common assistive technologies; test with disabled users and older users; get an accessibility audit
  before public beta.
- W3C "Involving Users in Evaluating Web Accessibility" (updated 30 April 2024, via summary): involve a small group of
  people with disabilities, informally and throughout development. It identifies usability problems that conformance
  evaluation misses, but "that alone cannot determine if a website is accessible". One person's experience does not
  represent everyone with that disability. Reports should state scope, methods and participant characteristics.
- Which screen reader goes with which browser. The best measured source is WebAIM Screen Reader User Survey 11 (July to
  August 2026, 1,780 responses, original). WebAIM warns the sample was not controlled and may not represent all screen
  reader users. 94.8 percent of respondents use a screen reader because of a disability.

| Result                              | Figure                                                                                                                                                                                    |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Primary desktop screen reader       | JAWS 55.0 percent, NVDA 32.9, VoiceOver 6.5, ZoomText/Fusion 2.1                                                                                                                          |
| Commonly used (multiple answers)    | JAWS 69.2, NVDA 59.3, VoiceOver 42.0, Narrator 36.1 (primary for only 0.4)                                                                                                                |
| Combinations                        | JAWS with Chrome 31.2, NVDA with Chrome 17.3, JAWS with Edge 17.0, NVDA with Firefox 9.1, NVDA with Edge 5.4, JAWS with Firefox 5.0, VoiceOver with Safari 4.3, VoiceOver with Chrome 1.6 |
| Desktop operating system            | Windows 90.7, Mac 6.3, Linux 1.6                                                                                                                                                          |
| Mobile platform                     | iOS 73.3, Android 24.0                                                                                                                                                                    |
| Mobile screen readers commonly used | VoiceOver 72.2, TalkBack 29.5                                                                                                                                                             |
| Primary mobile browser              | Safari 56.0, Chrome 28.2                                                                                                                                                                  |
| First action on a long page         | Navigate headings 67.8, Use Find 12.5, Read the page 9.7, Navigate links 6.7, Navigate landmarks 3.4                                                                                      |

Practical pairing from the data: JAWS or NVDA on Windows with Chrome, Edge or Firefox; VoiceOver with Safari on macOS
and iOS; TalkBack on Android. The survey does not cross-tabulate TalkBack with a browser, so a TalkBack and Chrome
pairing is my inference. Regional differences are large: NVDA leads JAWS in Africa, Asia and South America, JAWS leads
in North America, and Europe is about even.

- WCAG itself does not name a required assistive technology. It uses the "accessibility supported" concept, and a
  conformance claim may list the user agents used for testing.

## 3. ARIA

### 3.1 Sources and their status

| Source                                                                    | Status read on 2026-11-16                                                                                                                                                                                                                                                                                                                                                                                   |
| ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Using ARIA (`https://www.w3.org/TR/using-aria/`)                          | **W3C Discontinued Draft, 24 February 2026.** "No longer intended to advance or to be maintained." The status text says the four rules "are kept for historical purposes and for easier reference" and points readers to the Authoring Practices Guide. (Via summary; a search snippet quotes the same wording.)                                                                                            |
| ARIA in HTML (`https://www.w3.org/TR/html-aria/`)                         | W3C Recommendation, 11 August 2026 (a living Recommendation with frequent republication). Says authors "MAY use the ARIA `role` and `aria-*` attributes to change the exposed meaning", and defers the rules for using ARIA to WAI-ARIA 1.2. Its source has a section "Adhere to the rules of ARIA" and "avoid doing this" examples such as `<summary role="button">`. (Via summary, plus the source file.) |
| WAI-ARIA 1.2                                                              | W3C Recommendation, 6 June 2023. (History page, via summary.)                                                                                                                                                                                                                                                                                                                                               |
| WAI-ARIA 1.3                                                              | Working Draft, 4 June 2026. (History page, via summary.)                                                                                                                                                                                                                                                                                                                                                    |
| ARIA Authoring Practices Guide (APG) (`https://www.w3.org/WAI/ARIA/apg/`) | Maintained in `w3c/aria-practices`, licensed under the W3C Software and Document License. Head commit read: `f14b2490a6`, 2026-11-13. Its "Read Me First" page says it illustrates "appropriate use of ARIA 1.2".                                                                                                                                                                                           |

### 3.2 The rules of ARIA use, exact text

Source: Using ARIA, section 2 "Notes on ARIA Use in HTML" (Discontinued Draft of 24 February 2026, via summary, so the
quotations are as the summary tool gave them). The older Working Draft of 30 October 2017
(`https://www.w3.org/TR/2017/WD-using-aria-20171030/`) carries the first rule in its longer form, which a search snippet
confirmed.

1. First rule: "If you can use a native HTML element or attribute with the semantics and behavior you require already
   built in, instead of re-purposing an element and adding an ARIA role, state or property to make it accessible, then
   do so." The rule lists when native use may not be possible: the feature is missing from HTML or not supported by
   assistive technology, or visual design rules out the native element.
2. "Do not change native semantics, unless you really have to."
3. "All interactive ARIA controls must be usable with the keyboard."
4. "Do not use role="presentation" or aria-hidden="true" on a focusable element."

Older material, and many secondary sources, describe five rules (the fifth is "All interactive elements must have an
accessible name"). The discontinued draft I read lists four. I did not read a primary source for a fifth rule in the
current text, so treat "five rules" as unverified.

The APG "Read Me First" page (original source at the commit above) holds the closest official wording now: heading "No
ARIA is better than Bad ARIA"; "Principle 1: A role is a promise" (a `div` with `role="button"` promises keyboard
behaviour that the author must code); "Principle 2: ARIA Can Both Cloak and Enhance". It does not state the first rule
as such.

### 3.3 Measured evidence on ARIA and errors

Source: WebAIM Million 2026 (data from February 2026, 1,000,000 home pages, WAVE engine). Original.

- 82.7 percent of home pages used ARIA (excluding landmark roles), up from 79.4 percent in 2025. 133,589,803 ARIA
  attributes were found, 133 per page on average, 27 percent more than a year earlier and over six times the 2019 level.
- Pages with ARIA averaged 59.1 detected errors; pages without ARIA averaged 42. WebAIM says "this does not necessarily
  mean that ARIA introduced these errors (these pages were also more complex)". More ARIA on a page went with more
  detected errors.
- 5.7 percent of home pages had `role="menu"`; 22 percent of those menus introduced barriers because the required ARIA
  markup and interactions were missing.
- Averages per page: 23.3 `aria-hidden="true"`, 4.8 `role="button"`, 30.4 `tabindex` of 0 or -1.
- Home page complexity rose 14.3 percent in a year (1,437 elements per page).
- The report ties the trend to complexity and, as a hypothesis, to "automated or AI-assisted coding practices ('vibe
  coding')".
- 2025 comparison values (79.4 percent ARIA use) come from the 2026 report; I did not fetch the 2025 report.

So the evidence is a correlation, not a causal measurement. Claim only that heavier ARIA use correlates with more
detected errors, and that one ARIA widget (menus) fails often.

## 4. Beyond the web

### 4.1 EN 301 549

- Current version: **EN 301 549 V4.1.1 (2026-09)**, a Harmonised European Standard, "Accessibility requirements for ICT
  products and services", by ETSI, CEN and CENELEC. Adoption date 24 August 2026; ETSI listing shows publication 2
  September 2026. Latest announcement date 30 November 2026; latest national publication 31 May 2027; withdrawal of
  conflicting national standards 31 May 2028. (Original, ETSI PDF
  `https://www.etsi.org/deliver/etsi_en/301500_301599/301549/04.01.01_60/en_301549v040101p.pdf`.)
- Previous version: V3.2.1 (2021-03), based on WCAG 2.1. The ETSI directory also holds drafts 4.1.0 (2025-11 and
  2026-06).
- V4.1.1 aligns clauses 9, 10 and 11 with WCAG 2.2, revises real-time text to include total conversation, adds Annex ZA
  (Directive 2016/2102), Annex ZB (Directive 2019/882) and clause A.2 for evaluating conformance with Directive
  2019/882. It adds user-preference clauses 9.7, 10.7 and 11.7 (visible in the table of contents; clause 9.7 text read).
  4.1.1 Parsing is dropped and the six new A/AA criteria are added (the clause list shows 9.2.4.11, 9.2.5.7 and 9.2.5.8;
  secondary sources give the same six).
- It cites WCAG 2.2 as: "W3C Recommendation (12 December 2024)/ISO/IEC 40500:2025". Copyright notice for the cited WCAG
  text: W3C 2020-2024.
- Self-scoping: each requirement starts "Where ICT <precondition>". Conformance is required only when the precondition
  is true. Annex C (normative) gives sufficient tests but "does not provide a testing methodology".

Clause structure (original table of contents):

| Clause             | Content                                                                                                                                                                                                                                                                                     |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 to 3             | Scope, references, terms                                                                                                                                                                                                                                                                    |
| 4                  | Functional performance criteria (usage without vision, with limited vision, without colour perception, without hearing, with limited hearing, with no or limited vocal capability, with limited manipulation or strength, with limited reach, seizure triggers, limited cognition, privacy) |
| 5                  | Generic requirements: closed functionality, activation of accessibility features, biometrics, preserving accessibility information in conversion, tactile operable parts, key repeat, authoring tools                                                                                       |
| 6                  | ICT supporting real-time two-way communication: voice, real-time text (RTT), caller ID, video, total conversation                                                                                                                                                                           |
| 7                  | ICT with video capabilities: subtitles, audio description, user control                                                                                                                                                                                                                     |
| 8                  | Hardware: speech output, stationary ICT (reach, display location, floor space), operable parts, standard connections, colour and contrast                                                                                                                                                   |
| 9                  | Web                                                                                                                                                                                                                                                                                         |
| 10                 | Non-web documents                                                                                                                                                                                                                                                                           |
| 11                 | Non-web software (including mobile apps); 11.5 interoperability with keyboards and assistive technology; 11.6 documented accessibility features                                                                                                                                             |
| 12                 | Information about products and services (documentation, support)                                                                                                                                                                                                                            |
| 13                 | Relay and emergency service access                                                                                                                                                                                                                                                          |
| 14                 | Conformance                                                                                                                                                                                                                                                                                 |
| Annex A            | Conformance evaluation for Directives 2016/2102 and 2019/882                                                                                                                                                                                                                                |
| Annex B            | Relationship of requirements to functional performance criteria                                                                                                                                                                                                                             |
| Annex C            | Normative determination of conformance (sufficient tests)                                                                                                                                                                                                                                   |
| Annexes D to F     | Cognitive accessibility resources, guidance on use, change history                                                                                                                                                                                                                          |
| Annexes ZA, ZB, ZC | Relationship to Directive 2016/2102, 2019/882 and other directives                                                                                                                                                                                                                          |

How it maps WCAG to non-web content (original, clauses 9.0, 10.0, 11.0 and examples at 10.2 and 11.2):

- Clause 9 requirements read: "Where ICT is, or includes, a web page, the web page shall satisfy WCAG 2.2 Success
  Criterion 1.1.1 Non-text content." Level AA conformance with WCAG 2.2 equals conforming with all of 9.1 to 9.4 plus
  the conformance requirements in 9.6. For WCAG 2.0 and 2.1 the clause lists the exact exceptions that make Level AA
  equivalent.
- Clause 9.5 lists the 31 AAA criteria as informative. Clause 9.6 copies the five WCAG conformance requirements.
- Clauses 10 and 11 repeat the same structure with numbers mirrored (10.2.4.7 for 2.4.7 and so on). "Void" clauses keep
  the numbering aligned. Some criteria are referenced directly; others are reproduced in a table with a note stating the
  changes, for example replacing "web page" with "non-web document" or "non-web software" and removing the
  non-interference cross-reference.
- Void for non-web: 2.4.1 Bypass Blocks and 2.4.5 Multiple Ways (they apply to "sets" of documents or programs, which
  are rare). The 10.2.4.2 and 11.2.4.2 text adapts 2.4.2 Page Titled: documents need a title attribute only when the
  format supports one; software gives each window or screen a title.
- Preconditions narrow scope: for example clause 11 criteria apply to non-web software "that provides a user interface"
  and to functionality that is "not closed to programmatic access". Closed functionality (kiosks, for example) is
  handled in clause 5.1.
- Web views inside native apps: clause 9.0 note 3 and clause 11.0 note 3 say a web view embedded in an app "does not
  meet the definition of a web page", the clause 11 requirements apply to it, "there are no circumstances in which
  clause 9 requirements and the corresponding clause 11 requirements are both applicable", and clause 11 takes
  precedence.
- Clause 10 applies to documents that are not web pages, not embedded in web pages, or provided with pages but neither
  embedded nor rendered with them (downloadable files). Note 11 names ISO 14289-1:2014 and ISO 14289-2:2024 as the
  technical standards for accessible PDFs.
- Clause 10 note 5 and clause 11 say the criteria "are intended to harmonize with" the WCAG2ICT Note.

Legal status of V4.1.1 (see section 5): published, not yet cited in the Official Journal under either Directive as of
the sources I read. The EU Accessible EU Centre page of 7 September 2026 says V3.2.1 remains the reference until the
Commission cites V4.1.1.

### 4.2 WCAG2ICT

- "Guidance on Applying WCAG 2 to Non-Web Information and Communications Technologies (WCAG2ICT)": W3C Group Note dated
  11 December 2025 (`https://www.w3.org/TR/wcag2ict-22/`). Earlier versions: 21 August 2025, 15 November 2024, and
  WCAG2ICT 2.0. Editors Mary Jo Mueller, Phil Day, Daniel Montalvo. It covers WCAG 2.0, 2.1 and 2.2, is informative and
  sets no requirements. Endorsed by the Working Group, not by W3C or its Members. (Via summary; I read about the first
  100,000 characters of 330,000.)
- Method: replace "web page" with "document" or "software". A single document is the equivalent of a single page; for
  software a single "web page" is a single software program. "Set of web pages" becomes "set of documents" or "set of
  software programs", and sets of software are "extremely rare" ("if there is any ambiguity whether the group is a set,
  then the group is not a set").
- It notes that Section 508 and EN 301 549 exclude 2.4.1, 2.4.5, 3.2.3 and 3.2.4 for non-web documents and software, and
  that EN 301 549 also excludes 2.4.2 and 3.1.2 for non-web software. The Note leaves applicability to the implementer.
  (The V4.1.1 text I read confirms the 2.4.1 and 2.4.5 voids but I did not check the others.)
- Other adaptations: 1.3.4 Orientation does not apply to software never shown on re-orientable hardware (fixed wall
  directories, copier screens); 1.4.4 Resize Text for software may rely on platform text scaling; 1.4.10 Reflow applies
  directly; 4.1.1 is obsolete in 2.2.
- It adds terms "accessibility services of platform software" and "closed functionality", and an appendix of criteria
  that are problematic for closed functionality.

### 4.3 Mobile

- W3C WAI says there are no separate mobile guidelines. WCAG applies to "web pages and web applications, including
  content used on mobile devices", and the 2.1 and 2.2 additions include mobile-related criteria. (Via summary of
  `https://www.w3.org/WAI/standards-guidelines/mobile/`, updated 6 May 2025.)
- "Guidance on Applying WCAG 2.2 to Mobile Applications (WCAG2Mobile)" (`https://www.w3.org/TR/wcag2mobile-22/`): W3C
  Group Draft Note dated 6 May 2025. Informative. Scope: native apps, mobile web apps, and hybrid apps with web
  components. It is still a draft. (Via summary; first 100,000 of 214,000 characters.)
- WCAG2ICT is also a route for native apps, and EN 301 549 clause 11 applies to mobile apps (clause 11.0 lists "mobile
  applications"). WCAG2ICT is described by W3C as "a more general resource that also includes mobile apps".
- Platform guidance, named as pointers only:
  - Android: "Build accessible apps" (`https://developer.android.com/guide/topics/ui/accessibility`) with principles,
    testing, composables and Accessibility Scanner pages. Read; it does not name WCAG.
  - Apple: Accessibility on Apple Developer (`https://developer.apple.com/accessibility/`; only the page title could be
    read) and the Human Interface Guidelines accessibility page
    (`https://developer.apple.com/design/human-interface-guidelines/accessibility`; the page could not be read, so this
    URL is unverified).
  - The third-party Swift skill in section 7 names the App Store Accessibility Nutrition Labels. I have not checked that
    claim against Apple documentation.

## 5. Legal anchors (pointers only)

| Instrument                                                                                                      | WCAG version and level                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Source and date                                                                                                                                        |
| --------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Directive (EU) 2019/882, European Accessibility Act (EAA)                                                       | Not named. Technical route is a harmonised standard (EN 301 549) once cited in the Official Journal; Article 15(1) gives a presumption of conformity only then, and Article 15(3) lets the Commission adopt technical specifications if no standard is cited. Applies to products placed on the market and services provided after 28 June 2025 (Article 2, Article 31(2)). Transitional periods: services may keep using products lawfully used before 28 June 2025 until 28 June 2030; self-service terminals up to 20 years (Article 32). | EUR-Lex text (original), read 2026-11-16. The standardisation request is C(2022) 6456 of 14 September 2022 (EC document; also named in ETSI foreword). |
| Directive (EU) 2016/2102, Web Accessibility Directive (WAD)                                                     | WCAG not named in the Directive. Article 6 presumes conformity for content meeting harmonised standards cited in the Official Journal. Applies to public sector websites from 23 September 2019 (new) or 2020 (existing) and mobile apps from 23 June 2021.                                                                                                                                                                                                                                                                                  | EUR-Lex text (original).                                                                                                                               |
| Commission Implementing Decision (EU) 2021/1339 of 11 August 2021 (OJ L 289, 12 August 2021)                    | Cites EN 301 549 V3.2.1 (2021-03) as the harmonised standard for websites and mobile applications under the WAD, replacing V2.1.2. It concerns Directive 2016/2102 only. V3.2.1 is based on WCAG 2.1 AA (shown by the clause 9.0 list in V4.1.1).                                                                                                                                                                                                                                                                                            | EUR-Lex text (original).                                                                                                                               |
| EN 301 549 V4.1.1 (2026-09)                                                                                     | WCAG 2.2 AA. Not yet cited as of the sources I read. Several 2026 secondary sources say no standard is cited under the EAA; Deque says citation is expected around 30 November 2026, but that date is the "latest announcement" date for national transposition in the ETSI foreword, so the Deque date may be a misreading. Unverified.                                                                                                                                                                                                     | ETSI PDF (original). EU Accessible EU Centre news item, 7 September 2026 (EC site; via summary).                                                       |
| US Section 508 (Rehabilitation Act), 36 CFR part 1194, Appendix A, E205.4 and E207.2                            | WCAG 2.0 Level A and AA for electronic content and for software user interfaces. Non-web documents are excepted from 2.4.1, 2.4.5, 3.2.3 and 3.2.4.                                                                                                                                                                                                                                                                                                                                                                                          | eCFR, queried at date 2026-11-10 (original). I did not check whether an update to a later WCAG version is proposed.                                    |
| ADA Title II web and mobile rule, 28 CFR 35.200                                                                 | WCAG 2.1 Level A and AA (incorporates `REC-WCAG21-20180605`). Final rule 89 FR 31320, 24 April 2024, effective 24 June 2024. Interim final rule 91 FR 20902, 20 April 2026, moved compliance to **26 April 2027** (population 50,000 or more) and **26 April 2028** (under 50,000 and special districts). Comments closed 22 June 2026.                                                                                                                                                                                                      | Federal Register API and eCFR (original). The DOJ page `ada.gov/resources/web-rule-first-steps/` repeats the extension.                                |
| HHS Section 504 rule, 45 CFR 84.84                                                                              | WCAG 2.1 Level A and AA for web content and mobile apps of recipients. Dates in eCFR: 11 May 2027 (15 or more employees) and 10 May 2028 (fewer than 15).                                                                                                                                                                                                                                                                                                                                                                                    | eCFR (original). I did not read the HHS extension notice.                                                                                              |
| UK Public Sector Bodies (Websites and Mobile Applications) (No. 2) Accessibility Regulations 2018 (SI 2018/952) | The text defines the requirement as making a site "perceivable, operable, understandable and robust". I did not find WCAG named in the regulations I read (regulation 3). GOV.UK Service Manual says services must meet WCAG 2.2 AA "as a minimum" (page updated 29 October 2024).                                                                                                                                                                                                                                                           | legislation.gov.uk (original), GOV.UK (original).                                                                                                      |
| Canada, CAN/ASC-EN 301 549:2024                                                                                 | Identical adoption of EN 301 549:2021 (V3.2.1), so WCAG 2.1 AA for web. Adopted May 2024 by Accessibility Standards Canada. A proposal in Canada Gazette Part I (21 December 2024) would incorporate it by ambulatory reference into the Accessible Canada Regulations, with proposed web dates of 1 June 2027 (federal public sector) and 1 June 2028 (large and medium businesses). Whether a final regulation exists: unverified (one vendor page says SOR/2025-255).                                                                     | accessible.canada.ca page and Canada Gazette (original, via summary).                                                                                  |

ISO numbers (item 5):

- WCAG 2.0 is ISO/IEC 40500:2012. Evidence: EN 301 549 V4.1.1 clause 9.0 note 2: "WCAG 2.0 is identical to ISO/IEC
  40500:2012. WCAG 2.2 is identical to ISO/IEC 40500:2025." (Original.) A search snippet of the ISO preview says the
  second edition "cancels and replaces the first edition (ISO/IEC 40500:2012)".
- WCAG 2.2 is ISO/IEC 40500:2025, approved 21 October 2025 under the JTC 1 PAS procedure. The W3C WCAG overview (updated
  17 September 2026, via summary) says "ISO/IEC 40500:2025 is exactly the same as the October 2023 version of WCAG 2.2",
  that the December 2024 version is expected as ISO/IEC 40500:2026 by late 2026, and a search snippet shows ISO/IEC DIS
  40500 in the enquiry stage. So the ISO text and the current Recommendation text differ by the 2024 republication.
- WCAG 2.1: I found no ISO number. Neither the W3C overview nor ETSI names one. Mark as not found.

## 6. Licences

- WCAG 2.2 is under the **W3C Document License** (2023 version, in force since 1 January 2023). Evidence: the source
  build configuration has `license: "document"`, and the repository's `LICENSE.md` says all documents are under the W3C
  Document License. (Original.) The license page itself was read via summary
  (`https://www.w3.org/copyright/document-license/`).
- Permitted: copy and distribute the document in any medium for any purpose, without fee or royalty. Derivative works
  are permitted only "to implement the document's technical specifications in software, supporting materials, or
  software documentation". Conditions: link to the original document, keep the original copyright notice, include the
  document's status, and include the full notice where space permits. Attribution form: "Copyright © 2023 W3C®. This
  software or document includes material copied from or derived from [title and URI]". Not permitted: derivatives
  published as a technical specification; use of names or trademarks in advertising without written permission. Code
  components (Web IDL, W3C markup, marked code examples) fall under the W3C Software License.
- W3C "Permission to Use WAI Material" page (via summary): WAI material is free to use with attribution and no
  modification; the Document License "does not allow modifications or the creation of derivative works" in general. Some
  WAI material is licensed CC BY 4.0 and may be adapted.
- Answer for the skill: quoting success criterion numbers, names and short normative text with attribution, a link, the
  copyright line and the status falls under "copy and distribute". Writing original guidance that explains how to meet
  the criteria is arguably "supporting materials" that implement the specification, but I could not confirm that reading
  and this is not legal advice. Do not republish long stretches of the Recommendation as a substitute for it, and do not
  present a rewritten criterion as the criterion. Open item for the user.
- Other licences found:
  - APG and `w3c/aria-practices`: W3C Software and Document License (the permissive licence, which allows derivatives).
  - `w3c/wcag` repository text: W3C Document License, as above.
  - EN 301 549: ETSI copyright notice (page 2): no reproduction in any form without prior written authorisation of ETSI,
    except extracts "strictly necessary for the technical implementation of the normative deliverable". The skill must
    therefore cite EN 301 549 clause numbers and titles only and must not copy its text. The WCAG 2.2 content referenced
    in clauses 9 to 11 is under W3C copyright (page 11).
  - WCAG-EM and WCAG2ICT: licence not checked.
  - WebAIM reports and GDS audit: not checked. Cite and link; do not copy tables.

## 7. Third-party accessibility skills (design input only)

None of these is used as evidence for any fact above.

| Repository                                                        | Licence    | Read at                         | Structure                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ----------------------------------------------------------------- | ---------- | ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `https://github.com/Community-Access/accessibility-agents`        | MIT        | Commit `a538edc9ed`, 2026-11-07 | One package, read by several agent clients. More than 40 `SKILL.md` files under `skills/` (specialists such as aria-specialist, contrast-master, forms-specialist, document accessibility, regression detector, compliance mapping), plus hooks that block edits to user-facing files until an "accessibility lead" skill has reviewed, an MCP server and a GitHub Action. States a WCAG 2.2 AA target. Heavy: 1,085 files. |
| `https://github.com/KreerC/ACCESSIBILITY.md`                      | MIT        | Commit `2bf8ddcf87`, 2026-05-20 | Two short skills: `accessibility` (about 10 KB, "accessibility-first" rules, code comments with WCAG references) and `accessibility-testing` (pa11y and axe-core in CI; a per-component WCAG 2.2 table with pass, fail, not applicable, untested). The testing skill asks for AAA checks on each component, which differs from an AA default.                                                                               |
| `https://github.com/ginader/born-accessible-ui`                   | Apache-2.0 | Commit `06112e1d2b`, 2026-10-25 | One skill with `references/protocols.md` and `references/remediation.md`, a Plan, Build, Verify, Fix, Report loop, three protocols (plan semantics first, verified contrast, native HTML before ARIA) and Playwright with axe-core scripts that loop until zero automated violations. Author is a named accessibility specialist. Risk: "zero automated violations" is an automated-only exit criterion.                    |
| `https://github.com/zivtech/accessibility-skills`                 | GPL-3.0    | Commit `47e9ea61b9`, 2026-11-09 | About a dozen skills (planner, critic, role audit, test, ACR reporting, bug reporting, content judgment, workflow, verify) for Claude Code and an `.agents` copy, with evals, role definitions and model benchmarks. Targets WCAG 2.2 AA and Revised Section 508. Its README carries an unsourced 30 to 40 percent automated-detection claim. GPL-3.0 licence limits reuse of its text.                                     |
| `https://github.com/PasqualeVittoriosi/swift-accessibility-skill` | MIT        | Commit `3791850af7`, 2026-03-09 | One large skill (about 22 KB) for SwiftUI, UIKit and AppKit, plus references. "First-draft rules" (accessibility in the first draft), native APIs first, App Store Accessibility Nutrition Label categories. Useful as a native-app model; its platform claims are unchecked here.                                                                                                                                          |

Observed design patterns across these: an edit gate or review gate; a verification loop with Playwright and axe-core;
per-role specialist skills; reports from structured findings; strong dependence on automated checks. Patterns that carry
risk for a conformance skill: automated-only exit criteria, an AAA default, GPL text.

Other candidates I saw but did not read: `mrKanoh/wcag-accessibility-audit-skill` (MIT),
`tomaszboloz/WCAG-Accessibility-Skills` (MIT, explicit manual-review boundaries), `smukh/a11y-agent-skills` (MIT),
`weAAAre/a11y-agents-kit` (MIT), `rgmez/apple-accessibility-skills` (MIT), `iam-niranjan/wcag-skills` (MIT, no stars).

## 8. What the skill must teach that a capable agent likely gets wrong

This section is inference from the sources above, not a measured list of model errors. No source here measured agent
behaviour. The WebAIM Million 2026 author suggests AI-assisted coding may contribute to rising error counts, as a
hypothesis only.

01. Which version applies. WCAG 2.2 is the right design target, but law cites older versions: Section 508 cites 2.0; the
    ADA Title II rule and the HHS Section 504 rule cite 2.1; EN 301 549 V3.2.1 (the cited one under the Web
    Accessibility Directive) is 2.1 based; V4.1.1 is 2.2 based and not yet cited. An agent should state the target
    version and level, and say which legal text applies.
02. 4.1.1 Parsing is gone in 2.2. Agents often still "fix" duplicate ids or markup validity under 4.1.1. Policy that
    requires 2.0 or 2.1 may still need it.
03. New criteria in 2.2 and their thresholds: 24 by 24 CSS pixels (not 44, which is the AAA 2.5.5), focus not hidden by
    sticky headers or cookie banners, dragging alternatives, consistent help, redundant entry, no cognitive function
    test at login (do not block paste or password managers). Focus Appearance (2.4.13) is AAA, not AA.
04. Level discipline. AA means all A and AA criteria. AAA is not recommended as a general site policy. Do not present
    AAA checks as required.
05. Conformance is page-level and process-level. A component review cannot support a page conformance claim. All
    responsive variations count. Every page in a checkout flow must conform. A criterion that does not apply (no media,
    no timing) is satisfied.
06. "No automated violations" is not "accessible". Give figures with their method (section 2.2) and require manual
    keyboard, zoom and reflow, screen reader and, where possible, user testing.
07. ARIA discipline. Native element first; no `role="button"` without full keyboard behaviour; no `aria-hidden` or
    `role="presentation"` on focusable elements; an `aria-label` that differs from visible text breaks 2.5.3 Label in
    Name; more ARIA correlates with more errors; the APG patterns assume testing with real assistive technology. The
    rules now live in a discontinued draft and the APG, so cite them accordingly.
08. Contrast and sizing numbers and their exceptions (section 1.3), including non-text contrast, text spacing and
    reflow, and the logo and inactive-control exemptions.
09. Status messages (4.1.3) need roles or properties so they are announced without focus. Name, Role, Value (4.1.2) is
    met by standard controls; custom controls must supply it.
10. Native apps and non-web content: WCAG applies through WCAG2ICT (Note, informative) and EN 301 549 clauses 10 and 11,
    with "web page" reinterpreted. Embedded web views in a native app follow clause 11, not clause 9. 2.4.1 and 2.4.5
    are void for single documents and programs.
11. WCAG 3 is a draft; use 2.2.
12. Understanding and Techniques documents are informative. A sufficient technique is not a requirement and a failure
    example is not an automatic fail.
13. Citation hygiene: say which document, version and date. Cite EN 301 549 by clause number, since it cannot be copied.
    Treat screen reader survey percentages as a non-random sample.

## 9. Open questions and gaps

01. Whether EN 301 549 V4.1.1 has been cited in the Official Journal under Directive 2019/882 or 2016/2102 by the time
    the skill ships. I found no primary OJ source; several secondary sources say not yet. Check the Commission
    harmonised standards page or EUR-Lex.
02. Whether any Access Board proposal to move Section 508 from WCAG 2.0 to a later version exists. Not searched.
03. Other regimes not searched: Australia, Japan, Ontario (AODA), India, Brazil, Israel. Canada's final regulation
    status is unverified. The UK regulations' link to a WCAG version is unverified.
04. ISO: the ISO catalogue page returned 403. The ISO/IEC 40500:2026 or DIS status rests on W3C text and search
    snippets. No ISO number found for WCAG 2.1.
05. The "five rules of ARIA" claim: I could find only four rules in the discontinued draft. Check the W3C `using-aria`
    repository history if the fifth rule matters.
06. Vigo et al. 2013 was read through an abstract summary. The Deque figures come from a vendor page. A newer
    independent measurement of automated coverage on real sites would strengthen section 2.2; I did not find one in the
    time available.
07. Licence question for the skill: whether rewritten guidance counts as "supporting materials" under the W3C Document
    License. WCAG-EM, WCAG2ICT and WebAIM reuse terms were not checked. This needs the user's decision, not more
    research.
08. Third-party skills: I read only repository trees, first sections and READMEs, not whole skills. Their claims were
    not verified.
09. WCAG2Mobile is a draft Note dated 6 May 2025; I did not read past its abstract and first part. Check its current
    status again before citing it.
10. WCAG 2.2 normative text was read from source files at the tag; the published page was read via summary only. A diff
    against the published page was not done beyond the table-of-contents check and the AAA table in EN 301 549.
11. Apple's HIG and accessibility pages could not be rendered. Android guidance was read at the overview level only.
12. The WCAG-EM 1.0 Note was not read.

## 10. Hypotheses and how they resolved

| Hypothesis at the start                               | Result                                                                                                                                              |
| ----------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| EN 301 549 current version is V3.2.1 (2021).          | Refuted. V4.1.1 (2026-09) was published. V3.2.1 remains the version cited under the WAD.                                                            |
| WCAG-EM is the 2014 Note (1.0).                       | Refuted. WCAG-EM 2.0 is a Note of 23 July 2026.                                                                                                     |
| "Using ARIA" is the home of the rules.                | Partly refuted. It is a Discontinued Draft since 24 February 2026; the APG and ARIA in HTML carry the guidance.                                     |
| WCAG 3 is still a Working Draft.                      | Confirmed (10 September 2026).                                                                                                                      |
| WCAG 2.2 has an ISO number.                           | Confirmed: ISO/IEC 40500:2025. WCAG 2.0 is ISO/IEC 40500:2012.                                                                                      |
| ADA Title II compliance is April 2026 and April 2027. | Refuted. Extended to 26 April 2027 and 26 April 2028 by an interim final rule of 20 April 2026.                                                     |
| Automated tools find 30 to 40 percent.                | Not supported as stated. Measured figures range from about 13 to 50 percent depending on method, with a vendor claim of 57 percent by issue volume. |
| ARIA misuse is measured as harmful.                   | Only partly. WebAIM shows a correlation and says it may be complexity, not causation.                                                               |

Tools reached: `docs-mcp`, `crawl4ai`, `WebFetch`, `scrapling` (EUR-Lex), `searxng` (rate-limited late in the session)
and `sequential-thinking`. Route notes are in the agent's memory directory, not here.
