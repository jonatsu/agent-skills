# Provenance and Licensing

These are conservative authoring policies; determine legal obligations from the exact source license and the
relationship to it.

Use the target repository's license for original work. Use the upstream license for derived work unless its
terms permit and the author deliberately applies a compatible alternative. Verify licenses from the license
text at a pinned upstream revision. Repository metadata alone is insufficient evidence.

## Classify Every Source

Classify each source read during authoring by what changed after reading it:

| Relationship                                   | Required record                                     |
| ---------------------------------------------- | --------------------------------------------------- |
| Fact lookup, such as `--help` or a manual page | Cite the source near the affected claim when useful |
| Subject documentation the skill is built on    | A first-party entry in `ATTRIBUTIONS.md`            |
| Idea influenced independently written content  | A third-party entry in `ATTRIBUTIONS.md`            |
| Copied, adapted, or translated material        | An entry, plus `LICENSE.upstream`                   |
| Vendored code or assets                        | An entry, plus `LICENSE.upstream`                   |

A **first-party** source is published by the project the skill is about: its manuals, documentation, code, and
material built from them. Every other source is **third-party**: training material, books, other projects, and
other people's skills. Decide by impact whether first-party material earns an entry. Documentation or source code
the skill's guidance is extensively built on does, even when it was read to verify behavior; a single fact checked
against `--help` or a manual page does not.

Reading a third-party source creates an obligation when it changes the skill's guidance, workflow, structure,
examples, terminology, or failure modes, even when every sentence and example is written from scratch. Record
it also when its license is restrictive or proprietary and it served only as inspiration, so the entry can
state that nothing was copied. This is a conservative traceability policy. Do not present it as a universal
legal rule.

For copied, adapted, translated, or vendored material, determine the source license's actual obligations. This
workflow also requires the package to ship:

- `LICENSE.upstream` containing the upstream license text verbatim; and
- `NOTICE.upstream` when the upstream project supplies one or its license requires preservation.

When a package carries material from more than one upstream, give each further license its own file named for
its source, such as `LICENSE.upstream-<source>`, and name the file in that source's entry, so every copyright
notice keeps traveling beside the material it covers.

Check the upstream license before adapting material. When its terms do not permit the intended use or
redistribution, write an independent replacement from domain knowledge and do not copy the restricted
expression. If a source or its license cannot be verified, stop before making an authoritative attribution
claim and report what is missing.

## Write ATTRIBUTIONS.md

The file answers one question for a reader of the published package: what is this skill based on, under which
license, and what did each source give it? It describes the sources as they stand. Git history records how the
skill changed, so the file holds no work record of any kind.

Start from `assets/ATTRIBUTIONS.template.md`, and keep its shape:

- `# Attributions`, then the header bullets `Author` and `License`. A derived package adds one or two sentences
  on what its license requires, such as the Apache-2.0 section 4 statement that the files were modified and
  the instruction to keep `LICENSE.upstream` with the skill.
- `## First-party Sources` and `## Third-party Sources`, each holding one `###` entry per source. Omit a
  section that has no entries. Group sources by kind only, never by when or why they were read.
- `## Upstream License Notice`, only when a license requires its notice text to travel with the material.

Each entry has a heading in the form `### <Author or publisher>: <work>`, three bullets, and one to three sentences:

- `Source`: the URL, plus the path within the project when the source is part of one.
- `License`: the SPDX identifier or expression in backticks, such as `` `GPL-2.0-or-later` `` or
  `` `MIT AND CC-BY-SA-4.0` ``. A license with no SPDX identifier takes a `LicenseRef-` name, such as
  `` `LicenseRef-Proprietary` ``, and the prose explains its terms in one sentence.
- `Version`: the release, tag, or commit for a Git repository, a release archive, or any source where one of
  those is meaningful. That includes a PDF that embeds the tag or revision it was generated from. Otherwise use
  the documented software version, the date the material carries, or for a book its edition and publication
  date. When nothing pins the source, give the date it was read.

The sentences say what the source supplied, such as ideas, structure, examples, or failure cases, and whether
any prose, code, or assets were copied or adapted. Adapted material names the kind of adaptation in a clause at
most, never a list of the individual changes. A source whose material the skill no longer carries keeps its
entry, restated in the past tense: "Formerly adapted …; the current skill carries none of it." When a license
kept prose from being copied, say so briefly: "No prose was copied due to the content license." The revisions
that carried the material remain in history, and the entry keeps that relationship visible.

The file never contains:

- narration of repairs, reviews, investigations, or sessions, and dates of when work happened;
- correspondence tables, change lists, or per-file provenance tables;
- hashes of files that are regenerated, such as PDF checksums;
- sources a reader cannot inspect, such as the author's own deleted or absorbed skills;
- sources that were checked and found unrelated, or claims about how thorough a check was;
- restatements of the header or of an entry's `License` bullet, such as explaining a source license against the
  package's own license;
- lists of what was not taken from a source; and
- policy text, such as why entries are kept, which belongs in the repository's rules.

Preserve existing provenance artifacts and license files during updates.
