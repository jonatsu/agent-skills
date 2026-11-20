# Source Review: antislop

Date: 2026-11-20. Source: <https://github.com/miqdadbadjuber/anti-slop>, commit
`44b3547ed6d6f21eed777271602da113efc53c94`, MIT. The question was what our writing skills and the UI skills
could take from it. The review covered `antislop-copywriting` and `antislop-human` in full, and the core
`antislop` skill by outline.

## What the Source Is

Seven skills for AI coding agents building web interfaces. The core `antislop` skill bans generic visual and
copy patterns in web UI (gradients, glassmorphism, emoji icons, fake testimonials) through numbered rules and a
delivery gate. `antislop-copywriting` names 30 prose patterns, each with the pattern, why it reads as
machine-written, a before and after, and the rule it breaks. `antislop-human` covers contrast, keyboard, focus,
UI states, zoom, and interaction affordances for web UI, with a contrast-checker script. `antislop-code`,
`antislop-ui`, and `antislop-layoutmobile` were not reviewed.

## Prose Patterns Against `writing-for-humans`

`writing-for-humans` already covers most of the 30 patterns, often with more nuance: chat residue,
meta-commentary, empty promotion, false agency, unnamed authority, negative parallelism, aphorisms, run-ups,
staged candour, gap-filling guesses, forced triads, synonym rotation, bold lead-ins, em dashes, filler, and
stacked hedges. It also has what the source lacks: process residue, self-cancelling claims, editing distortions,
and the preserve-every-claim guardrail.

Patterns the source names that our skills do not:

- **Theatrical takeaways:** a line that labels a conclusion instead of stating it, such as "The takeaway is
  simple:", "That distinction matters.", "The message is clear:", or "Read that again."
- **Temporal runway openers:** "In today's fast-paced world", "In an era of".
- **Staccato runs:** several short fragments in a row staged as a punchline.
- **False ranges:** "from first click to final invoice", where the ends share no scale.
- **Scare quotes:** quotation marks used for emphasis or distance on ordinary words.
- **All-caps emphasis** inside human-facing prose.

Techniques worth taking:

- **The mind-verb test for false agency:** a verb that needs a mind (understands, knows, decides, wants) hides
  an actor, while an ordinary product verb ("the report shows") does not.
- **Use and mention:** a phrase quoted, discussed, or given as an example is not a tell.
- **An adversarial final question:** ask what in the text a reader would take as machine-written, then revise.
- **A short list of signs to preserve in review:** specific, hard-to-fabricate detail, mixed or unresolved
  views, and genuine asides.

Not worth taking: a flat em-dash ban (ours keeps a dash that carries a stated distinction), sentence-case list
items (repository conventions govern), and a read-aloud check an agent cannot perform.

## Front Doors and Documents

- **`writing-readmes`:** the source's empty-social-proof pattern ("trusted by thousands", "industry-leading")
  has no counterpart. A popularity, speed, or adoption claim needs a sourced figure or goes.
- **`writing-documentation` and the diagram skills:** the source's human rules carry over to documents. Images
  and diagrams need text alternatives, link text names its destination, and colour never carries meaning alone
  in a diagram's styling.

## Human Rules, Generalized

`antislop-human` is written for web UI, but each rule rests on a principle that holds in any medium:

| Principle                                     | Web rule in the source                                 | Where else it applies                                                |
| --------------------------------------------- | ------------------------------------------------------ | -------------------------------------------------------------------- |
| Measure a threshold; never judge it by eye    | Grey-on-grey contrast claimed to pass without a ratio  | Diagram colours, terminal colours, target sizes, timing limits       |
| Check the worst case, not the best spot       | Text over an image, tested at one bright point         | The darkest terminal theme, the narrowest pane, the longest value    |
| Give every signal a carrier besides colour    | Red border as the only error cue                       | CLI status, diagram node colours, log levels, dashboards             |
| Make every state perceivable                  | Missing empty, loading, and error states               | CLI output that is empty versus failed, a long job's progress, docs  |
| Show what can be acted on, and name it        | Icon-only buttons, divs as controls, no pointer cursor | Undiscoverable flags, unnamed links, a diagram edge with no label    |
| Respect the reader's settings                 | `prefers-reduced-motion`, 200 percent zoom             | `NO_COLOR`, terminal width, dark-mode rendering of docs and diagrams |
| Let nothing cover what the user is working on | The on-screen keyboard over the focused field          | A progress line overwriting output, a sticky header over an anchor   |
| Make every shipped theme work                 | Focus and contrast checked in one theme only           | Diagrams that vanish in dark mode, light and dark terminal themes    |

Gaps by skill:

- **`accessibility-engineering`:** contrast thresholds are stated, but nothing says to compute the ratio. The
  source ships a checker for exactly that failure. Checking text over an image at its worst spot, and
  `prefers-reduced-motion` as the mechanism for motion control, are also missing.
- **`usability-engineering`:** empty, loading, and error states; the visible signifiers of a control; and an
  on-screen keyboard that covers the focused field.
- **`cli-ui-ux`:** dim text and bright black can vanish on some themes, and a progress line can overwrite
  output. Empty output and failure must be distinguishable.
- **`mermaid-diagrams` and `drawio-diagrams`:** styled colours carry meaning with no label or shape, and nothing
  checks a diagram in dark mode.
- **`writing-documentation` and `writing-readmes`:** text alternatives for images and diagrams, link text that
  names its destination, and a stated outcome for what the reader sees when a step fails.

## Defects in the Source

- `antislop-human` sets WCAG large text at "18px+". WCAG defines it as 18 point (24 CSS pixels), or 14 point
  bold (about 18.7 CSS pixels). Nothing here should copy that threshold.
- The source's rules cite each other by number (R-02, R-36), so a pattern taken alone needs its reasoning
  restated, not its rule number.
