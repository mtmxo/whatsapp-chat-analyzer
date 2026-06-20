from datetime import datetime

from whatsapp_analyzer.analysis.statistics import (
    ChatStatistics,
    StatisticsAnalyzer,
    UserStats,
)
from whatsapp_analyzer.models import Chat, MediaKind, Message, MessageType


def _chat():
    return Chat([
        Message(datetime(2024, 6, 12, 9, 0), "Mario", "hello there friend", MessageType.TEXT),
        Message(datetime(2024, 6, 12, 9, 1), None, "encrypted", MessageType.SYSTEM),
        Message(datetime(2024, 6, 12, 9, 2), "Luigi", "hi", MessageType.TEXT),
        Message(datetime(2024, 6, 13, 10, 0), "Mario", "image omitted",
                MessageType.MEDIA, MediaKind.IMAGE),
        Message(datetime(2024, 6, 13, 10, 1), "Mario", "deleted", MessageType.DELETED),
    ])


def test_analyze_returns_chat_statistics():
    stats = StatisticsAnalyzer().analyze(_chat())
    assert isinstance(stats, ChatStatistics)


def test_total_and_system_counts():
    stats = StatisticsAnalyzer().analyze(_chat())
    assert stats.message_count == 5
    assert stats.system_count == 1


def test_per_user_excludes_system():
    stats = StatisticsAnalyzer().analyze(_chat())
    assert set(stats.per_user) == {"Mario", "Luigi"}


def test_user_stats_counts():
    stats = StatisticsAnalyzer().analyze(_chat())
    mario = stats.per_user["Mario"]
    assert isinstance(mario, UserStats)
    assert mario.message_count == 3
    assert mario.media_count == 1
    assert mario.deleted_count == 1
    # word/char counts only consider TEXT messages
    assert mario.word_count == 3          # "hello there friend"
    assert mario.char_count == len("hello there friend")


def test_user_stats_word_count_luigi():
    stats = StatisticsAnalyzer().analyze(_chat())
    assert stats.per_user["Luigi"].word_count == 1


def test_first_and_last_timestamp():
    stats = StatisticsAnalyzer().analyze(_chat())
    assert stats.first_timestamp == datetime(2024, 6, 12, 9, 0)
    assert stats.last_timestamp == datetime(2024, 6, 13, 10, 1)


def test_empty_chat():
    stats = StatisticsAnalyzer().analyze(Chat([]))
    assert stats.message_count == 0
    assert stats.per_user == {}
    assert stats.first_timestamp is None
    assert stats.last_timestamp is None
