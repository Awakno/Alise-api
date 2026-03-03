# Contributing

Thanks for your interest in contributing to Awlise.

## Development setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running checks

Build package artifacts locally:

```bash
python -m build
python -m twine check dist/*
```

## Pull requests

- Keep changes focused and small.
- Add or update tests when behavior changes.
- Ensure code stays consistent with the existing style.
