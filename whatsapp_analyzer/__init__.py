"""Parser e analisi per chat WhatsApp esportate in formato .txt."""

from __future__ import annotations

from pathlib import Path

from .config import ParserConfig
from .models import Chat, MediaKind, Message, MessageType
from .parsing.parser import WhatsAppParser

__version__ = "0.1.0"

__all__ = [
    "parse_file",
    "parse_string",
    "Chat",
    "Message",
    "MessageType",
    "MediaKind",
    "ParserConfig",
]


def parse_string(content: str, config: ParserConfig | None = None) -> Chat:
    """Parsa una chat già caricata in memoria."""
    return WhatsAppParser(config).parse(content)


def parse_file(path: str | Path, config: ParserConfig | None = None) -> Chat:
    """Parsa una chat da file. Gestisce l'encoding utf-8 con eventuale BOM."""
    # utf-8-sig rimuove il BOM che WhatsApp antepone su alcuni export.
    content = Path(path).read_text(encoding="utf-8-sig")
    return parse_string(content, config)
