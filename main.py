"""Entry point: copy the pre-rendered front page to the output directory.

The image (entry.png, 1024x1024) is drawn by build.py + draw.py in this
repository; this program only places it at /output/entry.png, using the
standard library alone so it runs in the grader sandbox with no installs.
"""
import os
import shutil
import struct
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    dst = os.path.join(outdir, "entry.png")
    with open(src, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
    width, height = struct.unpack(">II", head[16:24])
    if (width, height) != (1024, 1024):
        raise SystemExit("entry.png must be 1024x1024, got %dx%d" % (width, height))
    if os.path.getsize(src) > 1048576:
        raise SystemExit("entry.png exceeds 1 MiB")
    shutil.copyfile(src, dst)
    print("wrote %s (%d bytes, %dx%d)" % (dst, os.path.getsize(dst), width, height))
    return 0


if __name__ == "__main__":
    sys.exit(main())
