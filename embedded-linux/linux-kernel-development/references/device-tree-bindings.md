# Device-Tree Bindings

Writing a binding schema, validating it, validating device-tree sources against it, and ordering the patches. The
schema format and the tool minimums change between releases. Read the target tree's
`Documentation/devicetree/bindings/writing-schema.rst` and `submitting-patches.rst` before you write.

## Contents

- Binding Rules
- Install the Tools
- Write the Schema
- Validate
- Device-Tree Sources
- Order the Series

## Binding Rules

The tree's binding document goes further than the driver rule in the skill body. Every compatible string in a chip or
board `.dts` file needs a binding, even when no driver matches it yet. Put it in `Documentation/devicetree/bindings/`.
checkpatch warns when one is missing. When the driver does not yet match a documented compatible string, the binding
also lists one that it matches.

- Write the binding in DT schema format, which is json-schema vocabulary in YAML. It must pass
  `make dt_binding_check`.
- Describe the hardware, not the driver. `writing-bindings.rst` in the same directory holds the design rules for
  properties and compatible strings.
- License the binding file `(GPL-2.0-only OR BSD-2-Clause)`, the dual license the tree prefers.
- Treat an existing binding as a shared interface, because projects other than Linux use bindings. Read
  `Documentation/devicetree/bindings/ABI.rst` before you change one.
- When the devicetree maintainers disagree with the tree's document, follow the maintainers.

## Install the Tools

The dtschema project provides the validators. The tree's document installs it with `pip3 install dtschema`. That
needs `swig` and the Python development files first (`apt install swig python3-dev` on Debian and Ubuntu).

- Put the installed `dt-doc-validate`, `dt-mk-schema`, and `dt-validate` on `PATH`. Pip uses `~/.local/bin` by
  default.
- Install `yamllint` as well. dtschema uses it when present, and the binding build warns when it is missing.
- The build rejects an older dtschema. `DT_SCHEMA_MIN_VERSION` in `Documentation/devicetree/bindings/Makefile`
  names the minimum; read it from the tree in hand.
- Installing reaches the package index, so ask the user first when the machine or its Python is managed.
- Inference: prefer a virtual environment to the system Python.

## Write the Schema

Start from `Documentation/devicetree/bindings/example-schema.yaml` in the tree. Name the file after the first
compatible string. Inference: place it in the directory of the device class, as the tree's `adi,ad7476` example
suggests. Indent YAML with two spaces. This skeleton shows the required top-level keys:

```yaml
# SPDX-License-Identifier: (GPL-2.0-only OR BSD-2-Clause)
%YAML 1.2
---
$id: http://devicetree.org/schemas/iio/adc/vendor,example-adc.yaml#
$schema: http://devicetree.org/meta-schemas/core.yaml#

title: Example ADC from a vendor

maintainers:
  - Jane Doe <jane@example.com>

properties:
  compatible:
    const: vendor,example-adc

  reg:
    maxItems: 1

required:
  - compatible
  - reg

additionalProperties: false

examples:
  - |
    i2c {
        #address-cells = <1>;
        #size-cells = <0>;

        adc@48 {
            compatible = "vendor,example-adc";
            reg = <0x48>;
        };
    };
```

Each top-level key follows the tree's document:

- `$id` is a unique URI that starts with `http://devicetree.org/schemas/` and contains the file's path and name. No
  file needs to exist at that address. A relative `$ref` resolves against it.
- `$schema` names the meta-schema, and `title` is a one-line description of the hardware.
- `maintainers` lists the binding maintainers' email addresses. An optional `description` explains what the device
  does and links its datasheets.
- `select`, `allOf`, and `patternProperties` are optional. Most bindings need no `select`.
- Use `allOf` to include a schema for a device class, such as an I2C or SPI controller. Use `patternProperties` for
  names matched by regex.
- Keep `properties` and `required` in the same order, following `dts-coding-style.rst`.
- Give the top level, and every nested node, exactly one of `additionalProperties` or `unevaluatedProperties`.
- Use `additionalProperties: false` when the binding references no other schema.
- Use `unevaluatedProperties: false` when the binding references a schema whose properties are all allowed.
- `examples` is a list of DTS hunks that implement this binding alone. Show most of the properties. Use the named
  defines for interrupt and GPIO flags. Leave out `status`, unrelated nodes, and consumers.
- Indent example DTS with four spaces. YAML forbids tabs.

Property rules:

- For a common property such as `interrupts`, add only the constraints the common schema lacks. Examples are the
  count and the allowed values.
- Give a vendor-specific property a `description` and a `$ref` to a type in `schemas/types.yaml`. Boolean
  properties need no type.
- Leave out `minItems` and `maxItems` for a fixed list. The tools derive them from the number of `items` entries.
- When one binding covers several similar devices, define each property once at the top level with the broadest
  constraints. Narrow them in `if:then:` blocks, and never define a property inside `if:then:`.

## Validate

Validate the schema and its examples:

```sh
make dt_binding_check DT_SCHEMA_FILES=<class>/vendor,example-adc.yaml
```

- `dt_binding_check` checks each schema against the meta-schema. It also compiles and validates every `examples`
  entry.
- `DT_SCHEMA_FILES` takes one or more schema files or fixed-string patterns separated by `:`. Examples are
  `trivial-devices.yaml:rtc.yaml` and `/gpio/`.
- The tree's document says a new binding's example should pass `scripts/dtc/dt-check-style` in strict mode without
  warnings.
- Inference: run the check without `DT_SCHEMA_FILES` before you send, when other bindings reference your schema.

The check is done when the command exits without an error or a warning from your files. Fix a `yamllint` warning
too, because the binding build runs `yamllint` when it is installed.

## Device-Tree Sources

Validate `.dts` files against the schemas with `CHECK_DTBS=y` on the board's `.dtb` target:

```sh
make CHECK_DTBS=y vendor/board.dtb
```

- `make dtbs_check` validates every `.dtb`. `DT_SCHEMA_FILES` narrows either command to the schemas you changed.
- `dtbs_check` skips any schema file that has errors. Run `dt_binding_check` first, because only it reports every
  schema error.
- Inference: run with the same `ARCH` and output directory as the product build. Otherwise the target may name a
  different `.dtb`.
- Inference: an existing tree may report old warnings. Run the command on the base commit too, and fix only the
  reports your change adds.

Follow `Documentation/devicetree/bindings/dts-coding-style.rst` for the source itself:

- Node and property names use only lowercase letters, digits, and dashes. Labels use lowercase letters, digits, and
  underscores.
- Unit addresses use lowercase hexadecimal without leading zeros. Nodes with a unit address are sorted by it,
  ascending.
- Nodes without a unit address are sorted alphanumerically by name.
- An architecture may add stricter rules, so check its existing files.

## Order the Series

A binding patch carries only the `Documentation/` and `include/dt-bindings/` files. The code that uses the binding
follows in later patches.

- Title the binding patch `dt-bindings: <binding dir>: <summary>`. A few subsystems reverse it to
  `<binding dir>: dt-bindings: <summary>`: ASoC, media, regulators, SCSI, SPI, and UFS.
- Leave "Documentation", "doc", and "YAML" out of the subject, because all bindings are documentation in YAML.
- Place the binding before the driver that implements it in the series.
- Post `.dts` patches separately, or put them at the end of the series. The DTS does not depend on the driver.
- Expect the platform SoC tree to apply `.dts` files, never a driver subsystem tree.
- When a driver maintainer applies the whole series, split the `.dts` patches into their own series. Reference the
  binding submission in its cover letter.
- Send the series to the devicetree mailing list that the binding `submitting-patches.rst` names. Copy the
  devicetree maintainers that `scripts/get_maintainer.pl` lists.
