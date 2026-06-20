"""Export to pandas.DataFrame. pandas is an optional dependency."""

from __future__ import annotations

from ..models import Chat
from .base import Exporter


class DataFrameExporter(Exporter):
    def export(self, chat: Chat):
        try:
            import pandas as pd
        except ImportError as exc:  # clear message if the extra is not installed
            raise ImportError(
                "DataFrame export requires pandas. "
                "Install it with: pip install whatsapp-chat-analyzer[pandas]"
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
