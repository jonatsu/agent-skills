# Testing

## What Automated Tools Find

Automated tools find a minority to a modest majority of failures, depending on how they are counted, and a
clean run proves nothing. Measured figures:

- The UK Government Digital Service built a page with 142 deliberate failures and ran 13 tools. The best found
  40 percent, and 50 percent when counting items it flagged for manual review; the worst found 13 percent
  (audit page, last updated 13 April 2018).
- Vigo, Brown, and Conway tested six tools against WCAG 2.0 at W4A 2013: they covered at most half of the
  criteria and found 14 to 38 percent of the failures.
- Deque, the maker of axe, reports that axe-core found 57 percent of issues by volume in its customers' first
  audits (2021). It is a vendor figure, and counting by volume favours frequent, easy-to-detect issues.

Give any figure with its source and method. Tools cannot judge whether alternative text is meaningful, whether
the reading order makes sense, whether colour alone carries meaning, or whether a custom control works with a
screen reader.

## Manual Checks

- **Keyboard:** reach and operate every control with Tab, Shift+Tab, Enter, Space, the arrow keys, and Escape.
  Focus stays visible, follows a logical order, is never trapped, and is never hidden under sticky content.
- **Screen reader:** every control announces its name, role, and state; status messages are announced; images
  have a fitting text alternative; headings and landmarks give the structure.
- **Zoom and reflow:** 200 percent text resize, 320 CSS pixels wide, and the 1.4.12 text spacing values.
- **Colour:** contrast measured, and no information given by colour alone.
- **Motion and time:** animations can be paused, and time limits can be extended or turned off.

## Screen Readers and Browsers

WCAG names no required assistive technology. The WebAIM Screen Reader User Survey 11 (July to August 2026, 1,780
responses, not a random sample) shows the common pairings: JAWS or NVDA with Chrome, Edge, or Firefox on
Windows; VoiceOver with Safari on macOS and iOS; and TalkBack on Android. Test with at least one desktop and one
mobile pairing the users have, and record which ones in the report.

## Testing With Disabled Users

Involve a small group of disabled people, informally and throughout development (W3C, "Involving Users in
Evaluating Web Accessibility"). They find problems that a conformance check misses. Their results cannot decide
conformance on their own, and one person's experience does not stand for everyone with the same disability.
Report the scope, the methods, and the participants' characteristics.
