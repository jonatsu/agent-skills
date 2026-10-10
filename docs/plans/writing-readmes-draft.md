# writing-readmes — brainstorm draft

**Status:** implemented, one item deferred. The skill ships at `skills/shared/writing/writing-readmes/`,
`repo-management` and `writing-documentation` route to it, the template trim is applied, and the acceptance
gate passed — the root `README.md` was rewritten with the skill and accepted by the user on 2026-09-10.

**Stays active** because the deferred `evals/behavior.json` row below is still future work this plan owns.
Archive it to `docs/plans/archived/` once that eval exists or the user drops it.

**Date:** 2026-09-10

## Original idea

The user is unhappy with how READMEs currently come out and wants README writing split into a dedicated skill.
The seed was a `create-readme` skill draft carrying: a senior-engineer role preamble, four exemplar README URLs,
restrained emoji, no LICENSE/CONTRIBUTING/CHANGELOG sections, GFM plus GitHub admonitions, and a logo in the
header.

## Purpose

A front-door document should make a stranger want to use the project and able to start. Today that outcome has
no owner: the material is split three ways and none of it teaches the craft.

## Starting state

| Where                                         | What it owns today                                                                                               |
| --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `skills/shared/git/repo-management`           | 5 README templates, `references/readme-by-audience.md` (4 audience types, section matrix), README accuracy audit |
| `skills/shared/writing/writing-documentation` | Genre guidance incl. Diátaxis modes; mentions README twice, in passing                                           |
| `skills/shared/writing/writing-for-humans`    | Prose quality, invoked by both                                                                                   |

Confirmed defect, all four at once (user): guidance never loads for a README request; output is bland
template-fill; the section matrix is the wrong content model because it names sections without saying why one
earns its place; and the guidance is fragmented so any single invocation gets a third of it.

House practice, measured across `README.md`, `skills/README.md`, `services/README.md`: zero emoji, zero badges,
zero admonitions.

## Decisions

| Decision                                    | Recommended                                                                                    | Chosen                                                                                                                     | Why                                                                                                                                                                         | Status   |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| What is wrong today                         | Discovery + wrong content model, with bland output as the symptom                              | All four: discovery, output quality, content model, fragmentation                                                          | User confirmed every candidate defect                                                                                                                                       | resolved |
| How much the new skill owns                 | Full ownership incl. templates and audit                                                       | Craft only — `repo-management` keeps bootstrap, audience matrix, templates and the accuracy audit                          | A craft skill and a hygiene skill are different jobs; moving assets was not worth the cross-skill dependency                                                                | resolved |
| Discriminator vs `writing-documentation`    | By artifact, not by axis                                                                       | By artifact                                                                                                                | An axis test ("appeal vs comprehension") is a judgement made at load time by an agent that has read neither skill — that is the discovery defect                            | resolved |
| Where the how-to line falls                 | Front door only; standalone how-to guides stay in `writing-documentation`                      | Front door only                                                                                                            | A how-to is read by someone who already chose the project; it needs correct steps, not a hook                                                                               | resolved |
| Spine of the skill                          | Reader-journey, exemplars as reference, rubric as verification                                 | Same                                                                                                                       | A journey supplies the cut criterion the section matrix lacks                                                                                                               | resolved |
| Modes                                       | Draft + rewrite + quality critique                                                             | Same                                                                                                                       | The motivating request is rewrite-what-exists; without critique a "review my README" lands on the accuracy audit and passes a boring README                                 | resolved |
| Two skills with a review mode               | State each other's trigger in one line                                                         | Same, explicitly                                                                                                           | Descriptions alone have already failed to disambiguate once                                                                                                                 | resolved |
| Name                                        | `writing-readmes`                                                                              | `writing-readmes`                                                                                                          | Names the word users actually say; fits the `writing/` family. Scope gap covered by the description                                                                         | resolved |
| LICENSE / CONTRIBUTING / CHANGELOG sections | One-line pointers, no section bodies; update `repo-management`'s templates and matrix to match | Same                                                                                                                       | Prose maintained in two files drifts; "where do I go next" is answered by a pointer                                                                                         | resolved |
| Decoration                                  | Codify house practice: off by default                                                          | Never auto-applied; the agent recommends, the user decides. Applied unasked only where the surrounding set already uses it | Reaffirmed after nine-exemplar evidence argued for triggers. Removing an unwanted badge row costs more than asking for one                                                  | resolved |
| Device triggers                             | Replace taste with checkable conditions                                                        | Adopted, as grounds for a recommendation only                                                                              | TOC at ~6 top-level sections; one badge per trust question a skeptic would check by hand; center at 3+ stacked elements; HTML only where Markdown cannot express the layout | resolved |
| Humor                                       | Permit it, confined to motivating prose                                                        | Same                                                                                                                       | Two independent authors obey the identical rule: never inside a bullet, step or anything acted on; a dry spec must follow the joke                                          | resolved |
| Acceptance evidence                         | Validators + one real rewrite, judged by the user                                              | Same; target `README.md` at repo root                                                                                      | A green validator never shows the skill is useful on the corpus that motivated it                                                                                           | resolved |
| `evals/behavior.json`                       | Write after the skill has run, non-blocking                                                    | Deferred                                                                                                                   | **Cost:** no regression check, so a later edit can undo the spine and only a human read would catch it                                                                      | deferred |
| Exemplar licensing                          | Distill patterns in our own words; cite URLs; stay MIT                                         | Same                                                                                                                       | Structural patterns are not the copyrightable part; avoids licence inheritance and verifying four upstream licences                                                         | resolved |

## Direction

A new `skills/shared/writing/writing-readmes/` teaching how to make a front door good, organized around the
sequence of decisions a stranger makes: what is this → is it for me → does it actually work → how do I start →
where do I go next. Sections derive from the question they answer, so a section answering nothing is cut.

Three modes on that one spine: draft, rewrite, quality critique. Factual verification is not its job and routes
to `repo-management` by name.

## Scope

**In:** READMEs, quickstart and getting-started material, `docs/index` and project landing pages — anything a
stranger reads first. Drafting, rewriting, and quality critique. Distilled exemplar reference material. A
one-line trigger cross-reference added to `repo-management` and `writing-documentation`. Trimming
LICENSE/CONTRIBUTING/CHANGELOG bodies to pointers in `repo-management`'s templates and matrix.

**Out:** Diátaxis how-to guides, tutorials, references, explanations, records — `writing-documentation` keeps
these. Repository bootstrap, the audience matrix, the templates themselves, and the README accuracy audit —
`repo-management` keeps these. Prose-level editing — `writing-for-humans`.

**Parked:** `evals/behavior.json`. A `skills/copilot/` group. Whether `writing-documentation` should shed more
genres.

## Constraints and assumptions

- Placement `skills/shared/writing/writing-readmes/` needs no `base.yaml` edit; the `writing` domain exists
  (repository fact).
- A skill edit is two commits, the second being `just skills-sync` (repository rule).
- Editing `repo-management` assets is a stated, narrow exception to that skill keeping them — agreed in the
  Q8 decision, not a reopening of ownership.
- The exemplar URLs are user-supplied handed-over research and go to a subagent, per the user's standing rule.
  They are recorded in agent memory as `readme-inspiration-sources`.
- **Assumption, unverified:** the exemplars' JS/Azure-sample shape transfers to this repo's corpus of Python
  tools, Nix config and skill packages. The real-rewrite gate is what tests it.
- The seed's role preamble ("senior expert", "take a deep breath") is dropped as cargo-cult prompting; that is
  an authoring-craft call, not a user decision.

## Observable success signal

A rewritten root `README.md` that the user prefers to the current one on a single read, without being asked to
grade it against a checklist.

## Questions for technical design

- What is the minimum spine content in `SKILL.md` versus `references/`, given the skill must load usefully at
  its own size budget?
- How does the critique mode report — findings-first like `security-review`, or a graded pass?
- Does the reader-journey spine need a distinct shape for the config/dotfiles audience, whose reader is
  future-you rather than a stranger?
- What exactly do the two cross-reference lines say, and where do they go in each file?
