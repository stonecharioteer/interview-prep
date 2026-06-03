# Fly.io / Maelstrom Problems

This folder uses a flat layout with a shared runtime entrypoint.

## Layout

```text
flyio/
  main.py
  test_echo.py
  test_unique_ids.py
  notes_echo.md
  notes_unique_ids.md
```

## Conventions

- `main.py` contains the Maelstrom node entrypoint and handlers.
- Keep tests near the Fly.io code in this folder.
- Keep notes per problem as separate markdown files.
- Extract shared helpers only when repetition becomes real.
