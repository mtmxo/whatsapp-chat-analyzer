# Contributing

Thanks for your interest in the project! Here is how to get started.

## Development environment

The project uses [uv](https://docs.astral.sh/uv/) to manage the environment and dependencies.

```bash
# clone the repo
git clone https://github.com/mtmxo/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer

# create the virtualenv and install the dev dependencies
uv venv
uv pip install -e ".[dev,pandas]"
```

## Running the tests

```bash
uv run pytest
```

The suite must stay green. Every new feature or fix should come with its own tests.

## Code style

- Follow the PEP 8 conventions.
- Code, comments and documentation are written in English, and comments only where the
  code is not self-explanatory. Functional Italian strings (classifier keywords and the
  Italian sample fixtures) are kept on purpose to cover the multilingual parsing path.
- The architecture follows the SOLID principles: to add a format, a filter or an
  exporter you extend the matching abstraction (`FormatDetector`,
  `MessageTransformer`, `Exporter`) without changing the existing code.

## Change workflow

1. Open an issue to discuss the change, if it is not trivial.
2. Create a dedicated branch.
3. Develop with TDD: test first, then implementation.
4. Make sure `uv run pytest` is green.
5. Open a pull request describing what changes and why.

## Reporting a bug

Open an [issue](https://github.com/mtmxo/whatsapp-chat-analyzer/issues) including, if
possible, a small (anonymized) chat snippet that reproduces the problem.
