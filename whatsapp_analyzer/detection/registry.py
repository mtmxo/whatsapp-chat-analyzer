"""Registry dei detector + costruzione del datetime_format dal campione."""

from __future__ import annotations

import re
from dataclasses import replace

from ..exceptions import FormatDetectionError
from .android import AndroidFormatDetector
from .base import ChatFormat, FormatDetector
from .ios import IosFormatDetector


class DetectorRegistry:
    def __init__(self, detectors: list[FormatDetector] | None = None, locale: str = "it"):
        self.detectors = detectors or [IosFormatDetector(), AndroidFormatDetector()]
        self.locale = locale

    def detect(self, sample_lines: list[str]) -> ChatFormat:
        for detector in self.detectors:
            fmt = detector.detect(sample_lines)
            if fmt is not None:
                return replace(fmt, datetime_format=self._build_datetime_format(fmt, sample_lines))
        raise FormatDetectionError(
            "Nessun formato WhatsApp conosciuto riconosciuto nel file."
        )

    def _build_datetime_format(self, fmt: ChatFormat, sample_lines: list[str]) -> str:
        dates, times = [], []
        for line in sample_lines:
            m = fmt.header_regex.match(line)
            if m:
                dates.append(m.group("date"))
                times.append(m.group("time"))

        day_first = self._is_day_first(dates)
        year_token = "%Y" if self._year_has_4_digits(dates) else "%y"
        date_part = f"%d/%m/{year_token}" if day_first else f"%m/%d/{year_token}"

        twelve_hour = self._is_twelve_hour(times)
        hour_token = "%I" if twelve_hour else "%H"
        time_part = f"{hour_token}:%M:%S" if self._has_seconds(times) else f"{hour_token}:%M"
        if twelve_hour:
            time_part += " %p"
        return f"{date_part}, {time_part}"

    def _is_day_first(self, dates: list[str]) -> bool:
        # Si guarda quale delle prime due posizioni contiene un valore > 12:
        # quella è obbligatoriamente il giorno. Se nessuna lo è, il dato è ambiguo
        # e si ricade sul default del locale (it/eu = giorno per primo).
        for date in dates:
            first, second, *_ = date.split("/")
            if int(first) > 12:
                return True
            if int(second) > 12:
                return False
        return self.locale.lower() not in {"us", "en_us"}

    def _year_has_4_digits(self, dates: list[str]) -> bool:
        return any(len(date.split("/")[2]) == 4 for date in dates)

    def _is_twelve_hour(self, times: list[str]) -> bool:
        return any(re.search(r"[APap][Mm]", t) for t in times)

    def _has_seconds(self, times: list[str]) -> bool:
        # si conta solo la parte numerica, ignorando l'eventuale suffisso AM/PM
        return any(t.split()[0].count(":") == 2 for t in times)
