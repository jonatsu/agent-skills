# Run Scripts and Ignore Rules

## Table of Contents

- [Run Scripts](#run-scripts)
- [OS-Scoped Script Directories](#os-scoped-script-directories)
- [Reset run_once_ Scripts](#reset-run_once_-scripts)
- [Ignore Rules](#ignore-rules)

## Run Scripts

Scripts in source directory run automatically during `chezmoi apply`. Naming prefix controls when:

- `run_once_` — first apply only (result recorded in state)
- `run_onchange_` — when script content changes
- `run_always_` — every apply
- `run_before_` / `run_after_` — relative to file writes (composable: `run_once_before_`)

Two-digit numeric infix (`NN`) controls ordering within a phase:

```
run_onchange_before_00-decrypt-key.sh.tmpl   # runs first
run_onchange_before_10-install-pkgs.sh.tmpl  # runs second
run_onchange_after_00-rehash.sh.tmpl
```

## OS-Scoped Script Directories

Place scripts under `.chezmoiscripts/<os>/` to limit execution to a platform:

```
.chezmoiscripts/
├── linux/
│   └── run_onchange_before_00-install-pkgs.sh.tmpl
├── windows/
│   └── run_onchange_before_00-install-pkgs.ps1.tmpl
└── run_always_after_99-reload.sh.tmpl   # all platforms
```

`<os>` matches `.chezmoi.os`: `linux`, `darwin`, `windows`. Scripts outside a subdirectory run on all platforms.

Example `run_once_install-packages.sh.tmpl`:

```bash
#!/bin/bash
{{ if eq .chezmoi.os "darwin" -}}
brew install ripgrep fd bat
{{ else if eq .chezmoi.osRelease.id "ubuntu" -}}
sudo apt-get install -y ripgrep fd-find bat
{{ end -}}
```

## Reset run_once_ Scripts

Force re-execution on next apply:

```bash
chezmoi state delete-bucket --bucket=scriptState
```

Reference: https://www.chezmoi.io/reference/special-directories/chezmoi-scripts/

## Ignore Rules

`.chezmoiignore` lists source paths chezmoi should not manage. Supports `.tmpl` suffix, making ignore rules platform-conditional:

```
# Always ignore
node_modules
**/.DS_Store

# Platform-conditional — only ignore on non-Linux hosts
{{ if ne .chezmoi.os "linux" -}}
dot_config/systemd/
{{ end -}}

# Tool-conditional — ignore if binary not present
{{ if not (lookPath "nvim") -}}
dot_config/nvim/
{{ end -}}
```

`lookPath "binary"` returns path if found in `$PATH`, empty string otherwise. Use `| not | not` to coerce to bool, or wrap in `if` directly (empty string is falsy).

Reference: https://www.chezmoi.io/reference/special-files/chezmoiignore/
