"""Export verso pandas.DataFrame. pandas è una dipendenza opzionale."""

from __future__ import annotations

from ..models import Chat
from .base import Exporter


class DataFrameExporter(Exporter):
    def export(self, chat: Chat):
        try:
            import pandas as pd
        except ImportError as exc:  # messaggio chiaro se l'extra non è installato
            raise ImportError(
                "L'export su DataFrame richiede pandas. "
                "Installa con: pip install whatsapp-chat-analyzer[pandas]"
            ) from exc
        return pd.DataFrame(
            {
                "timestamp": [m.timestamp for m in chat],
                "sender": [m.sender for m in chat],
                "text": [m.text for m in chat],
                "type": [m.type.value for m in chat],
                "media_kind": [m.media_kind.value if m.media_kind else None for m in chat],
            }
        )
