#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261125 (b17, variant HEROALT).

Copies the pre-rendered front page (entry.png, built at build time by
gen.py) into the grader's output directory. Standard library only:
the grader runs with no third-party packages installed, so this file
imports nothing beyond os, sys, shutil, hashlib and struct. In
particular it must never import PIL or numpy: on the grading image
those imports raise ModuleNotFoundError and the run fails outright.

Layout of the image itself (see gen.py for the renderer):
  * header with the DATE CHECK: Wednesday 25 November 2026
  * Shenzhou-24 hero scene (first foreign astronaut on Tiangong)
  * two hero cards: Trump tariffs on 14 partners, AI chip selloff
  * 47-story grid across 10 regions, every card labelled with its
    region and a certainty letter (C confirmed, R reported, CL claim)

Usage (grader): python3 main.py
  reads  entry.png next to this file
  writes $MAKEFUN_OUTPUT_DIR/entry.png (default: ./out/entry.png)
  exits 0 only if the copied file is byte-identical to the source
"""
import hashlib
import os
import shutil
import struct
import sys

MAX_BYTES = 1048576          # RULES: at most 1 MiB
MAX_SIDE = 1024              # RULES: at most 1024 x 1024 px
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    """Print an error to stderr and exit non-zero (grader: run fails)."""
    print("main.py: error: " + message, file=sys.stderr)
    return 1


def sha256_of(path):
    """Hex digest of a file, streamed so large files stay cheap."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path):
    """Return (width, height) parsed from the PNG IHDR chunk.

    Pure struct parsing: no image library is needed (or allowed) here.
    Raises ValueError on anything that is not a well-formed PNG header.
    """
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[:8] != PNG_MAGIC:
        raise ValueError("not a PNG file (bad magic bytes)")
    if header[12:16] != b"IHDR":
        raise ValueError("not a PNG file (first chunk is not IHDR)")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def validate_source(path):
    """Check the source image against the competition's hard limits.

    Returns (width, height, size_bytes, sha256) on success, else None
    after printing the reason. Every failure here is a hard failure:
    an invalid image must never be silently copied as if it were fine.
    """
    if not os.path.isfile(path):
        print("main.py: error: source image missing: " + path, file=sys.stderr)
        return None
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        print("main.py: error: entry.png is %d bytes, over the 1 MiB limit"
              % size, file=sys.stderr)
        return None
    try:
        width, height = png_dimensions(path)
    except ValueError as exc:
        print("main.py: error: " + str(exc), file=sys.stderr)
        return None
    if width > MAX_SIDE or height > MAX_SIDE:
        print("main.py: error: image is %dx%d, over the 1024x1024 limit"
              % (width, height), file=sys.stderr)
        return None
    return width, height, size, sha256_of(path)


def main(argv):
    """Copy entry.png to the output dir and verify the copy byte-wise."""
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    checked = validate_source(source)
    if checked is None:
        return 1
    width, height, size, digest = checked
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not os.path.isabs(out_dir):
        out_dir = os.path.join(os.getcwd(), out_dir)
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    tmp = dest + ".tmp"
    shutil.copyfile(source, tmp)
    os.replace(tmp, dest)
    if sha256_of(dest) != digest:
        try:
            os.unlink(dest)
        except OSError:
            pass
        return fail("copied file differs from source (sha256 mismatch)")
    print("main.py: wrote %s (%dx%d, %d bytes, sha256 %s)"
          % (dest, width, height, size, digest))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
