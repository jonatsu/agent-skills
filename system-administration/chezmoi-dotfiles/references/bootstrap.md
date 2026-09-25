# Set Up Chezmoi on a New Machine

Read this when initializing an empty source directory or bringing an existing dotfiles repository to a new
machine. Check the installed `chezmoi init --help` before using version-sensitive options. See the official
[setup guide](https://www.chezmoi.io/user-guide/setup/) and
[`init` reference](https://www.chezmoi.io/reference/commands/init/) for the current contract.

First, identify the intended source repository and target home directory. Inspect any existing chezmoi source,
configuration, and actual files; an existing setup or local changes need reconciliation before initialization.
Do not infer a GitHub repository from a username when the user or repository has named a specific remote.

The committed `.chezmoi.$FORMAT.tmpl` lives at the source root. `chezmoi init` renders it into a per-machine
configuration file before applying targets. Confirm that the source repository contains the intended template
and that its prompts and secret backends can work on the new machine. Do not commit the generated local config
or any credentials it contains. The
[config template reference](https://www.chezmoi.io/reference/special-files/chezmoi-format-tmpl/) defines its
available data and functions.

Initialize without `--apply` when the targets and scripts still need review. Then inspect `chezmoi status`,
`chezmoi diff`, the selected configuration, scripts, externals, removals, and secrets. An apply preview can run
configured hooks, so inspect their effects before `chezmoi apply --dry-run --verbose`. Apply only the authorized
scope, then run `chezmoi verify` and check the remaining status. `init --apply` combines initialization with
that application step; use it only after the same review is complete.
