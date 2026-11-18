# Autopilot runs in past agent transcripts

This record answers four questions about unattended agent runs: how many there were and how they ended, what stalled\
them, what other failure patterns appeared, and which behaviours kept them going. It rests on a read of Claude Code,\
Codex, and Oh-My-Pi session transcripts on one workstation, taken on 2026-11-19. Projects are described by kind only.

## Scope and method

A run counts as an autopilot run when a goal loop was armed for it. In Claude Code the loop leaves `goal_status`\
records: one when the goal is set, one for every judge verdict, and one when the goal is cleared. The judge is the\
model that decides, each time the agent stops, whether the goal condition holds. Codex and Oh-My-Pi runs would show as\
`create_goal` and `goal` tool calls. Excluded work projects were not opened.

Counts come from scripts over the raw transcripts. Statements about cause come from reading the surrounding turns, so\
they are less certain than the counts. Wall-clock durations run from arming to the last goal record and include time\
spent waiting for the user.

## 1. Runs found and how they ended

| Harness     | Sessions in scope | Autopilot runs     | Note                                                                           |
| ----------- | ----------------- | ------------------ | ------------------------------------------------------------------------------ |
| Claude Code | 173               | 38, in 12 sessions | Every one of the 12 sessions ran in auto permission mode.                      |
| Codex       | 84                | 0                  | The rule text appears only inside evaluation probes; no goal tool call exists. |
| Oh-My-Pi    | 10                | 0                  | No goal call and no autopilot request.                                         |

The 38 Claude Code runs came from eleven project kinds: a dotfiles repository, a Nix configuration repository, an\
agent-configuration repository, a documentation project, an OCR tool, a sandbox launcher, a VM-management server, an\
OpenWrt build tool, and an agent plugin. The median run lasted 1.5 hours. Seventeen lasted under one hour, fifteen\
between one and three hours, and six lasted three hours or more (4.8, 7.3, 9.1, 10.3, 13.4, and 31.4 hours).

Twenty-six runs ended when the judge accepted the condition. Eleven of those passed on the first verdict, six cited\
parked items in the verdict, and four were accepted through the condition's own "stop and report" clause. The other\
twelve ended when the user cleared or replaced the goal (inferred from a goal record without a judge reason that\
follows a local-command notice). Six of those twelve followed five or more rejections, so they were stalls that the\
user ended; the rest were hand-offs after finished work or a replacement goal.

The judge issued 680 rejections in total. Fifteen runs had none, twelve had one to three, five had four to nine, and\
six had ten or more. One run accounted for 566 of the 680 (see pattern 3a).

Six runs ended with the user returning to unblock them: a locked signing key, two disk-space waits, a manual check that\
needed root, a review blocked by an outage, and a decision the agent could not make. Before the autopilot rule existed,\
the user described the opposite failure in one transcript: the agent "had stopped 5 minutes after I left it to go to\
sleep" on a question it could answer itself, or announced its next step and then did nothing. The sessions read here\
all postdate that complaint and show no case of it.

## 2. Permission stalls and denied calls

A denial that returns at once costs one retry. A permission prompt that nobody answers costs the whole run. The\
transcripts hold both, and the numbers differ by a factor of ten.

### 2a. Prompts that waited for a person (about 19 incidents)

Most of these were visible only through the user's later remarks or a long gap between a tool call and its result, so\
the count is a floor.

| Command shape                                                                                                                         | Incidents                                           | What happened                                                                                                                                                                   |
| ------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `cd <dir> && git push`, `git -C <dir> ...`, or a push piped through `tail`                                                            | 5, in one project                                   | The push left the standing opt-in and fell back to a prompt. One push sat 74 minutes. The user wrote: "Do not use the "cd <dir> && ..." form, you will get stuck on autopilot." |
| A quick command in a subagent lane (`mv`, `rm -rf`, `cd` plus `rm`, a heredoc write, a rebase)                                        | 7 of 653 subagent transcripts; one more user report | The lane stopped for 15 to 191 minutes while the main agent waited on it. The user noted that a lane "tends to get stuck on permission prompts I have to approve".              |
| A chained command (`... && git add ... && GIT_EDITOR=true git rebase --continue`), a script run from a scratch folder, a release push | 4, in one project                                   | The user answered each prompt in person and called the prompting "bit random".                                                                                                  |
| `AskUserQuestion`                                                                                                                     | 7 inside goal windows                               | The tool raises a "needs your permission" notification and blocks until answered. Three dialogs waited 58, 180, and 462 minutes.                                                |
| A build command the auto-mode classifier judged dangerous without an explanation                                                      | 1                                                   | The agent stopped and asked the user to allow it or run it.                                                                                                                     |
| A signed commit or push while the secret store behind the signing key was locked                                                      | 2                                                   | The commit hung to its timeout in the main session and in a subagent lane; the lane sat for about three hours. See pattern 3a.                                                  |

What would have avoided each stall:

- Run every push as its own call, `git push origin <branch>`, with nothing before or after it. The guard that enforces\
  this, a pre-tool hook, replies with the allowed shape, and the agent recovers on its next call.
- Avoid `cd` prefixes and `git -C`; the agent already starts in the repository.
- Give subagents the same standalone-command discipline in their brief, because a lane prompt reaches no one at night.
- Check before leaving that the signing agent is unlocked and that logins to MCP servers last until morning. The user\
  raised the login lifetime to 24 hours for this reason.
- Write goals so that a human-only step ends the run instead of waiting (pattern 3a).

### 2b. Denials that returned at once

Across the 12 sessions, 331 calls met a command-safety hook. Of these, 118 were interpreter one-liners, 66 were `rg -r`\
bundles, 18 were `rm -rf` outside the working directory, 13 were `fd -x`, 10 were `git checkout --`, and 8 were bulk\
`git add`. Twenty-two fell inside goal windows. In 51 of the 103 cases where the next call could be classified, the\
agent went on to another shell call; the rest switched to an edit, read, or write tool. I did not separate a rewritten\
command from a repeat. No run stalled on a hook block, because each reply names a rule and an alternative.

The auto-mode classifier denied 30 calls. Twenty of them came in one night as "no verdict" errors on a harmless\
lock-check command. The harness stops the turn after ten such replies in a row, and the goal loop restarted it each\
time. A second cluster was safeguard stops: 18 distinct requests, in four sessions, ended Opus subagents that were\
doing reviews.

Another 137 calls were refused with "Permission denied" or "The user does not want to proceed". Eight fell in goal\
windows. The transcript does not tell a user's refusal from an unanswered prompt.

## 3. Other stall and failure patterns

### 3a. A goal condition that only a human can satisfy (9 runs)

The judge counts "waiting for the user" as not met unless the condition says otherwise. The agent then has nothing to\
do except repeat a status line, and the loop wakes it again. Nine runs hit this:

- A locked signing key blocked every commit. The run drew 566 rejections over about six hours, until the user came back.
- A review step that the condition required on one model was stopped three times by safeguards, so the condition could\
  never hold. The agent asked the user to accept the other model and stopped. The run sat 31 hours with ten rejections.
- Two runs waited for free disk space that another session had to release (15 and 9 rejections).
- A manual check needed root (14 rejections); the agent wrote "only your answer ... can move this goal forward". The\
  user's verdict on the judge: "Goal judge is stupid sometimes".
- A conformance review reported mismatches that needed the owner's design decisions (10 rejections).
- An external check failed on a rate limit, and a user shutdown request conflicted with a loop that kept blocking the\
  exit (6 rejections).
- A memory floor stopped a build (7 rejections). The judge accepted the run once it read the "stop and report"\
  alternative.

The user's repair was a clause in the next goal. The run that followed the 566-rejection stall reads: "do not continue\
or retry after such a stop." It ended after one rejection. The user's own words before arming it: "Otherwise the goal\
judge will hammer you endlessly".

### 3b. Premature or stale completion (about 10 runs)

The judge rejected an early "done" when the proof predated the last change: a ledger line edited after the final check,\
a closing check run before the final commit, or a review that had not seen the fixes. By keyword match on the first two\
verdicts, about 10 runs hit this and about 16 hit an unfinished review gate. Each cleared within an hour once the agent\
reran the closing checks after its last commit. This was the judge working as intended.

### 3c. Asking the absent user (7 dialogs)

The seven `AskUserQuestion` dialogs in section 2a are the clearest cases. Three ran long because the agent asked, the\
loop re-armed, and nothing else was queued. Some stop-turn messages also ended on a question ("Do you approve the\
plan?"), which the loop answered with another prompt. These runs show agents parking a question and moving on, and they\
also show agents asking and waiting. The second behaviour happened mostly in runs whose condition did not name a\
parking place.

### 3d. Harness behaviours

- When only background subagents were running, the harness posted "idle check-ins paused until your next message" and\
  stopped waking the agent. This appeared in three sessions, three times each.
- A stop-hook goal loop keeps blocking exit until the goal is cleared. One run needed `/goal clear` before the user\
  could shut down.
- A usage limit reached mid-run ended work in two sessions, and one laptop suspended mid-command for ten hours. Neither\
  is a design failure, but both show that a run needs a way to resume from its ledger.

### 3e. Not seen

No run lost its task after compaction. About 10 to 20 compaction records fall inside goal windows (the count may\
double-count summary and boundary records), and each run continued from its goal text plus a checkpoint or ledger file.\
No run showed harmful scope creep. An agent that found an adjacent improvement wrote that it was "outside the current\
goal" and moved it to the roadmap.

## 4. What kept runs moving

| Behaviour                                                                       | Where it appeared                                                             | Example                                                                                                                          |
| ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Goal condition names a ledger the agent keeps current                           | 36 of 38 conditions                                                           | "Every item in the checkpoint shows a commit SHA or parked with its TODO heading."                                               |
| Closing evidence that a command prints                                          | 20 conditions name a clean `git status` or an exit code after the last commit | A condition ended with `git status --short` printing nothing, and the judge accepted on that evidence.                           |
| Explicit stop clause                                                            | 33 conditions; 4 runs accepted through it                                     | "Or stop and report when every remaining step waits on a parked question."                                                       |
| Parking a question with options and a recommendation, then taking the next item | 9 of 12 sessions                                                              | "Now I will park the six design questions in `TODO.md`, each with a recommendation and an alternative, for the owner to answer." |
| Recording each judgement call with how to undo it                               | 4 sessions                                                                    | "Each of these calls is recorded in the decision record's implementation notes, with how to undo it."                            |
| Write-back at each slice boundary                                               | 10 of 12 sessions                                                             | The agent committed a ledger update after every landed item, and the next verdict could cite it.                                 |
| A standing boundary list inside the goal                                        | 24 conditions: no push, no deploy, no secrets                                 | "Never push, publish, or use real agent or MCP logins; park those steps ... and continue."                                       |
| Separate review lanes while the agent waited                                    | most runs of three hours or more                                              | Code, security, and conformance reviews ran in parallel lanes, and the agent merged their findings.                              |
| Closing runs after the last commit                                              | 11 runs passed with no rejection                                              | The agent reran its checks after the final edit instead of citing earlier ones.                                                  |

Two of the longest runs show the pattern at its best. One ran ten hours with two rejections and landed four slices.\
Another ran 13 hours with none and ended when the user wound it down. Both had a parked-question rule in the goal text\
and a ledger entry for each slice.
