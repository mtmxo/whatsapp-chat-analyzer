import pytest

from whatsapp_analyzer.exceptions import ParseError, FormatDetectionError


def test_format_detection_error_is_parse_error():
    # FormatDetectionError must be catchable as a generic ParseError
    assert issubclass(FormatDetectionError, ParseError)


def test_parse_error_message():
    err = ParseError("malformed line")
    assert str(err) == "malformed line"


from datetime import datetime

from whatsapp_analyzer.models import Chat, MediaKind, Message, MessageType


def _msg(sender, text, type_=MessageType.TEXT, ts=None, media_kind=None):
    return Message(
        timestamp=ts or datetime(2024, 6, 12, 21, 34),
        sender=sender,
        text=text,
        type=type_,
        media_kind=media_kind,
    )


def test_message_is_immutable():
    msg = _msg("Mario", "hello")
    with pytest.raises(Exception):
        msg.text = "changed"


def test_message_defaults_media_kind_none():
    assert _msg("Mario", "hello").media_kind is None


def test_chat_behaves_like_sequence():
    chat = Chat([_msg("Mario", "a"), _msg("Luigi", "b")])
    assert len(chat) == 2
    assert chat[0].sender == "Mario"
    assert [m.sender for m in chat] == ["Mario", "Luigi"]


def test_chat_participants_excludes_system_none():
    chat = Chat([
        _msg("Mario", "a"),
        _msg(None, "Messages are encrypted", MessageType.SYSTEM),
        _msg("Luigi", "b"),
    ])
    assert chat.participants == {"Mario", "Luigi"}


def test_chat_filter_returns_new_chat():
    chat = Chat([_msg("Mario", "a"), _msg("Luigi", "b")])
    filtered = chat.filter(lambda m: m.sender == "Mario")
    assert isinstance(filtered, Chat)
    assert len(filtered) == 1
    assert len(chat) == 2  # the original is unchanged
