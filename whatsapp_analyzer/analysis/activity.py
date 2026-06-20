"""Temporal activity analysis: message volume over hours, weekdays and dates."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from datetime import date

from ..models import Chat
from .base import Analyzer


@dataclass(frozen=True)
class ActivityReport:
    by_hour: dict[int, int] = field(default_factory=dict)        # hour 0-23 -> count
    by_weekday: dict[int, int] = field(default_factory=dict)     # Monday 0 .. Sunday 6
    by_date: dict[date, int] = field(default_factory=dict)
    most_active_hour: int | None = None
    most_active_weekday: int | None = None


class ActivityAnalyzer(Analyzer):
    def analyze(self, chat: Chat) -> ActivityReport:
        by_hour: Counter[int] = Counter()
        by_weekday: Counter[int] = Counter()
        by_date: Counter[date] = Counter()
        for msg in chat:
            ts = msg.timestamp
            by_hour[ts.hour] += 1
            by_weekday[ts.weekday()] += 1
            by_date[ts.date()] += 1

        return ActivityReport(
            by_hour=dict(by_hour),
            by_weekday=dict(by_weekday),
            by_date=dict(by_date),
            most_active_hour=self._top_key(by_hour),
            most_active_weekday=self._top_key(by_weekday),
        )

    def _top_key(self, counter: Counter):
        # most_common returns ties in insertion order; good enough for a "peak" hint.
        return counter.most_common(1)[0][0] if counter else None
