# draw.io XML Format

The structure a `.drawio` file must have, and the rules that decide whether it opens and renders. The official
references are the source of truth when this file is silent: jgraph's
[XML reference](https://github.com/jgraph/drawio-mcp/blob/8c19abbdc3b214d6141989e5a2905defa7529902/shared/xml-reference.md),
[style reference](https://github.com/jgraph/drawio-mcp/blob/8c19abbdc3b214d6141989e5a2905defa7529902/shared/style-reference.md),
and [schema](https://github.com/jgraph/drawio-mcp/blob/8c19abbdc3b214d6141989e5a2905defa7529902/shared/mxfile.xsd).

## Contents

- Skeleton
- Vertices
- Edges
- Containers and layers
- Pages
- Styles
- Labels and escaping
- Compressed pages

## Skeleton

```xml
<mxfile>
  <diagram id="page-1" name="Overview">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="api" value="API" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="120" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="db" value="Orders DB" style="shape=cylinder3;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="240" y="30" width="80" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="api-db" value="SQL" style="edgeStyle=orthogonalEdgeStyle;html=1;" edge="1" parent="1"
                source="api" target="db">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

Cell `0` is the root and cell `1`, with `parent="0"`, is the default layer. Both are required, and every other cell
descends from `1`. Ids are strings and must be unique within a page; descriptive ids such as `api-db` make edits and
reviews easier than numbers. Coordinates are pixels from the top-left corner.

## Vertices

A shape is a cell with `vertex="1"` and a child `<mxGeometry x y width height as="geometry"/>`. Without the geometry
it has no position or size. A cell is a vertex or an edge, never both.

To attach custom properties, wrap the cell: `<object id="api" label="API" owner="team-a">` holds the `<mxCell>` with
its style, `vertex`, and `parent`. The id and label move to the wrapper.

## Edges

An edge is a cell with `edge="1"`, a `source` and a `target` naming existing cells, and a child
`<mxGeometry relative="1" as="geometry"/>`. An edge written as a self-closing `<mxCell .../>` does not render.

- **Waypoints** go inside the geometry: `<Array as="points"><mxPoint x="200" y="120"/></Array>`.
- **An edge without a source or target** uses `<mxPoint x=".." y=".." as="sourcePoint"/>` and `as="targetPoint"`
  inside the geometry instead, as a sequence-diagram lifeline does.
- **Routing:** `edgeStyle=orthogonalEdgeStyle` draws right-angled connectors; `edgeStyle=entityRelationEdgeStyle`
  suits entity-relationship lines. `exitX`/`exitY` and `entryX`/`entryY`, from 0 to 1, pin where the edge leaves
  and enters a shape.
- **The label** is the edge's `value`.

## Containers and Layers

A child cell sets `parent` to its container's id, and its coordinates become relative to that container's top-left
corner. Make a container with `swimlane;startSize=30;` for a titled box, `group;` for an invisible group, or add
`container=1;pointerEvents=0;` to any shape.

Place each edge under the innermost container that holds both of its ends; when an end lies outside every
container, the edge's parent is `1`. An edge filed further out than its ends is laid out in the wrong place by
`--layout`, and `--normalize` moves it back.

A further layer is another cell with `parent="0"`; cells on that layer use its id as their parent.

## Pages

Each page is a `<diagram>` with its own `name` and its own `mxGraphModel`. Ids only need to be unique within their
page. The CLI exports one page per image, chosen with `-p`, which counts from 1.

## Styles

A style is a string of `key=value;` pairs, and a bare word without `=` names a shape or base style:
`ellipse;whiteSpace=wrap;html=1;`. The keys used most:

| Purpose   | Keys                                                                                         |
| --------- | -------------------------------------------------------------------------------------------- |
| Shape     | `rounded=1`, `ellipse`, `rhombus`, `shape=cylinder3`, `shape=document`, `shape=note`, `text` |
| Color     | `fillColor=#dae8fc`, `strokeColor=#6c8ebf`, `fontColor=#333333`                              |
| Text      | `whiteSpace=wrap`, `html=1`, `fontSize=14`, `fontStyle=1` (bold), `align`, `verticalAlign`   |
| Edge      | `edgeStyle=orthogonalEdgeStyle`, `endArrow=block`, `dashed=1`, `curved=1`                    |
| Container | `swimlane`, `startSize=30`, `group`, `container=1`, `collapsible=0`                          |

Look up anything else in the style reference linked at the top, rather than guessing a key: draw.io ignores an
unknown key without complaint, so a guessed key simply does nothing.

## Labels and Escaping

A label is the cell's `value` attribute, so XML attribute escaping applies: `&amp;`, `&lt;`, `&gt;`, and `&quot;`.
With `html=1` the label is HTML, escaped once more inside the attribute: a line break is `&lt;br&gt;`. Without
`html=1`, a line break is `&#xa;`. Leave XML comments out of generated files; a `--` inside a comment makes the
whole file invalid.

## Compressed Pages

A page whose `<diagram>` holds Base64 text instead of an `<mxGraphModel>` is compressed: the model XML was
URL-encoded, deflated without a zlib header, and Base64-encoded. `scripts/drawio_check.py extract` reverses it. New
files from the draw.io desktop app and the CLI's `-f xml` export are plain, so compression usually appears in older
files or ones saved with File > Properties > Compressed turned on.
