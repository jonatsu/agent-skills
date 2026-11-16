---
name: session-reflect
description: Review a finished or ongoing agent session and turn what it taught into durable fixes, from memories and instruction rules to automated checks, reviewer standards and navigation pointers. Use for /session-reflect, a retrospective on a session, "capture learnings", "what should we change after this session", or "prune memories". To judge the code a session produced, use a code review instead.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Session Reflect

Turn one session into durable improvements, so the next session does not repeat its corrections, mistakes, and
manual work. A finding has two possible homes: what the agent should **remember** (a memory, an instruction rule)
and what the **environment** should change so the mistake cannot recur (a check, a reviewer standard, a pointer,
a script). This skill defines the routing, the thresholds and the autonomy boundary for both.

**Iron law: capture only what happened in this session.** Every candidate cites the turn or action it came from.
When nothing qualifies, say so and stop; a smooth session has little to teach, and inventing a lesson to fill the
sweep is the failure this law exists to stop.

## 0. Load your agent's reference

Identify the agent you are running in, then read its reference before anything else. It names where that agent
keeps memory, user and project instructions, and session logs, and any step only that agent has.

| Agent              | Reference                                              |
| ------------------ | ------------------------------------------------------ |
| Claude Code        | [references/claude-code.md](references/claude-code.md) |
| Codex CLI          | [references/codex.md](references/codex.md)             |
| GitHub Copilot CLI | [references/copilot-cli.md](references/copilot-cli.md) |
| Oh-My-Pi           | [references/oh-my-pi.md](references/oh-my-pi.md)       |

For any other agent, find the same facts in its own documentation, and say in the report which ones you could
not establish.

The session under review is the current one unless the user names another. A past session is read from the log
location the reference names, searched for the signals below and never read whole, because transcripts outgrow
the context window.

## 1. Scan the session for candidates

Look for each signal:

- **Corrections**: the user corrected an approach, an output, or an assumption.
- **Preferences**: the user stated how they want things done ("always…", "never…", "from now on…", "I prefer…").
- **Avoidable mistakes**: something went wrong that a captured guard or an automated check would prevent.
- **Slow navigation**: finding a file or fact took many searches, or a hidden dependency between files surprised
  the agent.
- **Expensive tool calls**: a call cost far more than its result was worth, or a tool's output was mostly noise.
- **Missing information**: the agent needed something it could not reach, such as a log, a service's state, or a
  document.
- **Repetition**: a command sequence or manual step recreated two or three times or more.
- **Reusable patterns**: a method or role useful beyond this task.
- **Operational discoveries**: a non-obvious fact about the current repository, such as a path, a gotcha, or a
  permission boundary.
- **Re-derivation**: the session rebuilt something a durable artifact already held: a fact a memory holds, a
  command an instruction file documents, a decision a record settled. Each instance shows an artifact that
  exists but failed, through wrong content, a wrong home, or a description the search could not match. Record
  which, because the repair differs: rewrite, move, or re-word the trigger. A session that re-derives nothing is
  worth reporting too.

## 2. Route each candidate

| Candidate                                        | Destination                                                               |
| ------------------------------------------------ | ------------------------------------------------------------------------- |
| Preference or correction that spans repositories | The agent's memory, at user scope where it has one                        |
| Standing behavioral rule                         | The agent's user-level instructions, or the source that deploys them      |
| Repo-specific operational fact                   | The repository's instruction file                                         |
| Mistake a tool could have caught                 | The repository's automated checks: a lint rule, a test, a hook, a CI job  |
| Mistake that needs judgement to catch            | The standards the repository's code review reads                          |
| Slow navigation                                  | A pointer from a file the agent already reads to where the answer lives   |
| Expensive or noisy tool call                     | A leaner command, filter, or flag, named where the agent will look for it |
| Missing information                              | Wider read access: a log teed to a file, a read-only view of the service  |
| Repeated command sequence                        | An in-repo script or task-runner recipe                                   |
| Reusable method or role                          | The source that owns the user's skills or agents, or the repository's own |
| Anything deferred                                | The repository's ledger (its TODO, backlog, or roadmap)                   |

Route each candidate to its own scope: a repo-specific fact stays in the repository, and a preference that spans
repositories goes to memory or user instructions, wherever it happened to surface. A preference about how the
user likes things done goes to memory. When the user states it as a standing rule for every session, it becomes
a user-level rule, which is heavy, so propose it.

When the session finished, superseded, or disproved work that a ledger entry tracks, remove the entry, after
moving anything a later reader still needs to its durable home.

**Classify a mistake before writing a rule for it.** A mechanical violation, one a fixed pattern describes (a
banned call, an import shape, a file-location rule), gets a deterministic check, because a check fails where a
sentence in a standards file does not. Only a real judgement call becomes prose, and it goes where the reviewer
reads it: review has the context room to apply a standard, while the agent doing the work does not. Before
proposing a new check, read the repository's own check and CI commands. A check that exists but is not wired in,
or is silently broken, is the finding. A repository with no automated check at all is a finding of its own.

**Establish what owns a destination before writing to it.** A user-level instructions, skills, or agents
directory may be a deployment artifact: a sync or render tool writes it from a source elsewhere and overwrites
it on the next run, so a capture written there is lost without an error. Determine the owner from the
environment at the time of the capture: a manifest, a lock file, a render template, or a tracked source that
claims it. When something owns it, the capture goes to that source; when nothing does, the directory is itself
the home.

**Read the destination before proposing a new artifact.** When something there already covers the candidate,
extend it. A near-duplicate is worse than no capture, because two artifacts on one subject drift apart and
neither stays authoritative.

## 3. Apply the graduated ladder

Promote each candidate to the cheapest durable form that fits:

- A note or instruction-file entry: recurring knowledge or a gotcha, about two encounters.
- An in-repo script or recipe: a manual command sequence, about three uses.
- A check: a mechanical mistake, once, when the check is cheap to build and run.
- A skill or agent prompt: a reusable method or role, three to five uses, and useful beyond one repository.
- A user-level rule: any confirmed correction or stated standing preference; once is enough.

A candidate below its threshold is reported as deferred and offered for the ledger.

**Filter by what class of failure it was, and codify only the third:**

- A capability limit: the task was simply hard. A rule cannot fix it and fires forever on sessions it does not
  help.
- A one-off environment fault: a flaky network, a half-applied config, a race. Recording it teaches a
  superstition.
- A defect in the setup: a tool whose contract surprised the agent, a rule that said the wrong thing, a step
  nobody documented. Only this kind earns a durable artifact.

Fix it at the lowest level that can express the fix: a stale fact is a context fix, and a surprising tool
contract belongs in that tool's reference, not in an always-loaded instructions file. Reach higher only when the
failure recurs after the lower fix.

A threshold is necessary, not sufficient. A user-level rule loads into every later session, including the ones
it was not written for. Before codifying one, state what it costs when it fires on the wrong session, and narrow
its wording to the case observed.

## 4. Respect the autonomy boundary

- **Light**: repository notes, instruction-file entries, in-repo scripts, and memories private to the user.
  Create them directly, then report what changed.
- **Heavy**: new or changed skills, agent prompts, user-level rules, checks, reviewer standards, and any memory
  that others can read. Propose first, with the exact text, the destination, and its scope, and write only after
  the user approves.

## 5. Write the captures

- **Verify a configuration claim first.** Before capturing a claim about configuration or permissions, read the
  setting it names. An error message is evidence that a guard fired, not proof of how the guard is configured.
- **Memory**: write through the facility the agent's reference names, in its own format. Where memory is files,
  read a neighbouring entry and match its fields rather than a remembered schema, because tooling writes some
  fields itself. Put everything recall must match in the text the facility searches. A fact true across every
  repository, or about this machine, says so in that text, and so does a fact with a foreseeable expiry ("while
  the vendored hook is in use"). Delete a memory proven wrong.
- **Update by delta.** When revising an existing memory or instruction file, change the wrong lines and leave
  the rest. A model asked to regenerate an accumulated document drops what it judges low-priority, so rewrite
  whole only when the user asks.
- **Repository files**: match the file's structure and voice, and convert relative dates to absolute ones.
- **New skills and agents**: follow the conventions of the source that owns them.
- **Keep secrets out.** Transcripts and logs hold credentials, tokens, hostnames, and client details. A capture
  names the file a credential lives in, never its value.
- After a material edit to a repository file, run the repository's formatter, linter, or pre-commit hooks on the
  changed files before calling it done.

## 6. Report

Report a table of **candidate → destination → action** (written, proposed, or deferred), each with its evidence,
most severe first. List the heavy proposals in their own block, so the user can approve or reject each one, and
offer the deferred ones for the repository's ledger. Add any count the agent's reference asks for.

## 7. Memory maintenance

When the user asks to prune or review memories, or about every ten captures, sweep the memory the agent's
reference names for entries to retire:

- **Expired**: the expiry condition its text names has been met. An expired memory is worse than a missing one,
  because a missing fact produces a question and a stale one produces confident wrong action.
- **Self-invalidated**: it names a condition for its own removal, and that condition has happened.
- **Superseded**: a newer memory or a committed rule now covers it.
- **Duplicate**: two entries hold one fact; merge them.
- **Wrong or drifted**: it contradicts the current repository, configuration, or the user's latest guidance.
- **Dangling**: a file, flag, or path it names no longer exists.

Deleting a memory changes user data, so propose each deletion or merge with its reason and evidence, and act
only on approval. Recalled memories may be stale: verify them against live files before acting on one.
