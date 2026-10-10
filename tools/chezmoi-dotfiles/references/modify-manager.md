# chezmoi_modify_manager

`chezmoi_modify_manager` is an optional, separately installed interpreter for chezmoi modify scripts. It
manages INI-style files that mix settings with program state, such as recent files, window geometry, or
per-machine IDs: chezmoi keeps the settings, and the program keeps the state. Read this only when it is installed
and a target's modify script names it; [Modify Scripts](../SKILL.md#modify-scripts) covers the plain-chezmoi
rules, which still apply.

The installed binary is the authority. Check `chezmoi_modify_manager --help`, `--help-syntax`, and
`--help-transforms` before relying on a flag, directive, or transform named here. This reference follows the
project documentation at commit `62a4c18` and has not been run against the binary.

Contents: how a target is built, capturing changes, directives, templates and re-adding, secrets, diagnosis and
upgrade, verification.

## How a Target Is Built

Each managed file has two source entries:

- `modify_<name>`, or `modify_<name>.tmpl` when it uses chezmoi templating: the directive file, with
  `#!/usr/bin/env chezmoi_modify_manager` as its first line.
- `<name>.src.ini`: the stored settings.

On apply, the tool walks the current file in the home directory and builds the new one:

- A key with no matching directive takes its value from `.src.ini`.
- A key that is absent from `.src.ini` and matched by no directive is deleted.
- An ignored key or section keeps the value from the home directory.
- A key present only in `.src.ini` is appended to the end of its section, and the owning program usually
  reorders it on its next write.

The root `.chezmoiignore` must contain `**/*.src.ini`, so chezmoi does not also deploy the stored settings as
files.

## Capture Changes With the Tool

Plain `chezmoi add` and `re-add` mishandle these targets, so use the tool's own commands:

- `chezmoi_modify_manager --add <target>` starts managing a file, or converts a file chezmoi already manages
  as a plain copy. It writes `.src.ini` and a skeleton directive file.
- `chezmoi_modify_manager --smart-add <target>` re-adds a target the tool already manages, and falls back to
  plain chezmoi for other targets. Use it when it is unclear which one manages the target.

A re-add filters the current file through the directives before writing `.src.ini`, so ignored keys never enter
the source. Review the source diff after every add, as with plain chezmoi.

## Directives

The directive file holds one directive per line, with `#` comments at the start of a line:

```text
#!/usr/bin/env chezmoi_modify_manager
source auto

ignore section "<section>"
ignore "<section>" "<key>"
ignore regex "<section regex>" "<key regex>"
```

- `source auto` locates `.src.ini` and needs chezmoi 2.46.1 or later. On older chezmoi, `--add` writes a templated
  `source` line instead. When some machines run an older chezmoi, set
  `CHEZMOI_MODIFY_MANAGER_ASSUME_CHEZMOI_VERSION` to the oldest version in use, so new directive files work on all
  of them.
- `ignore` keeps the home-directory value for a section or key, and keeps re-adds from copying it into the
  source.
- `set "<section>" "<key>" "<value>"` forces a value, and `remove` deletes matching entries. Both are meant for
  templated, per-machine differences. Check the separator the owning program writes, because `set` defaults to
  `=`; pass `separator="="` when the program writes no spaces.
- `transform` applies a built-in merge rule to a key, such as treating a value as an unordered list.
- `add:hide` keeps a key in the source but replaces its value on re-add; `add:remove` drops it on re-add.
- Use `<NO_SECTION>` as the section name for keys that appear before the first section header.

Choose rules from evidence. Run `chezmoi diff <target>` after the program has been used, or compare the file
across machines, and ignore exactly the keys that change on their own. Prefer exact section and key matches to
regex, because they are faster and cannot match more than intended.

When several directives could match a key, a section match wins, then an exact section-and-key match, then the
first matching regex in file order. The tool warns about overlapping regex matches; add
`no-warn-multiple-key-matches` only when the overlap is intended. Leave `^` and `$` out of regex directives,
because the tool joins section and key into one string before matching, and anchors then match the wrong place.

## Templates and Re-Adding

Apply renders a `.tmpl` directive file through chezmoi, but a re-add reads the directives raw. `ignore`,
`add:hide`, and `add:remove` therefore filter re-adds on every machine, even inside an `{{ if }}` block, and
template expressions in their arguments are not expanded.

Pair each templated `set` with an `add:remove` for the same key, placed outside the `if` block. Otherwise a
re-add on a machine where the `set` applied copies the per-machine value into the shared source.

Re-adding on a machine where `remove` deleted entries drops those entries from `.src.ini` for every machine.
Re-add on a machine that has the complete file, or restore the entries in the source by hand.

## Secrets

Keep a credential in the system keyring instead of `.src.ini`. Combine a keyring transform with `add:hide` for
the same key:

```text
transform "<section>" "<key>" keyring service="<service>" user="<user>"
add:hide "<section>" "<key>"
```

`add:hide` keeps the key in the source with its value hidden, and the keyring transform needs that key present to
fill in the value. Storing the value with `chezmoi_modify_manager --keyring-set <service> <user>` prompts for the
secret, so the user runs it.

## Diagnose and Upgrade

Run `chezmoi_modify_manager --doctor` first when a target misbehaves. It checks that the tool is on `PATH`, that
`.chezmoiignore` excludes `**/*.src.ini`, and the chezmoi version handling.

`chezmoi_modify_manager --upgrade` downloads and replaces the binary from GitHub releases. Run it only with the
user's approval, and prefer the package manager that installed the tool.

## Verify

The change is done when `chezmoi cat <target>` shows the intended settings, `chezmoi diff <target>` shows no
change to the ignored keys, and the source diff contains no state or secret values.
