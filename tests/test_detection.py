import re

from whatsapp_analyzer.detection.base import ChatFormat, FormatDetector


def test_chatformat_is_frozen():
    fmt = ChatFormat(header_regex=re.compile("x"), datetime_format="%d/%m/%y")
    try:
        fmt.datetime_format = "other"
        assert False, "ChatFormat should be immutable"
    except Exception:
        pass


def test_format_detector_is_abstract():
    # the ABC must not be instantiable without implementing detect()
    try:
        FormatDetector()
        assert False, "FormatDetector must not be instantiable"
    except TypeError:
        pass


from whatsapp_analyzer.detection.android import AndroidFormatDetector
from whatsapp_analyzer.detection.ios import IosFormatDetector


def test_ios_detector_matches_ios_lines():
    lines = ["[12/06/24, 21:34:05] Mario: hello"]
    fmt = IosFormatDetector().detect(lines)
    assert fmt is not None
    m = fmt.header_regex.match(lines[0])
    assert m.group("sender") == "Mario"
    assert m.group("text") == "hello"


def test_ios_detector_rejects_android_lines():
    lines = ["12/06/24, 21:34 - Mario: hello"]
    assert IosFormatDetector().detect(lines) is None


def test_android_detector_matches_android_lines():
    lines = ["12/06/24, 21:34 - Mario: hello"]
    fmt = AndroidFormatDetector().detect(lines)
    assert fmt is not None
    m = fmt.header_regex.match(lines[0])
    assert m.group("sender") == "Mario"
    assert m.group("text") == "hello"


def test_android_detector_rejects_ios_lines():
    lines = ["[12/06/24, 21:34:05] Mario: hello"]
    assert AndroidFormatDetector().detect(lines) is None


def test_android_detector_matches_system_line_without_sender():
    # system lines have no "sender:" but must still let the format be recognized
    lines = ["12/06/24, 21:34 - Messages are encrypted"]
    assert AndroidFormatDetector().detect(lines) is not None


import pytest

from whatsapp_analyzer.detection.registry import DetectorRegistry
from whatsapp_analyzer.exceptions import FormatDetectionError


def test_registry_detects_android():
    fmt = DetectorRegistry().detect(["12/06/24, 21:34 - Mario: hello"])
    assert fmt.datetime_format == "%d/%m/%y, %H:%M"


def test_registry_detects_ios_with_seconds_and_4digit_year():
    fmt = DetectorRegistry().detect(["[12/06/2024, 21:34:05] Mario: hello"])
    assert fmt.datetime_format == "%d/%m/%Y, %H:%M:%S"


def test_registry_disambiguates_month_first():
    # 13 in the second position => that position is the day => month first (MM/DD)
    fmt = DetectorRegistry().detect(["06/13/24, 21:34 - Mario: hello"])
    assert fmt.datetime_format == "%m/%d/%y, %H:%M"


def test_registry_ambiguous_uses_locale_default():
    # no value > 12: ambiguous. locale "it" => day first
    fmt = DetectorRegistry(locale="it").detect(["06/07/24, 21:34 - Mario: hello"])
    assert fmt.datetime_format == "%d/%m/%y, %H:%M"


def test_registry_raises_when_no_format():
    with pytest.raises(FormatDetectionError):
        DetectorRegistry().detect(["this is not a valid header"])
