# Worked Example

Read this when you need to see the output shape — the section order, the level of
detail, and how a reference replaces a copy. Do NOT load it when you already know
the shape; the rules in `SKILL.md` are what govern, and this file only
illustrates them.

NEVER copy this content. The repository, paths, branches, and commits below are
invented. Only the shape transfers.

## A `PRIME` brief

Delivered in the reply as one fenced block for the user to paste into a fresh
context. Note what is absent: no retelling of how the session got here, no
pasted plan, no skill list, and no section for material that did not exist.

````markdown
MISSION. You are picking up work on `acme/ingest` at branch
`feat/backpressure`, commit `4f1c9ab`. The last session landed the bounded
queue and started converting the retry path. This session finishes that
conversion — it is a single-thread implementation task, not a review pass.

Read these first, in order:

- `docs/adr/0007-backpressure.md` — the decision this work implements; the
  bounded-queue choice is settled there
- `src/pipeline/queue.rs` — where the change lands; the retry path at
  `queue.rs:180-240` is the part under edit
- `tests/pipeline/queue_test.rs` — the failing case that defines done

STATE. The bounded queue is implemented and merged as `4f1c9ab`; verified by
`cargo test -p pipeline`, 34 passed — that is the unit suite only, and the
integration suite has not been run against this change. The retry path is
half-converted: it compiles, and `queue_test.rs::retry_saturates` fails as
expected. Nothing else is in flight; the tree is clean.

NEXT. Make `retry_saturates` pass without reintroducing the unbounded channel.
Done means: that test green, the full `cargo test -p pipeline` green, and no
new `clippy` warnings.

LOCKED. The queue is bounded at 1024 by ADR 0007. Do not revisit the size or
propose an unbounded variant. The deciding argument was the downstream
service's per-minute rate limit, not memory pressure — so a memory measurement
is not grounds to reopen it.

SCOPE. The metrics rewrite on `feat/otel` is parked deliberately pending the
collector upgrade; leave it alone. The `_bench/` directory is scaffolding, not
dead code — do not delete or wire it up.

OPEN. Whether the retry backoff is exponential or fixed. Leaning exponential
with a 30s ceiling, because the downstream service rate-limits per minute.
Depends on nothing else; decide it and move.

CARRIED CONTEXT. The user prefers `thiserror` over hand-rolled error enums in
this crate, stated in passing. An earlier attempt used a semaphore and was
rejected as harder to reason about under cancellation — do not re-propose it.
Naming convention in this module is `*_saturates` for load tests, not
`*_full`.

PROCESS. `cargo clippy` runs in CI but not in the pre-commit hook, so run it
before committing rather than after. The integration suite needs
`DATABASE_URL` set or it silently skips.
````

## How a `DOCUMENT` brief differs

Same sections, three changes:

1. Identify the repository, branch, and commit once at the top, so the paths
   resolve on a machine that is not this one.
2. Write repository-relative paths throughout, never absolute ones.
3. Save it under the operating system's temporary directory and report the path.

A useful header for a travelling brief:

```markdown
# Handoff — backpressure retry path

- Repository: `git@github.com:acme/ingest.git`
- Branch: `feat/backpressure` at `4f1c9ab`
- Written: 2026-03-04
- All paths below are relative to the repository root.
```

## What the example deliberately omits

- **A `SKILLS` section**, because naming skills that may not exist in the
  reader's session is worse than naming none. Populate it from what is actually
  available at the time of writing, or leave it out.
- **`DEVIATIONS`**, because this work did not depart from its plan. An empty
  heading would have claimed otherwise.
