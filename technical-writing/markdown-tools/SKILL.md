---
name: markdown-tools
description: "Rewrap Markdown prose to a line limit and check Markdown files mechanically: broken relative links and heading anchors, links lost in a reference-style conversion, and words lost when a document is moved, merged, or split. Use after editing Markdown when lines run past the limit or a linter reports line length, after moving files or renaming headings, and to prove a restructure dropped nothing. Not for wording (writing-for-humans), document structure (writing-documentation), Mermaid rendering (mermaid-diagrams), or lint configuration (lint-config-audit)."
license: MIT
metadata:
  author: Joonas Onatsu
---

# Markdown Tools

Mechanical rewrites and checks for Markdown files, each one a command with a verdict. Run them after editing
Markdown and before the repository's own hooks. Wording belongs to `writing-for-humans`, document structure to
`writing-documentation`, and Mermaid blocks to `mermaid-diagrams`, which carries their render check.

Run each bundled script from this skill's directory, and read its `--help` before the first call.

## Rewrap Prose

Follow the repository's wrap convention. The preferred one wraps prose at the line limit and ends every line of a
paragraph but the last with a trailing-backslash hard break (`\`). A soft wrap keeps only the raw file short: the
rendered page joins it into one long line. The backslash, unlike two trailing spaces, stays visible and survives
editors that trim whitespace. Where a repository already soft-wraps, keep its convention.

```bash
python3 scripts/mdwrap.py docs/guide.md            # list the blocks it would change; exits 1 if any
python3 scripts/mdwrap.py --write docs/guide.md    # rewrap them in place
```

Set `--width` to the repository's line limit, such as markdownlint's `line_length`; it defaults to 120. The script
leaves front matter, headings, tables, code, reference definitions, HTML blocks and alert markers alone. It keeps
every code span and link on one line, and keeps list, heading, quote and fence markers off the start of a wrapped
line.

Rewrapping is done when check mode exits 0 and the repository's Markdown hooks pass. Run the hooks twice, because a
formatter such as mdformat can change a rewrapped line once more.

## Check Links and Anchors

Use [lychee](https://github.com/lycheeverse/lychee), a maintained link checker, rather than a script. Offline, it
checks every relative link's target file, every `#fragment` against the target's headings with GitHub's slug rules,
and reference-style definitions, without touching the network:

```bash
lychee --offline --include-fragments --no-progress docs/*.md README.md
```

It prints each broken link with its file, line and column, and exits 2 when any link is broken. Install it with a
package manager, `mise use -g lychee`, or `cargo install lychee`. A repository can run it as a pre-commit hook:

```yaml
- repo: https://github.com/lycheeverse/lychee.git
  rev: lychee-v0.24.2
  hooks:
    - id: lychee
      args: ["--offline", "--include-fragments", "--no-progress"]
```

Run it after moving or renaming a file, and after changing a heading. The check is done when it exits 0.

## Attributions

See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for the sources this skill is based on.
