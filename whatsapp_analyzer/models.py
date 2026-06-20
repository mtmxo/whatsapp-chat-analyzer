"""Parser data models: plain data, no parsing logic."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Callable, Iterator


class MessageType(Enum):
    TEXT = "text"
    MEDIA = "media"
    SYSTEM = "system"      # join/leave, group changes, encryption notices, ...
    DELETED = "deleted"


class MediaKind(Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    STICKER = "sticker"
    GIF = "gif"


@dataclass(frozen=True)
class Message:
    timestamp: datetime
    sender: str | None        # None for system messages (no author)
    text: str
    type: MessageType
    media_kind: MediaKind | None = None   # set only when type == MEDIA


class Chat:
    """A container of messages that behaves like a sequence."""

    def __init__(self, messages: list[Message]):
        self.messages = messages

    def __iter__(self) -> Iterator[Message]:
        return iter(self.messages)

    def __len__(self) -> int:
        return len(self.messages)

    def __getitem__(self, index):
        return self.messages[index]

    @property
    def participants(self) -> set[str]:
        return {m.sender for m in self.messages if m.sender is not None}

    def filter(self, predicate: Callable[[Message], bool]) -> "Chat":
        return Chat([m for m in self.messages if predicate(m)])

    def to_json(self) -> str:
        from .export.json_exporter import JsonExporter
        return JsonExporter().export(self)

    @classmethod
    def from_json(cls, data: str) -> "Chat":
        from .export.json_exporter import JsonExporter
        return JsonExporter().load(data)

    def to_csv(self) -> str:
        from .export.csv_exporter import CsvExporter
        return CsvExporter().export(self)

    def to_dataframe(self):
        from .export.dataframe_exporter import DataFrameExporter
        return DataFrameExporter().export(self)

    def statistics(self):
        from .analysis.statistics import StatisticsAnalyzer
        return StatisticsAnalyzer().analyze(self)

    def activity(self):
        from .analysis.activity import ActivityAnalyzer
        return ActivityAnalyzer().analyze(self)

    def content(self, stopwords: set[str] | None = None):
        from .analysis.content import ContentAnalyzer
        return ContentAnalyzer(stopwords=stopwords).analyze(self)
