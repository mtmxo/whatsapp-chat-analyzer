"""Astrazione comune agli exporter."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import Chat


class Exporter(ABC):
    @abstractmethod
    def export(self, chat: Chat):
        """Serializza una Chat nel formato dell'exporter."""
