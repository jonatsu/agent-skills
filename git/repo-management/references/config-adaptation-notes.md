# Config adaptation notes

These assets encode the author's preferred repository baseline. Preserve the profile for a new repository;
adapt it when an established repository already carries deliberate conventions.

- Preserve patch/diff safety by default. Formatters and fixing hooks should not rewrite `*.patch` or `*.diff`
  files unless the repo explicitly requests it.
- Add repo-specific exclusions only after confirming generated, vendored, or archived paths with the
  maintainer. Examples: generated docs, snapshots, or bundled third-party directories.
- Keep the active YAML, Markdown, and shell hooks when applying the preferred profile. Add further
  stack-specific hooks only after confirming the stack. Examples include Compose or Kubernetes schema
  checks, language formatters, framework linters, dependency scanners, or release-note validators.
- Add branch protection hooks only after confirming branch names and workflow. Do not assume any default or
  release branch name.
- Avoid wiring config to repo-specific ignore files by default. If a repo wants `.gitignore`-driven ignores,
  add it intentionally and document why.
- Keep comments that explain non-obvious choices, especially preservation of Markdown hard breaks, line-ending
  rules, and patch/diff protections.
- When a formatter and linter govern the same syntax, verify their combined result on a representative
  fixture and repeat the sequence. The second pass must make no changes and every checker must pass.
- Let mdformat be the only Markdown writer and keep markdownlint report-only. Use markdownlint's built-in
  frontmatter handling; a custom regex can expose the closing delimiter as a heading.
- Configure markdownlint with descriptive rule aliases such as `ul-style`; put the corresponding `MDxxx`
  identifier in the adjacent comment. Parameterized rules use an object value such as
  `"ul-style": { "style": "consistent" }`, not a bare style string.
- Keep markdownlint's unordered-list style compatible with mdformat's marker normalization. The shipped
  `consistent` setting is compatible. A 2026-09-03 probe found that markdownlint 0.41.0 silently failed to
  enforce `sublist`; 0.41.1 corrected markers across nested tables, fences, mixed nesting, loose lists,
  interrupted lists, and seven levels without changing alphanumeric content, then reached a clean second
  pass. `sublist` still conflicts with mdformat's single-marker output by design.
- Keep MD060 table-column styling disabled. A 2026-09-03 markdownlint 0.41.1 probe preserved a three-row table
  under compact and aligned modes and reached a clean second pass, but that narrow case does not outweigh the
  table-content loss observed under 0.41.0.
- Mirror every Markdown exclusion in pre-commit's `exclude` and markdownlint-cli2's `ignores`. A stale entry
  in either layer silently creates format-only or lint-only coverage.
- Neither Markdown hook sees a non-breaking space. U+00A0 is not whitespace to a parser, so a nested item or
  fence indented with one leaves its parent block, and the linter then reports a broken list or a missing blank
  line somewhere that reads as correct in every editor. Measured on mdformat 1.0.0 and markdownlint-cli2
  0.23.2: a hard tab in that position fails MD010, while both hooks pass a U+00A0 file and leave the character
  intact. The shipped `markdown-nbsp-indent` hook closes the gap. Keep it report-only so mdformat stays the
  sole writer; `language: pygrep` is built into pre-commit, so it adds no dependency.
- Scope an invisible-character hook to the leading whitespace run rather than banning the character. A mid-line
  U+00A0 is legitimate typography, as in `5000<U+00A0>ms`, and harms no block structure, so a blanket pattern
  fails honest prose. Write the UTF-8 bytes out and use alternation instead of a character class: pygrep
  compiles the entry as a bytes regex, where `[\xc2\xa0]` matches each byte alone and fires on the tail of
  characters such as `à` (`\xc3\xa0`). Single-quote the entry so YAML keeps the backslashes. Select files with
  `types_or: [markdown, mdx]`, because identify tags `.mdx` as `mdx` rather than `markdown`, and a plain
  `types: [markdown]` reports "no files to check" on every MDX file.
- Prove any check-only hook with both controls before trusting it. One file that must fail, one that must pass,
  and then the whole tree. A pattern that never matches and a pattern that matches everything are
  indistinguishable from a working one on a tree that happens to be clean.
- Give wrapping to one tool. The shipped profile uses mdformat `wrap = "keep"`; markdownlint supplies the
  numeric ceiling, and EditorConfig deliberately leaves Markdown line length unset.
- Keep mdformat's line ending at `lf` to agree with the global EditorConfig rule. `keep` leaves CRLF Markdown
  unchanged, so editorconfig-checker fails on every pass while mdformat reports success.
- Do not split an inline code span across physical lines. CommonMark turns its internal line ending into a
  space, so mdformat rejoins the span even when wrapping is set to `keep`.
- Exclude model-facing prompt files from both Markdown tools when formatting changes their payload semantics.
  Prefer narrow rule exceptions when only one rule conflicts.
- Run pre-commit against explicit changed files. Whole-tree formatting can rewrite generated or vendored
  content, and every mutating hook must remain at the `pre-commit` stage.
- Shell repos get both `shellcheck` (lint) and `shfmt` (format) — they only touch shell files via the hooks'
  own file matching, so both stay in the baseline.
- Keep shell formatting in `.editorconfig`, not in `shfmt` flags. shfmt reads `.editorconfig` —
  `indent_style`/`indent_size` plus its extensions (`switch_case_indent`, `binary_next_line`,
  `space_redirects`, `keep_padding`, `function_next_line`) — but ONLY when no formatting flag is passed on the
  command line; any printer flag (`-i`/`-ci`/`-sr`/…) makes shfmt ignore `.editorconfig` entirely. So give the
  shfmt hook operation flags only (e.g. `-w`) and let `.editorconfig` be the single source of truth.
  Do not set shfmt's `shell_variant` property to `auto`: shfmt 3.13.1 passes that value to a parser that does
  not support it and panics. Omit the property so shfmt infers the dialect from the file or shebang.
  `editorconfig-checker` ignores the remaining shfmt extension keys, so the two coexist.
