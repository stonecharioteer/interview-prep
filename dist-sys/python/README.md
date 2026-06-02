# Distributed Systems Python

This workspace uses `uv`.

## Setup

```bash
cd dist-sys/python
uv sync --group dev
```

## Layout

```text
flyio/
  echo/
  unique-ids/
  broadcast/
  grow-only-counter/
  kafka/

test/
```

## Running tests

```bash
cd dist-sys/python
uv run pytest
```

## Lint / format

```bash
cd dist-sys/python
uv run ruff check .
uv run ruff format .
```
