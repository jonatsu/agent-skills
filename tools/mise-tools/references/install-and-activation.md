## Install choices

Default install paths from upstream docs:

- universal install script, usually to `~/.local/bin/mise`
- package managers like brew, apt, dnf, scoop, winget, chocolatey, or snap
- vendored bootstrap script for CI or pinned automation

Prefer:

- local developer shell → regular install plus `mise activate <shell>`
- CI or agents → install mise, then use `mise exec --` or shims
- reproducible automation → vendored installer
  (`mise generate install-script --localize --write <path>`)
- containers with mounted home dirs → system installs with `mise install --system`

## Bound a large or slow cold install

Keep install-specific concurrency and timeout tuning command scoped. The `jobs` setting and `MISE_JOBS` also
bound ordinary `mise run` task concurrency, so a persistent low value slows unrelated daily work.

For a cold install with many tools or a fragile network, start with two concurrent jobs and two-minute network
timeouts while preserving caller overrides:

```sh
MISE_JOBS="${MISE_JOBS:-2}" \
MISE_HTTP_TIMEOUT="${MISE_HTTP_TIMEOUT:-2m}" \
MISE_FETCH_REMOTE_VERSIONS_TIMEOUT="${MISE_FETCH_REMOTE_VERSIONS_TIMEOUT:-2m}" \
mise install
```

These settings bound different operations:

- `MISE_JOBS` limits concurrent installation work and task execution.
- `MISE_HTTP_TIMEOUT` limits connection setup and each stalled response read. The read timer resets when data
  arrives.
- `MISE_FETCH_REMOTE_VERSIONS_TIMEOUT` limits remote version discovery.
- `MISE_HTTP_DOWNLOAD_TIMEOUT` limits one artifact's complete download, including retries and backoff.

Inspect the installed version's settings before changing its defaults. Extend the complete-download timeout
only when that budget fails. Increase a stalled-read or version-discovery timeout from the two-minute recovery
baseline only when evidence shows that the operation still makes progress; a very long timeout makes a dead
endpoint look like a slow one.

## Activation model guide

### `mise exec -- <command>`

Use when:

- writing scripts
- running CI steps
- issuing agent tool calls
- avoiding shell rc edits

Benefits:

- no prompt hook required
- exact command-scoped environment
- least surprising for automation

### `mise activate <shell>`

Use when:

- the user wants an interactive developer shell
- prompt-based env refresh is acceptable

Caveats:

- intended for interactive rc files, not login-only startup files
- adds some prompt overhead
- requires shell restart or re-source after edits

### `mise activate --shims`

Use when:

- non-interactive shells or editors need tool resolution
- prompt hooks are unreliable
- CI needs PATH-based access

Caveat:

- plain shell commands do not automatically get project `[env]` values unless a shimmed tool invocation
  triggers mise

## Shell mutation rules

Edit shell rc files only when the request already authorizes interactive-shell integration or the user
separately confirms that scope.

Prefer no-shell-mutation setups when:

- an agent can use `mise exec --`
- CI can call `mise exec --`
- the project only needs repeatable commands, not a fully activated interactive shell

## Container and image notes

- For image-baked tools that must survive mounted home directories, use `mise install --system`.
- Minimal images may require explicit libc handling.
- OCI support exists but is experimental.
- Alpine or other musl-centric images can complicate prebuilts.

## Verification commands

- `mise --version`
- `mise doctor`
- `mise env`
- `mise exec -- <tool> --version`
- `mise install --dry-run` to inspect missing tools without installing them

## Footguns

- Adding `mise activate` to the wrong shell startup file
- Expecting `mise use` inside a script to immediately expose the tool without `mise exec --`
- Baking user-home installs into containers where `~` will be mounted over later
