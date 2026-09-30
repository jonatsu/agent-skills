# Truth Audit

Find where a repository's documentation no longer tells the truth, or will soon stop, and hand the user a
menu of verified fixes to choose from. The audit covers any natural-language artifact that teaches a reader
what is true: READMEs, guides, runbooks, plans, decision records, notes, and agent instruction files. Code,
configuration, tests, and live behavior are the evidence, not the target; code comments and docstrings are left
to a code review.

A README accuracy check is this audit with a one-file surface; run the same steps. It asks whether the README
is still true, not whether it reads well; the second question belongs to a README-writing review, and a
thorough review asks both.

The audit is read-only. Nothing changes until the user selects items from the menu.

## Contents

- 1. Learn the repository's conventions
- 2. Map the claims
- 3. Verify before reporting
- 4. Classify the problems
- 5. Rank
- 6. Report the action menu
- 7. Execute the selected items

## 1. Learn the Repository's Conventions

Read the floor file, the documentation index, and any style or contributing guide first. Learn where each kind
of knowledge is filed, how documents are named and dated, and how a finished plan or an archived note is
marked. Every move, archival, or promotion you later propose lands in the home the repository defines, next to
an existing sibling of the same kind. Where the repository has no convention for a case, say so, and propose
one consistent with its structure.

Decide each document's freshness expectation from its genre before judging it. A dated investigation or a
frozen decision record is supposed to describe the past; it is stale only when it reads as current guidance.

## 2. Map the Claims

List the durable claims in the surface, and for each one the source that owns it:

- behavior of the product or system;
- setup, usage, operation, deployment, and recovery procedures;
- meanings of configuration, data, and API fields;
- permission, privacy, and safety boundaries;
- names, lifecycle, ownership, and deprecation state; and
- decisions, their rationale, and migration status.

A claim with no clear owner, with several competing statements, or living only in a fragile place such as a
copied example, an old plan, or a commit message, is already a finding.

## 3. Verify Before Reporting

Check each checkable claim against the source that owns it:

- commands against the task runner, package scripts, build files, and CI workflows;
- paths, file names, headings, and anchors against the tree;
- flags, environment variables, and defaults against the code or the tool's `--help`;
- capabilities and supported versions against code and dependency manifests;
- links against their targets; and
- present-tense operational claims against live behavior, when a safe probe exists.

Search for every reference to a document before proposing to move, merge, rename, or archive it. A claim you
cannot verify with the evidence available becomes an investigation item, labeled as such, never a finding.

## 4. Classify the Problems

Name each finding by its class, and fix the root rather than each symptom: three stale copies of one setting
usually need one owner and two pointers, not three edits.

- **Stale claim:** a command, path, link, name, or behavior that no longer matches its source.
- **Duplicated or unowned fact:** the same fact stated in several places, conflicting explanations, or a fact
  with no owner, including generated output edited by hand.
- **Mirror of a volatile fact:** a list of values, defaults, flags, routes, versions, or command output copied
  from a source a reader can look up. It adds an edit site to every change of the source. Replace it with a
  pointer plus whatever meaning or gotcha the source lacks. A self-referential count, such as "the three steps
  below", is the smallest case: delete the number and let the list speak.
- **Misleading status:** a finished plan that reads as active, an investigation that reads as a contract, or a
  draft that cannot be told from current guidance at first glance.
- **Wrong home:** a fact far from the file someone edits when the fact changes; a concept used by two areas
  but documented inside one of them; a lasting rule trapped in a dated investigation.
- **No update path:** nothing tells whoever changes the underlying truth to change this document. Propose a
  change-time note beside the source, such as "update the setup guide when changing this file", rather than a
  one-off correction.
- **Knowledge to promote:** the same question answered more than once in sessions, reviews, or chat; a
  commit message that explains the system rather than the change; a procedure improvised twice; a debug note
  whose conclusion is a lasting rule. Promote the rule and point back to the narrative.
- **Knowledge to retire:** a document nothing references, unchanged while its subject changed. Verify it once,
  then archive or delete it by the repository's convention.
- **Generic explanation:** a passage teaching a well-known tool or framework's standard behavior. The test: would
  the sentence be true in any repository using that tool? If yes, name the mechanism and keep only what differs
  here.
- **Missing check:** a runbook step without an observable success condition, or a procedure with no rollback.

## 5. Rank

Order findings by impact on the reader, confidence of the evidence, and cost of the fix, putting verified,
high-impact, cheap fixes first. Weight by how often the text is loaded: a sentence in an always-loaded
instruction file costs every session, while a page read on demand costs only its readers, so the same cut is
worth more on the floor.

## 6. Report the Action Menu

Open with one or two sentences on the surface covered and what was found. Then list each actionable item under
a letter, in rank order. Letters continue `A` to `Z`, then `AA`, and never change meaning within the
conversation, so the user can answer with them. Write each item as:

```markdown
B. Mark the finished auth migration plan as done

- Evidence: `docs/plans/auth-migration.md` reads as active; the deploy config and `docs/auth.md` show the
  migration completed.
- Why it matters: agents treat its open steps as pending work.
- Change: archive it by the repository's plan convention, and move its two open questions to the backlog.
- Done when: the plan sits in the archive, and the backlog holds both questions.
```

Label investigation items as such in the title, and state what evidence would settle each. Record the audit in
the repository's evaluations genre when it has one.

Then ask which letters to execute. Accept any compact answer, such as `A C`, `all except D`, or `investigate B first`.

## 7. Execute the Selected Items

Restate the selected letters in one sentence. Re-read each affected document before editing, because the tree
may have changed since the audit. Change only what the selected items name, and leave unrelated work in the
tree as it is. When re-reading shows an item no longer holds, stop that item and report why.

Before correcting a stale claim, decide whether the document or the implementation states the intended
behavior; a document can be right and the code wrong. Update a "last reviewed" or "verified" date only after
checking the content that date vouches for.

Run each item's done check, and report it as met or not. Items the user did not select stay in the report as
open.
