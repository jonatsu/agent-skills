# Config adaptation notes

These assets are generic baselines. Keep them small until the repository confirms
stronger needs.

- Preserve patch/diff safety by default. Formatters and fixing hooks should not
  rewrite `*.patch` or `*.diff` files unless the repo explicitly requests it.
- Add repo-specific exclusions only after confirming generated, vendored, or
  archived paths with the maintainer. Examples: generated docs, snapshots, or
  bundled third-party directories.
- Add stack-specific hooks only after confirming the stack. Examples: Compose or
  Kubernetes schema checks, language formatters, framework linters, dependency
  scanners, or release-note validators.
- Add branch protection hooks only after confirming branch names and workflow.
  Do not assume any default or release branch name.
- Avoid wiring config to repo-specific ignore files by default. If a repo wants
  `.gitignore`-driven ignores, add it intentionally and document why.
- Keep comments that explain non-obvious choices, especially preservation of
  Markdown hard breaks, line-ending rules, and patch/diff protections.
- Shell repos get both `shellcheck` (lint) and `shfmt` (format) — they only touch
  shell files via the hooks' own file matching, so both stay in the baseline.
- Keep shell formatting in `.editorconfig`, not in `shfmt` flags. shfmt reads
  `.editorconfig` — `indent_style`/`indent_size` plus its extensions
  (`switch_case_indent`, `binary_next_line`, `space_redirects`, `keep_padding`,
  `function_next_line`) — but ONLY when no formatting flag is passed on the
  command line; any printer flag (`-i`/`-ci`/`-sr`/…) makes shfmt ignore
  `.editorconfig` entirely. So give the shfmt hook operation flags only (e.g.
  `-w`) and let `.editorconfig` be the single source of truth.
  `editorconfig-checker` ignores shfmt's extension keys, so the two coexist.
