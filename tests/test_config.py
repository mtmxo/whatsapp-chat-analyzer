from whatsapp_analyzer.config import ParserConfig


def test_defaults():
    cfg = ParserConfig()
    assert cfg.locale == "it"
    assert cfg.max_lines_per_message == 1000
    assert cfg.transformers == []
    assert cfg.chat_format is None
    assert cfg.detectors is None
    assert cfg.classifier is None


def test_transformers_default_is_independent():
    # default_factory evita la lista condivisa tra istanze
    a = ParserConfig()
    a.transformers.append("x")
    assert ParserConfig().transformers == []
