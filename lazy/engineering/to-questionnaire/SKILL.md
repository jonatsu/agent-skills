---
name: to-questionnaire
description: Turn a decision you cannot answer alone into a Markdown questionnaire for the person who holds the missing knowledge, to fill in async or walk through in a meeting. Use to draft a discovery questionnaire, a question list for a stakeholder or domain expert, or an async information-gathering document. Not for being interviewed on your own design (interview-me) or writing a requirements spec (requirements-specification).
license: MIT
metadata:
  author: Joonas Onatsu
---

# To Questionnaire

Turn something you cannot answer alone into a **questionnaire**: a Markdown document you hand to one person to
fill in asynchronously, or work through together in a meeting. The recipient holds knowledge you lack; the
questionnaire pulls it out of them.

**Grill the send, not the subject.** Interview the user only about the *send*, which they can always answer: who
it goes to, and what they need back. The questions in the document then target the **gap** between what the
recipient knows and what the user needs — not the subject the user cannot speak to.

This is the inverse of `interview-me`. That skill interviews the user about their own plan or design; reach for
this instead when the user genuinely cannot answer, because the knowledge lives with someone else. It is not a requirements
specification (`requirements-specification`): it gathers what one person knows, it does not define a system's
behavior.

## Steps

1. **Who is it going to?** In one exchange, establish the recipient's role, expertise, and relationship to the
   user. This fixes the questionnaire's tone and how much context it must carry. Done when you know who the
   recipient is and what they know that the user does not.
2. **What do you need back?** In one exchange, establish the specific decisions or facts the user cannot resolve
   alone and needs from this person. Done when you have a concrete list of what the user must walk away able to
   do or decide.
3. **Write the questionnaire.** Draft questions aimed at the gap from steps 1–2, following the structure below.
   Write each question so the recipient can answer it without the user's context: no internal identifiers or
   team shorthand, and every term the recipient may not know explained once, at first use. Apply
   `writing-for-humans` and its reader-ready check to the finished document. Write it where the user says, or
   to `to-questionnaire-<slug>.md` in the current directory, slug from the topic, and report the path. Done when
   the file exists, every item from step 2 is covered by a question, and the reader-ready check passes.

## Document structure

Frame it as a **discovery questionnaire**: the user lacks context, the recipient holds it. Order questions
most-important-first — async means you may get only one pass — and group them under `##` headings by theme once
there are more than a handful. Use this template:

```markdown
# <Questionnaire title>

**Purpose:** why this questionnaire exists and the decision riding on it.

**From:** <the user>, **To:** <the recipient>, **How your answers will be used:** <where they go>

## Context

One paragraph orienting a recipient who was not in the user's head. Enough to answer well, not a page.

## How to answer

Deadline and rough effort. Partial answers and "I don't know" are useful — flag anything you are unsure of
rather than skipping it.

## <Theme heading>

One `##` section per theme, its questions most-important-first. Every question is one idea, never compound, with
an answer stub directly beneath it, and a one-line _why this matters_ only where the question could be misread or
invite a throwaway answer.

### What load is the system expected to handle at launch?

_Why this matters: it decides whether we provision for burst traffic now or defer it._

>

## Anything else?

A closing catch-all: anything we did not ask that we should know?
```
