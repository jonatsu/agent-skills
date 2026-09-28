# SOLID, Refactoring Discipline, and Quality Gates

Load this when a design decision turns on module responsibilities, when a refactor is in progress, or when
running the checks before a commit.

## SOLID Principles

Apply these to the seams between modules, not to every small function. They earn their weight where a design
must absorb change without a rewrite.

- Single Responsibility: give each module one reason to change. Split a unit that answers to two owners.
- Open/Closed: extend behavior by adding code, not by editing a working unit that other code depends on.
- Liskov Substitution: a subtype must stand in for its base type without surprising a caller.
- Interface Segregation: prefer several small, specific interfaces over one broad interface a client only
  partly uses.
- Dependency Inversion: depend on an abstraction, and let both the caller and the implementation depend on it,
  rather than binding a high-level unit to a concrete low-level one.

## Refactoring Discipline

Keep two kinds of change apart, and never mix them in one commit:

- Refactoring changes structure, not behavior. The existing tests must pass unchanged, and no behavior moves.
- Optimization changes performance, not behavior. Measure before and after, so a benchmark backs the claim.

Commit the current change before switching between the two, so a revert stays surgical and a regression is easy
to bisect.

## Performance Checklist

Scan a change for these before you call it done. Each is a common source of a regression that a functional test
does not catch:

- An N+1 pattern: a database or network call inside a loop that one batched query would replace.
- Blocking I/O on an asynchronous path, such as a synchronous read or a subprocess call that stalls the event
  loop.
- Excessive allocation in a hot path, where a reused buffer or a streamed result would hold memory flat.
- A missing bound on a result set: paginate or limit a query that can grow without one, or that fetches more
  fields than it uses.
- Independent asynchronous calls awaited one after another where they could run concurrently.
- An algorithm that is quadratic where the data reaches a size that a linear or logarithmic approach would keep
  cheap.
- A missed cache: a pure, repeated, expensive computation whose input rarely changes.

Optimize against a measurement, not a guess. A profile or a benchmark decides whether any of these is worth
changing for the data the code actually sees.

## Quality Gates

Run the repository's own checks, and let each one pass before you commit: the tests, the linter, the type
checker where the language has one, the build, and the security or secrets scan. The
`git-commits-and-recovery` skill owns the staging and commit procedure; this list is the bar a commit clears,
not a substitute for that procedure. When you must ship below the bar, name the failing gate and the reason
rather than silencing it.
