# High-impact ast-grep examples

Use these examples as starting shapes, not as unreviewed repository-wide fixes. Test each rule against a small
matching and non-matching fixture, preview every fix, and adapt language or framework details to the target.

Save one YAML fence as `rule.yml`, then use the same file for each stage:

```bash
# Inspect matches and proposed replacements without writing.
ast-grep scan --rule rule.yml --json=stream <path>

# Review and apply selected fixes interactively.
ast-grep scan --rule rule.yml --interactive <path>

# Apply every fix only after the preview and working-tree checks pass.
ast-grep scan --rule rule.yml --update-all <path>
```

A rule without `fix:` only reports matches. A multi-document file separated by `---`, such as the API
migration below, runs all of its rules in one scan on ast-grep 0.45.3.

## Find Async Functions Without Error Handling

This structural audit finds Python functions that contain `await` but no `try` statement. Whitespace, line
breaks, and the awaited expression do not matter.

```yaml
id: async-without-error-handling
language: python
rule:
  all:
    - kind: function_definition
    - has:
        pattern: await $EXPR
        stopBy: end
    - not:
        has:
          kind: try_statement
          stopBy: end
```

## Coordinate an API Migration

Multiple YAML documents can migrate related syntax in one rule file. This catalog example updates the import,
client initialization, and call site together instead of relying on three unrelated text replacements.

```yaml
id: import-openai
language: python
rule:
  pattern: import openai
fix: from openai import Client
---
id: rewrite-client
language: python
rule:
  pattern: openai.api_key = $KEY
fix: client = Client($KEY)
---
id: rewrite-chat-completion
language: python
rule:
  pattern: openai.Completion.create($$$ARGS)
fix: |-
  client.completions.create(
    $$$ARGS
  )
```

## Restrict a Performance Rewrite to Safe Contexts

A list comprehension cannot always become a generator. This rule rewrites it only when passed directly to a
known iterable consumer. The constraint supplies the semantic boundary that a broad text replacement lacks.

```yaml
id: prefer-generator-expressions
language: python
rule:
  pattern: $FUNC($LIST)
constraints:
  LIST:
    kind: list_comprehension
  FUNC:
    any:
      - pattern: any
      - pattern: all
      - pattern: sum
transform:
  INNER:
    substring:
      source: $LIST
      startChar: 1
      endChar: -1
fix: $FUNC($INNER)
```

The official [rule catalog](https://ast-grep.github.io/catalog/) contains further examples for scoped pytest
fixture refactors, recursive type modernization, framework migrations, security checks, and other languages.
