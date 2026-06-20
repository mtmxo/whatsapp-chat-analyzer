from whatsapp_analyzer.models import MediaKind, MessageType
from whatsapp_analyzer.parsing.classifier import MultilingualClassifier


def classify(text, sender="Mario"):
    return MultilingualClassifier().classify(sender, text)


def test_plain_text():
    assert classify("hello how are you") == (MessageType.TEXT, None)


def test_system_message_has_no_sender():
    # sender None => system message, regardless of the text
    assert classify("Mario added Luigi", sender=None) == (MessageType.SYSTEM, None)


def test_deleted_italian():
    assert classify("Questo messaggio è stato eliminato") == (MessageType.DELETED, None)


def test_deleted_english():
    assert classify("This message was deleted") == (MessageType.DELETED, None)


def test_media_omitted_italian():
    type_, kind = classify("‎<Media omessi>")
    assert type_ == MessageType.MEDIA


def test_media_image_english():
    type_, kind = classify("image omitted")
    assert (type_, kind) == (MessageType.MEDIA, MediaKind.IMAGE)


def test_media_audio_italian():
    type_, kind = classify("audio omesso")
    assert (type_, kind) == (MessageType.MEDIA, MediaKind.AUDIO)
