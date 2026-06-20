"""Per-user and overall statistics for a chat."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from ..models import Chat, MessageType
from .base import Analyzer


@dataclass(frozen=True)
class UserStats:
    sender: str
    message_count: int = 0
    word_count: int = 0
    char_count: int = 0
    media_count: int = 0
    deleted_count: int = 0


@dataclass(frozen=True)
class ChatStatistics:
    message_count: int = 0
    system_count: int = 0
    per_user: dict[str, UserStats] = field(default_factory=dict)
    first_timestamp: datetime | None = None
    last_timestamp: datetime | None = None


class StatisticsAnalyzer(Analyzer):
    def analyze(self, chat: Chat) -> ChatStatistics:
        # Accumulate plain counters per author, then freeze into UserStats.
        accumulators: dict[str, dict] = {}
        system_count = 0
        for msg in chat:
            if msg.sender is None:
                system_count += 1
                continue
            acc = accumulators.setdefault(
                msg.sender,
                {"messages": 0, "words": 0, "chars": 0, "media": 0, "deleted": 0},
            )
            acc["messages"] += 1
            if msg.type == MessageType.TEXT:
                acc["words"] += len(msg.text.split())
                acc["chars"] += len(msg.text)
            elif msg.type == MessageType.MEDIA:
                acc["media"] += 1
            elif msg.type == MessageType.DELETED:
                acc["deleted"] += 1

        per_user = {
            sender: UserStats(
                sender=sender,
                message_count=acc["messages"],
                word_count=acc["words"],
                char_count=acc["chars"],
                media_count=acc["media"],
                deleted_count=acc["deleted"],
            )
            for sender, acc in accumulators.items()
        }

        timestamps = [msg.timestamp for msg in chat]
        return ChatStatistics(
            message_count=len(chat),
            system_count=system_count,
            per_user=per_user,
            first_timestamp=min(timestamps) if timestamps else None,
            last_timestamp=max(timestamps) if timestamps else None,
        )
