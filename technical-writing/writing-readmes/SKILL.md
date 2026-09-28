---
name: writing-readmes
description: "Write, rewrite, or critique a README or other project front door (quickstart, getting-started page, docs landing page) so a stranger sees the point and can start. Use when a README reads flat or template-filled, a project needs one, or someone asks whether one is good. Not for tutorials, how-tos, references, or runbooks (writing-documentation), or for checking claims or scaffolding files (repo-management)."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Writing READMEs

Use this skill for a project's front door: the README, the quickstart or getting-started page, the
documentation landing page. A front door is the first thing a stranger reads about the project, and it is
judged in about ten seconds by someone who has not decided to care yet. Every other document is read by
someone who already chose the project.

- `writing-documentation` owns tutorials, how-to guides, references, explanations, runbooks and decision
  records.
- `repo-management` owns repository scaffolding, the README templates and audience matrix, and the accuracy
  audit that checks a README's claims against the tree.
- `writing-for-humans` owns the sentence and the paragraph, and its reader-ready check closes every draft here.

A review request splits by what is being judged: **does it read well** is this skill, **is it still true** is
`repo-management`'s audit. A thorough review wants both.

## Iron Law

**Every section answers a reader question, or it goes.**

A front door is not a form to complete. A section earns its place by answering something the reader is
actually asking at the moment they reach it, not by being conventional or appearing in a template. Given a
list of sections, an agent fills all of them, and the result is uniformly flat because nothing in it was
chosen.

## Workflow

- **Draft.** Establish what the project is and who it serves before writing a line. Where the repository does
  not settle it, ask; an invented purpose is the one error nothing downstream repairs. Deliver the plain
  document, then list the devices you recommend and the trigger each one meets. Done when every
  [Before Delivery](#before-delivery) item passes.
- **Rewrite.** Diagnose against the five questions first: which are unanswered, which are answered out of
  order, which sections answer nothing. Show the diagnosis before the replacement. This mode changes the
  framing, not the facts. Done when every accurate claim of the original survives or is listed as cut with its
  reason, and every Before Delivery item passes.
- **Critique.** Report against the five questions and the Iron Law, worst first, each finding naming the
  reader question it fails. Judge quality only, and route factual verification to `repo-management`. Done when
  every section is mapped to a question or reported as answering none.

Return text or a diff for an existing file unless the user asked for an in-place edit.

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
gets cut. Three consequences are commonly got wrong:

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
- **The point first.** Open on what the project is, not on the problem domain's history, "In today's world",
  or the project name restated as a definition.
- **Words the reader already knows.** A term the reader must already know to parse the first sentence has
  cost you the reader.

Test it by deleting everything after the first five lines and asking whether a stranger could say what the
project is and whether it is for them. If not, the opening is not carrying its weight, no matter what follows.

The reader does not share your knowledge anywhere else on the page either. Explain each project-specific term
once, at first use, and link an unfamiliar tool to its own documentation rather than describing it.

## Show It Working Before Asking for Anything

Concrete evidence answers question 3 and no amount of description substitutes.

- A short, real, copy-pasteable example with its actual output.
- A screenshot, terminal recording or diagram where the result is visual.
- Real values, not `foo` and `bar`. Invented placeholder data reads as a project nobody has run.

Keep it minimal. Strip setup that does not affect the result. One example that runs beats three that
illustrate.

**Frame every code block.** Each snippet carries either a sentence saying what it does and why the reader is
running it now, or a bold one-line label above it. The label form lets a skimmer read only the bold lines and
still follow the sequence.

**Surface a blocking prerequisite before the reader spends effort**, not inside the setup section where they
find it half-committed. Anything that can stop them — a platform requirement, an account, a cost — belongs
above the first instruction.

Show only output you have verified. If you cannot run the command, say so and leave the example unpadded
rather than fabricating a plausible transcript.

## Cut Hard

Common sections that usually answer nothing, and what to do instead:

| Section                             | Verdict                                                                              |
| ----------------------------------- | ------------------------------------------------------------------------------------ |
| Contributing, Changelog             | One-line pointer to the file. The prose belongs in `CONTRIBUTING.md`.                |
| License                             | One line naming the licence and linking `LICENSE`. Never the text.                   |
| Features, as a bullet list of nouns | Fold into question 2, or show it in the example instead.                             |
| Roadmap, Acknowledgements, Author   | Only where a reader's decision depends on it.                                        |
| CLI options, as a Markdown table    | Use a fenced block mirroring real `--help` output — it cannot drift from the binary. |

A front door that links out is doing its job. Every line the reader must scan past to reach question 4 is a
cost.

## Recommend Devices; Apply Them on Request

Produce the document plain: no table of contents, badge row, centered masthead, emoji, logo or raw HTML. Then
say which devices you would add and which trigger below each one meets. The user decides. Apply one unasked
only where the surrounding documentation set already uses it, because consistency is the stronger claim.

Each device solves one reader problem, and a recommendation that cannot name the problem is decoration:

- **Table of contents** — from roughly six top-level sections, where a reader would otherwise scroll past
  three screens to reach a section they already know they want. It goes below the opening block, never above
  it.
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

Undirected length is the defect, not length: every aid and every line traces to a reader problem. A long
document with the aids that make it navigable beats a short one that had to cut real content. The plain
version reaches the user first because a reader who wanted no badges and got them has to remove them, while a
reader who wanted them has to say one word.

## Humor Is Allowed, in Exactly One Place

Personality is not a cost. **A joke lives in the motivating sentence before an instruction — never inside a
bullet, a step, a table cell, or any sentence the reader must act on correctly.** Keep every section a reader
consults under pressure dry: prerequisites, install, troubleshooting. Follow each joke with the dry
specification it introduces; that is what keeps the humor from costing credibility.

A joke inside an instruction creates real ambiguity about whether a step is optional. An in-joke is safe only
where the audience's shared knowledge is safe to assume.

## Match the Set Before Imposing a Default

When the project already has documentation, infer its conventions before drafting: heading style, register,
example density, decoration. Two documents make a convention; one is a coincidence. An evidenced house
convention outranks this skill's defaults for anything it covers, because consistency across a project serves
a reader more than one improved page. `writing-documentation` carries the fuller method for building a style
profile. With no documentation set to match, this skill's defaults and `writing-for-humans` govern.

## Before Delivery

- Can a stranger answer "what is this" and "is it for me" from the first five lines alone?
- Is there concrete evidence it works, before the install instructions?
- Does the document state what the project does not do?
- Can a reader get to a working result from the shortest path shown, without leaving the page?
- Does every section map to one of the five questions?
- Are Contributing, Changelog and License pointers rather than prose?
- Is every example real, with real values and verified output?
- Is every device present either requested, or already conventional in the surrounding set?
- Were the devices you did not add named as recommendations, with the trigger that justifies each?
- Did the text pass `writing-for-humans`' reader-ready check, with every project-specific term explained or
  linked at first use?

Read [references/exemplars.md](references/exemplars.md) for the evidence behind these rules and the finer
moves: table-of-contents forms, categorized badge rows, opening shapes, and named moves with their conditions.
