# pdf-inspector

Read this reference when a PDF task needs more than ordinary anydoc conversion. It targets pdf-inspector
1.23.0. Check the installed version and its help before relying on flags after an upgrade.

## Relationship to anydoc

anydoc 0.2.4 uses pdf-inspector for PDFs. It returns complete Markdown when native extraction succeeds on every
page, and exits 3 when pages still need OCR. It hides classification details, page-level diagnostics,
coordinates, regions, layout signals, and local OCR.

Use anydoc for ordinary PDF-to-Markdown. Use pdf-inspector directly when the caller needs one of those richer
results. One PDF path is complete; running both repeats the PDF parse.

## Choose an Interface

| Need                                                               | Interface                            |
| ------------------------------------------------------------------ | ------------------------------------ |
| Shell extraction or classification with prebuilt binaries          | Node CLI, `pdf-inspector`            |
| Detailed CLI JSON, positioned items, compact output, or local OCR  | Rust CLIs, `pdf2md` and `detect-pdf` |
| Bytes, regions, coordinates, application integration, or local OCR | Python, Node, or Rust library        |
| Browser extraction without OCR                                     | WebAssembly                          |

The packages share a Rust core, but the command names and exposed options differ. Consult the selected binding's
reference for its complete API.

Prefer a pinned installation already present. These commands identify the two CLI distributions:

```bash
npx -y @firecrawl/pdf-inspector@1.23.0 --version  # Node CLI: pdf-inspector
cargo install pdf-inspector --version 1.23.0      # Rust CLIs: pdf2md and detect-pdf
```

The `npx` form downloads a native package and needs network access. The Cargo form builds from source and needs
Rust 1.88+. Python 3.8+ wheels and Node native packages cover the platforms listed in the pinned upstream docs;
other Python targets build from source.

## Command-Line Workflows

Use the Node CLI for the shortest extraction or classification path:

```bash
pdf-inspector document.pdf -o document.md
pdf-inspector document.pdf --pages 1,3,5 --json
pdf-inspector detect document.pdf --json
```

Use the Rust CLIs for detailed extraction controls:

```bash
pdf2md document.pdf --raw
pdf2md document.pdf --select-pages 1,3,5-10
pdf2md document.pdf --items-json
detect-pdf document.pdf --analyze --json
```

Node `--pages` and Rust `--select-pages` are 1-indexed. Rust `--pages` has a different job: it inserts page
markers. Write large Markdown or JSON output to a file and inspect only the required parts.

## Classification and Page Indexes

Classification distinguishes text-based, scanned, image-based, and mixed PDFs. It returns confidence and the
pages needing OCR. The fast detector samples eight pages by default; select a full scan in the Rust API when an
exact mixed-document decision matters.

Page numbering varies by API and result type:

| Result or input                                                       | Index base |
| --------------------------------------------------------------------- | ---------- |
| Python `PdfResult.pages_needing_ocr` and OCR result pages             | 1-indexed  |
| Python and Node lightweight `PdfClassification.pages_needing_ocr`     | 0-indexed  |
| Python `extract_pages_markdown(..., pages=...)` and returned page IDs | 0-indexed  |
| CLI selectors and positioned `TextItem.page`                          | 1-indexed  |
| Region APIs                                                           | 0-indexed  |

Check the source result contract before passing a page list into another API.

## Coordinates and Regions

Positioned text uses PDF points relative to the visible page box, which is `CropBox` intersected with
`MediaBox`, or `MediaBox` when that intersection is unavailable. The default sheet frame has a lower-left
origin and Y increases upward. Predominantly rotated pages may be turned so that text reads left-to-right.

Select the display frame when coordinates must match a rendered page image. Region APIs use a top-left origin
relative to the same visible page box and report `needs_ocr` for unreliable text. Persist the frame, origin,
page index base, and page rotation with every saved box.

The Python API exposes a direct positioned-text path:

```python
import pdf_inspector

items = pdf_inspector.extract_text_with_positions("document.pdf")
for item in items:
    print(item.page, item.text, item.x, item.y, item.width, item.height, item.rotation)
```

Use the binding's bytes variant when the application already owns validated bytes. Preserve encoding issues,
CMap gaps, and page-level OCR reasons alongside non-empty Markdown; each can show that extraction is incomplete.

## Selective Local OCR

Native extraction needs no OCR runtime. Selective local OCR needs compatible PDFium and ONNX Runtime shared
libraries plus the pinned PP-OCRv6 Small model set. The validated 1.23.0 runtime uses Firecrawl PDFium
`native-v7988`, ONNX Runtime 1.27.0, and model revision `oar-ocr-v0.7.0`.

Without offline mode and a populated model directory, the first routed page downloads and SHA-256-verifies
about 31 MB of model artifacts. Native extraction and local OCR keep PDF content on the machine. Missing
libraries, failed model acquisition, and OCR execution failures return errors.

```python
ocr = pdf_inspector.process_pdf_with_ocr(
    "scan.pdf",
    page_numbers=[1, 3],
    model_directory="/opt/models/pp-ocrv6-small",
    offline=True,
)
```

`pages_recommending_hosted` records low-confidence or incomplete local OCR without calling a hosted service.
Apply the main skill's external-processing rule before sending a document to one.

The full local OCR path has end-to-end upstream CI coverage on Linux x64. The macOS and Windows external-runtime
paths remain preview because they lack equivalent smoke jobs.

## Completion Criteria

A pdf-inspector run is complete when:

- the selected interface, version, options, and page index base are recorded;
- the output is checked against the source for reading order, tables, equations, rotated text, and missing pages;
- classification, OCR reasons, encoding issues, CMap gaps, and per-page OCR provenance are preserved when present;
- persisted coordinates include their frame, origin, page index base, and rotation; and
- the original PDF remains the authoritative artifact.

pdf-inspector reads PDFs. Use a PDF renderer for screenshots and another tool for editing, signing, form
filling, merging, splitting, or watermarking. Run untrusted PDFs with byte, page, time, and memory limits in an
isolated process.

## Authoritative Sources

- Release 1.23.0: <https://github.com/firecrawl/pdf-inspector/tree/v1.23.0>
- Python API: <https://github.com/firecrawl/pdf-inspector/blob/v1.23.0/docs/python.md>
- Node API: <https://github.com/firecrawl/pdf-inspector/blob/v1.23.0/napi/README.md>
- Rust API and CLIs: <https://github.com/firecrawl/pdf-inspector/blob/v1.23.0/docs/rust-api.md>
- OCR runtime: <https://github.com/firecrawl/pdf-inspector/blob/v1.23.0/docs/ocr-runtime.md>
- WebAssembly API: <https://github.com/firecrawl/pdf-inspector/blob/v1.23.0/wasm/README.md>
