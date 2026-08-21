# Templates, Variables, Partials

## Table of Contents

- [Convert to Template](#convert-to-template)
- [Common Template Patterns](#common-template-patterns)
- [Custom Variables](#custom-variables)
- [Inspect and Verify](#inspect-and-verify)
- [Template Partials](#template-partials)
- [Caution: re-adding template-managed files](#caution-re-adding-template-managed-files)

## Convert to Template

```bash
chezmoi add --template ~/.config/app/config.toml    # add as template
chezmoi chattr +template ~/.config/app/config.toml  # convert in-place (already managed)
```

## Common Template Patterns

```
# OS-conditional
{{ if eq .chezmoi.os "darwin" -}}
export HOMEBREW_PREFIX="/opt/homebrew"
{{ else if eq .chezmoi.os "linux" -}}
export HOMEBREW_PREFIX="/home/linuxbrew/.linuxbrew"
{{ end -}}

# Architecture-conditional
{{ if eq .chezmoi.arch "arm64" -}}
ARCH="aarch64"
{{ else -}}
ARCH="x86_64"
{{ end -}}

# Hostname-conditional
{{ if eq .chezmoi.hostname "work-laptop" -}}
export HTTP_PROXY="http://proxy.example.com:8080"
{{ end -}}

# Linux distro-conditional
{{ if eq .chezmoi.osRelease.id "ubuntu" -}}
alias update="sudo apt update && sudo apt upgrade"
{{ else if eq .chezmoi.osRelease.id "fedora" -}}
alias update="sudo dnf upgrade"
{{ end -}}

# Custom variable from [data] in chezmoi.toml
git_email = "{{ .email }}"
```

## Custom Variables

`~/.config/chezmoi/chezmoi.toml`:

```toml
[data]
  email = "user@example.com"
  editor = "nvim"
```

## Inspect and Verify

```bash
chezmoi data                                   # all template variables as JSON
chezmoi execute-template '{{ .chezmoi.os }}'   # test a snippet inline
chezmoi cat ~/.config/app/config.toml          # rendered output without applying
```

Built-in variables: https://www.chezmoi.io/reference/templates/variables/

## Template Partials

Reusable template fragments live in `.chezmoitemplates/` inside source directory. Include in any `.tmpl` file:

```
{{- template "fragment-name.tmpl" . }}
```

`.` passes full template data context through. Partials useful for shared shell env setup, common aliases, repeated config blocks.

Reference: https://www.chezmoi.io/reference/special-directories/chezmoitemplates/

## Caution: re-adding template-managed files

`chezmoi re-add` expands rendered destination back into source, overwriting `.tmpl` syntax. Check first:

```bash
chezmoi source-path ~/.config/app/config.toml
# If output ends in .tmpl → use chezmoi edit, not re-add
chezmoi edit ~/.config/app/config.toml
```
