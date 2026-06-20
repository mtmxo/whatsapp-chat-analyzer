from datetime import datetime

import whatsapp_analyzer as wa
from whatsapp_analyzer import (
    ActivityReport,
    ChatStatistics,
    ContentReport,
    Chat,
)
from whatsapp_analyzer.models import Message, MessageType


def _chat():
    return Chat([
        Message(datetime(2024, 6, 12, 9, 0), "Mario", "hello world hello", MessageType.TEXT),
        Message(datetime(2024, 6, 12, 9, 1), "Luigi", "hi", MessageType.TEXT),
    ])


def test_chat_statistics_shortcut():
    stats = _chat().statistics()
    assert isinstance(stats, ChatStatistics)
    assert stats.message_count == 2


def test_chat_activity_shortcut():
    report = _chat().activity()
    assert isinstance(report, ActivityReport)
    assert report.by_hour[9] == 2


def test_chat_content_shortcut():
    report = _chat().content()
    assert isinstance(report, ContentReport)
    assert report.top_words(1) == [("hello", 2)]


def test_chat_content_accepts_stopwords():
    report = _chat().content(stopwords={"hello"})
    assert "hello" not in dict(report.top_words())


def test_public_exports_available():
    for name in ("StatisticsAnalyzer", "ActivityAnalyzer", "ContentAnalyzer",
                 "ChatStatistics", "UserStats", "ActivityReport", "ContentReport"):
        assert hasattr(wa, name)
