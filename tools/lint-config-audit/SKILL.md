---
name: lint-config-audit
description: Audit and tighten a repository's existing linter, type-checker, and formatter configuration across its languages. Use to find stale suppressions and exclusions, outdated or misconfigured checkers, and unused rules worth enabling with their violation counts, or to enable an approved rule and fix its violations. Setting up a new repository's baseline hooks belongs to repo-management.
license: MIT
compatibility: Runs the repository's own checkers, so each one the audit covers must be installed. Reading latest releases needs network access.
metadata:
  author: Joonas Onatsu
---

# Lint Config Audit

Make a repository's checks catch more without losing anything they catch today. The audit finds suppressions
whose reason is gone, checkers that are stale or misconfigured, and rules worth enabling, each backed by a
count the agent ran. Implementation then lands each approved change on its own.

The request may name a focus, such as one language, a category such as security, or everything. Audit only
that focus, and name what you left out.

The audit is read-only. Every change to configuration or code waits for the user's decision on that specific
finding, because enabling a rule rewrites code across the tree and suppressing one removes protection.

## 1. Inventory the Checkers

Find every place a check runs: the pre-commit configuration, CI workflows, task-runner recipes, and each
tool's own configuration file. A checker can run in several layers with different settings, and a gap between
layers is a finding.

Record for each checker:

- the version the repository runs, and the latest release, read from its registry or changelog, never from
  memory;
- every configuration file it reads, including sections inside a shared file such as `pyproject.toml`;
- the rules it enables, ignores, and ignores per file; and
- the layers that run it, and whether they pass it the same configuration.

Read the configuration's comments as you go. A comment explaining why a rule is off is a recorded decision,
and step 4 respects it.

The step is done when every language in the focus has its checkers listed, or is reported as unchecked.

## 2. Prove Every Suppression

A suppression is anything that turns a check off for some code: a global ignore, a per-file ignore, an inline
directive, a path exclusion, or an environment override such as a parser option or a set of declared globals.
Each exists for a reason in the code, and a suppression whose reason is gone is stale.

Use the checker's own unused-suppression detection first, since it is exact and cheap.
[references/checker-recipes.md](references/checker-recipes.md) lists it per tool. Where a tool has none, lift the
suppression and rerun the check on exactly the code it covers: zero violations means it is stale. For an
environment override, search the covered code for the construct it allows, such as a Node global in browser
code.

**Zero violations means stale only when the command could have reported one.** A count taken with the
repository's configuration still applies every other suppression, so a rule silenced by a per-file ignore
reports clean under `--select`. Lift the suppression under test in the command itself, and prove the command
can see the rule by running it once on a file that violates it.

Check the layers against each other too: a path excluded in one layer and checked in another gets formatting
without linting, or linting without formatting.

The step is done when every suppression in the focus is classed as still needed, with the violation count or
construct that proves it, or as stale.

## 3. Find Misconfiguration

Look for duplicated or conflicting entries, rules the current version renamed or removed, exclusions naming
paths that no longer exist, and checkers whose runs disagree with their editor or CI copies. Most tools warn
about unknown rules when they run; read that output rather than trusting a silent exit.

Where a formatter and a linter govern the same syntax, run them in configured order twice. A sound pair
reaches a fixed point: the second pass changes nothing and every checker passes.

## 4. Count Candidate Rules

List the rules the installed version offers but the configuration does not enable. Skip a rule the
configuration documents as rejected, unless you have a concrete way around the recorded reason; name that way
in the report.

Count each candidate's violations across the focus, with the command from step 2's proof. A candidate at zero
is a free guardrail: enabling it costs no code change. For the rest, pick two or three real violations that
show why the rule matters here.

Rank candidates by value to this repository against the effort to fix. A rule that catches real defects
outranks a style preference, an auto-fixable rule costs less than one needing judgment, and a rule echoing a
convention the repository already documents in its style guide or agent instructions ranks higher.

## 5. Report

Present findings in this order, because each group costs less to act on than the next:

1. **Misconfiguration and staleness:** stale suppressions with their proof, available version updates, invalid
   or conflicting entries, and layer gaps.
2. **Free guardrails:** every zero-violation candidate, listed together.
3. **Rules worth enabling:** one entry per candidate, in rank order.
4. **Tightenings:** stricter modes of enabled rules, lower thresholds, and broad ignores that could narrow to
   the files that need them.
5. **Work already open:** existing branches or pull requests that change the same configuration, so the user
   can batch.

Write each rule worth enabling as:

````markdown
### <tool> <rule>: <what it catches> (<count> violations)

<Why it matters for this repository.>

`<path>:<line>`, before and after:

```<language>
<the real code, then the fixed code>
```

Effort: <auto-fixable, mechanical, or needs judgment>.
````

Then ask which findings to act on, and stop.

## 6. Apply Approved Changes

Land each approved finding as its own commit, in the repository's commit convention, so a reviewer can accept
or revert one rule without the others:

- **Enable a rule or tighten one:** change the configuration, fix every violation, and rerun the rule to zero.
- **Remove a stale suppression or fix a misconfiguration:** change only that entry.
- **Reject a candidate:** add a comment beside the configuration saying why it stays off, so the next audit
  respects the decision.

Fix a violation without changing behavior. When the only fix changes behavior, or you cannot tell, stop and
report that violation; adding a new suppression to finish the rule would remove protection the user did not
agree to lose. Run the formatter after fixing, and the tests that cover changed files.

Before each commit, diff the configuration: it adds or removes exactly the approved entry, and no existing
rule or exclusion has vanished. After a rebase, check again for duplicated or lost entries. Then run the
repository's full checks.

Branches, pushes, and pull requests follow the repository's conventions and need the user's authorization.

The work is done when every approved finding has landed or been reported as blocked, each commit passes the
repository's checks, and the undecided findings are listed for the user.
