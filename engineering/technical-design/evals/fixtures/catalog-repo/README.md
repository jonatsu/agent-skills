# catalogcheck

A command-line tool for checking product catalog files before they are published.

## Installation

Install it into a virtual environment with Python 3.12 or later:

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
```

## Usage

Pass the path of a catalog file:

```bash
.venv/bin/catalogcheck catalog.json
```

See [the API reference](docs/api.md) for the command and the Python entry point.
