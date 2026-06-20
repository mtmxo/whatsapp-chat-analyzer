"""Message type classification with Italian and English patterns."""

from __future__ import annotations

import re
from abc import ABC, abstractmethod

from ..models import MediaKind, MessageType


class MessageClassifier(ABC):
    @abstractmethod
    def classify(self, sender: str | None, text: str) -> tuple[MessageType, MediaKind | None]:
        """Determine the type (and optional media subtype) of a message."""


# "Deleted message" phrases in Italian and English. These strings must match the
# literal text WhatsApp writes, so the Italian keywords are intentional.
_DELETED = re.compile(
    r"questo messaggio è stato eliminato|hai eliminato questo messaggio"
    r"|this message was deleted|you deleted this message",
    re.IGNORECASE,
)

# Media lines look like "<kind> omess*/omitted". Order does not matter: we look
# for the subtype keyword inside the line already recognized as media.
_MEDIA = re.compile(r"omess\w+|omitted", re.IGNORECASE)

# Italian/English keywords WhatsApp uses for each media subtype.
_MEDIA_KINDS = {
    MediaKind.IMAGE: ("immagine", "image"),
    MediaKind.VIDEO: ("video",),
    MediaKind.AUDIO: ("audio",),
    MediaKind.STICKER: ("sticker", "adesivo"),
    MediaKind.GIF: ("gif",),
    MediaKind.DOCUMENT: ("documento", "document"),
}


class MultilingualClassifier(MessageClassifier):
    def classify(self, sender: str | None, text: str) -> tuple[MessageType, MediaKind | None]:
        if sender is None:
            return MessageType.SYSTEM, None
        stripped = text.strip().lstrip("‎")  # WhatsApp sometimes prepends an invisible LRM
        if _DELETED.search(stripped):
            return MessageType.DELETED, None
        if _MEDIA.search(stripped):
            return MessageType.MEDIA, self._media_kind(stripped)
        return MessageType.TEXT, None

    def _media_kind(self, text: str) -> MediaKind | None:
        lowered = text.lower()
        for kind, keywords in _MEDIA_KINDS.items():
            if any(kw in lowered for kw in keywords):
                return kind
        return None
