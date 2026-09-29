#!/usr/bin/env python3
"""Check a draw.io diagram's structure, or extract it as plain uncompressed XML.

Reads `.drawio` and `.xml` files, and editable `.drawio.svg` and `.drawio.png` images, whether their pages are
stored plain or compressed. Uses only the Python standard library.

    drawio_check.py check FILE...           report structural defects; exit 1 when any is found
    drawio_check.py extract FILE -o OUT     write the diagram as an uncompressed .drawio file

Exit status: 0 when clean, 1 when `check` finds a defect, 2 when a file cannot be read or decoded.
"""

from __future__ import annotations

import argparse
import base64
import sys
import urllib.parse
import xml.etree.ElementTree as ET
import zlib
from dataclasses import dataclass
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
# The web editor embeds `mxfile` in a tEXt chunk; the desktop CLI embeds `mxGraphModel` in a zTXt chunk.
PNG_DIAGRAM_KEYS = (b"mxfile", b"mxGraphModel")
ROOT_LAYER_ID = "0"
DEFAULT_LAYER_ID = "1"


class DiagramReadError(Exception):
    """The file holds no diagram this tool can decode."""


@dataclass(frozen=True)
class Page:
    """One diagram page: its name and its decoded mxGraphModel element."""

    name: str
    model: ET.Element


def decompress_page(text: str) -> str:
    """Decode a compressed page: Base64, then raw DEFLATE, then URL decoding."""
    try:
        inflated = zlib.decompress(base64.b64decode(text), -zlib.MAX_WBITS)
    except (ValueError, zlib.error) as error:
        raise DiagramReadError(f"compressed page does not decode: {error}") from error
    # unquote, not unquote_plus: draw.io encodes with encodeURIComponent, where "+" is literal.
    return urllib.parse.unquote(inflated.decode("utf-8"))


def read_png_diagram(data: bytes) -> str:
    """Return the diagram text embedded in a PNG's tEXt or zTXt chunk."""
    if not data.startswith(PNG_SIGNATURE):
        raise DiagramReadError("not a PNG file")
    offset = len(PNG_SIGNATURE)
    while offset + 8 <= len(data):
        length = int.from_bytes(data[offset : offset + 4], "big")
        kind = data[offset + 4 : offset + 8]
        body = data[offset + 8 : offset + 8 + length]
        offset += 12 + length
        if kind not in (b"tEXt", b"zTXt"):
            continue
        key, _, value = body.partition(b"\x00")
        if key not in PNG_DIAGRAM_KEYS:
            continue
        if kind == b"zTXt":
            # A zTXt value starts with one compression-method byte; 0 is zlib.
            value = zlib.decompress(value[1:])
        text = value.decode("latin-1" if kind == b"tEXt" else "utf-8")
        return urllib.parse.unquote(text) if not text.lstrip().startswith("<") else text
    raise DiagramReadError("PNG carries no embedded diagram; export it again with -e")


def read_diagram_text(path: Path) -> str:
    """Return the mxfile or mxGraphModel XML a file holds, from any supported container."""
    data = path.read_bytes()
    if data.startswith(PNG_SIGNATURE):
        return read_png_diagram(data)
    text = data.decode("utf-8")
    root = ET.fromstring(text)
    if root.tag.endswith("svg"):
        content = root.get("content")
        if not content:
            raise DiagramReadError("SVG carries no embedded diagram; export it again with -e")
        return content
    return text


def read_pages(path: Path) -> list[Page]:
    """Parse a file into its pages, decompressing any compressed page."""
    try:
        root = ET.fromstring(read_diagram_text(path))
    except (OSError, UnicodeDecodeError, ET.ParseError) as error:
        raise DiagramReadError(str(error)) from error
    if root.tag == "mxGraphModel":
        return [Page("(bare model)", root)]
    if root.tag != "mxfile":
        raise DiagramReadError(f"root element is <{root.tag}>, expected <mxfile> or <mxGraphModel>")
    pages: list[Page] = []
    for index, diagram in enumerate(root.findall("diagram"), start=1):
        name = diagram.get("name") or f"page {index}"
        model = diagram.find("mxGraphModel")
        if model is None:
            encoded = (diagram.text or "").strip()
            if not encoded:
                raise DiagramReadError(f"{name}: page is empty")
            try:
                model = ET.fromstring(decompress_page(encoded))
            except ET.ParseError as error:
                raise DiagramReadError(f"{name}: decompressed page is not XML: {error}") from error
        pages.append(Page(name, model))
    if not pages:
        raise DiagramReadError("<mxfile> holds no <diagram> page")
    return pages


def page_defects(page: Page) -> list[str]:
    """Return the structural defects that stop a page from opening or rendering correctly."""
    defects: list[str] = []
    root = page.model.find("root")
    if root is None:
        return ["mxGraphModel has no <root>"]
    cells = [cell for cell in root if cell.tag in ("mxCell", "UserObject", "object")]
    ids: dict[str, ET.Element] = {}
    for cell in cells:
        cell_id = cell.get("id")
        if not cell_id:
            defects.append(f"a <{cell.tag}> has no id")
        elif cell_id in ids:
            defects.append(f"id {cell_id!r} is used twice")
        else:
            ids[cell_id] = cell
    if ROOT_LAYER_ID not in ids:
        defects.append('root cell id="0" is missing')
    default_layer = ids.get(DEFAULT_LAYER_ID)
    if default_layer is None:
        defects.append('default layer id="1" is missing')
    elif _mx_cell(default_layer).get("parent") != ROOT_LAYER_ID:
        defects.append('cell id="1" must have parent="0"')
    for cell_id, cell in ids.items():
        defects.extend(_cell_defects(cell_id, _mx_cell(cell), ids))
    return defects


def _mx_cell(cell: ET.Element) -> ET.Element:
    # A cell with custom properties is an <object> or <UserObject> wrapping its <mxCell>.
    inner = cell.find("mxCell")
    return inner if cell.tag != "mxCell" and inner is not None else cell


def _cell_defects(cell_id: str, cell: ET.Element, ids: dict[str, ET.Element]) -> list[str]:
    if cell_id == ROOT_LAYER_ID:
        return []
    defects: list[str] = []
    parent = cell.get("parent")
    if parent is None:
        defects.append(f"cell {cell_id!r} has no parent")
    elif parent not in ids:
        defects.append(f"cell {cell_id!r} names missing parent {parent!r}")
    is_vertex, is_edge = cell.get("vertex") == "1", cell.get("edge") == "1"
    geometry = cell.find("mxGeometry")
    if is_vertex and is_edge:
        defects.append(f"cell {cell_id!r} is marked both vertex and edge")
    if is_vertex and geometry is None:
        defects.append(f"vertex {cell_id!r} has no <mxGeometry>, so it has no position or size")
    if is_edge:
        if geometry is None:
            defects.append(
                f'edge {cell_id!r} has no <mxGeometry relative="1" as="geometry"/>; it will not render'
            )
        for end in ("source", "target"):
            terminal = cell.get(end)
            if terminal is not None and terminal not in ids:
                defects.append(f"edge {cell_id!r} {end} names missing cell {terminal!r}")
    return defects


def serialize(pages: list[Page]) -> str:
    """Build an uncompressed mxfile document from decoded pages."""
    mxfile = ET.Element("mxfile")
    for page in pages:
        diagram = ET.SubElement(mxfile, "diagram", name=page.name)
        diagram.append(page.model)
    ET.indent(mxfile)
    return ET.tostring(mxfile, encoding="unicode") + "\n"


def run_check(paths: list[Path]) -> int:
    status = 0
    for path in paths:
        try:
            pages = read_pages(path)
        except DiagramReadError as error:
            print(f"{path}: cannot read: {error}", file=sys.stderr)
            status = 2
            continue
        for page in pages:
            for defect in page_defects(page):
                print(f"{path}: {page.name}: {defect}")
                status = max(status, 1)
    return status


def run_extract(path: Path, output: Path) -> int:
    try:
        pages = read_pages(path)
    except DiagramReadError as error:
        print(f"{path}: cannot read: {error}", file=sys.stderr)
        return 2
    _ = output.write_text(serialize(pages), encoding="utf-8")
    print(f"{path} -> {output} ({len(pages)} page(s))")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("check", help="report structural defects")
    check.add_argument("files", nargs="+", type=Path)
    extract = commands.add_parser(
        "extract", help="write the diagram as an uncompressed .drawio file"
    )
    extract.add_argument("file", type=Path)
    extract.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.command == "check":
        return run_check(args.files)
    return run_extract(args.file, args.output)


if __name__ == "__main__":
    sys.exit(main())
