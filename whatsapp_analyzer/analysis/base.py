"""Common abstraction for analyzers."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import Chat


class Analyzer(ABC):
    @abstractmethod
    def analyze(self, chat: Chat):
        """Compute a report from a Chat."""
