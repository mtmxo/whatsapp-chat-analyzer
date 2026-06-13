from pathlib import Path

from whatsapp_analyzer import Chat, ParserConfig, parse_file, parse_string

FIXTURES = Path(__file__).parent / "fixtures"


def test_parse_string_returns_chat():
    chat = parse_string("12/06/24, 21:35 - Mario: ciao")
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
