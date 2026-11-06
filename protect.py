"""Command-line usage:

    python protect.py file1.pdf file2.pdf --text "For Agency X only - 2026-11-06"
"""

import argparse
from pathlib import Path

from app import DOWNLOADS, unique_path
from watermark import watermark_pdf


def main():
    p = argparse.ArgumentParser(description="Watermark PDFs locally.")
    p.add_argument("files", nargs="+", type=Path)
    p.add_argument("--text", required=True, help="Watermark text")
    p.add_argument("--opacity", type=float, default=25, help="0-100 (default 25)")
    p.add_argument("--size", type=int, default=28, help="Font size (default 28)")
    p.add_argument("--color", default="#808080", help="Hex color (default #808080)")
    p.add_argument("--password", help="Optional password for the output PDF")
    p.add_argument("--out", type=Path, default=DOWNLOADS, help="Output folder (default ~/Downloads)")
    args = p.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    for f in args.files:
        try:
            data = watermark_pdf(
                f.read_bytes(), args.text, opacity=args.opacity / 100,
                font_size=args.size, color=args.color, password=args.password,
            )
            out = unique_path(args.out, f"{f.stem}_protected")
            out.write_bytes(data)
            print(f"✓ {f.name} -> {out}")
        except Exception as exc:
            print(f"✗ {f.name}: {exc}")


if __name__ == "__main__":
    main()
