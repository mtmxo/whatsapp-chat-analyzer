# whatsapp-chat-analyzer

[![Test](https://github.com/mtmxo/whatsapp-chat-analyzer/actions/workflows/tests.yml/badge.svg)](https://github.com/mtmxo/whatsapp-chat-analyzer/actions/workflows/tests.yml)
[![PyPI](https://img.shields.io/pypi/v/whatsapp-chat-analyzer)](https://pypi.org/project/whatsapp-chat-analyzer/)
[![Python](https://img.shields.io/pypi/pyversions/whatsapp-chat-analyzer)](https://pypi.org/project/whatsapp-chat-analyzer/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Robust parser for WhatsApp chats exported as `.txt` files, with automatic format
detection, clean data models and export to JSON, CSV and pandas.

The library is meant to be used in two ways: as a **solid foundation** to build custom
analyses on top of (it hands you tidy Python objects), and as a **ready-to-use tool**
thanks to the exporters and a small CLI.

## Features

- **Automatic format detection**: iOS and Android, `DD/MM` or `MM/DD` dates, 2- or
  4-digit years, 24h or 12h time with AM/PM. The format can also be forced.
- **Typed messages**: every message is classified as `TEXT`, `MEDIA`, `SYSTEM` or
  `DELETED`, with media subtype detection (image, video, audio, ...). The patterns are
  multilingual (Italian and English).
- **Multi-line messages** handled correctly.
- **Parse-time transformations**: date/author/system filters and name anonymization.
- **Export**: JSON (with re-import for round-tripping), CSV and `pandas.DataFrame`.
- **CLI** `wa-analyzer` to convert a chat without writing code.
- **Zero required dependencies** (standard library only); `pandas` is optional.

## Installation

```bash
pip install whatsapp-chat-analyzer
```

For `pandas.DataFrame` export:

```bash
pip install whatsapp-chat-analyzer[pandas]
```

Requirements: Python 3.10+.

## Quick start

```python
from whatsapp_analyzer import parse_file

chat = parse_file("export.txt")

print(len(chat), "messages")
print("Participants:", chat.participants)

for msg in chat:
    print(msg.timestamp, msg.sender, "->", msg.text)
```

If you already have the content in memory (for example loaded from an upload):

```python
from whatsapp_analyzer import parse_string

chat = parse_string(chat_text)
```

## How to export a chat

Export it from your phone without media:
**Chat settings → More → Export chat → Without media**. You will get a `.txt` file.
The library automatically handles the utf-8 BOM that WhatsApp adds to some exports.

## The data models

### `Chat`

It behaves like a sequence of `Message` objects (supports `len()`, indexing and
iteration) and offers a few conveniences:

```python
chat.participants            # set of authors (system messages excluded)
chat.filter(predicate)       # new Chat with only the messages matching the predicate
chat.to_json()               # -> str (see the Export section)
chat.to_csv()                # -> str
chat.to_dataframe()          # -> pandas.DataFrame (requires the pandas extra)
Chat.from_json(data)         # rebuild a Chat from a JSON export
```

### `Message`

It is an **immutable** object (`frozen` dataclass) with these fields:

| Field | Type | Notes |
|-------|------|-------|
| `timestamp` | `datetime` | message date and time |
| `sender` | `str \| None` | `None` for system messages (no author) |
| `text` | `str` | message body (multi-line ones include the `\n`) |
| `type` | `MessageType` | `TEXT`, `MEDIA`, `SYSTEM`, `DELETED` |
| `media_kind` | `MediaKind \| None` | set only when `type == MEDIA` |

`MediaKind` can be `IMAGE`, `VIDEO`, `AUDIO`, `DOCUMENT`, `STICKER`, `GIF`.

```python
from whatsapp_analyzer import MessageType

text = [m for m in chat if m.type == MessageType.TEXT]
media = [m for m in chat if m.type == MessageType.MEDIA]
```

## Configuration

All options go through `ParserConfig`, which also acts as a *dependency injection*
point: if a field is left as `None`, the parser uses the default implementation.

```python
from whatsapp_analyzer import parse_file, ParserConfig

config = ParserConfig(
    locale="it",                 # tie-break for ambiguous dates (DD/MM vs MM/DD)
    max_lines_per_message=1000,  # safeguard against corrupted files
    transformers=[],             # filters/anonymization (see below)
)

chat = parse_file("export.txt", config=config)
```

Available fields:

- `chat_format`: force a specific format and skip automatic detection.
- `detectors`: list of custom `FormatDetector`s (default: iOS + Android).
- `locale`: used to disambiguate dates when the day is ≤ 12 in both positions. With
  `"us"`/`"en_us"` month-first is assumed, otherwise day-first.
- `classifier`: an alternative `MessageClassifier`.
- `transformers`: list of transformations applied in order (see below).
- `max_lines_per_message`: beyond this threshold a message is truncated and a warning is
  emitted (protects against corrupted exports where the header is no longer recognized).

### Forcing the format

If you have an export with a format the automatic detection does not catch, you can
describe it by hand:

```python
import re
from whatsapp_analyzer import parse_file, ParserConfig
from whatsapp_analyzer.detection.base import ChatFormat

fmt = ChatFormat(
    header_regex=re.compile(
        r"^(?P<date>\d{2}/\d{2}/\d{4}), (?P<time>\d{2}:\d{2}) - "
        r"(?:(?P<sender>[^:]+): )?(?P<text>.*)$"
    ),
    datetime_format="%d/%m/%Y, %H:%M",
)

chat = parse_file("export.txt", ParserConfig(chat_format=fmt))
```

## Filters and anonymization

`transformer`s are applied to every message in the order you put them in the list. Each
one can modify the message or drop it.

```python
from datetime import datetime
from whatsapp_analyzer import parse_file, ParserConfig
from whatsapp_analyzer.transform.filters import (
    DateRangeFilter, AuthorFilter, SystemMessageFilter,
)
from whatsapp_analyzer.transform.anonymizer import Anonymizer

config = ParserConfig(transformers=[
    SystemMessageFilter(),                       # drop system messages
    DateRangeFilter(start=datetime(2024, 1, 1)), # only from 2024 onwards
    AuthorFilter(["Mario"], mode="include"),     # only Mario's messages
    Anonymizer(),                                # Mario -> User1, Luigi -> User2, ...
])

chat = parse_file("export.txt", config=config)
```

Notes:

- **Order matters.** As a rule of thumb, filter first and anonymize last.
- `AuthorFilter` accepts `mode="include"` or `mode="exclude"`.
- `Anonymizer` replaces **only the `sender` field** with a stable alias for the whole
  chat; it does not touch the message text.

## Export

```python
chat = parse_file("export.txt")

# JSON (timestamps in ISO 8601, enums as strings)
json_text = chat.to_json()

# Round-trip: reload without re-parsing the .txt
from whatsapp_analyzer import Chat
chat2 = Chat.from_json(json_text)

# CSV (one row per message)
csv_text = chat.to_csv()

# pandas (requires the [pandas] extra)
df = chat.to_dataframe()
```

The CSV and DataFrame columns are: `timestamp`, `sender`, `text`, `type`, `media_kind`.

## CLI

After installation the `wa-analyzer` command is available:

```bash
# JSON to stdout
wa-analyzer export.txt --to json

# CSV to a file, dropping system messages and anonymizing authors
wa-analyzer export.txt --to csv --out chat.csv --no-system --anonymize
```

Options:

| Flag | Description |
|------|-------------|
| `--to {json,csv}` | export format (default: `json`) |
| `--out PATH` | output file (default: stdout) |
| `--anonymize` | replace author names |
| `--no-system` | drop system messages |

## Extending the library

The architecture is meant to be extended without touching the existing code:

- new format → implement a `FormatDetector` and pass it in `ParserConfig(detectors=...)`;
- new transformation → extend `MessageTransformer`;
- new export → extend `Exporter`.

Example of a custom transformer:

```python
from dataclasses import replace
from whatsapp_analyzer.models import Message
from whatsapp_analyzer.transform.base import MessageTransformer

class UppercaseTransformer(MessageTransformer):
    def apply(self, msg: Message) -> Message | None:
        return replace(msg, text=msg.text.upper())
```

## License

MIT.
