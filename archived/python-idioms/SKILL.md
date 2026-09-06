---
name: python-idioms
description: Review or refactor Python toward idiomatic, findable code. Use when asked to review Python, make code more idiomatic, clean a module up to conventions, choose between attrs and a stdlib dataclass, judge whether a test may mock something, or when a search for code you believe exists returns nothing.
license: MIT
compatibility: Portable. Judgement rules only; anything a linter can decide belongs in the project's ruff configuration.
metadata:
  author: Joonas Onatsu
---

# Python Idioms

Judgement calls a linter cannot make, and the conventions this author prefers when nothing else decides.

**A project's own conventions outrank everything here.** Read its existing code, its `pyproject.toml`, and its
instruction files first. When they disagree with this skill, follow them and say so rather than silently
reformatting toward a different taste.

Anything ruff or mypy decides — line length, import order, quote style, `Optional[X]` versus `X | None`,
naming case — is settled by the project's configuration, not by this file. See `python-project-management`.

## Name So a Plain-Text Search Finds It

An agent reads code by searching for strings and looking at a small window around each hit. No hover, no
jump-to-definition, nothing carried from the last session. Every identifier is a search query.

**Give a generic verb its object.** `validate_smtp_config`, not `validate`. `queue_event_for_dispatch`, not
`queue`. Use the shortest name that greps uniquely, and put the rest in the docstring.

**Do not let the module path do the disambiguating.** The import separating `users/diff.py` from
`orders/diff.py` sits at the top of the file; the search hit is three hundred lines below it. Put the context
in the symbol.

**One concept, one spelling.** `org_id` or `organization_id`, never both. A synonym halves every future
search. Reuse the vocabulary already in the file you are editing.

**Never a bare-role filename.** `config.py`, `utils.py`, `types.py`, `handlers.py` say nothing in a result
list and collide with every other module's. Prefix the domain: `billing_plan_config.py`. `__init__.py` is a
thin re-export entry point, not a home for logic.

**Put the plain-words phrase in the docstring.** A search arrives as ordinary language — "rate limit",
"session expired" — and `RateLimiter` contains neither phrase as written. The definition is where a name
search lands, so one line there is the whole message:

```python
def check_session_expiry(session: Session) -> bool:
    """Whether the user session has expired. Uses source time, not insert time."""
```

State what the signature cannot: units, time zone, ownership, ordering.

**Keep searchable literals whole.** Interpolation destroys the thing being looked for. `github.pr.merged`
appears nowhere in the source of the first line:

```python
emit(f"github.{entity}.{action}")   # unsearchable
emit("github.pr.merged")            # greppable
```

This covers event names, feature flags, error codes, log keys, and metric names. Where the set is genuinely
open — per-dimension metric tags, generated route names, translation keys — keep the stem literal and
interpolate only the tail, so `metric("checkout.latency." + region)` still answers a search for
`checkout.latency`. A closed set of a dozen events is not an open set, however much a loop would tidy it.

**Start an error message with a unique literal prefix**, so a message copied from a log greps back to its
raise site. Interpolate the variable part, never the identifying part.

**Rename in the same change that alters behavior or audience.** A function that now handles subscriptions but
is still called `handle_trial` is invisible to every search for "subscription": the code goes missing without
moving.

## When a Search Comes Up Empty

A failed search is usually one of the rules above already broken. Work down this list before concluding the
code does not exist:

- **Search a fragment, not the whole string.** If the value was assembled, the full form appears nowhere.
  Grep the stem or the distinctive tail alone.
- **Search the plain-words phrase, not the identifier.** "session expired" finds the docstring that
  `SessionExpiryChecker` cannot match.
- **Search an error's literal prefix**, not the message you were given: the logged text contains interpolated
  values that appear nowhere in the source.
- **Try the other spelling.** `org_id` and `organization_id`, singular and plural, underscore and hyphen.
- **Search the caller, not the definition.** An import or call site is often easier to guess than the
  definition's name.

**When one of these is what found it, fix the cause in the same change.** You now know exactly which rule was
broken, and this is the cheapest moment to rename the symbol, add the docstring phrase, or unpick the
interpolation.

## Value Types

**Prefer `attrs` over stdlib `dataclasses` by default**: `@attrs.frozen` for value types, `attrs.evolve` in
place of `dataclasses.replace`.

This is a soft rule with a real exception. **Where pulling in `attrs` buys little — a single value type in one
file, a script, a package that otherwise has no third-party runtime dependency — prefer the built-in
`dataclass`.** `attrs` is a runtime dependency, so adopting it means adding it to every copy of that project's
dependency list, not only the one you are editing.

Either way, prefer frozen. A value type that cannot be mutated after construction removes a whole class of
aliasing bug, and `evolve`/`replace` makes the derived-copy case explicit.

## Testing Preferences

These duplicate the global workflow rules deliberately, so the guidance survives if that file is trimmed.
`python-testing` has the pytest mechanics; this is the policy.

- **A check proves only what it covers.** Linting, formatting, type checking and a successful build are not
  substitutes for a behavioral test.
- **Test pure logic directly, with real inputs and outputs. Never mock it.** A test that mocks the thing it is
  testing asserts only that the mock was configured.
- **Unit tests may mock only genuine side-effect boundaries**: external I/O, time, randomness, subprocesses.
- **Integration and end-to-end tests use real dependencies** in an isolated environment. A test with a stub
  in place of the real dependency is a unit test; classify it honestly rather than claiming coverage it does
  not have.

## Reach for the Standard Library First

In order: an existing pattern or helper in this codebase, then the standard library, then a dependency the
project already has, then the smallest new thing that meets the requirement. A new dependency is a permanent
maintenance and supply-chain cost paid for a one-off convenience.

Prefer `pathlib` over `os.path`, `enum` over string constants, `contextlib` over hand-rolled try/finally, and
`itertools` over a hand-written loop that reimplements one of its functions.

## Simplicity Over Cleverness

- **Write the obvious version first.** Clever comprehensions, metaclasses, and decorators that rewrite
  signatures cost every later reader more than they saved the author.
- **Do not add configurability, extension points, or abstraction for a need that does not exist yet.**
- **Tolerate small duplication** when the abstraction would cost more than the repetition. Remove duplication
  when it is meaningful and the abstraction genuinely clarifies.
- **Prefer a flat sequence of steps to nesting.** Early returns and guard clauses beat an arrow of `if`s.
- **Say what the code does in the code**, and reserve comments for why it does it that way.

## Reviewing Python

When asked to review, look for these before style:

1. Names that will not be found by a search, in the terms above.
2. A bare-role filename, or one concept spelled two ways.
3. An assembled literal that someone will later search for whole.
4. Mocking of pure logic, or an integration test with fakes in it.
5. A mutable default argument, a mutable class attribute, or a shared mutable value type.
6. Abstraction with exactly one implementation and no second one in sight.
7. A broad `except` that hides a bug, or a swallowed exception.

Report what a linter would have caught separately, or not at all if the project's configuration already
covers it. Repeating ruff's findings by hand wastes the review.
