"""Parser and analysis for WhatsApp chats exported as .txt files."""

from __future__ import annotations

from pathlib import Path

from .analysis.activity import ActivityAnalyzer, ActivityReport
from .analysis.content import ContentAnalyzer, ContentReport
from .analysis.statistics import ChatStatistics, StatisticsAnalyzer, UserStats
from .config import ParserConfig
from .models import Chat, MediaKind, Message, MessageType
from .parsing.parser import WhatsAppParser

__version__ = "0.2.0"

__all__ = [
    "parse_file",
    "parse_string",
    "Chat",
    "Message",
    "MessageType",
    "MediaKind",
    "ParserConfig",
    "StatisticsAnalyzer",
    "ChatStatistics",
    "UserStats",
    "ActivityAnalyzer",
    "ActivityReport",
    "ContentAnalyzer",
    "ContentReport",
]


def parse_string(content: str, config: ParserConfig | None = None) -> Chat:
    """Parse a chat already loaded in memory."""
    return WhatsAppParser(config).parse(content)


def parse_file(path: str | Path, config: ParserConfig | None = None) -> Chat:
    """Parse a chat from a file. Handles utf-8 encoding with an optional BOM."""
    # utf-8-sig strips the BOM that WhatsApp prepends to some exports.
    content = Path(path).read_text(encoding="utf-8-sig")
    return parse_string(content, config)
