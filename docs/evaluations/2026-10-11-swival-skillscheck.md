# Evaluation: swival/skillscheck as a Replacement for the Repository's Skill Checks

Date: 2026-10-11. Judged as a third-party replacement for the skill checks behind `just check`, to reduce the
repository's own checking code. The tool ran against this tree and against probe skills built for the gaps
below.

## Verdict

Do not adopt. Skillscheck covers the Agent Skills specification basics, but most of this repository's checking
code enforces local rules it has no equivalent for, so adopting it would retire about 20 lines. It cannot gate
anything here: without `--strict` no warning fails a run, and with `--strict` the asset templates' intentional
links fail it, with no exclude or suppression mechanism to exempt them.

## Source

- Repository: <https://github.com/swival/skillscheck>, commit `742d3733dfc8dc11a40b5f23f7993cf0cae33124`,
  version 0.9.7
- License: MIT
- Maintenance: one author, Frank Denis, 29 commits between 2026-03-11 and 2026-08-20; 7 stars, no open issues;
  classified as beta. Its own 443 tests pass.

## What It Checks

Skillscheck is a Python CLI (`uvx skillscheck <dir>`), also published as a VS Code extension. It needs no
configuration and has four check categories:

- **Specification:** frontmatter syntax, the `name` rules and directory match, description length, optional and
  unknown fields, `allowed-tools`, and duplicate names or descriptions across the skills of one run.
- **Quality:** description heuristics (a missing "use when", keyword stuffing), leaked secrets, binary and
  oversized files, extraneous README or LICENSE files at the skill root, files `SKILL.md` never links to,
  broken local links and anchors, unclosed fences, and repeated bold labels.
- **Progressive disclosure:** reference-file token budgets and reference nesting depth.
- **Agent compatibility:** `plugin.json`, `marketplace.json`, `gemini-extension.json`, `.cursor/`, `.roo/`,
  `.github/skills/`, and Codex `agents/openai.yaml` sidecars. None apply to this repository.

The CLI options are `--agents`, `--check` (by category), `--fix`, `--format json`, and `--strict`. There is no
configuration file, path exclusion, or per-finding suppression.

## Coverage of This Repository's Checks

| Hook                                                                                                                              | Coverage                                                                                                                                                          |
| --------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `skill-spec` (vendored `skills-ref`)                                                                                              | Mostly covered: the same frontmatter and name rules.                                                                                                              |
| `skill-names` (unique across every group)                                                                                         | Covered only by a whole-tree run, which also scans `archived/` and the test fixtures; nothing excludes them.                                                      |
| `skill-references` (nothing leaves the package)                                                                                   | Partial. An escaping link in a reference file is flagged, but a `SKILL.md` link to an existing file outside the package passes, and script paths are not checked. |
| `skill-descriptions` (one inline scalar, character budget)                                                                        | Length only. A folded `>-` description, which Kasetto records as its marker character, passes.                                                                    |
| `skill-policy` (`quick_validate`: author, license field, scope, scaffold placeholders, `LICENSE.upstream` with `ATTRIBUTIONS.md`) | Not covered.                                                                                                                                                      |
| `skill-attributions` (the provenance scheme)                                                                                      | Not covered.                                                                                                                                                      |
| `commit-identity`, `pushed-identity`                                                                                              | Outside its purpose.                                                                                                                                              |

The two partial rows were confirmed with probe skills: a folded description and a `SKILL.md` link to an existing
sibling package both produced no finding.

## Results on This Tree

Run per skill group over 53 skills: 0 errors, 18 warnings, and 82 informational findings.

- **Broken links, 9 warnings.** Eight are links in asset templates, such as `LICENSE` and `docs/README.md`, whose
  targets exist only in the repository a template is copied into. The ninth is an emoji anchor in an archived
  skill.
- **No "use when", 9 warnings.** A style heuristic; `writing-skill-descriptions` treats that phrasing as optional.
- **Orphans (29) and reference nesting (36), informational.** Mostly noise for this layout: a reference reached
  through another reference, such as `skill-forge`'s `references/provenance.md`, counts as an orphan, and the
  nesting check reports deliberate cross-reference links.

## What It Would Add

The one capability this repository lacks is checking that links between a skill's own files resolve, which is
the open `TODO.md` item "Broken Links Between a Skill's Own Files". Skillscheck cannot gate that here because of
the template false positives, so the planned existence check in `outside_references.py` remains the cheaper fix.

## Reconsider When

Skillscheck gains path exclusions or per-finding suppression, and a check for description scalar style or for
references that leave the package from `SKILL.md` and scripts.
