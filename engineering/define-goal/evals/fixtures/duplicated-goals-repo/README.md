# starfall-saves

Notes and tools for the save files of *Starfall Tactics* (1998), a turn-based strategy game whose publisher no
longer exists.

## Goals

1. Write a complete, readable description of the save file format, so anyone can build tools for it.
2. Build a small save editor on top of that description.

The format description comes first; the editor is a way to check that the description is right.

## Layout

- `docs/format-notes.md` holds what is known about the format so far.
- `tools/parse_save.py` reads a save file and prints its header.
