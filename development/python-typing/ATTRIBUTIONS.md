# Attributions

## Current Skill

- Skill: `python-typing`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: independently written, replacing a third-party package that taught a pre-3.12 generic syntax

## Predecessor

Replaces `python-type-safety` from
[wshobson/agents](https://github.com/wshobson/agents) `plugins/python-development/skills`, MIT, which was
deployed unreviewed until 2026-09-04. No text or code was carried across.

Its subject coverage informed this skill's scope: annotations, generics, Protocols, narrowing, `Any` policy,
and strict checker configuration. Two things were deliberately not carried:

- **The `TypeVar` plus `Generic[T]` form as the only generic syntax.** The predecessor taught it exclusively
  while declaring a 3.12 target, where PEP 695 inline parameters are available. This skill leads with the
  inline form and shows the older one for projects with a lower floor.
- **"Annotate every public signature" as the headline rule.** That is a habit nobody verbalizes, so a skill is
  the wrong carrier for it. This skill covers the cases where a capable writer actually stalls.

## Verified Behavior

Measured with mypy 2.3.1 under `--strict` on 2026-09-04 rather than taken from documentation:

- PEP 695 inline generics check correctly: `Box(1).get()` reveals `int`, and `first(["a"])` on
  `def first[T](items: Sequence[T]) -> T | None` reveals `str | None`.
- A `Protocol` with a `read` method is satisfied structurally by an unrelated class that defines one, with no
  inheritance or registration.
- `assert_never` in a `match` default reports the missing case by name. Adding `Color.GREEN` to a matched enum
  without a branch produces
  `Argument 1 to "assert_never" has incompatible type "Literal[Color.GREEN]"; expected "Never"`.

## Sources Consulted

The Python typing specification and the `typing` module documentation were used to confirm which features
arrived in which version: PEP 695 type parameter syntax in 3.12, `Self` in 3.11, `TypeIs` in 3.13. Facts
verified against a primary source require no package attribution; they are cited here because the version
floors are load-bearing for the guidance.

## Python Defaults Review, 2026-09-11

Reviewed Integralist's `.claude/rules/python.md` in `Integralist/agent-skills` at commit
`07155927c4a44cf97b050ea4f728fce840822ce9`:

<https://github.com/Integralist/agent-skills/blob/07155927c4a44cf97b050ea4f728fce840822ce9/.claude/rules/python.md>

The comparison informed the guidance on abstract collection imports and parameter capabilities.
The expression is independent; no upstream text or code is copied or adapted.
No license covering these rules was found in the pinned tree; the MCP component has separate licensing.
