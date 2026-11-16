#!/usr/bin/env python3
"""slowconv: convert a CSV file to JSON, one record at a time.

Each record is enriched by a slow lookup, so large files take a while.
"""

import argparse
import csv
import json
import time


def enrich(row):
    time.sleep(0.2)  # stands in for a slow network lookup
    row["checked"] = True
    return row


def main():
    p = argparse.ArgumentParser(prog="slowconv", description="Convert CSV to JSON.")
    p.add_argument("input", help="CSV file to read")
    p.add_argument("-o", "--output", required=True, help="JSON file to write")
    args = p.parse_args()

    with open(args.input, newline="") as src, open(args.output, "w") as out:
        out.write("[\n")
        first = True
        for row in csv.DictReader(src):
            if not first:
                out.write(",\n")
            out.write("  " + json.dumps(enrich(row)))
            out.flush()
            first = False
        out.write("\n]\n")


if __name__ == "__main__":
    main()
