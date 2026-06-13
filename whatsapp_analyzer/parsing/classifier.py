"""Classificazione del tipo di messaggio con pattern in italiano e inglese."""

from __future__ import annotations

import re
from abc import ABC, abstractmethod

from ..models import MediaKind, MessageType


class MessageClassifier(ABC):
    @abstractmethod
    def classify(self, sender: str | None, text: str) -> tuple[MessageType, MediaKind | None]:
        """Determina il tipo (e l'eventuale sottotipo media) di un messaggio."""


# Frasi di "messaggio eliminato" in italiano e inglese.
_DELETED = re.compile(
    r"questo messaggio è stato eliminato|hai eliminato questo messaggio"
    r"|this message was deleted|you deleted this message",
    re.IGNORECASE,
)

# Le righe media hanno forma "<tipo> omess*/omitted". L'ordine non conta:
# si cerca la keyword del sottotipo dentro la riga riconosciuta come media.
_MEDIA = re.compile(r"omess\w+|omitted", re.IGNORECASE)

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
        stripped = text.strip().lstrip("‎")  # WhatsApp antepone a volte un LRM invisibile
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
