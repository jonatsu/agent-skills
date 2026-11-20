# Unattended Runs by Harness

How each harness arms a goal loop, judges and ends it, and handles a prompt or question nobody answers. Find your
harness by the tools you hold and your system prompt, then read its section. This reference covers Claude Code 2.1.326,
Codex CLI 0.169.0, GitHub Copilot CLI 1.0.114, and Oh-My-Pi 18.22.0. Each was checked on 2026-11-19 by reading its
source, bundle, or documentation. Confirm a detail that matters with the harness's `--help` or changelog, because these
features change between releases.

## Contents

- Claude Code
- Codex CLI
- Oh-My-Pi
- GitHub Copilot CLI
- A harness with no goal loop

## Claude Code

- **Arm:** hand the user `/goal <condition>`, up to 4,000 characters. `claude -p "/goal <condition>"` runs the whole
  loop in one invocation. The model-side `SetGoal`, `GetGoal` and `PauseGoal` tools exist only when a remote flag
  enables them, never under `-p`, in background sessions, or in subagents. Leave `--bare` off a goal run, because it
  skips the hooks the loop runs on.
- **Judge:** a small model with no tools reads the recent transcript after every main-thread turn. A rejection comes
  back as `Stop hook feedback` quoting the condition and the missing evidence. After 8 rejections in a row the goal
  pauses, still set. The judge accepts a stop clause it can read in the condition, so a fully parked run ends as met.
- **Background work:** a running subagent or background shell defers the judge. Check-ins start after 30 minutes, and at
  most three idle check-ins fire between user prompts. A run left waiting only on a stalled lane can sit until the user
  returns.
- **Questions:** `AskUserQuestion` waits until answered unless the user set `askUserQuestionTimeout` (60s, 5m or 10m).
  The timeout never starts in a background session or under Remote Control.
- **Permission prompts:** an interactive prompt never resolves on idle. Auto mode resumes prompting after 3 consecutive
  or 20 total classifier blocks. Under `-p`, a call that needs approval is denied, and `--permission-prompts none` also
  tells the model nobody can approve and removes `AskUserQuestion`.
- **Persistence:** after compaction, the project `CLAUDE.md` is re-read from disk. Invoked skill bodies are re-injected,
  most recent first, up to 5,000 tokens each and 25,000 in total. The condition returns only in the next judge feedback,
  cut to 500 characters when it already appears in the transcript.
- **Subagents:** they never see the goal, and the judge never runs for them. A fork inherits the history that holds the
  kickoff message.
- **Settings to name:** `askUserQuestionTimeout`, allow rules for the run's commands, auto permission mode for an
  interactive goal run, and `permissions.denyInsteadOfPrompting` or `--permission-prompts none` for a `-p` run.

## Codex CLI

- **Arm:** hand the user `/goal <objective>` in the terminal interface, up to 4,000 characters. You may call
  `create_goal` when the user explicitly asks for a goal. Call `get_goal` first, because creation fails while an
  unfinished goal exists. `codex exec` stops after its first turn, so it never continues a goal. Run the goal in an
  interactive session or through an app-server client.
- **Judge:** you. Call `update_goal` with `complete` once every criterion has its closing evidence. Under the stop
  clause, a fully parked list counts as complete. `blocked` is for a blocker that has repeated for three consecutive
  goal turns, never for work that is merely hard or would benefit from clarification. The runtime also sets `blocked`
  after three empty automatic turns, or three turns whose commands all failed.
- **Questions:** `request_user_input` exists in Plan mode, and in Default mode only behind an experimental feature. A
  question written as plain text ends the turn, and the loop starts another one. Put the question in the ledger and keep
  working.
- **Permission prompts:** in a terminal session an approval prompt waits for a person. `codex exec` rejects every
  approval and question request, and the model sees an error. `-a never` stops the interactive session from asking.
- **Persistence:** `AGENTS.md` is re-rendered after compaction. A loaded skill body is a hidden fragment that local
  compaction drops. The objective reaches the model as a `goal_objective` item, cut at 1,000 tokens and sent again only
  when it changes. When it is missing or truncated, call `get_goal`.
- **Subagents:** a subagent has its own empty goal, and its tokens count against the parent's budget. The default
  `spawn_agent` copies the parent's history, so the child sees the goal text there but no goal state.
- **Settings to name:** the approval policy (`-a`), the sandbox mode, and a `notify` command that runs when a turn
  completes.

## Oh-My-Pi

- **Arm:** hand the user `/goal set <objective>`, or `omp --goal <objective>` to start a fresh interactive session in
  goal mode. A goal cannot run under `--print`. An unattended run needs an open terminal session, or an RPC host with
  `goal.continuationModes` including `"rpc"`. Goal mode and plan mode exclude each other.
- **Judge:** you, with `goal` `op: "complete"`. No other model checks it. Under the stop clause, a fully parked list
  counts as complete. To end the objective, use `complete`. Never call `drop` to change or end it, because it removes
  the `goal` tool.
- **Loop stop:** continuation stops when a turn repeats the previous turn's tool calls or makes no tool calls. Repeating
  a status line ends the loop without completing the goal, so finish with `complete` instead.
- **Questions:** in the terminal interface, `ask` waits forever unless the user set `ask.timeout`. Headless sessions
  have no `ask` tool.
- **Permission prompts:** the default approval mode is `yolo`, but `tools.restrictedFolders` and any `tools.approval`
  rule set to prompt still ask, and a prompt with no interface fails.
- **Persistence:** the objective is re-sent before every prompt in a `<goal_context>` block. `AGENTS.md` and `RULES.md`
  sit in the rebuilt system prompt. A loaded skill body can be summarized away at compaction and is not re-injected. The
  ledger's copy of the run rules is the one that survives.
- **Subagents:** they have no goal, and they drop every `AGENTS.md`. The `task` tool requires a `context` that carries
  the shared goal text. Put a rule a lane must follow in that context or in `RULES.md`.
- **Settings to name:** `ask.timeout`, `tools.approvalMode`, and `--max-time` to bound the session.

## GitHub Copilot CLI

- **Arm:** hand the user `/autopilot <objective>`, or its alias `/goal`. `--max-ai-credits <N>` sets a soft credit cap.
  `--max-autopilot-continues` caps continuations only outside an objective. Whether `copilot -p` accepts an objective is
  unverified.
- **Judge:** a read-only reviewer subagent checks each `task_complete` call against the objective. Cite the closing
  commands and their passing output in the summary, and list each parked question there. `PASS` ends the objective,
  `FAIL` and `INCONCLUSIVE` send you back, and `BLOCKED` pauses for the user.
- **Questions:** autopilot answers `ask_user` itself, saying the user is away and will review later. For a genuinely
  unresolvable question, park it and end with `task_complete` summarizing it.
- **Permission prompts:** autopilot denies any request that would prompt, so only allow rules decide what runs. Repeated
  denials stop the run at a safety limit, so rewrite a denied command rather than retrying it.
- **Persistence:** every continuation restates the full objective. Release notes say skills survive compaction, but the
  mechanism was not traced.
- **Subagents:** they do not see the objective. The task tool treats each one as stateless, so the brief must carry
  everything the lane needs.
- **Settings to name:** `--allow-tool` rules for the run's commands, `--max-ai-credits`, and desktop `notifications`.

## A Harness With No Goal Loop

Nothing resumes you when a turn ends. Keep working in the same turn until the end condition holds. Use the same ledger
and run rules, and end with the same report.
