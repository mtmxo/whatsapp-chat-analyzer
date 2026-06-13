"""Filtri applicabili durante il parsing."""

from __future__ import annotations

from datetime import datetime

from ..models import Message, MessageType
from .base import MessageTransformer


class DateRangeFilter(MessageTransformer):
    def __init__(self, start: datetime | None = None, end: datetime | None = None):
        self.start = start
        self.end = end

    def apply(self, msg: Message) -> Message | None:
        if self.start is not None and msg.timestamp < self.start:
            return None
        if self.end is not None and msg.timestamp > self.end:
            return None
        return msg


class AuthorFilter(MessageTransformer):
    def __init__(self, authors: list[str], mode: str = "include"):
        if mode not in {"include", "exclude"}:
            raise ValueError("mode deve essere 'include' o 'exclude'")
        self.authors = set(authors)
        self.mode = mode

    def apply(self, msg: Message) -> Message | None:
        present = msg.sender in self.authors
        keep = present if self.mode == "include" else not present
        return msg if keep else None


class SystemMessageFilter(MessageTransformer):
    def apply(self, msg: Message) -> Message | None:
        return None if msg.type == MessageType.SYSTEM else msg
