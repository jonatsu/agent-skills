# README by Audience

A README answers the questions its reader will actually have, and different readers need different sections.
Classify the repo (this mirrors the BOOTSTRAP audience question in Step 2), then pick the matching template
asset and include only the sections marked for that type.

## Project types

- **OSS** — public projects for contributors and users worldwide. Reader needs install, usage, contributing,
  license. Template: `assets/README.oss.template.md`.
- **Personal** — side projects, portfolio pieces, experiments. Reader is future-you and portfolio viewers.
  Template: `assets/README.personal.template.md`.
- **Internal** — team codebases, services, internal tools. Reader is a new teammate needing setup,
  architecture, and operational runbooks. Template: `assets/README.internal.template.md`.
- **Config** — XDG config dirs, dotfiles, script folders. Reader is future-you, probably confused, asking
  "what is this?". Template: `assets/README.config.template.md`.

When the type is unclear, ask. Default to the generic `assets/README.template.md` rather than assuming OSS.

## Section matrix

| Section            | OSS      | Personal | Internal | Config |
| ------------------ | -------- | -------- | -------- | ------ |
| Name / Description | Yes      | Yes      | Yes      | Yes    |
| Badges             | Yes      | Optional | No       | No     |
| Installation       | Yes      | Yes      | Yes      | No     |
| Usage / Examples   | Yes      | Yes      | Yes      | Brief  |
| What's here        | No       | No       | No       | Yes    |
| How to extend      | No       | No       | Optional | Yes    |
| Contributing       | Yes      | Optional | Yes      | No     |
| License            | Yes      | Optional | No       | No     |
| Architecture       | Optional | No       | Yes      | No     |
| Gotchas / Notes    | Optional | Optional | Yes      | Yes    |
| Last reviewed      | No       | No       | Optional | Yes    |

For prose quality inside whichever template you pick — skimmable structure, active voice, cut filler — apply
the `writing-for-humans` skill if it is available.

## Provenance

The project-type taxonomy, section matrix, and audience templates are adapted (MIT) from
`crafting-effective-readmes` in softaworks/agent-toolkit. See `ATTRIBUTIONS.md` for the full note.
