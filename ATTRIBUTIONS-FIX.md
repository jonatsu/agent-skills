# ATTRIBUTIONS.md Repair Ledger

Temporary. Tracks rewriting every `ATTRIBUTIONS.md` outside `archived/` to the scheme in
`skills-for-skills/skill-forge/references/provenance.md`. Delete this file when every row is done and the
structural check has landed.

Steps:

1. Scheme: `provenance.md`, `assets/ATTRIBUTIONS.template.md`, `authoring.md`, and `AGENTS.md`. Status: done.
2. Worked examples: `buildroot-development` and `yocto-openembedded-development`, by the main session. Status:
   done.
3. The remaining files, by Sonnet subagents at most two at a time, each reviewed before commit.
   Status: done.
4. A structural check under `checks/` that enforces the scheme, enabled once every row is done.
5. The documentation flaw patterns found here, written as general documentation guidelines in `AGENTS.md` or a
   shared rules file, proposed to the user before placing. The repair of other documentation follows later.

Status is `pending`, `done`, or `blocked`. A blocked row names what it waits on.

| Skill                                           | Lines before | Status | Notes          |
| ----------------------------------------------- | ------------ | ------ | -------------- |
| `agents/agents-context-docs`                    | 97           | done   |                |
| `agents/cc-safety-net`                          | 57           | done   |                |
| `agents/context-architecture`                   | 53           | done   |                |
| `agents/context-compression`                    | 52           | done   |                |
| `agents/dispatching-subagents`                  | 50           | done   |                |
| `agents/document-conversion`                    | 107          | done   |                |
| `agents/note-for-later`                         | 25           | done   |                |
| `agents/prompt-debugging`                       | 57           | done   |                |
| `agents/session-handoff`                        | 62           | done   |                |
| `agents/writing-prompts`                        | 49           | done   |                |
| `claude/session-reflect`                        | 49           | done   |                |
| `code-health/brooks-audit`                      | 42           | done   |                |
| `code-health/brooks-debt`                       | 42           | done   |                |
| `code-health/brooks-health`                     | 42           | done   |                |
| `code-health/brooks-review`                     | 42           | done   |                |
| `code-health/brooks-sweep`                      | 42           | done   |                |
| `code-health/brooks-test`                       | 42           | done   |                |
| `development/bash-shell`                        | 22           | done   |                |
| `development/coding-standards`                  | 44           | done   |                |
| `development/docker-podman-containers`          | 58           | done   |                |
| `development/posix-shell`                       | 15           | done   |                |
| `development/python/python-architecture`        | 55           | done   |                |
| `development/python/python-async-patterns`      | 87           | done   |                |
| `development/python/python-error-handling`      | 63           | done   |                |
| `development/python/python-parallelism`         | 57           | done   |                |
| `development/python/python-project-management`  | 79           | done   |                |
| `development/python/python-style`               | 33           | done   |                |
| `development/python/python-testing`             | 73           | done   |                |
| `development/python/python-typing`              | 62           | done   |                |
| `embedded-debugging/debug-hardware`             | 24           | done   |                |
| `embedded-debugging/debug-server-tools`         | 31           | done   |                |
| `embedded-debugging/embedded-linux-debugging`   | 38           | done   |                |
| `embedded-debugging/gdb-debugging`              | 30           | done   |                |
| `embedded-debugging/mcu-firmware-debugging`     | 24           | done   |                |
| `embedded-debugging/serial-console-debugging`   | 21           | done   |                |
| `embedded-linux/buildroot-development`          | 69           | done   | Worked example |
| `embedded-linux/embedded-linux-bringup`         | 112          | done   |                |
| `embedded-linux/kas-build-orchestration`        | 111          | done   |                |
| `embedded-linux/u-boot-development`             | 82           | done   |                |
| `embedded-linux/yocto-openembedded-development` | 155          | done   | Worked example |
| `embedded-linux/yocto-security-audit`           | 97           | done   |                |
| `embedded-linux/yocto-security-hardening`       | 163          | done   |                |
| `embedded-linux/yocto-vulnerability-management` | 126          | done   |                |
| `engineering/define-goal`                       | 40           | done   |                |
| `engineering/domain-modeling`                   | 48           | done   |                |
| `engineering/idea-brainstorming`                | 93           | done   |                |
| `engineering/implementation-planning`           | 93           | done   |                |
| `engineering/incremental-implementation`        | 14           | done   |                |
| `engineering/interview-me`                      | 52           | done   |                |
| `engineering/technical-design`                  | 86           | done   |                |
| `engineering/to-questionnaire`                  | 44           | done   |                |
| `engineering/writing-specs`                     | 40           | done   |                |
| `review/conformance-review`                     | 43           | done   |                |
| `review/security-review`                        | 93           | done   |                |
| `skills-for-skills/skill-forge`                 | 263          | done   |                |
| `skills-for-skills/writing-skill-descriptions`  | 54           | done   |                |
| `technical-writing/drawio-diagrams`             | 55           | done   |                |
| `technical-writing/writing-documentation`       | 200          | done   |                |
| `technical-writing/writing-for-humans`          | 120          | done   |                |
| `technical-writing/writing-readmes`             | 34           | done   |                |
| `testing-and-qa/systematic-debugging`           | 31           | done   |                |
| `testing-and-qa/test-driven-development`        | 19           | done   |                |
| `testing-and-qa/test-engineer`                  | 56           | done   |                |
| `tools/ast-grep`                                | 70           | done   |                |
| `tools/chezmoi-dotfiles`                        | 33           | done   |                |
| `tools/git-commits-and-recovery`                | 81           | done   |                |
| `tools/just-task-runner`                        | 23           | done   |                |
| `tools/lint-config-audit`                       | 27           | done   |                |
| `tools/mise-tools`                              | 28           | done   |                |
| `tools/repo-management`                         | 66           | done   |                |
| `tools/using-git-worktrees`                     | 50           | done   |                |
