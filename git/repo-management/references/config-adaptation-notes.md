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
