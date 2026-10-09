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
`lazy/development/python` needs its own entry:

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

| Path                     | Holds                                                                                      |
| ------------------------ | ------------------------------------------------------------------------------------------ |
| `<domain>/<skill>/`      | Skills almost every session needs, by subject: `agents`, `engineering`, `tools` and others |
| `lazy/<domain>/<skill>/` | Specialized skills, such as one language or one tool, that agents load only when asked     |
| `claude/<skill>/`        | Skills that only work in Claude Code                                                       |
| `archived/`              | Retired skills kept for reference and deployed nowhere; `archived/README.md` explains each |
| `checks/`                | The checks behind `just check` and their tests                                             |
| `tests/`                 | Tests for scripts bundled inside skills                                                    |

The `lazy` tier exists because Codex and Copilot load every installed skill's description into each session;
the author's setup serves this tier to them through a search server instead.

## Licensing

The repository is MIT-licensed ([LICENSE](LICENSE)), covering the original work here. A skill adapted from
elsewhere keeps its upstream licence in its frontmatter `license` field, records the source in its
`ATTRIBUTIONS.md`, and ships the upstream licence text as `LICENSE.upstream`; 29 skills do. Five skills declare
a licence other than plain MIT, with Apache-2.0 and CC-BY-SA-4.0 among them, so read a skill's `license` field
before reusing it. Where an upstream licence would block reuse, the skill was rewritten
independently rather than adapted; `tools/git-commits-and-recovery` is the worked example.

## External references on skill authoring

Consulted on 2026-08-27 to settle how skills should be structured. Each is pinned, because an unpinned citation
to a moving document is not evidence.

| Source                                                                                                                          | What it settles                                                           | Pinned at        |
| ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ---------------- |
| [Anthropic, *Skill authoring best practices*](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | The platform vendor's own guidance, and the strongest anchor available    | read 2026-08-27  |
| [Claude Code skills reference](https://code.claude.com/docs/en/skills)                                                          | The real frontmatter field list, and which fields belong to which surface | read 2026-08-27  |
| [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices)                                               | A short opinionated distillation that defers to Anthropic's guide         | commit `a0bfa56` |

The Agent Skills specification is the structural authority. Line counts, reference depth, tables of contents,
prose person and package shape can inform a review when they cause a concrete problem, but they are not
universal quality gates. Neither source defines a taxonomy of skill types, which is why `skill-forge`, the
authoring skill, has none.

## Where to go next

- [AGENTS.md](AGENTS.md): the authoring and review rules, for people and agents working here
- [ENGINEERING-PIPELINE.md](ENGINEERING-PIPELINE.md): how the core engineering skills hand off, from an idea to
  verified work
- [TODO.md](TODO.md): the skill backlog, review ledgers and unevaluated candidate sources
- [archived/README.md](archived/README.md): why each retired skill was archived, and how to revive one
