# The README and Its Front-Door Kin

Rules for the README, the quickstart or getting-started page, and the documentation landing page. A stranger who
has not decided to care yet judges these pages in about ten seconds.

## Contents

- [The Five Questions](#the-five-questions)
- [Answer Question 1 in the First Five Lines](#answer-question-1-in-the-first-five-lines)
- [Show It Working Before Asking for Anything](#show-it-working-before-asking-for-anything)
- [Cut Hard](#cut-hard)
- [Recommend Devices; Apply Them on Request](#recommend-devices-apply-them-on-request)
- [Humor Is Allowed, in Exactly One Place](#humor-is-allowed-in-exactly-one-place)
- [Before Delivery](#before-delivery)

## The Five Questions

A stranger works through these questions in order. They abandon the page at the first one that goes unanswered.

1. **What is this?** One sentence, concrete and literal. They should be able to repeat it to a colleague.
2. **Is it for me?** Who it serves, what problem it solves, and (the part most READMEs skip) what it does
   not do and who should use something else.
3. **Does it actually work?** Evidence before claims. Output, a screenshot, a real example with a real result.
4. **How do I start?** The shortest path from nothing to a working result.
5. **Where do I go next?** Pointers onward. Where readers will get stuck, order the pointers by how fast they
   resolve. Use this order: in-tool help, a diagnostic command, the FAQ, issue search, then a human. "See the
   docs" is the weakest version of this.

Order sections by these questions rather than by convention. Any candidate section maps to one of the five or
gets cut. Three consequences are commonly got wrong:

- **Question 3 comes before question 4.** A reader who is not yet convinced will not run your install command.
  Show the thing working, then tell them how to get it.
- **Question 2 requires a limit.** A front door that claims no boundary reads as marketing. A reader who
  discovers the boundary after installing is angrier than one who was told. Naming the alternatives and who
  each suits costs nothing and buys more credibility than any claim you can make about yourself.
- **Where the project resembles something the reader already has, say the reader's objection out loud.** State
  it verbatim, *"But doesn't X already do this?"*, then answer it with a concrete scenario. Hoping the
  reader infers the difference leaves the whole document's case unmade.

A released project has a sixth reader the five questions miss: the returning user, asking *what changed
for me*. They look in the README, not the changelog. Where a version boundary breaks something, keep the
migration note here.

## Answer Question 1 in the First Five Lines

The opening is the whole document's fate. Write it last, once you know what the project actually is, and hold
it to:

- **A title, then one sentence.** Not a paragraph. The sentence names what the thing is and what it is for,
  in the reader's vocabulary rather than the implementation's.
- **The point first.** Open on what the project is. Do not open on the problem domain's history, "In today's
  world", or the project name restated as a definition.
- **Words the reader already knows.** A term the reader must already know to parse the first sentence has
  cost you the reader.

Test the opening by deleting everything after the first five lines. Ask whether a stranger could say what the
project is and whether it is for them. If not, the opening is not carrying its weight, no matter what follows.

## Show It Working Before Asking for Anything

Concrete evidence answers question 3 and no amount of description substitutes.

- A short, real, copy-pasteable example with its actual output.
- A screenshot, terminal recording or diagram where the result is visual, with alt text stating what it shows.
- Real values, not `foo` and `bar`. Invented placeholder data reads as a project nobody has run.
- Sourced figures for any claim of popularity, speed, or adoption. "Trusted by thousands" and "blazing fast" are
  claims a stranger cannot check, so give the number and its source, or cut the claim.

Keep it minimal. Strip setup that does not affect the result. One example that runs beats three that
illustrate.

**Frame every code block.** Each snippet carries either a sentence saying what it does and why the reader is
running it now, or a bold one-line label above it. The label form lets a skimmer read only the bold lines and
still follow the sequence.

**Surface a blocking prerequisite before the reader spends effort**, not inside the setup section where they
find it half-committed. Anything that can stop them (a platform requirement, an account, a cost) belongs
above the first instruction.

Show only output you have verified. If you cannot run the command, say so and leave the example unpadded
rather than fabricating a plausible transcript.

## Cut Hard

Common sections that usually answer nothing, and what to do instead:

| Section                             | Verdict                                                                             |
| ----------------------------------- | ----------------------------------------------------------------------------------- |
| Contributing, Changelog             | One-line pointer to the file. The prose belongs in `CONTRIBUTING.md`.               |
| License                             | One line naming the licence and linking `LICENSE`. Never the text.                  |
| Features, as a bullet list of nouns | Fold into question 2, or show it in the example instead.                            |
| Roadmap, Acknowledgements, Author   | Only where a reader's decision depends on it.                                       |
| CLI options, as a Markdown table    | Use a fenced block mirroring real `--help` output; it cannot drift from the binary. |

A front door that links out is doing its job. Every line the reader must scan past to reach question 4 is a
cost.

## Recommend Devices; Apply Them on Request

Produce the document plain: no table of contents, badge row, centered masthead, emoji, logo or raw HTML. Then
say which devices you would add and which trigger below each one meets. The user decides. Apply one unasked
only where the surrounding documentation set already uses it, because consistency is the stronger claim.

Each device solves one reader problem, and a recommendation that cannot name the problem is decoration:

- **Table of contents**: from roughly six top-level sections, where a reader would otherwise scroll past
  three screens to reach a section they already know they want. It goes below the opening block, never above
  it.
- **Badges**: one per distinct trust question a skeptical adopter would otherwise check by hand. Typical
  questions: does it run on my system, is it maintained, does the suite pass, what licence, what version.
  Five is the observed ceiling. Omitting one is a decision too: a project with no build carries no build badge.
- **Centered masthead**: only where three or more elements stack above the fold. Where prose starts a line or
  two after the title, leave it left-aligned.
- **Raw HTML**: where the layout is something Markdown cannot express. Examples: grouped badge rows, a
  bordered box, a forced line break inside a table cell, an image sized to signal importance. A document that
  is linear text and code gains nothing from it.
- **Admonitions**: for a skippable aside, never a required step, so that skimming past one costs nothing.
  Calibrate the type to the severity rather than repeating one. GitHub-only; they degrade to blockquotes
  elsewhere.
- **Emoji**: where they do a job, such as marking each section in a long table of contents for scanning.

The defect is undirected length, not length itself: every aid and every line traces to a reader problem. A long
document with the aids that make it navigable beats a short one that had to cut real content. The plain
version reaches the user first because the costs are asymmetric. A reader who wanted no badges and got them
has to remove them, while a reader who wanted them has to say one word.

## Humor Is Allowed, in Exactly One Place

Personality is not a cost. A joke lives in the motivating sentence before an instruction. A joke never lives
inside a bullet, a step, a table cell, or any sentence the reader must act on correctly. Keep every section a
reader consults under pressure dry: prerequisites, install, troubleshooting. Follow each joke with the dry
specification it introduces; that is what keeps the humor from costing credibility.

A joke inside an instruction creates real ambiguity about whether a step is optional. An in-joke is safe only
where the audience's shared knowledge is safe to assume.

## Before Delivery

These checks come on top of the checks for every landing file in `SKILL.md`.

- Can a stranger answer "what is this" and "is it for me" from the first five lines alone?
- Is there concrete evidence it works, before the install instructions?
- Does the document state what the project does not do?
- Can a reader get to a working result from the shortest path shown, without leaving the page?
- Does the install section cover every install route, with a minimum runtime or interpreter version rather than
  an exact one?
- Does every section map to one of the five questions?
- Are Contributing, Changelog and License pointers rather than prose?
- Is every example real, with real values and verified output?
- Does every popularity, speed, or adoption claim carry a sourced figure?
- Is every device present either requested, or already conventional in the surrounding set?
- Were the devices you did not add named as recommendations, with the trigger that justifies each?

Read [exemplars.md](exemplars.md) for the evidence behind these rules. It also holds the finer moves:
table-of-contents forms, categorized badge rows, opening shapes, and named moves with their conditions.
