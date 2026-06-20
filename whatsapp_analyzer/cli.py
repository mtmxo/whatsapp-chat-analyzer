"""Minimal CLI: parsing + export, with a few flag-driven filters."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import parse_file
from .config import ParserConfig
from .transform.anonymizer import Anonymizer
from .transform.filters import SystemMessageFilter


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wa-analyzer",
        description="Parse a WhatsApp chat and export it to JSON or CSV.",
    )
    parser.add_argument("input", help=".txt file exported from WhatsApp")
    parser.add_argument("--to", choices=["json", "csv"], default="json",
                        help="export format (default: json)")
    parser.add_argument("--out", help="output file (default: stdout)")
    parser.add_argument("--anonymize", action="store_true",
                        help="replace author names")
    parser.add_argument("--no-system", action="store_true",
                        help="drop system messages")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    # Transformer order is explicit: filter first, then anonymize.
    transformers = []
    if args.no_system:
        transformers.append(SystemMessageFilter())
    if args.anonymize:
        transformers.append(Anonymizer())

    chat = parse_file(args.input, ParserConfig(transformers=transformers))
    output = chat.to_json() if args.to == "json" else chat.to_csv()

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output + "\n")
    return 0
