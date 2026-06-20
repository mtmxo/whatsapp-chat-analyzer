"""Abstractions for detecting the format of a chat."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Pattern


@dataclass(frozen=True)
class ChatFormat:
    """Describes how a chat's header line is structured."""

    header_regex: Pattern     # groups: date, time, sender, text
    datetime_format: str      # format for datetime.strptime


class FormatDetector(ABC):
    """Strategy: try to recognize a format from a sample of lines."""

    @abstractmethod
    def detect(self, sample_lines: list[str]) -> ChatFormat | None:
        """Return the ChatFormat if the sample matches, otherwise None."""
