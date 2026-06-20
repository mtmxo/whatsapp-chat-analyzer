"""Centralized parser configuration and dependency-injection point."""

from __future__ import annotations

from dataclasses import dataclass, field

from .detection.base import ChatFormat, FormatDetector
from .parsing.classifier import MessageClassifier
from .transform.base import MessageTransformer


@dataclass
class ParserConfig:
    # override / detection
    chat_format: ChatFormat | None = None
    detectors: list[FormatDetector] | None = None
    locale: str = "it"

    # classification
    classifier: MessageClassifier | None = None

    # transformations (list order = order of application)
    transformers: list[MessageTransformer] = field(default_factory=list)

    # safeguards
    max_lines_per_message: int = 1000
