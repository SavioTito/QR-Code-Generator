"""Command-line interface for the QR code generator.

Examples:
    python -m qrgen.cli "https://www.cuchd.in"
    python -m qrgen.cli "Hello World" -o hello.png -e H
    python -m qrgen.cli "https://www.cuchd.in" --logo assets/cu_logo.png -o branded.png
"""
from __future__ import annotations

import argparse
import sys
from typing import Optional, Sequence

from .core import generate_qr


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="qrgen",
        description="Generate a QR code from text or a URL.",
    )
    parser.add_argument(
        "data", nargs="?", help="Text or URL to encode. Prompted for if omitted."
    )
    parser.add_argument(
        "-o", "--output", default="qrcode.png", help="Output image file (default: qrcode.png)."
    )
    parser.add_argument(
        "-e", "--error", default="M", choices=["L", "M", "Q", "H"],
        help="Error-correction level (default: M).",
    )
    parser.add_argument("--fill", default="black", help="Foreground color (default: black).")
    parser.add_argument("--back", default="white", help="Background color (default: white).")
    parser.add_argument("--logo", help="Path to a logo image to embed in the centre.")
    parser.add_argument(
        "--box-size", type=int, default=10, help="Pixels per QR module (default: 10)."
    )
    parser.add_argument(
        "--border", type=int, default=4, help="Quiet-zone width in modules (default: 4)."
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    data = args.data
    if not data:
        try:
            data = input("Enter the text or URL to encode: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 1

    try:
        path = generate_qr(
            data,
            args.output,
            error=args.error,
            fill=args.fill,
            back=args.back,
            logo=args.logo,
            box_size=args.box_size,
            border=args.border,
        )
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except FileNotFoundError as exc:
        print(f"Error: logo file not found: {exc}", file=sys.stderr)
        return 1

    print(f"QR code saved as {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
