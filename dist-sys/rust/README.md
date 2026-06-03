# Distributed Systems Rust

This workspace uses `cargo`.

## Create a new problem crate

```bash
cd dist-sys/rust
cargo new flyio/echo
```

After that, run:

```bash
cd dist-sys/rust
cargo test --manifest-path flyio/echo/Cargo.toml
```

## Layout

```text
flyio/
  echo/
  unique-ids/
  broadcast/
  grow-only-counter/
  kafka/
```

Use one crate per problem while things are still exploratory.
