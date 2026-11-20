# Agent Skills

My set of [Agent Skills](https://agentskills.io/specification) for various aspects of software engineering and
development: planning, design, specs, reviews and testing. A second focus is embedded Linux, with firmware
debugging and reverse engineering alongside it.

This repository holds the skills and the checks that keep them valid; it installs nothing. If you want a
managed, versioned skill catalog with an installer, this is the wrong place; if you want working skills to copy
or adapt, it is the right one.

## How the skills are checked

Every skill passes the Agent Skills specification validator and a stricter local policy before it is committed.
Behaviour evaluations go further: they run an agent on a real task with and without a skill and grade the
difference. [docs/evaluations/](docs/evaluations/README.md) holds the dated records.

## Using a skill

Copy a skill's folder, such as `engineering/technical-design/`, into your agent's skills directory, for example
`~/.claude/skills/` for Claude Code. The folder needs nothing outside itself. Check the skill's `license` field
before reusing it; see [Licensing](#licensing).

To install a whole group with [Kasetto](https://github.com/pivoshenko/kasetto), point an entry at this
repository, pin a commit, and name the group as the `sub-dir`. Kasetto discovers skills exactly one level under
that directory, so a nested group such as `development/python` needs its own entry:

```yaml
skills:
  - source: https://github.com/jonatsu/agent-skills
    ref: <commit>
    sub-dir: engineering
    skills: "*"
```

## Working on the skills

You need [mise](https://mise.jdx.dev/). `mise install` provides every other tool `mise.toml` lists, at the
version `mise.lock` pins.

```sh
mise install
uv sync
pre-commit install
just check
```

`just check` scans the whole history for secrets, then runs every pre-commit hook over the tree and both test
suites. `pre-commit install` also adds an identity check at commit and at push, which fails on any address other
than the author's GitHub noreply address. In a fork, change that address in `checks/skill_checks/identity.py`.
[AGENTS.md](AGENTS.md) holds the authoring rules: where a new skill goes, how it is reviewed, and how it is
licensed.

## Layout

| Path                        | Holds                                                                          |
| --------------------------- | ------------------------------------------------------------------------------ |
| `<domain>/<skill>/`         | Skills grouped by subject, such as `engineering`, `review` or `embedded-linux` |
| `<domain>/<group>/<skill>/` | A closely related set within a domain, such as `development/python`            |
| `checks/`                   | The checks behind `just check` and their tests                                 |
| `tests/`                    | Tests for scripts bundled inside skills                                        |
| `docs/`                     | Evaluation records, findings, and plans                                        |

## Licensing

The original work is MIT-licensed ([LICENSE](LICENSE)). A skill adapted from elsewhere keeps its upstream
licence, such as `Apache-2.0` or `CC-BY-SA-4.0`, in its frontmatter `license` field. It records its sources in
its `ATTRIBUTIONS.md` and ships the upstream licence text as `LICENSE.upstream`.

## Where to go next

- [Engineering pipeline](engineering/README.md): how the core engineering skills fit together, from an idea to
  verified work
- [Reverse engineering](reverse-engineering/README.md): binary and firmware investigation, analysis tools, and
  specialist techniques
- [Evaluations](docs/evaluations/README.md): dated evaluation records, and how to run a behaviour evaluation
- [AGENTS.md](AGENTS.md): the authoring and review rules, for people and agents working here
- [TODO.md](TODO.md): the skill backlog and unevaluated candidate sources
- The `archived` branch: retired skills kept for reference, with why each was archived

## Writing your own skills

- [Agent Skills specification](https://agentskills.io/specification): the format every skill here follows
- [Anthropic, *Skill authoring best practices*](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):
  how to structure, word, and test a skill
- [Anthropic, *Claude Code skills reference*](https://code.claude.com/docs/en/skills): the frontmatter fields
  Claude Code adds and how it uses them
- [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices): a short, opinionated
  distillation that defers to Anthropic's guide
