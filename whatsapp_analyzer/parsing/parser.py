"""Two-phase parser: detect the format, then parse the lines."""

from __future__ import annotations

import warnings
from dataclasses import dataclass, field
from datetime import datetime

from ..config import ParserConfig
from ..detection.registry import DetectorRegistry
from ..models import Chat, Message
from .classifier import MultilingualClassifier

# Number of header lines sampled for format detection.
_SAMPLE_SIZE = 50


@dataclass
class _RawMessage:
    """A raw message under construction, before classification and transformers."""

    timestamp: datetime
    sender: str | None
    lines: list[str] = field(default_factory=list)
    truncated: bool = False


class WhatsAppParser:
    def __init__(self, config: ParserConfig | None = None):
        self.config = config or ParserConfig()
        self.classifier = self.config.classifier or MultilingualClassifier()

    def parse(self, content: str) -> Chat:
        lines = content.splitlines()
        chat_format = self._resolve_format(lines)
        raw_messages = self._split_messages(lines, chat_format)
        messages = [self._finalize(raw, chat_format) for raw in raw_messages]
        messages = [m for m in (self._transform(m) for m in messages) if m is not None]
        return Chat(messages)

    def _resolve_format(self, lines: list[str]):
        if self.config.chat_format is not None:
            return self.config.chat_format
        registry = DetectorRegistry(
            detectors=self.config.detectors, locale=self.config.locale
        )
        return registry.detect(lines[:_SAMPLE_SIZE])

    def _split_messages(self, lines, chat_format) -> list[_RawMessage]:
        messages: list[_RawMessage] = []
        current: _RawMessage | None = None
        for line in lines:
            match = chat_format.header_regex.match(line)
            if match:
                # Normalize the space before AM/PM so it matches "%p"
                # (some exports write "9:36PM", others "9:36 PM").
                raw_time = match.group("time").upper().replace("AM", " AM").replace("PM", " PM")
                raw_time = " ".join(raw_time.split())
                current = _RawMessage(
                    timestamp=datetime.strptime(
                        f"{match.group('date')}, {raw_time}",
                        chat_format.datetime_format,
                    ),
                    sender=match.group("sender"),
                    lines=[match.group("text")],
                )
                messages.append(current)
            elif current is not None:
                # Continuation line: it belongs to the open message.
                # The safeguard prevents appending forever on corrupted files.
                if len(current.lines) >= self.config.max_lines_per_message:
                    if not current.truncated:
                        warnings.warn(
                            "Message truncated: exceeded max_lines_per_message "
                            f"({self.config.max_lines_per_message})."
                        )
                        current.truncated = True
                    continue
                current.lines.append(line)
        return messages

    def _finalize(self, raw: _RawMessage, chat_format) -> Message:
        text = "\n".join(raw.lines)
        msg_type, media_kind = self.classifier.classify(raw.sender, text)
        return Message(
            timestamp=raw.timestamp,
            sender=raw.sender,
            text=text,
            type=msg_type,
            media_kind=media_kind,
        )

    def _transform(self, msg: Message) -> Message | None:
        for transformer in self.config.transformers:
            msg = transformer.apply(msg)
            if msg is None:
                return None
        return msg
