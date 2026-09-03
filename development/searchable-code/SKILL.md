---
name: searchable-code
description: Name and write code so plain-text search finds it, and recover a search that came up empty. Covers identifier uniqueness, doc comments that match natural-language greps, whole string literals, and error messages that grep back to their throw site. Use when naming or renaming exports, files, events, flags, or error strings, when reviewing names, or when a grep for code you believe exists returns nothing. Findability only, not architecture, formatting, or type design.
license: MIT
metadata:
  author: Joonas Onatsu
---

# Searchable Code

Agents find code by searching for strings and reading a small window around each hit. There is no hover text,
no jump-to-definition, and nothing carried over from the last session. Every identifier is therefore a search
query, and every miss costs reads that buy nothing.

These rules make a symbol resolvable in one search. They govern findability only — module boundaries,
formatting, and type design are separate concerns.

## Name for the search that will look for it

Use the shortest name that greps uniquely and put the rest in the doc comment. A one-word export usually
collides once a codebase is large enough to have two of anything; one domain word settles most of them. Test
it rather than assuming either way — grep the candidate before committing to it. `diffUserObjects` over `diff`,
`queueEventForDispatch` over `queue`. Give a generic verb its object: `sanitizeEmailHtml`, not `sanitize`.
Qualify as far as uniqueness requires, then stop.

**Do not let the module path do the disambiguating.** The import that separates `users/diff.ts` from
`orders/diff.ts` sits at the top of the file; the search hit is three hundred lines below it. Put the context
in the symbol. The exception is a rigid convention where the path carries the meaning, such as every contract
file exporting `Input` and `Output`.

**One concept, one spelling.** `organizationId` or `orgId`, never both — a synonym splits every future search
in half. Reuse the vocabulary already in the file you are editing rather than introducing a near-synonym.

**Never use a bare-role filename.** `config.ts`, `types.ts`, `utils.ts`, `handlers.ts` say nothing in a result
list and collide with every other module's. Prefix the domain: `billing-plan-config.ts`. `index.ts` is
acceptable only as a thin re-export entry point.

## Write the words someone will actually search for

**A camelCase identifier does not match a phrase search.** Searches arrive as ordinary language — "rate
limit", "session expired" — and `RateLimiter` contains neither phrase as written. The doc comment is where
you repair that: put the phrase in spaced-out words so the grep lands on the definition.

```python
def check_session_expiry(session):
    """Checks whether the user session has expired. Uses source time, not insert time."""
```

One line on every export, stating what the signature cannot: units, timezone, ownership, ordering. The
definition is where a name search lands, so that line is the whole message.

## Keep literals whole

**Never assemble a string that someone will later search for.** Interpolation destroys the thing being looked
for — `github.pr.merged` appears nowhere in the source of the first line below:

```go
emit(fmt.Sprintf("github.%s.%s", entity, action)) // unsearchable
emit("github.pr.merged")                          // greppable
```

This covers event names, feature flags, error codes, log keys, and metric names. Write the full literal even
where a loop looks tidier.

**The exception is an open set**, where enumerating every value is impractical: per-dimension metric tags,
generated route names, translation keys. Keep the searchable stem literal and interpolate only the tail, so
`metric("checkout.latency." + region)` still answers a search for `checkout.latency`. This is the same shape
the error-message rule uses below. A closed set — the handful of events your system actually emits — is not
an open set, however much a loop would tidy it.

**Start error messages with a unique literal prefix**, so a message copied out of a log greps straight back to
the throw site:

```ts
throw new Error(`Webhook signature mismatch for ${id}`); // findable
throw new Error(`${prefix}: mismatch`); // not
```

Interpolate the variable part, never the identifying part.

## Keep the name true to what the code does

**Rename in the same commit that changes behavior or audience.** A name describing the old behavior cannot be
found by anyone searching for the new one, so the code goes missing without moving: a function that now
handles subscriptions but is still called `handleTrial` is invisible to every search for "subscription". That
includes visibility markers — a `_private` helper other modules now import needs a public name.

## When a search comes up empty

A failed search is usually one of the rules above already broken, and each has its own recovery. Work down
this list before concluding the code does not exist:

- **Search a fragment, not the whole string.** If the value was assembled, the full form appears nowhere.
  Grep the stem (`checkout.latency`, `github.`) or the distinctive tail on its own.
- **Search the plain-words phrase, not the identifier.** "session expired" finds the doc comment that
  `SessionExpiryChecker` cannot match. If a phrase search finds the definition and a name search did not, the
  doc comment is doing its job and the name is not.
- **Search the literal prefix of an error, not the message you were given.** A logged message contains
  interpolated values that appear nowhere in the source; the fixed leading words do.
- **Try the other spelling.** `orgId` and `organizationId`, singular and plural, hyphen and underscore. A
  synonym in the codebase is why the first search missed.
- **Search the caller, not the definition.** An import or call site names a symbol you can then search
  directly, and is often easier to guess than the definition's name.

**When one of these is what found it, fix the cause in the same change.** The next search will fail the same
way otherwise, and you now know exactly which rule was broken. That is the cheapest moment to rename the
symbol, add the doc-comment phrase, or unpick the interpolation.

## Before committing

1. Would one search for each new exported name find its implementation?
2. Does every log, error, event, and flag string exist verbatim in the source, or at least its stem where the
   set is genuinely open?
3. Is the constraint a caller must know, but the signature cannot show, written at the definition?
4. Does each doc comment contain the plain-words phrase someone would search for?
5. Did anything change behavior without changing its name?
6. Where code moved, is it gone from where it came from?
