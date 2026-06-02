# Distributed Systems Practice

This workspace is for distributed systems exercises, including Fly.io / Maelstrom work.

## Layout

- `python/` — Python workspace managed with `uv`
- `rust/` — Rust workspace managed with `cargo`
- `notes/` — notes, invariants, and experiment logs

## Suggested problem layout

Keep problems grouped by platform and named by problem, not by year.

```text
python/flyio/echo/
rust/flyio/echo/
```

Each problem directory can hold:

- implementation
- tests
- notes

## Getting started

Python:

```bash
cd dist-sys/python
uv sync --group dev
```

Rust:

```bash
cd dist-sys/rust
cargo new flyio/echo
```

Recommended first problems:

1. `echo`
2. `unique-ids`
3. `broadcast`
4. `grow-only-counter`
5. `kafka`
