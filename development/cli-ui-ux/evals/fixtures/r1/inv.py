#!/usr/bin/env python3
"""inv: keep a small inventory of items in inventory.json."""

import argparse
import json
import os
import sys
from datetime import UTC, datetime

STORE = os.environ.get("INV_STORE", "inventory.json")


def die(msg, code=1):
    print(f"inv: error: {msg}", file=sys.stderr)
    sys.exit(code)


def load():
    if not os.path.exists(STORE):
        return []
    with open(STORE) as f:
        return json.load(f)


def save(items):
    with open(STORE, "w") as f:
        json.dump(items, f, indent=2)


def find(items, item_id):
    for item in items:
        if item["id"] == item_id:
            return item
    die(f"no item with id {item_id}")


def cmd_list(args):
    items = load()
    if args.format == "json":
        print(json.dumps(items, indent=2))
        return
    for i in items:
        print(f"{i['id']}\t{i['name']}\t{i['quantity']}\t{','.join(i['tags'])}")


def cmd_show(args):
    item = find(load(), args.id)
    if args.format == "json":
        out = {
            "id": item["id"],
            "name": item["name"],
            "quantity": item["quantity"],
            "tags": item["tags"],
            "createdAt": item["created_at"],
            "updatedAt": item["updated_at"],
        }
        print(json.dumps(out, indent=2))
        return
    for key in ("id", "name", "quantity", "tags", "created_at", "updated_at"):
        print(f"{key}: {item[key]}")


def cmd_add(args):
    items = load()
    now = datetime.now(UTC).isoformat(timespec="seconds")
    new_id = max((i["id"] for i in items), default=0) + 1
    item = {
        "id": new_id,
        "name": args.name,
        "quantity": args.quantity,
        "tags": [],
        "created_at": now,
        "updated_at": now,
    }
    items.append(item)
    save(items)
    if args.format == "json":
        print(json.dumps(item, indent=2))
    else:
        print(new_id)
        print(f"added item {new_id}", file=sys.stderr)


def cmd_remove(args):
    items = load()
    item = find(items, args.id)
    items.remove(item)
    save(items)
    if args.format == "json":
        print(json.dumps({"removed": item["id"]}))
    else:
        print(f"removed item {item['id']}", file=sys.stderr)


def cmd_tag(args):
    items = load()
    for item in items:
        if item["id"] == args.id:
            break
    else:
        print(f"Error: item {args.id} not found")
        return
    if args.tag not in item["tags"]:
        item["tags"].append(args.tag)
        item["updated_at"] = datetime.now(UTC).isoformat(timespec="seconds")
    save(items)
    if args.format == "json":
        print(json.dumps(item, indent=2))
    else:
        print(f"tagged item {item['id']} with {args.tag}", file=sys.stderr)


def cmd_stats(args):
    items = load()
    stats = {
        "item_count": len(items),
        "total_quantity": sum(i["quantity"] for i in items),
        "tag_count": len({t for i in items for t in i["tags"]}),
    }
    if args.output == "json":
        print(json.dumps(stats, indent=2))
    else:
        for k, v in stats.items():
            print(f"{k}: {v}")


def main():
    p = argparse.ArgumentParser(prog="inv", description="Keep a small inventory of items.")
    sub = p.add_subparsers(dest="cmd", required=True)

    def fmt(sp):
        sp.add_argument(
            "--format",
            choices=["text", "json"],
            default="text",
            help="output format (default: text)",
        )

    s = sub.add_parser("list", help="List all items")
    fmt(s)
    s.set_defaults(func=cmd_list)

    s = sub.add_parser("show", help="Show one item")
    s.add_argument("id", type=int)
    fmt(s)
    s.set_defaults(func=cmd_show)

    s = sub.add_parser("add", help="Add an item")
    s.add_argument("name")
    s.add_argument("--quantity", type=int, default=1, help="how many (default: 1)")
    fmt(s)
    s.set_defaults(func=cmd_add)

    s = sub.add_parser("remove", help="Remove an item")
    s.add_argument("id", type=int)
    fmt(s)
    s.set_defaults(func=cmd_remove)

    s = sub.add_parser("tag", help="Tag an item")
    s.add_argument("id", type=int)
    s.add_argument("tag")
    fmt(s)
    s.set_defaults(func=cmd_tag)

    s = sub.add_parser("stats", help="Show inventory statistics")
    s.add_argument(
        "--output", choices=["text", "json"], default="text", help="output format (default: text)"
    )
    s.set_defaults(func=cmd_stats)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
