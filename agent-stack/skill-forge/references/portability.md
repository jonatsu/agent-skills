# Portability

Check frontmatter portability and runtime portability independently. A skill can satisfy either while failing the other.

## Frontmatter Portability

Use fields defined by the Agent Skills specification for new portable skills. Store extension data as string-valued
entries under `metadata` when that representation is appropriate. Add vendor-specific top-level fields only when the user
explicitly targets that vendor and accepts the compatibility boundary.

Validate the result with `skills-ref`. Do not maintain a second copy of the external schema in the skill.

## Runtime Portability

Portable is the default when `metadata.scope` is absent. Portable skills:

- may require a tool intrinsic to their purpose;
- declare material runtime requirements in `compatibility`;
- refer to bundled files with relative paths from the skill root;
- avoid authoring-machine paths, usernames, package-manager assumptions, and repository-local commands;
- check optional surrounding tools before using them; and
- report unavailable required dependencies clearly.

A named dependency is legitimate when the skill is about that tool or cannot perform its stated capability without it.
Do not force a misleading fallback merely to appear tool-agnostic.

## Repository-Specific Skills

A repository-specific skill sets:

```yaml
metadata:
  scope: repo-local
```

It names the repository near the start of its body. It may then rely on that repository's commands, paths, conventions,
and checked-in tools because those bindings are part of its purpose. It still declares external environment requirements
and avoids assumptions about the author's machine.

Before changing scope, check whether consumers expect the current portability boundary. Narrowing a portable skill to one
repository is a behavioral change, not a documentation cleanup.
