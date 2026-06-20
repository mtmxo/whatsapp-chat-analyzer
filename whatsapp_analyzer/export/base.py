"""Common abstraction for exporters."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import Chat


class Exporter(ABC):
    @abstractmethod
    def export(self, chat: Chat):
        """Serialize a Chat into the exporter's format."""
