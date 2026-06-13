import re

from whatsapp_analyzer.detection.base import ChatFormat, FormatDetector


def test_chatformat_is_frozen():
    fmt = ChatFormat(header_regex=re.compile("x"), datetime_format="%d/%m/%y")
    try:
        fmt.datetime_format = "altro"
        assert False, "ChatFormat dovrebbe essere immutabile"
    except Exception:
        pass


def test_format_detector_is_abstract():
    # non si deve poter istanziare l'ABC senza implementare detect()
    try:
        FormatDetector()
        assert False, "FormatDetector non deve essere istanziabile"
    except TypeError:
        pass


from whatsapp_analyzer.detection.android import AndroidFormatDetector
from whatsapp_analyzer.detection.ios import IosFormatDetector


def test_ios_detector_matches_ios_lines():
    lines = ["[12/06/24, 21:34:05] Mario: ciao"]
    fmt = IosFormatDetector().detect(lines)
    assert fmt is not None
    m = fmt.header_regex.match(lines[0])
    assert m.group("sender") == "Mario"
    assert m.group("text") == "ciao"


def test_ios_detector_rejects_android_lines():
    lines = ["12/06/24, 21:34 - Mario: ciao"]
    assert IosFormatDetector().detect(lines) is None


def test_android_detector_matches_android_lines():
    lines = ["12/06/24, 21:34 - Mario: ciao"]
    fmt = AndroidFormatDetector().detect(lines)
    assert fmt is not None
    m = fmt.header_regex.match(lines[0])
    assert m.group("sender") == "Mario"
    assert m.group("text") == "ciao"


def test_android_detector_rejects_ios_lines():
    lines = ["[12/06/24, 21:34:05] Mario: ciao"]
    assert AndroidFormatDetector().detect(lines) is None


def test_android_detector_matches_system_line_without_sender():
    # le righe di sistema non hanno "sender:" ma devono comunque far riconoscere il formato
    lines = ["12/06/24, 21:34 - I messaggi sono crittografati"]
    assert AndroidFormatDetector().detect(lines) is not None
