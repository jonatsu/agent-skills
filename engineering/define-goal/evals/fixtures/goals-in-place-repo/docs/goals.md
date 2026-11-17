# Goals

## Purpose

Keep a one-way mirror of one working folder on a removable disk, so that losing the laptop loses no work.

## Success

A folder restored from the mirror matches the source by checksum, file for file.

## Scope

- In: copying new and changed files from the source to the destination; reporting what was copied.
- Out: any network transfer; two-way sync; scheduling.
- The tool never deletes or changes anything in the source folder.
- The tool deletes from the destination only when `--prune` is given.
- The owner decides any change to this file.

## Method

Python standard library only, tested with pytest through `just test`.
