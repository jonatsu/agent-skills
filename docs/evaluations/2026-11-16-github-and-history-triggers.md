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

## Limits

The runs used one client, one model, and subagents rather than main sessions, whose skill listing may differ.
Three runs per request measure a rate only coarsely. The usage record behind this evaluation counts Claude Code
transcripts only, while a tier change in agent-setup also changes what Codex, Copilot, and Oh-My-Pi list.
