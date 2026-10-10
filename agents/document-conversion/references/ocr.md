# Vision Descriptions and OCR

This guide distinguishes two features that are often conflated:

1. Built-in image metadata/description
2. Official `markitdown-ocr` vision plugin

MarkItDown also ships Azure Document Intelligence and Azure Content Understanding integrations, behind the
`az-doc-intel` and `az-content-understanding` extras. They are not documented here; read the upstream guide
if a task needs cloud layout extraction, structured custom fields, audio, or video.

## Decision Guide

| Requirement                                             | Best fit                                                 |
| ------------------------------------------------------- | -------------------------------------------------------- |
| Describe a standalone JPEG/PNG or images on PPTX slides | Built-in `llm_client` path                               |
| Read text from PDF/DOCX/PPTX/XLSX embedded images       | `markitdown-ocr`                                         |
| OCR scanned PDFs                                        | `markitdown-ocr` full-page fallback, or an Azure service |
| Data must remain local                                  | Use a separate local OCR/layout parser                   |

Neither built-in descriptions nor the official plugin is a local Tesseract workflow. Both send image bytes to
an external provider.

## Data-Handling Rule

Run `security.md`'s Preflight Checklist before using an external OCR or vision provider. OCR-specific: each
selected image or page becomes a separate provider call, so estimate the per-page cost before sending a large
scanned document.

## Built-in Image Descriptions

The built-in JPEG/PNG and PPTX paths can call an OpenAI-compatible client. MarkItDown encodes image bytes as a data
URI and calls:

```text
client.chat.completions.create(model=..., messages=...)
```

Install a reviewed client version:

```bash
uv pip install "markitdown[pptx]" "openai"
```

```python
from markitdown import MarkItDown
from openai import OpenAI

# The SDK obtains only its named provider credential through its normal
# configuration. The image and prompt are sent to that provider.
client = OpenAI()

converter = MarkItDown(
    llm_client=client,
    llm_model="gpt-4o",
    llm_prompt=(
        "Describe the scientific figure. Transcribe visible labels, identify "
        "axes and units, and report trends without inventing missing values."
    ),
)

result = converter.convert_local("figure.png")
print(result.markdown)
```

Use a provider/model approved by the user; model identifiers and availability are provider-specific.

### Limitations

- Built-in image conversion accepts JPEG and PNG.
- Without ExifTool or an LLM client, output can be empty.
- A description is not guaranteed OCR or quantitative chart extraction.
- Generated descriptions can hallucinate labels, values, or relationships.
- Always compare critical claims with the original image.

## Official `markitdown-ocr` Plugin

Install it with its client library:

```bash
uv pip install \
  "markitdown" \
  "markitdown-ocr" \
  "openai"
```

Review discovery before activation:

```bash
markitdown --list-plugins
```

Configure through Python:

```python
from markitdown import MarkItDown
from openai import OpenAI

converter = MarkItDown(
    enable_plugins=True,
    llm_client=OpenAI(),
    llm_model="gpt-4o",
    llm_prompt=(
        "Extract all visible text exactly. Preserve table rows, columns, "
        "symbols, signs, decimal points, and units. Do not summarize."
    ),
)

result = converter.convert_local("scanned-paper.pdf")
print(result.markdown)
```

### Supported plugin paths

- PDF embedded images, interleaved by page position
- Full-page rendering fallback for scanned PDF pages without extractable text
- PyMuPDF rendering fallback for some malformed PDFs
- DOCX embedded images
- PPTX image shapes, placeholders, and grouped images
- XLSX worksheet images

OCR blocks are inserted using markers similar to:

```text
*[Image OCR]
<extracted text>
[End OCR]*
```

### Operational behavior

- The plugin registers enhanced converters at priority `-1.0`, ahead of built-ins.
- Every selected image/page can become a separate provider call.
- If a provider call fails, conversion can continue without that image's OCR.
- If no `llm_client` is supplied, the plugin loads but silently falls back to standard conversion.
- Large scanned documents can be expensive and slow because pages are rendered at 300 DPI.

### No CLI configuration path

The plugin README shows `--llm-client` and `--llm-model`, but MarkItDown's core CLI parser defines neither;
check `markitdown --help`. Use the Python API above rather than copying that CLI example.

## Validation for OCR Output

1. Record the package/plugin version, provider, model, endpoint region, and date.
2. Compare a sample of pages against the source.
3. Check minus signs, decimal points, Greek letters, superscripts, units, and table boundaries.
4. Flag uncertain or illegible spans instead of silently normalizing them.
5. Reconcile page counts and section headings.
6. Keep the original artifact and provider response provenance.

## Sources

- MarkItDown guide: <https://github.com/microsoft/markitdown/blob/main/README.md>
- OCR plugin: <https://github.com/microsoft/markitdown/tree/main/packages/markitdown-ocr>
- CLI parser, checked for LLM flags:
  <https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/__main__.py>
