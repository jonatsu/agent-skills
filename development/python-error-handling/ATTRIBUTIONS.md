# Attributions

## Current Skill

- Skill: `python-error-handling`
- Current author: Joonas Onatsu
- Current license: MIT
- Status: independently written, replacing a same-named third-party package

## Predecessor

Replaces `python-error-handling` from
[wshobson/agents](https://github.com/wshobson/agents) `plugins/python-development/skills`, MIT, which was
deployed unreviewed until 2026-09-04. The name is reused because it is the searchable name for the subject; no
text or code was carried across.

Its subject coverage informed this skill's scope: boundary validation, converting external data to domain
types, exception hierarchies, chaining, partial-failure batches, and the built-in exception table. The idea of
mapping failure kinds to built-in exceptions before defining new ones is retained.

Two things were deliberately not carried:

- **The predecessor's own chaining rule was contradicted by its own example.** Its summary said to use
  `raise ... from e`, while its worked example re-raised inside an `except ValueError` block with no `from`.
- **Its `ValidationError` example** used a name it never imported or defined.

## Verified Behavior

Measured on CPython 3.13.15 on 2026-09-04 rather than taken from documentation:

- Raising inside an `except` block with no `from` sets `__context__` to the original exception and leaves
  `__cause__` as `None`, so the original is preserved and the traceback reads "During handling of the above
  exception, another occurred".
- `raise New() from exc` sets both `__cause__` and `__context__`, and sets `__suppress_context__` to `True`.
- `raise New() from None` sets `__suppress_context__` to `True` with `__cause__` as `None`, hiding the
  original from the traceback while still recording it in `__context__`.
- `except* ValueError` receives only the `ValueError` members of an `ExceptionGroup`, and a sibling
  `except* KeyError` receives only the `KeyError` members.

The first three measurements are why this skill states that omitting `from` does not lose the original, which
is the opposite of what the guidance is usually shortened to.

## External Tools Referenced

Named without vendored API surface: pydantic, attrs, cattrs, voluptuous. Their interfaces move, so the
upstream documentation is the authority rather than any summary here.
