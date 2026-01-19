#!/usr/bin/env bash
set -euo pipefail

year=${1:-}
lang=${2:-}
file=${3:-}

if [[ -z "$year" || -z "$lang" ]]; then
  echo "Usage: scripts/run-solution.sh <year> <lang> [file]"
  exit 1
fi

if [[ "$year" == "2026" && ( "$lang" == "py" || "$lang" == "python" ) ]]; then
  # Run pytest for 2026 Python tests
  cd python && uv run pytest test/test_2026_*.py -v
elif [[ "$year" == "2026" && "$lang" == "rust" ]]; then
  if [[ -z "$file" ]]; then
    echo "Rust requires a file argument: just run 2026 rust <file>"
    exit 1
  fi
  mkdir -p rust/solutions/2026/.bin
  rustc "rust/solutions/2026/$file" -o rust/solutions/2026/.bin/solution
  rust/solutions/2026/.bin/solution
else
  echo "Unsupported combination. Use: just run 2026 py|python|rust [file]"
  exit 1
fi
