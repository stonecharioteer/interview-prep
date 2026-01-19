
# Use bash for all commands (fail on errors and undefined vars)
set shell := ["bash", "-euo", "pipefail", "-c"]

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

# JavaScript tests
run-tests-js:
  gum style --foreground 212 --background 17 --border double --align center --padding "1 4" "Running JavaScript Tests 🟨✨"
  cd js && npm test || cd ..


# JavaScript tests with filters
run-some-tests-js FILTER:
  gum style --foreground 212 --background 17 --border double --align center --padding "1 4" "Running JavaScript Tests 🟨✨ with filter {{FILTER}}"
  cd js && node --test --test-name-pattern {{FILTER}} || cd ..

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
  just run-tests-js
  just run-tests-rust

# Run all language tests with filters
run-some-tests-all FILTER:
  just run-some-tests-py {{FILTER}}
  just run-some-tests-js {{FILTER}}
  just run-some-tests-rust {{FILTER}}

# Run 2026 Python tests via pytest
run-2026-py:
  cd python && uv run pytest test/test_2026_*.py -v

# Run a 2026 Rust solution script from repo root (compiled to a local bin dir)
run-2026-rust FILE:
  mkdir -p rust/solutions/2026/.bin
  rustc rust/solutions/2026/{{FILE}} -o rust/solutions/2026/.bin/solution
  rust/solutions/2026/.bin/solution

# Run a solution with: just run 2026 py (file optional for py, required for rust)
run YEAR LANG FILE="":
  scripts/run-solution.sh {{YEAR}} {{LANG}} {{FILE}}
