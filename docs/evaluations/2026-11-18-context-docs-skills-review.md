# Review: agents-context-docs and context-architecture

Date: 2026-11-18. A skill-forge review of `agents/agents-context-docs` and `agents/context-architecture` at
`0f312e1`, weighed against how Claude Code and Codex agents actually reach repository documents. The two skills
share one boundary: `agents-context-docs` owns the instruction file (the floor), and `context-architecture` owns
the documents the floor routes to.

## Verdict

Both skills are `not ready`. Their structure is valid and much of their guidance holds, but both treat a route in
the floor as the way agents reach documents, and that is not how the user's most-used client behaves. The loading
reference is also stale for Claude Code and silent on Codex, the user's two main clients.

Both validators pass for both packages: the Agent Skills specification validator (`skills-ref validate`) and the
repository policy validator (`quick_validate.py`), each `1 checked, 0 failed`.

## How Agents Reach Documents

Transcript mining measured, for each document an agent read, the last place its path appeared before the read.
The unit is the first read of each in-repository Markdown document per session, excluding the instruction file,
skill packages, and scratch space. Reads whose path the user or a subagent brief supplied are counted apart. The
sources are Claude Code transcripts from 15 of the author's personal repositories over the 45 days to
2026-11-18, and all of the author's Codex transcripts. Most Codex use is in work and restricted repositories,
which the Claude Code sample excludes, so the two columns cover different repositories. Codex reads files through
shell commands, so a Codex read is a command that prints a named document. A search counts as discovery only when
its own input did not already name the document.

| Last source before the read            | Claude Code (645 reads) | Codex (885 reads) |
| -------------------------------------- | ----------------------- | ----------------- |
| Search result (Grep, Glob, `rg`, `fd`) | 40%                     | 28%               |
| Route from another document            | 20%                     | 38%               |
| Route straight from the floor          | 6%                      | 9%                |
| Other tool output, git, summaries      | 30%                     | 14%               |
| No earlier mention                     | 4%                      | 12%               |

Where the floor itself listed the document, Claude Code read it straight from the floor in 21% of cases (36 of
175), arrived through another document in 17%, and reached it through a search in 38%. Codex, over 256 such
reads, went straight from the floor in 30%, through another document in 32%, and through a search in 30%. Codex
follows links between documents far more than Claude Code does; both use the floor's own routes for a minority
of reads. The measurements carry error: the floor compared is today's version, and a search that follows a route
may only confirm it.

Anthropic describes the Claude Code behavior as its design: "CLAUDE.md files are naively dropped into context up
front, while primitives like glob and grep allow it to navigate its environment and retrieve files just-in-time"
([Effective context engineering for AI agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)).
The user's global agent rules also steer toward search tools and name no rule for following the floor's routes.

## Findings

### 1. Routes are treated as delivery, but Claude Code mostly searches (high, confirmed)

- **Evidence:** `context-architecture` defines reachability as a structural route from the floor (`SKILL.md`,
  Enforcement; `references/writing-rules.md`, "Separate Structural Routes From References"), and its checker
  measures nothing else. Search gets one paragraph, which states "Half of agent navigation is text search"
  without a source, contrary to the skill's own rule that every claim is verified or flagged. The measurement
  above shows search as Claude Code's largest path and floor routes as its smallest.
- **Consequence:** a layout can pass both checkers and still go unread, because the document is reachable only
  by a route that Claude Code rarely takes, and nothing requires it to be findable by the words a task uses. The
  walk test is the only behavioral gate, and it records route versus search only as a note.
- **Repair:** keep routes, since they serve human readers and Codex. Make search findability an equal
  requirement: a file named for its subject, a first line and headings that carry the task's vocabulary and
  literal identifiers, and route conditions phrased in that vocabulary. Replace the "half" claim with the
  measured split and its date. Have the walk test score route versus search per load.
- **Validation:** a controlled run on a synthetic repository, comparing documents with and without the
  search-surface rules, and the before-and-after mining agreed with the agent-setup session.

### 2. Obligations behind voluntary routes go unread (high, suspected)

- **Evidence:** `agents-context-docs` already keeps an obligation in the floor as one imperative line
  (`SKILL.md`, Shared Invariants), which the measurement supports. But `context-architecture` routes scoped
  instruction files from the floor (`references/default-layout.md`; `agents-context-docs`
  `assets/AGENTS.template.md`, Pointers: "Open the matching file yourself before working in its area").
  `agents-context-docs` `references/initialize.md` forbids `.claude/rules` and comparable client surfaces unless
  a target-client requirement justifies them, and `references/loading-model.md` advises avoiding unverified
  path-scoping frontmatter. Claude Code's documentation recommends exactly
  those for size: "Move instructions that matter for only part of the codebase into path-scoped rules, which load
  only when Claude works with matching files" ([memory](https://code.claude.com/docs/en/memory), read
  2026-11-18).
- **Consequence:** a rule an agent must obey in one subtree reaches Claude Code only if it follows a route it
  takes about one time in five.
- **Repair:** for must-follow scoped rules, prefer a mechanism the target client loads by itself (a nested
  instruction file the client discovers, or path-scoped rules) and keep the floor route as the portable
  fallback. Keep reference and evidence behind routes.
- **Validation:** the same controlled run, with a scoped rule delivered by route against delivery by an
  automatically loaded file.

### 3. The loading reference is stale for Claude Code and has no Codex adapter (high, confirmed)

- **Evidence:** `agents-context-docs/references/loading-model.md` records Claude Code as not reading
  `AGENTS.md` ("not read *(reported)*") and verified at 2.1.269. Claude Code's documentation now says it reads
  `AGENTS.md` when no `CLAUDE.md` exists, from version 2.1.277, and reads only `CLAUDE.md` when both exist. The
  installed version is 2.1.326. The reference covers Claude Code, OpenCode, and Copilot CLI and has no Codex
  section, though Codex is one of the author's two main clients and loads `AGENTS.md` as an injected message
  ("# AGENTS.md instructions for …" in its transcripts).
- **Consequence:** an agent following the reference reasons from a false Claude Code rule and has no verified
  facts for Codex nesting, overrides, or size limits.
- **Repair:** re-verify the Claude Code row and section against current documentation, stamped with version and
  read date; keep the `CLAUDE.md` symlink as the default because some sessions cannot read `AGENTS.md`, and say
  why. Add a Codex adapter verified from its documentation. Update the matching sentence in
  `context-architecture` ("`CLAUDE.md` as a symlink where a client requires that name") and the template
  comment.
- **Validation:** each adapter row cites its source and version; a fresh session per client confirms the
  loaded set where the client can report it.

### 4. The floor template lacks the boundary and goals slots other guidance requires (medium, confirmed)

- **Evidence:** `references/maintain.md` requires that "Boundaries are collected rather than scattered, so an
  agent can find what it must never do", but neither `assets/AGENTS.template.md` nor `references/templates.md`
  has a section for boundaries or for what to do when unsure. `context-architecture`'s default layout says the
  floor points to the project goals and states who decides, and `define-goal` writes that line, but the template
  has no slot for it.
- **Consequence:** a floor built from the template scatters its never-do rules across Gotchas and Conventions,
  and the goals pointer lands wherever the writing agent puts it.
- **Repair:** add a short "Boundaries" section (never without asking, and what to do when unsure) and a goals
  line under the identity paragraph, in both the template and the shapes file.
- **Validation:** initialize a fixture repository from the template and check that the boundaries and goals
  pointer each have one home.

### 5. Size guidance omits the client's own threshold (low, confirmed)

- **Evidence:** the checker's default budget is 2,000 words (`scripts/check_agent_context.py`). Claude Code's
  documentation sets "target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce
  adherence", and says imports "don't reduce its context cost".
- **Consequence:** small; the word budget is close to the line target, but the skill cites no source for it.
- **Repair:** cite the client threshold beside the default, and state that an import does not reduce the cost.

## Preserve

- The obligation-versus-evidence split in `agents-context-docs`: obligations stay on the floor, evidence moves to
  findings. The measurement supports it.
- The accretion test and the checker that measures it.
- The walk test as the behavioral gate, with its failure-mode table.

## Controlled Comparison

Twelve headless Claude Code 2.1.326 runs on Sonnet, three per condition, tested route wording against search
findability after the repairs. Each run worked in a fresh copy of a synthetic ten-document Python repository,
with the author's global instructions and skills loaded. Every run got the same task, adding a nullable
`delivered_at` column. The rule it needed lived in one document: after adding a migration, run
`python tools/rehash.py`, which rewrites a signed checksum file. Automatic loading was not tested, because the
client documentation already fixes that behavior.

| Route in `AGENTS.md`                         | Target document                       | Reached | By route | By search | Applied |
| -------------------------------------------- | ------------------------------------- | ------: | -------: | --------: | ------: |
| Plain ("Database notes: path")               | `notes-3.md`, rule in paragraph four  |     3/3 |        1 |         2 |     3/3 |
| Trigger-keyed ("Before adding … a column …") | `notes-3.md`                          |     3/3 |        3 |         0 |    2/3¹ |
| Plain                                        | `database-migrations.md`, terms first |     3/3 |        3 |         0 |     3/3 |
| Trigger-keyed                                | `database-migrations.md`              |     3/3 |        3 |         0 |     3/3 |

¹ The third run read the rule and drafted a plan that ran `rehash.py`, then stopped to ask before editing, as
the global instructions direct for a new change. It counts as a stop for confirmation, not a missed rule.

Every run reached the document, so the comparison hit its ceiling. A floor route led to the document in 10 of 12
runs whatever its wording. The two search arrivals were both in the weakest condition, a plain route to a
generically named file, where the agent searched for "migration" first and found the rule by its text. Three runs
per condition cannot separate the conditions, but the result bounds the field measurement. When a route exists
and the repository is small, Sonnet takes it. The low floor-route share measured in real sessions therefore points
at routes that are missing for the task, or lost among many documents, more than at route wording. Search
findability still decided the way in where the route was weakest, which supports keeping both repairs.

The runs cost USD 2.66 at API rates. No safeguard event occurred.

## Evidence

- **Executable check:** both validators on both packages; transcript-mining scripts over Claude Code and Codex
  sessions, with three hand-checked samples per client that led to two classifier corrections.
- **Heuristic walkthrough:** both packages read in full against the measured behavior and the client documentation.
- **Model evaluation:** the controlled comparison above, scored from each run's own tool calls and final
  repository state with no grader model; three runs' tool sequences were checked by hand against the scores.

Coverage limits: OpenCode and Copilot CLI behavior was not measured; the controlled comparison ran only Claude
Code on Sonnet, in a repository small enough that every condition reached the document; the Claude Code and
Codex samples cover different repositories; the mining logic is kept in the author's private configuration repository, which
reproduces these counts row for row, so a reader of this record cannot regenerate them.
