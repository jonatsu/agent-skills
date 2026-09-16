---
name: writing-readmes
description: "Write, rewrite, or judge the quality of a project's front door: a README, quickstart, getting-started page, or docs landing page, so a stranger sees the point and can start. Use when a README reads flat or template-filled, when a project needs one from scratch, or when asked whether one is any good. Not for tutorials, how-to guides, references, or runbooks, which are writing-documentation. Not for checking a README's claims against the repository or scaffolding baseline files, which are repo-management."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Writing READMEs

Use this skill for a project's front door: the README, the quickstart or getting-started page, the
documentation landing page. A front door is the first thing a stranger reads about the project, and it is
judged in about ten seconds by someone who has not decided to care yet.

That deadline is what separates this skill from its neighbours. Every other document is read by someone who
already chose the project.

- `writing-documentation` owns tutorials, how-to guides, references, explanations, runbooks and decision
  records — and reviews documents for structure and accuracy.
- `repo-management` owns repository scaffolding, the README templates and audience matrix, and the accuracy
  audit that checks a README's claims against the tree. Route "are these commands still real?" there.
- `writing-for-humans` owns the sentence and the paragraph. Apply it to whatever this skill produces.

A review request splits by what is being judged: **does it read well** is this skill, **is it still true** is
`repo-management`'s audit. A thorough review wants both.

## Iron Law

**Every section answers a reader question, or it goes.**

A front door is not a form to complete. Sections do not earn their place by being conventional, by appearing
in a template, or by existing in the last project's README. A section earns its place by answering something
the reader is actually asking at the moment they reach it — and nothing else does.

This is the rule that a section checklist cannot give you, and its absence is why generic READMEs happen:
given a list of sections, an agent fills all of them, and the result is uniformly flat because nothing in it
was chosen.

## The Five Questions

A stranger works through these in order. They abandon the page at the first one that goes unanswered.

1. **What is this?** One sentence, concrete, no metaphor. They should be able to repeat it to a colleague.
2. **Is it for me?** Who it serves, what problem it solves, and — the part most READMEs skip — what it does
   not do and who should use something else.
3. **Does it actually work?** Evidence before claims. Output, a screenshot, a real example with a real result.
4. **How do I start?** The shortest path from nothing to a working result.
5. **Where do I go next?** Pointers onward. Where readers will get stuck, order them by how fast they resolve:
   in-tool help, then a diagnostic command, then the FAQ, then issue search, then a human. "See the docs" is
   the weakest version of this.

Order sections by these questions rather than by convention. Any candidate section maps to one of the five or
gets cut — that is the Iron Law applied.

Two consequences worth stating, because they are commonly got wrong:

- **Question 3 comes before question 4.** A reader who is not yet convinced will not run your install command.
  Show the thing working, then tell them how to get it.
- **Question 2 requires a limit.** A front door that claims no boundary reads as marketing, and a reader who
  discovers the boundary after installing is angrier than one who was told. Naming the alternatives and who
  each suits costs nothing and buys more credibility than any claim you can make about yourself.
- **Where the project resembles something the reader already has, say the reader's objection out loud.** State
  it verbatim — *"But doesn't X already do this?"* — then answer it with a concrete scenario. Hoping the
  reader infers the difference leaves the whole document's case unmade.

A released project has a sixth reader the five questions miss: the **returning user**, asking *what changed
for me*. They look in the README, not the changelog. Where a version boundary breaks something, keep the
migration note here.

## Answer Question 1 in the First Five Lines

The opening is the whole document's fate. Write it last, once you know what the project actually is, and hold
it to:

- **A title, then one sentence.** Not a paragraph. The sentence names what the thing is and what it is for,
  in the reader's vocabulary rather than the implementation's.
- **No preamble.** Do not open with the problem domain's history, with "In today's world", or with a
  restatement of the project name as a definition.
- **No unexplained jargon.** A term the reader must already know to parse the first sentence has cost you
  the reader.

Test it by deleting everything after the first five lines and asking whether a stranger could say what the
project is and whether it is for them. If not, the opening is not carrying its weight, no matter what follows.

## Show It Working Before Asking for Anything

Concrete evidence answers question 3 and no amount of description substitutes.

- A short, real, copy-pasteable example with its actual output.
- A screenshot, terminal recording or diagram where the result is visual.
- Real values, not `foo` and `bar`. Invented placeholder data reads as a project nobody has run.

Keep it minimal. Strip setup that does not affect the result. One example that runs beats three that
illustrate.

**Never ship a bare code block.** Every snippet carries either a sentence saying what it does and why the
reader is running it now, or a bold one-line label above it. The label form lets a skimmer read only the bold
lines and still follow the sequence.

**Surface a blocking prerequisite before the reader spends effort**, not inside the setup section where they
find it half-committed. Anything that can stop them — a platform requirement, an account, a cost — belongs
above the first instruction.

Never invent output. If you cannot verify what the command prints, say so and leave the example unpadded
rather than fabricating a plausible transcript.

## Cut Hard

Common sections that usually answer nothing, and what to do instead:

| Section                             | Verdict                                                                              |
| ----------------------------------- | ------------------------------------------------------------------------------------ |
| Contributing, Changelog             | One-line pointer to the file. The prose belongs in `CONTRIBUTING.md`.                |
| License                             | One line naming the licence and linking `LICENSE`. Never the text.                   |
| Table of contents                   | Earns its place from roughly six top-level sections; below that it is furniture.     |
| Features, as a bullet list of nouns | Fold into question 2, or show it in the example instead.                             |
| Roadmap, Acknowledgements, Author   | Only where a reader's decision depends on it.                                        |
| Badges                              | Only where they report live state a reader would act on.                             |
| CLI options, as a Markdown table    | Use a fenced block mirroring real `--help` output — it cannot drift from the binary. |

A front door that links out is doing its job. Length is not thoroughness — every line the reader must scan
past to reach question 4 is a cost.

## Every Device Earns Its Place — but Never Add One Uninvited

**Do not apply a table of contents, badge row, centered masthead, emoji, logo or raw HTML on your own
initiative.** Produce the document without them, then say which ones you would add and why the trigger below
is met. The user decides. Apply one unasked only where the surrounding documentation set already uses it, and
consistency is the stronger claim.

The triggers are the grounds for a recommendation, not permission to act on it. Each device solves one reader
problem, and a recommendation that cannot name the problem is decoration:

- **Table of contents** — from roughly six top-level sections, where a reader would otherwise scroll past
  three screens to reach a section they already know they want. Form follows how self-explanatory the titles
  are: a bullet list, a horizontal nav row for a short flat document, or a two-column table with a gloss where
  titles like "Pipeline" do not explain themselves. It goes below the opening block, never above it.
- **Badges** — one per distinct trust question a skeptical adopter would otherwise check by hand: does it run
  on my system, is it maintained, does the suite pass, what licence, what version. Five is the observed
  ceiling. Omitting one is a decision too: a project with no build carries no build badge.
- **Centered masthead** — only where three or more elements stack above the fold. Where prose starts a line or
  two after the title, leave it left-aligned.
- **Raw HTML** — where the layout is something Markdown cannot express: grouped badge rows, a bordered box, a
  forced line break inside a table cell, an image sized to signal importance. A document that is linear text
  and code gains nothing from it.
- **Admonitions** — for a skippable aside, never a required step, so that skimming past one costs nothing.
  Calibrate the type to the severity rather than repeating one. GitHub-only; they degrade to blockquotes
  elsewhere.
- **Emoji** — where they do a job, such as marking each section in a long table of contents for scanning.

Length is not the defect. **Undirected** length is, and so is a device answering no reader question. A long
document with the aids that make it navigable beats a short one that had to cut real content — but every aid
must trace to a problem the content created.

So the plain version reaches the user first, with the recommendations named beside it. A reader who wanted no
badges and got them has to remove them; a reader who wanted them has to say one word.

## Humor Is Allowed, in Exactly One Place

Personality is not a cost. Two of the strongest exemplars are funny, and they independently obey one rule:
**a joke lives in the motivating sentence before an instruction — never inside a bullet, a step, a table cell,
or any sentence the reader must act on correctly.**

One confines humor to its introduction and its community section, and is entirely dry through features,
prerequisites, install and troubleshooting — every section a reader consults under pressure. The other jokes in
each command's lead-in, then drops straight into a joke-free list of exactly what that command does. The dry
specification immediately after is what keeps the humor from costing credibility.

A joke inside an instruction creates real ambiguity about whether a step is optional. A joke with nothing dry
following it leaves the reader holding only the joke. An in-joke is safe only where the audience's shared
knowledge is safe to assume.

## Match the Set Before Imposing a Default

When the project already has documentation, infer its conventions before drafting: heading style, register,
example density, decoration. Two documents make a convention; one is a coincidence.

An evidenced house convention outranks this skill's defaults for anything it covers. Consistency across a
project serves a reader more than one improved page. `writing-documentation` carries the fuller method for
building a style profile.

## Modes

- **Draft.** Establish what the project is and who it serves before writing a line. Where that is not
  recoverable from the repository, ask rather than guess — an invented purpose is the one error nothing
  downstream repairs. Deliver the plain document, then list the devices you recommend and the trigger each
  one meets.
- **Rewrite.** Diagnose first, in the terms of the five questions: which are unanswered, which are answered
  out of order, which sections answer nothing. Show the diagnosis before producing the replacement. Preserve
  every accurate claim; this mode changes the framing, not the facts.
- **Critique.** Report against the five questions and the Iron Law, worst first, each finding naming the
  reader question it fails. Judge quality only, and route factual verification to `repo-management`. Do not
  edit the file unless the user asked for a rewrite.

For an existing file, return the text or a diff unless the user asked for an in-place edit.

## Review

- Can a stranger answer "what is this" and "is it for me" from the first five lines alone?
- Is there concrete evidence it works, before the install instructions?
- Does the document state what the project does not do?
- Can a reader get to a working result from the shortest path shown, without leaving the page?
- Does every section map to one of the five questions?
- Are Contributing, Changelog and License pointers rather than prose?
- Is every example real, with real values and unfabricated output?
- Is every device present either requested, or already conventional in the surrounding set?
- Were the devices you did not add named as recommendations, with the trigger that justifies each?

Read [references/exemplars.md](references/exemplars.md) for worked patterns distilled from front doors that
demonstrably read well, and the moves behind them.
