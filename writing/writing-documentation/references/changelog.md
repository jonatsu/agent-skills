# Changelogs

Detail behind the change-note shape in `SKILL.md`, for a changelog maintained as a file in the project rather
than a one-off release announcement.

## Decide Whether One Is Warranted

A changelog earns its place when change history stops being recoverable from commit messages alone: when
readers are users rather than contributors, when releases are versioned and consumed by other projects, or
when upgrade decisions depend on knowing what changed between two versions.

A project whose commits are already structured and whose consumers read the repository directly does not need
one. Say so rather than adding a file that will go stale.

## Structure

Newest first, so the reader's most likely question is answered without scrolling. Each release carries a
version and a release date. An `Unreleased` section at the top collects merged changes that have not shipped,
which is what keeps the file current between releases rather than reconstructed at release time.

Group entries by the kind of change, using only the groups a release actually contains:

| Group        | Covers                                                        |
| ------------ | ------------------------------------------------------------- |
| `Added`      | New capabilities                                              |
| `Changed`    | Altered behavior of something that already existed            |
| `Deprecated` | Still working, scheduled for removal, with the replacement    |
| `Removed`    | Gone, with the version that deprecated it                     |
| `Fixed`      | Defects corrected                                             |
| `Security`   | Vulnerabilities addressed, so a reader can prioritize upgrade |

Where versions carry compatibility meaning, keep the grouping honest against that scheme: an entry under
`Changed` or `Removed` that breaks a documented interface belongs to a major release, and a reader who finds
one in a patch release has been misled about the upgrade's risk.

## Write the Entry for the Reader, Not the Commit

An entry states the user-visible effect. A commit subject states the work performed. They are rarely the same
sentence, and copying the second in place of the first is the dominant failure in a maintained changelog.

- Write one entry per user-visible change, not one per commit. Several commits delivering one capability are
  one entry.
- Lead with what the reader can now do, or must now do differently.
- Include the action where a change requires one: a configuration key to set, a call to migrate, a default that
  moved. A breaking change without its migration step is an incomplete entry.
- Link the issue or pull request for the reader who needs the full history, rather than reproducing it.
- Omit changes with no observable effect: internal refactoring, test-only work, and dependency bumps that alter
  nothing the reader can see. A changelog that records them buries the entries that matter.

## Worked Example

```markdown
# Changelog

## [Unreleased]

### Added

- Reports can be exported as CSV alongside PDF (#412).

## [2.1.0] - 2026-03-11

### Added

- Time-limited report download links, so support can share a report without forwarding the file (#387).

### Changed

- Report retention now defaults to 90 days, previously unlimited. Set `reports.retention` to `unlimited` to
  keep the old behavior; existing reports are not deleted on upgrade (#390).

### Deprecated

- `GET /reports/{id}/content` returns the same bytes but will be removed in 3.0. Use the download link from
  `GET /reports/{id}` instead (#387).

### Fixed

- Reports above 40 MB failed to render instead of returning an error the caller could act on (#401).

### Security

- Report download links were not invalidated when a user lost access to the owning tenant (#399).
```

The retention entry is the one to model. It names the new default, the old one, the key that restores it, and
the fact that the change is not retroactive — everything a reader needs to decide whether the upgrade is safe,
without opening the issue.
