# Harness Goal Loops

How each harness sets, forwards, and judges a goal. Find your harness by the tools you hold and your system
prompt, then follow its section. Current known: Claude Code 2.1.288, Codex CLI 0.160.0, GitHub Copilot CLI
1.0.91 and Oh-My-Pi 18.5.1, checked 2026-10-04 by reading each harness's source or bundle. Confirm a detail that
matters with the harness's `/help`, its `--help`, or its changelog, because these features change between
releases.

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
  define or set a goal is one. Pass `token_budget` only when the user named a budget.
- **Forwarded as:** a hidden continuation turn whenever the thread goes idle with the goal active, carrying the
  objective and an audit to run before claiming completion. The objective is not in the system prompt.
- **Judged by:** you. Call `update_goal` with `complete` only after every criterion's verification output is in
  hand. Use `blocked` for a stop condition that persists, not on the first obstacle; the continuation prompt
  carries the exact rule. Use `paused` only when the user asks.
- **Ends on:** completion, a blocked or paused status, an exhausted budget, or repeated turns that make no
  progress. The user edits with `/goal edit` and resumes with `/goal resume`.
- **Subagents:** they do not see the goal, but their tokens count against its budget.

## Oh-My-Pi

The `goal` tool, with `op` values `create`, `get`, `complete`, `resume` and `drop`, exists only while goal mode
is active or during the `/guided-goal` interview.

- **Set:** outside goal mode, hand the user `/goal set <objective>`, or suggest `/guided-goal`, which interviews
  the user into the same five sections this skill writes: objective, success criteria, verification,
  boundaries, and stop conditions. Inside goal mode, use `goal` with `op: "get"`, then `op: "create"`; `create`
  fails while a goal exists. Set `token_budget` only when the user named one. Goal mode and plan mode exclude
  each other.
- **Forwarded as:** a hidden `<goal_context>` message on every prompt, with the objective, budget, audit rules
  and a todo summary, and a hidden continuation prompt shortly after each turn ends.
- **Judged by:** you, with `op: "complete"` after auditing the repository state against every criterion.
- **Ends on:** completion, a drop or pause, an exhausted budget, two continuation turns with no new tool
  activity, or every open todo blocked. An interrupt or a resumed session pauses the goal until the user
  resumes it.
- **Subagents:** they do not see the goal.

## Claude Code

You cannot set a goal yourself unless a `ProposeGoal` tool is in your tool list; it is behind a feature flag
and absent in plan mode, background sessions, subagents, and non-interactive runs.

- **Set:** hand the user `/goal <condition>`, with the condition from this skill, up to 4,000 characters. With
  `ProposeGoal`, propose the same condition, at most 500 characters; the user approves it with one keypress.
  A new `/goal` replaces the old one, and `/goal clear` removes it.
- **Forwarded as:** a kickoff message when the goal is set, then, after each turn the judge rejects, a message
  quoting the condition and the judge's reason. There is no system-prompt section and no reminder on other
  turns.
- **Judged by:** a separate small model with no tools, after every turn of the main session. It reads only the
  most recent part of the transcript, so the passing verification output must sit there, near the end. A met or
  impossible verdict clears the goal; after 8 rejected turns in a row the goal pauses, still set.
- **Ends on:** a met or impossible verdict, the 8-rejection pause, `/goal clear`, or an account or model error.
  Do not tell the user to run `/goal clear` after success; a met goal clears itself.
- **Subagents:** the judge never runs for them, and they do not see the goal.

## GitHub Copilot CLI

`/goal` is an alias of `/autopilot`, and you cannot set an objective yourself.

- **Set:** hand the user `/autopilot <objective>`. A credit limit is `--max-ai-credits <N>`, added only when the
  user named one. A new objective replaces the current one.
- **Forwarded as:** a hidden message stating the objective when it is set, and a continuation naming the active
  objective whenever the agent goes idle.
- **Judged by:** a read-only reviewer subagent, when you call `task_complete`. It weighs your summary against
  the objective, so the summary must cite the verification commands and their passing output. A rejection sends
  you back to work; a blocked verdict pauses for the user.
- **Ends on:** an accepted `task_complete`, a pause for the user, an exhausted credit limit, or a lack of
  progress. The user resumes a credit-paused objective with `/autopilot --max-ai-credits <N>`.
- **Subagents:** not verified whether they see the objective; restate it in their briefs regardless.

## A Harness With No Goal Loop

No loop resumes you, so the checkpoint copy is the goal. Work toward it in the same turn, report against each
criterion when you stop, and name any criterion whose evidence is still missing.
