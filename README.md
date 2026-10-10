# Agent Skills

A collection of 82 Agent Skills, each a self-contained folder of instructions and optional scripts that Claude
Code, Codex, GitHub Copilot CLI and Oh-My-Pi load on demand.

The skills cover software engineering work: specs, technical design, implementation planning, code review,
testing, Git, documentation, Python, shell, Nix, embedded Linux and firmware debugging, and authoring further
skills. They are one person's working set, written and reviewed for daily use, and published so others can read
or reuse them.

This repository holds the skill packages and the checks that keep them valid, and nothing that installs them.
It does not decide which agent gets which skill or deploy anything: the author's private configuration
repository does that, pinning a reviewed commit of this one through
[Kasetto](https://github.com/pivoshenko/kasetto). If you want a managed, versioned skill catalog with an
installer, this is the wrong place; if you want working skills to copy or adapt, it is the right one.

## What a check run looks like

Every skill passes the [Agent Skills specification](https://agentskills.io/specification) validator and a
stricter local policy before it is committed. Validating one skill:

```console
$ just skill-check engineering/technical-design
Agent Skills specification (skills-ref)

1 checked, 0 failed
Skill Forge local policy (quick_validate)

1 checked, 0 failed, 0 with warnings
```

## Using a skill

Copy a skill's folder, such as `engineering/technical-design/`, into your agent's skills directory, for example
`~/.claude/skills/` for Claude Code. Each folder is self-contained: nothing in it links to or loads a file outside
itself. `just check` catches the common breaks, a Markdown link or a script path that climbs out of the folder.
Mind the licensing section below; some skills carry their upstream licence.

To install a whole group with Kasetto, point an entry at this repository, pin a commit, and name the group as
the `sub-dir`. Kasetto discovers skills exactly one level under that directory, so a nested group such as
`development/python` needs its own entry:

```yaml
skills:
  - source: https://github.com/jonatsu/agent-skills
    ref: <commit>
    sub-dir: engineering
    skills: "*"
```

## Working on the skills

You need [mise](https://mise.jdx.dev/). `mise install` provides every other tool at the version `mise.lock`
pins: Python, uv, [just](https://just.systems/), [pre-commit](https://pre-commit.com/), ShellCheck, shfmt and
[Betterleaks](https://github.com/betterleaks/betterleaks).

```sh
mise install
uv sync
pre-commit install
just check
```

`just check` scans the whole history for secrets, then runs every pre-commit hook over the tree and both test
suites. The hooks include the two skill validators, and checks that no skill description is a folded YAML
scalar, that no two skills share a name, and that no skill links outside its own folder. `pre-commit install`
also adds two identity checks, at commit and at push, that fail on any address other than the author's GitHub
noreply address. [AGENTS.md](AGENTS.md) holds the authoring rules: where a new skill goes, how it is reviewed, and how
it is licensed.

## Layout

| Path                        | Holds                                                                                      |
| --------------------------- | ------------------------------------------------------------------------------------------ |
| `<domain>/<skill>/`         | Skills grouped by subject: `agents`, `engineering`, `tools`, `embedded-linux` and others   |
| `<domain>/<group>/<skill>/` | A closely related set within a domain, such as `development/python`                        |
| `claude/<skill>/`           | Skills that only work in Claude Code                                                       |
| `archived/`                 | Retired skills kept for reference and deployed nowhere; `archived/README.md` explains each |
| `checks/`                   | The checks behind `just check` and their tests                                             |
| `tests/`                    | Tests for scripts bundled inside skills                                                    |

The layout says what a skill is about, not how an agent loads it. Which skills an agent lists in every session
and which it loads on demand is the installer's choice.

## Licensing

The original work in this repository is MIT-licensed ([LICENSE](LICENSE)). Skills adapted from
elsewhere keep their upstream licence in the skill's frontmatter `license` field, record their source(s)
in an `ATTRIBUTIONS.md` document in the skill directory, and ship their upstream licence text as `LICENSE.upstream`.

Some skills may declare other than plain MIT license, like `Apache-2.0` or `CC-BY-SA-4.0`, so check the skill's
`license` field before reusing it. Where a skills upstream licence would block reuse, the skill was rewritten
independently rather than adapted. A rewrite example skill is `tools/git-commits-and-recovery`.

## Skill authoring references

These sources were consulted about how the skills should be written and structured.

| Source                                                                                                                          | Description                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| [Agent Skills specification](https://agentskills.io/specification)                                                              | Complete format specification for Agent Skills, which all skills here follow |
| [Anthropic, *Skill authoring best practices*](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | Solid and high quality best practices guidance by Anthropic                  |
| [Anthropic, *Claude Code skills reference*](https://code.claude.com/docs/en/skills)                                             | Claude Code specific frontmatter fields and their usage                      |
| [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices)                                               | Short opinionated distillation that defers to Anthropic's guide              |

## Where to go next

- [AGENTS.md](AGENTS.md): the authoring and review rules, for people and agents working here
- [ENGINEERING-PIPELINE.md](engineering/README.md): core engineering skills structure, intended fit together and workflow,
  from an idea to verified work
- [TODO.md](TODO.md): the skill backlog, review ledgers and unevaluated candidate sources
- [archived/README.md](archived/README.md): why each retired skill was archived, and how to revive one
