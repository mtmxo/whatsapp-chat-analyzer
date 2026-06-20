"""Exceptions raised by the parsing module."""


class ParseError(Exception):
    """Generic error while parsing a chat."""


class FormatDetectionError(ParseError):
    """No known format was recognized in the file."""
