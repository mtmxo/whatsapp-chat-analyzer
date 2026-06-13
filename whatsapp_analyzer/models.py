"""Modelli dati del parser: solo dati, nessuna logica di parsing."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Callable, Iterator


class MessageType(Enum):
    TEXT = "text"
    MEDIA = "media"
    SYSTEM = "system"      # join/leave, cambio gruppo, crittografia, ...
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
    sender: str | None        # None per i messaggi di sistema (senza autore)
    text: str
    type: MessageType
    media_kind: MediaKind | None = None   # valorizzato solo se type == MEDIA


class Chat:
    """Contenitore di messaggi che si comporta come una sequenza."""

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
