# MarkItDown Setup

Read this when `SKILL.md` sends you here to install or verify MarkItDown. anydoc needs no setup beyond the
pinned tool, so nothing here applies to it.

This skill targets **MarkItDown 0.1.7**, released 29 July 2026. New code should use `result.markdown`;
`result.text_content` remains only as a soft-deprecated compatibility alias.

## Check before installing

```bash
markitdown --version
python3 <skill-root>/scripts/inspect_installation.py
```

`inspect_installation.py` runs without either converter present and reports both, plus the extras, plugin
entry points and external executables available. It exits non-zero only when **neither** converter is
usable, because either one alone satisfies most of this skill's job. The version gate applies to a converter
that is actually installed: an installed converter that is not the skill's target version also exits
non-zero, so pass `--allow-version-mismatch` when a nearby release is acceptable.

**A CLI on `PATH` is not the same as an importable library.** The bundled conversion scripts do
`import markitdown`, so they need an interpreter that can see the package. A `markitdown` installed through
pipx or mise satisfies the shell command but not the import.

## Install

```bash
uv venv --python 3.12 .venv
source .venv/bin/activate
```

Every built-in feature:

```bash
uv pip install "markitdown[all]==0.1.7"
```

Or only the converters the task needs:

```bash
uv pip install "markitdown[pdf,docx,pptx,xlsx]==0.1.7"
```

Available extras in 0.1.7:

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

```bash
uv pip install "markitdown==0.1.7" "markitdown-mcp==0.0.1a4"
markitdown-mcp
```

`mcp_and_plugins.md` covers transports and their security properties.
