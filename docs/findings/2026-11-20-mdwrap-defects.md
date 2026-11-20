# mdwrap Defects

Date: 2026-11-20. Status: every defect below is fixed in `markdown-tools`' `scripts/mdwrap.py`, or kept as a tested
limitation; the tests in `tests/test_markdown_tools_mdwrap.py` reproduce each one.

The earlier `mdwrap.py`, then in `repo-management`, found Markdown structure line by line with regular expressions. It
had no model of containers, such as block quotes and list items, or of inline spans, such as code spans and links.
Agents reported few failures, mostly frontmatter flattened and "run the hooks twice", but synthetic reproductions,
fuzzing, and a run over this repository's Markdown at three widths found the classes below. The rebuild parses with
markdown-it-py and rewrites only paragraph lines. Before writing, it compares the rendering of each document before
and after and refuses any change.

## Defects

01. **Code spans of more than one backtick split.** The scanner flipped a flag on each backtick, so a span written
    with a run of two broke across lines and the hard-break backslash landed inside the code. Fixed: spans follow
    CommonMark's run matching.
02. **Fences inside block quotes and list items joined into prose.** Fixed: the parser decides what is a paragraph.
03. **Deliberate line structure lost.** Two-space breaks and `<br>` disappeared, and short lines such as label lines
    or bare list markers were joined. Fixed: deliberate breaks split a paragraph into separately wrapped segments,
    and a paragraph whose lines all fit is never touched.
04. **Fights with mdformat.** A word such as `2018.` escaped at a line start lost its escape mid-line and regained it
    at the next start, so each tool undid the other. Fixed for line starts. A bracket group that is not a link and
    spans a hard break is still escaped by mdformat; this is a tested limitation.
05. **Silent skips.** An unbalanced bracket or backtick stopped wrapping and exited 0, as did long link text, a
    line starting with inline HTML, list continuations indented four spaces, and footnote first lines. Fixed: these
    wrap, and a paragraph that cannot be rewrapped safely is reported as skipped with its reason.
06. **No soft-wrap mode.** Check mode flagged every multi-line paragraph in a soft-wrapping repository. Fixed with
    `--soft`.
07. **Line length counted differently from the linter.** Every line over the width counted, so a line ending in a
    long URL was flagged even though markdownlint's MD013 accepts a line with no whitespace past the width. Fixed:
    a line is too long only when MD013 would say so.
08. **Tables without leading pipes joined.** Fixed: the parser's table rule recognizes them.
09. **HTML blocks partly rewrapped, and no opt-out.** Fixed: HTML blocks stay byte-identical, and regions between
    `<!-- mdformat off -->` and `<!-- mdformat on -->` are skipped.
10. **Literal backslashes collided with the hard-break marker.** A word ending in a backslash, placed at a line end,
    became an escaped backslash. Fixed: no break follows a word ending in an odd number of backslashes.
11. **A wrapped line could open a block.** A line starting with `***`, `___`, or `|` became a rule or broke
    idempotence. Fixed: such words never start a line.
12. **Line endings and byte-order marks changed.** CRLF became LF, and a byte-order mark hid frontmatter, which was
    then flattened. Fixed: line endings and the mark are preserved.
13. **Partial writes.** A missing file stopped a run after earlier files were written. Fixed: every file is read and
    processed before any is written, through a temporary file and a rename.
14. **A wrapped line could start with a word beginning `#`.** CommonMark reads `#140)` at a line start as text, but
    markdownlint's MD018 fix reads it as a heading missing its space and turns it into `# 140)`. Fixed: no wrapped
    line starts with `#`.
15. **Only MD013's default mode was counted.** A repository that sets MD013's `stern` or `strict` option failed the
    linter while check mode reported nothing to rewrap. Fixed with `--line-length-mode`.

## Limitations

A stranded short last line is not rebalanced. Width counts code points, not display columns. A paragraph that may be
display math (`$$`) is skipped. YAML frontmatter closed by `...` is not recognized. In stern mode, a line holding
only links counts as too long, although MD013 accepts it.
