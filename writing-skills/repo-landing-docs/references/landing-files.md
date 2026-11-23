# Landing Files Other Than the README

Each section gives the rules a file's template cannot carry, and the check that tells you the file is done. The
visitor question each file answers is in `SKILL.md`'s Choose the Files table.

## Contents

- [CONTRIBUTING.md](#contributingmd)
- [SECURITY.md](#securitymd)
- [CODE_OF_CONDUCT.md](#code_of_conductmd)
- [Issue and Pull Request Templates](#issue-and-pull-request-templates)
- [CHANGELOG.md](#changelogmd)
- [ROADMAP.md](#roadmapmd)
- [SUPPORT.md](#supportmd)
- [GOVERNANCE.md](#governancemd)
- [FUNDING.yml](#fundingyml)
- [LICENSE](#license)

## CONTRIBUTING.md

Write the project's real workflow, taken from the repository. Name the check command a contributor runs, read
from the task runner or CI. Then give the commit message convention, the branch and review process, and what gets
a change rejected. A generic workflow reads as boilerplate, and a contributor who follows it still fails review.
Require a sign-off or a contributor agreement only where the project already does. Leave maintainer procedures,
such as releasing, to other documents, since an outside contributor never runs them.

Done when an outsider could send an acceptable change by following this file alone.

## SECURITY.md

Name one private reporting channel that works today. That is GitHub's private vulnerability reporting, or an
address the maintainers read. Private vulnerability reporting is a repository setting that owners enable. List
enabling it as a step for the user rather than assuming it is on. Add a supported-versions table only for a
project with versioned releases. State a response window only where the maintainers commit to it. A missed promise
costs more trust than no promise.

Done when a reporter knows where to report, what to include, and what happens next, without opening a public
issue.

## CODE_OF_CONDUCT.md

For a public project, adopt a recognised code verbatim from its canonical source, and record its version. The
Contributor Covenant is the common choice. Its authority comes from the recognised text, so a paraphrase loses
it. Fill in the enforcement contact the code asks for. The bundled template is a short custom code for a small or
private space.

Done when the code names a real contact who is not the only person a report might concern, or the user has
accepted that limit.

## Issue and Pull Request Templates

The bundled files are Markdown templates. GitHub's YAML issue forms (`.github/ISSUE_TEMPLATE/<name>.yml`) are a
different format with no bundled template; write one only on request.

Ask only for what triage needs. Map each prompt to the decision it informs, such as reproducing a bug. Delete
prompts that inform no decision, because a long form drives reporters to skip it. An optional
`.github/ISSUE_TEMPLATE/config.yml` can turn off blank issues with `blank_issues_enabled: false`. Its
`contact_links` entries, each with `name`, `url`, and `about`, send support and security requests elsewhere.

Done when every prompt names a decision it informs.

## CHANGELOG.md

Choose the form by how the project ships, and keep an existing changelog's established style.

- **Versioned releases:** use `CHANGELOG.template.md`, in the Keep a Changelog 1.1.0 format. Read
  [changelog.md](changelog.md) before writing an entry; it holds when a changelog is warranted, its structure, the
  entry rules, and a worked example.
- **No releases,** such as a configuration repository: use `CHANGELOG.dated.template.md`, with one heading per
  date a change reached the main branch. Its reader is often the maintainer. Entries may be commit subjects
  verbatim when the repository already keeps them that way.

In both forms, keep the newest entry first and write dates as `YYYY-MM-DD`. List every breaking change with what
the reader should do about it.

Done when a reader coming from any listed version or date can find every change that affects them.

## ROADMAP.md

Make each item one outcome a user will be able to see, stated as what they can do. A task or a component is not an
item, because a visitor cannot tell whether it meets their need. Group items as Now, Next, and Later. Date an item
only when the maintainers commit to the date. Keep the Not Planned section, which answers the visitor whose request
was declined. Link the ledger that holds the detailed work, such as the TODO file or the issue tracker. When an
item ships, remove it here and record it in the changelog.

Done when each item names an outcome and the page points to where the detailed work lives.

## SUPPORT.md

List the help routes in the order they resolve a problem fastest. That order is built-in help, a diagnostic
command, the documentation, an issue search, then a person. Name the requests the project does not support, so
they go elsewhere first. Send security reports to `SECURITY.md`.

Done when each route in the file exists and works.

## GOVERNANCE.md

GitHub gives this file no special treatment; it is a convention. Describe how decisions are really made, not how
they ideally would be. Cover the roles, the decision process, the tie-break, the path to maintainer, and how the
document itself changes. A project with a single maintainer needs no file. One sentence in `CONTRIBUTING.md`
saying so replaces it.

Done when a contributor can tell who decides a disputed change and how.

## FUNDING.yml

The file lives only at `.github/FUNDING.yml` on the default branch, where it adds a sponsor button. Each external
platform takes one account. GitHub Sponsors takes one organization and up to four developers, and `custom` takes
up to four URLs. Quote a custom URL that contains a colon. List only accounts the maintainers control.

Done when every account or URL in the file belongs to the maintainers.

## LICENSE

The user chooses the licence; never pick one for them. Copy its canonical text unchanged, filling in only the
fields it marks, such as the year and the copyright holder. GitHub detects a licence by comparing the file with
known licence texts, so an edited text may go unrecognised. Keep the file at the root, where licence scanners
conventionally look. Give the README a one-line pointer naming the licence.

Done when the text matches the canonical source apart from its marked fields.
