"""Configurazione centralizzata del parser e punto di dependency injection."""

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

    # classificazione
    classifier: MessageClassifier | None = None

    # trasformazioni (ordine lista = ordine di applicazione)
    transformers: list[MessageTransformer] = field(default_factory=list)

    # salvaguardie
    max_lines_per_message: int = 1000
