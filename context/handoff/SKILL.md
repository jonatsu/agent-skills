---
name: handoff
description: "Write a continuity brief so the next session resumes work instead of re-deriving it — either a paste-ready priming prompt for a fresh context, or a saved markdown handoff document for another agent, machine, or person. Use when the user says 'hand off', 'write a handoff', 'handoff doc', 'prime the next session', 'brief the next agent', 'I am about to clear the context', 'continuity doc', 'pick up where we left off', or when a long session hits a clean seam with substantial work left and context depth is starting to cost reasoning quality. Actions: hand off, prime, brief, carry context forward, capture what dies with this session. NOT for authoring project documentation, READMEs, or ADRs, and NOT for capturing durable learnings into memory or rules files."
metadata:
  author: Joonas Onatsu
  license: MIT
---

# Handoff

IRON LAW: A handoff is an operating brief, NEVER a recap of the conversation.
Write only what the next session cannot recover on its own. If a commit, plan,
ADR, or issue already holds it, cite the path and move on. The material that
MUST be written down is the part that exists nowhere but this context.

## Pre-empt the Misread

A fresh reader's mistakes are predictable. It over-reads a passing check as
proof, tidies an inconsistency that was left deliberately, treats a list of
things to verify as a list of things to fix. Each costs a session to undo and
one sentence to prevent.

So when a statement invites a wrong conclusion, block it in the same breath:

- "Verified by targeted eval, not a full sweep."
- "This is not a fix list. It is a verification list that mostly ends in fixes."
- "Parked on purpose — not dead code, and not yours to re-enable."

This is the third discipline, alongside self-sufficiency and no duplication. Ask
it of every claim: what is the wrong thing to conclude from this, and have I
said that it is wrong?

## Mode Gate

Classify the request before writing anything:

- `PRIME` — the same work continues in a fresh context on this machine, usually
  right after the user clears the session. The output is a paste-ready first
  message, delivered in the reply for copying. Nothing is saved to disk.
- `DOCUMENT` — the work goes to another agent, another machine, or a person, or
  the user asked for a file. The output is a markdown document saved to disk.

Infer the mode from the request; ask only when it is genuinely ambiguous. Both
modes use the same sections. They differ only in destination, addressee, and how
paths are written.

For a worked brief in both modes, read `references/example-brief.md`. Skip it
once the shape is familiar — the rules below govern, not the example.

## Workflow

- [ ] 1. Classify the mode
- [ ] 2. Gather ground truth ⚠️ REQUIRED — never write from memory alone
- [ ] 3. Draft only the sections that have content
- [ ] 4. Run the self-check ⚠️ REQUIRED
- [ ] 5. Deliver

## Gather Ground Truth ⚠️ REQUIRED

Confirm the facts this turn. A path, branch, commit, or command result you did
not verify MUST NOT appear in the brief — a stale reference is the one failure
the next session cannot detect for itself.

In a Git repository, at minimum establish the branch, the working-tree state,
and the commits this session produced:

```bash
git status --short
git branch --show-current
git log --oneline -10
```

Confirm that every file you are about to list still exists at the path you name.
When the brief will claim something is verified, MUST name the command that
verified it and its result. If it was never run, say so instead.

Verify to establish facts, not to inventory state. Every item that reaches the
brief MUST name the decision it unblocks. If you cannot say which choice the next
session makes differently because of it, cut it — diligence is not a
justification, and the writer never observes a useless line failing.

**Pass identity, never tallies.** Paths, branch names, symbol and heading names,
and commit subjects travel intact. Counts do not: commits ahead of a remote,
changed-file counts, diffstat totals, percentages, and line numbers are all
derived over a tree the next session is about to move, so the very work this brief
enables is what invalidates them.

**Volatile state gets a command, not a value.** Write "run `git status -sb`",
never "the remote is 3 commits ahead". Freezing a recomputable number is worse
than omitting it: the reader may trust the snapshot instead of re-running it, so a
fact that was fresh arrives stale and carrying false confidence. Spend the space
on what cannot be recomputed — the constraint you were handed, the approach you
rejected and why, the dead end already explored.

## Sections

Five sections are always present. The rest MUST appear when they have content
and MUST be omitted entirely when they do not — a heading with nothing under it
tells the reader a lie about completeness.

### MISSION — always

Open with where the reader is and what kind of session this is: the repository,
branch, and commit; what the previous session did, in a line; and what this one
is for. A cleanup lane, a design pass, and a debugging hunt call for different
behaviour, and the reader cannot infer which from a task list.

State any precondition on the whole session here rather than inside NEXT. "Read
the files below and confirm the work list before editing anything" belongs above
the reading list, where a reader who skims still meets it.

### READ FIRST — always

Every file the next session must read to rebuild context, in reading order, each
with one line on why it matters and what to take from it. Include the artifacts
the work depends on: plans, specs, ADRs, issues, PRs, reference docs.

Point inside the file, not just at it — which section is authoritative, which
entry is load-bearing, what must be done before the file is usable. "Read the
contract" is weaker than "read the contract; two of its mandates are hard
requirements, and both tools it names must be loaded before use".

Under-listing is the common failure. The reader cannot know what it has not been
shown, so a file you leave out is a file it will never open. A narrow task may
need one entry; a deep one may need a dozen.

MUST cite by path or URL. MUST NOT paste the contents — that is the duplication
this skill exists to prevent. When a citation form decays — a line number in a
file under active edit — say so and give the stable handle to re-find it by.

### STATE — always

What is done, and how it was verified. Anchor claims to commits, and name the
command that proved each one.

NEVER write "should work". Either it was checked and you say what checked it, or
it is unverified and you say that. An unverified claim presented as done is the
most expensive error a handoff can carry, because the next session builds on it.

State the verification's limit as well as its result. "Passes the eval gate" and
"is known to build" are different claims, and a reader that conflates them
builds on sand. Name what the check did NOT cover.

Record any temporary change made to obtain a result and then undone, and how you
know it was undone. An unreverted probe is invisible to the next session and
reads as intended code.

**Record the files read and deliberately left alone, not only the ones changed.**
A path examined and found irrelevant is knowledge no command can recover — it
exists nowhere but in this session — and omitting it buys an exact repeat of the
search that produced it. One line each, with the reason: "the controller — read,
no change needed, the check lives in the middleware". This is the cheapest entry
in the whole brief and the one most often left out.

For files that did change, name what changed inside them — the function, the
section, the config key — not merely the path. A path tells the reader where to
look; it does not tell them what they are looking for, and a summary that says
"updated the config" sends them to re-read the whole file.

This is not in tension with passing a command rather than a value: the working
tree is recomputable and belongs to `git status`, but what you read, what you
rejected, and why are history, and history has no command.

Cover what is in progress and what is blocked, each with the branch, file, or
external dependency involved.

### NEXT — always

The immediate task and its completion bar: what "done" means concretely enough
that the next session can tell when it has arrived. Then whatever is queued
behind it, in order.

"Continue the work" is not a task. "Land the parser fix on `feature/parse`,
green CI, then open the PR" is.

For a long list of independent items, group by how far each item's premise can
be trusted rather than by sequence: confirmed and ready; probably already done,
so verify and close; target has moved, so relocate before acting. That grouping
encodes the outcome most easily missed — closing a dead item is finishing it,
not skipping it.

### CARRIED CONTEXT — always

What was learned that is written down nowhere else. This is the section that
justifies the whole brief: everything else survives in Git, and this does not.

- Naming, structure, and style choices the user steered mid-session
- Conventions inferred from the code that no document states
- Preferences stated in passing
- Options already considered and ruled out, and why — otherwise the next session
  proposes them again in good faith, and the user pays to reject them twice
- Dead ends already explored, so they are not re-explored

### LOCKED — when non-empty

Decisions already settled, with the instruction not to reopen them. Without
this, a fresh agent redesigns finished work in good faith.

Record the decision AND the one line that decided it — not the debate, but the
argument that won. A decision without its argument is an order the reader cannot
evaluate, so it has no way to tell whether something it just learned is grounds
to reopen the question or noise to ignore. "Kept because the deploy order is
hard, not to prevent slips" shows exactly where the edge of the decision runs.

### SCOPE — when non-empty

What is deliberately out of bounds: work that is blocked and must be left alone,
material parked on purpose, and tasks that exist and MUST NOT be started this
session. Say which, and give the reason in a clause.

This is not LOCKED. LOCKED settles decisions; SCOPE draws boundaries around
work. Without it a conscientious reader finds the parked thing and helpfully
un-parks it.

### OPEN — when non-empty

Decisions the next session MUST make. For each: the options, the current lean,
and what the decision depends on. Recording the lean is the point — it saves the
next session re-deriving a position the user already holds.

Omit decisions that can be deferred; a list of everything unsettled is noise.

### DEVIATIONS — when non-empty

Where the implementation departs from the written plan, and why. Without this
the next session "fixes" the deviation back and undoes deliberate work.

### PROCESS — when non-empty

The failure modes that already cost rework in this lane: gates to run before
committing rather than after, staging traps, tool restrictions, environment
limits, commands that are blocked or unavailable. Each entry should have already
bitten once.

### SKILLS — when non-empty

Name the skills the next session should use, and what each is for.

Prefer naming a skill where its trigger is described, rather than in a roster of
its own: "when two decisions would land in one reply, use the interview skill
and put them one at a time" beats a decontextualized list. A skill bound to its
condition gets used; a listed one gets skimmed. Keep this section for what has
no natural home elsewhere.

MUST name only skills available in the current session. NEVER copy a skill list
from another project, another machine, or this skill's own examples — a
recommendation that does not resolve is worse than none, because the next
session wastes a turn discovering it.

## Tailoring to the Next Session's Focus

When the user names what the next session is for, weight the sections toward it:

| Focus | Emphasize |
|---|---|
| Ship, deploy, release | Exact commands, required checks, approvers, rollback path |
| Review, audit | What changed, sensitive files, the checklist to apply |
| Debug, investigate | Symptom, reproduction, what was already ruled out, smallest failing case |
| Design, plan | Constraints, rejected alternatives and why, what is reversible |
| Test, QA | Existing coverage, gaps, edge cases, how success is measured |

Treat any text passed with the invocation as that statement of focus: it names
what the next session is for, not what this one did.

Absent a stated focus, weight toward NEXT and CARRIED CONTEXT.

## Length

Scale the brief to the work, not to a target number. A single-task continuation
needs a dozen lines. A lane with ten independent items, a drifted work list, and
a long tail of environment traps may need ten times that and still carry no
slack.

The test is duplication, not length: a brief longer than the artifacts it cites
has copied rather than referenced — go back and replace the copies with paths.
Compress by trusting the reader, which can open any file you name. Reasoning
worth preserving belongs in an ADR that the brief then cites.

## Redaction ⚠️ REQUIRED

MUST NOT write secrets into the brief: API keys, tokens, passwords, private
URLs, or personal data. This applies with force in `DOCUMENT` mode, where the
file outlives the session and may be sent elsewhere. Name the secret's location
(`the token in the deploy config`) rather than its value.

## Self-Check ⚠️ REQUIRED

Before delivering, verify each:

- [ ] Every path, branch, and commit was confirmed this turn
- [ ] Every item names a decision it unblocks; nothing is present merely because
      it was easy to collect
- [ ] No tally the reader could recompute — commits ahead, changed-file counts,
      line numbers — is stated as a value instead of a command
- [ ] No section duplicates an artifact it could have cited
- [ ] Every "done" claim names what verified it, or is marked unverified
- [ ] No empty or placeholder sections remain
- [ ] No pronoun refers to this conversation — the reader cannot see it
- [ ] Skills named are available in this session
- [ ] No secrets in the text
- [ ] Every claim that invites a wrong conclusion says what the wrong one is
- [ ] Work deliberately left undone is in SCOPE, not merely absent
- [ ] READ FIRST would let a reader with zero context start work

Then run the one check the list cannot encode: read the brief back as the next
session — knowing nothing but these words — and find the first question you
cannot answer from it. That question is the gap. Fill it and read again.

## Delivery

### PRIME

Deliver the brief in the reply as a single fenced block the user can copy whole.
Address it to the agent that will receive it, in the imperative. Do not save a
file; the paste is the delivery.

Self-sufficiency is absolute here. NEVER write "as we discussed", "the approach
we chose", or any pronoun pointing at a conversation the reader cannot see.
Every reference MUST resolve from the text alone.

### DOCUMENT

Save under the operating system's temporary directory. Establish the tool by
probe, never by assumption: `command -v mktemp` first, and when it is absent fall
back to `$TMPDIR`, then `/tmp`, then the platform equivalent. NEVER write
into the working tree unless the user names a path there; an untracked file in a
repository gets committed by accident.

MUST read the target path before writing it. If a file already exists there,
stop and ask rather than overwriting.

When the brief may travel to another machine, write repository-relative paths
and identify the repository and branch once at the top, so the paths resolve
somewhere else.

Report the saved path in the reply.

## Anti-Patterns

- **Retelling the conversation.** Chronology is not a brief. The next session
  needs the current state and what to do, not how the session got there.
- **Duplicating an artifact.** Pasting a plan, ADR, spec, issue body, or commit
  message instead of citing its path. The copy goes stale; the path does not.
- **"Should work."** An unverified claim written as a finished one.
- **Empty scaffold.** Emitting every heading and filling half of them.
- **Handing off a handoff.** If the brief mostly summarizes the previous brief,
  the session did no work worth carrying — say that instead.
- **Stale paths.** Branches deleted, files moved, commits rebased away.
- **The frozen tally.** A number the reader could recompute in one command —
  commits ahead of a remote, files changed, a line number — pasted as a fact. It
  is stale on arrival and invites trust it has not earned. Name the command.
- **Inventorying state.** Collecting everything cheap to gather because gathering
  looks like rigor. Each line must earn its place by unblocking a decision.
- **Under-listing READ FIRST.** The most common failure, and invisible to the
  reader who suffers it.
- **Recommending skills that do not exist here.**
- **Silently dropping scope.** Work left undone on purpose, recorded nowhere, so
  the next session either redoes it or wanders into it unaware.
- **The unbounded claim.** "Verified" with no statement of what the check did not
  cover, which the reader then reads as covering everything.
- **Burying the task.** If NEXT is not obvious on a skim, the brief failed.
