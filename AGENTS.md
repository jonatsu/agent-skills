# AGENTS.md: agent-skills

Instructions for agents working in this repository; `CLAUDE.md` is a symlink to this file. The repository holds
skill packages and the checks behind `just check`, nothing that installs them. It stands alone: describe it on
its own terms, and name a repository that installs or consumes these skills only in `TODO.md` and other ledgers
that track work between the two.

Read the focused source before acting:

- `README.md` describes the layout and how the skills are used.
- `engineering/README.md` states the intended flow of the core engineering skills, from idea to verified work.
  Read it before changing a pipeline skill's handoff or scope.
- `archived/README.md` on the `archived` branch defines the archive procedure, and its "Review is deferred" rows
  record which reviews are still outstanding.
- `TODO.md` holds the skill backlog and unevaluated candidate sources. An entry leaves it once it is done,
  handled elsewhere, or stale, after anything a later reader needs has moved to its durable home.

## Commands

```bash
just check                     # history secrets scan, every hook, both test suites; run before calling work done
just skill-check <skill-dir>   # both validators over one skill
uv run --frozen skill-checks --help   # each single check over the whole tree, such as spec or rust-examples
```

**Running only one validator is the mistake the pair exists to prevent.** The specification validator passes a
file that breaks every repository policy, and the policy validator does not check frontmatter shape at all.
Report them separately; never describe one as covering the other. `just skill-check` runs both even when the
first fails.

## This Repository Is Public

- Never commit a secret, a customer or client name or detail, a personal path, an email address, or an internal
  host, in a file or a commit message. Hooks catch secrets, your home directory path, and email addresses
  outside the noreply and reserved example domains; names, client details, and hosts are your responsibility,
  as are commit messages.
  Use reserved example values (`example.com`, `/home/user`) in a skill's examples.
- Material drawn from the author's private or work projects can carry their vocabulary without their name:
  project, product, host, layer, machine, or configuration names, and paths into them. Before committing work
  that drew on such a project, ask the user which projects it touched, unless your agent memory already records
  them. Derive each project's terms from its own repository, and keep the terms and their sources only in your
  agent memory, never in this repository or a commit message. Scan the change, any untracked drafts, and
  `git log --all -S` for each term, with a positive control that proves the scan can match. When a match or a
  doubt remains, ask the user before committing.
- Commit as the GitHub noreply address in `checks/skill_checks/identity.py`; the `commit-identity` hook fails
  any other. Pushing publishes, so push only when the user asks.
- Commits use Conventional Commits, `type(scope): subject`, with the scope naming the skill or tool changed.

## Placing a Skill

- **By coupling.** Agent-agnostic skills go in a domain at the root. A skill that works with only one agent,
  because it is about that agent's own files or features, goes in a directory named for that agent. No skill
  needs one yet.
- **Then by subject.** A skill that fits two domains goes where a reader would look first. **A skill name must
  stay unique across every group**; `just check` fails on a duplicate, because agents receive every skill flat.
- **Never by how it is loaded.** Whether an agent lists a skill in every session or loads it on demand is the
  installer's choice, made by skill name; no directory here encodes it.
- **A new group, or emptying one, changes what an installer receives.** A Kasetto entry names one group as its
  `sub-dir` and finds skills exactly one level below it, so a skill moved into a group no entry names stops
  reaching that installer. Say so in the commit body.

## Writing and Reviewing Skills

**Always:**

- Use `skill-forge` and `writing-for-agents` when drafting or making any change to a skill, before the draft is
  shown, and `writing-skill-descriptions` whenever a description is written or changed.
- Use `skill-forge`'s review mode for every skill review. It governs assessment and evidence; its authoring
  mode governs the shape of a proposed repair and any separately authorized edit.
- Keep every skill self-contained: no link, path or script reference may leave its folder. `just check` fails a
  Markdown link or a script path that does, but it matches patterns line by line; check any other reference
  yourself. A script in one skill may be run by this repository's checks, never by another skill.
- Keep every skill complete for its own job. When two skills both need a rule, each carries its own version,
  sized to that job, because an agent often loads only one of them. Point to a sibling skill for extra depth,
  never for correctness. When you change a shared rule, update every skill that carries it.
- Label every Rust code block in a skill with what it must prove: `rust` builds and passes clippy, `rust,run`
  also runs, and `rust,compile_fail,E0277` fails with that error. For an error without a code, write
  `rust,compile_fail` and make the block's first line `// error: <the compiler's message>`. Label a `Cargo.toml` fragment
  `toml,manifest` and a `clippy.toml` one `toml,clippy-config`. Write a snippet that should not be checked as
  `text`; an unlabelled `toml` block in a skill with Rust examples fails the check. Examples may use only the
  dependencies in `checks/rust_examples/Cargo.toml`.
- Keep a skill's `description` one inline YAML scalar. Kasetto records a folded one as its marker character.
- Write `ATTRIBUTIONS.md` to the scheme in `skill-forge`'s `references/provenance.md`: what the skill is based
  on, under which license, and what each source gave it, in first-party and third-party sections. It is never a
  work ledger; repairs, reviews, and investigations belong in Git history.
- Keep a third-party source entry permanently, restated in the past tense once the material is replaced. The
  revisions that carried the material stay in history, so deleting the entry hides a relationship a later
  reader still needs. The author's own absorbed or deleted skills get no entry; no reader can inspect them.
- Ask what a user would have to say for a proposed skill to load, before writing it. Guidance for a moment
  nobody verbalizes, such as whenever someone writes code, belongs in an agent's rules instead; a skill for
  such a moment does not activate, and no wording repairs it.
- Keep a skill's licence: an adapted skill carries its upstream licence in the `license` field plus
  `ATTRIBUTIONS.md`. Where an upstream licence blocks the use needed, write an independent replacement rather
  than a relicensed adaptation. Relicensing needs the user's approval.

**Never:**

- Treat a review request as authorization to change the skill. Report first unless the user also requested
  implementation.
- Spend time validating or repairing an archived skill marked deferred, unless its review is explicitly
  resumed.

## Writing Documentation

A durable document describes its subject as it stands. These rules come from
`docs/findings/2026-10-11-documentation-flaw-patterns.md`, which holds the examples.

- Record the current state only. Repairs, reviews, investigations, and the dates they happened belong in Git
  history and the repository's ledgers, as do lists of what was checked and found irrelevant.
- Write a `docs/evaluations/` record only for evidence a later decision will cite and that costs real work to
  reproduce: model runs, usage counts, or a review of one of our own skills whose findings stay open. For a
  third-party source, put each idea worth taking in a `TODO.md` entry that names the source by URL and commit,
  and record what a skill takes in its `ATTRIBUTIONS.md`. A source declined with nothing taken gets one line,
  with its reason, under "Declined Sources" in `docs/evaluations/README.md`.
- Pin material with identifiers that survive regeneration: a release, tag, or commit, the version the material
  embeds, or the date it carries. Keep the precision the evidence supports; without a recorded pin, give the read
  date rather than deriving one.
- Cite only what a reader of the published document can inspect.
- State each fact once. Keep a rule in the repository's rules rather than in every file it governs, and never
  restate a header or a structured field in prose.
- Lead with the fact a reader scans for, and group content by what it is, never by when or why it was gathered.
- Say what something is or supplied. Summarize to the main points rather than inventorying every item, name the
  kind of a change rather than listing each one, and add an exclusion only where a reader would otherwise assume
  the opposite.
- Give each section a reader question to answer, and state facts without arguing the document's own legitimacy.
- Point to another document with one neutral sentence.
- Use a dash only where grammar requires one; a comma, colon, semicolon, or parentheses carries most clause
  relationships.

## Archive Without Losing Structure

- Keep every package file byte-identical to its last version on `main`: `SKILL.md`, references, scripts,
  attribution and upstream licence files.
- Archived skills live on the `archived` branch, never on `main`. Copy the package there as `archived/<skill>/`,
  then remove it from `main`. When archiving an entire domain, keep it as `archived/<domain>/<skill>/` rather
  than flattening its packages.
- Add `ARCHIVED.md` inside each moved package and update `archived/README.md` on that branch.

## Git Safety in `git-commits-and-recovery`

The skill deliberately stays model-invokable: `disable-model-invocation: true` would withhold its guidance, not
prevent an agent from running Git commands. Safety relies on the agents' always-loaded staging rule and on
deterministic command guards, not on the skill's confirmation gates.
