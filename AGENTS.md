# AGENTS.md: agent-skills

Instructions for agents working in this repository; `CLAUDE.md` is a symlink to this file. The repository holds
skill packages and the checks behind `just check`, nothing that deploys them. The author's private configuration
repository installs them from a pinned commit of this one.

Read the focused source before acting:

- `README.md` describes the layout and how the skills are used.
- `ENGINEERING-PIPELINE.md` states the intended flow of the core engineering skills, from idea to verified work.
  Read it before changing a pipeline skill's handoff, tier, or scope.
- `archived/README.md` defines the archive procedure, and its "Review is deferred" rows record which reviews are
  still outstanding.
- `TODO.md` holds the skill backlog and unevaluated candidate sources.

## Commands

```bash
just check                     # history secrets scan, every hook, both test suites; run before calling work done
just skill-check <skill-dir>   # both validators over one skill
uv run --frozen skill-checks spec | policy | descriptions | names | references   # one check, whole tree
```

**Running only one validator is the mistake the pair exists to prevent.** The specification validator passes a
file that breaks every repository policy, and the policy validator does not check frontmatter shape at all.
Report them separately; never describe one as covering the other. `just skill-check` runs both even when the
first fails.

## This Repository Is Public

- Never commit a secret, a customer or client name or detail, a personal path, an email address, or an internal
  host, in a file or a commit message. Only secrets are scanned automatically; the rest is your responsibility.
  Use reserved example values (`example.com`, `/home/user`) in a skill's examples.
- Commit as the GitHub noreply address in `checks/skill_checks/identity.py`; the `commit-identity` hook fails
  any other. Pushing publishes, so push only when the user asks.
- Commits use Conventional Commits, `type(scope): subject`, with the scope naming the skill or tool changed.

## Placing a Skill

- **By coupling.** Agent-agnostic skills go in a domain at the root. Claude Code-only skills, about `CLAUDE.md`,
  `.claude/agents` or Claude subagents, go in `claude/`.
- **Then by subject.** A skill that fits two domains goes where a reader would look first. **A skill name must
  stay unique across every group**; `just check` fails on a duplicate, because agents receive every skill flat.
- **Then by tier.** A skill almost every session needs stays direct. A specialized one, such as one language,
  one named tool, or a rarely requested method, goes under `lazy/` in the same domain.
- **A new group, or emptying one, needs a matching change where the skills are installed.** The installing
  configuration names each group as a Kasetto `sub-dir`, Kasetto finds skills exactly one level below it, and a
  missing or new group fails the next pin bump there. Say so in the commit body.

## Writing and Reviewing Skills

**Always:**

- Use `skill-forge` when creating, editing, restructuring, or replacing a skill, and
  `writing-skill-descriptions` whenever a description is written or changed.
- Use `skill-forge`'s review mode for every skill review. It governs assessment and evidence; its authoring
  mode governs the shape of a proposed repair and any separately authorized edit.
- Keep every skill self-contained: no link, path or script reference may leave its folder. `just check` fails
  one that does. A script in one skill may be run by this repository's checks, never by another skill.
- Keep a skill's `description` one inline YAML scalar. Kasetto records a folded one as its marker character.
- Keep an `ATTRIBUTIONS.md` source entry permanently, restated in the past tense once the material is
  replaced. The revisions that carried the material stay in history, so deleting the entry hides a
  relationship a later reader still needs.
- Ask what a user would have to say for a proposed skill to load, before writing it. Guidance for a moment
  nobody verbalizes, such as whenever someone writes code, belongs in an agent's rules instead; a skill for
  such a moment does not activate, and no wording repairs it.
- Keep a skill's licence: an adapted skill carries its upstream licence in the `license` field plus
  `ATTRIBUTIONS.md`. Where an upstream licence blocks the use needed, write an independent replacement rather
  than a relicensed adaptation. Relicensing needs the user's approval.

**Never:**

- Treat a review request as authorization to change the skill. Report first unless the user also requested
  implementation.
- Spend time validating or repairing an archived skill marked deferred, unless its review is explicitly
  resumed.

## Archive Without Losing Structure

- Keep every package file byte-identical to the last deployed version: `SKILL.md`, references, scripts,
  attribution and upstream licence files.
- Move an individual package to `archived/<skill>/`. When archiving an entire domain, keep it as
  `archived/<domain>/<skill>/` rather than flattening its packages.
- Add `ARCHIVED.md` inside each moved package and update `archived/README.md`.

## Git Safety in `git-commits-and-recovery`

The skill deliberately stays model-invokable: `disable-model-invocation: true` would withhold its guidance, not
prevent an agent from running Git commands. Safety relies on the agents' always-loaded staging rule and on
deterministic command guards, not on the skill's confirmation gates.
