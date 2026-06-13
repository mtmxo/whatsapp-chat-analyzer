# Changelog

Tutte le modifiche rilevanti al progetto sono documentate in questo file.

Il formato si ispira a [Keep a Changelog](https://keepachangelog.com/it/1.1.0/)
e il progetto adotta il [versionamento semantico](https://semver.org/lang/it/).

## [0.1.1] - 2026-06-13

### Aggiunto
- File `LICENSE` (MIT).
- Workflow di CI che esegue i test su Python 3.10, 3.11 e 3.12.
- Metadati di packaging: classifiers e URL del progetto in `pyproject.toml`.
- `CONTRIBUTING.md` e `CHANGELOG.md`.
- Badge nel README.

## [0.1.0] - 2026-06-13

### Aggiunto
- Parser a due fasi con riconoscimento automatico del formato (iOS e Android).
- Disambiguazione delle date `DD/MM` vs `MM/DD` e supporto orario 12h con AM/PM.
- Modelli dati immutabili `Message` e `Chat`, con tipi `TEXT`/`MEDIA`/`SYSTEM`/`DELETED`.
- Classificatore multilingua (italiano e inglese) per media, messaggi di sistema ed eliminati.
- Trasformazioni in fase di parsing: filtri per data/autore/sistema e anonimizzazione dei nomi.
- Export verso JSON (con round-trip), CSV e `pandas.DataFrame`.
- CLI `wa-analyzer` per parsing ed export.

[0.1.1]: https://github.com/mtmxo/whatsapp-chat-analyzer/releases/tag/v0.1.1
[0.1.0]: https://github.com/mtmxo/whatsapp-chat-analyzer/releases/tag/v0.1.0
