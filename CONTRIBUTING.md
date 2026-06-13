# Come contribuire

Grazie per l'interesse nel progetto! Ecco come muoverti.

## Ambiente di sviluppo

Il progetto usa [uv](https://docs.astral.sh/uv/) per gestire ambiente e dipendenze.

```bash
# clona il repo
git clone https://github.com/mtmxo/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer

# crea il virtualenv e installa le dipendenze di sviluppo
uv venv
uv pip install -e ".[dev,pandas]"
```

## Eseguire i test

```bash
uv run pytest
```

La suite deve restare verde. Ogni nuova funzionalità o correzione va accompagnata dai
relativi test.

## Stile del codice

- Si seguono le convenzioni PEP 8.
- I commenti vanno scritti in italiano e solo dove il codice non è auto-esplicativo.
- L'architettura segue i principi SOLID: per aggiungere un formato, un filtro o un
  exporter si estende l'astrazione corrispondente (`FormatDetector`,
  `MessageTransformer`, `Exporter`) senza modificare il codice esistente.

## Workflow per le modifiche

1. Apri una issue per discutere la modifica, se non banale.
2. Crea un branch dedicato.
3. Sviluppa in TDD: prima il test, poi l'implementazione.
4. Verifica che `uv run pytest` sia verde.
5. Apri una pull request descrivendo cosa cambia e perché.

## Segnalare un bug

Apri una [issue](https://github.com/mtmxo/whatsapp-chat-analyzer/issues) includendo,
se possibile, un piccolo estratto di chat che riproduce il problema (anonimizzato).
