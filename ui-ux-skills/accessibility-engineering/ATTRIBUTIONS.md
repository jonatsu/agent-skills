# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## First-party Sources

### W3C: Web Content Accessibility Guidelines (WCAG) 2.2

- Source: <https://www.w3.org/TR/WCAG22/>, source files in <https://github.com/w3c/wcag>
- License: `LicenseRef-W3C-Document-License`
- Version: W3C Recommendation of 12 December 2024, tag `WCAG22-20241212`

The skill's target, its criteria, levels, thresholds, conformance requirements, and claim contents come from
the Recommendation. Success criterion numbers and names are quoted as the Recommendation states them. The W3C
Document License permits that copying with this attribution. Every explanation was written independently.
Copyright © 2020-2024 World Wide Web Consortium.

### W3C: WCAG Evaluation Methodology (WCAG-EM) 2.0

- Source: <https://www.w3.org/TR/2026/NOTE-wcag-em-2-20260723/>
- License: `LicenseRef-W3C-Document-License`
- Version: W3C Group Note of 23 July 2026

The Note supplied the five evaluation steps and the sampling approach of the full evaluation. No prose was
copied.

### W3C: Guidance on Applying WCAG 2 to Non-Web ICT (WCAG2ICT), and Mobile Accessibility

- Source: <https://www.w3.org/TR/wcag2ict-22/> and <https://www.w3.org/WAI/standards-guidelines/mobile/>
- License: `LicenseRef-W3C-Document-License`
- Version: WCAG2ICT Group Note of 11 December 2025; mobile page updated 6 May 2025

These supplied how WCAG applies to documents, software, and native apps, and the unit of evaluation for
each. No prose was copied.

### W3C: ARIA Authoring Practices Guide and Using ARIA

- Source: <https://www.w3.org/WAI/ARIA/apg/>, <https://github.com/w3c/aria-practices>, and
  <https://www.w3.org/TR/using-aria/>
- License: `W3C-20150513`
- Version: `aria-practices` commit `f14b2490a6`; Using ARIA Discontinued Draft of 24 February 2026

The guide and the rules of ARIA use supplied the native-first rule, the ban on hiding focusable elements, the
disclosure pattern for site navigation, and moving focus into a dialog and back to its trigger. No prose was
copied.

### W3C: Making Content Usable for People with Cognitive and Learning Disabilities

- Source: <https://www.w3.org/TR/coga-usable/>, <https://github.com/w3c/coga>
- License: `LicenseRef-W3C-Document-License`
- Version: Working Group Note of 29 April 2021; `coga` commit `f15bbd18d1`

The note supplied the eight objectives for cognitive and learning disabilities and its status as informative
guidance beyond WCAG. No prose was copied.

### W3C: Involving Users in Evaluating Web Accessibility

- Source: <https://www.w3.org/WAI/test-evaluate/involving-users/>
- License: `LicenseRef-W3C-Document-License`
- Version: updated 30 April 2024

The page supplied how to involve disabled users and the limits of what their results show. No prose was copied.

### ETSI, CEN, and CENELEC: EN 301 549, Accessibility Requirements for ICT Products and Services

- Source: <https://www.etsi.org/deliver/etsi_en/301500_301599/301549/04.01.01_60/en_301549v040101p.pdf>
- License: `LicenseRef-Proprietary`
- Version: V4.1.1 (2026-09)

The standard supplied the clause structure, the conditional form of its requirements, the user-preference
clauses, and the sub-clauses for closed functionality. It also supplied the measured limits for stationary ICT
and its rules for non-web documents, software, and hardware. ETSI forbids reproduction, so the skill cites clause
numbers, titles, and measurements and copies no text.

## Third-party Sources

### Government Digital Service: GOV.UK Design System error summary

- Source: <https://design-system.service.gov.uk/components/error-summary/>
- License: `MIT AND OGL-UK-3.0`
- Version: read 2026-11-27

The code is under MIT and the guidance text under the Open Government Licence. The component supplied moving focus to
the error summary after a failed submission. No text or code was copied.

### FerroxLabs: wayland `cognitive-accessibility` skill

- Source: <https://github.com/FerroxLabs/wayland>,
  `src/process/resources/skills-library/bodies/skills/web-development/cognitive-accessibility/SKILL.md`
- License: `AGPL-3.0-or-later`
- Version: `4c030c7b01c241df7b6e3535635a970f10d781af`

The repository's `package.json` declares the licence, and the file's own frontmatter claims Apache-2.0. Comparing the
skill with this one exposed the design steps that omitted 1.3.5, 3.3.4, and the consistency criteria, the missing
guidance on where focus moves, and the need for COGA and 2.2.1. Every fact was taken from the W3C and GOV.UK sources
above, and no text or code was copied.

### WebAIM: Screen Reader User Survey 11

- Source: <https://webaim.org/projects/screenreadersurvey11/>
- License: `LicenseRef-Proprietary`
- Version: survey of July to August 2026

The survey supplied the common screen reader and browser pairings that the testing guidance names. No text or
tables were copied.

### Miqdad Badjuber: antislop `antislop-human` skill

- Source: <https://github.com/miqdadbadjuber/anti-slop>, `skills/antislop-human/`
- License: `MIT`
- Version: `44b3547ed6d6f21eed777271602da113efc53c94`

The skill supplied four ideas: an agent should compute a contrast ratio rather than judge it by eye, text over
an image fails at its lowest-contrast point, the reduced-motion setting deserves honouring, and every shipped
theme needs checking. `scripts/contrast.py` and the rule around it were written
independently; no code or text was copied.
