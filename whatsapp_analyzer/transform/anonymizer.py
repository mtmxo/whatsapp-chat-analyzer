"""Anonymize only the sender field, with a consistent mapping across the chat."""

from __future__ import annotations

from dataclasses import replace

from ..models import Message
from .base import MessageTransformer


class Anonymizer(MessageTransformer):
    def __init__(self, prefix: str = "User"):
        self.prefix = prefix
        self._mapping: dict[str, str] = {}

    def apply(self, msg: Message) -> Message | None:
        if msg.sender is None:
            return msg
        alias = self._mapping.get(msg.sender)
        if alias is None:
            alias = f"{self.prefix}{len(self._mapping) + 1}"
            self._mapping[msg.sender] = alias
        return replace(msg, sender=alias)
