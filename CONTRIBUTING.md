# Contributing

This project uses standard Python tooling for formatting, linting, security checks, and tests.

## Setup

- Use Python 3.11+
- Create a virtual environment and install dev tools:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Formatting

- Format with Black and organize imports with isort:

```bash
black .
isort .
```

## Linting

- Run fast Ruff checks or Flake8:

```bash
ruff check .
# or
flake8
```

## Type checks

- Run mypy:

```bash
mypy .
```

## Security checks

- Run bandit:

```bash
bandit -r .
```

## Tests

- Use pytest:

```bash
pytest
```

## Notes

- Exclusions are configured for venv/.venv and Django migrations.
- Keep line length to 88 and follow Black formatting.
