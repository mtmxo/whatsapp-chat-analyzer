"""Flat CSV export, one row per message."""

from __future__ import annotations

import csv
import io

from ..models import Chat
from .base import Exporter

_FIELDS = ["timestamp", "sender", "text", "type", "media_kind"]


class CsvExporter(Exporter):
    def export(self, chat: Chat) -> str:
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(_FIELDS)
        for msg in chat:
            writer.writerow([
                msg.timestamp.isoformat(),
                msg.sender or "",
                msg.text,
                msg.type.value,
                msg.media_kind.value if msg.media_kind else "",
            ])
        return buffer.getvalue()
