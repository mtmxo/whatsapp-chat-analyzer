from datetime import datetime

from whatsapp_analyzer.analysis.content import ContentAnalyzer, ContentReport
from whatsapp_analyzer.models import Chat, MediaKind, Message, MessageType


def _text(text, sender="Mario"):
    return Message(datetime(2024, 6, 12, 9, 0), sender, text, MessageType.TEXT)


def _chat():
    return Chat([
        _text("hi hi Mario"),
        _text("hi Luigi how are you"),
        Message(datetime(2024, 6, 12, 9, 1), None, "encrypted", MessageType.SYSTEM),
        Message(datetime(2024, 6, 12, 9, 2), "Mario", "image omitted",
                MessageType.MEDIA, MediaKind.IMAGE),
    ])


def test_analyze_returns_report():
    assert isinstance(ContentAnalyzer().analyze(_chat()), ContentReport)


def test_top_words_counts_text_only():
    report = ContentAnalyzer().analyze(_chat())
    # "hi" appears 3 times across TEXT messages; media/system text is ignored
    assert report.top_words(1) == [("hi", 3)]


def test_words_are_lowercased():
    report = ContentAnalyzer().analyze(Chat([_text("Hello HELLO hello")]))
    assert report.top_words(1) == [("hello", 3)]


def test_numbers_and_punctuation_are_ignored():
    report = ContentAnalyzer().analyze(Chat([_text("yes! yes, 2024 ok")]))
    counts = dict(report.top_words())
    assert counts == {"yes": 2, "ok": 1}


def test_stopwords_are_excluded():
    report = ContentAnalyzer(stopwords={"how", "are"}).analyze(_chat())
    words = dict(report.top_words())
    assert "how" not in words
    assert "are" not in words
    assert words["hi"] == 3


def test_emoji_counts():
    report = ContentAnalyzer().analyze(Chat([_text("ok 😀👍 nice 😀")]))
    assert report.emoji_counts["😀"] == 2
    assert report.emoji_counts["👍"] == 1
    assert report.top_emojis(1) == [("😀", 2)]


def test_emoji_do_not_pollute_words():
    report = ContentAnalyzer().analyze(Chat([_text("great 👍")]))
    assert dict(report.top_words()) == {"great": 1}


def test_empty_chat():
    report = ContentAnalyzer().analyze(Chat([]))
    assert report.top_words() == []
    assert report.emoji_counts == {}
