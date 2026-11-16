# Evaluation: Do `github-ops` and `git-history-investigation` Trigger?

Date: 2026-11-16. The skill usage record of the same day
([2026-11-16-skill-usage.md](2026-11-16-skill-usage.md)) found that neither skill loaded once in Claude Code
between 2026-10-08 and 2026-11-16, although both sit in the direct tier, listed with their full description in
every session. This evaluation asked whether realistic requests for their work make an agent load them.

## Verdict

`github-ops` loaded on 3 of 9 requests that its description names, below the threshold of half set before the
runs. `git-history-investigation` loaded on none of 6. Neither loaded on a near miss. Every answer was correct
without the skill: the history answers cited their commits from pickaxe and line-log searches, and the GitHub
answers read the API correctly. The control skill, `bash-shell`, did not load on a shell review either, so short
requests a capable agent can answer alone often load no skill at all.

## Method

Claude Code `general-purpose` subagents on Opus ran each request three times, each in a fresh context, with the
repository and GitHub read-only. No brief mentioned skills. A run counted as a trigger when its transcript holds
a `Skill` tool call for the skill. The deployed descriptions were those of agent-skills `44a9050`.

| Request                                                               | Expected skill              | Loaded                             |
| --------------------------------------------------------------------- | --------------------------- | ---------------------------------- |
| Did the latest GitHub Actions run pass, and why not?                  | `github-ops`                | 0 of 3                             |
| Which branch protection or rulesets apply to `main`?                  | `github-ops`                | 2 of 3                             |
| Review two weeks of Actions runs and diagnose each failure            | `github-ops`                | 1 of 3                             |
| Write a CONTRIBUTING paragraph about pull requests and CI (near miss) | none                        | none, 3 of 3                       |
| Who added an `AGENTS.md` rule, in which commit, and was it changed?   | `git-history-investigation` | 0 of 3                             |
| Which commit removed a skill from `main`, and where did its files go? | `git-history-investigation` | 0 of 3                             |
| How do I squash two unpushed commits safely? (near miss)              | `git-commits-and-recovery`  | `git-commits-and-recovery`, 3 of 3 |
| Review a Bash loop for quoting bugs (control)                         | `bash-shell`                | 0 of 3                             |

## Follow-Up: Main Sessions and a Revised `github-ops` Description

A second round tested a candidate description that leads with inspecting and diagnosing and names "whether CI
passed or why a run failed" first. A separate Sonnet subagent wrote the held-out requests from the skill's body
alone, without seeing either description: six substantive GitHub requests, four of them phrased by outcome
without naming `gh`, and three near misses (a local commit move, a pull-request description, a shell review of
the workflow file). Each request ran three times as a headless Claude Code main session on Opus
(`claude -p --no-session-persistence`, read-only tools). The candidate arm temporarily replaced the deployed
description and restored it afterwards.

| Requests                        | Current description  | Candidate description |
| ------------------------------- | -------------------- | --------------------- |
| Six held-out GitHub requests    | 18 of 18             | 18 of 18              |
| Three near misses               | no `github-ops` load | no `github-ops` load  |
| First round: latest run passed? | 0 of 3               | 1 of 3                |
| First round: branch protection  | 3 of 3               | 2 of 3                |
| First round: two weeks of CI    | 3 of 3               | 3 of 3                |

The candidate did no better, so the description stays. The low first-round rate came mostly from the subagent
context: the same three original requests loaded the skill on 6 of 9 runs as main sessions against 3 of 9 as
subagents. A short status question remains the one request shape that rarely loads it, with either wording.

## Limits

The runs used one client and one model. The first round ran as subagents and the follow-up as headless main
sessions, so neither covers an interactive session with earlier conversation in context.
Three runs per request measure a rate only coarsely. The usage record behind this evaluation counts Claude Code
transcripts only, while a tier change in agent-setup also changes what Codex, Copilot, and Oh-My-Pi list.
