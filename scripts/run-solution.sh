#!/usr/bin/env bash
set -euo pipefail

year=${1:-}
lang=${2:-}
file=${3:-}

if [[ -z "$year" || -z "$lang" || -z "$file" ]]; then
  echo "Usage: scripts/run-solution.sh <year> <lang> <file>"
  exit 1
fi

if [[ "$year" == "2026" && ( "$lang" == "py" || "$lang" == "python" ) ]]; then
  python "python/solutions/2026/$file"
elif [[ "$year" == "2026" && "$lang" == "rust" ]]; then
  mkdir -p rust/solutions/2026/.bin
  rustc "rust/solutions/2026/$file" -o rust/solutions/2026/.bin/solution
  rust/solutions/2026/.bin/solution
else
  echo "Unsupported combination. Use: just run 2026 py|python|rust <file>"
  exit 1
fi
