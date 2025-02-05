
# Use bash for all commands
set shell := ["bash", "-cu"]

# Run all tests (default runs all languages)
run-tests LANG="all":
  just run-tests-{{LANG}}

# Run tests with filters (default runs all languages)
run-some-tests FILTER LANG="all":
  just run-some-tests-{{LANG}} {{FILTER}}

# Python tests
run-tests-py:
  gum style --foreground 212 --background 17 --border double --align center --padding "1 4" "Running Python Tests 🐍"
  cd python && uv run pytest || cd ..

# Python tests with filters
run-some-tests-py FILTER:
  gum style --foreground 212 --background 17 --border double --align center --padding "1 4" "Running Python Tests 🐍 with filter {{FILTER}}"
  cd python && uv run pytest -- -k {{FILTER}} || cd ..

# TypeScript tests
run-tests-ts:
  gum style --foreground 212 --background 17 --border double --align center --padding "1 4" "Running Typescript Tests 🟨✨"
  cd js && deno test || cd ..


# Typescript tests with filters
run-some-tests-ts FILTER:
  gum style --foreground 212 --background 17 --border double --align center --padding "1 4" "Running Typescript Tests 🟨✨ with filter {{FILTER}}"
  cd js && deno test --filter {{FILTER}} || cd ..

# Rust tests
run-tests-rust:
  gum style --foreground 212 --background 17 --border double --align center --padding "1 4" "Running Rust Tests 🦀" 
  cd rust && cargo test || cd ..

# Rust tests with filters
run-some-tests-rust FILTER:
  gum style --foreground 212 --background 17 --border double --align center --padding "1 4" "Running Rust Tests 🦀 with filter {{FILTER}}"

# Run all languages (aggregated)
run-tests-all:
  just run-tests-py
  just run-tests-ts
  just run-tests-rust

# Run all language tests with filters
run-some-tests-all FILTER:
  just run-some-tests-py {{FILTER}}
  just run-some-tests-ts {{FILTER}}
  just run-some-tests-rust {{FILTER}}
