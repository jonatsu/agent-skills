# Maintainability Review

Load this when reviewing a change for maintainability: whether the next engineer can read and change it without
the author there to explain it. Correctness belongs to `change-review`, and design decay across modules to
`brooks-review`.

## Standards, in Order of Authority

1. The project's instruction files and the conventions the surrounding code already follows. A default in this
   skill never overrides them.
2. The skill for the file's language, such as `python-style`, `bash-shell`, or `rust-style`, when one is
   available. Load it before reviewing that file; its rule wins over a default here.
3. This skill's body and references. Read the matching reference before filing a finding it governs.

## Method

1. Set the scope: what the user names, or else the working tree, from `git status`, `git diff`, and
   `git diff --cached`, with each untracked file read in full. Skip generated code, lock files, and vendored
   sources.
2. Read each changed hunk with enough surrounding code to see the conventions it should follow, and check the
   code the change added or rewrote against every standard.
3. Before calling code duplicated or dead, confirm it with a text search or the language server's references.

Review test files to the same standards, relaxed only where test clarity wins: a short setup repeated inline is
not duplication, and a literal expected value is the specification, not a magic number. Judge the change, not the
whole file: a problem in untouched code is a finding only when the change makes it worse or copies it.

Report a finding only when following the standard would clearly help the next reader or the next change. A
difference from a default is not a finding.

The review is done when every changed hunk has been checked against every standard and the language skill, and
each finding names the file, the line, and the standard it breaks.

## Report

1. **Verdict**: `Ready`, `Ready after changes`, or `Not ready`, then one sentence saying why. Any open Must fix
   finding rules out `Ready`; use `Not ready` when the change needs restructuring rather than local fixes.
2. **Scope**: the range or files reviewed, and the language skills loaded.
3. **Findings**, most costly first, each tagged `F1`, `F2`, and so on. Give each its tier, the file and line, the
   standard it breaks (a project rule, a language skill rule, or a section of this skill), the concrete
   maintenance cost, and the specific fix.
   - **Must fix**: a broken project rule, or a clear threshold crossed with real cost, such as a 120-line function
     doing four jobs, the same rule defined twice, or a swallowed error.
   - **Should fix**: a real cost that may wait for a recorded follow-up, such as one concept under two names.
   - **Consider**: a clearer name, an extraction, or a comment to delete. Report at most five, and say how many you
     left out.
4. **Unverified**: suspected duplication or dead code you could not confirm, with the search that would settle it.
5. **Next checks**: the reviews to run next, such as `change-review` for correctness.
6. **What holds**, only when something specific should survive a revision: at most two sentences, with the file
   and line.

A clean change gets the verdict, the scope, and the next checks.
