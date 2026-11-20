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

Run each bundled script from this skill's directory with `uv run`, which installs the Markdown parser the script
declares; plain `python3` works only where `markdown-it-py` and `mdit-py-plugins` are installed. Read a script's
`--help` before its first call. Each prints one finding per line as `path:line: message`, and exits 0 when it finds
nothing, 1 when it finds something, and 2 on a usage error or a missing dependency.

## Rewrap Prose

Follow the repository's wrap convention. The preferred one wraps prose at the line limit and ends every line of a
paragraph but the last with a trailing-backslash hard break (`\`). A soft wrap keeps only the raw file short: the
rendered page joins it into one long line. The backslash, unlike two trailing spaces, stays visible and survives
editors that trim whitespace. Where a repository already soft-wraps, keep its convention.

Pass `--soft` in a soft-wrapping repository; without it, the script writes hard breaks.

```bash
uv run scripts/mdwrap.py docs/guide.md            # list the paragraphs it would rewrap
uv run scripts/mdwrap.py --write docs/guide.md    # rewrap them in place
```

Set `--width` to the repository's line limit, such as markdownlint's `line_length`; it defaults to 120. A line counts
as too long the way markdownlint counts it: past the width with whitespace beyond it, so a line ending in a long URL
passes. Only a paragraph with such a line is rewrapped, and everything outside paragraphs stays byte-identical. Code
spans, inline HTML, autolinks, and link destinations never break, and a two-space or `<br>` break the author wrote
stays. The script refuses any rewrap that would change the rendered output, and reports that paragraph as
`skipped` with its reason; fix a skipped paragraph by hand. It writes nothing unless every file it was given parses.

Pass `--line-length-mode stern` or `strict` when the repository's MD013 configuration sets that option.

Run the linter without `--fix` first, and review the diff of anything `--fix` changes. Its list renumbering (MD029)
changes step numbers without updating prose that cites a step by number.

Rewrapping is done when check mode exits 0 and the repository's Markdown hooks pass.

## Check Links and Anchors

Use [lychee](https://github.com/lycheeverse/lychee), a maintained link checker, rather than a script. Offline, it
checks every relative link's target file, every `#fragment` against the target's headings with GitHub's slug rules,
reference-style definitions, and `<img src>` in HTML blocks, without touching the network:

```bash
lychee --offline --include-fragments --no-progress --root-dir . .
```

Add `--root-dir .` when the documents use root-relative links such as `/docs/setup.md`; without it, lychee reports
every one of them as unresolvable, valid or not. Renaming a heading breaks links in files the commit never touched,
so check the whole tree, not only the changed files.

It prints each broken link with its file, line and column, and exits 2 when any link is broken. Install it with a
package manager, `mise use -g lychee`, or `cargo install lychee`. A repository can run it as a pre-commit hook:

```yaml
- repo: https://github.com/lycheeverse/lychee.git
  rev: lychee-v0.24.2
  hooks:
    - id: lychee
      args: ["--offline", "--include-fragments", "--no-progress", "--root-dir", ".", "."]
      pass_filenames: false
```

Run it after moving or renaming a file, and after changing a heading. The check is done when it exits 0.

## Verify a Reference-Link Conversion

Converting inline links to reference-style links rewrites every link's source, so a destination, a fragment, or a
link's text can change unseen. Give `reflinks.py` each file's version from before the conversion and the version
after; it never runs Git, so produce the old version yourself:

```bash
git show HEAD:docs/guide.md > /tmp/guide-old.md
uv run scripts/reflinks.py /tmp/guide-old.md docs/guide.md
```

It reports each link lost or added, each definition nothing uses, and each `[label]` with no definition, which
renders as plain text. A changed link shows as lost at its old line and added at its new line. The conversion is
done when it exits 0.

## Verify a Restructure Lost Nothing

Moving, merging, or splitting documents should keep every word that carried content. `tokendiff.py` counts the
word tokens in the source files and the destination files, skipping code blocks, Mermaid, front matter, and link
destinations, and lists every token the destination has fewer of:

```bash
git show HEAD:docs/install.md > /tmp/install.md
git show HEAD:docs/upgrade.md > /tmp/upgrade.md
uv run scripts/tokendiff.py --from /tmp/install.md /tmp/upgrade.md --to docs/setup.md
```

Account for every lost token: restore it, or confirm that its loss was deliberate, such as a removed duplicate or
filler. Pass deliberate losses with `--ignore WORD` or `--ignore-file FILE`. The restructure is done when it exits
0 with those ignores.

## Attributions

See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for the sources this skill is based on.
