import warnings
from datetime import datetime

from whatsapp_analyzer.config import ParserConfig
from whatsapp_analyzer.models import MessageType
from whatsapp_analyzer.parsing.parser import WhatsAppParser
from whatsapp_analyzer.transform.filters import SystemMessageFilter

ANDROID = "12/06/24, 21:34 - Mario: hello"


def parse(text, config=None):
    return WhatsAppParser(config or ParserConfig()).parse(text)


def test_parses_single_message():
    chat = parse(ANDROID)
    assert len(chat) == 1
    msg = chat[0]
    assert msg.sender == "Mario"
    assert msg.text == "hello"
    assert msg.type == MessageType.TEXT
    assert msg.timestamp == datetime(2024, 6, 12, 21, 34)


def test_parses_multiline_message():
    text = "12/06/24, 21:34 - Mario: first line\nsecond line\nthird line"
    chat = parse(text)
    assert len(chat) == 1
    assert chat[0].text == "first line\nsecond line\nthird line"


def test_system_message_has_none_sender():
    text = "12/06/24, 21:34 - Messages are encrypted with end-to-end encryption"
    chat = parse(text)
    assert chat[0].sender is None
    assert chat[0].type == MessageType.SYSTEM


def test_transformer_chain_drops_messages():
    text = (
        "12/06/24, 21:34 - Messages are encrypted\n"
        "12/06/24, 21:35 - Mario: hello"
    )
    cfg = ParserConfig(transformers=[SystemMessageFilter()])
    chat = parse(text, cfg)
    assert len(chat) == 1
    assert chat[0].sender == "Mario"


def test_max_lines_safeguard_emits_warning():
    body = "\n".join(["line"] * 10)
    text = f"12/06/24, 21:34 - Mario: start\n{body}"
    cfg = ParserConfig(max_lines_per_message=3)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        chat = parse(text, cfg)
    assert any("max_lines_per_message" in str(w.message) for w in caught)
    # the message is truncated to 3 total lines (header + 2 continuations)
    assert chat[0].text.count("\n") == 2


def test_ios_format_parsed():
    chat = parse("[12/06/2024, 21:34:05] Mario: hello")
    assert chat[0].sender == "Mario"
    assert chat[0].timestamp == datetime(2024, 6, 12, 21, 34, 5)
