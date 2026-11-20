# WCAG 2.2 Facts Agents Misquote

WCAG 2.2 is a W3C Recommendation of 12 December 2024, at <https://www.w3.org/TR/WCAG22/>. It has 86 success
criteria: 31 at Level A, 24 at AA, and 31 at AAA. Its four principles and 13 guidelines are unchanged from
WCAG 2.1, and content that conforms to 2.2 also conforms to 2.0 and 2.1. WCAG 2.2 is also ISO/IEC 40500:2025,
and WCAG 2.0 is ISO/IEC 40500:2012.

## What Changed in 2.2

Nine criteria are new:

| Criterion                                  | Level |
| ------------------------------------------ | ----- |
| 2.4.11 Focus Not Obscured (Minimum)        | AA    |
| 2.4.12 Focus Not Obscured (Enhanced)       | AAA   |
| 2.4.13 Focus Appearance                    | AAA   |
| 2.5.7 Dragging Movements                   | AA    |
| 2.5.8 Target Size (Minimum)                | AA    |
| 3.2.6 Consistent Help                      | A     |
| 3.3.7 Redundant Entry                      | A     |
| 3.3.8 Accessible Authentication (Minimum)  | AA    |
| 3.3.9 Accessible Authentication (Enhanced) | AAA   |

4.1.1 Parsing was removed, because assistive technology no longer parses HTML directly. Do not report
duplicate IDs or invalid markup under 4.1.1 for a WCAG 2.2 target. A policy that requires WCAG 2.0 or 2.1 may
still require it, so check which version applies.

The new criteria were added at the end of each guideline, so the order of criteria within a guideline says
nothing about their level. Read the level marker.

## Thresholds

- **1.4.3 Contrast (Minimum), AA:** text at least 4.5:1, and large-scale text at least 3:1. Incidental text,
  such as inactive controls or decoration, and logotypes have no requirement. Large-scale text is at least 18
  point (24 CSS pixels), or 14 point (about 18.7 CSS pixels) when bold.

  The ratio is (L1 + 0.05) / (L2 + 0.05), where L1 is the relative luminance of the lighter colour and L2 of the
  darker. For relative luminance, divide each sRGB channel by 255. Linearize it: c / 12.92 when c is at most
  0.04045, otherwise ((c + 0.055) / 1.055) to the power 2.4. Then L = 0.2126 R + 0.7152 G + 0.0722 B. Compare the
  unrounded ratio with the threshold: 4.499:1 fails 4.5:1.

- **1.4.4 Resize Text, AA:** text resizes to 200 percent without assistive technology and without loss of
  content or function. Blocking zoom with `user-scalable=no` or a low `maximum-scale` is the usual failure.
  The W3C test rule "Meta viewport allows for zoom" checks for it. Confirm that the setting stops a 200 percent
  resize.

- **1.4.10 Reflow, AA:** no scrolling in two directions at 320 CSS pixels wide, or 256 high for content that
  scrolls sideways. That width equals a 1280-pixel window at 400 percent zoom. Content that needs a
  two-dimensional layout, such as maps, data tables, and video, is exempt.

- **1.4.11 Non-text Contrast, AA:** controls, their states, and meaningful graphics at least 3:1 against what
  is next to them.

- **1.4.12 Text Spacing, AA:** nothing is lost when users apply four settings, each a multiple of the font
  size. The values are line height 1.5, paragraph spacing 2, letter spacing 0.12, and word spacing 0.16.

- **2.2.2 Pause, Stop, Hide, A:** moving, blinking, or scrolling content that starts automatically, lasts more
  than five seconds, and is shown alongside other content needs a way to pause, stop, or hide it.

- **2.3.3 Animation from Interactions** is AAA, not AA. Honouring the platform's reduced-motion setting, such
  as CSS `prefers-reduced-motion` (technique C39), is a sufficient way to meet it.

- **2.4.11 Focus Not Obscured (Minimum), AA:** a focused control is not entirely hidden by author content,
  such as a sticky header or a cookie banner.

- **2.4.13 Focus Appearance** is AAA, not AA.

- **2.5.8 Target Size (Minimum), AA:** pointer targets at least 24 by 24 CSS pixels, with exceptions for
  spacing, an equivalent control, inline links, browser controls, and essential sizes. The 44-pixel figure is
  the AAA criterion 2.5.5.

- **2.5.7 Dragging Movements, AA:** anything done by dragging can also be done with single clicks or taps.

- **3.3.7 Redundant Entry, A:** information the user already entered in the same process is filled in again
  or offered for selection. The exceptions are re-entry that is essential or needed for security, and
  information that is no longer valid.

- **3.3.8 Accessible Authentication (Minimum), AA:** no step of logging in needs a cognitive function test,
  such as recalling a password or solving a puzzle. A step is exempt when it offers one of four exceptions:

  - an alternative method without such a test;
  - a mechanism that helps complete it;
  - a test that asks the user to recognise objects;
  - a test that asks the user to identify content they provided themselves.

  A password field that blocks paste or password managers removes the usual mechanism, so it fails unless an
  alternative exists.

- **4.1.2 Name, Role, Value, A:** standard HTML controls meet it when used as specified; custom controls must
  supply name, role, state, and value themselves.

- **4.1.3 Status Messages, AA:** a status message is announced by assistive technology without taking focus,
  through a role or property such as `role="status"` or `role="alert"`.

## What Is Normative

Only the Recommendation's text is normative. Understanding WCAG 2.2 and Techniques for WCAG 2.2 are
informative, so content may pass a criterion without any documented technique.

WCAG 3 is a Working Draft, last dated 10 September 2026. It does not replace WCAG 2 and cannot be used for
conformance, so target WCAG 2.2.
