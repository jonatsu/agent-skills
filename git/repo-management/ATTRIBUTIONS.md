# Attributions

## Current skill

- Skill: `repo-management`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: original skill; one component adapted from upstream

## Adapted component

- Component: the README project-type taxonomy — the audience section matrix in
  `references/readme-by-audience.md` and the audience template assets (`assets/README.oss.template.md`,
  `README.personal.template.md`, `README.internal.template.md`, `README.config.template.md`) — plus, added
  2026-08-25, the stale-README check in `SKILL.md`.
- Upstream project: [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit), skill
  `crafting-effective-readmes`.
- Upstream revision: `011baf4acea99174acb5486a9b662a7e084be63b`.
- Upstream license: MIT, Copyright (c) 2026 Leonardo Flores. Read from the repository's `LICENSE` file on
  2026-08-25; the copyright line was missing from this file until then, which left the notice below
  incomplete.

## Adaptation note

Only the taxonomy (four project types, the section-by-audience matrix, and the per-audience section sets) was
carried over. The templates were rewritten to this skill's `{{PLACEHOLDER}}` convention and anti-patterns — no
fabricated badges, emails, or URLs — and the generic `assets/README.template.md` remains the default. The rest
of `repo-management` is original.

## Re-review, 2026-08-25

The upstream skill was read in full — `SKILL.md`, `README.md`, `style-guide.md`, `section-checklist.md`,
`using-references.md` and all four templates — to find what the first adoption left behind. One idea had been:
its "Reviewing" task, which reads an existing README and checks it against the project's actual state. Nothing
in this repository's skills owned that check. `writing-documentation`'s review checklist grades prose,
`agents-management` reads the README only to avoid duplicating it into AGENTS.md, and this skill's REFRESH
mode left a README that "already exists and is healthy" alone without ever testing healthy. It is implemented
here as report-only, per this skill's Iron Law, rather than as the upstream's edit-and-update step.

Nothing else was taken. `style-guide.md` is five common-mistake bullets already covered by the templates and
by `writing-for-humans`, and the task taxonomy's other three entries map onto the existing BOOTSTRAP and
REFRESH modes.

**The upstream skill vendors three third-party documents into its `references/` directory, and the toolkit's
MIT licence does not cover them.** `references/art-of-readme.md` is hackergrrl's Art of README and keeps its
own licence line — **Creative Commons Attribution 2.0**, not MIT. `references/make-a-readme.md`
(makeareadme.com, Danny Guo) and `references/standard-readme-spec.md` (RichardLitt/standard-readme) each carry
a source link and no licence statement at all. Nothing from any of the three is used here, and nothing should
be lifted from them on the strength of the enclosing skill's licence. Recorded because the skill reads as
uniformly MIT and only one of those files says otherwise.

Two tells this repository's review record had taught to expect from this toolkit were absent: there is no
scored rubric anywhere in the skill, and its examples fabricate nothing — every template is bracketed
placeholders throughout, including its badge URLs.

## Upstream license

See [LICENSE.upstream](LICENSE.upstream) for the complete MIT license text.

## Divergence from upstream

On 2026-09-10 the Contributing and License rows of the section matrix, and the corresponding sections in the
OSS, personal, and generic templates, were reduced to one-line pointers rather than section bodies. Upstream
carries fuller sections. The change is permitted by the upstream MIT license and reflects a local decision
recorded in `docs/plans/skills/writing-readmes-draft.md`.
