# Oh-My-Pi

The agent directory is `~/.omp/agent`.

## Where things live

- **Memory**: set by `memory.backend` in `~/.omp/agent/config.yml`, which is `off` by default. With `mnemopi`,
  memory is a local database the agent reaches through tools: `retain` saves facts, `recall` and `reflect` read
  them, and `memory_edit` changes or removes one. `mnemopi.scoping` decides where `retain` writes: with
  `per-project-tagged`, to the project's bank by default and to the shared bank with `scope: "global"`. With the
  `local` backend, memory is the `memory://root/MEMORY.md` file instead. When the backend is `off`, route memory
  candidates to instructions.
- **User instructions**: `~/.omp/agent/AGENTS.md` and `~/.omp/agent/RULES.md`. The user `AGENTS.md` shadows the
  other agents' user-level instruction files, and task subagents read `RULES.md` but not `AGENTS.md`, so a rule
  subagents must follow goes in `RULES.md`.
- **Project instructions**: `AGENTS.md` and `RULES.md` in the nearest `.omp/` directory, else an `AGENTS.md` or
  `CLAUDE.md` up to the repository root.
- **Session logs**: JSONL at `~/.omp/agent/sessions/<encoded-cwd>/<timestamp>_<session-id>.jsonl`.

## Writing a memory

Save a cross-repository fact with `retain` and `scope: "global"`, and a repo-specific one with the default
scope. Mnemopi also retains turns on its own, so check with `recall` before saving a fact the session already
stated. Where `learn` is enabled, it saves a lesson and can create or update a skill; a skill change made that
way still counts as heavy, so propose it first.

For memory maintenance, read entries with `recall` and change or remove them with `memory_edit`, after the
user approves each change.
