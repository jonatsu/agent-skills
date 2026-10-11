# ATTRIBUTIONS.md Repair Ledger

Temporary. Tracks rewriting every `ATTRIBUTIONS.md` outside `archived/` to the scheme in
`skills-for-skills/skill-forge/references/provenance.md`. Delete this file when every row is done and the
structural check has landed.

Steps:

1. Scheme: `provenance.md`, `assets/ATTRIBUTIONS.template.md`, `authoring.md`, and `AGENTS.md`. Status: done.
2. Worked examples: `buildroot-development` and `yocto-openembedded-development`, by the main session. Status:
   done.
3. The remaining files, by Sonnet subagents at most two at a time, each reviewed before commit.
4. A structural check under `checks/` that enforces the scheme, enabled once every row is done.
5. The documentation flaw patterns found here, written as general documentation guidelines in `AGENTS.md` or a
   shared rules file, proposed to the user before placing. The repair of other documentation follows later.

Status is `pending`, `done`, or `blocked`. A blocked row names what it waits on.

| Skill                                           | Lines before | Status  | Notes          |
| ----------------------------------------------- | ------------ | ------- | -------------- |
| `agents/agents-context-docs`                    | 97           | done    |                |
| `agents/cc-safety-net`                          | 57           | done    |                |
| `agents/context-architecture`                   | 53           | done    |                |
| `agents/context-compression`                    | 52           | done    |                |
| `agents/dispatching-subagents`                  | 50           | done    |                |
| `agents/document-conversion`                    | 107          | done    |                |
| `agents/note-for-later`                         | 25           | done    |                |
| `agents/prompt-debugging`                       | 57           | done    |                |
| `agents/session-handoff`                        | 62           | done    |                |
| `agents/writing-prompts`                        | 49           | done    |                |
| `claude/session-reflect`                        | 49           | done    |                |
| `code-health/brooks-audit`                      | 42           | pending |                |
| `code-health/brooks-debt`                       | 42           | pending |                |
| `code-health/brooks-health`                     | 42           | pending |                |
| `code-health/brooks-review`                     | 42           | pending |                |
| `code-health/brooks-sweep`                      | 42           | pending |                |
| `code-health/brooks-test`                       | 42           | pending |                |
| `development/bash-shell`                        | 22           | pending |                |
| `development/coding-standards`                  | 44           | pending |                |
| `development/docker-podman-containers`          | 58           | pending |                |
| `development/posix-shell`                       | 15           | pending |                |
| `development/python/python-architecture`        | 55           | pending |                |
| `development/python/python-async-patterns`      | 87           | pending |                |
| `development/python/python-error-handling`      | 63           | pending |                |
| `development/python/python-parallelism`         | 57           | pending |                |
| `development/python/python-project-management`  | 79           | pending |                |
| `development/python/python-style`               | 33           | pending |                |
| `development/python/python-testing`             | 73           | pending |                |
| `development/python/python-typing`              | 62           | pending |                |
| `embedded-debugging/debug-hardware`             | 24           | pending |                |
| `embedded-debugging/debug-server-tools`         | 31           | pending |                |
| `embedded-debugging/embedded-linux-debugging`   | 38           | pending |                |
| `embedded-debugging/gdb-debugging`              | 30           | pending |                |
| `embedded-debugging/mcu-firmware-debugging`     | 24           | pending |                |
| `embedded-debugging/serial-console-debugging`   | 21           | pending |                |
| `embedded-linux/buildroot-development`          | 69           | done    | Worked example |
| `embedded-linux/embedded-linux-bringup`         | 112          | done    |                |
| `embedded-linux/kas-build-orchestration`        | 111          | done    |                |
| `embedded-linux/u-boot-development`             | 82           | done    |                |
| `embedded-linux/yocto-openembedded-development` | 155          | done    | Worked example |
| `embedded-linux/yocto-security-audit`           | 97           | done    |                |
| `embedded-linux/yocto-security-hardening`       | 163          | done    |                |
| `embedded-linux/yocto-vulnerability-management` | 126          | done    |                |
| `engineering/define-goal`                       | 40           | pending |                |
| `engineering/domain-modeling`                   | 48           | pending |                |
| `engineering/idea-brainstorming`                | 93           | pending |                |
| `engineering/implementation-planning`           | 93           | pending |                |
| `engineering/incremental-implementation`        | 14           | pending |                |
| `engineering/interview-me`                      | 52           | pending |                |
| `engineering/technical-design`                  | 86           | pending |                |
| `engineering/to-questionnaire`                  | 44           | pending |                |
| `engineering/writing-specs`                     | 40           | pending |                |
| `review/conformance-review`                     | 43           | pending |                |
| `review/security-review`                        | 93           | pending |                |
| `skills-for-skills/skill-forge`                 | 263          | pending |                |
| `skills-for-skills/writing-skill-descriptions`  | 54           | pending |                |
| `technical-writing/drawio-diagrams`             | 55           | pending |                |
| `technical-writing/writing-documentation`       | 200          | pending |                |
| `technical-writing/writing-for-humans`          | 120          | pending |                |
| `technical-writing/writing-readmes`             | 34           | pending |                |
| `testing-and-qa/systematic-debugging`           | 31           | pending |                |
| `testing-and-qa/test-driven-development`        | 19           | pending |                |
| `testing-and-qa/test-engineer`                  | 56           | pending |                |
| `tools/ast-grep`                                | 70           | pending |                |
| `tools/chezmoi-dotfiles`                        | 33           | pending |                |
| `tools/git-commits-and-recovery`                | 81           | pending |                |
| `tools/just-task-runner`                        | 23           | pending |                |
| `tools/lint-config-audit`                       | 27           | pending |                |
| `tools/mise-tools`                              | 28           | pending |                |
| `tools/repo-management`                         | 66           | pending |                |
| `tools/using-git-worktrees`                     | 50           | pending |                |
