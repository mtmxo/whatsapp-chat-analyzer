"""Common abstraction for filters and transformations."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import Message


class MessageTransformer(ABC):
    @abstractmethod
    def apply(self, msg: Message) -> Message | None:
        """Return the (possibly modified) message, or None to drop it."""
