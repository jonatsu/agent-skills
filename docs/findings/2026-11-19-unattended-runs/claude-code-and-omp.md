Claude Code 2.1.326 and Oh-My-Pi (omp) 18.22.0, read on 2026-11-19.

Evidence labels: **[read]** means read at the cited place; **[inferred]** means concluded from read code or text\
without running it; **[live]** means only a live run can settle it. No model call was made and no session was started.

Sources and how to find them:

- Claude Code docs: pages under `https://code.claude.com/docs/en/<page>.md` (goal, headless, permission-modes,\
  sandboxing, sub-agents, context-window, skills, tools-reference, hooks, agent-view), and the changelog at\
  `https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md`.
- Claude Code bundle: the 2.1.326 `claude` binary is a Bun executable whose JavaScript modules are plain text. A module\
  is cited by a distinctive string to search for and by the byte offset of its `// @bun @bytecode` marker (`rg -a -b`\
  finds both). `claude --help` is cited as "help".
- omp: the npm package `@oh-my-pi/pi-coding-agent` 18.22.0 ships TypeScript under `src/`, cited as `src/<path>:<line>`.\
  Its documentation is bundled in `dist/docs-index.generated.txt` (a JSON array of page names on line 1, and the page\
  texts as gzip and base64 on line 2), cited as `docs: <page>`. Upstream is `https://github.com/can1357/oh-my-pi`.\
  `omp --help` is cited as "help".
- Baseline for "what changed": the notes made on 2026-10-04 at Claude Code 2.1.288 and omp 18.5.1.

## Claude Code 2.1.326

### 1. Goal loop now

**Setting a goal.** `/goal <condition>` sets it; `/goal` alone shows status; `/goal clear` (aliases `stop`, `off`,\
`reset`, `none`, `cancel`) removes it\
\[read: docs: goal.md "Use /goal"; bundle module 309797481, string `new Set(["clear","stop","off","reset","none","cancel"])`\].\
The condition may hold 4,000 characters \[read: same module, `vvn=4e3`; docs: goal.md "Write an effective condition"\].\
One goal is active per session; a new `/goal` replaces the old one [read: goal.md]. Setting a goal starts a turn at\
once, with the condition as the directive\
\[read: goal.md; module 355693643 returns `Goal set: <condition>` plus the kickoff prompt\]. The kickoff text is\
unchanged: "A session-scoped Stop hook is now active with condition: ... treat the condition itself as your directive"\
\[read: module 309797481, `v9r`\].

**Who may set it.** The user, with `/goal`, in an interactive session, in `claude -p "/goal ..."`, the desktop app, and\
Remote Control\
\[read: goal.md "Run non-interactively"; module 334144009, non-interactive variant has `supportsNonInteractive:!0`\]. Two\
gates apply: workspace trust (waived under `-p`), and the hooks gate (`/goal` fails when `disableAllHooks` or\
`allowManagedHooksOnly` is set, or while organization settings have not been read yet)\
\[read: module 309797481, messages `hooks_gate`, `hooks_held`, `trust_gate`; goal.md "Requirements"\]. A `/goal` message\
relayed from Slack or Teams is refused with "didn't set, clear or show the goal"\
\[read: module 309797481 `IHa`; module 355693643, gated on `tengu_mellow_sunset`\].

**Model-set goals.** The model now has three goal tools, all deferred and all behind one gate:

- `SetGoal` (internal name `ProposeGoal`, still accepted as an alias) proposes a condition of at most 500 characters.\
  By default it asks the user for approval. `ask_user: false` sets the goal directly only when the user's own words\
  stated the outcome; while a goal is active the dialog is always shown [read: modules 313958940 and 345395031].
- `GetGoal` returns the condition, the evaluator's last reason, and a `paused` flag. Its description says to use it\
  "when you have lost track of the goal, for example after the conversation was summarized"\
  [read: modules 314769823 and 345416313].
- `PauseGoal` pauses the goal until the user's next message, with a reason of at most 500 characters shown to the user;\
  the description limits it to a blocker "only the user can remove", never because work is hard or slow\
  [read: modules 314768206 and 345407478].

The gate is `function krt()` in module 332828055: it returns nothing for non-interactive or remote sessions, for\
background sessions, and unless the remote flag `tengu_propose_goal` (default `false`) is on, and it also returns\
nothing when the setting `modelProposedGoals` is `disabled` [read]. All three tools throw inside subagents ("cannot be\
used in agent contexts") [read: same modules]. The cached flags on the research machine held no `tengu_propose_goal`\
entry, so the default applies [read]; whether the server turns it on for some accounts is [live].

**How the goal returns to the model.** It is a session-scoped prompt-type Stop hook. After each main-thread turn, a\
"not met" verdict becomes a blocking Stop-hook message of the form `Stop hook feedback:` then\
`[<condition>]: <reason>`; the condition is cut to 500 characters when the transcript already holds `[<condition>]:` in\
a user message \[read: module 315497248, `[${e.prompt}]: ${reason}` and `TAs=500`\]. The `goal_status` and `goals`\
attachments map to no model message (`goal_status:()=>[]`, `goals:(e)=>[]`) [read: module 315497248]. Nothing re-sends\
the goal to the model except the kickoff, each feedback message, `GetGoal`, and check-in or retry prompts\
(`Goal check-in: «<condition>»`) [read: module 325815919; goal.md "Background work defers evaluation"].

**Who judges.** A separate small fast model, not the working model. The prompt-hook runner sends the transcript and the\
condition to `e.model ?? _T()` (the small fast model, Haiku by default, changed with `ANTHROPIC_DEFAULT_HAIKU_MODEL`),\
with a 30 s timeout and no tools, and expects `{ok, reason, impossible?}`; the system prompt text begins "You are\
evaluating a stop-condition hook in Claude Code"\
[read: module 315497248; goal.md "How evaluation works" and "Evaluation model and cost"]. It "doesn't run commands or\
read files independently" [read: goal.md].

**Budgets and caps.** No token or cost budget on the goal itself [read: goal.md lists none]. A turn or time clause in\
the condition is judged by the evaluator from the transcript [read: goal.md]. The Stop-hook block cap is\
`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`, default 8, and `0` removes the cap; hitting it ends the turn with a warning and the\
goal pauses ("Goal paused · goal checks kept finding it unmet this turn") [read: module 325815919]. The docs describe a\
second stop: "no tool use for several turns in a row" returns control with the goal still set\
[read: goal.md; the code for this rule was not located, so the exact count is unverified]. Print-mode caps still apply\
to a goal run: `--max-turns` and `--max-budget-usd` [read: cli-reference.md, flags table]. Evaluation is deferred while\
a subagent or background shell runs; check-ins start at 30 minutes (`CLAUDE_CODE_GOAL_CHECKIN_MINUTES`, `0` turns them\
and automatic retries off), double up to four times the interval, and at most three idle check-ins fire between user\
prompts [read: goal.md].

**How it ends.** Met: the goal clears and an achieved entry (with duration, turns, tokens) is recorded. Impossible,\
judged by the evaluator: it clears with a failed entry. Unrecoverable errors clear it (authentication, full disk, empty\
credits, context overflow that compaction cannot clear, unavailable model; text "Goal cleared after an unrecoverable\
error ... Run /goal again to continue"). Transient errors retry up to three times, then pause; rate limits, usage\
limits and a hook that ended the turn pause it \[read: goal.md "When a turn fails"; module 325815919 table `lh`\].\
`/clear` removes it. A resumed session restores a goal that was still active, on every resume route, with the turn\
count, timer and token baseline reset\
\[read: goal.md "Resume with an active goal"; module 309797481 `qZn` scans for the last `goal_status` attachment\]. A\
paused goal (new) keeps its condition; the check still ends a goal it finds met or impossible, but does not send the\
model back until the user's next message [read: module 345407478 description].

**Changed since 2026-10-04 (2.1.288).**

- `ProposeGoal` is now `SetGoal`, and `GetGoal` and `PauseGoal` are new. A model can read the goal back and hand a\
  blocker to the user, but only behind the same default-off remote flag and never in `-p`, background sessions, or\
  subagents [read].
- The hooks gate gained a "settings not read yet" case, and relayed chat messages cannot set, clear or show a goal\
  [read].
- The goal state now carries a `paused` state and a token count; status shows token spend\
  \[read: module 355693643 prints `Goal paused: ...`; goal.md "Check status"\].
- Docs now state the no-progress stop (no tool use for several turns) and the idle check-in cap with version numbers\
  (idle check-ins v2.1.236, cap v2.1.246, automatic retries v2.1.269, resume-picker restore v2.1.239) [read: goal.md].
- Changelog: 2.1.326 fixed "`/goal clear` or a new `/goal` not sticking when typed while Stop hooks were running and\
  background work was still in progress" [read: CHANGELOG.md, 2.1.326].
- Unchanged: evaluator model and prompt, kickoff text, feedback format, 4,000 and 500 character limits, block cap 8,\
  and the `krt` gate's `tengu_propose_goal` default `false` [read].

### 2. Unattended operation

**Non-interactive mode.** `claude -p "<prompt>"` runs once and exits; exit code 0 on success, non-zero on failure;\
SIGTERM exits 143 [read: headless.md "Basic usage", "Stop a run with SIGTERM"].\
`--output-format text|json|stream-json`, `--input-format text|stream-json`, `--include-partial-messages`,\
`--include-hook-events`, `--json-schema`, `--max-turns`, `--max-budget-usd`, `--no-session-persistence`,\
`--fallback-model` [read: help; cli-reference.md]. A `-p` goal runs the whole loop in one invocation; text output\
prints only the final response, so use `--output-format stream-json --verbose` to watch it\
[read: goal.md "Run non-interactively"]. `--bare` skips hooks, skills, plugins, MCP discovery, auto memory and\
CLAUDE.md, and the docs call it the recommended mode for scripted calls (it will become the `-p` default); hooks are\
skipped too, so a goal run, which depends on the hooks machinery, should not use it\
\[read: headless.md "Start faster with bare mode"; the goal-with-bare combination is [inferred] from goal.md "Requirements"\].\
At exit, a `-p` run waits up to 10 minutes (`CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS`) for background commands, subagents,\
Monitor watches and pending `/loop` wakeups [read: headless.md "Background tasks at exit"].

**Permission modes.** `--permission-mode` takes `acceptEdits`, `auto`, `bypassPermissions`, `manual`, `dontAsk`, `plan`\
[read: help]. Since 2.1.302 a `-p` run with no mode set starts in Manual mode, and calls that need approval are denied\
unless a rule, `PermissionRequest` hook or `--permission-prompt-tool` approves them\
[read: headless.md "Auto-approve tools"; permission-modes.md "Tool calls denied in claude -p"].\
`--permission-prompts none` (v2.1.259) denies anything that would prompt, tells the model nobody can approve, and\
removes `AskUserQuestion` [read: headless.md "Turn off permission prompts in unattended runs"; help].\
`permissions.denyInsteadOfPrompting` does the same persistently [read: same]. `--allowedTools` and `--disallowedTools`\
set rules; `dontAsk` fits a locked-down CI run [read: permission-modes.md table]. A goal does not change the permission\
mode; the docs advise `/goal` in auto mode for unattended goal turns [read: goal.md "Set a goal"]. Auto mode pauses and\
resumes prompting after 3 consecutive or 20 total classifier blocks; in a `-p` run with no prompt tool the action is\
simply not run and the run continues\
[read: permission-modes.md "When auto mode falls back", "Repeated-block thresholds"]. `--dangerously-skip-permissions`\
is documented for containers or VMs only [read: permission-modes.md table; help]. `--restricted` removes\
command-running tools, ignores user, project and local settings files, and confines file tools to the working\
directories [read: help].

**Sandboxing.** The Bash sandbox (off by default; `/sandbox` or `sandbox.enabled`) confines shell commands to the\
working directory for writes, a domain allowlist for the network, on macOS, Linux (bubblewrap, socat) and WSL2; file\
tools, MCP servers and hooks run outside it; with an unsupported platform it silently runs unsandboxed unless\
`sandbox.failIfUnavailable` is set [read: sandboxing.md "What the sandbox restricts", intro, Linux setup]. Other\
isolation: worktrees (`-w`, `isolation: worktree` for subagents) [read: help; sub-agents.md].

**Continuing later.** `--continue` resumes the latest conversation in the directory;\
`--resume <id|name|path-to-.jsonl>` resumes a specific one, from any directory; `--fork-session` copies it;\
`--session-id`, `-n/--name` name it [read: headless.md "Continue conversations"; help]. A SIGTERM-interrupted turn is\
left as is on resume unless `CLAUDE_CODE_RESUME_INTERRUPTED_TURN=1` [read: headless.md "Stop a run with SIGTERM"].\
Background sessions: `claude --bg` starts a detached session (not combinable with `-p`) and prints an id;\
`claude agents`, `attach`, `logs`, `stop`, `respawn`, `rm` manage them; `--resume <id> --bg` continues one in the\
background [read: help; headless.md "Basic usage"; agent-view.md]. Scheduling independent of any open session: cloud\
and Desktop scheduled tasks, `/loop` on an interval [read: goal.md "See also"; scheduled-tasks.md].

### 3. Persistence of guidance during a long run

- **Instruction file (CLAUDE.md).** Survives compaction: the project-root CLAUDE.md and unscoped rules are "Re-injected\
  from disk", as is auto memory. Nested CLAUDE.md files and `paths:` rules reload on demand and are summarized away\
  until then [read: context-window.md "What survives compaction"; memory.md "Instructions seem lost after /compact"].\
  Under `-p` CLAUDE.md loads as in an interactive session unless `--bare` or `--safe-mode` is set\
  [read: headless.md; help].
- **Loaded skill.** The rendered `SKILL.md` stays in the conversation as one message and is not re-read on later turns\
  [read: skills.md "Skill content lifecycle"]. After compaction invoked skill bodies are re-injected, capped at 5,000\
  tokens per skill and 25,000 tokens in total, most recent first, so an old skill can drop out; skill descriptions are\
  rebuilt and re-sent (v2.1.304) [read: context-window.md table; skills.md; CHANGELOG.md 2.1.304]. Truncation keeps the\
  start of the file [read: context-window.md].
- **System prompt.** `--system-prompt-snapshot on` (default) records the system prompt, including\
  `--append-system-prompt` text, on the first request and reuses that record on every request and resume until the\
  conversation is compacted, even when a later launch passes different text [read: help].
- **Goal text.** It sits in the session Stop hook and in `AppState.activeGoal`, not in the model's context\
  \[read: module 309797481, `L7e` adds the hook and `activeGoal`\]. Compaction does not appear to touch either\
  [inferred: no compaction path reads them]. After compaction the model sees the condition again only in the next\
  `Stop hook feedback` message (with the 500 character cut when the transcript still holds the condition), or by\
  calling `GetGoal`, which is gated off by default and in `-p` [read for each piece; the combined effect is inferred].\
  Whether a resume after a compaction still finds the `goal_status` attachment that restores the goal is [live].
- **Each continuation turn.** The Stop hook re-runs every main-thread turn end; the feedback carries\
  `[<condition>]: <reason>`, which both restates the condition and gives the evaluator's missing evidence\
  [read: module 315497248].
- Other items: idle compaction (summarizes a 200K+ token conversation idle for about 54 minutes) exists since 2.1.299\
  and can be switched off with `"idleCompaction": false` [read: CHANGELOG.md 2.1.299].

### 4. Talking to an absent user

- **Blocked question in an interactive or background session.** `AskUserQuestion` waits until answered. The optional\
  `askUserQuestionTimeout` (60s, 5m or 10m) closes it, submits any selected options, and tells the model the user may\
  be away so it proceeds on its own judgment; the timer never starts in a background session or under Remote Control\
  [read: tools-reference.md "AskUserQuestion tool behavior"]. Its tool prompt says to use it only when "blocked on a\
  decision that is genuinely the user's to make" [read: module 313338171]. Permission prompts never auto-resolve on\
  idle [read: tools-reference.md].
- **In `-p`.** There is no person to answer. Calls needing approval are denied; with `--permission-prompts none` the\
  model is told nobody can approve and `AskUserQuestion` is removed; an unanswered MCP elicitation is cancelled\
  [read: headless.md]. Whether `AskUserQuestion` is listed in a plain `-p` run without that flag was not read; the\
  denial is [inferred] from the host-less permission rule.
- **Goal-specific.** `PauseGoal` is the built-in "record a blocker and stop pushing" channel, but it is\
  interactive-only and flag-gated (section 1). A paused goal shows "Goal paused · send a message to continue" with the\
  model's reason [read: module 345407478].
- **Notify.** `PushNotification` sends a desktop notification locally and a phone push with Remote Control or in a\
  cloud session [read: tools-reference.md]. Settings `agentPushNotifEnabled`, `inputNeededNotifEnabled`,\
  `preferredNotifChannel` control them [read: settings-reference.md index]. `Notification` hooks fire for\
  `permission_prompt` (after about six seconds), `idle_prompt` (about 60 seconds after a response), `agent_needs_input`\
  and `agent_completed` (only while agent view is open), and usage-limit events [read: hooks.md "Notification"].\
  `--brief` turns on `SendUserMessage`, "which Claude uses to message you"\
  [read: help; where the message goes in a headless run is unverified].
- **Agent view.** Background sessions waiting for an answer show as "Needs input" with the exact question; a reply from\
  the peek panel answers a question, but permission dialogs need attaching\
  [read: agent-view.md "Read session state", "Peek and reply"].
- **Hooks as the place to put it.** A `Stop` or `Notification` hook can run a script when a goal run stops or waits\
  \[read: hooks.md; the use for a goal run is [inferred]\].

### 5. Subagents during a goal run

- A non-fork subagent starts with a fresh context: its own system prompt, the delegation message, the CLAUDE.md\
  hierarchy (including `AGENTS.md` loaded as project instructions), a git status snapshot, and skills named in its\
  `skills` field. It does not see the conversation, the skills already invoked, or the goal\
  [read: sub-agents.md "What loads at startup"]. Explore and Plan skip CLAUDE.md and git status; `omitClaudeMd: true`\
  drops CLAUDE.md for a custom subagent [read: sub-agents.md].
- A fork inherits the whole history, system prompt and tools, so it sees the kickoff message that states the goal\
  condition\
  \[read: sub-agents.md "How forks differ from other subagents"; that the kickoff sits in the inherited history is [inferred]\].
- The goal evaluator never runs for a subagent: the goal runner returns early when `e.agentId` is set, and `SetGoal`,\
  `GetGoal` and `PauseGoal` throw in agent contexts\
  \[read: module 325815919 `if(e.agentId||fo(r)!=="main")return`; modules 345395031, 345416313, 345407478\]. A running\
  subagent or background shell defers the main goal's evaluation to a later turn\
  [read: goal.md "Background work defers evaluation"].
- Consequence: a delegation brief has to restate the success criterion a subagent is responsible for [inferred].

## Oh-My-Pi 18.22.0

### 1. Goal loop now

**Setting a goal.** Interactive slash commands: `/goal [text]` toggles or sets, with subcommands `set <objective>`,\
`show`, `pause`, `resume`, `drop`, `budget`; `/guided-goal` has the agent interview the user, then call `goal create`\
\[read: `src/slash-commands/builtin-modes.ts:335-368`; `src/modes/interactive-mode.ts:651-653`\]. Launch flag\
`--goal <objective>` starts a fresh interactive session in goal mode; it is rejected with `--print` or `--mode`, with\
any resume, continue, fork or import flag, with a positional message, `@file` or stdin, with `--plan-yolo` or\
`--no-tools`, with startup plan mode, and when `goal.enabled` is off \[read: help; `src/cli/args.ts:145-205`\]. RPC hosts\
send `{type:"goal", op:"get|create|resume|pause|drop", objective?, token_budget?}`\
\[read: docs: rpc.md "Command Schema" and "`goal` payload"; `src/modes/rpc/rpc-goal.ts:20-26`\]. Goal mode and plan mode\
exclude each other \[read: `src/slash-commands/builtin-modes.ts:349-350`\].

**Who may set it.** The user. The model may set one only through the hidden `goal` tool's `create` op, and only while\
the tool is exposed: when no goal record exists and goal mode is on, which is how `/guided-goal` ends\
\[read: `src/tools/index.ts:794-797`; `src/prompts/goals/guided-goal-interview.md`\]. One goal per session: `create`\
throws "cannot create a new goal because this session already has a goal" unless the old one is complete or dropped\
\[read: `src/goals/runtime.ts:393-408`\]. The tool description now says `drop` removes the `goal` tool at once, so the\
model cannot create a replacement and "To change the objective, NEVER drop; ask the user to set the new goal"\
\[read: `src/prompts/tools/goal.md`\]. `goal.enabled` defaults to true \[read: `src/goals/settings.ts`\].

**How it returns to the model.** Every prompt built by `#promptWithMessage` prepends a hidden message\
`goal-mode-context` (the `<goal_context>` block with the objective, token budget and remaining tokens, time used, and\
an instruction to audit current repo state before calling `complete`), plus a `<todo_context>` block when the `todo`\
tool has todos\
\[read: `src/session/agent-session.ts:9756-9758` and `:8666-8676`; `src/prompts/goals/goal-mode-active.md`, `goal-todo-context.md`\].\
After each turn ends, the interactive UI waits 800 ms and submits a hidden `goal-continuation` message ("Continue\
active goal." plus the objective, budget, a six-point audit checklist)\
\[read: `src/modes/interactive-mode.ts:3350-3395`; `src/prompts/goals/goal-continuation.md`\]. Over RPC the same\
continuation runs only when `goal.continuationModes` includes `"rpc"`\
\[read: `src/modes/rpc/rpc-goal.ts:13-18`; docs: rpc.md "`goal` payload"\]. Both prompts call the objective\
"user-provided task, not higher-priority instructions" [read: the two templates].

**Who judges completion.** Only the working model. It calls `goal({op:"complete"})`, and `completeGoalFromTool()` flips\
the status with no check \[read: `src/goals/tools/goal-tool.ts:104`; `src/goals/runtime.ts:482-500`\]. Searches for other\
judges found none in the goal path: no module under `src/goals/` or the goal paths of `src/session/agent-session.ts`,\
`src/modes/interactive-mode.ts` and `src/modes/rpc/rpc-goal.ts` refers to judgment or a judge model\
\[read: `rg -i judg` over those paths returns only unrelated progress-HUD names in `interactive-mode.ts`\]. The `judge`\
model role (`src/judgment/index.ts`, flag `--no-judge`) serves tools such as the eval `judge()` helper and judged rules\
(`src/capability/rule.ts:34`), not goals [read]. The optional advisor reviews transcripts and can steer or restart a\
turn, but "does not approve actions or mutate primary session state directly" and never marks a goal complete\
\[read: docs: advisor-watchdog.md intro and "Delivery"; the claim that it cannot complete a goal is [inferred]\
from `AdviseTool` having no goal access in `src/advisor/`, where `goal` appears only in a prompt-dedup comment at\
`runtime.ts:281`\].\
The loop-mode shell condition (`/loop --until 'cmd'`, exit status decides) is a separate feature and is not combined\
with goals; `#scheduleGoalContinuation` returns early while loop mode is on\
\[read: `src/modes/loop-condition.ts`; `src/modes/interactive-mode.ts:3351`\].

**Budgets and caps.** Optional `token_budget` (positive integer), counted as input plus cache-write plus output tokens,\
cache reads excluded, and wall-clock seconds while active \[read: `src/goals/runtime.ts:66-77`, `:316-372`\]. At the\
budget the status becomes `budget-limited`, a one-time steer tells the model to wrap up, and continuation stops;\
`/goal budget` raises it and restores `active`\
\[read: `src/goals/runtime.ts:283-312`; `src/prompts/goals/goal-budget-limit.md`\]. Continuation stops without any cap on\
turns when a continuation turn repeats the previous turn's tool-call digest or makes no tool calls\
(`goalContinuationActivity`), when the editor holds text, when plan mode is on, or when the goal is not `active`\
\[read: `src/goals/state.ts:50-70`; `src/modes/interactive-mode.ts:3350-3362`, `:5744-5745`\]. Session-level caps also\
apply: `--max-cost <usd>` (print mode exits 3), `--warn-cost`, `--max-time <duration>`\
[read: help; docs: cli-reference.md "Headless / print mode"].

**How it ends.** The model completes it; the user drops or pauses it; Esc (an interrupt) pauses it; a normal session\
resume pauses an active goal until `/goal resume` (the TUI keeps it active across internal session switches); over RPC\
a goal restored at process start is paused until `goal resume`; `abort` stops continuation and pauses the goal\
\[read: `src/goals/runtime.ts:244-300`; `src/modes/interactive-mode.ts:5956-5990`; docs: rpc.md "`goal` payload"\].\
Setting `goal.enabled` false clears the record on resume \[read: `src/modes/interactive-mode.ts:5957-5961`\].

**Changed since 2026-10-04 (18.5.1).**

- Todos can no longer be blocked, so goal continuation no longer stops on a blocked-only todo list, a rule the earlier\
  notes described [read: CHANGELOG.md 18.20.0, "Todo tasks can no longer be blocked"].
- The `goal` tool's `drop` text changed (removes the tool, no replacement) \[read: `src/prompts/tools/goal.md`\].
- The RPC goal controller grew host-abort, session-change and settle handling, documented in rpc.md\
  \[read: `src/modes/rpc/rpc-goal.ts`; docs: rpc.md\].
- Unchanged: the working model is the only judge, the `goal-mode-context` and `goal-continuation` mechanism, the budget\
  accounting, the identical-activity stop, and `goal.continuationModes` default `["interactive"]` [read].

### 2. Unattended operation

**Headless modes.** `-p/--print` processes the prompts and exits, printing the last assistant answer (text mode); stdin\
that is not a TTY selects print mode; `--mode json` emits a session header and JSON-line events; `--mode rpc` and\
`--mode rpc-ui` give a line-delimited JSON command, response and event protocol over stdio; `omp acp` serves the Agent\
Client Protocol [read: docs: cli-reference.md "Headless / print mode", "Output modes"; help]. In print mode terminal\
turn failures give a non-zero exit status and `--max-cost` exits 3 [read: same]. `--wait-async` (or `async.printWake`)\
keeps print mode alive for background jobs and wakes the session with each result; `--max-time` bounds the run; the\
docs say to bound unattended runs with it [read: same]. A goal cannot start in print mode (`--goal` refuses it) and\
`print-mode.ts` has no goal continuation\
\[read: `src/cli/args.ts:146-148`; `rg goal src/modes/print-mode.ts` finds nothing\]. An unattended goal needs either an\
interactive TUI (for example inside a terminal multiplexer, [inferred]) or an RPC host that creates the goal and sets\
`goal.continuationModes` to include `"rpc"` [read: docs: rpc.md].

**Approvals.** `tools.approvalMode` is `always-ask`, `always-ask-cached`, `write` or `yolo`; the default is `yolo`;\
`--approval-mode`, `--auto-approve` and `--yolo` override per session\
\[read: `src/tools/settings.ts:313-317`; docs: approval-mode.md "Modes"\]. User policies `tools.approval.<tool>` (allow,\
deny, prompt) and `tools.restrictedFolders` (always prompt, even in yolo) apply; a call that must prompt fails when no\
UI exists, and restricted-folder calls are refused without a UI\
[read: docs: approval-mode.md "Restricted folders", "User overrides"]. The `goal` tool is `read` tier for `get` and\
`write` tier otherwise, so a stricter mode prompts for `complete` \[read: `src/goals/tools/goal-tool.ts:65-66`\]. Task\
subagents run headless in yolo [read: docs: approval-mode.md "Subagents"]. `--plan-yolo` auto-approves the plan in\
print mode [read: help; docs: cli-reference.md].

**Sandboxing.** No process or filesystem sandbox. The docs say bash pattern rules are not containment ("An approved\
command retains the shell's ambient filesystem, network, and subprocess access") and that extensions and browser tools\
are not sandboxed [read: docs: approval-mode.md "Safety overrides"; extension-loading.md; tools/browser.md].\
`--offline`, `--no-judge` and `--no-spotlight` only restrict auxiliary model services to the active provider\
[read: help]. Isolated subagent checkouts (`isolation.backend`, ovnfs) separate working copies, not privileges\
[read: docs: settings.md; CHANGELOG.md 18.17.0].

**Continuing later.** `--continue`, `--resume [id]`, `--session-dir`, `--no-session`, `--fork`; `--restore [id]`\
resumes and then continues what a crashed or killed process left unfinished, including its subagents, interactive only\
and without a prompt [read: help; docs: cli-reference.md "Session history"]. A normal resume pauses an active goal\
(section 1); a continued print-mode run can take a new prompt, as in `omp --continue "..."`\
[read: docs: cli-reference.md examples]. `omp session` packs a session for another machine [read: help].

### 3. Persistence of guidance during a long run

- **Instruction file.** `AGENTS.md` and other context files are rendered into the trailing `<project-context>` block of\
  the system prompt, which is rebuilt rather than part of the compactable history\
  [read: docs: context-files.md "Discovered context files ..."; system-prompt-customization.md]. `RULES.md` is "an\
  always-apply rule" whose full body is carried on every request [read: docs: context-files.md]. That compaction cannot\
  remove either is [inferred] from the system prompt being outside the message history.
- **Loaded skill.** Skills appear in the system prompt as name and description; a body enters the context through the\
  `read` tool on `skill://name` or through `/skill:name`, which injects it as a custom message\
  [read: docs: skills.md "System prompt exposure", "Interactive /skill commands"]. Tool-output pruning never prunes\
  `skill` tool results or `read` results of `skill://` paths [read: docs: compaction.md, default prune policy].\
  Compaction itself can still summarize the body away; no re-injection of a loaded skill body was found [inferred].
- **Goal text.** The goal state lives in the session (`mode_change` entries and `#goalModeState`), not in the message\
  history. `#promptWithMessage` rebuilds and prepends `goal-mode-context` on every prompt, and the post-compaction\
  auto-continue prompt goes through `#promptWithMessage` too, so the goal returns after compaction and on every\
  continuation turn \[read: `src/session/agent-session.ts:2835-2850`, `:5738-5780`, `:9756-9758`\]. A compaction in the\
  middle of a single long turn is not followed by a re-injection until the next prompt, which is [inferred] from the\
  prepend happening only at prompt build; mid-run compaction logs `goalActive` but does not rebuild the message\
  \[read: `src/session/session-maintenance.ts:3052`\].
- **Todo state** is also re-injected with the goal while todos exist\
  \[read: `src/prompts/goals/goal-todo-context.md`; `src/session/agent-session.ts:8666-8676`\].
- **After compaction** the "auto-continue" prompt says only "Resume the user's latest intent. Re-read kept recent\
  messages above the summary" \[read: `src/prompts/system/auto-continue.md`\].

### 4. Talking to an absent user

- **The `ask` tool exists only when a person can answer.** `AskTool.createIf` requires `canPromptUser ?? hasUI`;\
  `hasUI` is `isInteractive || mode === "rpc-ui"`, so print, json and plain rpc sessions never get it\
  \[read: `src/tools/ask.ts:378`; `src/main.ts:2409`\]. If a headless session still reaches it, it aborts the context\
  with "Ask tool requires interactive mode" \[read: `src/tools/ask.ts:445-450`\]. A headless fork (`/tan`) instead\
  receives text telling it to "finish with your final answer and put each open question there with its options and your\
  recommendation" \[read: `src/prompts/tools/ask-headless-fork.md`\].
- **In the TUI,** `ask` shows an HTML form. `ask.timeout` defaults to 0 (no timeout); a non-zero value submits the\
  form's current, preselected values and sets `timedOut`; plan mode always disables the timeout\
  \[read: docs: tools/ask.md "Limits & Caps"; `src/modes/settings.ts` `cfgAskTimeout`\]. `ask.notify` (default on) sends\
  a terminal notification "Waiting for input"; `completion.notify` (default on) notifies when a turn finishes;\
  `error.notify` (default off) notifies on an error stop\
  \[read: `src/modes/settings.ts:1416-1485`; docs: tools/ask.md "Side Effects"\].
- **Recap and hubs.** `recap.enabled` generates a short recap after the terminal has been idle (default 240 s)\
  \[read: `src/modes/settings.ts` `cfgRecap*`\]. Idle recaps read the goal text\
  \[read: `src/session/idle-maintenance.ts:305-355`\].
- **Blocked-question record.** No built-in tool writes a blocked question to a file or sends it out; the budget steer\
  and the continuation prompt tell the model to leave "the user a clear next step" and "stop turn; user or runtime\
  decides next steps" in its reply \[read: `src/prompts/goals/goal-budget-limit.md`, `goal-continuation.md`\]. The\
  `guided-goal` template's "Stop conditions" section asks the user to name when to halt and surface to a human, but the\
  harness does not enforce it \[read: `src/prompts/goals/guided-goal-interview.md`\].
- **In `-p`** with `--wait-async`, background results can wake the session; nothing waits for a person\
  [read: docs: cli-reference.md].

### 5. Subagents during a goal run

- A task subagent is its own `AgentSession` with its own goal state, which is unset, and the `goal` tool is not in its\
  tool set unless goal mode is active in that session\
  \[read: `src/tools/index.ts:684-690`, `:794-797`; `src/sdk.ts:2758-2759`, session-scoped getters\]. The `task` tool\
  prompt asks the caller to put shared `# Goal` text in the batch `context`, and the call fails with "Missing\
  `context`" when it is absent \[read: `src/prompts/tools/task.md:35`; `src/task/index.ts:324`\].
- Task subagents drop every context file whose basename is `AGENTS.md`, including the user-level one, but keep\
  `CLAUDE.md`, `RULES.md` and MCP tools\
  [read: docs: system-prompt-customization.md "Inputs by session type"; context-files.md]. A helper that must follow a\
  rule needs it in `RULES.md` or in the task text [read: docs: context-files.md].
- Subagents receive the session's discovered skill list (names and descriptions) through normal session creation, with\
  no per-task pinning; an agent definition can auto-inject skill bodies with the `autoloadSkills` frontmatter field\
  [read: docs: skills.md lines on "Task tool subagents" and the autoload format].
- Subagent token spend and the goal budget: whether subagent tokens count toward `tokensUsed` was not traced\
  (`#goalUsage` reads the session's own totals, `src/session/agent-session.ts:15431`) [inferred: own session only]. A\
  cost cap set on the main thread applies to running subagents [read: CHANGELOG.md 18.17.0].
- Live confirmation that a subagent spawned during goal mode receives no `goal-mode-context` is [live]; the code path\
  above gives no way for it to.
