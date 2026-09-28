# Run Recipes in GitHub Actions

When a workflow needs Just, inspect its existing tool installation and version policy. If it does not already
install Just, use [extractions/setup-just](https://github.com/extractions/setup-just) before the first `just`
step. Check the action's current README for the release tag and inputs rather than copying a remembered version.
Set `just-version` when the project pins its toolchain or needs a minimum feature; the action otherwise selects
the latest matching Just release. For a basic workflow with checkout already configured:

```yaml
steps:
  - uses: extractions/setup-just@v4
  - run: just check
```

Keep the workflow's working directory and environment consistent with local invocation. Preview the recipe
and its dependencies before placing it in CI, especially when it writes, deploys, or needs secrets. Verify the
workflow's selected Just version supports the justfile syntax.
