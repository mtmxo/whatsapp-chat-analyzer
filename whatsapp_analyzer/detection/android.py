"""Detector per il formato di export Android: data, ora - Sender: testo."""

from __future__ import annotations

import re

from .base import ChatFormat, FormatDetector

_ANDROID_HEADER = re.compile(
    r"^(?P<date>\d{1,2}/\d{1,2}/\d{2,4}), "
    r"(?P<time>\d{1,2}:\d{2}(?::\d{2})?(?:\s?[APap][Mm])?) - "
    r"(?:(?P<sender>[^:]+): )?(?P<text>.*)$"
)


class AndroidFormatDetector(FormatDetector):
    def detect(self, sample_lines: list[str]) -> ChatFormat | None:
        if any(_ANDROID_HEADER.match(line) for line in sample_lines):
            return ChatFormat(header_regex=_ANDROID_HEADER, datetime_format="")
        return None
