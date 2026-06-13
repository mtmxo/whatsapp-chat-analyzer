"""Eccezioni del modulo di parsing."""


class ParseError(Exception):
    """Errore generico durante il parsing di una chat."""


class FormatDetectionError(ParseError):
    """Nessun formato conosciuto riconosciuto nel file."""
