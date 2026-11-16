# Standards Beyond WCAG and the Versions Laws Cite

## EN 301 549

EN 301 549 V4.1.1 (2026-09), "Accessibility requirements for ICT products and services", is the European
harmonised standard from ETSI, CEN, and CENELEC. It is based on WCAG 2.2. Its text may not be copied, so cite it
by clause number and title only.

| Clause | Covers                                                                                                                                    |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| 4      | Functional performance criteria: use without vision, with limited vision, without hearing, with limited manipulation or reach, and others |
| 5      | Generic requirements, including closed functionality, biometrics, and tactile operable parts                                              |
| 6      | Real-time two-way communication: voice, real-time text, video                                                                             |
| 7      | Video: subtitles, audio description, user controls                                                                                        |
| 8      | Hardware: speech output, reach and display location of stationary ICT, operable parts, colour                                             |
| 9      | Web content: WCAG 2.2, criterion by criterion, plus user preferences                                                                      |
| 10     | Non-web documents                                                                                                                         |
| 11     | Non-web software, including mobile apps                                                                                                   |
| 12     | Documentation and support services                                                                                                        |
| 13     | Relay and emergency services                                                                                                              |

Each requirement starts with a condition, "Where ICT …", and applies only when the condition holds. Meeting
clauses 9.1 to 9.4 and 9.6 equals WCAG 2.2 Level AA. Clause 9 also holds 9.7, which WCAG does not contain: a web
page must not block the browser's modes that apply the user's preference settings, or override documented
platform accessibility features, unless that is essential. Clauses 10.7 and 11.7 require the same of documents
and software. So meeting WCAG 2.2 AA does not by itself meet clause 9.

- **Native apps and software:** clause 11 restates the WCAG criteria for software. A web view inside a native
  app falls under clause 11, not clause 9.
- **Documents:** clause 10 covers files that are not web pages, such as downloadable PDFs. ISO 14289 (PDF/UA)
  is the technical standard for accessible PDF.
- **Closed functionality,** such as a kiosk or a ticket machine that users cannot connect their own assistive
  technology to: clause 5.1 requires the device to provide access itself. Its sub-clauses cover non-visual
  access (5.1.3), text enlargement (5.1.4), visual output for sound (5.1.5), operation without a keyboard
  interface (5.1.6), and access without speech (5.1.7). Clause 5.2 covers turning accessibility features on,
  and 5.5 tactilely discernible operable parts.
- **Stationary ICT,** such as a kiosk fixed to the floor or a wall: clause 8.3 sets measured limits above the
  floor of the access space. No part of a display screen is lower than 800 mm (8.3.2), and information needed
  to operate it is no higher than 1 600 mm (8.3.3.1). At least one of each operable part is between 800 and
  1 100 mm (8.3.5.1); where the design cannot allow that, operable parts sit between 380 and 1 220 mm
  (8.3.5.2). Clause 8.3 also sets reach depth, forward and side reach, and the free space underneath, and
  clause 8.4 covers operable parts such as numeric keys.

The W3C Note WCAG2ICT (11 December 2025) explains how to read WCAG for non-web content: "web page" becomes
"document" or "software". It is informative, and EN 301 549 clauses 10 and 11 are meant to agree with it.

WCAG2ICT is not a standard and defines no conformance. It takes a whole document, or a whole software
program, as the unit of evaluation in place of a web page. A conformance requirement for non-web ICT comes from
EN 301 549 or from the regulation that cites it.

For native mobile apps, WCAG applies through WCAG2ICT and EN 301 549 clause 11. W3C's mobile guidance,
"Guidance on Applying WCAG 2.2 to Mobile Applications" (WCAG2Mobile), is an in-progress draft. The platform
APIs are in Android's accessibility guide, <https://developer.android.com/guide/topics/ui/accessibility>, and
Apple's accessibility documentation, <https://developer.apple.com/documentation/accessibility>.

## Versions Laws Cite

Laws often cite an older WCAG version than 2.2. Design to 2.2, which also meets 2.0 and 2.1, and report against
the version the user's law names. These facts were checked on 2026-11-16 and change; recheck a date before
relying on it.

| Instrument                                                                      | Cites                                                                                   |
| ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| EU Web Accessibility Directive (2016/2102), public sector sites and apps        | EN 301 549 V3.2.1, based on WCAG 2.1 AA, through Implementing Decision 2021/1339        |
| European Accessibility Act (2019/882), products and services since 28 June 2025 | No harmonised standard cited yet; V4.1.1 (WCAG 2.2) is written for it but not yet cited |
| US Section 508 (36 CFR 1194)                                                    | WCAG 2.0 A and AA                                                                       |
| US ADA Title II rule (28 CFR 35.200)                                            | WCAG 2.1 A and AA; compliance from 26 April 2027 or 26 April 2028 by entity size        |
| US HHS Section 504 rule (45 CFR 84.84)                                          | WCAG 2.1 A and AA                                                                       |
| UK public sector (GOV.UK Service Manual)                                        | WCAG 2.2 AA as the minimum                                                              |

These are pointers, not legal advice. Tell the user to confirm a legal obligation with the regulation's own text
or a lawyer.
