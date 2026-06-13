import pytest

from whatsapp_analyzer.exceptions import ParseError, FormatDetectionError


def test_format_detection_error_is_parse_error():
    # FormatDetectionError deve essere catturabile come ParseError generico
    assert issubclass(FormatDetectionError, ParseError)


def test_parse_error_message():
    err = ParseError("riga malformata")
    assert str(err) == "riga malformata"
