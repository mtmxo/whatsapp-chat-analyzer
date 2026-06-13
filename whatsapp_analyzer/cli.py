"""CLI minima: parsing + export, con qualche filtro da flag."""

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
        description="Parsa una chat WhatsApp ed esportala in JSON o CSV.",
    )
    parser.add_argument("input", help="file .txt esportato da WhatsApp")
    parser.add_argument("--to", choices=["json", "csv"], default="json",
                        help="formato di export (default: json)")
    parser.add_argument("--out", help="file di output (default: stdout)")
    parser.add_argument("--anonymize", action="store_true",
                        help="sostituisce i nomi degli autori")
    parser.add_argument("--no-system", action="store_true",
                        help="esclude i messaggi di sistema")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    # L'ordine dei transformer è esplicito: prima si filtra, poi si anonimizza.
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
