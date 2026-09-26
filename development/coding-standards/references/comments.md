# Commenting Standards

A comment earns its place by carrying reasoning the code cannot show on its own. It explains why the code
exists or behaves as it does: a constraint, a trade-off, a rejected alternative, a gotcha. It does not narrate
what the code does or how it does it, which a fluent reader of the language already sees. Silence is the correct
output when the code needs no comment, not a gap to fill.

Before writing a comment, ask whether a better name would remove the need. When it would, rename the variable,
function, or constant instead. A comment is the fallback for reasoning that naming cannot carry.

## Explain Why, Not What

Bad, because it restates what the code already shows:

```python
# check if user is admin
if user.role == "admin":
    ...
```

Good, because it carries a constraint the code cannot show:

```python
# Billing exports stay admin-only until the SOC 2 audit closes.
if user.role == "admin":
    ...
```

Bad, because it narrates the mechanics:

```python
# loop through items and sum the non-refund values
total = sum(item.value for item in items if not item.is_refund)
```

Good, because the reason is not obvious from the code:

```python
# Refunds carry negative values that would double-count against gross revenue.
total = sum(item.value for item in items if not item.is_refund)
```

Keep a comment short and prefer one line. Write the non-obvious why: why the obvious approach fails and this
one works.

## Comments Worth Writing

- Business logic whose rule is not visible in the code, such as a progressive tax bracket or an eligibility
  cutoff.
- A non-obvious algorithm choice, such as naming the algorithm and why it fits the problem.
- A regex, with a plain statement of what it matches.
- An external constraint or gotcha, such as an API rate limit, a library bug, or an ordering requirement.
- A configuration constant, with the source or reasoning behind its value.
- A public API doc-comment: parameters, return shape, and error conditions, which is a contract for callers who
  will not read the implementation.

## Annotations

Use a labelled annotation for work left undone or a hazard, and name the condition that resolves it, so the
note is actionable rather than a standing reminder:

```text
TODO: replace with proper user authentication after the security review lands
FIXME: connection pool leaks under sustained load; investigate before the next release
HACK: works around a bug in library v2.1.0; remove after the upgrade
NOTE: assumes UTC for every timestamp in this module
WARNING: mutates the argument in place rather than returning a copy
SECURITY: validate this input against injection before it reaches the query
```

## Anti-Patterns

- Commented-out code. Delete it; version control keeps the history.
- Changelog comments, such as who changed a line and when. That history belongs in version control, not the
  source.
- Decorative dividers and banner comments. They add visual noise and no meaning.
- A comment that restates the function or variable name.

## Keep Comments From Going Stale

A comment about the code beside it gets corrected by the next person editing that code. A comment about anything
else rots silently, so avoid the forms that go wrong without anything failing:

- Do not bake a current setting value into a comment. A retention window, port, size, or delay goes stale the
  moment someone re-tunes the code. Describe the role and let the code be the source of truth for the number:
  write "retention is tuned below", not "30-day retention".
- Do not state a countable inventory of other files, such as "seven modules do X: a, b, c". Its truth changes
  whenever any unrelated file changes, and a reader cannot tell a stale list from a current one. State the
  predicate instead, such as "any module that reads X without a fallback", and let the reader derive the set.
  This governs prose docs as much as comments.
- State the configuration as it stands, not the debugging story that produced it. Once a bug is resolved,
  comment the resulting choice and why it holds, not the conflict you hit and worked around. The process belongs
  in version control, not the source.

## Cleaning Up a Legacy File

Strip the existing comments first, then add each one back only after justifying it against the rules above.
Rebuilding the set from nothing is more reliable than editing a pile of comments that never earned their place.
