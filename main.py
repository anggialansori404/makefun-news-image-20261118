#!/usr/bin/env python3
"""make.fun entry for news-image-20261118.

Writes the day's news image to /output/entry.png. The image itself is
entry.png beside this file (drawn by draw_image.py from the headlines
of Wednesday, 18 November 2026); this program only copies it, using
nothing but the Python standard library, so it runs in the grader's
offline sandbox and writes the same bytes on every run.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def output_dir() -> Path:
    # In the grader the writable directory is /output; locally the
    # caller points MAKEFUN_OUTPUT_DIR at a scratch folder instead.
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> None:
    if not SOURCE.is_file():
        raise SystemExit(f"entry image missing: {SOURCE}")
    target = output_dir() / "entry.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, target)
    # The gate runs this program twice and both runs must write the
    # same bytes; a plain copy of a committed file guarantees that.
    if target.stat().st_size != SOURCE.stat().st_size:
        raise SystemExit("copied image differs from the source image")


if __name__ == "__main__":
    main()
