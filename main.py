"""Python 3.13 sandbox entry: publish exactly one frozen original image.

Drawing happens in render_news.py during authoring. Judging needs only Python's
standard library, no Pillow installation, fonts, internet or writable source.
"""
import os
from pathlib import Path


def main():
    source = Path(__file__).resolve().parent / "news.png"
    output = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output.mkdir(parents=True, exist_ok=True)
    target = output / "entry.png"
    target.write_bytes(source.read_bytes())
    target.chmod(0o644)


if __name__ == "__main__":
    main()
