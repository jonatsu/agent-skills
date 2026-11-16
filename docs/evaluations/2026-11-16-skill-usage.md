# Evaluation: Skill Usage Since the October Renaming

Date: 2026-11-16. The question was which deployed skills Claude Code actually loads, now that a month of
sessions has accumulated under the current skill names. The earlier measurement of 2026-09-08 was unusable,
because the set had just been renamed and every counter had reset.

## Verdict

Of the 93 skills deployed to Claude Code, 63 loaded at least once between 2026-10-08 and 2026-11-16, across
1,245 transcripts. Five direct-tier skills, which every session lists with their full description, never
loaded: `context-compression`, `domain-modeling`, `git-history-investigation`, `github-ops`, and
`writing-specs`. Twenty-five lazy skills never loaded either; most cover embedded and Yocto work, the `brooks`
code-health set, or skills added this week. `test-engineer` loaded only when the user typed its name, never on
an agent's own choice, while `python-testing` loaded 21 times.

## Method

The counts cover Claude Code on one machine. Every transcript under `~/.config/claude/projects/` changed since
2026-10-08 was read, and only records dated on or after that day were counted:

- **Agent loads:** `Skill` tool calls in a main session's transcript.
- **Subagent loads:** `Skill` tool calls in a transcript under a `subagents/` folder.
- **Typed by user:** a slash command naming the skill in a user message.

A plugin prefix such as `plugin:skill` was dropped, so each skill counts under its own name. The tier comes from
agent-setup's `skills/kasetto/base.yaml`, where every listed skill is direct and every other skill is lazy. The
deployed set comes from agent-setup's `skills/kasetto/claude/kasetto.lock`. Transcripts are kept for 90 days,
and the oldest dates from 2026-09-04, so none in the window was pruned.

`skillUsage.lastUsedAt` in `.claude.json` mostly agrees with the transcripts, which are the evidence here. Three
skills (`embedded-linux-bringup`, `serial-console-debugging`, `yocto-security-hardening`) carry a date after
2026-10-08 although no transcript loads them; the transcripts show them only being edited or reviewed. Two
skills (`brooks-audit`, `test-engineer`) load in transcripts without a recent date there.

A load shows that a skill reached the agent, not that it helped or that the request needed it. A zero for a
direct skill therefore means either that no request needed it or that its description failed to trigger; this
count cannot tell the two apart.

## Results

The table lists unused skills first, then the rest by total loads. "Own" means `jonatsu/agent-skills`.

| Skill                            | Source                   | Tier   | Agent loads | Subagent loads | Typed by user | Last use   | Class          |
| -------------------------------- | ------------------------ | ------ | ----------- | -------------- | ------------- | ---------- | -------------- |
| `coding-standards`               | own                      | direct | 14          | 28             | 47            | 2026-11-16 | used           |
| `python-style`                   | own                      | lazy   | 35          | 41             | 0             | 2026-11-16 | used           |
| `git-commits-and-recovery`       | own                      | direct | 58          | 6              | 0             | 2026-11-15 | used           |
| `bash-shell`                     | own                      | direct | 44          | 13             | 0             | 2026-11-15 | used           |
| `conformance-review`             | own                      | lazy   | 1           | 45             | 0             | 2026-11-13 | used           |
| `technical-design`               | own                      | direct | 14          | 3              | 29            | 2026-11-16 | used           |
| `rust-testing`                   | own                      | lazy   | 2           | 40             | 0             | 2026-11-14 | used           |
| `writing-prompts`                | own                      | direct | 42          | 0              | 0             | 2026-11-15 | used           |
| `rust-style`                     | own                      | lazy   | 4           | 35             | 0             | 2026-11-13 | used           |
| `security-review`                | own                      | lazy   | 0           | 2              | 37            | 2026-11-16 | used           |
| `skill-forge`                    | own                      | lazy   | 16          | 23             | 0             | 2026-11-16 | used           |
| `define-goal`                    | own                      | direct | 36          | 0              | 0             | 2026-11-15 | used           |
| `writing-for-agents`             | mattpocock/skills        | direct | 23          | 11             | 0             | 2026-11-16 | used           |
| `brooks-audit`                   | own                      | lazy   | 0           | 0              | 29            | 2026-09-15 | used           |
| `rust-error-handling`            | own                      | lazy   | 1           | 28             | 0             | 2026-11-13 | used           |
| `cli-ui-ux`                      | own                      | lazy   | 8           | 15             | 5             | 2026-11-16 | used           |
| `note-for-later`                 | own                      | direct | 21          | 0              | 4             | 2026-11-16 | used           |
| `writing-documentation`          | own                      | direct | 14          | 10             | 0             | 2026-11-16 | used           |
| `test-driven-development`        | own                      | lazy   | 2           | 15             | 6             | 2026-11-13 | used           |
| `interview-me`                   | own                      | direct | 22          | 0              | 0             | 2026-11-16 | used           |
| `python-testing`                 | own                      | lazy   | 12          | 9              | 0             | 2026-11-16 | used           |
| `implementation-planning`        | own                      | direct | 18          | 1              | 0             | 2026-11-14 | used           |
| `posix-shell`                    | own                      | direct | 13          | 6              | 0             | 2026-11-15 | used           |
| `rust-unix-processes`            | own                      | lazy   | 2           | 17             | 0             | 2026-11-13 | used           |
| `writing-skill-descriptions`     | own                      | lazy   | 8           | 10             | 0             | 2026-11-16 | used           |
| `nix-flakes`                     | own                      | lazy   | 11          | 6              | 0             | 2026-11-16 | used           |
| `chezmoi-dotfiles`               | own                      | lazy   | 14          | 2              | 0             | 2026-11-07 | used           |
| `rust-async`                     | own                      | lazy   | 2           | 14             | 0             | 2026-11-13 | used           |
| `writing-for-humans`             | own                      | direct | 5           | 10             | 0             | 2026-11-16 | used           |
| `yocto-openembedded-development` | own                      | lazy   | 15          | 0              | 0             | 2026-11-11 | used           |
| `docker-podman-containers`       | own                      | lazy   | 6           | 6              | 0             | 2026-11-16 | used           |
| `dispatching-subagents`          | own                      | direct | 10          | 0              | 0             | 2026-11-15 | used           |
| `agents-context-docs`            | own                      | direct | 7           | 1              | 0             | 2026-11-15 | used           |
| `home-manager`                   | own                      | lazy   | 8           | 0              | 0             | 2026-11-07 | used           |
| `python-error-handling`          | own                      | lazy   | 2           | 5              | 0             | 2026-11-16 | used           |
| `python-typing`                  | own                      | lazy   | 0           | 7              | 0             | 2026-11-16 | used           |
| `systematic-debugging`           | own                      | lazy   | 3           | 0              | 4             | 2026-11-09 | used           |
| `systemd-units`                  | own                      | lazy   | 6           | 1              | 0             | 2026-11-15 | used           |
| `kasetto-skill-tool`             | own                      | lazy   | 6           | 0              | 0             | 2026-11-02 | used           |
| `mise-tools`                     | own                      | lazy   | 6           | 0              | 0             | 2026-11-16 | used           |
| `test-engineer`                  | own                      | lazy   | 0           | 0              | 6             | 2026-09-14 | used           |
| `cc-safety-net`                  | own                      | lazy   | 4           | 1              | 0             | 2026-10-27 | used           |
| `just-task-runner`               | own                      | lazy   | 3           | 2              | 0             | 2026-11-16 | used           |
| `repo-management`                | own                      | direct | 5           | 0              | 0             | 2026-11-15 | used           |
| `context-architecture`           | own                      | direct | 3           | 1              | 0             | 2026-11-09 | used           |
| `idea-brainstorming`             | own                      | direct | 4           | 0              | 0             | 2026-11-10 | used           |
| `kas-build-orchestration`        | own                      | lazy   | 4           | 0              | 0             | 2026-11-02 | used           |
| `writing-readmes`                | own                      | direct | 4           | 0              | 0             | 2026-11-07 | used           |
| `direnv-nix-direnv`              | own                      | lazy   | 2           | 1              | 0             | 2026-11-10 | used           |
| `nix-packaging`                  | own                      | lazy   | 3           | 0              | 0             | 2026-11-11 | used           |
| `session-handoff`                | own                      | direct | 3           | 0              | 0             | 2026-10-12 | used           |
| `u-boot-development`             | own                      | lazy   | 3           | 0              | 0             | 2026-11-02 | used           |
| `document-conversion`            | own                      | lazy   | 2           | 0              | 0             | 2026-10-29 | used           |
| `incremental-implementation`     | own                      | direct | 2           | 0              | 0             | 2026-11-09 | used           |
| `python-architecture`            | own                      | lazy   | 1           | 1              | 0             | 2026-11-16 | used           |
| `python-async-patterns`          | own                      | lazy   | 2           | 0              | 0             | 2026-10-09 | used           |
| `python-project-management`      | own                      | lazy   | 1           | 1              | 0             | 2026-11-16 | used           |
| `apt-fetch-emulation`            | own                      | lazy   | 0           | 1              | 0             | 2026-10-16 | used           |
| `ast-grep`                       | own                      | direct | 0           | 1              | 0             | 2026-10-24 | used           |
| `gdb-debugging`                  | own                      | lazy   | 1           | 0              | 0             | 2026-10-12 | used           |
| `nixos-config`                   | own                      | lazy   | 1           | 0              | 0             | 2026-10-13 | used           |
| `session-reflect`                | own                      | direct | 1           | 0              | 0             | 2026-11-10 | used           |
| `using-git-worktrees`            | own                      | direct | 1           | 0              | 0             | 2026-10-24 | used           |
| `context-compression`            | own                      | direct | 0           | 0              | 0             | never      | direct, unused |
| `domain-modeling`                | own                      | direct | 0           | 0              | 0             | 2026-09-27 | direct, unused |
| `git-history-investigation`      | own                      | direct | 0           | 0              | 0             | never      | direct, unused |
| `github-ops`                     | own                      | direct | 0           | 0              | 0             | 2026-10-03 | direct, unused |
| `writing-specs`                  | own                      | direct | 0           | 0              | 0             | never      | direct, unused |
| `accessibility`                  | own                      | lazy   | 0           | 0              | 0             | never      | lazy, unused   |
| `brooks-debt`                    | own                      | lazy   | 0           | 0              | 0             | never      | lazy, unused   |
| `brooks-health`                  | own                      | lazy   | 0           | 0              | 0             | never      | lazy, unused   |
| `brooks-review`                  | own                      | lazy   | 0           | 0              | 0             | never      | lazy, unused   |
| `brooks-sweep`                   | own                      | lazy   | 0           | 0              | 0             | never      | lazy, unused   |
| `brooks-test`                    | own                      | lazy   | 0           | 0              | 0             | never      | lazy, unused   |
| `buildroot-development`          | own                      | lazy   | 0           | 0              | 0             | never      | lazy, unused   |
| `debug-hardware`                 | own                      | lazy   | 0           | 0              | 0             | never      | lazy, unused   |
| `debug-server-tools`             | own                      | lazy   | 0           | 0              | 0             | never      | lazy, unused   |
| `drawio-diagrams`                | own                      | lazy   | 0           | 0              | 0             | 2026-10-02 | lazy, unused   |
| `embedded-linux-bringup`         | own                      | lazy   | 0           | 0              | 0             | 2026-10-10 | lazy, unused   |
| `embedded-linux-debugging`       | own                      | lazy   | 0           | 0              | 0             | never      | lazy, unused   |
| `lint-config-audit`              | own                      | lazy   | 0           | 0              | 0             | never      | lazy, unused   |
| `mcu-firmware-debugging`         | own                      | lazy   | 0           | 0              | 0             | never      | lazy, unused   |
| `mermaid-diagrams`               | softaworks/agent-toolkit | lazy   | 0           | 0              | 0             | 2026-09-24 | lazy, unused   |
| `nix-secrets`                    | own                      | lazy   | 0           | 0              | 0             | 2026-07-19 | lazy, unused   |
| `prompt-debugging`               | own                      | lazy   | 0           | 0              | 0             | never      | lazy, unused   |
| `python-parallelism`             | own                      | lazy   | 0           | 0              | 0             | 2026-09-16 | lazy, unused   |
| `serial-console-debugging`       | own                      | lazy   | 0           | 0              | 0             | 2026-10-10 | lazy, unused   |
| `systemd-networking`             | own                      | lazy   | 0           | 0              | 0             | never      | lazy, unused   |
| `to-questionnaire`               | own                      | lazy   | 0           | 0              | 0             | never      | lazy, unused   |
| `usability`                      | own                      | lazy   | 0           | 0              | 0             | never      | lazy, unused   |
| `yocto-security-audit`           | own                      | lazy   | 0           | 0              | 0             | 2026-09-11 | lazy, unused   |
| `yocto-security-hardening`       | own                      | lazy   | 0           | 0              | 0             | 2026-10-19 | lazy, unused   |
| `yocto-vulnerability-management` | own                      | lazy   | 0           | 0              | 0             | 2026-10-06 | lazy, unused   |
