#!/usr/bin/env python3
"""Entry program for news-image-20261126.

Copies entry/entry.png to MAKEFUN_OUTPUT_DIR (default /output),
verifying the PNG after the copy. Standard library only, no network.
"""
import hashlib
import os
import shutil
import struct
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "entry", "entry.png")
MAX_BYTES = 1048576


def read_png_header(path):
    """Return (width, height) from a PNG's IHDR chunk."""
    with open(path, "rb") as fh:
        magic = fh.read(8)
        if magic != b"\x89PNG\r\n\x1a\n":
            raise ValueError("not a PNG file")
        length = struct.unpack(">I", fh.read(4))[0]
        ctype = fh.read(4)
        if ctype != b"IHDR" or length != 13:
            raise ValueError("missing or malformed IHDR chunk")
        width, height = struct.unpack(">II", fh.read(8))
    return width, height


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dest)
    size = os.path.getsize(dest)
    if size > MAX_BYTES:
        raise ValueError(f"entry.png is {size} bytes, over the 1 MiB limit")
    width, height = read_png_header(dest)
    if (width, height) != (1024, 1024):
        raise ValueError(f"entry.png is {width}x{height}, expected 1024x1024")
    digest = hashlib.sha256(open(dest, "rb").read()).hexdigest()
    source_digest = hashlib.sha256(open(SRC, "rb").read()).hexdigest()
    if digest != source_digest:
        raise ValueError("copied entry.png does not match the source file")
    os.chmod(dest, 0o644)
    print(f"wrote {dest}: {size} bytes, {width}x{height}, sha256={digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
