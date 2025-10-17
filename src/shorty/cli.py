"""Command line interface for the ``shorty`` code shortening tool."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .shortener import shorten_code


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Shorten source code by stripping comments and blank lines.")
    parser.add_argument("source", nargs="?", type=Path, help="Path to the source file. Reads stdin when omitted.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Optional path to write the shortened code. Defaults to stdout.",
    )
    parser.add_argument(
        "-l",
        "--language",
        help="Language of the input file. Affects which comment styles are removed.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.source is None:
        text = sys.stdin.read()
    else:
        try:
            text = args.source.read_text(encoding="utf-8")
        except FileNotFoundError:
            parser.error(f"File not found: {args.source}")
            return 2

    shortened = shorten_code(text, language=args.language)

    if args.output:
        args.output.write_text(shortened, encoding="utf-8")
    else:
        sys.stdout.write(shortened)

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
