# Evaluation: Does `repo-landing-docs` Change Landing Documents Other Than the README?

Date: 2026-11-23. The skill grew from a README skill into one that owns every landing document, and its review
found that only the README had ever been evaluated. This evaluation asked whether the skill changes what an agent
writes for the other files, and for a refresh of a whole repository.

## Verdict

The skill made a difference where a control fills gaps with invention or with work nobody asked for. It made no
difference where the task was already easy.

- **ROADMAP.md: clear gain.** The control listed internal work (a module split, a Windows CI job) as roadmap
  items. It added sections nobody requested and rewrote the TODO ledger, which the task did not cover. The skill
  arm kept only outcomes a user can see, put the declined GUI under Not Planned, added no dates, and linked the
  ledger instead of copying it.
- **SECURITY.md: clear gain.** The control invented response times (7, 30, and 90 days), a scope section, and an
  advisory process. The skill arm left out the response window because no source committed to one. It listed
  enabling private vulnerability reporting as a step for the maintainer instead of assuming it was on.
- **Refresh: moderate gain.** Both arms proposed a file set before writing and found the missing `LICENSE`. The
  control's plan listed a fix for a crash that never shipped in a release. It also pointed `SECURITY.md` at
  GitHub's private reporting button without checking that the setting was enabled. The skill arm gave a reason
  for each file it left out (GOVERNANCE, SUPPORT, ROADMAP, FUNDING). It diagnosed the README against the five
  reader questions and refused to invent example output.
- **CONTRIBUTING.md: small gain.** Both arms used the real `just check` command and the commit convention. The
  control added a release procedure and an inbound licence clause the project does not require. The skill arm
  left both out, as its rules say.
- **CHANGELOG.md: no difference.** Both arms omitted the refactor, test, and dependency commits, dropped the fix
  for the unshipped crash, and flagged the breaking change. The skill arm also left the template's commented link
  definition, with its placeholder, in the delivered file.

## Method

Claude Code `general-purpose` subagents on Sonnet ran each task once per arm, ten runs in all, in fresh contexts.
The fixture was a synthetic Python CLI repository, with a README of two sections, an `AGENTS.md` stating the
commit convention and the single maintainer, a `justfile` check recipe, and a `docs/TODO.md` mixing user requests
with internal tasks. After a `v1.3.0` tag, its history held a refactor, a new option, a fix for a crash in that
new option, a breaking output change, a real bug fix, a test, and a dependency bump. Every run treated the fixture
as read-only and wrote its result to a separate file. The skill arm was told to read `SKILL.md` at agent-skills
`80c8c31` and the references it names. No arm could use the Skill tool, so neither could load a deployed skill.

| Task                                       | Skill arm                                | Control arm                                         |
| ------------------------------------------ | ---------------------------------------- | --------------------------------------------------- |
| SECURITY.md with a given contact address   | no invented commitments                  | invented response times, scope, and advisories      |
| CONTRIBUTING.md                            | real workflow, no release procedure      | real workflow, plus releases and a licence clause   |
| CHANGELOG.md since the tag                 | correct; template comment left in        | correct                                             |
| ROADMAP.md from the TODO file              | user outcomes only, ledger linked        | internal tasks included, ledger rewritten           |
| Refresh plan for a public, open repository | reasoned file set, five reader questions | sound file set, unshipped fix and unchecked setting |

## Limits

Each task ran once per arm on one model, so a single difference may be noise. The fixture's code was a stub, so
no arm could run the tool or check its options. Because the skill arm could not load `writing-for-humans`, which
the skill requires, its prose quality was not graded. Routing among `repo-landing-docs`, `repo-setup`, and
`repo-audit` was not measured, because the renamed skills were not yet deployed.
