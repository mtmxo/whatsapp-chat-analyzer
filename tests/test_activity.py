from datetime import date, datetime

from whatsapp_analyzer.analysis.activity import ActivityAnalyzer, ActivityReport
from whatsapp_analyzer.models import Chat, Message, MessageType


def _msg(ts, sender="Mario"):
    return Message(ts, sender, "x", MessageType.TEXT)


def _chat():
    return Chat([
        _msg(datetime(2024, 6, 10, 9, 0)),    # Monday
        _msg(datetime(2024, 6, 10, 9, 30)),   # Monday, same hour
        _msg(datetime(2024, 6, 10, 22, 0)),   # Monday, late
        _msg(datetime(2024, 6, 11, 9, 15)),   # Tuesday
    ])


def test_analyze_returns_report():
    report = ActivityAnalyzer().analyze(_chat())
    assert isinstance(report, ActivityReport)


def test_by_hour_counts():
    report = ActivityAnalyzer().analyze(_chat())
    assert report.by_hour[9] == 3
    assert report.by_hour[22] == 1
    assert 0 not in report.by_hour  # empty hours are not present


def test_by_weekday_counts():
    report = ActivityAnalyzer().analyze(_chat())
    # weekday(): Monday == 0, Tuesday == 1
    assert report.by_weekday[0] == 3
    assert report.by_weekday[1] == 1


def test_by_date_counts():
    report = ActivityAnalyzer().analyze(_chat())
    assert report.by_date[date(2024, 6, 10)] == 3
    assert report.by_date[date(2024, 6, 11)] == 1


def test_most_active_hour_and_weekday():
    report = ActivityAnalyzer().analyze(_chat())
    assert report.most_active_hour == 9
    assert report.most_active_weekday == 0


def test_empty_chat():
    report = ActivityAnalyzer().analyze(Chat([]))
    assert report.by_hour == {}
    assert report.most_active_hour is None
    assert report.most_active_weekday is None
