"""Astrazioni per la detection del formato di una chat."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Pattern


@dataclass(frozen=True)
class ChatFormat:
    """Descrive come è strutturata la riga-header di una chat."""

    header_regex: Pattern     # gruppi: data, ora, sender, text
    datetime_format: str      # formato per datetime.strptime


class FormatDetector(ABC):
    """Strategy: prova a riconoscere un formato da un campione di righe."""

    @abstractmethod
    def detect(self, sample_lines: list[str]) -> ChatFormat | None:
        """Ritorna il ChatFormat se il campione corrisponde, altrimenti None."""
