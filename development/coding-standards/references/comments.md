# Commenting Standards

A comment earns its place by carrying reasoning the code cannot show on its own. It explains why the code
exists or behaves as it does: a constraint, a trade-off, a rejected alternative, a gotcha. It leaves what the
code does and how it does it to the code, which a fluent reader of the language already sees. Silence is the
correct output when the code needs no comment, not a gap to fill.

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

Use a labelled annotation for work left undone or a hazard. Name the condition that resolves it, so the note is
actionable rather than a standing reminder:

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
- A label with no checkable fact, such as "Important", "Main logic", or an end marker like "end if". Keep a
  label only when it states something a reader could verify, such as "retries only on 5xx responses".
- Emoji and capitals for emphasis. Use the annotation vocabulary above when a comment needs weight.
- Numbered step comments narrating a long function. When the flow needs step labels to be followed, extract each
  step into a function whose name says what the label said.
- A comment that is worth keeping but too long. Deciding to keep it and deciding its length are separate tests:
  cut it to the sentence that carries the reason.

## Keep Comments From Going Stale

A comment about the code beside it gets corrected by the next person editing that code. A comment about anything
else rots silently, so avoid the forms that go wrong without anything failing:

- Describe a setting's role and leave its current value to the code. A retention window, port, size, or delay
  goes stale the moment someone re-tunes the code, so the code stays the source of truth for the number: write
  "retention is tuned below", not "30-day retention".
- State a predicate in place of a countable inventory of other files, such as "any module that reads X without a
  fallback" in place of "seven modules do X: a, b, c". An inventory changes truth whenever any unrelated file
  changes, and a reader cannot tell a stale list from a current one. The reader derives the set from the
  predicate. This governs prose docs as much as comments.
- State the configuration as it stands, not the debugging story that produced it. Once a bug is resolved,
  comment the resulting choice and why it holds, not the conflict you hit and worked around. The process belongs
  in version control, not the source.

## Cleaning Up a Legacy File

In a file whose cleanup is the task, strip the existing comments first, except license and copyright headers,
shebang and encoding lines, and tool directives such as `# noqa`, `# type: ignore`, `// @ts-ignore`, and
`// eslint-disable`, which change how tools treat the code. Then add each removed comment back only after
justifying it against the rules above. Confirm afterwards that the diff touches only comment lines.
Rebuilding the set from nothing is more reliable than editing a pile of comments that never earned their place.
