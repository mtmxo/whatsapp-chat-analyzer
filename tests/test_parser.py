import warnings
from datetime import datetime

from whatsapp_analyzer.config import ParserConfig
from whatsapp_analyzer.models import MessageType
from whatsapp_analyzer.parsing.parser import WhatsAppParser
from whatsapp_analyzer.transform.filters import SystemMessageFilter

ANDROID = "12/06/24, 21:34 - Mario: ciao"


def parse(text, config=None):
    return WhatsAppParser(config or ParserConfig()).parse(text)


def test_parses_single_message():
    chat = parse(ANDROID)
    assert len(chat) == 1
    msg = chat[0]
    assert msg.sender == "Mario"
    assert msg.text == "ciao"
    assert msg.type == MessageType.TEXT
    assert msg.timestamp == datetime(2024, 6, 12, 21, 34)


def test_parses_multiline_message():
    text = "12/06/24, 21:34 - Mario: prima riga\nseconda riga\nterza riga"
    chat = parse(text)
    assert len(chat) == 1
    assert chat[0].text == "prima riga\nseconda riga\nterza riga"


def test_system_message_has_none_sender():
    text = "12/06/24, 21:34 - I messaggi sono crittografati con la crittografia end-to-end"
    chat = parse(text)
    assert chat[0].sender is None
    assert chat[0].type == MessageType.SYSTEM


def test_transformer_chain_drops_messages():
    text = (
        "12/06/24, 21:34 - I messaggi sono crittografati\n"
        "12/06/24, 21:35 - Mario: ciao"
    )
    cfg = ParserConfig(transformers=[SystemMessageFilter()])
    chat = parse(text, cfg)
    assert len(chat) == 1
    assert chat[0].sender == "Mario"


def test_max_lines_safeguard_emits_warning():
    body = "\n".join(["riga"] * 10)
    text = f"12/06/24, 21:34 - Mario: inizio\n{body}"
    cfg = ParserConfig(max_lines_per_message=3)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        chat = parse(text, cfg)
    assert any("max_lines_per_message" in str(w.message) for w in caught)
    # il messaggio viene troncato a 3 righe totali (header + 2 continuazioni)
    assert chat[0].text.count("\n") == 2


def test_ios_format_parsed():
    chat = parse("[12/06/2024, 21:34:05] Mario: ciao")
    assert chat[0].sender == "Mario"
    assert chat[0].timestamp == datetime(2024, 6, 12, 21, 34, 5)
