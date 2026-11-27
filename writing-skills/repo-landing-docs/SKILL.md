---
name: repo-landing-docs
description: "Write, refresh, or critique a repository's landing documents from bundled templates (README, quickstart or docs landing page, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, SUPPORT, GOVERNANCE, FUNDING.yml, CHANGELOG, ROADMAP, LICENSE, issue and pull request templates). Use when a repository needs one of these, when its README reads flat or template-filled, when its landing docs need refreshing, or when someone asks whether one is good. Not for tutorials, how-tos, references, or runbooks (writing-documentation), for checking whether their claims are still true (context-architecture), or for config files and hooks (repo-setup)."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Repository Landing Docs

Use this skill for the documents a visitor reads to judge a project, use it, contribute to it, or follow where it
is going. The README and its kin, the quickstart and the documentation landing page, are the project's front door.
A front door is the first thing a stranger reads about the project. Someone who has not decided to care yet judges
it in about ten seconds. The other landing documents serve a visitor who has a specific question, such as how to
report a vulnerability or how to get a change accepted.

- `writing-documentation` owns tutorials, how-to guides, references, explanations, runbooks and decision
  records.
- `repo-setup` owns configuration files, hooks, and the repository bootstrap that calls this skill.
- `context-architecture` owns the truth audit that checks a document's claims against the tree.
- `writing-for-humans` owns the sentences. Load it before drafting prose, and finish with its reader-ready pass
  as well as this skill's Before Delivery checks.
- `markdown-tools` owns mechanical Markdown work. Where the repository wraps lines with trailing-backslash hard
  breaks, rewrap a finished document with its `mdwrap.py` rather than by hand.

Plain language, as ISO 24495-1:2023 defines it, is wording, structure, and design so clear that the intended
readers can easily do three things. They find what they need, understand what they find, and use that
information. The README's five questions apply the standard's relevant and findable principles to a stranger
who has not yet chosen the project. "Write for a Stranger" applies its understandable principle.

A review request splits by what is being judged. "Does it read well" is this skill; "is it still true" is
`context-architecture`'s truth audit. A thorough review wants both.

## Iron Law

**Every section answers a reader question, or it goes.**

A section earns its place by answering something the reader is actually asking at the moment they reach it.
Convention and presence in a template earn nothing. Given a list of sections, an agent fills all of them, and
the result is uniformly flat because nothing in it was chosen.

## Workflow

- **Draft.** Establish what the project is and who it serves before writing a line. Where the repository does
  not settle it, ask; an invented purpose is the one error nothing downstream repairs. Start from the file's
  template in `assets/`. Deliver the plain document. For a README, then list the devices you recommend and the
  trigger each one meets. Done when every [Before Delivery](#before-delivery) item passes.
- **Refresh.** Inventory the landing documents the repository has and where each lives. Decide which ones its
  kind of project needs, using [Choose the Files](#choose-the-files). Propose the set: each file to add, rewrite,
  or leave, with its reason. Then draft or rewrite each approved file. Done when every approved file passes its
  checks and every file left alone is named.
- **Rewrite.** Diagnose against the reader questions first: which are unanswered, which are answered out of
  order, which sections answer nothing. Show the diagnosis before the replacement. This mode changes the
  framing, not the facts. Done when every accurate claim of the original survives or is listed as cut with its
  reason. Every Before Delivery item must pass too.
- **Critique.** Report as [Critique Report](#critique-report) describes. Judge quality only, and route factual
  verification to `context-architecture`'s truth audit. Done when every section is mapped to a question or
  reported as answering none.

Return text or a diff for an existing file unless the user asked for an in-place edit.

Before drafting, rewriting, or critiquing a file, read its reference:

- for the README, quickstart, or docs landing page, [references/readme.md](references/readme.md): the five reader
  questions, the opening, evidence, cuts, devices, and its own checks;
- for any other landing file, [references/landing-files.md](references/landing-files.md): the rules each file's
  template cannot carry, and the check that tells you each file is done.

## Choose the Files

Each file answers one visitor question. Add a file when its question will be asked; a file nobody needs is one
more to keep true.

| File                             | Visitor question                           | Add it when                                       |
| -------------------------------- | ------------------------------------------ | ------------------------------------------------- |
| `README.md`                      | What is this, and is it for me?            | Always                                            |
| `LICENSE`                        | May I use this?                            | The user has chosen a licence                     |
| `CONTRIBUTING.md`                | How do I get a change accepted?            | Outsiders may send changes                        |
| `SECURITY.md`                    | How do I report a vulnerability privately? | The project is public                             |
| `CODE_OF_CONDUCT.md`             | How will I be treated, and whom do I tell? | People other than the maintainer interact         |
| Issue and pull request templates | What do the maintainers need from me?      | Outsiders open issues or pull requests            |
| `CHANGELOG.md`                   | What changed for me since my version?      | Users upgrade between versions or dated states    |
| `ROADMAP.md`                     | Where is this going, and is my need on it? | Users plan around the project's direction         |
| `SUPPORT.md`                     | Where do I get help?                       | Help requests arrive in the wrong channel         |
| `GOVERNANCE.md`                  | Who decides, and how?                      | More than one person holds merge or release power |
| `FUNDING.yml`                    | How do I pay for this?                     | The maintainers accept money                      |

Each file's template sits in `assets/` under the file's name, such as `assets/SECURITY.template.md`. The issue
templates are in `assets/ISSUE_TEMPLATE/`, and the pull request template is `assets/PULL_REQUEST_TEMPLATE.md`. The
changelog has a versioned and a dated template. `LICENSE` has none; use the licence's canonical text.

For the README, read [references/readme-by-audience.md](references/readme-by-audience.md) to choose between the
generic, open-source, personal, internal, and configuration templates. Its section matrix settles which sections a
project type needs; the rest of this file makes them worth reading.

Fill a template completely, and replace every `{{PLACEHOLDER}}` with a fact from the repository or the user. A
plausible invented contact, command, or response time misleads the visitor who acts on it. When no source supplies
a fact, leave its placeholder and name it in your report. Delete each section that answers no question for this
project.

### Place the Files

Follow the repository's convention first. Many repositories keep `CHANGELOG.md` and `ROADMAP.md` under `docs/`.
Without a convention, put each file at the root. The issue templates, the pull request template, and `FUNDING.yml`
go in `.github/` instead. GitHub reads `README.md` and the community files from `.github/`, the root, or `docs/`, in
that order. The community files are `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, and `SUPPORT.md`. A
copy in `.github/` therefore hides one at the root. `FUNDING.yml` works only in `.github/`, and `LICENSE` stays at
the root by convention.

Point to each other landing file that exists from the README in one line, at the path where it lives. That covers
`CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `SUPPORT.md`, `CHANGELOG.md`, `ROADMAP.md`, `GOVERNANCE.md`,
and `LICENSE`. Where the audience matrix marks a section "No" for the project type, its pointer goes too.

## Write for a Stranger

The reader does not share your knowledge anywhere on the page. Explain each term they may not know, whether
project-specific or a standard, format, or technique, once at first use. Link an unfamiliar tool or standard to
its own documentation rather than describing it.

Give each sentence one idea. Keep an instruction to one action in the imperative, within 20 words, with any
condition before its command. Keep any other sentence within 25 words. These limits are this skill's proxies,
adapted from ASD-STE100; ISO 24495-1 judges a text by how well its readers use it. Prefer the familiar word and
the verb that carries the meaning, and give each concept one term.

Lead each section and paragraph with its point. Bold only the one-line label above a code block or a hazard the
reader must not miss. Never bold the opening words of every list item. Keep every fact, number, and condition the
project's own sources give, and state nothing they do not.

## Match the Set Before Imposing a Default

When the project already has documentation, infer its conventions before drafting: heading style, register,
example density, decoration. Two documents make a convention; one is a coincidence. An evidenced house
convention outranks this skill's defaults for anything it covers, because consistency across a project serves
a reader more than one improved page. `writing-documentation` carries the fuller method for building a style
profile. With no documentation set to match, this skill's defaults govern.

## Before Delivery

For every landing file:

- Is every placeholder replaced by a sourced fact, or left in place and named in your report?

- Does the file sit where the repository's convention, or the placement default, puts it?

- Where Place the Files calls for a README pointer, does it name the path where the file lives?

- Does every sentence carry one idea within its limit, with each condition before its command?

- Is every term a stranger may not know explained or linked at first use?

- Does each section lead with its point, with bold limited to code-block labels and hazards?

- Did every fact, number, and condition from the project's sources survive, with nothing added they do not state?

- For the README and its front-door kin, did every check in `references/readme.md` pass too?

## Critique Report

A critique judges how well each file answers its visitor's questions, and changes nothing. Report:

1. **Verdict**: `Ready`, `Ready after changes`, or `Not ready`, then one sentence saying whether a visitor gets
   the file's questions answered, in order. Any open Must fix finding rules out `Ready`; use `Not ready` when the
   file needs a rewrite rather than local fixes.
2. **Scope**: the files and their revision, the template or audience row judged against, and the section map:
   each section with the reader question it answers, or "none".
3. **Findings**, most consequential first, each tagged `F1`, `F2`, and so on. Give each its tier, the section,
   the reader question it fails, what that costs the visitor, and the fix as a concrete change.
   - **Must fix**: the file fails the question it exists for. Examples are a README that never says what the
     project is or how to start, a `SECURITY.md` with no private channel, and a placeholder or invented fact
     left in.
   - **Should fix**: a question answered late or out of order, a section that answers no question, a term a
     stranger cannot follow, or template filler.
   - **Consider**: an optional improvement. Report at most five, and say how many you left out.
4. **Unverified**: each claim whose truth the critique cannot judge, such as a command or a contact, left for
   `context-architecture`'s truth audit.
5. **Next checks**: that truth audit, and any check from the file's reference still to run.
6. **What holds**, only when something specific should survive a rewrite: at most two sentences, with its
   location.

A clean file gets the verdict, the scope, and the next checks.
