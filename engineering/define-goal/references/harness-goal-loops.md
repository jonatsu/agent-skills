# Harness Goal Loops

How each harness sets, forwards, and judges a goal. Find your harness by the tools you hold and your system
prompt, then follow its section. Current known: Claude Code 2.1.326, Codex CLI 0.169.0, GitHub Copilot CLI
1.0.114 and Oh-My-Pi 18.22.0, checked 2026-11-19 by reading each harness's source, bundle, or documentation.
Confirm a detail that matters with the harness's `/help`, its `--help`, or its changelog, because these features
change between releases.

## Contents

- Codex CLI
- Oh-My-Pi
- Claude Code
- GitHub Copilot CLI
- A harness with no goal loop

## Codex CLI

You hold `get_goal`, `create_goal`, and `update_goal`.

- **Set:** call `get_goal` first. Keep an active goal that still matches the request; when one conflicts, ask
  the user to finish, pause, or clear it with `/goal clear` before you create another, because `create_goal`
  fails while an unfinished goal exists. Then call `create_goal` with the five-part goal as the objective, up to
  4,000 characters, condition first. The tool accepts a goal only on an explicit request, and a request to
  define or set a goal is one. A budget goes in `token_budget`. The user sets one with `/goal <objective>` in the
  terminal interface; no command-line flag sets a goal.
- **Forwarded as:** a hidden continuation turn whenever the thread goes idle with the goal active, carrying an
  audit to run before claiming completion. The objective travels separately, as a `goal_objective` item cut at
  1,000 tokens and sent again only when it changes. When it is missing or truncated, call `get_goal`.
- **Judged by:** you. Call `update_goal` with `complete` only after every criterion's verification output is in
  hand. Use `blocked` only after the same blocker has repeated for three consecutive goal turns; the continuation
  prompt carries the exact rule. Use `paused` only when the user asks.
- **Ends on:** completion, a blocked or paused status, an exhausted budget, a usage limit, or three automatic
  turns with no activity or only failed commands, which the runtime marks `blocked`. The user edits with
  `/goal edit` and resumes with `/goal resume`.
- **Headless:** `codex exec` stops after its first turn, so a goal never continues there.
- **Subagents:** each has its own empty goal, and its tokens count against the parent's budget. The default
  `spawn_agent` copies the parent's history, so a child sees the goal text there but no goal state.

## Oh-My-Pi

The `goal` tool, with `op` values `create`, `get`, `complete`, `resume` and `drop`, exists only while goal mode
is active or during the `/guided-goal` interview.

- **Set:** outside goal mode, hand the user `/goal set <objective>` or `omp --goal <objective>`, or suggest
  `/guided-goal`, which interviews the user into the same five sections this skill writes: objective, success
  criteria, verification, boundaries, and stop conditions. Inside goal mode, use `goal` with `op: "get"`, then
  `op: "create"`; `create` fails while a goal exists. A budget goes in `token_budget`. Goal mode and plan mode
  exclude each other, and a goal cannot run under `--print`.
- **Forwarded as:** a hidden `<goal_context>` message on every prompt, with the objective, budget, audit rules
  and a todo summary, and a hidden continuation prompt shortly after each turn ends.
- **Judged by:** you, with `op: "complete"` after auditing the repository state against every criterion. Never
  call `drop` to change the objective: it removes the `goal` tool, so ask the user to set the new goal.
- **Ends on:** completion, a drop or pause, an exhausted budget, or a continuation turn that makes no tool calls
  or repeats the previous turn's tool calls. An interrupt or a resumed session pauses the goal until the user
  resumes it.
- **Subagents:** they do not see the goal, and they drop every `AGENTS.md`. The `task` tool requires a `context`
  that carries the shared goal text.

## Claude Code

You cannot set a goal yourself unless `SetGoal` is in your tool list. It sits behind a remote feature flag, and
it is absent under `-p`, in background sessions, and in subagents.

- **Set:** hand the user `/goal <condition>`, with the condition from this skill, up to 4,000 characters. It also
  works as `claude -p "/goal <condition>"`, which runs the whole loop in one invocation. With `SetGoal`, propose
  the same condition, at most 500 characters; the user approves it with one keypress. A new `/goal` replaces the
  old one, and `/goal clear` removes it.
- **Forwarded as:** a kickoff message when the goal is set, then, after each turn the judge rejects, a message
  quoting the condition and the judge's reason, cut to 500 characters once the condition is in the transcript.
  When `GetGoal` is in your tool list, it reads the condition back after a compaction.
- **Judged by:** a separate small model with no tools, after every turn of the main session. It reads only the
  most recent part of the transcript, so the passing verification output must sit there, near the end. A met or
  impossible verdict clears the goal; after 8 rejected turns in a row the goal pauses, still set. A running
  subagent or background shell defers the judgment.
- **Ends on:** a met or impossible verdict, the 8-rejection pause, several turns with no tool use, `/goal clear`,
  or an unrecoverable account or model error. `PauseGoal`, where present, hands the user a blocker only they can
  remove. A met goal clears itself, so success leaves the user nothing to clear.
- **Subagents:** the judge never runs for them, and they do not see the goal.

## GitHub Copilot CLI

`/goal` is an alias of `/autopilot`, and you cannot set an objective yourself.

- **Set:** hand the user `/autopilot <objective>`. A credit limit is `--max-ai-credits <N>`. A new objective
  replaces the current one.
- **Forwarded as:** a hidden message stating the objective when it is set, and a continuation restating the full
  objective whenever the agent goes idle.
- **Judged by:** a read-only reviewer subagent, when you call `task_complete`. It weighs your summary against
  the objective, so the summary must cite the verification commands and their passing output. `FAIL` or
  `INCONCLUSIVE` sends you back to work; `BLOCKED` pauses for the user.
- **Ends on:** an accepted `task_complete`, a pause for the user, an exhausted credit limit, or repeated turns
  without tool progress. `--max-autopilot-continues` caps continuations only outside an objective. The user
  resumes a credit-paused objective with `/autopilot --max-ai-credits <N>`.
- **Subagents:** they do not see the objective, and each starts stateless, so restate it in their briefs.

## A Harness With No Goal Loop

No loop resumes you, so the checkpoint copy is the goal. Work toward it in the same turn, report against each
criterion when you stop, and name any criterion whose evidence is still missing.
