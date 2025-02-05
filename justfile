
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
  echo "Running Python tests..."
  cd python && uv run pytest || cd ..

# Python tests with filters
run-some-tests-py FILTER:
  echo "Running Python tests with filter {{FILTER}}..."
  cd python && uv run pytest -- -k {{FILTER}} || cd ..

# TypeScript tests
run-tests-ts:
  echo "Running TypeScript tests..."
  cd js && deno test || cd ..


# Typescript tests with filters
run-some-tests-ts FILTER:
  echo "Running TypeScript tests with filter {{FILTER}}..."
  cd js && deno test --filter {{FILTER}} || cd ..

# Rust tests
run-tests-rust:
  echo "Running Rust tests..."
  cd rust && cargo test || cd ..

# Rust tests with filters
run-some-tests-rust FILTER:
  echo "Placeholder: Running Rust tests with filter {{FILTER}}..."

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
