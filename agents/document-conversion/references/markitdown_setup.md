# MarkItDown Setup

Read this when `SKILL.md` sends you here to install or verify MarkItDown. anydoc needs no setup beyond an
installed tool, so nothing here applies to it.

New code should use `result.markdown`;
`result.text_content` remains only as a soft-deprecated compatibility alias.

## Check before installing

```bash
markitdown --version
python3 <skill-root>/scripts/inspect_installation.py
```

`inspect_installation.py` runs without either converter present and reports both, plus the extras, plugin
entry points and external executables available. It exits non-zero only when **neither** converter is
usable, because either one alone satisfies most of this skill's job. It reports each installed converter's version
without judging it; compare against SKILL.md's Sources section when a detail here looks wrong.

**A CLI on `PATH` is not the same as an importable library.** The bundled conversion scripts do
`import markitdown`, so they need an interpreter that can see the package. A `markitdown` installed through
pipx, `uv tool`, or mise's `pipx:` backend satisfies the shell command but not the import, because each
installs into an isolated environment of its own.

That isolation is not a dead end: **the console script's shebang names the interpreter that can import it.**

```bash
MARKITDOWN_PYTHON=$(head -1 "$(command -v markitdown)" | sed 's|^#!||')
"$MARKITDOWN_PYTHON" <skill-root>/scripts/inspect_installation.py
"$MARKITDOWN_PYTHON" <skill-root>/scripts/batch_convert.py documents/ markdown/
```

This needs no second install and no network, and it survives an upgrade because nothing version-specific is
written down. It works for any installer that produces a console script, which is all of the above.

Check it before relying on it: `inspect_installation.py` under that interpreter should report
`import health: OK`. If the shebang points at a wrapper rather than a real interpreter, fall back to an
ephemeral environment instead:

```bash
uv run --with "markitdown[all]" python <skill-root>/scripts/batch_convert.py documents/ markdown/
```

## Install

```bash
uv venv --python 3.12 .venv
source .venv/bin/activate
```

Every built-in feature:

```bash
uv pip install "markitdown[all]"
```

Or only the converters the task needs:

```bash
uv pip install "markitdown[pdf,docx,pptx,xlsx]"
```

Available extras (confirm against the installed package's metadata):

- `pptx`, `docx`, `xlsx`, `xls`, `pdf` and `outlook`
- `audio-transcription` and `youtube-transcription`
- `az-doc-intel` and `az-content-understanding`
- `all`

Verify with the same two commands used above.

**`[all]` does not install the separate `markitdown-ocr` plugin or an OpenAI-compatible client.** Those are
separate installs; `ocr.md` covers them.

## Converting a binary stream

Use a binary, seekable stream and supply metadata when the stream has no filename:

```python
from markitdown import MarkItDown, StreamInfo

converter = MarkItDown()

with open("report.pdf", "rb") as stream:
    result = converter.convert_stream(
        stream,
        stream_info=StreamInfo(
            extension=".pdf",
            mimetype="application/pdf",
            filename="report.pdf",
        ),
    )

print(result.markdown)
```

Non-seekable streams are copied fully into memory before conversion.

## CLI controls worth knowing

```bash
markitdown --list-plugins
markitdown --use-plugins document.pdf -o document.md
markitdown image.bin -x .png -m image/png -o image.md
markitdown page.html --keep-data-uris -o page.md
```

`--keep-data-uris` can make output very large and may preserve embedded sensitive data. Enable it only when
the task requires it.

## MCP server

See `mcp_and_plugins.md` for installing, running, and securing MarkItDown's MCP server.
