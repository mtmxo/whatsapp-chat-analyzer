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
