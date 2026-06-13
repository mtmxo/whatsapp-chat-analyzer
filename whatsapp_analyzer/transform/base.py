"""Astrazione comune a filtri e trasformazioni."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import Message


class MessageTransformer(ABC):
    @abstractmethod
    def apply(self, msg: Message) -> Message | None:
        """Ritorna il messaggio (eventualmente modificato) o None per scartarlo."""
