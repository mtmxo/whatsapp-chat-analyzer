from datetime import datetime

from whatsapp_analyzer.models import Message, MessageType
from whatsapp_analyzer.transform.anonymizer import Anonymizer
from whatsapp_analyzer.transform.filters import (
    AuthorFilter,
    DateRangeFilter,
    SystemMessageFilter,
)


def _msg(sender, ts, type_=MessageType.TEXT):
    return Message(timestamp=ts, sender=sender, text="x", type=type_)


def test_date_range_filter_keeps_in_range():
    f = DateRangeFilter(start=datetime(2024, 1, 1), end=datetime(2024, 12, 31))
    assert f.apply(_msg("Mario", datetime(2024, 6, 1))) is not None


def test_date_range_filter_drops_out_of_range():
    f = DateRangeFilter(start=datetime(2024, 1, 1), end=datetime(2024, 12, 31))
    assert f.apply(_msg("Mario", datetime(2025, 1, 1))) is None


def test_author_filter_include():
    f = AuthorFilter(["Mario"], mode="include")
    assert f.apply(_msg("Mario", datetime(2024, 6, 1))) is not None
    assert f.apply(_msg("Luigi", datetime(2024, 6, 1))) is None


def test_author_filter_exclude():
    f = AuthorFilter(["Mario"], mode="exclude")
    assert f.apply(_msg("Mario", datetime(2024, 6, 1))) is None
    assert f.apply(_msg("Luigi", datetime(2024, 6, 1))) is not None


def test_system_message_filter_drops_system():
    f = SystemMessageFilter()
    assert f.apply(_msg(None, datetime(2024, 6, 1), MessageType.SYSTEM)) is None
    assert f.apply(_msg("Mario", datetime(2024, 6, 1))) is not None


def test_anonymizer_replaces_sender_consistently():
    anon = Anonymizer()
    m1 = anon.apply(_msg("Mario", datetime(2024, 6, 1)))
    m2 = anon.apply(_msg("Luigi", datetime(2024, 6, 1)))
    m3 = anon.apply(_msg("Mario", datetime(2024, 6, 2)))
    assert m1.sender == "User1"
    assert m2.sender == "User2"
    assert m3.sender == "User1"  # stessa mappatura per lo stesso autore


def test_anonymizer_leaves_system_sender_none():
    anon = Anonymizer()
    m = anon.apply(_msg(None, datetime(2024, 6, 1), MessageType.SYSTEM))
    assert m.sender is None


def test_anonymizer_does_not_touch_text():
    anon = Anonymizer()
    msg = Message(
        timestamp=datetime(2024, 6, 1), sender="Mario",
        text="ciao Mario", type=MessageType.TEXT,
    )
    assert anon.apply(msg).text == "ciao Mario"
