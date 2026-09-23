# ast-grep rule reference

Rule syntax for `ast-grep scan`. A rule is a declarative condition an AST node must satisfy. Rules come in
three categories:

- **Atomic** — match one node by an intrinsic property: `pattern`, `kind`, `regex`, `nthChild`, `range`.
- **Relational** — match by position relative to other nodes: `inside`, `has`, `precedes`, `follows`.
- **Composite** — combine other rules: `all`, `any`, `not`, `matches`.

Every field of a rule object is optional, but at least one positive key (such as `kind` or `pattern`) must be
present. A node matches a rule object when it satisfies **every** field in it — an implicit AND. Where a
metavariable captured by one field is used by another, wrap the fields in an explicit `all` so the matching
order is guaranteed.

| Property   | Type                     | Category   | Purpose                                          |
| ---------- | ------------------------ | ---------- | ------------------------------------------------ |
| `pattern`  | string or object         | atomic     | Match a node by code pattern                     |
| `kind`     | string                   | atomic     | Match a node by its tree-sitter kind name        |
| `regex`    | string                   | atomic     | Match a node's text by Rust regex                |
| `nthChild` | number, string or object | atomic     | Match by index among the parent's children       |
| `range`    | range object             | atomic     | Match by character position                      |
| `inside`   | object                   | relational | Node is inside a node matching the sub-rule      |
| `has`      | object                   | relational | Node has a descendant matching the sub-rule      |
| `precedes` | object                   | relational | Node appears before a node matching the sub-rule |
| `follows`  | object                   | relational | Node appears after a node matching the sub-rule  |
| `all`      | list of rules            | composite  | Every sub-rule matches                           |
| `any`      | list of rules            | composite  | Some sub-rule matches                            |
| `not`      | object                   | composite  | The sub-rule does not match                      |
| `matches`  | string                   | composite  | A named utility rule matches                     |

## Atomic Rules

### pattern

String form matches directly with ast-grep pattern syntax:

```yaml
pattern: console.log($ARG)
```

Object form controls parsing when the pattern alone is ambiguous:

- `context` supplies surrounding code so the snippet parses as the intended construct.
- `selector` picks which node of the parsed context is the actual matcher.
- `strictness` selects the matching algorithm: `cst`, `smart` (default), `ast`, `relaxed`, `signature`.

```yaml
pattern:
  selector: field_definition
  context: class { $F }
```

Reach for `context`/`selector` when a fragment cannot stand alone as a statement — a class field, an object
entry, a `case` arm.

### kind

Matches by the tree-sitter node kind name from the language's grammar, such as `call_expression` or
`function_declaration`. Kind names are language-specific: confirm one with
`ast-grep run --pattern '<snippet>' --lang <lang> --debug-query=cst` rather than assuming it.

### regex

Matches the node's **entire** text against a Rust regex. It is not a positive rule, so pair it with a `kind`
or `pattern` rather than using it alone.

### nthChild

Matches by 1-based index among the parent's children, counting named nodes only.

- A number matches that exact position.
- A string uses the `An+B` formula, for example `2n+1`.
- An object takes `position`, `reverse: true` to count from the end, and `ofRule` to filter the sibling list
  before counting.

### range

Matches a node by character position. `start` and `end` each take 0-based `line` and `column`; `start` is
inclusive and `end` is exclusive. Useful for driving ast-grep from another tool's output, not for authored
rules.

## Relational Rules

```yaml
inside:
  pattern: class $C { $$$ }
  stopBy: end
has:
  pattern: await $EXPR
  stopBy: end
```

`precedes` and `follows` take `stopBy` but not `field`.

### stopBy

Controls where the relational search stops:

- `neighbor` (**default**) — stop as soon as the immediately surrounding node does not match.
- `end` — search to the end of the direction: the root for `inside`, the leaves for `has`.
- a rule object — stop at the first surrounding node matching that rule, inclusive.

The default is the single most common cause of a relational rule matching nothing. Use `stopBy: end` unless
a shallow search is specifically what you want.

### field

Restricts the relation to a named sub-node of the target, for example the `operator` field of a binary
expression. Available on `inside` and `has` only.

## Composite Rules

```yaml
all:                              # every sub-rule; also fixes matching order
  - kind: call_expression
  - pattern: console.log($ARG)

any:                              # some sub-rule
  - pattern: console.log($$$)
  - pattern: console.warn($$$)

not:                              # the sub-rule must not match
  pattern: console.log($ARG)
```

`matches: <rule-id>` references a utility rule by id, which is how rules are reused and how recursive rules
are written.

## Metavariables

| Form     | Captures                                  |
| -------- | ----------------------------------------- |
| `$VAR`   | one **named** node                        |
| `$$VAR`  | one **unnamed** node, such as an operator |
| `$$$VAR` | zero or more nodes, non-greedy            |
| `$_VAR`  | matches but does not capture              |

Names must be uppercase letters, digits and underscores: `$META`, `$META_VAR` and `$_` are valid; `$invalid`,
`$123` and `$KEBAB-CASE` are not.

Reusing a name constrains equality — `$A == $A` matches `a == a` but not `a == b`. An underscore-prefixed name
does not capture, so `$_FUNC($_FUNC)` matches `test(a)` as well as `testFunc(1 + 1)`.

`$$$` absorbs a variable number of arguments or statements: `console.log($$$)` matches every arity, and
`function $FUNC($$$ARGS) { $$$ }` matches any function.

Two constraints decide whether a metavariable works at all:

- Only the exact syntax above is recognized.
- The metavariable must be the **entire** text of its node. `obj.on$EVENT`, `"Hello $WORLD"`, `a $OP b` and
  `$jq` all fail. For the operator case, match the node instead:

```yaml
rule:
  kind: binary_expression
  has:
    field: operator
    pattern: $$OP
```

## Worked Rules

Functions containing an `await`:

```yaml
rule:
  kind: function_declaration
  has:
    pattern: await $EXPR
    stopBy: end
```

`console.log` inside a class method:

```yaml
rule:
  pattern: console.log($$$)
  inside:
    kind: method_definition
    stopBy: end
```

Async functions using `await` with no surrounding try/catch:

```yaml
rule:
  all:
    - kind: function_declaration
    - has:
        pattern: await $EXPR
        stopBy: end
    - not:
        has:
          pattern: try { $$$ } catch ($E) { $$$ }
          stopBy: end
```

See [examples.md](examples.md) for larger Python audits and rewrites adapted from the official catalog.

## Rule Lifecycle and JSON Output

Use `ast-grep new rule` to scaffold a reusable rule and `ast-grep test` to run its snapshot cases. Keep the
small matching and non-matching examples with the rule so a later edit proves both sides of its boundary.

`run --json` and `scan --json` emit a bare match array. `range.start.line` is 0-based. A `$$$REST` capture
appears under `metaVariables.multi` and includes unnamed separator nodes. For example,
`console.log($ARG, $$$REST)` against `console.log("value", 1, 2)` captures `1`, `,`, and `2`, not two
arguments. Filter node kinds before counting. Use `--json=compact` for one line per run or `--json=stream` for
one object per match.

## When a Rule Matches Nothing

1. Dump the real structure with `--debug-query=cst` before adjusting the rule.
2. Add `stopBy: end` to every relational rule.
3. Check each `kind` against that dump, not against the grammar you expect.
4. Confirm each metavariable is the whole text of its node.
5. Strip the rule to its simplest positive part, then add conditions back one at a time.
