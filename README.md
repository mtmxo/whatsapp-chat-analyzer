# whatsapp-chat-analyzer

[![Test](https://github.com/mtmxo/whatsapp-chat-analyzer/actions/workflows/tests.yml/badge.svg)](https://github.com/mtmxo/whatsapp-chat-analyzer/actions/workflows/tests.yml)
[![PyPI](https://img.shields.io/pypi/v/whatsapp-chat-analyzer)](https://pypi.org/project/whatsapp-chat-analyzer/)
[![Python](https://img.shields.io/pypi/pyversions/whatsapp-chat-analyzer)](https://pypi.org/project/whatsapp-chat-analyzer/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Parser robusto per le chat WhatsApp esportate in formato `.txt`, con riconoscimento
automatico del formato, modelli dati puliti ed export verso JSON, CSV e pandas.

La libreria nasce per essere usata in due modi: come **base solida** su cui costruire
analisi personalizzate (ti restituisce oggetti Python ordinati) e come **strumento
pronto all'uso** grazie agli export e a una piccola CLI.

## Caratteristiche

- **Riconoscimento automatico del formato**: iOS e Android, date `DD/MM` o `MM/DD`,
  anno a 2 o 4 cifre, orario 24h oppure 12h con AM/PM. Il formato si può anche forzare.
- **Messaggi tipizzati**: ogni messaggio è classificato come `TEXT`, `MEDIA`, `SYSTEM`
  o `DELETED`, con riconoscimento del sottotipo media (immagine, video, audio, ...).
  I pattern sono multilingua (italiano e inglese).
- **Messaggi multi-linea** gestiti correttamente.
- **Trasformazioni in fase di parsing**: filtri per data/autore/sistema e
  anonimizzazione dei nomi.
- **Export**: JSON (con re-import per il round-trip), CSV e `pandas.DataFrame`.
- **CLI** `wa-analyzer` per convertire una chat senza scrivere codice.
- **Zero dipendenze obbligatorie** (solo standard library); `pandas` è opzionale.

## Installazione

```bash
pip install whatsapp-chat-analyzer
```

Per l'export verso `pandas.DataFrame`:

```bash
pip install whatsapp-chat-analyzer[pandas]
```

Requisiti: Python 3.10+.

## Uso rapido

```python
from whatsapp_analyzer import parse_file

chat = parse_file("export.txt")

print(len(chat), "messaggi")
print("Partecipanti:", chat.participants)

for msg in chat:
    print(msg.timestamp, msg.sender, "->", msg.text)
```

Se hai già il contenuto in memoria (ad esempio caricato da un upload):

```python
from whatsapp_analyzer import parse_string

chat = parse_string(testo_della_chat)
```

## Come esportare una chat

Esportala dal telefono senza i media:
**Impostazioni chat → Altro → Esporta chat → Senza file multimediali**. Otterrai un
file `.txt`. La libreria gestisce automaticamente il BOM utf-8 che WhatsApp aggiunge
ad alcuni export.

## I modelli dati

### `Chat`

Si comporta come una sequenza di `Message` (supporta `len()`, indicizzazione e
iterazione) e offre alcune comodità:

```python
chat.participants            # set degli autori (esclusi i messaggi di sistema)
chat.filter(predicate)       # nuova Chat con i soli messaggi che soddisfano il predicato
chat.to_json()               # -> str (vedi sezione Export)
chat.to_csv()                # -> str
chat.to_dataframe()          # -> pandas.DataFrame (richiede l'extra pandas)
Chat.from_json(data)         # ricostruisce una Chat da un export JSON
```

### `Message`

È un oggetto **immutabile** (`frozen` dataclass) con questi campi:

| Campo | Tipo | Note |
|-------|------|------|
| `timestamp` | `datetime` | data e ora del messaggio |
| `sender` | `str \| None` | `None` per i messaggi di sistema (senza autore) |
| `text` | `str` | corpo del messaggio (per i multi-linea include i `\n`) |
| `type` | `MessageType` | `TEXT`, `MEDIA`, `SYSTEM`, `DELETED` |
| `media_kind` | `MediaKind \| None` | valorizzato solo quando `type == MEDIA` |

`MediaKind` può valere `IMAGE`, `VIDEO`, `AUDIO`, `DOCUMENT`, `STICKER`, `GIF`.

```python
from whatsapp_analyzer import MessageType

testo = [m for m in chat if m.type == MessageType.TEXT]
media = [m for m in chat if m.type == MessageType.MEDIA]
```

## Configurazione

Tutte le opzioni passano da `ParserConfig`, che funge anche da punto di
*dependency injection*: se un campo è lasciato a `None`, il parser usa l'implementazione
di default.

```python
from whatsapp_analyzer import parse_file, ParserConfig

config = ParserConfig(
    locale="it",                 # tie-break per le date ambigue (DD/MM vs MM/DD)
    max_lines_per_message=1000,  # salvaguardia anti file corrotti
    transformers=[],             # filtri/anonimizzazione (vedi sotto)
)

chat = parse_file("export.txt", config=config)
```

Campi disponibili:

- `chat_format`: forza un formato specifico e salta il riconoscimento automatico.
- `detectors`: lista di `FormatDetector` personalizzati (default: iOS + Android).
- `locale`: usato per disambiguare le date quando il giorno è ≤ 12 in entrambe le
  posizioni. Con `"us"`/`"en_us"` si assume mese per primo, altrimenti giorno per primo.
- `classifier`: un `MessageClassifier` alternativo.
- `transformers`: lista di trasformazioni applicate in ordine (vedi sotto).
- `max_lines_per_message`: oltre questa soglia un messaggio viene troncato e viene
  emesso un warning (protegge da export corrotti dove l'header non viene più
  riconosciuto).

### Forzare il formato

Se hai un export con un formato che il riconoscimento automatico non prende, puoi
descriverlo a mano:

```python
import re
from whatsapp_analyzer import parse_file, ParserConfig
from whatsapp_analyzer.detection.base import ChatFormat

formato = ChatFormat(
    header_regex=re.compile(
        r"^(?P<date>\d{2}/\d{2}/\d{4}), (?P<time>\d{2}:\d{2}) - "
        r"(?:(?P<sender>[^:]+): )?(?P<text>.*)$"
    ),
    datetime_format="%d/%m/%Y, %H:%M",
)

chat = parse_file("export.txt", ParserConfig(chat_format=formato))
```

## Filtri e anonimizzazione

I `transformer` vengono applicati a ogni messaggio nell'ordine in cui li metti nella
lista. Ognuno può modificare il messaggio o scartarlo.

```python
from datetime import datetime
from whatsapp_analyzer import parse_file, ParserConfig
from whatsapp_analyzer.transform.filters import (
    DateRangeFilter, AuthorFilter, SystemMessageFilter,
)
from whatsapp_analyzer.transform.anonymizer import Anonymizer

config = ParserConfig(transformers=[
    SystemMessageFilter(),                       # rimuove i messaggi di sistema
    DateRangeFilter(start=datetime(2024, 1, 1)), # solo dal 2024 in poi
    AuthorFilter(["Mario"], mode="include"),     # solo i messaggi di Mario
    Anonymizer(),                                # Mario -> User1, Luigi -> User2, ...
])

chat = parse_file("export.txt", config=config)
```

Note:

- **L'ordine conta.** Di norma conviene filtrare prima e anonimizzare per ultimo.
- `AuthorFilter` accetta `mode="include"` o `mode="exclude"`.
- `Anonymizer` sostituisce **solo il campo `sender`** con un alias stabile per tutta
  la chat; non tocca il testo dei messaggi.

## Export

```python
chat = parse_file("export.txt")

# JSON (timestamp in ISO 8601, enum come stringhe)
testo_json = chat.to_json()

# Round-trip: ricarica senza ri-parsare il .txt
from whatsapp_analyzer import Chat
chat2 = Chat.from_json(testo_json)

# CSV (una riga per messaggio)
testo_csv = chat.to_csv()

# pandas (richiede l'extra [pandas])
df = chat.to_dataframe()
```

Le colonne di CSV e DataFrame sono: `timestamp`, `sender`, `text`, `type`, `media_kind`.

## CLI

Dopo l'installazione è disponibile il comando `wa-analyzer`:

```bash
# JSON su stdout
wa-analyzer export.txt --to json

# CSV su file, escludendo i messaggi di sistema e anonimizzando gli autori
wa-analyzer export.txt --to csv --out chat.csv --no-system --anonymize
```

Opzioni:

| Flag | Descrizione |
|------|-------------|
| `--to {json,csv}` | formato di export (default: `json`) |
| `--out PATH` | file di output (default: stdout) |
| `--anonymize` | sostituisce i nomi degli autori |
| `--no-system` | esclude i messaggi di sistema |

## Estendere la libreria

L'architettura è pensata per essere estesa senza modificare il codice esistente:

- nuovo formato → implementa un `FormatDetector` e passalo in `ParserConfig(detectors=...)`;
- nuova trasformazione → estendi `MessageTransformer`;
- nuovo export → estendi `Exporter`.

Esempio di transformer personalizzato:

```python
from dataclasses import replace
from whatsapp_analyzer.models import Message
from whatsapp_analyzer.transform.base import MessageTransformer

class UppercaseTransformer(MessageTransformer):
    def apply(self, msg: Message) -> Message | None:
        return replace(msg, text=msg.text.upper())
```

## Licenza

MIT.
