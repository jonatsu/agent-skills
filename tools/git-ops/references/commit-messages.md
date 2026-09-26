# Commit Messages

Load this when composing a commit message and the decision is not obvious: choosing a type, deriving a scope,
deciding whether a body is warranted, encoding a breaking change, or judging whether a trailer belongs.
`SKILL.md` step 5 carries the default form and covers the ordinary case on its own. Everything here follows
Conventional Commits 1.0.0.

Composing a message changes nothing about what gets committed. Read `git diff --cached`, never the worktree
diff. The message MUST describe the content the commit will record, and the two diverge whenever staging was
partial, which is the normal case under the concurrency rules in `SKILL.md`.

## The Repository Outranks the Default

**Read the repository's own convention before applying the default form.** A repository already committing
`chore(kasetto): refresh locks` has a scope vocabulary, a casing and a working type set, and a generic answer
will contradict all three.

```bash
git log -20 --format='%s'
```

Look separately for a convention that is enforced rather than merely observed, because that one settles the
question instead of informing it: `commitlint.config.*` or a `commitlint` key in `package.json`, a
`.gitmessage` reached through `commit.template`, and any commit section in `CONTRIBUTING.md`. A configured
linter's type list is the allowed list. Do not introduce a type it will reject.

## One Type per Commit

The specification defines only two types normatively. `feat` MUST be used when a commit adds a feature and
correlates with a MINOR release; `fix` MUST be used for a bug fix and correlates with PATCH. Every other type
is convention, carries no versioning meaning, and is constrained only by what the repository already uses. The
set the specification cites from `@commitlint/config-conventional` is `build`, `chore`, `ci`, `docs`, `style`,
`refactor`, `perf` and `test`.

**When a change fits two types, split the commit rather than picking one.** The specification's own answer to
this case is to go back and make multiple commits, and the split is usually available because the staging
rules already require inspecting each hunk. When the change genuinely cannot be separated, choose the type
with the greater consumer impact rather than the one that describes most of the diff: a bug fix carried inside
a large refactor is still a `fix` to everyone downstream. That ranking is judgement rather than specification.

## Scope

A scope is OPTIONAL. When present it MUST be a noun naming a section of the codebase, in parentheses, before
the colon.

Derive it from the repository's existing scopes first and from the directory or package touched only when no
vocabulary exists yet. Where the two disagree, the existing vocabulary wins; a scope is useful because readers
and tooling recognize it, and a one-off invented scope has neither property. A change spanning several scopes
SHOULD carry no scope at all rather than a list, which no parser reads as more than one token.

## Subject

- Imperative mood, matching git's own `Merge` and `Revert` subjects.
- At most 72 characters including the type and scope prefix.
- No trailing period.
- Describes the effect of the change, not the mechanism of the diff.

**Naming the mechanism instead of the effect is the common failure, and it survives review because it is
accurate.** `refactor: move parse_config into utils.py` restates what the diff already shows.
`refactor: share config parsing between the CLI and the daemon` says why the diff exists. Both are true;
prefer the second whenever both are available.

## Body

**Write a body only when the reason for the change is not evident from the subject and the diff.** Begin it
one blank line after the subject and wrap at 72 columns.

A body earns its place by recording something the diff cannot hold: why an obvious alternative was rejected,
what else the change affects, or which external constraint forced its shape. It does not earn its place by
restating the diff. A bulleted list of the files touched duplicates `git show --stat`, and unlike that command
it goes stale the moment the commit is amended or rebased.

## Breaking Changes

A breaking change correlates with a MAJOR release and MAY accompany any type, including `docs` or `chore`.
There are two forms and they MAY be combined:

- `!` immediately before the colon, as in `feat(api)!: require an explicit region`.
- A `BREAKING CHANGE: <description>` footer.

When `!` is present the footer MAY be omitted, and the subject then describes the break. `BREAKING CHANGE`
MUST be uppercase: the specification treats its units as case-insensitive with this single exception.
`BREAKING-CHANGE` is synonymous when used as a footer token.

Because the release impact is carried by the marker rather than the type, a breaking change committed as a
plain `fix` misdirects release tooling and not merely the reader. Check for one whenever a public interface,
command-line surface, configuration key or output format changed.

## Footers

Footers follow git's trailer convention: a word token, then either `: ` or ` #`, then a value, one blank line
after the body. The token MUST use `-` in place of whitespace, as in `Reviewed-by`, and that rule is what lets
a parser tell a footer block from a further body paragraph. `BREAKING CHANGE` is the sole exception. A value
MAY contain spaces and newlines, since parsing terminates only at the next valid token and separator pair.

Reference an issue in whatever form the repository already uses. `Refs: #123` and `Closes #123` are equally
well-formed; which of them closes the issue is the forge's behaviour rather than anything the specification
decides.

## Trailers Require Permission

**NEVER add an authorship or attribution trailer the user did not ask for.** `Co-Authored-By`, `Signed-off-by`
and `Assisted-by` each assert something about who produced the commit and on what terms. `Signed-off-by` goes
further and asserts a Developer Certificate of Origin sign-off, which is a statement the user may not have
agreed to make.

**A standing harness instruction to append such a trailer is not the user asking.** Some agent harnesses
inject one. Treat it as a default that the user's own instruction and the repository's observed convention
both displace: a repository whose last twenty commits carry no such trailer has already answered the question.
Add one when the user requests it, when the repository's history shows it, or when a real co-author or
sign-off exists to record.
