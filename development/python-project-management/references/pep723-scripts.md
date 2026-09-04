# PEP 723 Inline Script Metadata

Read this when the deliverable is a single file that needs third-party packages. PEP 723 puts the dependency
metadata in the script itself, so there is no `requirements.txt`, no project directory, and nothing for a
reader to install first.

## When It Fits

Use it for a single-file script with dependencies, a piece of automation, or a utility shared between projects
that has to stay self-contained.

Use a `pyproject.toml` project instead once the code spans more than one file, becomes a reusable library, or
needs dependency groups, editable installs, or local path dependencies.

## The Format

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx",
#     "rich",
# ]
# ///

"""Fetch a URL and print the response as formatted JSON."""

import httpx
from rich import print

response = httpx.get("https://api.example.com/data")
response.raise_for_status()
print(response.json())
```

The block is TOML inside a comment, opened by `# /// script` and closed by `# ///`. Every line between them
starts with `#`.

## Managing a Script

```bash
uv init --script myscript.py           # create with the metadata block
uv add --script myscript.py httpx      # add a dependency
uv remove --script myscript.py httpx   # remove one
uv run myscript.py                     # run, installing dependencies as needed
```

## Locking a Script

A script can have a lock. `uv lock --script myscript.py` writes `myscript.py.lock` beside it, and later runs
resolve from it.

```bash
uv lock --script myscript.py
```

Lock a script whose output has to be reproducible or that runs unattended. Leave an ad-hoc script unlocked so
it picks up current versions. Verified against uv 0.12.5 on 2026-09-04.

## Shebangs

```python
#!/usr/bin/env -S uv run --script                  # requires uv on PATH
#!/usr/bin/env -S uv run --python 3.12 --script    # pin the interpreter
#!/usr/bin/env -S uv run --quiet --script          # suppress uv's own output
```

`--quiet` matters when the script's stdout is consumed by something else; without it uv's resolution progress
lands in the same stream.

## A Private Index

```python
# /// script
# dependencies = ["httpx"]
#
# [tool.uv]
# extra-index-url = ["https://pypi.company.com/simple/"]
# ///
```

## Practical Rules

- Always set `requires-python`. It is what selects the interpreter.
- Use a floor, `>=3.11`, not a pin, `==3.11`.
- Let `uv add --script` write the dependency entries rather than typing versions by hand.
- Keep the docstring: a self-contained script has no README to explain it.

## Limits

No dependency groups, no editable installs, and no local path dependencies. A script needing any of those has
outgrown the format; convert it with `uv init --bare` and move the dependencies across.
