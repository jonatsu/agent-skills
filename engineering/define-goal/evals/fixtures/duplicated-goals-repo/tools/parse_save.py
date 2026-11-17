"""Print the header of a Starfall Tactics save file."""

import struct
import sys
from pathlib import Path


def main() -> None:
    data = Path(sys.argv[1]).read_bytes()
    magic, version, turn = struct.unpack_from("<4sHH", data, 0)
    print(f"magic={magic!r} version={version} turn={turn}")


if __name__ == "__main__":
    main()
