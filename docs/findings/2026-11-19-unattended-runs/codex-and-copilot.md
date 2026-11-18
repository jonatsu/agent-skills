Codex CLI 0.169.0 and GitHub Copilot CLI 1.0.114, read on 2026-11-19 without any model call.

# Unattended runs in Codex CLI and Copilot CLI

Every claim carries one of three marks. "Read" means observed at the cited location. "Inferred" means concluded from\
code paths or text without running them. "Unverified" means the reading could not settle it and only a live run can.

## Sources

Codex: the open source at tag `rust-v0.169.0` (commit `d32063f96c2dff1dc96af839b3952abb6acfeda4`) of\
`github.com/openai/codex`; paths below are relative to `codex-rs/`. The tag was compared with `rust-v0.160.0` using\
`git diff`. Help text comes from the installed `codex-cli 0.169.0` (`codex --help`, `codex exec --help`,\
`codex exec resume --help`, `codex queue --help`, `codex features list`). Official pages:\
`https://learn.chatgpt.com/docs/long-running-work`, `https://learn.chatgpt.com/docs/non-interactive-mode` and\
`https://learn.chatgpt.com/docs/reference/slash-commands` (the old `developers.openai.com/codex` addresses redirect\
there).

Copilot: the closed source ships as an executable that unpacks to `~/.cache/copilot/pkg/linux-x64/1.0.114/`. In that\
folder, `cli-main.js` holds the interface, `prebuilds/linux-x64/runtime.node` holds the prompts and the runtime (cited\
as `runtime.node` plus a byte offset; extract with `rg -a -b -o` and `dd`), `changelog.json` holds release notes, and\
`copilot-sdk/generated/*.d.ts` hold the typed session events. Help text comes from `copilot --help` and\
`copilot help config|permissions|limits|sessions|commands|environment`. Official page:\
`https://docs.github.com/en/copilot/concepts/agents/copilot-cli/autopilot`.

---

## Codex CLI 0.169.0

### 1. Goal loop now

How a goal is set, and by whom:

- The user sets it with `/goal <objective>` in the terminal interface; the usage string is\
  `/goal [<objective>|clear|edit|pause|resume]` (read: `tui/src/goal_display.rs:5`; `tui/src/slash_command.rs:143`).\
  Programs set it through the app-server JSON-RPC methods `thread/goal/set`, `thread/goal/get` and `thread/goal/clear`\
  (read: `app-server-protocol/src/protocol/common.rs:651-665`).
- No command-line flag sets a goal. `codex --help` and `codex exec --help` contain no "goal", and `codex features list`\
  shows `goals  stable  true` (read: help output; `codex features list` line 70).
- The model can create a goal with `create_goal`. Its description says to "create a goal only when explicitly requested\
  by the user or system/developer instructions; do not infer goals from ordinary tasks", and `token_budget` is to be\
  omitted "unless explicitly requested" (read: `ext/goal/src/spec.rs:37,46`). The tool fails while an unfinished goal\
  exists (read: `ext/goal/src/tool.rs:236`).
- `update_goal` accepts `complete`, `blocked` and `paused`. It describes `paused` as requiring "an explicit user\
  request", and it limits `blocked` to a condition that has repeated "for at least three consecutive goal turns" (read:\
  `ext/goal/src/spec.rs:66,75-78`). The model cannot resume a goal or set a budget or usage limit status (read:\
  `spec.rs`).

How the goal returns to the model:

- When the thread goes idle while the goal is `active`, the goal extension starts a new turn whose input is the\
  continuation prompt, with trigger `goal` (read: `ext/goal/src/extension.rs:180-196`; `ext/goal/src/runtime.rs:434`).\
  Setting a goal with `/goal` reaches the model the same way (read: 0.160 notes; the code path is unchanged in the\
  diff).
- Since 0.160 the objective text is not in the continuation template. The template now says to "use the current\
  goal_objective context as the task to pursue" and, if it is "missing or truncated", to retrieve it with `get_goal`\
  (read: `ext/goal/templates/goals/continuation.md:3`). The objective travels as an untrusted additional-context entry\
  named `goal_objective` on the turn request (read: `ext/goal/src/steering.rs:57-72`). For a goal the model creates,\
  the same entry is injected into the running turn (read: `ext/goal/src/tool.rs:241-252`).
- That entry reaches the model as a `function_call_output` item named `goal_objective` in namespace `agent`, because\
  the feature `untrusted_as_tool_output` is stable and on (read: `codex features list` line 202;\
  `core/src/state/additional_context.rs:76-84`; `context-fragments/src/additional_context.rs:36-44`). It is cut in the\
  middle at 1,000 tokens (read: `context-fragments/src/additional_context.rs:9,144-147`), and it is sent again only\
  when its value changes or its key was absent from an earlier request (read:\
  `core/src/state/additional_context.rs:51-60,114`). A test shows the first continuation request carries the same item\
  as the request that created the goal (read: `app-server/tests/suite/v2/thread_resume.rs:3950-3965`).
- Goal edits made by the user now enter history as a hidden user-role message `User set the goal: "<json objective>"`\
  or `User cleared the goal.`, and an objective over 700 bytes is replaced by an "omitted" note (read:\
  `core/src/context/user_goal.rs:11,59-118`). The app-server processor records them on every set and clear (read:\
  `app-server/src/request_processors/thread_goal_processor.rs:184-210,299-305`). The automatic approval reviewer treats\
  such a message as user authorization (read: `core/src/agent/control/user_authorization.rs:141`).
- The rest of the continuation prompt is unchanged: a no-progress check, a completion audit that treats completion as\
  unproven until current evidence proves every requirement, and a blocked audit (read: `continuation.md`).

Who judges completion:

- The working model judges, by calling `update_goal` with `complete`; no evaluator model exists (read:\
  `ext/goal/src/tool.rs:272-330`; `continuation.md`, "Completion audit").

Budgets and caps:

- A token budget is optional (read: `spec.rs:37`). The config key `[goals] max_goal_token_budget` caps it and becomes\
  the default (read: `config/src/config_toml.rs:758`). The objective is limited to 4,000 characters (read:\
  `protocol/src/protocol.rs:4500`).
- The runtime sets the goal to `blocked` after three consecutive automatic turns with an empty answer and no activity,\
  after three consecutive goal turns with failed `exec` calls and no success, and after a non-retryable turn error. It\
  sets `usage_limited` on a usage-limit error (read: `ext/goal/src/accounting.rs:172,244-245`;\
  `ext/goal/src/runtime.rs:315-337`). No cap on the number of continuations exists (read: no counter in\
  `continue_if_idle`, `runtime.rs:434-523`).
- Elapsed time is accounted and reported but not enforced (carried from the 0.160 notes; no change in the diff touches\
  it).

How it ends:

- The statuses are `active`, `paused`, `blocked`, `usage_limited`, `budget_limited` and `complete` (read: 0.160 notes,\
  `state` schema; unchanged). The user pauses, resumes, edits or clears with `/goal`. The interface shows `blocked` as\
  "stalled" (read: `tui/src/goal_display.rs:37`).

What changed since the 2026-10-04 notes:

- The objective moved out of the continuation prompt into the deduplicated, truncated `goal_objective` item. This is\
  the largest change.
- User goal set and clear now enter history as authorization evidence. The 0.160 notes found no caller for this; the\
  app-server processor is the caller (read: `thread_goal_processor.rs:202-204,304`).
- An interrupted automatic turn with no activity now counts toward the three-empty-turn block (read: diff of\
  `accounting.rs` and `extension.rs:183-196`).
- The tool descriptions in `spec.rs` and the `create_goal` explicit-request rule are unchanged.

### 2. Unattended operation

- `codex exec` runs one non-interactive session. Flags relevant to unattended work (read: `codex exec --help`):\
  `-s, --sandbox <read-only|workspace-write|danger-full-access>`, `--approve-for-me` (routes approval requests through\
  automatic review with the workspace-write sandbox), `--dangerously-bypass-approvals-and-sandbox`, `--worktree`,\
  `--add-dir`, `--skip-git-repo-check`, `--trust`, `--ephemeral`, `--json`, `-o, --output-last-message`,\
  `--output-schema`, `--ignore-user-config` and `--ignore-rules`. The official page states that `codex exec` defaults\
  to a read-only sandbox and that `--full-auto` is no longer supported (read:\
  `https://learn.chatgpt.com/docs/non-interactive-mode`).
- Headless approval is `never`: "Default to never ask for approvals in headless mode" (read: `exec/src/lib.rs:632`).\
  Interactive `codex` also accepts `-a on-request|never` (read: `codex --help`).
- `codex exec` answers every server-side request that would need a person: it rejects command, file-change and\
  permission approvals, `request_user_input` and dynamic tool calls with "not supported in exec mode", and it cancels\
  MCP elicitations (read: `exec/src/lib.rs:2236-2360`).
- `codex exec` shuts down when its first turn completes, fails or is interrupted (read:\
  `exec/src/event_processor_with_jsonl_output.rs:529-565`). Inferred: automatic goal continuations therefore do not run\
  inside `codex exec`. A forked `exec` thread is created with `defer_goal_continuation` unless ephemeral, which fits\
  that design (read: `exec/src/lib.rs:1196`). With `--ephemeral` the goal tools refuse: "Goal tools require a\
  persistent thread." (read: `ext/goal/src/tool.rs:178`).
- Resuming and continuing later: `codex exec resume [SESSION_ID|--last] [PROMPT]`, `codex exec fork`,\
  `codex resume [--last]`, `codex fork` (read: help output; `https://learn.chatgpt.com/docs/non-interactive-mode`,\
  "Resume a non-interactive session"). `codex exec resume --help` lists no `--sandbox` or `--approve-for-me` flag\
  (read).
- New command `codex queue --thread <id|name> --message <text> [--resume]` queues a user message for an existing\
  session; `--resume` then tries to resume the thread on the local daemon or a remote server (read:\
  `codex queue --help`). The implementation is a "durable, storage-neutral user-message queue and idle dispatch" (read:\
  `ext/queue/src/lib.rs:1`).
- The goal lives in `$CODEX_HOME/goals_1.sqlite`, one row per thread, and resume re-arms goal accounting only for an\
  `active` goal (read: `ext/goal/src/runtime.rs:410-431`). Inferred: a resumed `active` goal starts a continuation once\
  the thread is idle, through `on_thread_idle` (read: `extension.rs:171,196`); a live run would confirm it.
- Inferred: the only route to a goal that runs unattended through several turns is a client of the app-server protocol\
  that calls `thread/goal/set`, or a terminal session left running; `codex exec` can create a goal only if the prompt\
  explicitly instructs `create_goal`, and it then stops after one turn.

### 3. Persistence during a long run

- AGENTS.md survives compaction. It is a world-state section, and compaction re-renders the full world state and\
  inserts it before the last real user message or the summary (read: `core/src/context/world_state/agents_md.rs:17-80`;\
  `core/src/session/world_state.rs:262`; `core/src/compact.rs:84-112,665-710`). A changed AGENTS.md is announced with\
  the notice "These AGENTS.md instructions replace all previously provided AGENTS.md instructions." (read:\
  `agents_md.rs:11-12`).
- The skill catalog starts a fresh listing and budget after compaction (read: `ext/skills/src/catalog_delta.rs:3`). A\
  loaded skill body is a `<skill>` user fragment, which counts as a hidden contextual fragment (read:\
  `core/src/context/contextual_user_message.rs:23-31`). Local compaction keeps only messages that `parse_user_message`\
  accepts, and that function returns nothing for contextual fragments (read: `core/src/event_mapping.rs:114-117`;\
  `core/src/compact.rs:618-633`). Inferred: a loaded skill body is not retained by local compaction. Remote compaction\
  was not traced.
- The goal row lives in SQLite outside the history, so compaction cannot remove it. The text the model sees is another\
  matter. The continuation prompt and the `goal_objective` item are history items, and local compaction drops hidden\
  fragments in the same way (inferred from the lines above). The deduplication store is not reset by compaction (read:\
  no reset in `core/src/compact*.rs` or `core/src/state/session.rs:222-247`). Inferred: after compaction the next\
  continuation may carry the continuation prompt without the objective, and the prompt's own fallback is to call\
  `get_goal`. Unverified: a live run is needed to see whether the item is re-sent.
- Goal edits the user accepts after a compaction snapshot are re-appended after the replacement history (read:\
  `core/src/session/mod.rs:4912-4930`).
- Hook events `PreCompact`, `PostCompact`, `SessionStart`, `Stop` and `SubagentStart` exist (read:\
  `protocol/src/protocol.rs:1822-1837`). Which of them can add model context was not traced.

### 4. Talking to an absent user

- The only built-in record of a blocked question is the goal status `blocked`. The model may set it only after the same\
  blocker has repeated for three consecutive goal turns, and it must not set it "merely because the work is hard, slow,\
  uncertain, incomplete, or would benefit from clarification" (read: `spec.rs:77`; `continuation.md`, "Blocked audit").\
  A blocked goal stops the loop, and the interface shows it as "stalled" (read: `goal_display.rs:37`). The model has no\
  field for a question: the reason goes in its final message.
- Nothing pushes a goal status outward. The notification code mentions no goal (read:\
  `rg -i goal tui/src/chatwidget/notifications.rs` finds nothing). The user can configure `notify`, an external command\
  run with a JSON payload such as `{"type":"agent-turn-complete","turn-id":"12345"}` (read:\
  `core/src/config/mod.rs:818-826`; `hooks/src/legacy_notify.rs:92`), and terminal notifications (read:\
  `tui/src/local_settings_tests.rs:340`).
- `request_user_input` is offered in Plan mode, and in Default mode only when the under-development feature\
  `default_mode_request_user_input` is on (default off) (read: `tools/src/tool_config.rs:5-16`;\
  `features/src/lib.rs:2099-2103`). Under `codex exec` it fails with "not supported in exec mode" (read:\
  `exec/src/lib.rs:2276-2287`).
- The official page says a started goal "keeps the same sandbox and approval policy and pauses when it needs a\
  decision", and that automatic approval reviews let a separate reviewer judge eligible requests (read:\
  `https://learn.chatgpt.com/docs/long-running-work`). Inferred: in a terminal session an approval prompt waits for a\
  person; under `codex exec` the request is rejected and the model sees an error.
- Inferred: a question written as plain assistant text ends the turn with activity, so the automatic continuation fires\
  again; the loop ends only through the blocked audit, the empty-turn block or a budget.

### 5. Subagents during a goal run

- A subagent thread has its own goal row; nothing copies the parent's goal (read: `state` primary key on `thread_id`,\
  0.160 notes; unchanged). Subagent threads get the goal tools except review subagents (read:\
  `ext/goal/src/extension.rs:104-111`). Their token use is added to the root goal (read: `extension.rs:470`;\
  `accounting.rs:305`).
- New finding: `spawn_agent` in multi-agent v2, which is stable and on, forks the parent's full history by default. The\
  tool says `fork_turns` "Defaults to `all`; use `none` to start without parent history" (read:\
  `core/src/tools/handlers/multi_agents_spec.rs:665-668`; `core/src/tools/handlers/multi_agents_v2/spawn.rs:221-226`;\
  `codex features list` line 121). The older tool forks only when `fork_context` is true (read:\
  `multi_agents_spec.rs:627-631`).
- A forked child copies the parent's user, assistant and tool items but drops `ThreadGoalUpdated` events (read:\
  `core/src/agent/history.rs:195-330,374`). Inferred: a default child sees whatever goal text is still in the parent's\
  history, including AGENTS.md and skill fragments, but has no goal state and no instruction to treat the goal as its\
  own; a child spawned with `fork_turns="none"` sees none of it. Which multi-agent version a given session runs was not\
  traced, because the feature list shows `multi_agent` as deprecated and on and `multi_agent_v2` as stable and on.

---

## GitHub Copilot CLI 1.0.114

### 1. Goal loop now

Copilot calls its goal an autopilot objective, and `/goal` is an alias of `/autopilot`.

How a goal is set, and by whom:

- The user sets it with `/autopilot <objective> [--max-ai-credits <N>]` or `/goal`; with no text or with `on` or `off`,\
  the command toggles the mode instead (read: `cli-main.js` slash-command definition with `aliases:["/goal"]`;\
  `copilot help commands`). `copilot --plan --mode autopilot` moves from planning to autopilot without waiting for plan\
  approval (read: `https://docs.github.com/en/copilot/concepts/agents/copilot-cli/autopilot`).
- No flag sets an objective (read: `copilot --help`). The flags are `--autopilot`,\
  `--mode <interactive|plan|autopilot>`, `--max-autopilot-continues <count>` and `--max-ai-credits <credits>`.
- The model cannot set one. The strings `create_goal`, `update_goal` and `get_goal` occur nowhere in `cli-main.js` or\
  `runtime.node` (read: `rg -a -c`). The model's only lever is `task_complete`, which works only in autopilot (read:\
  `runtime.node` offset 24448489, "These task_complete instructions apply only in autopilot mode").
- The SDK exposes `session.autopilotObjective.getState` and `setStayInAutopilot` and the workspace calls that read,\
  write and delete the objective file; no set-objective call appears in the typed definitions (read:\
  `copilot-sdk/generated/rpc.d.ts:10321-10360`; `runtime.node` method names). Unverified: whether\
  `copilot -p "/goal ..."` registers an objective in prompt mode. The official programmatic example is\
  `copilot --autopilot --yolo --max-autopilot-continues 10 -p "<prompt>"` with no objective (read: the autopilot page).

How the goal returns to the model:

- Setting an objective sends a message that begins "The user set this explicit autopilot objective with /autopilot:"\
  and tells the agent to "work autonomously" until the objective is "fully achieved, blocked by a real issue, or the\
  user changes the objective" (read: `runtime.node` offset 9084670). Each continuation, built by\
  `prepareContinuationJson` when the session goes idle, restates "Active autopilot objective:" with the full objective\
  text and says to call `task_complete` only when it is "fully achieved and verified" (read: `runtime.node` offset\
  9277100).
- Without an objective, the continuation is the generic "You have not yet marked the task as complete" message (read:\
  0.91 notes; the continuation machinery is unchanged in the strings). Internal control messages carry "This is an\
  internal autopilot control message, not an end-user request" (read: `runtime.node` string).
- Autopilot mode also has a system block `<autopilot_mode>`: "Decide; don't ask", "Bias to action" and "Verify before\
  claiming success", which names when to call `task_complete`, including when "genuinely blocked" (read: `runtime.node`\
  offset 12759397). Switching mode off sends "Autopilot mode is no longer active. Do not follow autopilot-only\
  instructions from earlier in the conversation." (read: `runtime.node` offset 13965856).

Who judges completion:

- An independent read-only subagent, "Autopilot Completion Review", judges each `task_complete` call under an\
  objective. Its first line must be `VERDICT: PASS`, `FAIL`, `INCONCLUSIVE` or `BLOCKED`. PASS ends the objective, FAIL\
  and INCONCLUSIVE send the worker back for another turn, and BLOCKED pauses the objective and stops autopilot for a\
  human (read: `runtime.node` offset 13435972 and the text following it).
- The reviewer input has the objective, the worker summary and recent tool evidence, and now also a\
  `<visible_assistant_response>` section so the summary may complement a reply the user already saw (read:\
  `runtime.node` offsets 9039733, 9203873).
- The reviewer fails open or closed in three recorded ways: "was unavailable; the completion was accepted", "did not\
  accept this objective after repeated attempts. Accepting the completion so autopilot does not loop", and "could not\
  verify this objective was complete after repeated attempts. Blocking the objective" (read: `runtime.node` offsets\
  25300443, 13439305, 13439515). Three flags gate it, `AUTOPILOT_COMPLETION_REVIEWER`, `..._PLAIN_AUTOPILOT` and\
  `..._STEERING`, each read from a remote experiment service with a static fallback (read: `runtime.node` offset\
  25272384). Unverified: their defaults and the retry count.
- The result of a completion request is `completed`, `continue` or `blocked`, and a blocked result can carry a\
  structured blocker (read: `copilot-sdk/generated/session-events.d.ts:638-644,5363-5436`).

Budgets and caps:

- `--max-ai-credits` is a soft cap with a minimum of 30 credits; the next model call is blocked after it is passed, and\
  the timeline warns near 50, 75 and 90 percent (read: `copilot help limits`). On exhaustion the objective pauses, and\
  `/autopilot --max-ai-credits <N>` resumes it with a fresh window (read: `runtime.node` strings near offset 9273000;\
  `session-events.d.ts:960-961`).
- `--max-autopilot-continues` defaults to 5 and caps "automatic continuations outside an active objective; zero allows\
  none" (read: `runtime.node` offset 10605326). This answers the 2026-10-04 open question: an objective's own\
  continuations are not capped by this flag.
- A run with no tool progress across consecutive continuation turns stops, and an objective is paused with the text\
  "Autopilot paused the objective after repeated turns without successful tool progress. Resume it once the blocker is\
  resolved." (read: `runtime.node` offsets 9275521, 9275787). The stop sits behind the flag\
  `AUTOPILOT_NO_PROGRESS_STOP` (read: `runtime.node` offset 13675667; default unverified). Repeated permission denials\
  stop the run at a "run-wide safety limit" (read: `runtime.node` offset 10796258).

How it ends:

- Objective states are `active`, `paused` and `completed`, with a legacy `cap_reached` (read: `rpc.d.ts:735-742`;\
  `session-events.d.ts:108-116`). A stop emits `session.autopilot_stopped` with a reason such as `task_complete`,\
  `aborted`, `error` or `background_timeout` (read: `session-events.d.ts:2699-2710`). A reviewer BLOCKED ends with\
  "Autopilot stopped: the completion reviewer reported a blocker that requires your input." (read: `runtime.node`\
  offset 9275922). Esc, Ctrl+C and API errors also stop it (read: 0.91 notes).

What changed since the 2026-10-04 notes (these are new to the notes; the product may have behaved this way earlier, and\
the 1.0.91 bundle is no longer installed to compare):

- `--max-autopilot-continues` does not cap an active objective.
- The `<autopilot_mode>` block, the no-progress pause wording and the permission-denial limit are now recorded.
- The reviewer prompt gained `<visible_assistant_response>`, and a blocked completion can carry a structured\
  permission-recovery blocker (read: changelog entries 1.0.106 to 1.0.108; `session-events.d.ts:5440-5477`).
- Release notes since 1.0.91 add: a `preToolUse` hook's "ask" is denied in autopilot (1.0.97); a background autopilot\
  answers `ask_user` itself and the continuation-limit stop is explained (1.0.107); interactive autopilot waits for MCP\
  input and consent (1.0.108); resuming shows the saved paused goal (1.0.107) (read: `changelog.json`).

### 2. Unattended operation

- `copilot -p "<prompt>"` runs non-interactively and exits after completion; add `--autopilot` so the CLI continues\
  after the first turn (read: `copilot --help`; the autopilot page, "Running Autopilot mode programmatically"). Prompt\
  mode ignores `defaultMode` (read: `copilot help config`).
- Approval: `--allow-all` and `--yolo` grant all tools, paths and URLs; `--allow-tool` and `--deny-tool` take rules,\
  and deny wins over every allow. `--allow-all-tools` carries the warning "Non-interactive mode cannot ask, so it\
  denies tool requests that no allow rule (or `--assisted-approval`) approves" (read: `copilot --help`).\
  `--assisted-approval` sends requests to a probabilistic safety judge and is valid only for non-interactive runs\
  (read: `copilot --help`;\
  `https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-programmatic-reference`). In autopilot and\
  `-p` runs, "a tool permission request that would prompt is denied" (read: `copilot help permissions`). Without all\
  permissions, the confirmation dialog warns that requests "will be auto-denied" (read: `cli-main.js`, "Enable\
  autopilot mode").
- Other flags for unattended use: `--max-ai-credits`, `--no-ask-user`, `--silent`, `--output-format json`, `--share`,\
  `--usage-output-file`, `--trust-folder`, `--fleet`, `--enable-memory` (prompt mode starts with memory off) (read:\
  `copilot --help`; `copilot help config`). `COPILOT_TASK_WAIT_TIMEOUT_SECONDS` sets how long `-p`, including\
  `-p --autopilot`, waits for background work, 600 seconds by default (read: `copilot help environment`).
- Resume: `--continue` resumes the latest session, `--resume [id|prefix|name]` a chosen one, and `--session-id` an\
  existing or new one (read: `copilot --help`; `copilot help sessions`). A resumed session keeps its conversation,\
  model, mode and allow-all state (read: `copilot help sessions`). `copilot -p --resume` is supported, and a resumed\
  prompt-mode run compacts an over-threshold history first (read: `changelog.json` 1.0.106, 1.0.110). A session lives\
  in `~/.copilot/session-state/<session-id>/` with `events.jsonl`, `workspace.yaml`, `plan.md`, `session.db`,\
  `checkpoints/` and `files/` (read: `copilot help sessions`). Resuming an autopilot session shows the saved paused\
  goal and how to continue; the way to resume is `/autopilot --max-ai-credits <N>` (read: `changelog.json` 1.0.107;\
  `runtime.node` string near offset 9274000).
- A Stop hook (`hooks.agentStop`) can keep a prompt-mode run going: prompt-mode autopilot "waits for blocked Stop-hook\
  continuations before exiting" (read: `changelog.json` 1.0.107; `runtime.node` hook catalog).

### 3. Persistence during a long run

- Custom instructions (AGENTS.md and related files): `/context` reports "System Prompt, Custom Instructions, System\
  Tools, MCP Tools, Messages, Free Space and Buffer" as separate parts (read: `copilot help commands`). Compaction\
  summarizes the conversation, and "all conversation history will be removed" except the summary (read: `runtime.node`\
  offset 13599158). Inferred: custom instructions sit outside the messages and so survive compaction. A cited mechanism\
  was not found.
- Skills: the prompt lists `<available_skills>` (read: `runtime.node` offset 9035588). Release notes say "Skills remain\
  effective after conversation history is compacted" and "Skill instructions persist correctly across conversation\
  turns" (read: `changelog.json` 0.0.399, 1.0.25). The mechanism was not traced.
- The objective: the full objective text is repeated in every continuation prompt (read: `runtime.node` offset 9277100)\
  and persisted in `autopilot-objective.json` next to `plan.md` (read: 0.91 notes; `runtime.node` workspace calls\
  `readAutopilotObjective`, `writeAutopilotObjective`). A hand-off seed template with `<autopilot_objective>` and\
  `<current_state>` also exists (read: `runtime.node` offsets 9039288-9039339). Inferred: it is used when a fresh\
  context window starts; the trigger was not found.
- The `<autopilot_mode>` instructions: the text "Do not follow autopilot-only instructions from earlier in the\
  conversation" implies they live in conversation history (inferred), but the prompt context also has a key\
  `autopilotAdditionalInstructions` (read: `runtime.node` string), so they may be in the system prompt. Unverified:\
  whether they survive compaction.
- Compaction saves a checkpoint under the session folder, and a `<session_context>` block lists `checkpoints/index.md`\
  so the agent can re-read earlier work (read: `runtime.node` near offset 9032300). The summary has the sections\
  Overview, History, Work Done, Technical Details, Important Files and Next Steps, and `/compact` accepts focus\
  instructions (read: `runtime.node` offsets 13598200-13601500; `changelog.json` 1.0.52).

### 4. Talking to an absent user

- Autopilot answers `ask_user` itself. The runtime replies that "the user is not available to respond and will review\
  your work later", asks the agent to "work autonomously and make good decisions", and says that if the request is\
  "genuinely ambiguous or unresolvable" it should "stop and call task_complete summarizing the ambiguity" (read:\
  `runtime.node` offset 24491362). `copilot help permissions` states the same behavior, and the timeline shows "Making\
  best guess" (read: `copilot help permissions`; `changelog.json` 0.0.422, 1.0.64, 1.0.107).
- So the blocked-question channel is the `task_complete` summary. With the reviewer on, a genuine blocker becomes a\
  `BLOCKED` verdict that pauses the objective, with reviewer findings written as "a work order" for the human (read:\
  `runtime.node` reviewer prompt, offset 13435972). The completion event then carries `outcome: blocked` and a\
  `blocker` with `resumable` set, and permission blockers record attempts and a bound on autonomous retries (read:\
  `session-events.d.ts:5363-5477,616-630`). Autopilot tells the agent "Do not retry or rephrase it; report that\
  progress is blocked." (read: `runtime.node` offset 12704546).
- `--no-ask-user` removes the question form; the agent can still ask in its replies (read: `copilot --help`). Inferred:\
  a question written as plain text ends a turn without `task_complete`, and the continuation message, which says not to\
  stop for open questions, pushes the agent on.
- Interactive autopilot waits for the user on MCP input and consent requests; background autopilot sessions and `-p`\
  runs decline them (read: `copilot help permissions`; `changelog.json` 1.0.108).
- Notification: `notifications` (desktop toasts when attention is needed or the agent finishes), `beep` and\
  `terminalNotifications` default to off (read: `copilot help config`). The hook `notification` fires on system\
  notifications and never blocks (read: `runtime.node` hook catalog). `-p` runs offer the exit code, the JSONL stream\
  and `--share`; a blocked prompt exits non-zero (read: `changelog.json` 1.0.71, 1.0.109).

### 5. Subagents during a goal run

- No code path that hands the objective to an ordinary subagent was found. The objective tag appears in the hand-off\
  seed and in the reviewer input template (read: `runtime.node` offsets 9039288, 9039733). Inferred: ordinary subagents\
  do not see the objective. Unverified without a live run.
- The task tool tells the model "Each agent is stateless - provide complete context in your prompt" (read:\
  `runtime.node` offset 13400495), so a brief must restate what a lane needs.
- Skills can pass to a subagent: the runtime reads "inherited subagent skill" content and reports when "the parent\
  session has no loaded skills" (read: `runtime.node` offset 25177364). Custom instructions have a per-agent skip key,\
  `skipCustomInstructions` (read: `runtime.node` string). Whether a given subagent receives AGENTS.md was not traced.
- Subagents share the parent session's credit limit and honor the parent's tool approvals (read: `copilot help limits`;\
  `changelog.json` 1.0.102). Permission-recovery episodes record the subagent that owns them (read:\
  `session-events.d.ts:5457-5459`).
