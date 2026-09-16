---
name: ast-grep
description: Search and rewrite code structurally with ast-grep, matching Abstract Syntax Tree shapes rather than text. Use when locating language constructs that text search cannot express, writing or debugging ast-grep patterns and YAML rules, or applying a mechanical code change across many files. Use ast-grep-outline to map a file or directory's structure instead of matching a pattern.
license: MIT
compatibility: Requires the ast-grep CLI (`ast-grep`, also installed as `sg`). Documented against 0.45.3.
metadata:
  author: Joonas Onatsu
---

# ast-grep Structural Search and Rewrite

ast-grep matches complete AST nodes, not text substrings. That is its advantage over `rg` and its main
failure mode: a pattern whose node shape differs from the target code matches nothing, and reports the same
empty output as genuinely absent code.

Use it when the query is structural — a call with a particular argument shape, a function containing an
`await`, a class missing a method — or when a mechanical edit must apply uniformly across a codebase. Use `rg`
for literal strings, comments, and anything outside parseable source.

## Workflow

Work from a known-matching example outward. Guessing a rule against a whole repository gives no signal when
it returns nothing.

1. **Fix the target.** Which language, which construct, which variations count as a match, and what must be
   excluded.
2. **Write an example.** A short snippet containing exactly what should match. Keep it in a scratch file or
   pipe it on stdin.
3. **Write the simplest rule that could work.** Start with `pattern`. Fall back to `kind` plus relational
   rules when the pattern cannot express the structure. See
   [references/rule-reference.md](references/rule-reference.md) for the full rule syntax.
4. **Test against the example**, not the codebase. Iterate until it matches.
5. **Run against the codebase**, then read the match count critically before trusting it.

### Testing a Rule

Inline rules avoid a file for quick iteration:

```bash
echo 'async function t() { await fetch(); }' | ast-grep scan --stdin --inline-rules 'id: test
language: javascript
rule:
  kind: function_declaration
  has:
    pattern: await $EXPR
    stopBy: end'
```

Use a rule file once the rule outgrows one screen:

```bash
ast-grep scan --rule test_rule.yml test_example.js
```

Single-quote the whole inline rule so the shell leaves `$EXPR` alone. Inside double quotes every metavariable
needs `\$`, which is where hand-written inline rules usually break.

### Searching

```bash
ast-grep run --pattern 'console.log($ARG)' --lang javascript path/       # simple, single-node
ast-grep scan --rule my_rule.yml path/                                   # relational or composite logic
```

`run --pattern` handles one node shape with no surrounding conditions. Anything needing `inside`, `has`,
`all`, `any`, or `not` is a `scan` rule.

## Rewriting

`run --rewrite` and a rule's `fix:` field both **print a diff and change nothing** by default. The write only
happens with `--update-all` (or `--interactive` to confirm hunk by hunk).

```bash
ast-grep run --pattern 'console.log($$$A)' --rewrite 'logger.debug($$$A)' --lang javascript src/   # preview
ast-grep run --pattern 'console.log($$$A)' --rewrite 'logger.debug($$$A)' --lang javascript src/ --update-all
```

In a rule file, `fix:` sits beside `rule:` at the top level:

```yaml
id: no-console
language: javascript
severity: warning
message: use the logger
rule:
  pattern: console.log($$$A)
fix: logger.debug($$$A)
```

Read the preview diff before applying one. A rewrite reuses whatever the metavariables captured, so a pattern
that is one node too broad silently rewrites more than intended — and `--update-all` over a dirty tree leaves
nothing to diff against. Commit or stash first.

For a rewrite that will be kept and rerun, `ast-grep new rule` scaffolds a rule and `ast-grep test` runs
snapshot tests over a rule directory.

## Debugging a Rule That Matches Nothing

Zero matches means either "the code is absent" or "the pattern has the wrong node shape". Distinguish them
before reporting an absence.

Inspect how the code and the pattern are actually parsed:

```bash
ast-grep run --pattern 'class User { constructor() {} }' --lang javascript --debug-query=cst
ast-grep run --pattern 'class $NAME { $$$BODY }' --lang javascript --debug-query=pattern
```

`cst` shows every node including punctuation, `ast` only named nodes, and `pattern` shows ast-grep's own
reading of the pattern. Use `cst` to find the right `kind` name for a language.

Then, in order:

1. Test the pattern against a snippet **known** to contain the code.
2. Strip the rule back to its simplest positive part and add conditions one at a time.
3. Add `stopBy: end` to every `inside` and `has`. The default `neighbor` stops at the first non-matching node,
   which is rarely what a search wants.
4. Verify each `kind` against `--debug-query=cst` output rather than against the grammar you expect.

**Qualified paths are whole nodes.** `env::var($ENV)` does not match `std::env::var("X")`. Try the bare and
the fully qualified form, or absorb the intermediate nodes with `$$$`.

**A metavariable must be the entire text of its node.** `obj.on$EVENT`, `"Hello $WORLD"` and `a $OP b` never
capture; use `$$OP` for an unnamed node such as an operator.

## Reading `--json` Output

`--json` prints a bare JSON array of matches, with no wrapper object. `scan --json` uses the same schema.
Two properties bite:

- `range.start.line` is **0-based**. Add 1 before printing a file:line reference.
- A `$$$REST` list metavariable lands in `metaVariables.multi` and **includes unnamed separator nodes**. For
  `console.log("value", 1, 2)` matched by `console.log($ARG, $$$REST)`, `REST` is `1`, `,`, `2` — three
  entries, not two. Filter before counting arguments.

Single metavariables land in `metaVariables.single`.

```bash
ast-grep run --pattern 'foo($ARG)' --lang javascript --json . \
  | jq -r '.[] | "\(.file):\(.range.start.line + 1): \(.metaVariables.single.ARG.text)"'
```

`--json=compact` gives one line per run and `--json=stream` one object per match, for piping.
