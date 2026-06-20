from pathlib import Path

from whatsapp_analyzer import Chat, ParserConfig, parse_file, parse_string

FIXTURES = Path(__file__).parent / "fixtures"


def test_parse_string_returns_chat():
    chat = parse_string("12/06/24, 21:35 - Mario: hello")
    assert isinstance(chat, Chat)
    assert chat[0].sender == "Mario"


def test_parse_file_reads_fixture():
    chat = parse_file(FIXTURES / "android_it.txt")
    assert chat.participants == {"Mario", "Luigi"}
    assert chat[-1].text == "ciao Mario\ncome stai?"


def test_parse_file_accepts_config():
    cfg = ParserConfig(locale="it")
    chat = parse_file(FIXTURES / "android_it.txt", config=cfg)
    assert len(chat) == 3


def test_parse_ios_english_media():
    from datetime import datetime

    from whatsapp_analyzer.models import MediaKind, MessageType
    chat = parse_file(FIXTURES / "ios_en.txt")
    assert chat[0].sender == "John"
    # 9:34:05 PM in 12h format must become 21:34:05
    assert chat[0].timestamp == datetime(2024, 6, 12, 21, 34, 5)
    assert chat[-1].type == MessageType.MEDIA
    assert chat[-1].media_kind == MediaKind.IMAGE
