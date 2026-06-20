# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and the project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed
- Translated the whole codebase, comments, docstrings, documentation and tests to
  English. Functional Italian strings (classifier keywords and the Italian sample
  fixtures) are kept on purpose to cover the multilingual parsing path.

## [0.1.1] - 2026-06-13

### Added
- `LICENSE` file (MIT).
- CI workflow running the test suite on Python 3.10, 3.11 and 3.12.
- Packaging metadata: classifiers and project URLs in `pyproject.toml`.
- `CONTRIBUTING.md` and `CHANGELOG.md`.
- Badges in the README.

## [0.1.0] - 2026-06-13

### Added
- Two-phase parser with automatic format detection (iOS and Android).
- `DD/MM` vs `MM/DD` date disambiguation and 12h time support with AM/PM.
- Immutable `Message` and `Chat` data models, with `TEXT`/`MEDIA`/`SYSTEM`/`DELETED` types.
- Multilingual classifier (Italian and English) for media, system and deleted messages.
- Parse-time transformations: date/author/system filters and name anonymization.
- Export to JSON (with round-trip), CSV and `pandas.DataFrame`.
- `wa-analyzer` CLI for parsing and export.

[0.1.1]: https://github.com/mtmxo/whatsapp-chat-analyzer/releases/tag/v0.1.1
[0.1.0]: https://github.com/mtmxo/whatsapp-chat-analyzer/releases/tag/v0.1.0
