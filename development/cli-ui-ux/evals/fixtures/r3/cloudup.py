#!/usr/bin/env python3
"""cloudup: upload build artifacts to a storage region.

Settings come from built-in defaults, the user config
($XDG_CONFIG_HOME/cloudup/config.toml), the project config (./.cloudup.toml),
CLOUDUP_* environment variables, and command-line flags.
"""

import argparse
import os
import sys
import tomllib

DEFAULTS = {"region": "eu-north-1", "endpoint": "https://storage.example.com", "retries": "3"}


def user_config_path():
    base = os.environ.get("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config")
    return os.path.join(base, "cloudup", "config.toml")


def load_toml(path):
    if not os.path.exists(path):
        return {}
    with open(path, "rb") as f:
        data = tomllib.load(f)
    return {k: str(v) for k, v in data.items() if k in DEFAULTS}


def resolve(args):
    settings = dict(DEFAULTS)
    settings.update(load_toml(".cloudup.toml"))
    settings.update(load_toml(user_config_path()))
    for key in DEFAULTS:
        value = getattr(args, key, None)
        if value is not None:
            settings[key] = str(value)
    for key in DEFAULTS:
        env = os.environ.get(f"CLOUDUP_{key.upper()}")
        if env:
            settings[key] = env
    return settings


def cmd_config(args, settings):
    for key, value in settings.items():
        print(f"{key}={value}")


def cmd_upload(args, settings):
    for path in args.files:
        if not os.path.exists(path):
            print(f"cloudup: error: cannot read '{path}': no such file", file=sys.stderr)
            sys.exit(1)
    for path in args.files:
        # Real uploads are out of scope for this build; print the plan instead.
        print(f"{settings['endpoint']}/{settings['region']}/{os.path.basename(path)}")


def main(argv=None):
    p = argparse.ArgumentParser(prog="cloudup", description="Upload build artifacts.")
    p.add_argument("--region", help="storage region")
    p.add_argument("--endpoint", help="storage endpoint URL")
    p.add_argument("--retries", type=int, help="upload retries")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("config", help="Print the resolved settings")
    s.set_defaults(func=cmd_config)
    s = sub.add_parser("upload", help="Upload files")
    s.add_argument("files", nargs="+")
    s.set_defaults(func=cmd_upload)
    args = p.parse_args(argv)
    args.func(args, resolve(args))


if __name__ == "__main__":
    main()
