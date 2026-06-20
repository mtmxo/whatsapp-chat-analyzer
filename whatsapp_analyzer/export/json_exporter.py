"""JSON export/import with an explicit schema, for round-tripping."""

from __future__ import annotations

import json
from datetime import datetime

from ..models import Chat, MediaKind, Message, MessageType
from .base import Exporter


class JsonExporter(Exporter):
    def export(self, chat: Chat) -> str:
        return json.dumps([self._encode(m) for m in chat], ensure_ascii=False, indent=2)

    def load(self, data: str) -> Chat:
        return Chat([self._decode(item) for item in json.loads(data)])

    def _encode(self, msg: Message) -> dict:
        return {
            "timestamp": msg.timestamp.isoformat(),
            "sender": msg.sender,
            "text": msg.text,
            "type": msg.type.value,
            "media_kind": msg.media_kind.value if msg.media_kind else None,
        }

    def _decode(self, item: dict) -> Message:
        media = item["media_kind"]
        return Message(
            timestamp=datetime.fromisoformat(item["timestamp"]),
            sender=item["sender"],
            text=item["text"],
            type=MessageType(item["type"]),
            media_kind=MediaKind(media) if media else None,
        )
