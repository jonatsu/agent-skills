#!/bin/sh
# Write the bookmark names, one per line, for the docs site's link index.
set -eu
cd "$(dirname "$0")/.."
./bm list --json | jq -r '.[].name' > link-index.txt
