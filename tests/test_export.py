import csv
import io
from datetime import datetime

import pytest

from whatsapp_analyzer.models import Chat, MediaKind, Message, MessageType


def _chat():
    return Chat([
        Message(datetime(2024, 6, 12, 21, 35), "Mario", "hello", MessageType.TEXT),
        Message(datetime(2024, 6, 12, 21, 36), None, "encrypted", MessageType.SYSTEM),
        Message(datetime(2024, 6, 12, 21, 37), "Luigi", "image omitted",
                MessageType.MEDIA, MediaKind.IMAGE),
    ])


def test_json_roundtrip():
    chat = _chat()
    restored = Chat.from_json(chat.to_json())
    assert restored.messages == chat.messages


def test_json_uses_iso_and_enum_names():
    payload = _chat().to_json()
    assert "2024-06-12T21:35:00" in payload
    assert "\"type\": \"text\"" in payload
    assert "\"media_kind\": \"image\"" in payload


def test_csv_has_header_and_rows():
    output = _chat().to_csv()
    rows = list(csv.reader(io.StringIO(output)))
    assert rows[0] == ["timestamp", "sender", "text", "type", "media_kind"]
    assert len(rows) == 4  # header + 3 messages


def test_dataframe_export():
    pd = pytest.importorskip("pandas")
    df = _chat().to_dataframe()
    assert list(df.columns) == ["timestamp", "sender", "text", "type", "media_kind"]
    assert len(df) == 3
