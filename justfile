
# Use bash for all commands (fail on errors and undefined vars)
set shell := ["bash", "-euo", "pipefail", "-c"]

# Run all tests (default runs all languages)
run-tests LANG="all":
  just run-tests-{{LANG}}

# Run tests with filters (default runs all languages)
run-some-tests FILTER LANG="all":
  just run-some-tests-{{LANG}} {{FILTER}}

# Run tests for a specific year and language: just run 2026 py
run YEAR LANG:
  just run-{{YEAR}}-{{LANG}}

# ============ Python ============

# Python tests
run-tests-py:
  gum style --foreground 212 --background 17 --border double --align center --padding "1 4" "Running Python Tests 🐍"
  cd python && uv run pytest

# Python tests with filters
run-some-tests-py FILTER:
  gum style --foreground 212 --background 17 --border double --align center --padding "1 4" "Running Python Tests 🐍 with filter {{FILTER}}"
  cd python && uv run pytest -k "{{FILTER}}"

# Run 2026 Python tests
run-2026-py:
  gum style --foreground 212 --background 17 --border double --align center --padding "1 4" "Running 2026 Python Tests 🐍"
  cd python && uv run pytest test/test_2026_*.py -v

# ============ TypeScript ============

# TypeScript tests (using vitest)
run-tests-js:
  gum style --foreground 212 --background 17 --border double --align center --padding "1 4" "Running TypeScript Tests 🟨"
  cd js && npm test

# TypeScript tests with filters
run-some-tests-js FILTER:
  gum style --foreground 212 --background 17 --border double --align center --padding "1 4" "Running TypeScript Tests 🟨 with filter {{FILTER}}"
  cd js && npx vitest run -t "{{FILTER}}"

# Run 2026 TypeScript tests
run-2026-js:
  gum style --foreground 212 --background 17 --border double --align center --padding "1 4" "Running 2026 TypeScript Tests 🟨"
  cd js && npx vitest run test/2026 -v

# ============ Rust ============

# Rust tests
run-tests-rust:
  gum style --foreground 212 --background 17 --border double --align center --padding "1 4" "Running Rust Tests 🦀"
  cd rust && cargo test

# Rust tests with filters
run-some-tests-rust FILTER:
  gum style --foreground 212 --background 17 --border double --align center --padding "1 4" "Running Rust Tests 🦀 with filter {{FILTER}}"
  cd rust && cargo test "{{FILTER}}"

# Run 2026 Rust tests
run-2026-rust:
  gum style --foreground 212 --background 17 --border double --align center --padding "1 4" "Running 2026 Rust Tests 🦀"
  cd rust && cargo test year_2026

# ============ All Languages ============

# Run all languages (aggregated)
run-tests-all:
  just run-tests-py
  just run-tests-js
  just run-tests-rust

# Run all language tests with filters
run-some-tests-all FILTER:
  just run-some-tests-py {{FILTER}}
  just run-some-tests-js {{FILTER}}
  just run-some-tests-rust {{FILTER}}

# Run 2026 tests for all languages
run-2026-all:
  just run-2026-py
  just run-2026-js
  just run-2026-rust

# ============ Progress Tracking ============

# Progress CLI - pass any args/subcommands directly
# Examples:
#   just progress                          # show DSA summary
#   just progress study                    # show study summary
#   just progress study book-add "Title"   # add a book
#   just progress mark 28 python solved    # mark exercise
#   just progress --help                   # see all commands
progress *ARGS:
  @cd scripts && uv run --project ../python python -m progress {{ARGS}}

# ============ Help ============

# Show usage tips for the progress CLI
cheat:
  @glow cheatsheet.md
