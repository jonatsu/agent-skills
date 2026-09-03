# Copy-Editing Diagnostics

Use this reference for a long draft, a difficult diagnosis, or the final AI-mark cleanup scan. It is a
diagnostic aid, not a blocklist.

Remove definitive production residue when found. Treat ordinary stylistic features as weak signals that need
supporting evidence from the surrounding passage.

## Chat Residue

Remove language that belongs to an assistant-user exchange rather than the document's reader:

- "I hope this helps."
- "Let me know if you would like me to expand."
- "Certainly!" or "Great question!"
- "Would you like me to…" at the end of a section
- "Here is an overview of…" when the document itself is the overview

## Meta-Commentary

Consider removing a sentence that announces the document instead of advancing it:

- "In this section, we will…"
- "The rest of this document explains…"
- "Let me walk you through…"
- "As we will see…"

Keep navigation that helps the reader act, such as a pointer to a file, condition, or next step.

## Empty Promotion

Ask what a sentence actually claims when it relies on importance words such as "crucial", "transformative",
"robust", "seamless", or "groundbreaking". Replace the word only when the specific behavior, consequence, or
constraint can be stated without changing the claim.

## False Agency

Flag a sentence when it gives an inanimate abstraction a human action and hides an actor the source can
establish:

| Pattern                       | Safer action                                           |
| ----------------------------- | ------------------------------------------------------ |
| "the complaint becomes a fix" | Name who filed it and who fixed it, if known.          |
| "the decision emerges"        | Name who decided, if known.                            |
| "the data tells us"           | Name who interpreted the data and what they concluded. |

Do not invent the missing actor. Ask the author or state the gap.

## Clustered Rhetorical Setup

One contrast or rhetorical question may be deliberate. Inspect a passage when several sentences stage a reveal,
announce insight, or end in a manufactured payoff instead of making the claim directly.

## Invisible Marks and Metadata

Inspect formats that can carry invisible text or metadata when cleaning AI-produced output. Remove a character
or field only when its purpose as an AI-origin marker is established. Preserve legitimate Unicode needed for
language, accessibility, bidirectional text, typography, or emoji composition. Preserve authorship,
interoperability, and application metadata unless the user included it in scope or it is a confirmed AI mark.

When removing a confirmed invisible mark, verify that the rendered text and intended semantics did not change.
