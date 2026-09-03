---
name: searchable-code
description: Name and write code so plain-text search finds it — identifier uniqueness, doc comments that match natural-language greps, whole string literals, and error messages that grep back to their throw site. Use when naming or renaming exports, files, events, flags, or error strings, when reviewing names, or when code turns out to be hard to find by grep. Covers findability only, not architecture, formatting, or type design.
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

Use the shortest name that greps uniquely and put the rest in the doc comment. A one-word export collides
across any large codebase; one domain word usually settles it. `diffUserObjects` over `diff`,
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

```ts
/** Checks whether the user session has expired. Uses source time, not insert time. */
```

One line on every export, stating what the signature cannot: units, timezone, ownership, ordering. The
definition is where a name search lands, so that line is the whole message.

## Keep literals whole

**Never assemble a string that someone will later search for.** Interpolation destroys the thing being looked
for — `github.pr.merged` appears nowhere in the source of the first line below:

```ts
emit(`github.${entity}.${action}`); // unsearchable
emit("github.pr.merged"); // greppable
```

This covers event names, feature flags, error codes, log keys, and metric names. Write the full literal even
where a loop looks tidier.

**Start error messages with a unique literal prefix**, so a message copied out of a log greps straight back to
the throw site:

```ts
throw new Error(`Webhook signature mismatch for ${id}`); // findable
throw new Error(`${prefix}: mismatch`); // not
```

Interpolate the variable part, never the identifying part.

## Keep one answer in one place

**One definition site per symbol.** Moving a function means deleting the original in the same change. Two
definitions make every search ambiguous, and one of them will rot.

**Rename in the same commit that changes behavior or audience.** A stale name is misinformation with a high
open rate, and that includes visibility markers: a `_private` helper other modules now import needs a public
name.

## Before committing

1. Would one search for each new exported name find its implementation?
2. Does every log, error, event, and flag string exist verbatim in the source?
3. Is the constraint a caller must know, but the signature cannot show, written at the definition?
4. Does each doc comment contain the plain-words phrase someone would search for?
5. Did anything change behavior without changing its name?
6. Where code moved, is it gone from where it came from?
