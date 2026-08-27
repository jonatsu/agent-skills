# Named failure patterns

A diagnosis catalogue, not a checklist. Load it AFTER scoring a dimension low, to name what
is wrong and state the repair. Reading it first biases the score toward the patterns it
happens to list.

Each entry names the dimension it hits, so a finding lands on one dimension rather than being
counted twice.

- **The Tutorial** — explains basics the model knows. Fix: delete; keep only expert decisions
  and trade-offs. Hits D1.
- **The Dump** — 800-line SKILL.md, no layering. Fix: routing and decision trees in the body,
  detail in `references/`. Hits D5.
- **The Orphan references** — reference files with no load trigger. Fix: add explicit "read
  this when…" and "do NOT load…". Hits D5.
- **The Checkbox procedure** — mechanical Step 1/2/3 for what the model already does. Fix:
  convert to "before X, ask yourself…". Hits D2. One question decides it: does the task have
  real ordering and real prerequisites — steps that fail or mislead out of sequence? If yes
  the checklist is earned; if no it is a no-op, however tidy it looks.
- **The Transcription** — a CLI surface, parameter schema, config-key list or inventory count
  copied out of a tool that reports it live. Fix: replace with a pointer to the live source,
  keeping only the residue that source does not carry. Hits D1. Confirm the source is correct
  and reachable before cutting.
- **The Vague warning** — "be careful", "consider edge cases". Fix: specific NEVER list with
  non-obvious reasons. Hits D3.
- **The Broken Own Rule** — the package states a rule and then breaks it in its own examples,
  templates, commands, or conduct: a rubric that penalizes a pattern its templates
  demonstrate, a countable claim ("each of these carries a warning") falsified by the package,
  a portability rule contradicted by the line beneath it. Fix: check every rule against the
  instances it governs, not against other rules. Hits whichever dimension the broken instance
  sits in. This is the most-missed defect class, because both halves are individually correct
  and only their relationship is wrong.
- **The Invisible skill** — great body, vague description, never fires. Fix: WHAT + WHEN +
  keywords, and a negative trigger. Hits D4.
- **The Freedom mismatch** — rigid scripts for creative work, or vague guidance for fragile
  ops. Fix: match freedom to fragility. Hits D6.
- **The Unchecked skill** — asserts how tools, formats or systems behave and cites nothing:
  no source, no date, no adversary, no recount. Every claim rests on the author having been
  confident. Fix: trace each empirical claim to a primary source and stamp it with the date
  read; have an independent reader try to refute the load-bearing ones; recount every
  countable claim. Executed evaluations are better still, where the skill can afford them.
  Hits D7.
- **The Local skill** — works only on the machine it was written on: an assumed tool, a
  hardcoded install path, a `~`-rooted path to its own files. Fix: `command -v` probes,
  relative paths, accept alternatives. Hits D8, capped.
- **The Borrowed Runner** — a portable skill invoking another repository's task recipe
  (`just check`, `npm run lint`, `make test`), often with a `command -v` probe for the runner
  binary presented as verification. Fix: discover the repo's own entry point at run time in a
  stated detection order, and skip with a report when none is found. Hits D8, capped. Exempt
  when the skill declares `metadata.scope: repo-local`.
- **The Undeclared Local** — a skill that reads as repo-specific, names one repository's
  runners or paths, and declares no scope. Fix: declare `metadata.scope: repo-local` and name
  the repository, or remove the bindings. Hits D8, capped — an absent declaration means
  portable, so this is a defect and not a contract. Do NOT let the obvious usefulness of the
  bindings argue you into reading intent that the frontmatter does not state.
- **The Subject's Coattails** — a tool-subject skill that binds legitimately to its own
  subject and then assumes a second tool, a project-local runner, or a config path on the same
  authority. Fix: probe everything that is not the subject. Hits D8, capped.
